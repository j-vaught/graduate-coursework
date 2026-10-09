"""Independent analytic and numerical checks of the shared BlueBoat model."""

from __future__ import annotations

import json
from typing import Any

import numpy as np
from scipy.linalg import null_space

from propulsion import CONFIG, FORCE, PWM, realizable_force, static_force
from simulate import DATA, FloatArray, P, rhs, run, write_json


def linearization(speed: float) -> tuple[FloatArray, FloatArray]:
    a = np.zeros((6, 6))
    a[0, 3] = 1
    a[1, 2] = speed
    a[1, 4] = 1
    a[2, 5] = 1
    a[3, 3] = -(P.surge_linear_N_s_m + 2 * P.surge_quadratic_N_s2_m2 * abs(speed)) / P.mass_kg
    a[4, 4] = -P.sway_linear_N_s_m / P.mass_kg
    a[4, 5] = -speed
    a[5, 5] = -P.yaw_linear_N_m_s / P.yaw_inertia_kg_m2
    b = np.zeros((6, 2))
    b[3] = 1 / P.mass_kg
    b[5] = np.array([-1, 1]) * P.thruster_spacing_m / (2 * P.yaw_inertia_kg_m2)
    return a, b


def main() -> None:
    runs = json.loads((DATA / "runs.json").read_text())
    checks: dict[str, Any] = {}
    total = 2 * realizable_force(15)
    root = np.sqrt(P.surge_linear_N_s_m**2 + 4 * P.surge_quadratic_N_s2_m2 * total)
    positive = (-P.surge_linear_N_s_m + root) / (2 * P.surge_quadratic_N_s2_m2)
    negative = (-P.surge_linear_N_s_m - root) / (2 * P.surge_quadratic_N_s2_m2)
    t = np.asarray(runs["equal"]["time"])
    exponential = np.exp(-root / P.mass_kg * np.maximum(t - 1, 0))
    exact_surge = positive * (1 - exponential) / (1 - positive / negative * exponential)
    checks["surge_exact_max_error_m_s"] = float(np.max(np.abs(exact_surge - runs["equal"]["u"])))
    t = np.asarray(runs["differential"]["time"])
    torque = P.thruster_spacing_m / 2 * (realizable_force(15) - realizable_force(10))
    exact_yaw = (
        torque
        / P.yaw_linear_N_m_s
        * (1 - np.exp(-P.yaw_linear_N_m_s / P.yaw_inertia_kg_m2 * np.maximum(t - 1, 0)))
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
        P.thrust_min_N - 1e-10 <= min(result[field])
        and max(result[field]) <= P.thrust_max_N + 1e-10
        for result in runs.values()
        for field in ("left", "right")
    )
    checks["installed_forward_rating_matches_N"] = bool(
        np.isclose(2 * FORCE.max(), CONFIG["installed_forward_thrust_kgf"] * 9.80665)
    )
    checks["payload_within_capacity"] = (
        CONFIG["battery_mass_total_kg"] + CONFIG["equipment_allowance_kg"]
        <= CONFIG["batteries_plus_payload_limit_kg"]
    )
    checks["spacing_inside_beam"] = 0 < P.thruster_spacing_m < CONFIG["beam_m"]
    checks["shared_blueboat_parameters"] = all(
        result["platform"] == "BlueBoat" and result["parameters"]["mass_kg"] == P.mass_kg
        for result in runs.values()
    )
    checks["signed_thrust_map_monotone"] = bool(
        np.all(np.diff([static_force(pwm) for pwm in PWM]) >= 0)
    )
    controls = []
    for speed in (0.0, 1.0):
        a, b = linearization(speed)
        controllability = np.hstack([np.linalg.matrix_power(a, power) @ b for power in range(6)])
        rank = int(np.linalg.matrix_rank(controllability))
        unreachable = null_space(controllability.T)
        modes = np.linalg.eigvals(unreachable.T @ a @ unreachable)
        force = P.surge_linear_N_s_m * speed + P.surge_quadratic_N_s2_m2 * speed**2
        controls.append(
            {
                "surge_speed_m_s": speed,
                "controllability_rank": rank,
                "uncontrollable_real_eigenvalues": modes.real.tolist(),
                "A": a.tolist(),
                "B": b.tolist(),
                "trim_total_force_N": force,
                "trim_within_limits": P.thrust_min_N <= force / 2 <= P.thrust_max_N,
            }
        )
        state = np.array([0, 0, 0, speed, 0, 0], dtype=float)
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
    metrics = {
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
        "blind_90s_states": {
            name: {field: runs[f"blind_{name}"][field][-1] for field in ("x", "y", "u", "distance")}
            for name in ("calm", "crosswind", "headwind")
        },
        "differential_endpoint_m": [runs["differential"]["x"][-1], runs["differential"]["y"][-1]],
        "turning_radius_m": float(
            np.hypot(runs["differential"]["u"][-1], runs["differential"]["v"][-1])
            / abs(runs["differential"]["r"][-1])
        ),
        "surge_total_force_N": float(total),
        "differential_yaw_moment_N_m": float(torque),
    }
    assert checks["surge_exact_max_error_m_s"] < 1e-8
    assert checks["yaw_exact_max_error_rad_s"] < 1e-8
    assert checks["wind_exact_max_error_m"] < 1e-8
    assert checks["step_refinement_max_state_difference"] < 1e-7
    assert checks["linearization_0_max_jacobian_error"] < 1e-6
    assert checks["linearization_1_max_jacobian_error"] < 1e-6
    assert all(value for value in checks.values() if isinstance(value, bool))
    assert [case["controllability_rank"] for case in controls] == [4, 6]
    assert all(case["trim_within_limits"] for case in controls)
    write_json(
        DATA / "validation.json",
        {
            "checks": checks,
            "convergence": convergence,
            "control_analysis": controls,
            "metrics": metrics,
            "validation_scope": "Analytic consistency, numerical convergence, physical bounds, and common configuration. No on-water validation or slide-curve matching.",
        },
    )
    write_json(
        DATA / "analytic_checks.json",
        {
            "surge": {"time": runs["equal"]["time"], "exact": exact_surge.tolist()},
            "wind": {"time": runs["wind"]["time"], "exact": exact_wind.tolist()},
        },
    )
    print(json.dumps({"checks": checks, "metrics": metrics}, indent=2))


if __name__ == "__main__":
    main()
