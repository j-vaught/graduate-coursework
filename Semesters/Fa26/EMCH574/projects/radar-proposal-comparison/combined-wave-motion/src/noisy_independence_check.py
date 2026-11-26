"""Compare product and paired registration gains under the noisy timing grid."""

import argparse
import csv
import json
from pathlib import Path

import numpy as np

import paired_experiment as model

PHASES = 32
VISITS = 192
DELAYS = (0.05, 0.625)
POINTING = ("body", "level")
SIGMA_RANGE = 0.25
SIGMA_BEARING = 0.25


def mapping_passes(run, frequency, amplitude, phase):
    f, a, phases = model.components(frequency, amplitude, phase)
    time = run["t"]
    _, body, _, _ = model.pose(time, f, a, phases, model.DAMPING)
    target = run["target"]
    offset = target - run["origin"]
    body_offset = np.einsum("nji,nj->ni", body, offset)
    rng = np.random.default_rng(model.SEED + 100000 + phase)
    bearing_noise = rng.normal(0, SIGMA_BEARING * model.RAD, VISITS)
    slant = run["slant"] + rng.normal(0, SIGMA_RANGE, VISITS)
    body_bearing = np.arctan2(body_offset[:, 1], body_offset[:, 0]) + bearing_noise
    level_bearing = np.arctan2(offset[:, 1], offset[:, 0]) + bearing_noise
    level = np.broadcast_to(np.eye(3), body.shape)
    for delay in DELAYS:
        origin, rotation, _, _ = model.pose(time - delay, f, a, phases, model.DAMPING)
        body_xyz = model.inverse_plane(slant, body_bearing, origin, rotation, target[:, 2])
        level_xyz = model.inverse_plane(slant, level_bearing, origin, level, target[:, 2])
        errors = np.linalg.norm(np.array([body_xyz, level_xyz])[:, :, :2] - target[:, :2], axis=2)
        yield errors <= model.TOLERANCE


def evaluate(frequency, amplitude):
    masked_phase_results = []
    for phase in range(PHASES):
        run = model.run(
            frequency,
            amplitude,
            phase,
            visits=VISITS,
            samples=601,
            range_sigma_m=SIGMA_RANGE,
            bearing_sigma_deg=SIGMA_BEARING,
        )
        acquire = run["acquired"][[0, 2]]
        exact = run["errors"][[1, 2]] <= model.TOLERANCE
        np.testing.assert_array_equal(exact & acquire, run["usable"][[1, 2]])
        passes = np.array(list(mapping_passes(run, frequency, amplitude, phase)))
        np.testing.assert_array_equal(passes[-1, 0] & acquire[0], run["usable"][0])
        arms = []
        for delayed in passes:
            masks = (acquire, exact, delayed, acquire & exact, acquire & delayed)
            arms.append(np.array(masks).sum(axis=-1))
        masked_phase_results.append(arms)
    counts = np.array(masked_phase_results).sum(axis=0)
    scheduled = PHASES * VISITS
    for speed_index, delay in enumerate(DELAYS):
        for pointing_index, pointing in enumerate(POINTING):
            acq, exact, delayed, joint_exact, joint_delayed = counts[speed_index, :, pointing_index]
            actual = (joint_exact - joint_delayed) / scheduled
            independent = acq * (exact - delayed) / scheduled**2
            covariance_exact = joint_exact / scheduled - acq * exact / scheduled**2
            covariance_delayed = joint_delayed / scheduled - acq * delayed / scheduled**2
            error = covariance_delayed - covariance_exact
            np.testing.assert_allclose(error, independent - actual, atol=1e-14, rtol=0)
            yield {
                "wave_hz": frequency,
                "wave_amplitude_m": amplitude,
                "pointing": pointing,
                "delay_s": delay,
                "scheduled_visits": scheduled,
                "acquired": int(acq),
                "exact_mapping_pass": int(exact),
                "delayed_mapping_pass": int(delayed),
                "exact_joint_pass": int(joint_exact),
                "delayed_joint_pass": int(joint_delayed),
                "joint_registration_gain_pp": actual * 100,
                "product_registration_gain_pp": independent * 100,
                "product_minus_joint_gain_pp": error * 100,
                "acquisition_mapping_cov_exact": covariance_exact,
                "acquisition_mapping_cov_delayed": covariance_delayed,
            }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=Path("data/experiment-results.json"))
    parser.add_argument("--latency-check", type=Path, default=Path("data/latency_noise_grid.csv"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    grid = json.loads(args.baseline.read_text())["operating_map"]
    assert len(grid) == 111
    with args.latency_check.open() as handle:
        previous = {
            (float(row["frequency_hz"]), float(row["amplitude_m"]), float(row["pose_age_s"])): row
            for row in csv.DictReader(handle)
        }
    rows = []
    for cell in grid:
        frequency, amplitude = cell["frequency_hz"], cell["amplitude_m"]
        for row in evaluate(frequency, amplitude):
            historic = previous[frequency, amplitude, row["delay_s"]]
            field = "usable_count" if row["pointing"] == "body" else "level_usable_count"
            assert row["delayed_joint_pass"] == int(historic[field])
            assert row["exact_joint_pass"] == int(previous[frequency, amplitude, 0.0][field])
            rows.append(row)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    for pointing in POINTING:
        for delay in DELAYS:
            errors = np.array(
                [
                    row["product_minus_joint_gain_pp"]
                    for row in rows
                    if row["pointing"] == pointing and row["delay_s"] == delay
                ]
            )
            percentiles = np.quantile(abs(errors), [0.5, 0.9, 1])
            print(f"{pointing}, {delay:g} s, absolute p50/p90/max: {percentiles}")


if __name__ == "__main__":
    main()
