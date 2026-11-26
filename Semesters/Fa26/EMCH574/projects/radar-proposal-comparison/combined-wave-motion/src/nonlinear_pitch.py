"""Compare quadratic pitch damping on common radar visits on COMECH or COCESR."""

import argparse
import csv
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

import paired_experiment as model

NATURAL_OMEGA = 2 * np.pi * model.NATURAL
LINEAR_DAMPING = 2 * model.DAMPING * NATURAL_OMEGA
REFERENCE_AMPLITUDE_M = 0.15
TORQUE_RATIOS = (0.0, 0.25, 0.5, 1.0)
PHASE_COUNT = 32
VISITS = 192
PATH_SAMPLES = 601
CASES = (
    ("reference_lower_frequency", 0.345, 0.150),
    ("reference", 0.350, 0.150),
    ("reference_higher_frequency", 0.355, 0.150),
    ("correction_lower_frequency", 0.30375, 0.432),
    ("correction_lower_amplitude", 0.3325, 0.376),
    ("maximum_linear_correction", 0.3325, 0.432),
    ("pilot_wave", 0.350, 0.360),
)


def static_pitch(frequency, amplitude):
    wave_number = (2 * np.pi * frequency) ** 2 / model.G
    return model.HULL_PITCH_GAIN * wave_number * amplitude * np.cos(model.HEADING)


def linear_amplitude(frequency, amplitude):
    transfer = model.transfer(frequency, model.NATURAL, model.DAMPING)
    return static_pitch(frequency, amplitude) * abs(transfer)


REFERENCE_SPEED = NATURAL_OMEGA * linear_amplitude(model.NATURAL, REFERENCE_AMPLITUDE_M)


def integrate_pitch(frequency, amplitude, torque_ratio, *, spinup, steps_per_period):
    omega = 2 * np.pi * frequency
    period = 1 / frequency
    start = spinup * period
    quadratic = torque_ratio * LINEAR_DAMPING / REFERENCE_SPEED
    forcing_amplitude = NATURAL_OMEGA**2 * static_pitch(frequency, amplitude)

    def derivative(time, state):
        pitch, rate = state
        forcing = -forcing_amplitude * np.sin(omega * time)
        restoring = NATURAL_OMEGA**2 * pitch
        damping = LINEAR_DAMPING * rate + quadratic * rate * abs(rate)
        return rate, forcing - restoring - damping

    solution = solve_ivp(
        derivative,
        (0.0, start + period),
        (0.0, 0.0),
        method="DOP853",
        max_step=period / steps_per_period,
        rtol=1e-11,
        atol=1e-13,
        dense_output=True,
    )
    if not solution.success or solution.sol is None:
        raise RuntimeError(solution.message)
    dense = solution.sol

    def pitch_response(phase):
        return dense(start + np.remainder(phase, 2 * np.pi) / omega)[0]

    time = np.linspace(start, start + period, 8193)
    pitch, rate = dense(time)
    previous_pitch, previous_rate = dense(time - period)
    pitch_repeat_error = float(np.max(np.abs(pitch - previous_pitch)))
    rate_repeat_error = float(np.max(np.abs(rate - previous_rate)))
    assert pitch_repeat_error < 1e-8 and rate_repeat_error < 1e-8

    input_power = -forcing_amplitude * np.sin(omega * time) * rate
    quadratic_power = quadratic * np.abs(rate) ** 3
    damping_power = LINEAR_DAMPING * rate**2 + quadratic_power
    assert np.all(quadratic_power >= 0) and np.all(damping_power >= 0)
    input_work = np.trapezoid(input_power, time)
    dissipated_energy = np.trapezoid(damping_power, time)
    energy_change = 0.5 * (rate[-1] ** 2 - rate[0] ** 2)
    energy_change += 0.5 * NATURAL_OMEGA**2 * (pitch[-1] ** 2 - pitch[0] ** 2)
    relative_energy_residual = (
        abs(input_work - dissipated_energy - energy_change) / dissipated_energy
    )
    assert relative_energy_residual < 1e-7

    phase = np.linspace(0.0, 2 * np.pi, len(time) - 1, endpoint=False)
    fundamental = 2 * np.mean(pitch[:-1] * np.exp(-1j * phase))
    third_harmonic = 2 * np.mean(pitch[:-1] * np.exp(-3j * phase))
    return pitch_response, {
        "peak_pitch_deg": float(np.max(np.abs(pitch)) / model.RAD),
        "peak_angular_speed_rad_s": float(np.max(np.abs(rate))),
        "fundamental_lag_deg": float((np.pi / 2 - np.angle(fundamental)) / model.RAD),
        "third_harmonic_to_fundamental": float(abs(third_harmonic) / abs(fundamental)),
        "quadratic_fraction_of_dissipation": float(
            np.trapezoid(quadratic_power, time) / dissipated_energy
        ),
        "cycle_pitch_repeat_error_rad": pitch_repeat_error,
        "cycle_rate_repeat_error_rad_s": rate_repeat_error,
        "cycle_energy_relative_residual": float(relative_energy_residual),
    }


