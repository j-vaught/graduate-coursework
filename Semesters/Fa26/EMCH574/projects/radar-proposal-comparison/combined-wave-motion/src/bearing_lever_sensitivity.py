"""Sweep target azimuth and antenna lever motion on matched wave and visit schedules."""

import argparse
import csv
import json
from pathlib import Path

import numpy as np

import paired_experiment as model

FREQUENCY = 0.3325
AMPLITUDE = 0.432
PHASES = 32
VISITS = 192
PATH_SAMPLES = 601
AZIMUTHS = (0, 45, 90, 135, 180, -90)


def fixed_lever_pose(t, freq, amp, ph, damping, pitch_phase=0.0, *, pitch_response=None):
    """Keep the same static antenna origin but remove rotation of its lever arm."""
    origin, rotation, pitch, roll = model.pose(
        t, freq, amp, ph, damping, pitch_phase, pitch_response=pitch_response
    )
    rotating_offset = np.einsum("nij,j->ni", rotation, model.LEVER)
    return origin - rotating_offset + model.LEVER, rotation, pitch, roll


def run_visits(**settings):
    # For each direction reset the antenna scan phase so the buoy visit is
    # still one quarter-rotation after the pose assigned to the scan midpoint.
    return [
        model.run(FREQUENCY, AMPLITUDE, phase, visits=VISITS, samples=PATH_SAMPLES, **settings)
        for phase in range(PHASES)
    ]


def verify_baseline(path, baseline, forward):
    saved = json.loads(path.read_text())
    cell = next(
        case
        for case in saved["operating_map"]
        if np.isclose(case["frequency_hz"], FREQUENCY)
        and np.isclose(case["amplitude_m"], AMPLITUDE)
    )
    for published, implicit, explicit in zip(cell["realizations"], baseline, forward, strict=True):
        for field in ("t", "target", "errors", "acquired", "usable"):
            np.testing.assert_array_equal(implicit[field], explicit[field])
        np.testing.assert_array_equal(published["acquired_count"], implicit["acquired"].sum(axis=1))
        np.testing.assert_array_equal(published["usable_count"], implicit["usable"].sum(axis=1))
    frequency, amplitude, phase = model.components(FREQUENCY, 0.0, 0)
    time = np.array([0.0])
    original, *_ = model.pose(time, frequency, amplitude, phase, model.DAMPING)
    fixed, *_ = fixed_lever_pose(time, frequency, amplitude, phase, model.DAMPING)
    np.testing.assert_array_equal(original, fixed)


def verify_geometry(azimuth, baseline, rotating, fixed):
    direction = azimuth * model.RAD
    target_xy = model.RANGE * np.array([np.cos(direction), np.sin(direction)])
    expected_xy = np.broadcast_to(target_xy, (VISITS, 2))
    for original, body_lever, fixed_lever in zip(baseline, rotating, fixed, strict=True):
        for run in (body_lever, fixed_lever):
            for field in ("t", "pitch", "roll"):
                np.testing.assert_array_equal(run[field], original[field])
            np.testing.assert_allclose(run["target"][:, :2], expected_xy)
        np.testing.assert_array_equal(body_lever["target"], fixed_lever["target"])
        rotation = model.rotation(body_lever["pitch"], body_lever["roll"])
        offset = np.einsum("nij,j->ni", rotation, model.LEVER) - model.LEVER
        np.testing.assert_allclose(body_lever["origin"] - fixed_lever["origin"], offset, atol=1e-14)


def summarize(azimuth, lever, runs):
    metrics = model.summarize(runs)
    acquired = np.concatenate([run["acquired"][0] for run in runs])
    usable = np.concatenate([run["usable"] for run in runs], axis=1)
    midpoint_error = np.concatenate([run["errors"][0] for run in runs])
    return {
        "target_azimuth_deg": azimuth,
        "lever_motion": lever,
        "frequency_hz": FREQUENCY,
        "amplitude_m": AMPLITUDE,
        "nominal_buoy_radius_m": model.RANGE,
        "scan_period_s": model.PERIOD,
        "spoke_minus_midpoint_s": model.PERIOD / 4,
        "phases": PHASES,
        "visits_per_phase": VISITS,
        "path_samples": PATH_SAMPLES,
        "scheduled_count": len(acquired),
        "body_acquired_count": int(acquired.sum()),
        "midpoint_usable_count": int(usable[0].sum()),
        "spoke_usable_count": int(usable[1].sum()),
        "level_usable_count": int(usable[2].sum()),
        "midpoint_usable_fraction": metrics["fraction"][0],
        "spoke_usable_fraction": metrics["fraction"][1],
        "level_usable_fraction": metrics["fraction"][2],
        "correction_gain": metrics["correction_gain"],
        "correction_ci95_halfwidth": metrics["correction_ci95_halfwidth"],
        "leveling_gain": metrics["stabilization_gain"],
        "leveling_ci95_halfwidth": metrics["stabilization_ci95_halfwidth"],
        "acquired_midpoint_error_p95_m": (
            float(np.quantile(midpoint_error[acquired], 0.95)) if acquired.any() else None
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, default=Path("data/experiment-results.json"))
    args = parser.parse_args()
    baseline = run_visits()
    rows = []
    for azimuth in AZIMUTHS:
        rotating = run_visits(target_azimuth_deg=azimuth)
        if azimuth == 0:
            verify_baseline(args.baseline, baseline, rotating)
        fixed = run_visits(target_azimuth_deg=azimuth, pose_model=fixed_lever_pose)
        verify_geometry(azimuth, baseline, rotating, fixed)
        rows.append(summarize(azimuth, "rotating", rotating))
        rows.append(summarize(azimuth, "fixed", fixed))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Verified the forward baseline and wrote {len(rows)} cases to {args.output}")


if __name__ == "__main__":
    main()
