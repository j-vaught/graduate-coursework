"""Fit forced heave and pitch on the public CK-14e tank tests and replay the radar model.

Pass the published data repository at commit 9844883148636fe651aa73afa6d2b9fbb3562e91
(https://github.com/cnr-inm-mao/ck14-e_experimental-data) as the first argument.
The archival deposit is https://doi.org/10.5281/zenodo.17315035.

The SMC IMU User Guide v5.2, Sec. 2.2, defines bow-down pitch and upward heave.
https://www.shipmotion.eu/files/SMC%20IMU%20User%20Guide%20v5.2.pdf
The Teledyne PDS User Manual, Sec. 4.4.1.2, shows project-selectable pitch units.
https://www.teledynemarine.com/en-us/products/SiteAssets/PDS/Teledyne%20PDS%20User%20Manual.pdf
Because the public export does not state its project units, also test reversing
the recorded pitch and heave signs individually and jointly in the overlap case.
"""

from __future__ import annotations

import argparse
import csv
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import numpy as np
from scipy.io import loadmat
from scipy.optimize import minimize_scalar
from scipy.signal import butter, detrend, hilbert, sosfiltfilt

import paired_experiment as model
from pointing_registration_factorial import (
    ARMS,
    PATH_SUBDIVISIONS,
    PHASE_COUNT,
    VISIT_COUNT,
    level_mapping_errors,
)

HULL_LENGTH_M = 1.40
WAVELENGTH_RATIOS = (1.5, 2.0, 3.0)
POSE_DELAY_S = model.PERIOD / 4
TWO_PI = 2 * np.pi

# One-based columns 1, 3, 9, 22 and 33 in the archive's MATLAB header.
TIME_MS, PITCH, PITCH_RATE, FIXED_COG_ELEVATION, MOVING_COG_ELEVATION = (0, 2, 8, 21, 32)


def raw_attitude(directory):
    path = directory / "CSV" / "250307_REG_WP_PM_moored_1.csv"
    # Raw PDS2000 rows after the four-line preamble. Time is Unix seconds.
    time, pitch, heave = np.loadtxt(path, delimiter=",", skiprows=4, usecols=(0, 2, 7), unpack=True)
    assert np.all(np.diff(time) > 0)
    return time, pitch, heave


def regular_run(directory, index):
    stem = f"ck14pp_c18_{index}"
    with ZipFile(directory / "processed" / f"{stem}.zip") as archive:
        payload = archive.read(f"{stem}.mat")
    return loadmat(BytesIO(payload), variable_names=["measpp"])["measpp"]


def fit_frequency(t, elevation, nominal):
    def error(frequency):
        angle = TWO_PI * frequency * t
        basis = np.column_stack((np.cos(angle), np.sin(angle), np.ones_like(t), t))
        coef, _, _, _ = np.linalg.lstsq(basis, elevation, rcond=None)
        return np.mean((basis @ coef - elevation) ** 2)

    fit = minimize_scalar(error, bounds=(0.94 * nominal, 1.06 * nominal), method="bounded")
    assert fit.success
    return float(fit.x)


def wave_quadratures(t, elevation, frequency):
    finite = np.isfinite(elevation)
    elevation = np.interp(t, t[finite], elevation[finite])
    sample_rate = 1 / np.median(np.diff(t))
    band = butter(
        2, [0.55 * frequency, 1.45 * frequency], fs=sample_rate, btype="bandpass", output="sos"
    )
    return hilbert(sosfiltfilt(band, elevation))


def fit_response(t, wave, motion, train, heldout):
    dynamic = np.column_stack((wave.real, -wave.imag))
    design = np.column_stack((dynamic, np.ones_like(t), t))
    before = np.linalg.lstsq(design[train], motion[train], rcond=None)[0]
    after = np.linalg.lstsq(design[heldout], motion[heldout], rcond=None)[0]
    prediction = dynamic @ before[:2]
    residual = detrend(motion[heldout] - prediction[heldout])
    error = np.linalg.norm(residual) / np.linalg.norm(detrend(motion[heldout]))
    return complex(*before[:2]), complex(*after[:2]), float(error)


def head_sea(x, y, t, frequency, amplitude, phase):
    """The incident wave travels against the nominal forward body axis."""
    return model.wave(-np.asarray(x) / np.cos(model.HEADING), 0.0, t, frequency, amplitude, phase)


