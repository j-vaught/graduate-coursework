# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.2,<3", "scipy>=1.15,<2", "pillow>=11,<14"]
# ///
"""Replay synchronized CANOE azimuth timing and navigation on fixed test points."""

import argparse
import csv
import hashlib
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from urllib.request import Request, urlopen

import numpy as np
from PIL import Image
from scipy.spatial import KDTree
from scipy.spatial.transform import Rotation, Slerp

from paired_experiment import inverse_plane

BUCKET = "https://canoe-data.s3.us-west-2.amazonaws.com/"
ROUTES = {"canoe-2025-08-21-19-16": 1000, "canoe-2025-08-28-14-50": 150}
SCANS_PER_ROUTE = 120
CALIBRATIONS = ("T_novatel_boat.txt", "T_boat_lidar.txt", "T_lidar_radar.txt")
TOLERANCE_M = 0.50
NAV_PADDING_US = 200_000
ECHO_MINIMUM_CODE = 100
ECHO_GRID_M = 2.0
ECHO_MINIMUM_SCANS = 30
ECHO_LAG_SCANS = 4
ECHO_MATCH_LIMIT_M = 1.5


def download(url: str, interval: tuple[int, int] | None = None) -> bytes:
    headers = {"Range": f"bytes={interval[0]}-{interval[1]}"} if interval else {}
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers=headers), timeout=30) as response:
                if interval and response.status != 206:
                    raise ValueError(f"Server ignored the byte range for {url}")
                return response.read()
        except OSError:
            if attempt == 2:
                raise
    raise RuntimeError(url)


def fetch_file(cache: Path, key: str) -> Path:
    path = cache / key
    if not path.is_file():
        path.parent.mkdir(parents=True, exist_ok=True)
        content = download(BUCKET + key)
        with NamedTemporaryFile(dir=path.parent, delete=False) as temporary:
            temporary.write(content)
        Path(temporary.name).replace(path)
    return path


def timestamp(line: bytes) -> int:
    return int(line.split(b",", 1)[0])


