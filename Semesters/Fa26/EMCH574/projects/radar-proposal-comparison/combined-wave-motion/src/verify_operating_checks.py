"""Independent ODE, power and quadrature checks for the original illustrative model.

Run with numpy and scipy on COMECH or COCESR. Output is written to the
provided directory. Parameters for the original model come from config.json.
"""

import argparse
import csv
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


def forced_response(config):
    natural = 2 * np.pi * config["vessel_pitch_natural_hz"]
    zeta = config["vessel_pitch_damping"]
    static = config["static_pitch_deg"]
    rows = []
    for ratio in np.arange(0.2, 2.01, 0.1):
        omega = natural * ratio
        period = 2 * np.pi / omega
        time = np.linspace(60 * period, 65 * period, 2001)

        def rhs(t, state, omega=omega):
            return [
                state[1],
                natural**2 * static * np.cos(omega * t)
                - 2 * zeta * natural * state[1]
                - natural**2 * state[0],
            ]

        solution = solve_ivp(
            rhs,
            (0, time[-1]),
            (0, 0),
            t_eval=time,
            method="DOP853",
            rtol=1e-10,
            atol=1e-11,
            max_step=period / 25,
        )
        if not solution.success:
            raise RuntimeError(solution.message)
        design = np.column_stack((np.cos(omega * time), np.sin(omega * time)))
        cosine, sine = np.linalg.lstsq(design, solution.y[0], rcond=None)[0]
        amplitude = np.hypot(cosine, sine)
        phase = np.rad2deg(np.arctan2(sine, cosine))
        expected_amp = static / np.hypot(1 - ratio**2, 2 * zeta * ratio)
        expected_phase = np.rad2deg(np.arctan2(2 * zeta * ratio, 1 - ratio**2))
        rows.append(
            {
                "ratio": float(ratio),
                "numerical_amp_deg": float(amplitude),
                "analytical_amp_deg": float(expected_amp),
                "numerical_phase_deg": float(phase),
                "analytical_phase_deg": float(expected_phase),
                "relative_amplitude_error": float(abs(amplitude / expected_amp - 1)),
                "phase_error_deg": float(phase - expected_phase),
            }
        )
    return rows