def harmonic_pose(pitch_rao, heave_rao):
    """Use vibration alone while setting surge, roll, and yaw to zero."""

    def pose(t, frequency, amplitude, phase, _damping, _pitch_phase=0.0, **_):
        wave = amplitude[0] * np.exp(1j * (TWO_PI * frequency[0] * t - phase[0]))
        pitch = np.real(pitch_rao * wave)
        heave = np.real(heave_rao * wave)
        zeros = np.zeros_like(t)
        rotation = model.rotation(pitch, zeros)
        center = np.column_stack((zeros, zeros, model.RADAR_HEIGHT - model.LEVER[2] + heave))
        return center + rotation @ model.LEVER, rotation, pitch, zeros

    return pose


def replay_radar(response, pose_name, pose, bearing):
    errors, acquired, margins = [], [], []
    for phase in range(PHASE_COUNT):
        run = model.run(
            response["frequency_hz"],
            response["wave_amplitude_m"],
            phase,
            visits=VISIT_COUNT,
            samples=PATH_SUBDIVISIONS,
            target_azimuth_deg=bearing,
            surface_model=head_sea,
            pose_model=pose,
        )
        errors.append(np.insert(run["errors"], 2, level_mapping_errors(run, phase, {}), axis=0))
        acquired.append(run["acquired"][[0, 1, 2, 2]])
        margins.append(run["margin_motion"])
    distance = np.asarray(errors)
    echo = np.asarray(acquired)
    scheduled = PHASE_COUNT * VISIT_COUNT
    rows = []
    for tolerance in (model.TOLERANCE, 0.25):
        counts = (echo & (distance <= tolerance)).sum(axis=(0, 2))
        registration_gain = (counts[1] - counts[0]) * 100 / scheduled
        stand_alone_pointing = (counts[2] - counts[0]) * 100 / scheduled
        sequential_pointing = (counts[3] - counts[1]) * 100 / scheduled
        rows.append(
            {
                "run": response["run"],
                "response": pose_name,
                "bearing_deg": bearing,
                "tolerance_m": tolerance,
                "scheduled": scheduled,
                "body_midpoint_error_p95_m": np.quantile(distance[:, 0], 0.95),
                "body_midpoint_error_max_m": np.max(distance[:, 0]),
                "body_echo_margin_min_db": np.min(margins),
                **{f"{arm}_usable": count for arm, count in zip(ARMS, counts, strict=True)},
                "body_registration_gain_pp": registration_gain,
                "stand_alone_pointing_gain_pp": stand_alone_pointing,
                "pointing_after_registration_gain_pp": sequential_pointing,
                "interaction_pp": sequential_pointing - stand_alone_pointing,
            }
        )
    return rows


