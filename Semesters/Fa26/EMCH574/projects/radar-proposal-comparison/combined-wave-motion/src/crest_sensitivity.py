"""Test the bound second harmonic of a regular wave at fixed hull motion."""

import argparse
import csv
import json
from functools import partial
from pathlib import Path

import numpy as np

import paired_experiment as model


def stokes_surface(x, y, t, freq, amp, phase, *, harmonic_scale=1.0):
    """Evaluate deep-water second-order Stokes elevation for one component."""
    (frequency,), (amplitude,), (initial_phase,) = freq, amp, phase
    omega = 2 * np.pi * frequency
    wavenumber = omega**2 / model.G
    along_wave = np.cos(model.HEADING) * x + np.sin(model.HEADING) * y
    fundamental_phase = wavenumber * along_wave - omega * t + initial_phase
    second_harmonic = 0.5 * wavenumber * amplitude**2 * np.cos(2 * fundamental_phase)
    return model.wave(x, y, t, freq, amp, phase) + harmonic_scale * second_harmonic


def check_wave(frequency, amplitude):
    """Check crest and trough heights, exact peak slope, and its analytic bound."""
    omega = 2 * np.pi * frequency
    wavenumber = omega**2 / model.G
    steepness = wavenumber * amplitude
    assert steepness <= model.MAX_STEEPNESS
    bound = steepness + steepness**2
    peak_slope_cosine = 4 * steepness / (np.sqrt(1 + 32 * steepness**2) + 1)
    peak_slope_phase = np.arccos(peak_slope_cosine)
    peak_slope = steepness * np.sin(peak_slope_phase) * (1 + 2 * steepness * peak_slope_cosine)
    harmonic_amplitude = 0.5 * steepness * amplitude

    args = (np.array([frequency]), np.array([amplitude]), np.array([0.2]))
    phase = np.array([0.0, np.pi, peak_slope_phase])
    x = (phase - args[2][0]) / wavenumber * np.cos(model.HEADING)
    y = (phase - args[2][0]) / wavenumber * np.sin(model.HEADING)
    z = stokes_surface(x, y, 0, *args)
    np.testing.assert_allclose(
        z[:2], amplitude * np.array([1, -1]) + harmonic_amplitude, atol=1e-12
    )
    dx = 1e-4 * np.cos(model.HEADING)
    dy = 1e-4 * np.sin(model.HEADING)
    slope = (
        stokes_surface(x + dx, y + dy, 0, *args) - stokes_surface(x - dx, y - dy, 0, *args)
    ) / 2e-4
    np.testing.assert_allclose(abs(slope), [0, 0, peak_slope], rtol=1e-7, atol=1e-10)
    assert peak_slope <= bound
    return steepness, harmonic_amplitude, peak_slope, bound


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=Path("data/experiment-results.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cached = json.loads(args.cache.read_text())
    assumptions = cached["metadata"]["assumptions"]
    visits = assumptions["visits_per_realization"]
    samples = assumptions["crest_samples"]
    phase_indices = range(assumptions["phase_realizations"])
    reference = next(case for case in cached["sensitivity"] if case["name"] == "reference")
    strongest = max(cached["operating_map"], key=lambda case: case["correction_gain"])
    pilot = cached["pilot"]
    cases = (
        (
            "reference",
            assumptions["reference_frequency_hz"],
            assumptions["reference_amplitude_m"],
            phase_indices,
            reference,
        ),
        (
            "strongest_linear_correction",
            strongest["frequency_hz"],
            strongest["amplitude_m"],
            phase_indices,
            strongest,
        ),
        ("pilot", pilot["frequency_hz"], pilot["amplitude_m"], [pilot["phase"]], pilot),
    )
    processing = cached["metadata"]["classifications"]
    rows = []
    for name, frequency, amplitude, phases, cache_case in cases:
        ka, harmonic, peak_slope, bound = check_wave(frequency, amplitude)
        airys, stokes = [], []
        refinement_flips = np.zeros(len(processing), dtype=int)
        for index in phases:
            air = model.run(frequency, amplitude, index, visits=visits, samples=samples)
            control = model.run(
                frequency,
                amplitude,
                index,
                visits=visits,
                samples=samples,
                surface_model=partial(stokes_surface, harmonic_scale=0.0),
            )
            for key, values in air.items():
                if isinstance(values, np.ndarray):
                    np.testing.assert_array_equal(control[key], values)
            assert control["run_lengths"] == air["run_lengths"]
            if name == "pilot":
                for key, values in cache_case["trace"].items():
                    np.testing.assert_allclose(air[key], values, rtol=0, atol=1e-10)
            else:
                realization = cache_case["realizations"][index]
                np.testing.assert_array_equal(
                    air["acquired"].sum(axis=1), realization["acquired_count"]
                )
                np.testing.assert_array_equal(
                    air["usable"].sum(axis=1), realization["usable_count"]
                )

            nonlinear = model.run(
                frequency,
                amplitude,
                index,
                visits=visits,
                samples=samples,
                surface_model=stokes_surface,
            )
            for key in ("t", "pitch", "roll", "origin", "midpoint"):
                np.testing.assert_array_equal(nonlinear[key], air[key])
            refined = model.run(
                frequency,
                amplitude,
                index,
                visits=visits,
                samples=2 * samples - 1,
                surface_model=stokes_surface,
            )
            refinement_flips += np.count_nonzero(nonlinear["usable"] != refined["usable"], axis=1)
            airys.append(air)
            stokes.append(nonlinear)

        total = len(phases) * visits
        for method, label in enumerate(processing):
            airy_acquired = sum(np.count_nonzero(run["acquired"][method]) for run in airys)
            airy_usable = sum(np.count_nonzero(run["usable"][method]) for run in airys)
            stokes_acquired = sum(np.count_nonzero(run["acquired"][method]) for run in stokes)
            stokes_usable = sum(np.count_nonzero(run["usable"][method]) for run in stokes)
            rows.append(
                {
                    "case": name,
                    "frequency_hz": frequency,
                    "amplitude_m": amplitude,
                    "ka": ka,
                    "harmonic_amplitude_m": harmonic,
                    "stokes_peak_surface_slope": peak_slope,
                    "stokes_surface_slope_bound": bound,
                    "method": label,
                    "visits": total,
                    "airy_acquired": airy_acquired,
                    "airy_usable": airy_usable,
                    "airy_usable_fraction": airy_usable / total,
                    "stokes_acquired": stokes_acquired,
                    "stokes_usable": stokes_usable,
                    "stokes_usable_fraction": stokes_usable / total,
                    "stokes_minus_airy_usable_pp": 100 * (stokes_usable - airy_usable) / total,
                    "stokes_path_refinement_usable_flips": refinement_flips[method],
                }
            )

    with args.output.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Verified zero-harmonic and cached baselines. Wrote {args.output}")


if __name__ == "__main__":
    main()
