"""Compare periodic and narrowband forcing over equal observation windows."""

import argparse
import csv
from pathlib import Path

import numpy as np

import paired_experiment as model
from outage_clock import DURATION, FREQUENCY, PEAK_PITCH_DEG, PHASE_COUNT

SCAN_PERIODS = (1.25, 2.50, 3.75)
FREQUENCY_RATIOS = np.array([0.98, 1.0, 1.02])
VARIANCE_WEIGHTS = np.array([0.08, 0.84, 0.08])


def narrowband_components(frequency, amplitude, phase_index, _irregular=False):
    _, _, carrier_phase = model.components(frequency, amplitude, phase_index)
    rng = np.random.default_rng(model.SEED + 300_000 + phase_index)
    sideband_phases = rng.uniform(0, 2 * np.pi, 2)
    phases = np.array([sideband_phases[0], carrier_phase[0], sideband_phases[1]])
    return frequency * FREQUENCY_RATIOS, amplitude * np.sqrt(VARIANCE_WEIGHTS), phases


def wavenumber(frequency):
    return (2 * np.pi * frequency) ** 2 / model.G


def pitch_rao(frequency):
    response = model.transfer(frequency, model.NATURAL, model.DAMPING)
    return model.HULL_PITCH_GAIN * wavenumber(frequency) * np.cos(model.HEADING) * abs(response)


def evaluate(amplitude, period, component_model):
    times = np.arange(period / 2, DURATION, period)
    usable_fractions = []
    longest_gaps = []
    for phase_index in range(PHASE_COUNT):
        result = model.run(
            FREQUENCY,
            amplitude,
            phase_index,
            scan=period,
            times=times,
            component_model=component_model,
        )
        usable = result["usable"][1]
        usable_fractions.append(float(usable.mean()))
        longest_gaps.append(float(np.diff(np.r_[0.0, times[usable], DURATION]).max()))
    return np.array(usable_fractions), np.array(longest_gaps)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    amplitude = PEAK_PITCH_DEG * model.RAD / pitch_rao(FREQUENCY)
    frequencies, amplitudes, _ = narrowband_components(FREQUENCY, amplitude, 0)
    np.testing.assert_allclose(np.sum(amplitudes**2), amplitude**2, rtol=1e-14)
    slope_bound = float(np.dot(wavenumber(frequencies), amplitudes))
    pitch_amplitudes = amplitudes * pitch_rao(frequencies) / model.RAD
    assert slope_bound <= model.MAX_STEEPNESS
    assert np.sum(pitch_amplitudes) <= model.MAX_ANGLE_DEG
    assert np.sum(pitch_amplitudes) * 0.6 * np.tan(model.HEADING) <= model.MAX_ANGLE_DEG
    bandwidth = float(np.sqrt(np.dot(VARIANCE_WEIGHTS, (frequencies - FREQUENCY) ** 2)))

    rows = []
    for period in SCAN_PERIODS:
        regular_usable, regular_gap = evaluate(amplitude, period, model.components)
        narrow_usable, narrow_gap = evaluate(amplitude, period, narrowband_components)
        difference_pp = 100 * (narrow_usable - regular_usable)
        rows.append(
            {
                "window_s": DURATION,
                "record_count": PHASE_COUNT,
                "scan_period_s": period,
                "carrier_hz": FREQUENCY,
                "rms_elevation_m": amplitude / np.sqrt(2),
                "regular_pitch_amplitude_deg": PEAK_PITCH_DEG,
                "narrowband_rms_frequency_spread_hz": bandwidth,
                "narrowband_surface_slope_bound": slope_bound,
                "narrowband_peak_pitch_bound_deg": float(np.sum(pitch_amplitudes)),
                "narrowband_rms_pitch_deg": float(np.linalg.norm(pitch_amplitudes) / np.sqrt(2)),
                "regular_mean_usable_fraction": float(regular_usable.mean()),
                "narrowband_mean_usable_fraction": float(narrow_usable.mean()),
                "paired_usable_difference_pp": float(difference_pp.mean()),
                "paired_usable_interval_halfwidth_pp": float(
                    1.96 * np.std(difference_pp, ddof=1) / np.sqrt(PHASE_COUNT)
                ),
                "regular_p95_longest_gap_s": float(np.quantile(regular_gap, 0.95, method="higher")),
                "narrowband_p95_longest_gap_s": float(
                    np.quantile(narrow_gap, 0.95, method="higher")
                ),
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
