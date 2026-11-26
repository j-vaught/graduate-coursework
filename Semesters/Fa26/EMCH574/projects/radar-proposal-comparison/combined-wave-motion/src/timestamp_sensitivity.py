"""Reproduce the fixed-echo pose timestamp-delay sensitivity."""

import argparse
import csv
from pathlib import Path

import numpy as np

import paired_experiment as model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    frequency = 0.3325
    amplitude = 0.432
    phase_count = 32
    visits = 192
    delays = [0.0, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.625, 0.75, 1.0]
    measured_fraction = {delay: [] for delay in delays}
    baseline_fraction = []
    counts = {delay: {"acquired": 0, "usable": 0, "outside": 0} for delay in delays}

    for phase in range(phase_count):
        result = model.run(frequency, amplitude, phase, visits=visits, samples=601)
        f, a, p = model.components(frequency, amplitude, phase)
        _, rotation, _, _ = model.pose(result["t"], f, a, p, model.DAMPING)
        target_vector = result["target"] - result["origin"]
        body_vector = np.einsum("nji,nj->ni", rotation, target_vector)
        azimuth = np.arctan2(body_vector[:, 1], body_vector[:, 0])
        acquired = result["acquired"][0]
        baseline = result["usable"][0]
        baseline_fraction.append(np.mean(baseline))

        for delay in delays:
            origin, attitude, _, _ = model.pose(result["t"] - delay, f, a, p, model.DAMPING)
            reconstructed = model.inverse_plane(
                result["slant"], azimuth, origin, attitude, result["target"][:, 2]
            )
            error = np.linalg.norm(reconstructed[:, :2] - result["target"][:, :2], axis=1)
            usable = acquired & (error <= model.TOLERANCE) & np.isfinite(error)
            if delay == 0:
                assert np.array_equal(usable, result["usable"][1])
            if delay == 0.625:
                assert np.array_equal(usable, baseline)

            acquired_count = int(acquired.sum())
            usable_count = int(usable.sum())
            counts[delay]["acquired"] += acquired_count
            counts[delay]["usable"] += usable_count
            counts[delay]["outside"] += acquired_count - usable_count
            measured_fraction[delay].append(np.mean(usable))

    total_visits = phase_count * visits
    rows = []
    for delay in delays:
        fractions = np.array(measured_fraction[delay])
        gain = fractions - np.array(baseline_fraction)
        mean_gain = float(np.mean(gain))
        ci_half_width = float(1.96 * np.std(gain, ddof=1) / np.sqrt(phase_count))
        case = counts[delay]
        assert case["acquired"] == case["usable"] + case["outside"]
        rows.append(
            {
                "frequency_hz": frequency,
                "amplitude_m": amplitude,
                "delay_s": delay,
                "phase_realizations": phase_count,
                "visits_per_phase": visits,
                "crest_samples": 601,
                "scheduled_count": total_visits,
                "acquired_count": case["acquired"],
                "below_threshold_count": total_visits - case["acquired"],
                "acquired_outside_tolerance_count": case["outside"],
                "usable_count": case["usable"],
                "usable_fraction": float(np.mean(fractions)),
                "correction_gain": mean_gain,
                "correction_ci95_halfwidth": ci_half_width,
            }
        )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} delay cases to {output}")


if __name__ == "__main__":
    main()
