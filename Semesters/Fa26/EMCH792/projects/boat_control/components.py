"""Delayed M200 actuation and selected sensor models on the shared BlueBoat plant."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, replace
from itertools import pairwise
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp

from propulsion import FORCE, INSTALLATION_SCALE, RAW_FORCE, inverse_force, static_force
from simulate import DATA, FloatArray, P, rhs, run, write_json


@dataclass(frozen=True)
class ComponentAssumptions:
    controller_period_s: float = 0.020
    compute_s: float = 0.005
    command_transport_s: float = 0.010
    actuator_dead_time_s: float = 0.020
    thrust_time_constant_s: float = 0.200
    gnss_period_s: float = 0.050
    gnss_latency_s: float = 0.080
    gnss_position_sigma_m: float = 0.020
    gnss_velocity_sigma_m_s: float = 0.030
    imu_period_s: float = 0.005
    imu_latency_s: float = 0.005
    gyro_bias_rad_s: float = 0.001
    gyro_sigma_rad_s: float = 0.002
    accel_sigma_m_s2: float = 0.020
    heading_sigma_deg: float = 2.000
    camera_period_s: float = 1 / 30
    camera_acquisition_s: float = 0.010
    vision_compute_s: float = 0.020
    camera_width_px: float = 1920.0
    camera_fx_px: float = 700.0
    camera_cx_px: float = 960.0
    camera_center_sigma_px: float = 2.000
    camera_disparity_sigma_px: float = 0.500
    camera_baseline_m: float = 0.120
    camera_range_gate_m: float = 20.0
    gnss_heading_sigma_deg: float = 0.150
    gnss_primary_x_m: float = -0.500
    camera_target_x_m: float = 15.0
    camera_target_y_m: float = 3.0


A = ComponentAssumptions()


def wrap(angle: FloatArray) -> FloatArray:
    return (angle + np.pi) % (2 * np.pi) - np.pi


def desired(time: float, scenario: str) -> tuple[float, float]:
    if scenario == "motor":
        pwm = 1500 if time < 1.023 else 1950 if time < 3.023 else 1050 if time < 5.023 else 1500
        return pwm, pwm
    if scenario == "equal":
        return (inverse_force(15), inverse_force(15)) if time >= 1.023 else (1500, 1500)
    if scenario == "differential":
        return (inverse_force(8), inverse_force(10)) if 1.023 <= time < 6.023 else (1500, 1500)
    raise ValueError(scenario)


def plant(scenario: str, assumptions: ComponentAssumptions = A) -> dict[str, Any]:
    """Integrate exactly between delayed command events, with an eight-state plant."""
    duration = 12.0 if scenario != "motor" else 7.0
    time = np.linspace(0, duration, round(duration / 0.005) + 1)
    state = np.zeros(8)
    states = np.full((time.size, 8), np.nan)
    applied_setpoint = np.zeros((time.size, 2))
    ticks = np.arange(
        0, duration + assumptions.controller_period_s / 2, assumptions.controller_period_s
    )
    execution_delay = (
        assumptions.compute_s + assumptions.command_transport_s + assumptions.actuator_dead_time_s
    )
    events = [(0.0, (0.0, 0.0))]
    last = (0.0, 0.0)
    for tick in ticks:
        value = tuple(static_force(v) for v in desired(float(tick), scenario))
        event_time = float(tick + execution_delay)
        if value != last and event_time < duration:
            events.append((event_time, value))
            last = value
    events.append((duration, last))
    for (start, command), (end, _) in pairwise(events):

        def augmented_rhs(_time: float, z: FloatArray, demand=command) -> FloatArray:
            return np.r_[
                rhs(z[:6], float(z[6]), float(z[7]), (0, 0)),
                (np.asarray(demand) - z[6:]) / assumptions.thrust_time_constant_s,
            ]

        solution = solve_ivp(
            augmented_rhs,
            (start, end),
            state,
            rtol=1e-10,
            atol=1e-12,
            max_step=0.02,
            dense_output=True,
        )
        assert solution.success and solution.sol is not None
        indices = (time >= start) & (time <= end)
        states[indices] = solution.sol(time[indices]).T
        applied_setpoint[indices] = command
        state = solution.y[:, -1]
    assert np.isfinite(states).all()
    demand = np.asarray([desired(float(t), scenario) for t in time])
    result: dict[str, Any] = {
        "platform": "BlueBoat",
        "parameters": asdict(P),
        "time": time.tolist(),
        "states": states.tolist(),
        "events": [{"time": t, "left": v[0], "right": v[1]} for t, v in events[:-1]],
    }
    for i, key in enumerate(("x", "y", "psi", "u", "v", "r", "left", "right")):
        result[key] = states[:, i].tolist()
    result["demand_left"] = [static_force(v) for v in demand[:, 0]]
    result["pwm_demand_left"] = demand[:, 0].tolist()
    result["delayed_setpoint_left"] = applied_setpoint[:, 0].tolist()
    return result


def sensors(result: dict[str, Any]) -> dict[str, Any]:
    """Sample acquisition-time truth and deliver timestamped noisy measurements later."""
    truth_time = np.asarray(result["time"])
    truth_state = np.asarray(result["states"])
    duration = float(truth_time[-1])
    rng = np.random.default_rng(792)

    def sampled(period: float) -> tuple[FloatArray, FloatArray]:
        sample_time = np.arange(0, duration + period / 2, period)
        values = np.column_stack(
            [np.interp(sample_time, truth_time, truth_state[:, i]) for i in range(8)]
        )
        return sample_time, values

    gt, gz = sampled(A.gnss_period_s)
    velocity_e = gz[:, 3] * np.cos(gz[:, 2]) - gz[:, 4] * np.sin(gz[:, 2])
    velocity_n = gz[:, 3] * np.sin(gz[:, 2]) + gz[:, 4] * np.cos(gz[:, 2])
    gnss = {
        "sample_time": gt.tolist(),
        "available_time": (gt + A.gnss_latency_s).tolist(),
        "x": (
            gz[:, 0]
            + A.gnss_primary_x_m * np.cos(gz[:, 2])
            + rng.normal(0, A.gnss_position_sigma_m, gt.size)
        ).tolist(),
        "y": (
            gz[:, 1]
            + A.gnss_primary_x_m * np.sin(gz[:, 2])
            + rng.normal(0, A.gnss_position_sigma_m, gt.size)
        ).tolist(),
        "heading": wrap(
            gz[:, 2] + rng.normal(0, np.deg2rad(A.gnss_heading_sigma_deg), gt.size)
        ).tolist(),
        "solution_mode": "RTK_FIXED throughout this test; dropouts are not simulated",
        "velocity_e": (
            velocity_e
            - A.gnss_primary_x_m * gz[:, 5] * np.sin(gz[:, 2])
            + rng.normal(0, A.gnss_velocity_sigma_m_s, gt.size)
        ).tolist(),
        "velocity_n": (
            velocity_n
            + A.gnss_primary_x_m * gz[:, 5] * np.cos(gz[:, 2])
            + rng.normal(0, A.gnss_velocity_sigma_m_s, gt.size)
        ).tolist(),
    }
    it, iz = sampled(A.imu_period_s)
    derivatives = np.asarray([rhs(z[:6], z[6], z[7], (0, 0)) for z in iz])
    # At the center of mass, body acceleration includes rotating-frame terms.
    accel_x = derivatives[:, 3] - iz[:, 4] * iz[:, 5]
    accel_y = derivatives[:, 4] + iz[:, 3] * iz[:, 5]
    imu = {
        "sample_time": it.tolist(),
        "available_time": (it + A.imu_latency_s).tolist(),
        "r": (iz[:, 5] + A.gyro_bias_rad_s + rng.normal(0, A.gyro_sigma_rad_s, it.size)).tolist(),
        "accel_x": (accel_x + rng.normal(0, A.accel_sigma_m_s2, it.size)).tolist(),
        "accel_y": (accel_y + rng.normal(0, A.accel_sigma_m_s2, it.size)).tolist(),
        "heading": wrap(
            iz[:, 2] + rng.normal(0, np.deg2rad(A.heading_sigma_deg), it.size)
        ).tolist(),
        "heading_status": "proxy for calibrated magnetometer-aided attitude/heading output; raw magnetic field is not simulated",
    }
    ct, cz = sampled(A.camera_period_s)
    dx, dy = A.camera_target_x_m - cz[:, 0], A.camera_target_y_m - cz[:, 1]
    distance = np.hypot(dx, dy)
    beta = wrap(np.arctan2(dy, dx) - cz[:, 2])
    depth = distance * np.cos(beta)
    image_x = A.camera_cx_px - A.camera_fx_px * np.tan(beta)
    visible = (depth > 0) & (image_x >= 0) & (image_x <= A.camera_width_px)
    occluded = (ct >= 5) & (ct < 6)
    valid = visible & ~occluded
    image_x += rng.normal(0, A.camera_center_sigma_px, ct.size)
    disparity = A.camera_fx_px * A.camera_baseline_m / np.maximum(depth, 0.1)
    disparity += rng.normal(0, A.camera_disparity_sigma_px, ct.size)
    valid &= (image_x >= 0) & (image_x <= A.camera_width_px) & (disparity > 0)
    valid &= distance <= A.camera_range_gate_m
    bearing = np.arctan((A.camera_cx_px - image_x) / A.camera_fx_px)
    stereo_distance = A.camera_fx_px * A.camera_baseline_m / (disparity * np.cos(bearing))
    camera: dict[str, Any] = {
        "sample_time": ct.tolist(),
        "available_time": (ct + A.camera_acquisition_s + A.vision_compute_s).tolist(),
        "valid": valid.tolist(),
        "in_view": visible.tolist(),
        "occluded": occluded.tolist(),
        "true_bearing_deg": np.rad2deg(beta).tolist(),
        "true_distance": distance.tolist(),
        "model": "Rectified stereo target at camera height; frame aligned with boat CG for this planar test. No images or learned detections are rendered.",
    }
    for field, values in (
        ("image_x", image_x),
        ("disparity", disparity),
        ("bearing_deg", np.rad2deg(bearing)),
        ("stereo_distance", stereo_distance),
    ):
        camera[field] = [
            float(value) if accept else None for value, accept in zip(values, valid, strict=True)
        ]
    return {"gnss": gnss, "imu": imu, "camera": camera}


def main() -> None:
    DATA.mkdir(exist_ok=True)
    cases = {
        "motor": plant("motor"),
        "differential": plant("differential"),
        **{
            f"equal_{tau:g}": plant("equal", replace(A, thrust_time_constant_s=tau))
            for tau in (0.1, 0.2, 0.4)
        },
    }
    ideal = run("Ideal equal thrust", 12, [(0, 1.023, 0, 0), (1.023, 12, 15, 15)])
    cases["equal_ideal"] = ideal
    measured = sensors(cases["differential"])
    visibility_states = np.zeros((3, 8))
    visibility_states[:, 2] = (0, np.pi, np.pi / 2)
    visibility_test = sensors(
        {
            "time": [0, A.camera_period_s, 2 * A.camera_period_s],
            "states": visibility_states.tolist(),
        }
    )
    motor = cases["motor"]
    t = np.asarray(motor["time"])
    force = np.asarray(motor["left"])
    first_on = motor["events"][1]["time"]
    exact = FORCE.max() * (1 - np.exp(-np.maximum(t - first_on, 0) / A.thrust_time_constant_s))
    prior_to_reverse = t < motor["events"][2]["time"]
    max_error = float(np.max(np.abs(force[prior_to_reverse] - exact[prior_to_reverse])))
    measured_t90 = float(t[np.flatnonzero(force >= 0.9 * FORCE.max())[0]] - 1.023)
    period = A.controller_period_s
    execution = A.compute_s + A.command_transport_s + A.actuator_dead_time_s
    timing = {
        "controller_period_ms": 1000 * period,
        "compute_budget_ms": 1000 * A.compute_s,
        "transport_ms": 1000 * A.command_transport_s,
        "actuator_dead_time_ms": 1000 * A.actuator_dead_time_s,
        "demand_to_motor_onset_bound_ms": 1000 * (period + execution),
        "measured_test_onset_ms": 1000 * (first_on - 1.023),
        "motor_90_percent_from_demand_s": measured_t90,
        "motor_90_percent_after_onset_s": A.thrust_time_constant_s * np.log(10),
        "sensor_age_bounds_ms": {
            "gnss": 1000 * (A.gnss_period_s + A.gnss_latency_s),
            "imu": 1000 * (A.imu_period_s + A.imu_latency_s),
            "camera": 1000 * (A.camera_period_s + A.camera_acquisition_s + A.vision_compute_s),
        },
        "serial_compute_utilization_assumption": A.compute_s / period
        + A.vision_compute_s / A.camera_period_s,
    }
    noise = {
        "distance_m": np.linspace(5, 50, 91).tolist(),
        "sigma_range_m": (
            np.linspace(5, 50, 91) ** 2
            * A.camera_disparity_sigma_px
            / (A.camera_fx_px * A.camera_baseline_m)
        ).tolist(),
    }
    checks = {
        "actuator_exact_step_max_error_N": max_error,
        "force_within_bounds": all(
            np.min(case[side]) >= FORCE.min() - 1e-8 and np.max(case[side]) <= FORCE.max() + 1e-8
            for name, case in cases.items()
            if name != "equal_ideal"
            for side in ("left", "right")
        ),
        "camera_occlusion_invalid": all(
            not valid
            for time, valid in zip(
                measured["camera"]["sample_time"], measured["camera"]["valid"], strict=True
            )
            if 5 <= time < 6
        ),
        "camera_behind_or_out_of_view_invalid": all(
            not valid
            for in_view, valid in zip(
                measured["camera"]["in_view"], measured["camera"]["valid"], strict=True
            )
            if not in_view
        ),
        "camera_gate_test": visibility_test["camera"]["valid"] == [True, False, False],
        "stereo_inverse_exact": bool(
            np.isclose(
                A.camera_fx_px * A.camera_baseline_m / (A.camera_fx_px * A.camera_baseline_m / 10),
                10,
            )
        ),
        "neutral_deadband_zero": all(static_force(pwm) == 0 for pwm in (1475, 1500, 1525)),
        "pwm_saturation": bool(
            static_force(1950) == FORCE.max() and static_force(1050) == FORCE.min()
        ),
        "timestamps_causal": all(
            np.all(np.asarray(sensor["available_time"]) >= np.asarray(sensor["sample_time"]))
            for sensor in measured.values()
        ),
    }
    checks["shared_blueboat_parameters"] = all(
        case["platform"] == "BlueBoat" and case["parameters"] == asdict(P)
        for case in cases.values()
    )
    assert max_error < 1e-6
    assert all(checks[key] for key in checks if key != "actuator_exact_step_max_error_N")
    checks["first_order_90_percent_time_error_s"] = abs(
        (measured_t90 - (first_on - 1.023)) - A.thrust_time_constant_s * np.log(10)
    )
    assert checks["first_order_90_percent_time_error_s"] < 0.0051
    summary = {
        "camera_valid_frames": sum(measured["camera"]["valid"]),
        "camera_total_frames": len(measured["camera"]["valid"]),
        "ideal_surge_at_2s_m_s": float(np.interp(2, ideal["time"], ideal["u"])),
        "delayed_surge_at_2s_m_s": float(
            np.interp(2, cases["equal_0.2"]["time"], cases["equal_0.2"]["u"])
        ),
    }
    write_json(DATA / "component_assumptions.json", asdict(A))
    write_json(DATA / "component_runs.json", cases)
    write_json(DATA / "component_sensors.json", measured)
    write_json(
        DATA / "component_validation.json",
        {
            "checks": checks,
            "timing": timing,
            "summary": summary,
            "installation_scale": float(INSTALLATION_SCALE),
            "raw_forward_max_N": float(RAW_FORCE.max()),
            "installed_forward_max_N": float(FORCE.max()),
            "installed_reverse_min_N": float(FORCE.min()),
        },
    )
    write_json(DATA / "camera_range_sensitivity.json", noise)
    for name, case in cases.items():
        fields = ("time", "x", "y", "psi", "u", "v", "r", "left", "right")
        np.savetxt(
            DATA / f"component_{name}.csv",
            np.column_stack([case[field] for field in fields]),
            delimiter=",",
            header=",".join(fields),
            comments="",
            fmt="%.10g",
        )
    print(json.dumps({"checks": checks, "timing": timing, "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
