"""Independent analytic, numerical, and slide-image checks for the reconstruction."""

from __future__ import annotations

import json
from typing import Any

import numpy as np
from scipy.linalg import null_space

from simulate import DATA, FloatArray, P, rhs, run, write_json


def linearization(speed: float) -> tuple[FloatArray, FloatArray]:
    a = np.zeros((6, 6))
    a[0, 3] = 1
    a[1, 2] = speed
    a[1, 4] = 1
    a[2, 5] = 1
    a[3, 3] = -(P.surge_linear_N_s_m + 2 * P.surge_quadratic_N_s2_m2 * speed) / P.mass_kg
    a[4, 4] = -P.sway_linear_N_s_m / P.mass_kg
    a[4, 5] = -speed
    a[5, 5] = -P.yaw_linear_N_m_s / P.yaw_inertia_kg_m2
    b = np.zeros((6, 2))
    b[3] = 1 / P.mass_kg
    b[5] = np.array([-1, 1]) * P.thruster_spacing_m / (2 * P.yaw_inertia_kg_m2)
    return a, b


def main() -> None:
    runs = json.loads((DATA / "runs.json").read_text())
    traces = json.loads((DATA / "slide_traces.json").read_text())
    checks: dict[str, Any] = {}
    root = np.sqrt(P.surge_linear_N_s_m**2 + 4 * P.surge_quadratic_N_s2_m2 * 200)
    positive = (-P.surge_linear_N_s_m + root) / (2 * P.surge_quadratic_N_s2_m2)
    negative = (-P.surge_linear_N_s_m - root) / (2 * P.surge_quadratic_N_s2_m2)
    t = np.asarray(runs["equal"]["time"])
    exponential = np.exp(-root / P.mass_kg * np.maximum(t - 1, 0))
    exact_surge = positive * (1 - exponential) / (1 - positive / negative * exponential)
    checks["surge_exact_max_error_m_s"] = float(np.max(np.abs(exact_surge - runs["equal"]["u"])))
    t = np.asarray(runs["differential"]["time"])
    exact_yaw = 0.15 * (
        1 - np.exp(-P.yaw_linear_N_m_s / P.yaw_inertia_kg_m2 * np.maximum(t - 1, 0))
    )
    checks["yaw_exact_max_error_rad_s"] = float(
        np.max(np.abs(exact_yaw - runs["differential"]["r"]))
    )
    t = np.asarray(runs["wind"]["time"])
    tau = P.mass_kg / P.sway_linear_N_s_m
    wind_speed = P.wind_force_N / P.sway_linear_N_s_m
    exact_wind = wind_speed * (t - tau * (1 - np.exp(-t / tau)))
    checks["wind_exact_max_error_m"] = float(np.max(np.abs(exact_wind - runs["wind"]["y"])))
    decay = np.asarray(runs["decay"]["states"])
    energy = (
        0.5 * P.mass_kg * (decay[:, 3] ** 2 + decay[:, 4] ** 2)
        + 0.5 * P.yaw_inertia_kg_m2 * decay[:, 5] ** 2
    )
    checks["unforced_energy_monotone"] = bool(np.all(np.diff(energy) <= 1e-10))
    checks["initial_kinetic_energy_J"] = float(energy[0])
    convergence = []
    for name, result in runs.items():
        finer = run(
            name,
            result["time"][-1],
            result["segments"],
            tuple(result["states"][0]),
            tuple(result["wind_world_N"]),
            max_step=0.025,
        )
        error = float(np.max(np.abs(np.asarray(result["states"]) - np.asarray(finer["states"]))))
        convergence.append({"case": name, "max_state_difference": error})
    checks["step_refinement_max_state_difference"] = max(
        row["max_state_difference"] for row in convergence
    )
    checks["thrusters_within_limits"] = all(
        P.thrust_min_N <= min(result[field]) and max(result[field]) <= P.thrust_max_N
        for result in runs.values()
        for field in ("left", "right")
    )
    controls = []
    for speed in (0.0, 1.0):
        a, b = linearization(speed)
        controllability = np.hstack([np.linalg.matrix_power(a, power) @ b for power in range(6)])
        rank = int(np.linalg.matrix_rank(controllability))
        unreachable = null_space(controllability.T)
        modes = np.linalg.eigvals(unreachable.T @ a @ unreachable)
        controls.append(
            {
                "surge_speed_m_s": speed,
                "controllability_rank": rank,
                "uncontrollable_real_eigenvalues": modes.real.tolist(),
                "A": a.tolist(),
                "B": b.tolist(),
            }
        )
        state = np.array([0, 0, 0, speed, 0, 0], dtype=float)
        force = P.surge_linear_N_s_m * speed + P.surge_quadratic_N_s2_m2 * speed**2
        h = 1e-6
        jacobian = np.column_stack(
            [
                (
                    rhs(state + np.eye(6)[i] * h, force / 2, force / 2, (0, 0))
                    - rhs(state - np.eye(6)[i] * h, force / 2, force / 2, (0, 0))
                )
                / (2 * h)
                for i in range(6)
            ]
        )
        checks[f"linearization_{speed:g}_max_jacobian_error"] = float(np.max(np.abs(jacobian - a)))
    comparisons = (
        ("equal_u", "equal", "u", "m/s", 439 / 1.4),
        ("differential_u", "differential", "u", "m/s", 517.5 / 2.6),
        ("differential_v", "differential", "v", "m/s", 517.5 / 2.6),
        ("differential_r", "differential", "r", "rad/s", 517.5 / 2.6),
        ("pulse_v", "pulse", "v", "m/s", 314.5 / 0.08),
        ("pulse_r", "pulse", "r", "rad/s", 285.33 / 0.4),
        ("decay_u", "decay", "u", "m/s", 421.5),
        ("decay_v", "decay", "v", "m/s", 421.5),
        ("decay_r", "decay", "r", "rad/s", 421.5),
        ("wind_y", "wind", "y", "m", 437 / 22),
        ("blind_calm_distance", "blind_calm", "distance", "m", 451 / 30),
        ("blind_crosswind_distance", "blind_crosswind", "distance", "m", 451 / 30),
        ("blind_headwind_distance", "blind_headwind", "distance", "m", 451 / 30),
    )
    rows = []
    residuals = {}
    for key, case, field, unit, pixels_per_unit in comparisons:
        points = np.asarray(traces[key])
        result = runs[case]
        error = np.interp(points[:, 0], result["time"], result[field]) - points[:, 1]
        rows.append(
            {
                "trace": key,
                "case": case,
                "field": field,
                "unit": unit,
                "samples": len(points),
                "rmse": float(np.sqrt(np.mean(error**2))),
                "max_abs_error": float(np.max(np.abs(error))),
                "rmse_pixels": float(np.sqrt(np.mean(error**2)) * pixels_per_unit),
                "pixels_per_unit": pixels_per_unit,
            }
        )
        residuals[key] = {"time": points[:, 0].tolist(), "error": error.tolist()}
    metrics: dict[str, Any] = {
        "surge_terminal_m_s": float(positive),
        "differential_terminal_u_m_s": runs["differential"]["u"][-1],
        "differential_terminal_v_m_s": runs["differential"]["v"][-1],
        "differential_terminal_r_rad_s": runs["differential"]["r"][-1],
        "pulse_peak_v_m_s": max(runs["pulse"]["v"]),
        "pulse_min_r_rad_s": min(runs["pulse"]["r"]),
        "drift_60s_m": runs["wind"]["y"][-1],
        "drift_terminal_m_s": wind_speed,
        "wind_time_constant_s": tau,
        "yaw_time_constant_s": P.yaw_inertia_kg_m2 / P.yaw_linear_N_m_s,
        "blind_90s_errors_m": {
            name: runs[f"blind_{name}"]["distance"][-1]
            for name in ("calm", "crosswind", "headwind")
        },
        "max_slide_rmse_pixels": max(float(row["rmse_pixels"]) for row in rows),
    }
    assert checks["surge_exact_max_error_m_s"] < 1e-8
    assert checks["yaw_exact_max_error_rad_s"] < 1e-8
    assert checks["wind_exact_max_error_m"] < 1e-8
    assert checks["unforced_energy_monotone"] and checks["thrusters_within_limits"]
    assert checks["step_refinement_max_state_difference"] < 1e-7
    assert checks["linearization_0_max_jacobian_error"] < 1e-6
    assert checks["linearization_1_max_jacobian_error"] < 1e-6
    assert metrics["max_slide_rmse_pixels"] < 1.0
    assert [case["controllability_rank"] for case in controls] == [4, 6]
    write_json(
        DATA / "validation.json",
        {
            "checks": checks,
            "convergence": convergence,
            "source_comparisons": rows,
            "control_analysis": controls,
            "metrics": metrics,
            "comparison_scope": "Raster trace agreement; the original solver and raw samples were not available.",
            "identification_scope": "Calm blind-schedule trace fitted; headwind and crosswind traces evaluated without refitting.",
        },
    )
    write_json(DATA / "residuals.json", residuals)
    print(json.dumps({"checks": checks, "metrics": metrics, "source_comparisons": rows}, indent=2))


if __name__ == "__main__":
    main()