def run_benchmark(directory, index, wavelength_ratio, raw):
    measured = regular_run(directory, index)
    base_time = measured[0, TIME_MS] / 1000
    t = (measured[:, TIME_MS] - measured[0, TIME_MS]) / 1000
    end = t[-1]
    nominal = np.sqrt(model.G / (TWO_PI * wavelength_ratio * HULL_LENGTH_M))
    steady = np.flatnonzero((t >= 1 / nominal) & (t < end - 1 / nominal))
    train, heldout = np.array_split(steady, 2)
    frequency = fit_frequency(t[steady], measured[steady, FIXED_COG_ELEVATION] / 1000, nominal)
    local_wave = wave_quadratures(t, measured[:, MOVING_COG_ELEVATION] / 1000, frequency)
    amplitude = float(np.median(abs(local_wave[steady])))
    raw_time, raw_pitch, raw_heave = raw
    assert raw_time[0] <= base_time and base_time + end <= raw_time[-1]
    heave = np.interp(t, raw_time - base_time, raw_heave)
    pitch = measured[:, PITCH]
    assert np.corrcoef(pitch, np.interp(t, raw_time - base_time, raw_pitch))[0, 1] > 0.999
    pitch_fit, pitch_test, pitch_error = fit_response(t, local_wave, pitch, train, heldout)
    heave_fit, heave_test, heave_error = fit_response(t, local_wave, heave, train, heldout)
    pitch_rate_fit, _, rate_error = fit_response(
        t, local_wave, measured[:, PITCH_RATE], train, heldout
    )
    harmonically_derived_rate = 1j * TWO_PI * frequency * pitch_fit
    wavenumber = (TWO_PI * frequency) ** 2 / model.G
    pitch_paper = (
        -1j
        * model.HULL_PITCH_GAIN
        * wavenumber
        * model.transfer(frequency, model.NATURAL, model.DAMPING)
        / model.RAD
    )
    heave_paper = model.transfer(frequency, 0.8, 0.3)
    measured_mismatch = pitch[heldout] - np.interp(t[heldout] - POSE_DELAY_S, t, pitch)
    mismatch_factor = 2 * abs(np.sin(np.pi * frequency * POSE_DELAY_S))
    observed_slope = wavenumber * amplitude
    assert observed_slope <= model.MAX_STEEPNESS
    assert max(abs(pitch_fit), abs(pitch_test)) * amplitude <= model.MAX_ANGLE_DEG
    response = {
        "run": f"ck14pp_c18_{index}",
        "wavelength_to_hull_length": wavelength_ratio,
        "record_duration_s": end,
        "calibration_duration_s": t[train[-1]] - t[train[0]],
        "holdout_duration_s": t[heldout[-1]] - t[heldout[0]],
        "frequency_hz": frequency,
        "wave_amplitude_m": amplitude,
        "wave_steepness": observed_slope,
        "pitch_rate_measured_harmonic_peak_deg_s": abs(pitch_rate_fit) * amplitude,
        "pitch_rate_derived_harmonic_peak_deg_s": abs(harmonically_derived_rate) * amplitude,
        "pitch_rate_phase_difference_deg": np.angle(
            pitch_rate_fit / harmonically_derived_rate, deg=True
        ),
        "pitch_rate_holdout_error_ratio": rate_error,
        "pitch_phase_mismatch_measured_p95_deg": float(np.quantile(abs(measured_mismatch), 0.95)),
        "pitch_phase_mismatch_empirical_peak_deg": mismatch_factor * abs(pitch_fit) * amplitude,
        "pitch_phase_mismatch_prescribed_peak_deg": mismatch_factor * abs(pitch_paper) * amplitude,
    }
    for name, (fit, test, paper, error) in {
        "pitch": (pitch_fit, pitch_test, pitch_paper, pitch_error),
        "heave": (heave_fit, heave_test, heave_paper, heave_error),
    }.items():
        response[f"{name}_rao_magnitude"] = abs(fit)
        response[f"{name}_rao_phase_deg"] = np.angle(fit, deg=True)
        response[f"{name}_holdout_rao_magnitude"] = abs(test)
        response[f"{name}_holdout_rao_phase_deg"] = np.angle(test, deg=True)
        response[f"{name}_holdout_phase_shift_deg"] = np.angle(test / fit, deg=True)
        response[f"{name}_holdout_error_ratio"] = error
        response[f"{name}_prescribed_rao_magnitude"] = abs(paper)
        response[f"{name}_prescribed_rao_phase_deg"] = np.angle(paper, deg=True)
        response[f"{name}_first_harmonic_peak"] = abs(fit) * amplitude
    radar = []
    for pose_name, (pitch_rao, heave_rao) in {
        "empirical": (pitch_fit, heave_fit),
        "empirical_holdout_fit": (pitch_test, heave_test),
        "prescribed": (pitch_paper, heave_paper),
    }.items():
        pose = harmonic_pose(pitch_rao * model.RAD, heave_rao)
        for bearing in (0, 45, 90):
            radar.extend(replay_radar(response, pose_name, pose, bearing))
        if index == 2 and pose_name != "prescribed":
            for label, pitch_sign, heave_sign in (
                ("pitch_reversed", -1, 1),
                ("heave_reversed", 1, -1),
                ("both_reversed", -1, -1),
            ):
                changed_pose = harmonic_pose(
                    pitch_sign * pitch_rao * model.RAD, heave_sign * heave_rao
                )
                radar.extend(replay_radar(response, f"{pose_name}_{label}", changed_pose, 45))
    return response, radar


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_directory", type=Path)
    parser.add_argument("--response", type=Path, required=True)
    parser.add_argument("--retrofit", type=Path, required=True)
    args = parser.parse_args()
    raw = raw_attitude(args.source_directory)
    responses, radar = [], []
    for index, ratio in enumerate(WAVELENGTH_RATIOS, start=2):
        response, experiments = run_benchmark(args.source_directory, index, ratio, raw)
        responses.append(response)
        radar.extend(experiments)
        print(
            index,
            response["frequency_hz"],
            response["wave_amplitude_m"],
            response["pitch_rao_phase_deg"],
            response["heave_rao_phase_deg"],
            response["pitch_holdout_error_ratio"],
            response["heave_holdout_error_ratio"],
        )
        for row in experiments:
            print(
                row["response"],
                row["bearing_deg"],
                row["tolerance_m"],
                row["body_midpoint_error_p95_m"],
                row["body_registration_gain_pp"],
                row["stand_alone_pointing_gain_pp"],
                row["pointing_after_registration_gain_pp"],
                row["interaction_pp"],
            )
    write_csv(args.response, responses)
    write_csv(args.retrofit, radar)


if __name__ == "__main__":
    main()
