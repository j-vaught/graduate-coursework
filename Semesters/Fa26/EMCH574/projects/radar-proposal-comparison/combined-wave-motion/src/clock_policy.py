"""Evaluate a frequency-only scan-speed choice against fixed scan speeds."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

import paired_experiment as model

DURATION = 480.0
PHASE_COUNT = 256
FREQUENCY_WINDOW = 120.0
SPEEDS = (48, 36, 24)
AMPLITUDES = (0.17, 0.34, 0.56)
FREQUENCIES = np.linspace(0.173, 0.613, 25)
TURN = 2 * np.pi


def visit_times(rpm):
    period = 60 / rpm
    return np.arange(period / 2, DURATION, period)


def visit_phases(frequency, times, starts):
    return (TURN * frequency * times[None, :] - starts[:, None]) % TURN


def longest_update_gaps(times, acquired):
    """Measure update-to-update gaps with observation-window censoring."""
    return np.array([np.diff(np.r_[0.0, times[record], DURATION]).max() for record in acquired])


def p95(values):
    return float(np.quantile(values, 0.95, method="higher"))


def predict_clock(frequency):
    # Idealized frequency estimate rounded to the bins of a 120 s record.
    estimate = np.round(frequency * FREQUENCY_WINDOW) / FREQUENCY_WINDOW
    starts = TURN * (np.arange(PHASE_COUNT) + 0.5) / PHASE_COUNT
    predicted = {}
    for rpm in SPEEDS:
        times = visit_times(rpm)
        # A single fixed visible sector covering half the cycle.
        acquired = visit_phases(estimate, times, starts) < np.pi
        predicted[rpm] = p95(longest_update_gaps(times, acquired))
    # Iteration order favors the fastest clock in ties.
    return float(estimate), min(predicted, key=predicted.__getitem__), predicted


def phase_margin(frequency, amplitude, phase_samples, ray_samples):
    """Evaluate the production acquisition model once per periodic phase grid."""
    phases = np.linspace(0.0, TURN, phase_samples, endpoint=False)
    times = phases / (TURN * frequency)
    result = model.run(frequency, amplitude, 0, times=times, phase_origin=0.0, samples=ray_samples)
    return phases, result["margin_motion"]


def evaluate_cell(frequency, amplitude, starts, phase_samples, ray_samples):
    estimate, selected, predicted = predict_clock(frequency)
    phases, margins = phase_margin(frequency, amplitude, phase_samples, ray_samples)
    margin_by_speed = {}
    for rpm in SPEEDS:
        times = visit_times(rpm)
        phase = visit_phases(frequency, times, starts)
        margin_by_speed[rpm] = np.interp(phase, phases, margins, period=TURN)

    rows = []
    for margin_model in ("fixed", "dwell"):
        gaps = {}
        usable = {}
        for rpm in SPEEDS:
            shift = 0.0
            if margin_model == "dwell":
                shift = 10 * np.log10((60 / rpm) / model.PERIOD)
            acquired = (margin_by_speed[rpm] + shift) >= 0
            gaps[rpm] = longest_update_gaps(visit_times(rpm), acquired)
            usable[rpm] = float(acquired.mean())
        actual = {rpm: p95(gaps[rpm]) for rpm in SPEEDS}
        oracle = min(actual, key=actual.__getitem__)
        row = {
            "frequency_hz": round(float(frequency), 9),
            "amplitude_m": amplitude,
            "estimated_frequency_hz": estimate,
            "window_s": DURATION,
            "common_phase_records": len(starts),
            "margin_model": margin_model,
            "selected_rpm": selected,
            "oracle_rpm": oracle,
            "selected_p95_s": actual[selected],
            "oracle_p95_s": actual[oracle],
            "selected_gain_over_48_rpm_s": actual[48] - actual[selected],
            "selected_gain_over_24_rpm_s": actual[24] - actual[selected],
            "oracle_gain_over_48_rpm_s": actual[48] - actual[oracle],
            "selected_regret_s": actual[selected] - actual[oracle],
            "paired_p95_selected_minus_48_rpm_s": p95(gaps[selected] - gaps[48]),
            "paired_p95_selected_minus_24_rpm_s": p95(gaps[selected] - gaps[24]),
        }
        for rpm in SPEEDS:
            row[f"predicted_{rpm}_rpm_p95_s"] = predicted[rpm]
            row[f"actual_{rpm}_rpm_p95_s"] = actual[rpm]
            row[f"actual_{rpm}_rpm_usable_fraction"] = usable[rpm]
        rows.append(row)
    return rows


def summarize(rows):
    for margin_model in ("fixed", "dwell"):
        cells = [row for row in rows if row["margin_model"] == margin_model]
        selections = {rpm: sum(row["selected_rpm"] == rpm for row in cells) for rpm in SPEEDS}
        print(f"{margin_model}: {len(cells)} cells, selections {selections}")
        for column in (
            "selected_gain_over_48_rpm_s",
            "selected_gain_over_24_rpm_s",
            "oracle_gain_over_48_rpm_s",
            "selected_regret_s",
        ):
            differences = np.array([float(row[column]) for row in cells])
            equal = np.isclose(differences, 0.0, atol=1e-8)
            positive = np.count_nonzero((differences > 0) & ~equal)
            negative = np.count_nonzero((differences < 0) & ~equal)
            print(
                f"  {column}: +/0/- {positive}/{equal.sum()}/{negative}, "
                f"median {np.median(differences):.3f}, mean {differences.mean():.3f}, "
                f"range {differences.min():.3f} to {differences.max():.3f} s"
            )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--phase-samples", type=int, default=8192)
    parser.add_argument("--ray-samples", type=int, default=601)
    args = parser.parse_args()

    rng = np.random.default_rng(model.SEED + 400_000)
    starts = rng.uniform(0, TURN, PHASE_COUNT)
    rows = []
    for frequency in FREQUENCIES:
        wavenumber = (TURN * frequency) ** 2 / model.G
        for amplitude in AMPLITUDES:
            if wavenumber * amplitude <= model.MAX_STEEPNESS:
                rows.extend(
                    evaluate_cell(
                        frequency, amplitude, starts, args.phase_samples, args.ray_samples
                    )
                )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summarize(rows)


if __name__ == "__main__":
    main()
