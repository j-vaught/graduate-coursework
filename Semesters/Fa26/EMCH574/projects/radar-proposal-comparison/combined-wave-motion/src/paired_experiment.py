"""Paired radar visits for the wave-driven correction study.

Run with Python, NumPy and SciPy on the designated compute server.
All numerical values in this model are documented assumptions except the
antenna beamwidth and scan period from the DRS4D-NXT manufacturer's manual.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from pathlib import Path
from typing import TypedDict

import numpy as np
from numpy.typing import NDArray

G = 9.81
RAD = np.pi / 180
BETA = 25 * RAD
PERIOD = 2.5
NATURAL = 0.35
DAMPING = 0.15
WAVELENGTH = 0.03
RANGE = 100.0
HEADING = 25 * RAD
RADAR_HEIGHT = 2.0
TARGET_HEIGHT = 0.22
LEVER = np.array([0.6, 0.0, 0.8])
MARGIN = 10.0
TOLERANCE = 0.5
SEED = 5742026
HULL_PITCH_GAIN = 0.25
MAX_STEEPNESS = 0.20
MAX_ANGLE_DEG = 10.0
PitchResponse = Callable[[NDArray[np.float64]], NDArray[np.float64]]


class SensitivityInputs(TypedDict, total=False):
    damping: float
    margin: float
    tol: float
    scan: float
    irregular: bool
    scan_offset: float
    height_sigma_m: float
    bearing_sigma_deg: float
    range_sigma_m: float


def rotation(pitch, roll):
    cp, sp = np.cos(pitch), np.sin(pitch)
    cr, sr = np.cos(roll), np.sin(roll)
    r = np.empty((len(pitch), 3, 3))
    r[:, 0, 0] = cp
    r[:, 0, 1] = sp * sr
    r[:, 0, 2] = sp * cr
    r[:, 1, 0] = 0
    r[:, 1, 1] = cr
    r[:, 1, 2] = -sr
    r[:, 2, 0] = -sp
    r[:, 2, 1] = cp * sr
    r[:, 2, 2] = cp * cr
    return r


def transfer(freq, natural, damping):
    r = freq / natural
    return 1.0 / (1.0 - r * r + 2j * damping * r)


def components(freq, amplitude, phase, irregular=False):
    if irregular:
        ratios = np.array([0.72, 0.83, 0.92, 1.0, 1.08, 1.18, 1.29])
        weights = np.array([0.08, 0.13, 0.19, 0.23, 0.19, 0.12, 0.06])
        rng = np.random.default_rng(SEED + phase)
        ph = rng.uniform(0, 2 * np.pi, len(ratios))
        # RMS surface elevation matches a regular wave of the same amplitude.
        amplitudes = amplitude * np.sqrt(weights)
        return freq * ratios, amplitudes, ph
    rng = np.random.default_rng(SEED + phase)
    return np.array([freq]), np.array([amplitude]), rng.uniform(0, 2 * np.pi, 1)


def wave(x, y, t, freq, amp, ph):
    x, y, t = np.broadcast_arrays(x, y, t)
    omega = 2 * np.pi * freq
    k = omega**2 / G
    theta = (
        k[:, None] * np.cos(HEADING) * x.ravel()[None, :]
        + k[:, None] * np.sin(HEADING) * y.ravel()[None, :]
        - omega[:, None] * t.ravel()[None, :]
        + ph[:, None]
    )
    return (amp[:, None] * np.cos(theta)).sum(axis=0).reshape(x.shape)


def pose(
    t, freq, amp, ph, damping, pitch_phase=0.0, *, pitch_response: PitchResponse | None = None
):
    """Return antenna pose, optionally evaluating pitch from its regular-wave phase."""
    omega = 2 * np.pi * freq
    k = omega**2 / G
    wave_phase = omega[:, None] * t[None, :] - ph[:, None]
    exp_t = np.exp(1j * wave_phase)
    # Local slope is k a sin(omega t - phi). Positive Ry tilts the
    # bow down, so its slope-following pitch excitation has the opposite sign.
    if pitch_response is None:
        pitch = np.real(
            (
                1j
                * HULL_PITCH_GAIN
                * k
                * amp
                * np.cos(HEADING)
                * transfer(freq, NATURAL, damping)
                * np.exp(1j * pitch_phase)
            )[:, None]
            * exp_t
        ).sum(axis=0)
    else:
        if len(freq) != 1:
            raise ValueError("A periodic pitch response requires a single wave component")
        pitch = pitch_response(wave_phase[0] + pitch_phase)
    roll = np.real(
        (
            0.6
            * HULL_PITCH_GAIN
            * k
            * amp
            * np.sin(HEADING)
            * transfer(freq, NATURAL, damping)
            * np.exp(1j * np.pi / 3)
        )[:, None]
        * exp_t
    ).sum(axis=0)
    heave = np.real((amp * transfer(freq, 0.8, 0.3))[:, None] * exp_t).sum(axis=0)
    # Surge amplitude and phase are prescribed relative to the surface elevation.
    surge = np.real((1j * amp * np.cos(HEADING))[:, None] * exp_t).sum(axis=0)
    ref = np.column_stack((surge, np.zeros_like(t), RADAR_HEIGHT - LEVER[2] + heave))
    r = rotation(pitch, roll)
    origin = ref + np.einsum("nij,j->ni", r, LEVER)
    return origin, r, pitch, roll


def inverse_plane(rho, alpha, origin, r, height):
    body_a = np.column_stack((np.cos(alpha), np.sin(alpha), np.zeros(len(alpha))))
    a = np.einsum("nij,nj->ni", r, body_a)
    b = r[:, :, 2]
    vertical_projection = np.hypot(a[:, 2], b[:, 2])
    q = (height - origin[:, 2]) / (rho * vertical_projection)
    valid = np.abs(q) <= 1
    eps = np.arcsin(np.clip(q, -1, 1)) - np.arctan2(a[:, 2], b[:, 2])
    xyz = origin + rho[:, None] * (np.cos(eps)[:, None] * a + np.sin(eps)[:, None] * b)
    xyz[~valid] = np.nan
    return xyz


def run(
    freq,
    amplitude,
    phase,
    scan=PERIOD,
    damping=DAMPING,
    margin=MARGIN,
    tol=TOLERANCE,
    visits=128,
    samples=301,
    irregular=False,
    pitch_phase=0.0,
    times=None,
    bearing_sigma_deg=0.0,
    range_sigma_m=0.0,
    height_sigma_m=0.0,
    scan_offset=0.25,
    phase_origin=None,
    pitch_response: PitchResponse | None = None,
    surface_model=wave,
    pose_model=pose,
    *,
    target_azimuth_deg=0.0,
    component_model=components,
    horizontal_orbit=False,
):
    f, a, p = component_model(freq, amplitude, phase, irregular)
    if phase_origin is not None:
        assert not irregular
        p = np.array([phase_origin])
    # Scheduled spoke at a quarter rotation after scan midpoint.
    # The observed target bearing is applied at that acquisition instant.
    mid = (np.arange(visits) + 1) * scan
    t = mid + scan * scan_offset
    if times is not None:
        t = np.asarray(times)
        visits = len(t)
        mid = np.floor(t / scan + 0.5) * scan
    origin, r, pitch, roll = pose_model(
        t, f, a, p, damping, pitch_phase, pitch_response=pitch_response
    )
    midpoint, rm, _, _ = pose_model(
        mid, f, a, p, damping, pitch_phase, pitch_response=pitch_response
    )
    target_azimuth = target_azimuth_deg * RAD
    target_x = np.full(visits, RANGE * np.cos(target_azimuth))
    target_y = np.full(visits, RANGE * np.sin(target_azimuth))
    target = np.column_stack(
        (target_x, target_y, TARGET_HEIGHT + surface_model(target_x, target_y, t, f, a, p))
    )
    if horizontal_orbit:
        # The Airy-wave horizontal displacement is -a sin(phase) along propagation.
        # Evaluate both orbital components at the mean point to first order.
        displacement = wave(target_x, target_y, t, f, a, p + np.pi / 2)
        target[:, :2] += displacement[:, None] * np.array([np.cos(HEADING), np.sin(HEADING)])
    v = target - origin
    rho = np.linalg.norm(v, axis=1)
    body = np.einsum("nji,nj->ni", r, v)
    alpha = np.arctan2(body[:, 1], body[:, 0])
    level_angle = np.arctan2(v[:, 2], np.hypot(v[:, 0], v[:, 1]))
    body_angle = np.arctan2(body[:, 2], np.hypot(body[:, 0], body[:, 1]))

    fraction = np.arange(1, samples) / samples
    pos = origin[:, None, :] + fraction[None, :, None] * v[:, None, :]
    surface = surface_model(pos[:, :, 0], pos[:, :, 1], t[:, None], f, a, p)
    h = surface - pos[:, :, 2]
    nu = h * np.sqrt(2 / (WAVELENGTH * rho[:, None] * fraction[None, :] * (1 - fraction[None, :])))
    nu_max = np.max(nu, axis=1)
    loss = np.maximum(0.0, 6.9 + 20 * np.log10(np.hypot(nu_max - 0.1, 1) + nu_max - 0.1))
    loss[nu_max <= -0.78] = 0.0
    beam_loss = 80 * np.log10(2) * (body_angle / BETA) ** 2
    level_loss = 80 * np.log10(2) * (level_angle / BETA) ** 2
    margin_motion = margin - beam_loss - 2 * loss
    margin_level = margin - level_loss - 2 * loss
    detected = margin_motion >= 0
    detected_level = margin_level >= 0

    rng = np.random.default_rng(SEED + 100000 + phase)
    bearing_error = rng.normal(0, bearing_sigma_deg * RAD, visits)
    range_error = rng.normal(0, range_sigma_m, visits)
    measured_range = rho + range_error
    measured_alpha = alpha + bearing_error
    height_error = rng.normal(0, height_sigma_m, visits)
    measured_height = target[:, 2] + height_error
    correct = inverse_plane(measured_range, measured_alpha, origin, r, measured_height)
    baseline = inverse_plane(measured_range, measured_alpha, midpoint, rm, measured_height)
    err_baseline = np.linalg.norm(baseline[:, :2] - target[:, :2], axis=1)
    err_correct = np.linalg.norm(correct[:, :2] - target[:, :2], axis=1)
    # An ideal level antenna uses its level-frame azimuth and exact pose.
    level_alpha = np.arctan2(v[:, 1], v[:, 0]) + bearing_error
    level_r = np.broadcast_to(np.eye(3), (visits, 3, 3))
    stabilized = inverse_plane(measured_range, level_alpha, origin, level_r, measured_height)
    err_level = np.linalg.norm(stabilized[:, :2] - target[:, :2], axis=1)
    errors = np.array([err_baseline, err_correct, err_level])
    acquisitions = np.array([detected, detected, detected_level])
    usable = acquisitions & (errors <= tol) & np.isfinite(errors)
    below = (~acquisitions).mean(axis=1)
    outside = (acquisitions & ~usable).mean(axis=1)
    maxrun = []
    run_lengths = []
    for u in usable:
        runs = np.diff(np.flatnonzero(np.r_[True, u, True])) - 1
        maxrun.append(int(np.max(runs)))
        run_lengths.append(runs[runs > 0].tolist())
    assert np.allclose(below + outside + usable.mean(axis=1), 1)
    assert np.array_equal(acquisitions[0], acquisitions[1])
    return {
        "t": t,
        "pitch": pitch,
        "roll": roll,
        "wave": surface_model(np.zeros(visits), np.zeros(visits), t, f, a, p),
        "margin_motion": margin_motion,
        "margin_level": margin_level,
        "errors": errors,
        "positions": np.stack((baseline, correct, stabilized)),
        "acquired": acquisitions,
        "usable": usable,
        "below": below,
        "outside": outside,
        "maxrun": np.array(maxrun),
        "run_lengths": run_lengths,
        "surface_clearance": np.min(-h, axis=1),
        "slant": rho,
        "body_angle": body_angle,
        "level_angle": level_angle,
        "midpoint": midpoint,
        "origin": origin,
        "target": target,
    }


def summarize(runs):
    values = np.array([v["usable"].mean(axis=1) for v in runs])
    below = np.array([v["below"] for v in runs])
    outside = np.array([v["outside"] for v in runs])
    gain = values[:, 1] - values[:, 0]
    added = values[:, 2] - values[:, 1]

    # Equal-weight, independent realizations; normal intervals describe
    # realization-to-realization Monte Carlo variability.
    def interval_halfwidth(z):
        return 1.96 * np.std(z, axis=0, ddof=1) / np.sqrt(len(z))

    pooled = [[length for v in runs for length in v["run_lengths"][i]] for i in range(3)]
    realizations = []
    for phase_index, case in enumerate(runs):
        count = case["usable"].shape[1]
        acquired_count = case["acquired"].sum(axis=1)
        usable_count = case["usable"].sum(axis=1)
        realizations.append(
            {
                "phase_index": phase_index,
                "visits": count,
                "acquired_count": acquired_count.tolist(),
                "below_threshold_count": (count - acquired_count).tolist(),
                "acquired_outside_tolerance_count": (acquired_count - usable_count).tolist(),
                "usable_count": usable_count.tolist(),
                "unusable_run_lengths": case["run_lengths"],
            }
        )
    return {
        "realizations": realizations,
        "run_lengths": pooled,
        "fraction": values.mean(axis=0).tolist(),
        "fraction_ci95_halfwidth": interval_halfwidth(values).tolist(),
        "below": below.mean(axis=0).tolist(),
        "outside": outside.mean(axis=0).tolist(),
        "correction_gain": float(gain.mean()),
        "correction_ci95_halfwidth": float(interval_halfwidth(gain)),
        "stabilization_gain": float(added.mean()),
        "stabilization_ci95_halfwidth": float(interval_halfwidth(added)),
        "maxrun_mean": np.mean([v["maxrun"] for v in runs], axis=0).tolist(),
        "maxrun_p95": np.quantile([v["maxrun"] for v in runs], 0.95, axis=0).tolist(),
    }


def trace(r):
    fields = [
        "t",
        "wave",
        "pitch",
        "roll",
        "margin_motion",
        "margin_level",
        "errors",
        "acquired",
        "usable",
        "surface_clearance",
        "body_angle",
        "level_angle",
    ]
    return {k: r[k].tolist() for k in fields}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True)
    p.add_argument("--quick", action="store_true")
    args = p.parse_args()
    phases = 8 if args.quick else 32
    visits = 96 if args.quick else 192
    path_samples = 601
    grid = []
    frequencies = np.linspace(0.16, 0.62, 13) if args.quick else np.linspace(0.16, 0.62, 17)
    amplitudes = np.linspace(0.04, 0.60, 8) if args.quick else np.linspace(0.04, 0.60, 11)
    for f in frequencies:
        for a in amplitudes:
            k = (2 * np.pi * f) ** 2 / G
            peak_pitch = (
                HULL_PITCH_GAIN
                * k
                * a
                * np.cos(HEADING)
                * abs(transfer(np.array([f]), NATURAL, DAMPING)[0])
            )
            if k * a > MAX_STEEPNESS or peak_pitch / RAD > MAX_ANGLE_DEG:
                continue
            result = summarize(
                [run(f, a, k, visits=visits, samples=path_samples) for k in range(phases)]
            )
            grid.append(
                dict(
                    frequency_hz=float(f),
                    amplitude_m=float(a),
                    steepness=float(k * a),
                    peak_pitch_deg=float(peak_pitch / RAD),
                    **result,
                )
            )
    # Equal pitch amplitudes for an isolated test of dynamics and scan timing.
    matched = []
    target_pitch = 3 * RAD
    for f in [0.20, 0.28, 0.35, 0.42, 0.50]:
        needed = target_pitch / (
            HULL_PITCH_GAIN
            * abs(transfer(np.array([f]), NATURAL, DAMPING)[0])
            * ((2 * np.pi * f) ** 2 / G)
            * np.cos(HEADING)
        )
        if (2 * np.pi * f) ** 2 / G * needed > MAX_STEEPNESS:
            continue
        for scan in [1.25, 2.5, 3.75]:
            for coupling_phase in [0.0, np.pi / 2]:
                result = summarize(
                    [
                        run(
                            f,
                            needed,
                            k,
                            scan=scan,
                            pitch_phase=coupling_phase,
                            visits=visits,
                            samples=path_samples,
                        )
                        for k in range(phases)
                    ]
                )
                uniform = summarize(
                    [
                        run(
                            f,
                            needed,
                            k,
                            scan=scan,
                            pitch_phase=coupling_phase,
                            phase_origin=2 * np.pi * k / phases,
                            visits=visits,
                            samples=path_samples,
                        )
                        for k in range(phases)
                    ]
                )
                # Static benchmark assumes target at the beam center at rest,
                # pitch-only sinusoidal tilt, and no diffraction or mapping loss.
                angle_threshold = BETA * np.sqrt(MARGIN / (80 * np.log10(2)))
                static_fraction = (
                    1.0
                    if target_pitch <= angle_threshold
                    else 2 / np.pi * np.arcsin(angle_threshold / target_pitch)
                )
                matched.append(
                    dict(
                        frequency_hz=f,
                        amplitude_m=float(needed),
                        pitch_deg=3.0,
                        scan_s=scan,
                        pitch_phase_rad=coupling_phase,
                        static_beam_only_fraction=float(static_fraction),
                        uniform_phase_fraction=uniform["fraction"],
                        uniform_phase_maxrun_p95=uniform["maxrun_p95"],
                        steepness=float((2 * np.pi * f) ** 2 / G * needed),
                        **result,
                    )
                )
    frequencies_irr, amplitudes_irr, _ = components(0.35, 0.15, 0, True)
    wave_numbers_irr = (2 * np.pi * frequencies_irr) ** 2 / G
    wave_slope_bound = float(np.sum(wave_numbers_irr * amplitudes_irr))
    pitch_bound = float(
        np.sum(
            HULL_PITCH_GAIN
            * wave_numbers_irr
            * amplitudes_irr
            * np.cos(HEADING)
            * np.abs(transfer(frequencies_irr, NATURAL, DAMPING))
        )
        / RAD
    )
    roll_bound = float(
        np.sum(
            0.6
            * HULL_PITCH_GAIN
            * wave_numbers_irr
            * amplitudes_irr
            * np.sin(HEADING)
            * np.abs(transfer(frequencies_irr, NATURAL, DAMPING))
        )
        / RAD
    )
    assert wave_slope_bound <= MAX_STEEPNESS and max(pitch_bound, roll_bound) <= MAX_ANGLE_DEG
    sensitivity = []
    sensitivity_inputs: list[tuple[str, SensitivityInputs]] = [
        ("reference", {}),
        ("damping_low", {"damping": 0.12}),
        ("damping_high", {"damping": 0.30}),
        ("margin_5dB", {"margin": 5}),
        ("margin_15dB", {"margin": 15}),
        ("tolerance_0.25m", {"tol": 0.25}),
        ("tolerance_1m", {"tol": 1}),
        ("scan_36rpm", {"scan": 60 / 36}),
        ("scan_48rpm", {"scan": 60 / 48}),
        ("irregular", {"irregular": True}),
        ("scan_offset_zero", {"scan_offset": 0.0}),
        ("scan_offset_near_half", {"scan_offset": 0.49}),
        ("target_height_error_025m", {"height_sigma_m": 0.25}),
        ("measurement_noise_idealized", {"bearing_sigma_deg": 0.25, "range_sigma_m": 0.25}),
    ]
    for name, options in sensitivity_inputs:
        effective_damping = options.get("damping", DAMPING)
        reference_k = (2 * np.pi * 0.35) ** 2 / G
        peak_regular = (
            HULL_PITCH_GAIN
            * reference_k
            * 0.15
            * np.cos(HEADING)
            * abs(transfer(np.array([0.35]), NATURAL, effective_damping)[0])
            / RAD
        )
        assert reference_k * 0.15 <= MAX_STEEPNESS and peak_regular <= MAX_ANGLE_DEG
        result = summarize(
            [
                run(0.35, 0.15, k, visits=visits, samples=path_samples, **options)
                for k in range(phases)
            ]
        )
        sensitivity.append(dict(name=name, **result))
    # Find deterministic phase realization showing both mechanisms.
    candidates = []
    for f, a in [
        (0.35, 0.36),
        (0.30, 0.44),
        (0.35, 0.15),
        (0.35, 0.20),
        (0.40, 0.24),
        (0.45, 0.24),
        (0.50, 0.18),
    ]:
        if (2 * np.pi * f) ** 2 / G * a > MAX_STEEPNESS or HULL_PITCH_GAIN * (
            (2 * np.pi * f) ** 2 / G
        ) * a * np.cos(HEADING) * abs(
            transfer(np.array([f]), NATURAL, DAMPING)[0]
        ) / RAD > MAX_ANGLE_DEG:
            continue
        r = run(f, a, 0, visits=visits, samples=path_samples)
        both = np.any(~r["acquired"][0]) and np.any(r["acquired"][0] & ~r["usable"][0])
        candidates.append({"frequency_hz": f, "amplitude_m": a, "both": bool(both), "result": r})
    pilot = next((v for v in candidates if v["both"]), candidates[0])
    output = {
        "metadata": {
            "radar": "Furuno DRS4D-NXT",
            "radar_manual": "https://www.furunousa.com/-/media/sites/furuno/document_library/documents/manuals/public_manuals/ifr36490a_drs4dnxt.pdf",
            "vertical_beamwidth_deg": 25,
            "scan_period_s": 2.5,
            "physical_model": (
                "Regular deep-water component plus damped pitch/roll/heave and prescribed "
                "orbital surge; single effective knife-edge wave obstruction; "
                "deterministic threshold; known target elevation; ideal zero-latency "
                "per-spoke pose; level stabilized pointing."
            ),
            "assumptions": {
                "range_m": RANGE,
                "heading_deg": 25,
                "radar_height_m": RADAR_HEIGHT,
                "target_height_above_local_surface_m": TARGET_HEIGHT,
                "natural_frequency_hz": NATURAL,
                "damping_ratio": DAMPING,
                "hull_pitch_slope_gain": HULL_PITCH_GAIN,
                "max_regular_steepness": MAX_STEEPNESS,
                "max_angle_deg": MAX_ANGLE_DEG,
                "lever_arm_m": LEVER.tolist(),
                "margin_db": MARGIN,
                "position_tolerance_m": TOLERANCE,
                "wavelength_m": WAVELENGTH,
                "visit_phase_in_scan": 0.25,
                "reference_frequency_hz": 0.35,
                "reference_amplitude_m": 0.15,
                "phase_realizations": phases,
                "visits_per_realization": visits,
                "crest_samples": 601,
                "seed": SEED,
                "phase_cycle": "independent seeded uniform random wave phases",
                "irregular_steepness_bound": wave_slope_bound,
                "irregular_pitch_bound_deg": pitch_bound,
                "irregular_roll_bound_deg": roll_bound,
                "irregular": (
                    "seven independent random phases, prescribed spectrum with equal "
                    "wave-elevation RMS to regular case"
                ),
                "measurement_noise": (
                    "Sensitivity only: independent zero-mean Gaussian bearing and slant-range "
                    "error with prescribed standard deviations 0.25 deg and 0.25 m; common "
                    "draws pair processing cases. These illustrative error distributions are "
                    "not derived from manufacturer specifications."
                ),
                "caveat": (
                    "Target visit times are prescribed on a uniform schedule at a quarter "
                    "scan from the pose timestamp; platform motion does not shift spoke "
                    "acquisition time. Known instantaneous target height is supplied to "
                    "inverse geometry. Detection is deterministic, with no clutter or "
                    "receiver noise."
                ),
            },
            "classifications": [
                "mid_scan_pose",
                "per_spoke_pose",
                "ideal_level_pointing_per_spoke_pose",
            ],
            "confidence": (
                "95% normal interval of the mean across independently sampled phase "
                "realizations; gains paired per realization"
            ),
            "created": "2026-11-26",
        },
        "operating_map": grid,
        "matched_pitch": matched,
        "sensitivity": sensitivity,
        "pilot": {
            "frequency_hz": pilot["frequency_hz"],
            "amplitude_m": pilot["amplitude_m"],
            "phase": 0,
            "both_failure_types": pilot["both"],
            "trace": trace(pilot["result"]),
            "continuous": trace(
                run(
                    pilot["frequency_hz"],
                    pilot["amplitude_m"],
                    0,
                    samples=601,
                    times=np.arange(0, 40, 0.05),
                )
            ),
        },
    }
    Path(args.output).write_text(json.dumps(output, indent=2) + "\n")
    print(
        "Wrote",
        args.output,
        "grid cases",
        len(grid),
        "phases",
        phases,
        "visits",
        visits,
        "pilot",
        pilot["frequency_hz"],
        pilot["amplitude_m"],
        "both failures",
        pilot["both"],
    )
    print(
        "Reference fractions", next(v for v in sensitivity if v["name"] == "reference")["fraction"]
    )


if __name__ == "__main__":
    main()