def fetch_navigation(cache: Path, route: str, first_us: int, last_us: int) -> Path:
    key = f"{route}/novatel/novatel_poses.csv"
    path = cache / route / "novatel" / "novatel_poses_clip.csv"
    if path.is_file():
        return path

    url = BUCKET + key
    with urlopen(Request(url, method="HEAD"), timeout=30) as response:
        size = int(response.headers["Content-Length"])
    header, first, *_ = download(url, (0, 8191)).splitlines()
    last = download(url, (size - 8192, size - 1)).splitlines()[-1]
    start_us = first_us - NAV_PADDING_US
    end_us = last_us + NAV_PADDING_US
    approximate_byte = int(
        (start_us - timestamp(first)) / (timestamp(last) - timestamp(first)) * (size - 8192)
    )
    for step in range(9):
        margin = 500_000 * 2**step
        start_byte = max(0, approximate_byte - margin)
        end_byte = min(size - 1, approximate_byte + margin + (end_us - start_us) // 2)
        lines = download(url, (start_byte, end_byte)).splitlines()[1:-1]
        if timestamp(lines[0]) <= start_us and timestamp(lines[-1]) >= end_us:
            clip = [line for line in lines if start_us - 1000 <= timestamp(line) <= end_us + 1000]
            path.write_bytes(b"\n".join([header, *clip]) + b"\n")
            return path
    raise ValueError(f"No bracketing navigation samples for {route}")


def load_poses(path: Path) -> np.ndarray:
    return np.loadtxt(path, delimiter=",", skiprows=1, usecols=range(7), ndmin=2)


def sensor_rotation(angles_rad: np.ndarray) -> Rotation:
    # The CANOE SDK uses passive principal rotations C1(x) C2(y) C3(z).
    return Rotation.from_euler("XYZ", -angles_rad)


def csv_output(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def manifest_row(path: Path, key: str, selection: str = "whole object") -> dict[str, Any]:
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {
        "public_source": BUCKET + key,
        "selection": selection,
        "local_bytes": path.stat().st_size,
        "local_sha256": digest,
    }


def persistent_echo_pairs(
    route: str,
    echoes: list[np.ndarray],
    centre_xy: np.ndarray,
    mid_times: np.ndarray,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    # Group and associate the same recorded returns using the arithmetic mean of the
    # two plotted positions so the matching rule is symmetric between the estimators.
    neutral = [echo.mean(axis=1) for echo in echoes]
    cells = [
        [tuple(cell) for cell in np.floor((points - centre_xy) / ECHO_GRID_M).astype(int)]
        for points in neutral
    ]
    persistence = Counter(cell for frame in cells for cell in set(frame))
    selected = [
        np.array([persistence[cell] >= ECHO_MINIMUM_SCANS for cell in frame], dtype=bool)
        for frame in cells
    ]
    echo_pairs: list[dict[str, Any]] = []
    matched_distances = []
    for first in range(len(echoes) - ECHO_LAG_SCANS):
        second = first + ECHO_LAG_SCANS
        a_index = np.flatnonzero(selected[first])
        b_index = np.flatnonzero(selected[second])
        a_points = neutral[first][a_index]
        b_points = neutral[second][b_index]
        if not len(a_points) or not len(b_points):
            continue

        distance, b_nearest = KDTree(b_points).query(a_points)
        _, a_nearest = KDTree(a_points).query(b_points)
        mutual = (a_nearest[b_nearest] == np.arange(len(a_points))) & (
            distance <= ECHO_MATCH_LIMIT_M
        )
        if not np.any(mutual):
            continue
        matched_a = echoes[first][a_index[mutual]]
        matched_b = echoes[second][b_index[b_nearest[mutual]]]
        error = np.linalg.norm(matched_a - matched_b, axis=2)
        matched_distances.append(error)
        echo_pairs.append(
            {
                "route": route,
                "first_scan_midpoint_utc_us": int(mid_times[first]),
                "second_scan_midpoint_utc_us": int(mid_times[second]),
                "matched_returns": len(error),
                "midpoint_pair_distance_p50_m": float(np.median(error[:, 0])),
                "spoke_time_pair_distance_p50_m": float(np.median(error[:, 1])),
                "midpoint_pair_distance_mean_m": float(np.mean(error[:, 0])),
                "spoke_time_pair_distance_mean_m": float(np.mean(error[:, 1])),
            }
        )

    distances = np.vstack(matched_distances)
    difference = distances[:, 0] - distances[:, 1]
    paired_means = np.array(
        [
            row["midpoint_pair_distance_mean_m"] - row["spoke_time_pair_distance_mean_m"]
            for row in echo_pairs
        ]
    )
    return echo_pairs, {
        "route": route,
        "retained_cells": sum(count >= ECHO_MINIMUM_SCANS for count in persistence.values()),
        "eligible_returns": sum(int(mask.sum()) for mask in selected),
        "scan_pairs": len(echo_pairs),
        "returns_matched": len(distances),
        "midpoint_median_m": float(np.median(distances[:, 0])),
        "spoke_time_median_m": float(np.median(distances[:, 1])),
        "midpoint_mean_m": float(np.mean(distances[:, 0])),
        "spoke_time_mean_m": float(np.mean(distances[:, 1])),
        "midpoint_p90_m": float(np.quantile(distances[:, 0], 0.90)),
        "spoke_time_p90_m": float(np.quantile(distances[:, 1], 0.90)),
        "fraction_individual_distance_smaller": float(np.mean(difference > 0)),
        "fraction_scan_pair_mean_smaller": float(np.mean(paired_means > 0)),
    }


def run_route(
    cache: Path,
    route: str,
    max_range_m: int,
) -> tuple[list[dict[str, Any]], ...]:
    radar_key = f"{route}/novatel/radar_poses.csv"
    radar_path = fetch_file(cache, radar_key)
    radar = load_poses(radar_path)
    middle = len(radar) // 2
    half = SCANS_PER_ROUTE // 2
    radar = radar[middle - half : middle + half]
    mid_times = radar[:, 0].astype(np.int64)
    assert len(radar) == SCANS_PER_ROUTE
    assert np.all(np.diff(mid_times) > 0)

    scans = [f"{route}/radar/{t}.png" for t in mid_times]
    calibration = [f"{route}/calib/{name}" for name in CALIBRATIONS]
    config_key = f"{route}/calib/radar_config.yaml"
    with ThreadPoolExecutor(12) as pool:
        files = list(
            pool.map(lambda key: fetch_file(cache, key), scans + calibration + [config_key])
        )
    scan_files = files[:SCANS_PER_ROUTE]
    radar_config = files[-1].read_text().splitlines()
    config = {
        line.split(":")[0]: line.split(":")[1].split("#")[0].strip()
        for line in radar_config
        if line.startswith(("encoder_size:", "range_gain:", "range_offset:"))
    }
    encoder_size = int(config["encoder_size"])
    assert any(line.strip() == f"{route}: {max_range_m}" for line in radar_config)

    nav_path = fetch_navigation(cache, route, int(mid_times[0]), int(mid_times[-1]))
    nav = load_poses(nav_path)
    assert np.all(np.diff(nav[:, 0]) == 1000)
    novatel_to_radar = np.eye(4)
    for path in files[SCANS_PER_ROUTE:-1]:
        novatel_to_radar = novatel_to_radar @ np.loadtxt(path)
    lever = novatel_to_radar[:3, 3]
    radar_to_nav_rotation = novatel_to_radar[:3, :3]
    reference_us = mid_times[0]
    nav_time = (nav[:, 0] - reference_us) * 1e-6
    interpolate_rotation = Slerp(nav_time, sensor_rotation(nav[:, 4:7]))

    def pose(utc_us: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        time = (utc_us - reference_us) * 1e-6
        assert time.min() >= nav_time[0] and time.max() <= nav_time[-1]
        orientation = interpolate_rotation(time).as_matrix()
        position = np.column_stack([np.interp(time, nav_time, nav[:, j]) for j in range(1, 4)])
        return position + orientation @ lever, orientation @ radar_to_nav_rotation

    mid_position, mid_rotation = pose(mid_times)
    published_rotation = sensor_rotation(radar[:, 4:7]).as_matrix()
    midpoint_position_check = np.linalg.norm(mid_position - radar[:, 1:4], axis=1)
    midpoint_angle_check = np.rad2deg(
        Rotation.from_matrix(mid_rotation @ published_rotation.transpose(0, 2, 1)).magnitude()
    )
    assert midpoint_position_check.max() < 0.001, midpoint_position_check.max()
    assert midpoint_angle_check.max() < 0.01, midpoint_angle_check.max()
    # The stored radar frame points down. The inverse geometry uses an up-pointing frame,
    # so rotate it about the radar x axis and reverse the measured azimuth in that frame.
    assert np.all(mid_rotation[:, 2, 2] < 0)
    to_upward = np.diag([1, -1, -1])

    bearing_deg = np.arange(0, 360, 45)
    bearings = np.deg2rad(bearing_deg)
    directions = np.column_stack((np.cos(bearings), np.sin(bearings), np.zeros(len(bearings))))
    centre = mid_position[half] - np.array([0, 0, 1])
    ranges = (30, 100)
    targets = np.vstack([centre + distance * directions for distance in ranges])
    target_index = np.arange(len(targets))
    visits: list[dict[str, Any]] = []
    echoes: list[np.ndarray] = []
    scan_start_us = []
    scan_end_us = []
    spoke_count = 0
    reversed_times = 0
    max_abs_spoke_delay_us = 0

    for scan_index, path in enumerate(scan_files):
        with Image.open(path) as image:
            data = np.asarray(image)
        utc = data[:, :8].copy().view("<i8").ravel()
        encoder = data[:, 8:10].copy().view("<u2").ravel()
        valid = data[:, 10] == 255
        assert len(utc) == 400
        assert abs(utc[len(utc) // 2 - 1] - mid_times[scan_index]) <= 1
        assert np.all(encoder < encoder_size) and np.any(valid)
        scan_start_us.append(utc.min())
        scan_end_us.append(utc.max())
        spoke_count += int(valid.sum())
        reversed_times += int(np.sum(np.diff(utc) < 0))
        max_abs_spoke_delay_us = max(
            max_abs_spoke_delay_us, int(np.max(np.abs(utc[valid] - mid_times[scan_index])))
        )
        azimuth = 2 * np.pi * encoder / encoder_size
        origin, rotation = pose(utc)

        amplitude = data[:, 11:]
        distance_bins = np.arange(amplitude.shape[1]) * max_range_m / amplitude.shape[1] * float(
            config["range_gain"]
        ) + float(config["range_offset"])
        gate = np.flatnonzero((distance_bins >= 20) & (distance_bins <= 110))
        peak_bin = gate[np.argmax(amplitude[:, gate], axis=1)]
        peak_code = amplitude[np.arange(len(utc)), peak_bin]
        echo_row = np.flatnonzero(valid & (peak_code >= ECHO_MINIMUM_CODE))
        plane_vector = distance_bins[peak_bin[echo_row], None] * np.column_stack(
            (np.cos(azimuth[echo_row]), np.sin(azimuth[echo_row]), np.zeros(len(echo_row)))
        )
        mid_enu = mid_position[scan_index] + plane_vector @ mid_rotation[scan_index].T
        spoke_enu = origin[echo_row] + np.einsum("sij,sj->si", rotation[echo_row], plane_vector)
        echoes.append(np.stack((mid_enu[:, :2], spoke_enu[:, :2]), axis=1))

        delta_world = targets[None, :, :] - origin[:, None, :]
        delta_body = np.einsum("sji,stj->sti", rotation, delta_world)
        bearing = np.arctan2(delta_body[:, :, 1], delta_body[:, :, 0])
        beam_offset = np.abs(np.angle(np.exp(1j * (bearing - azimuth[:, None]))))
        row = np.argmin(np.where(valid[:, None], beam_offset, np.inf), axis=0)
        assert np.max(beam_offset[row, target_index]) < np.deg2rad(1.0)
        slant = np.linalg.norm(delta_body[row, target_index], axis=1)
        assert np.max(slant) < max_range_m
        exact_bearing = -bearing[row, target_index]
        midpoint = inverse_plane(
            slant,
            exact_bearing,
            np.broadcast_to(mid_position[scan_index], origin[row].shape),
            np.broadcast_to(mid_rotation[scan_index] @ to_upward, rotation[row].shape),
            targets[:, 2],
        )
        deskewed = inverse_plane(
            slant, exact_bearing, origin[row], rotation[row] @ to_upward, targets[:, 2]
        )
        mid_error = np.linalg.norm(midpoint[:, :2] - targets[:, :2], axis=1)
        spoke_error = np.linalg.norm(deskewed[:, :2] - targets[:, :2], axis=1)
        assert np.max(spoke_error) < 1e-8

        for index, (beam_row, error_mid, error_spoke) in enumerate(
            zip(row, mid_error, spoke_error, strict=True)
        ):
            visits.append(
                {
                    "route": route,
                    "nominal_range_m": ranges[index // len(bearings)],
                    "test_point_enu_angle_deg": int(bearing_deg[index % len(bearings)]),
                    "scan_midpoint_utc_us": int(mid_times[scan_index]),
                    "spoke_utc_us": int(utc[beam_row]),
                    "spoke_index": int(beam_row),
                    "encoder_to_target_deg": round(
                        float(np.rad2deg(beam_offset[beam_row, index])), 6
                    ),
                    "midpoint_error_m": round(float(error_mid), 9),
                    "spoke_time_error_m": float(error_spoke),
                }
            )

    total_period = np.diff(mid_times) * 1e-6
    summary = []
    for distance in ranges:
        selected = [row for row in visits if row["nominal_range_m"] == distance]
        midpoint_errors = np.array([row["midpoint_error_m"] for row in selected])
        intervals = [
            np.diff(
                [row["spoke_utc_us"] for row in selected if row["test_point_enu_angle_deg"] == b]
            )
            for b in bearing_deg
        ]
        usable_intervals = [
            np.diff(
                [
                    row["spoke_utc_us"]
                    for row in selected
                    if row["test_point_enu_angle_deg"] == b
                    and row["midpoint_error_m"] <= TOLERANCE_M
                ]
            )
            for b in bearing_deg
        ]
        summary.append(
            {
                "route": route,
                "nominal_range_m": distance,
                "first_scan_midpoint_utc_us": int(mid_times[0]),
                "last_scan_midpoint_utc_us": int(mid_times[-1]),
                "scans": len(mid_times),
                "valid_spokes": spoke_count,
                "local_spoke_timestamp_reversals": reversed_times,
                "median_rotation_period_s": float(np.median(total_period)),
                "max_spoke_midpoint_delay_s": max_abs_spoke_delay_us * 1e-6,
                "scan_coverage_s": float((scan_end_us[-1] - scan_start_us[0]) * 1e-6),
                "visits": len(selected),
                "midpoint_error_p50_m": float(np.median(midpoint_errors)),
                "midpoint_error_p95_m": float(np.quantile(midpoint_errors, 0.95)),
                "midpoint_error_max_m": float(np.max(midpoint_errors)),
                "midpoint_over_0p50m": int(np.sum(midpoint_errors > TOLERANCE_M)),
                "spoke_time_error_max_m": max(row["spoke_time_error_m"] for row in selected),
                "spoke_revisit_max_s": float(np.max(intervals) * 1e-6),
                "midpoint_usable_revisit_max_s": float(
                    max(np.max(interval) for interval in usable_intervals) * 1e-6
                ),
                "radar_pose_check_max_m": float(midpoint_position_check.max()),
                "radar_pose_check_max_deg": float(midpoint_angle_check.max()),
            }
        )
    sources = [manifest_row(radar_path, radar_key)]
    sources.extend(
        manifest_row(path, key)
        for path, key in zip(files, scans + calibration + [config_key], strict=True)
    )
    sources.append(
        manifest_row(
            nav_path,
            f"{route}/novatel/novatel_poses.csv",
            f"UTC microseconds {int(nav[0, 0])} to {int(nav[-1, 0])}, newline normalized",
        )
    )
    echo_pairs, echo_summary = persistent_echo_pairs(route, echoes, centre[:2], mid_times)
    return visits, summary, sources, echo_pairs, [echo_summary]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cache", type=Path, help="cache for public radar scans and pose clips")
    parser.add_argument("output", type=Path, help="directory for the replay CSV files")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    results = [run_route(args.cache, route, max_range) for route, max_range in ROUTES.items()]
    for filename, rows_by_route in zip(
        (
            "canoe-registration-visits.csv",
            "canoe-registration-summary.csv",
            "canoe-inputs.csv",
            "canoe-echo-pairs.csv",
            "canoe-echo-summary.csv",
        ),
        zip(*results, strict=True),
        strict=True,
    ):
        csv_output(args.output / filename, [row for rows in rows_by_route for row in rows])


if __name__ == "__main__":
    main()
