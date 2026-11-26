# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.2,<3", "scipy>=1.15,<2", "pillow>=11,<14"]
# ///
"""Replay synchronized CANOE navigation and compare repeated radar returns."""

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
from scipy.stats import t as student_t

from paired_experiment import inverse_plane

BUCKET = "https://canoe-data.s3.us-west-2.amazonaws.com/"
ROUTES = {
    "canoe-2025-08-20-16-07": 1000,
    "canoe-2025-08-20-18-07": 1000,
    "canoe-2025-08-21-11-31": 1000,
    "canoe-2025-08-21-14-08": 1000,
    "canoe-2025-08-21-19-16": 1000,
    "canoe-2025-08-28-14-13": 150,
    "canoe-2025-08-28-14-50": 150,
    "canoe-2025-08-28-16-15": 1000,
}
VIRTUAL_REPLAY_ROUTES = {"canoe-2025-08-21-19-16", "canoe-2025-08-28-14-50"}
SCANS_PER_ROUTE = 120
CALIBRATIONS = ("T_novatel_boat.txt", "T_boat_lidar.txt", "T_lidar_radar.txt")
TOLERANCE_M = 0.50
NAV_PADDING_US = 200_000
ECHO_MINIMUM_CODE = 100
ECHO_GRID_M = 2.0
ECHO_MINIMUM_SCANS = 30
ECHO_LAG_SCANS = 4
MATCH_RULES = (("neutral", 1.5), ("neutral", 1.0), ("neutral", 2.0), ("agreement", 1.5))
DIAGNOSTIC_LAGS = (1, 4, 8)
RANGE_BANDS_METRES = ((20, 110), (20, 50), (50, 80), (80, 110))


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
        write_bytes_atomic(path, download(BUCKET + key))
    return path


def write_bytes_atomic(path: Path, content: bytes) -> None:
    with NamedTemporaryFile(dir=path.parent, delete=False) as temporary:
        temporary.write(content)
    Path(temporary.name).replace(path)


def timestamp(line: bytes) -> int:
    return int(line.split(b",", 1)[0])


def fetch_navigation(cache: Path, route: str, window: int, first_us: int, last_us: int) -> Path:
    key = f"{route}/novatel/novatel_poses.csv"
    suffix = "" if window == 50 else f"_{window}"
    path = cache / route / "novatel" / f"novatel_poses_clip{suffix}.csv"
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
            write_bytes_atomic(path, b"\n".join([header, *clip]) + b"\n")
            return path
    raise ValueError(f"No bracketing navigation samples for {route}")


def load_poses(path: Path) -> np.ndarray:
    return np.loadtxt(path, delimiter=",", skiprows=1, usecols=range(7), ndmin=2)


def sensor_rotation(angles_rad: np.ndarray) -> Rotation:
    # The CANOE SDK uses passive principal rotations C1(x) C2(y) C3(z).
    return Rotation.from_euler("XYZ", -angles_rad)


def csv_output(path: Path, rows: list[dict[str, Any]]) -> None:
    with NamedTemporaryFile(dir=path.parent, mode="w", newline="", delete=False) as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    Path(stream.name).replace(path)


def manifest_row(path: Path, key: str, selection: str = "whole object") -> dict[str, Any]:
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {
        "public_source": BUCKET + key,
        "selection": selection,
        "local_bytes": path.stat().st_size,
        "local_sha256": digest,
    }


def mutual_neighbors(
    a_points: np.ndarray, b_points: np.ndarray, limit: float
) -> tuple[np.ndarray, np.ndarray]:
    distance, b_nearest = KDTree(b_points).query(a_points)
    _, a_nearest = KDTree(a_points).query(b_points)
    mutual = (a_nearest[b_nearest] == np.arange(len(a_points))) & (distance <= limit)
    return b_nearest, mutual


