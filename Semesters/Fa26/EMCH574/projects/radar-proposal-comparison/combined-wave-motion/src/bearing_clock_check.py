"""Replay four radar arms with a common physical crossing clock and yaw retained."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

import paired_experiment as model
from pointing_registration_factorial import ARMS, PHASE_COUNT, VISIT_COUNT, level_mapping_errors

CASES = {
    "reference": (0.3500, 0.150),
    "strongest_registration": (0.3325, 0.432),
    "overlapping_retrofits": (0.36125, 0.376),
}
BEARINGS_DEG = (-90.0, 0.0, 45.0, 89.5, 90.0, 90.5, 135.0, 180.0)
YAW_AMPLITUDES_DEG = (0.0, 1.0)
MIDPOINT_BORESIGHT = -np.pi / 2
TURN = 2 * np.pi
SPIN = TURN / model.PERIOD
MIDPOINTS = np.arange(1, VISIT_COUNT + 1) * model.PERIOD


def wrap(angle):
    return (angle + np.pi) % TURN - np.pi


def yaw_rotation(t, frequency, phase, peak):
    yaw = peak * np.sin(TURN * frequency * t - phase)
    c, s = np.cos(yaw), np.sin(yaw)
    rotation = np.zeros((len(t), 3, 3))
    rotation[:, 0, 0] = rotation[:, 1, 1] = c
    rotation[:, 1, 0] = s
    rotation[:, 0, 1] = -s
    rotation[:, 2, 2] = 1
    return rotation


def vessel_pose(peak):
    def pose(t, frequency, amplitude, phase, damping, pitch_phase=0.0, **kwargs):
        base = model.pose(t, frequency, amplitude, phase, damping, pitch_phase, **kwargs)
        if peak == 0.0:
            return base
        origin, pitch_roll, pitch, roll = base
        ref = origin - pitch_roll @ model.LEVER
        attitude = yaw_rotation(t, frequency[0], phase[0], peak) @ pitch_roll
        return ref + attitude @ model.LEVER, attitude, pitch, roll

    return pose


def crossing_times(frequency, amplitude, phase, bearing, pose):
    """Use unwrapped crossings and assign actual scan membership afterward."""
    nominal_times = MIDPOINTS + wrap(bearing - MIDPOINT_BORESIGHT) / SPIN
    target_x, target_y = model.RANGE * np.array([np.cos(bearing), np.sin(bearing)])

    def flight_bearing(times):
        origin, attitude, _, _ = pose(times, frequency, amplitude, phase, model.DAMPING)
        elevation = model.TARGET_HEIGHT + model.wave(
            target_x, target_y, times, frequency, amplitude, phase
        )
        target = np.column_stack(
            (
                np.full_like(times, target_x),
                np.full_like(times, target_y),
                elevation,
            )
        )
        offset = np.einsum("nji,nj->ni", attitude, target - origin)
        return np.arctan2(offset[:, 1], offset[:, 0])

    times = nominal_times.copy()
    for _ in range(10):
        times = nominal_times + wrap(flight_bearing(times) - bearing) / SPIN
    residual = wrap(flight_bearing(times) - bearing - SPIN * (times - nominal_times))
    assert np.max(np.abs(residual)) < 1e-9
    assert np.min(np.diff(times)) > 0.5 * model.PERIOD
    return times, nominal_times


def heading_preserving_errors(run, yaw_peak, wave_frequency, initial_phase):
    times = run["t"]
    midtimes = np.floor(times / model.PERIOD + 0.5) * model.PERIOD
    at_spoke = yaw_rotation(times, wave_frequency, initial_phase, yaw_peak)
    at_midpoint = yaw_rotation(midtimes, wave_frequency, initial_phase, yaw_peak)
    v = np.einsum("nji,nj->ni", at_spoke, run["target"] - run["origin"])
    azimuth = np.arctan2(v[:, 1], v[:, 0])
    errors = []
    for origin, attitude in ((run["midpoint"], at_midpoint), (run["origin"], at_spoke)):
        position = model.inverse_plane(run["slant"], azimuth, origin, attitude, run["target"][:, 2])
        errors.append(np.linalg.norm(position[:, :2] - run["target"][:, :2], axis=1))
    np.testing.assert_allclose(errors[1], run["errors"][2], atol=5e-13, rtol=0)
    return errors[0], errors[1]


def evaluate(case, carrier, amplitude, bearing_deg, yaw_peak_deg, clock, subdivisions):
    bearing = bearing_deg * model.RAD
    yaw_peak = yaw_peak_deg * model.RAD
    pose = vessel_pose(yaw_peak)
    records = []
    wrong_level_records = []
    delays = []
    corrections = []
    seam_crossings = 0
    for record in range(PHASE_COUNT):
        f, a, phase = model.components(carrier, amplitude, record)
        if clock == "bearing":
            times, nominal_times = crossing_times(f, a, phase, bearing, pose)
        else:
            times = nominal_times = MIDPOINTS + 0.25 * model.PERIOD
        midtimes = np.floor(times / model.PERIOD + 0.5) * model.PERIOD
        seam_crossings += np.count_nonzero(midtimes != MIDPOINTS)
        corrections.append(times - nominal_times)
        delays.append(times - midtimes)
        run = model.run(
            carrier,
            amplitude,
            record,
            times=times,
            samples=subdivisions,
            pose_model=pose,
            target_azimuth_deg=bearing_deg,
        )
        level_midpoint, level_spoke = heading_preserving_errors(run, yaw_peak, carrier, phase[0])
        zero_yaw_midpoint = level_mapping_errors(run, record, {})
        if yaw_peak == 0.0:
            np.testing.assert_allclose(level_midpoint, zero_yaw_midpoint, atol=5e-13, rtol=0)
        errors = np.stack((*run["errors"][:2], level_midpoint, level_spoke))
        echoes = run["acquired"][[0, 1, 2, 2]]
        records.append(echoes & (errors <= model.TOLERANCE))
        wrong_level_records.append(run["acquired"][2] & (zero_yaw_midpoint <= model.TOLERANCE))
    visits = PHASE_COUNT * VISIT_COUNT
    counts = np.sum(records, axis=(0, 2))
    pose_only, pointing_only, pointing_after_pose = (
        100 * (counts[[1, 2, 3]] - counts[[0, 0, 1]]) / visits
    )
    return {
        "case": case,
        "frequency_hz": carrier,
        "amplitude_m": amplitude,
        "bearing_deg": bearing_deg,
        "yaw_peak_deg": yaw_peak_deg,
        "clock": clock,
        "scheduled": visits,
        "scan_assignment_changes": seam_crossings,
        "minimum_signed_pose_delay_s": np.min(delays),
        "maximum_signed_pose_delay_s": np.max(delays),
        "maximum_crossing_shift_s": np.max(np.abs(corrections)),
        **{f"{name}_usable": count for name, count in zip(ARMS, counts, strict=True)},
        "pose_only_gain_pp": pose_only,
        "level_only_gain_pp": pointing_only,
        "level_after_pose_gain_pp": pointing_after_pose,
        "interaction_pp": pointing_after_pose - pointing_only,
        "level_midpoint_usable_erasing_yaw": np.sum(wrong_level_records),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ray-samples", type=int, default=601)
    args = parser.parse_args()
    rows = [
        evaluate(case, f, a, bearing, yaw, clock, args.ray_samples)
        for case, (f, a) in CASES.items()
        for yaw in YAW_AMPLITUDES_DEG
        for bearing in BEARINGS_DEG
        for clock in ("quarter", "bearing")
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
