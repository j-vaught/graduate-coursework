"""Compare the product of the marginal pass rates with common-visit usability."""

import argparse
import csv
import json
from pathlib import Path

import numpy as np

import paired_experiment as model

ARMS = ("body_midpoint", "body_spoke", "level_spoke")
VISITS = 192
PHASES = 32
SUBDIVISIONS = 601
BOOTSTRAPS = 10_000


def visit_counts(frequency, amplitude, options, baseline=None):
    counts = []
    for phase in range(PHASES):
        run = model.run(frequency, amplitude, phase, visits=VISITS, samples=SUBDIVISIONS, **options)
        # The simulator supplies counterfactual coordinates even when the
        # receive gate fails. Use all scheduled visits for both marginals.
        position_pass = run["errors"] <= model.TOLERANCE
        acquisition = run["acquired"]
        joint = acquisition & position_pass
        np.testing.assert_array_equal(joint, run["usable"])
        if baseline is not None:
            reference = baseline["realizations"][phase]
            assert reference["visits"] == VISITS
            np.testing.assert_array_equal(acquisition.sum(axis=1), reference["acquired_count"])
            np.testing.assert_array_equal(joint.sum(axis=1), reference["usable_count"])
        counts.append(np.stack((acquisition, position_pass, joint), axis=1).sum(axis=-1))
    return np.array(counts)


def rates(counts, scheduled):
    probability = counts / scheduled
    independent = probability[..., 0] * probability[..., 1]
    joint = probability[..., 2]
    return independent, joint


def summarize(name, frequency, amplitude, phase_counts):
    scheduled = VISITS * PHASES
    counts = phase_counts.sum(axis=0)
    independent, joint = rates(counts, scheduled)
    row = {
        "case": name,
        "frequency_hz": frequency,
        "amplitude_m": amplitude,
        "scheduled": scheduled,
    }
    for index, arm in enumerate(ARMS):
        acquired, mapped, usable = counts[index]
        row[f"{arm}_acquired"] = int(acquired)
        row[f"{arm}_mapping_pass"] = int(mapped)
        row[f"{arm}_joint_usable"] = int(usable)
        row[f"{arm}_actual_pct"] = joint[index] * 100
        row[f"{arm}_independent_pct"] = independent[index] * 100
        row[f"{arm}_independent_minus_joint_pp"] = (independent[index] - joint[index]) * 100
    for name, after, before in (("registration", 1, 0), ("leveling", 2, 1), ("combined", 2, 0)):
        row[f"{name}_gain_actual_pp"] = (joint[after] - joint[before]) * 100
        row[f"{name}_gain_independent_pp"] = (independent[after] - independent[before]) * 100
        row[f"{name}_gain_independent_minus_joint_pp"] = (
            row[f"{name}_gain_independent_pp"] - row[f"{name}_gain_actual_pp"]
        )
    return row


def bootstrap(phase_counts):
    rng = np.random.default_rng(model.SEED + 2_000_000)
    sampled_phase = rng.integers(PHASES, size=(BOOTSTRAPS, PHASES))
    # Resample whole records and compute both marginals from the same resample.
    counts = phase_counts[sampled_phase].sum(axis=1)
    independent, joint = rates(counts, PHASES * VISITS)
    midpoint_error = independent[:, 0] - joint[:, 0]
    registration_gain_error = independent[:, 1] - independent[:, 0] - joint[:, 1] + joint[:, 0]
    intervals = np.quantile(
        np.column_stack((midpoint_error, registration_gain_error)), [0.025, 0.975], axis=0
    )
    return intervals * 100


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=Path("data/experiment-results.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    original = json.loads(args.baseline.read_text())
    grid = original["operating_map"]
    assert len(grid) == 111
    rows = []
    phase_counts = []
    for cell in grid:
        frequency, amplitude = cell["frequency_hz"], cell["amplitude_m"]
        counts = visit_counts(frequency, amplitude, {}, cell)
        np.testing.assert_array_equal(counts[:, 1:, 1], VISITS)
        rows.append(summarize("grid", frequency, amplitude, counts))
        phase_counts.append(counts)

    midpoint_error_key = "body_midpoint_independent_minus_joint_pp"
    midpoint_errors = np.array([row[midpoint_error_key] for row in rows])
    largest = int(np.argmax(np.abs(midpoint_errors)))
    strongest = max(range(len(grid)), key=lambda i: grid[i]["correction_gain"])
    for index, row in enumerate(rows):
        row["bootstrap_reason"] = ""
        row["midpoint_error_q025_pp"] = ""
        row["midpoint_error_q975_pp"] = ""
        row["registration_gain_error_q025_pp"] = ""
        row["registration_gain_error_q975_pp"] = ""
        if index in (largest, strongest):
            interval = bootstrap(phase_counts[index])
            row.update(
                bootstrap_reason="largest_error" if index == largest else "strongest_registration",
                midpoint_error_q025_pp=interval[0, 0],
                midpoint_error_q975_pp=interval[1, 0],
                registration_gain_error_q025_pp=interval[0, 1],
                registration_gain_error_q975_pp=interval[1, 1],
            )

    reference_noisy = next(
        cell for cell in original["sensitivity"] if cell["name"] == "measurement_noise_idealized"
    )
    for name, frequency, amplitude, bearing_noise, baseline in (
        ("reference_noise", 0.350, 0.150, 0.25, reference_noisy),
        ("strongest_noise_0.25deg", 0.3325, 0.432, 0.25, None),
        ("strongest_noise_1deg", 0.3325, 0.432, 1.0, None),
    ):
        options = {"bearing_sigma_deg": bearing_noise, "range_sigma_m": 0.25}
        counts = visit_counts(frequency, amplitude, options, baseline)
        rows.append(summarize(name, frequency, amplitude, counts))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Verified {len(grid)} original cells and wrote {len(rows)} cases to {args.output}.")
    print(f"Midpoint product error median: {np.median(midpoint_errors):.3f} pp")
    print(
        f"Midpoint product error range: {min(midpoint_errors):.3f} to {max(midpoint_errors):.3f} pp"
    )


if __name__ == "__main__":
    main()