def persistent_masks(
    echoes: list[np.ndarray], centre_xy: np.ndarray
) -> tuple[list[np.ndarray], int]:
    # Define eligibility from the mean of the plotted positions, which is unchanged
    # if the midpoint and spoke-time estimators exchange labels.
    neutral = [echo.mean(axis=1) for echo in echoes]
    cells = [
        [tuple(cell) for cell in np.floor((points - centre_xy) / ECHO_GRID_M).astype(int)]
        for points in neutral
    ]
    persistence = Counter(cell for frame in cells for cell in set(frame))
    masks = [
        np.array([persistence[cell] >= ECHO_MINIMUM_SCANS for cell in frame], dtype=bool)
        for frame in cells
    ]
    retained = sum(count >= ECHO_MINIMUM_SCANS for count in persistence.values())
    return masks, retained


def persistent_echo_pairs(
    route: str,
    window: int,
    echoes: list[np.ndarray],
    centre_xy: np.ndarray,
    mid_times: np.ndarray,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    masks, retained = persistent_masks(echoes, centre_xy)
    selected = [echo[mask] for echo, mask in zip(echoes, masks, strict=True)]
    pairs, windows = [], []
    for association, limit in MATCH_RULES:
        echo_pairs = []
        matched_distances = []
        for first in range(len(echoes) - ECHO_LAG_SCANS):
            second = first + ECHO_LAG_SCANS
            a, b = selected[first], selected[second]
            if len(a) == 0 or len(b) == 0:
                continue
            if association == "neutral":
                nearest, mutual = mutual_neighbors(a.mean(axis=1), b.mean(axis=1), limit)
            else:
                # A pair survives only when both estimators independently agree.
                nearest, mutual = mutual_neighbors(a[:, 0], b[:, 0], limit)
                alt_nearest, alt_mutual = mutual_neighbors(a[:, 1], b[:, 1], limit)
                mutual &= alt_mutual & (nearest == alt_nearest)
            if not np.any(mutual):
                continue
            error = np.linalg.norm(a[mutual] - b[nearest[mutual]], axis=2)
            matched_distances.append(error)
            echo_pairs.append(
                {
                    "route": route,
                    "window_percentile": window,
                    "association": association,
                    "association_gate_m": limit,
                    "first_scan_midpoint_utc_us": int(mid_times[first]),
                    "second_scan_midpoint_utc_us": int(mid_times[second]),
                    "matched_returns": len(error),
                    "midpoint_pair_distance_p50_m": float(np.median(error[:, 0])),
                    "spoke_time_pair_distance_p50_m": float(np.median(error[:, 1])),
                    "midpoint_pair_distance_mean_m": float(np.mean(error[:, 0])),
                    "spoke_time_pair_distance_mean_m": float(np.mean(error[:, 1])),
                }
            )
        pairs.extend(echo_pairs)
        distances = np.vstack(matched_distances) if matched_distances else np.empty((0, 2))
        difference = distances[:, 0] - distances[:, 1]
        paired_means = np.array(
            [
                float(row["midpoint_pair_distance_mean_m"])
                - float(row["spoke_time_pair_distance_mean_m"])
                for row in echo_pairs
            ]
        )
        median, mean, p90 = (np.full(2, np.nan) for _ in range(3))
        if len(distances):
            median, p90 = np.quantile(distances, [0.5, 0.9], axis=0)
            mean = distances.mean(axis=0)
        windows.append(
            {
                "route": route,
                "window_percentile": window,
                "association": association,
                "association_gate_m": limit,
                "first_scan_midpoint_utc_us": int(mid_times[0]),
                "last_scan_midpoint_utc_us": int(mid_times[-1]),
                "median_rotation_period_s": float(np.median(np.diff(mid_times)) * 1e-6),
                "max_lag_duration_s": float(
                    np.max(mid_times[ECHO_LAG_SCANS:] - mid_times[:-ECHO_LAG_SCANS]) * 1e-6
                ),
                "retained_cells": retained,
                "eligible_returns": sum(len(frame) for frame in selected),
                "scan_pairs": len(echo_pairs),
                "returns_matched": len(distances),
                "midpoint_median_m": float(median[0]),
                "spoke_time_median_m": float(median[1]),
                "midpoint_mean_m": float(mean[0]),
                "spoke_time_mean_m": float(mean[1]),
                "midpoint_p90_m": float(p90[0]),
                "spoke_time_p90_m": float(p90[1]),
                "fraction_individual_distance_smaller": float(np.mean(difference > 0))
                if len(difference)
                else np.nan,
                "fraction_scan_pair_mean_smaller": float(np.mean(paired_means > 0))
                if len(paired_means)
                else np.nan,
            }
        )
    return pairs, windows


def range_lag_diagnostics(
    route: str,
    window: int,
    echoes: list[np.ndarray],
    ranges: list[np.ndarray],
    spoke_times: list[np.ndarray],
    centre_xy: np.ndarray,
    mid_times: np.ndarray,
) -> list[dict[str, Any]]:
    """Use the same first scans and selection rules for every tested lag."""
    masks, _ = persistent_masks(echoes, centre_xy)
    selected = [echo[mask] for echo, mask in zip(echoes, masks, strict=True)]
    selected_ranges = [r[mask] for r, mask in zip(ranges, masks, strict=True)]
    selected_times = [t[mask] for t, mask in zip(spoke_times, masks, strict=True)]
    neutral = [echo.mean(axis=1) for echo in selected]
    anchor_count = len(mid_times) - max(DIAGNOSTIC_LAGS)
    outputs = []
    for lag in DIAGNOSTIC_LAGS:
        separation, pair_ranges, pair_times = [], [], []
        for first in range(anchor_count):
            second = first + lag
            if len(neutral[first]) == 0 or len(neutral[second]) == 0:
                continue
            nearest, mutual = mutual_neighbors(neutral[first], neutral[second], 1.5)
            if np.any(mutual):
                matches = nearest[mutual]
                separation.append(
                    np.linalg.norm(selected[first][mutual] - selected[second][matches], axis=2)
                )
                pair_ranges.append(
                    (selected_ranges[first][mutual] + selected_ranges[second][matches]) / 2
                )
                pair_times.append(
                    (selected_times[second][matches] - selected_times[first][mutual]) * 1e-6
                )
        distances = np.vstack(separation) if separation else np.empty((0, 2))
        distance_from_antenna = np.concatenate(pair_ranges) if pair_ranges else np.empty(0)
        elapsed = np.concatenate(pair_times) if pair_times else np.empty(0)
        lag_seconds = (mid_times[lag : lag + anchor_count] - mid_times[:anchor_count]) * 1e-6
        for low, high in RANGE_BANDS_METRES:
            eligible = (distance_from_antenna >= low) & (distance_from_antenna < high)
            measured = distances[eligible]
            p95, p99 = np.full((2, 2), np.nan)
            elapsed_median = np.nan
            elapsed_p95 = np.nan
            if len(measured):
                p95, p99 = np.quantile(measured, [0.95, 0.99], axis=0)
                elapsed_median, elapsed_p95 = np.quantile(elapsed[eligible], [0.50, 0.95])
            mean_reduction = (
                float(np.mean(measured[:, 0] - measured[:, 1])) if len(measured) else np.nan
            )
            outputs.append(
                {
                    "route": route,
                    "window_percentile": window,
                    "lag_rotations": lag,
                    "median_lag_s": float(np.median(lag_seconds)),
                    "anchor_scans": anchor_count,
                    "range_lower_inclusive_m": low,
                    "range_upper_exclusive_m": high,
                    "matched_returns": len(measured),
                    "matched_spoke_lag_median_s": float(elapsed_median),
                    "matched_spoke_lag_p95_s": float(elapsed_p95),
                    "mean_distance_reduction_m": mean_reduction,
                    "midpoint_distance_p95_m": float(p95[0]),
                    "spoke_time_distance_p95_m": float(p95[1]),
                    "midpoint_distance_p99_m": float(p99[0]),
                    "spoke_time_distance_p99_m": float(p99[1]),
                }
            )
    return outputs


def summarize_range_lag(diagnostics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Summarize mean and tail distances with equal window weights within each session."""
    rows = []
    for low, high in RANGE_BANDS_METRES:
        support = Counter(
            (row["route"], row["window_percentile"])
            for row in diagnostics
            if row["range_lower_inclusive_m"] == low
            and row["range_upper_exclusive_m"] == high
            and row["matched_returns"] > 0
        )
        common_windows = {
            window for window, count in support.items() if count == len(DIAGNOSTIC_LAGS)
        }
        for lag in DIAGNOSTIC_LAGS:
            subset = [
                row
                for row in diagnostics
                if row["lag_rotations"] == lag
                and row["range_lower_inclusive_m"] == low
                and row["range_upper_exclusive_m"] == high
                and (row["route"], row["window_percentile"]) in common_windows
            ]
            statistics = (
                "mean_distance_reduction_m",
                "midpoint_distance_p95_m",
                "spoke_time_distance_p95_m",
                "midpoint_distance_p99_m",
                "spoke_time_distance_p99_m",
            )
            route_values = {
                route: [[row[key] for key in statistics] for row in subset if row["route"] == route]
                for route in ROUTES
            }
            route_means = [np.mean(values, axis=0) for values in route_values.values() if values]
            averages = np.mean(route_means, axis=0)
            rows.append(
                {
                    "lag_rotations": lag,
                    "range_lower_inclusive_m": low,
                    "range_upper_exclusive_m": high,
                    "sessions": len(route_means),
                    "windows": len(subset),
                    "matched_returns": sum(row["matched_returns"] for row in subset),
                    **dict(zip(statistics, averages, strict=True)),
                }
            )
    return rows


def echo_intervals(
    windows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Pair within windows, weight windows equally, and cluster by session or date."""
    sessions, intervals = [], []
    for association, limit in MATCH_RULES:
        matched = [
            row
            for row in windows
            if row["association"] == association
            and row["association_gate_m"] == limit
            and row["returns_matched"] > 0
        ]
        session_means = {}
        for route in ROUTES:
            members = [row for row in matched if row["route"] == route]
            if not members:
                continue
            change = np.array([r["midpoint_mean_m"] - r["spoke_time_mean_m"] for r in members])
            session_means[route] = float(change.mean())
            sessions.append(
                {
                    "route": route,
                    "association": association,
                    "association_gate_m": limit,
                    "windows": len(members),
                    "matched_returns": sum(r["returns_matched"] for r in members),
                    "mean_distance_reduction_m": float(change.mean()),
                    "min_window_mean_distance_reduction_m": float(change.min()),
                    "max_window_mean_distance_reduction_m": float(change.max()),
                }
            )
        days = {route.removeprefix("canoe-")[:10] for route in session_means}
        day_means = [
            float(np.mean([value for route, value in session_means.items() if day in route]))
            for day in sorted(days)
        ]
        for cluster, means in (("session", list(session_means.values())), ("date", day_means)):
            n = len(means)
            average = float(np.mean(means))
            half_width = float(student_t.ppf(0.975, n - 1) * np.std(means, ddof=1) / np.sqrt(n))
            intervals.append(
                {
                    "association": association,
                    "association_gate_m": limit,
                    "cluster": cluster,
                    "clusters": n,
                    "windows": len(matched),
                    "matched_returns": sum(row["returns_matched"] for row in matched),
                    "mean_distance_reduction_m": average,
                    "ci95_low_m": average - half_width,
                    "ci95_high_m": average + half_width,
                    "min_cluster_mean_distance_reduction_m": float(np.min(means)),
                    "max_cluster_mean_distance_reduction_m": float(np.max(means)),
                }
            )
    return sessions, intervals


def run_window(
    cache: Path,
    route: str,
    max_range_m: int,
    window: int,
    radar_path: Path,
    radar: np.ndarray,
) -> tuple[list[dict[str, Any]], ...]:
    radar_key = f"{route}/novatel/radar_poses.csv"
    middle = len(radar) * window // 100
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

    nav_path = fetch_navigation(cache, route, window, int(mid_times[0]), int(mid_times[-1]))
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
    replay_virtual = route in VIRTUAL_REPLAY_ROUTES and window == 50
    visits: list[dict[str, Any]] = []
    echoes: list[np.ndarray] = []
    echo_ranges: list[np.ndarray] = []
    echo_times: list[np.ndarray] = []
    spoke_displacement = []
    spoke_heading_change = []
    scan_start_us = []
    scan_end_us = []
    spoke_count = 0
    reversed_times = 0
    max_abs_spoke_delay_us = 0
    heading = np.arctan2(mid_rotation[:, 1, 0], mid_rotation[:, 0, 0])
    intervals_s = np.diff(mid_times) * 1e-6
    heading_rate = np.rad2deg(np.diff(np.unwrap(heading)) / intervals_s)
    horizontal_speed = np.linalg.norm(np.diff(mid_position[:, :2], axis=0), axis=1) / intervals_s

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
        spoke_displacement.extend(
            np.linalg.norm(origin[valid, :2] - mid_position[scan_index, :2], axis=1)
        )
        spoke_heading = np.arctan2(rotation[valid, 1, 0], rotation[valid, 0, 0])
        spoke_heading_change.extend(
            np.rad2deg(np.abs(np.angle(np.exp(1j * (spoke_heading - heading[scan_index])))))
        )

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
        echo_ranges.append(distance_bins[peak_bin[echo_row]])
        echo_times.append(utc[echo_row])

        if not replay_virtual:
            continue
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
    for distance in ranges if replay_virtual else ():
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
    echo_pairs, echo_summary = persistent_echo_pairs(route, window, echoes, centre[:2], mid_times)
    diagnostics = range_lag_diagnostics(
        route, window, echoes, echo_ranges, echo_times, centre[:2], mid_times
    )
    telemetry = {
        "route": route,
        "window_percentile": window,
        "scan_midpoints": len(mid_times),
        "spokes": len(spoke_displacement),
        "median_horizontal_speed_m_s": float(np.median(horizontal_speed)),
        "max_horizontal_speed_m_s": float(np.max(horizontal_speed)),
        "p95_abs_heading_rate_deg_s": float(np.quantile(np.abs(heading_rate), 0.95)),
        "max_abs_heading_rate_deg_s": float(np.max(np.abs(heading_rate))),
        "p95_spoke_midpoint_horizontal_displacement_m": float(
            np.quantile(spoke_displacement, 0.95)
        ),
        "max_spoke_midpoint_horizontal_displacement_m": float(np.max(spoke_displacement)),
        "p95_spoke_midpoint_abs_heading_difference_deg": float(
            np.quantile(spoke_heading_change, 0.95)
        ),
        "max_spoke_midpoint_abs_heading_difference_deg": float(np.max(spoke_heading_change)),
    }
    return visits, summary, sources, echo_pairs, echo_summary, diagnostics, [telemetry]


def run_route(cache: Path, route: str, max_range_m: int) -> list[tuple[list[dict[str, Any]], ...]]:
    radar_path = fetch_file(cache, f"{route}/novatel/radar_poses.csv")
    radar = load_poses(radar_path)
    # Quarter windows cannot intersect the central one once the source has 480 scans.
    windows = (25, 50, 75) if len(radar) >= 4 * SCANS_PER_ROUTE else (50,)
    results = []
    for window in windows:
        result = run_window(cache, route, max_range_m, window, radar_path, radar)
        results.append(result)
        print(f"{route} window {window}: {result[4][0]['returns_matched']} matches", flush=True)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cache", type=Path, help="cache for public radar scans and pose clips")
    parser.add_argument("output", type=Path, help="directory for the replay CSV files")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(4) as pool:
        runs = list(pool.map(lambda item: run_route(args.cache, *item), ROUTES.items()))
    results = [run for route in runs for run in route]
    visits, virtual_summary, inputs, pairs, windows, diagnostics, telemetry = (
        [row for batch in batches for row in batch] for batches in zip(*results, strict=True)
    )
    unique_inputs = {(row["public_source"], row["selection"]): row for row in inputs}
    sessions, intervals = echo_intervals(windows)
    outputs = {
        "canoe-registration-visits.csv": visits,
        "canoe-registration-summary.csv": virtual_summary,
        "canoe-inputs.csv": list(unique_inputs.values()),
        "canoe-echo-pairs.csv": pairs,
        "canoe-echo-summary.csv": windows,
        "canoe-echo-session-summary.csv": sessions,
        "canoe-echo-intervals.csv": intervals,
        "canoe-motion-telemetry.csv": telemetry,
        "canoe-echo-range-lag.csv": diagnostics,
        "canoe-echo-range-lag-summary.csv": summarize_range_lag(diagnostics),
    }
    for filename, rows in outputs.items():
        csv_output(args.output / filename, rows)


if __name__ == "__main__":
    main()
