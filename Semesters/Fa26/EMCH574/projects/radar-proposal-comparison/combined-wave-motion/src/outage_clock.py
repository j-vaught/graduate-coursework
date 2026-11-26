"""Compare gaps between usable radar updates over a common elapsed duration."""

import argparse
import csv
from pathlib import Path

import numpy as np

import paired_experiment as model

FREQUENCY = 0.42
PEAK_PITCH_DEG = 3.0
DURATION = 480.0
PHASE_COUNT = 256
SCAN_PERIODS = (1.25, 1 / FREQUENCY, 2.5, 3.75)
INTERVAL_VARIATIONS = (0.0, 0.05, 0.10)


def visit_times(period, variation, phase_index):
    """Generate visits inside the observation window from perturbed scan intervals."""
    first = period / 2
    count = int(np.ceil(DURATION / (period * (1 - variation))))
    rng = np.random.default_rng(model.SEED + 200_000 + phase_index)
    perturbations = rng.uniform(-variation, variation, count)
    times = first + np.r_[0.0, np.cumsum(period * (1 + perturbations))]
    return times[times < DURATION]


def evaluate(amplitude, period, variation):
    usable_fractions = []
    longest_gaps = []
    visit_counts = []
    for phase_index in range(PHASE_COUNT):
        times = visit_times(period, variation, phase_index)
        result = model.run(
            FREQUENCY,
            amplitude,
            phase_index,
            scan=period,
            times=times,
            phase_origin=2 * np.pi * (phase_index + 0.5) / PHASE_COUNT,
        )
        usable = result["usable"][1]
        usable_fractions.append(float(usable.mean()))
        longest_gaps.append(float(np.diff(np.r_[0.0, times[usable], DURATION]).max()))
        visit_counts.append(len(times))

    cycles_per_scan = FREQUENCY * period
    return {
        "wave_frequency_hz": FREQUENCY,
        "wave_amplitude_m": amplitude,
        "peak_pitch_deg": PEAK_PITCH_DEG,
        "window_s": DURATION,
        "phase_count": PHASE_COUNT,
        "nominal_scan_period_s": period,
        "nominal_wave_cycles_per_scan": cycles_per_scan,
        "scan_interval_perturbation_fraction": variation,
        "min_visit_count": min(visit_counts),
        "max_visit_count": max(visit_counts),
        "mean_usable_fraction": float(np.mean(usable_fractions)),
        "p50_longest_gap_s": float(np.quantile(longest_gaps, 0.50, method="higher")),
        "p95_longest_gap_s": float(np.quantile(longest_gaps, 0.95, method="higher")),
        "no_usable_update_records": longest_gaps.count(DURATION),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    k = (2 * np.pi * FREQUENCY) ** 2 / model.G
    response = model.transfer(np.array([FREQUENCY]), model.NATURAL, model.DAMPING)[0]
    pitch_per_meter = model.HULL_PITCH_GAIN * k * np.cos(model.HEADING) * abs(response)
    amplitude = PEAK_PITCH_DEG * model.RAD / pitch_per_meter
    assert k * amplitude <= model.MAX_STEEPNESS
    rows = [
        evaluate(amplitude, period, variation)
        for period in SCAN_PERIODS
        for variation in INTERVAL_VARIATIONS
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