def run_visits(frequency, amplitude, pitch_response=None):
    return [
        model.run(
            frequency,
            amplitude,
            phase,
            visits=VISITS,
            samples=PATH_SAMPLES,
            pitch_response=pitch_response,
        )
        for phase in range(PHASE_COUNT)
    ]


def check_visits(expected, actual):
    for original, test in zip(expected, actual, strict=True):
        assert np.array_equal(original["acquired"], test["acquired"])
        assert np.array_equal(original["usable"], test["usable"])


def check_saved_baseline(saved, frequency, amplitude, linear):
    matches = [
        cell
        for cell in saved["operating_map"]
        if np.isclose(cell["frequency_hz"], frequency)
        and np.isclose(cell["amplitude_m"], amplitude)
    ]
    if frequency == model.NATURAL and amplitude == REFERENCE_AMPLITUDE_M:
        matches.extend(cell for cell in saved["sensitivity"] if cell["name"] == "reference")
    for cell in matches:
        assert len(cell["realizations"]) == PHASE_COUNT
        for saved_phase, recomputed in zip(cell["realizations"], linear, strict=True):
            assert saved_phase["visits"] == VISITS
            assert np.array_equal(saved_phase["usable_count"], recomputed["usable"].sum(axis=1))
            assert np.array_equal(saved_phase["acquired_count"], recomputed["acquired"].sum(axis=1))
    return bool(matches)


def result_row(name, frequency, amplitude, torque_ratio, linear, saved_baseline):
    response, diagnostics = integrate_pitch(
        frequency, amplitude, torque_ratio, spinup=60, steps_per_period=128
    )
    refined_response, _ = integrate_pitch(
        frequency, amplitude, torque_ratio, spinup=80, steps_per_period=256
    )
    phase = np.linspace(0.0, 2 * np.pi, 8192, endpoint=False)
    refined_error = float(np.max(np.abs(response(phase) - refined_response(phase))))
    assert refined_error < 1e-7
    runs = run_visits(frequency, amplitude, response)
    check_visits(runs, run_visits(frequency, amplitude, refined_response))
    if torque_ratio == 0.0:
        check_visits(linear, runs)
        linear_transfer = model.transfer(frequency, model.NATURAL, model.DAMPING)
        analytical = np.real(
            1j * static_pitch(frequency, amplitude) * linear_transfer * np.exp(1j * phase)
        )
        assert np.max(np.abs(response(phase) - analytical)) < 1e-10
    assert diagnostics["peak_pitch_deg"] <= model.MAX_ANGLE_DEG

    result = model.summarize(runs)
    use = np.array([trial["usable"].mean(axis=1) for trial in runs])
    linear_use = np.array([trial["usable"].mean(axis=1) for trial in linear])
    delta = use - linear_use
    gain_delta = np.diff(delta, axis=1)
    gain_delta_ci = 1.96 * np.std(gain_delta, axis=0, ddof=1) / np.sqrt(PHASE_COUNT)
    max_margin_delta = max(
        np.max(np.abs(new["margin_level"] - base["margin_level"]))
        for new, base in zip(runs, linear, strict=True)
    )
    # Level pointing has zero pitch angle by construction. Its margin still
    # follows the changed antenna origin and the corresponding diffraction ray.
    return {
        "case": name,
        "frequency_hz": frequency,
        "amplitude_m": amplitude,
        "quadratic_torque_ratio": torque_ratio,
        "reference_angular_speed_rad_s": float(REFERENCE_SPEED),
        **diagnostics,
        "midpoint_usable_fraction": result["fraction"][0],
        "spoke_usable_fraction": result["fraction"][1],
        "level_usable_fraction": result["fraction"][2],
        "correction_gain": result["correction_gain"],
        "correction_ci95_halfwidth": result["correction_ci95_halfwidth"],
        "leveling_gain": result["stabilization_gain"],
        "leveling_ci95_halfwidth": result["stabilization_ci95_halfwidth"],
        "correction_gain_change_from_linear": float(gain_delta[:, 0].mean()),
        "correction_gain_change_ci95_halfwidth": float(gain_delta_ci[0]),
        "leveling_gain_change_from_linear": float(gain_delta[:, 1].mean()),
        "leveling_gain_change_ci95_halfwidth": float(gain_delta_ci[1]),
        "max_level_margin_change_from_linear_db": float(max_margin_delta),
        "refined_pitch_difference_rad": refined_error,
        "refined_decision_changes": 0,
        "saved_baseline_checked": saved_baseline and torque_ratio == 0,
        "phases": PHASE_COUNT,
        "visits_per_phase": VISITS,
        "path_samples": PATH_SAMPLES,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--baseline", default=Path("data/experiment-results.json"), type=Path)
    args = parser.parse_args()
    saved = json.loads(args.baseline.read_text())
    rows = []
    for name, frequency, amplitude in CASES:
        assert (2 * np.pi * frequency) ** 2 * amplitude / model.G <= model.MAX_STEEPNESS
        linear = run_visits(frequency, amplitude)
        saved_checked = check_saved_baseline(saved, frequency, amplitude, linear)
        for ratio in TORQUE_RATIOS:
            rows.append(result_row(name, frequency, amplitude, ratio, linear, saved_checked))
        print(f"Verified {name}", flush=True)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} cases to {args.output}")


if __name__ == "__main__":
    main()