def path_refinement(config):
    c = config
    f = c["wave_frequency_hz"]
    omega = 2 * np.pi * f
    k = omega**2 / c["gravity_m_s2"]
    kx = k * np.cos(np.deg2rad(c["wave_heading_deg"]))
    phase = np.arange(720) * 2 * np.pi / 720
    t = phase / omega

    def lag(fn, zeta):
        q = f / fn
        return np.arctan2(2 * zeta * q, 1 - q * q)

    def gain(fn, zeta):
        q = f / fn
        return 1 / np.hypot(1 - q * q, 2 * zeta * q)

    h = (
        c["wave_amplitude_m"]
        * gain(c["vessel_heave_natural_hz"], c["vessel_heave_damping"])
        * np.cos(-phase + lag(c["vessel_heave_natural_hz"], c["vessel_heave_damping"]))
    )
    ht = (
        c["wave_amplitude_m"]
        * gain(c["target_heave_natural_hz"], c["target_heave_damping"])
        * np.cos(
            kx * c["target_range_m"]
            - phase
            + lag(c["target_heave_natural_hz"], c["target_heave_damping"])
        )
    )
    q = f / c["vessel_pitch_natural_hz"]
    lagp = np.arctan2(2 * c["vessel_pitch_damping"] * q, 1 - q * q)
    pitch = (
        np.deg2rad(c["static_pitch_deg"])
        * gain(c["vessel_pitch_natural_hz"], c["vessel_pitch_damping"])
        * np.cos(phase - lagp)
    )
    roll = (
        c["roll_to_pitch_ratio"]
        * np.deg2rad(c["static_pitch_deg"])
        * gain(c["vessel_pitch_natural_hz"], c["vessel_pitch_damping"])
        * np.cos(phase - lagp + np.deg2rad(c["roll_phase_deg"]))
    )
    lever = np.array(c["lever_arm_m"])
    cr, sr = np.cos(roll), np.sin(roll)
    cp, sp = np.cos(pitch), np.sin(pitch)
    x0 = cp * lever[0] + sp * (sr * lever[1] + cr * lever[2])
    y0 = cr * lever[1] - sr * lever[2]
    z0 = (
        c["radar_reference_height_m"]
        - lever[2]
        + h
        - sp * lever[0]
        + cp * (sr * lever[1] + cr * lever[2])
    )
    x1 = np.full_like(t, c["target_range_m"])
    y1 = np.zeros_like(t)
    z1 = c["target_reference_height_m"] + ht
    distance = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2 + (z1 - z0) ** 2)

    def evaluate(samples):
        r = np.arange(1, samples) / samples
        x = x0[:, None] + r * (x1 - x0)[:, None]
        y = y0[:, None] + r * (y1 - y0)[:, None]
        z = z0[:, None] + r * (z1 - z0)[:, None]
        wave = c["wave_amplitude_m"] * np.cos(
            k
            * (
                x * np.cos(np.deg2rad(c["wave_heading_deg"]))
                + y * np.sin(np.deg2rad(c["wave_heading_deg"]))
            )
            - phase[:, None]
        )
        nu = (wave - z) * np.sqrt(2 / (c["radio_wavelength_m"] * distance[:, None] * r * (1 - r)))
        peak = nu.max(axis=1)
        loss = np.where(peak <= -0.78, 0, 6.9 + 20 * np.log10(np.hypot(peak - 0.1, 1) + peak - 0.1))
        return loss, (z - wave).min(axis=1)

    reference_loss, reference_clearance = evaluate(3200)
    rows = []
    for samples in (51, 101, 201, 401, 501, 801, 1600):
        loss, clearance = evaluate(samples)
        rows.append(
            {
                "path_samples": samples,
                "max_one_way_diffraction_error_db": float(np.max(abs(loss - reference_loss))),
                "max_clearance_error_m": float(np.max(abs(clearance - reference_clearance))),
                "phase_count": len(phase),
            }
        )
    return rows


def write_csv(path, rows):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()
    c = json.loads(Path(args.config).read_text())
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    rows = forced_response(c)
    paths = path_refinement(c)
    write_csv(out / "verification_forced_response.csv", rows)
    write_csv(out / "verification_path_convergence.csv", paths)
    # Each one-way pattern has half power at +/- beta/2. Two-way power is squared.
    beamwidth = 25.0
    one_way = np.exp(-4 * np.log(2) * (0.5 * beamwidth / beamwidth) ** 2)
    two_way_db = 10 * np.log10(one_way**2)
    speed = 2.0
    scan = 2.5
    sample_time = np.linspace(-scan / 2, scan / 2, 10001)
    midpoint_error = abs(speed * sample_time)
    checks = {
        "forced_response_max_relative_amplitude_error": max(
            r["relative_amplitude_error"] for r in rows
        ),
        "forced_response_max_abs_phase_error_deg": max(abs(r["phase_error_deg"]) for r in rows),
        "beamwidth_deg": beamwidth,
        "one_way_power_at_half_power_angle": one_way,
        "two_way_loss_db": -two_way_db,
        "constant_velocity_m_s": speed,
        "scan_period_s": scan,
        "midpoint_bound_m": speed * scan / 2,
        "midpoint_max_error_m": float(max(midpoint_error)),
        "original_model_path_convergence": paths,
        "limitations": (
            "Translation bound uses a constant velocity, perfect range and a common flat "
            "target plane. Path test applies to the prescribed single-wave illustrative "
            "model, not the new experiment."
        ),
    }
    (out / "verification_checks.json").write_text(json.dumps(checks, indent=2) + "\n")


if __name__ == "__main__":
    main()
