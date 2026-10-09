"""Causal event scheduling, sensor delivery, and a controller-ready PWM boundary."""

from __future__ import annotations

import heapq
import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict, dataclass
from types import MappingProxyType
from typing import Any

import numpy as np

from propulsion import CONFIG, STATIC

from .config import Experiment
from .physics import Physics, motor_target, physical, trim


@dataclass(frozen=True)
class Command:
    port_pwm_us: float
    starboard_pwm_us: float

    def validate(self) -> None:
        if not all(math.isfinite(v) for v in (self.port_pwm_us, self.starboard_pwm_us)):
            raise ValueError("PWM commands must be finite")


@dataclass(frozen=True)
class CommandChange:
    time_s: float
    command: Command


@dataclass(frozen=True)
class Measurement:
    sensor: str
    sample_time_s: float
    available_time_s: float
    values: Mapping[str, float | None]
    valid: bool


@dataclass(frozen=True)
class Observation:
    time_s: float
    measurements: Mapping[str, Measurement]
    perfect_state: tuple[float, ...] | None


Policy = Callable[[Observation], Command | None]


def default_commands(c: Experiment) -> list[CommandChange]:
    _, pulse, _ = trim(c)
    a = c.command_amplitude_us
    choices = {
        "straight": [(0, pulse, pulse), (2, pulse + a, pulse + a), (6, pulse, pulse)],
        "turn": [
            (0, pulse, pulse),
            (2, pulse + a, pulse + a),
            (4, pulse - a, pulse + a),
            (6, pulse, pulse),
        ],
        "pulse": [(0, pulse, pulse), (2, pulse + a, pulse - a), (3, pulse, pulse)],
        "coast": [(0, 1500, 1500)],
    }
    return [
        CommandChange(float(t), Command(float(l), float(r)))
        for t, l, r in choices[c.scenario]
        if t <= c.duration_s
    ]


def ticks(period: float, duration: float) -> list[float]:
    values = (np.arange(math.floor(duration / period + 1e-9) + 1) * period).tolist()
    return [float(v) for v in values if v <= duration + 1e-10]


def run(
    c: Experiment, commands: Sequence[CommandChange] | None = None, policy: Policy | None = None
) -> dict[str, Any]:
    c.validate()
    if policy is not None and not c.flags.command_sampling:
        raise ValueError("A policy requires command_sampling=true for explicit decision ticks")
    program = list(default_commands(c) if commands is None else commands)
    if not program or program[0].time_s != 0:
        raise ValueError("Command program must start at time zero")
    for i, change in enumerate(program):
        change.command.validate()
        if not math.isfinite(change.time_s) or change.time_s < 0 or change.time_s > c.duration_s:
            raise ValueError("Command times must be finite and within the run")
        if i and change.time_s <= program[i - 1].time_s:
            raise ValueError("Command change times must increase strictly")
    physics = Physics(c)
    trim_force, trim_pwm, slope = trim(c)
    state = np.r_[c.initial_state, trim_force, trim_force]
    target = state[6:].copy()
    latest: dict[str, Measurement] = {}
    sensor_records: dict[str, list[dict[str, Any]]] = {key: [] for key in ("gnss", "imu", "camera")}
    logs: list[list[float]] = []
    command_log: list[dict[str, Any]] = []
    actuation_log: list[dict[str, Any]] = []
    decision_log: list[dict[str, Any]] = []
    events: list[tuple[float, int, int, str, Any]] = []
    serial = 0

    def queue(time: float, priority: int, kind: str, payload: Any) -> None:
        nonlocal serial
        serial += 1
        heapq.heappush(events, (time, priority, serial, kind, payload))

    for name, period, enabled in (
        ("gnss", c.sensors.gnss_period_s, c.flags.gnss_enabled),
        ("imu", c.sensors.imu_period_s, c.flags.imu_enabled),
        ("camera", c.sensors.camera_period_s, c.flags.camera_enabled),
    ):
        if enabled:
            for t in ticks(period, c.duration_s):
                queue(t, 0, "acquire", name)
    for t in ticks(c.log_period_s, c.duration_s):
        queue(t, 4, "log", None)
    if abs(ticks(c.log_period_s, c.duration_s)[-1] - c.duration_s) > 1e-9:
        queue(c.duration_s, 4, "log", None)
    decision_times = (
        ticks(c.actuator.command_period_s, c.duration_s)
        if c.flags.command_sampling
        else [p.time_s for p in program]
    )
    for i, t in enumerate(decision_times):
        queue(t, 2, "decision", i)
    # Each channel has independent named streams, even when other flags change.
    sensor_rng = {
        name: np.random.default_rng(np.random.SeedSequence([c.seed, 10 + i]))
        for i, name in enumerate(sensor_records)
    }
    dropout_rng = {
        name: np.random.default_rng(np.random.SeedSequence([c.seed, 20 + i]))
        for i, name in enumerate(sensor_records)
    }
    timing_rng = np.random.default_rng(np.random.SeedSequence([c.seed, 30]))
    missed_rng = np.random.default_rng(np.random.SeedSequence([c.seed, 31]))

    def acquire(name: str, time: float) -> tuple[Measurement, dict[str, float], dict[str, Any]]:
        s, f = c.sensors, c.flags
        x, y, psi, u, v, r = state[:6]
        cs, sn = math.cos(psi), math.sin(psi)
        rng = sensor_rng[name]
        normal = rng.normal(size=6)
        dropout = dropout_rng[name].random() < getattr(s, name + "_dropout_probability")
        enabled_noise, enabled_bias = float(f.sensor_noise), float(f.sensor_bias)
        metadata: dict[str, Any] = {}
        if name == "gnss":
            ell = s.gnss_x_m if f.antenna_lever_arm else 0
            truth = {
                "x_m": x + ell * cs,
                "y_m": y + ell * sn,
                "heading_rad": psi,
                "velocity_e_m_s": cs * u - sn * v - ell * r * sn,
                "velocity_n_m_s": sn * u + cs * v + ell * r * cs,
            }
            sigma = np.array(
                [
                    s.gnss_position_sigma_m,
                    s.gnss_position_sigma_m,
                    s.gnss_heading_sigma_rad,
                    s.gnss_velocity_sigma_m_s,
                    s.gnss_velocity_sigma_m_s,
                ]
            )
            bias = np.array([s.gnss_bias_e_m, s.gnss_bias_n_m, 0, 0, 0])
            values = dict(
                zip(
                    truth,
                    (
                        np.array(list(truth.values()))
                        + enabled_noise * normal[:5] * sigma
                        + enabled_bias * bias
                    ).tolist(),
                    strict=True,
                )
            )
            valid, latency = True, s.gnss_delay_s
            metadata["solution_mode"] = "RTK_FIXED"
        elif name == "imu":
            dz = physics.rhs(time, state, state[6:])
            truth = {
                "yaw_rate_rad_s": r,
                "accel_x_m_s2": dz[3] - v * r,
                "accel_y_m_s2": dz[4] + u * r,
            }
            sigma = np.array(
                [s.gyro_sigma_rad_s, s.acceleration_sigma_m_s2, s.acceleration_sigma_m_s2]
            )
            bias = np.array([s.gyro_bias_rad_s, 0, 0])
            values = dict(
                zip(
                    truth,
                    (
                        np.array(list(truth.values()))
                        + enabled_noise * normal[:3] * sigma
                        + enabled_bias * bias
                    ).tolist(),
                    strict=True,
                )
            )
            valid, latency = True, s.imu_delay_s
        else:
            dx, dy = s.target_e_m - x, s.target_n_m - y
            depth, lateral = cs * dx + sn * dy, -sn * dx + cs * dy
            distance = math.hypot(dx, dy)
            truth = {"range_m": distance, "bearing_rad": math.atan2(lateral, depth)}
            center = s.camera_width_px / 2
            image_x = center - s.camera_fx_px * lateral / max(depth, 1e-9)
            disparity = s.camera_fx_px * s.camera_baseline_m / max(depth, 1e-9)
            image_x += enabled_noise * normal[0] * s.camera_center_sigma_px
            disparity += enabled_noise * normal[1] * s.camera_disparity_sigma_px
            occluded = f.camera_occlusion and s.occlusion_start_s <= time < s.occlusion_end_s
            valid = (
                depth > 0
                and 0 <= image_x <= s.camera_width_px
                and disparity > 0
                and distance <= s.camera_max_range_m
                and not occluded
            )
            bearing = math.atan((center - image_x) / s.camera_fx_px)
            estimated_range = (
                s.camera_fx_px * s.camera_baseline_m / max(disparity * math.cos(bearing), 1e-9)
            )
            values = {"range_m": estimated_range, "bearing_rad": bearing}
            latency = s.camera_delay_s
            metadata.update(occluded=occluded, depth_m=depth)
        valid = bool(valid and not (f.sensor_dropout and dropout))
        metadata["random_dropout"] = f.sensor_dropout and dropout
        if not valid:
            values = {key: None for key in values}
        arrival = time + (latency if f.sensor_delay else 0)
        measurement = Measurement(name, time, arrival, MappingProxyType(values), valid)
        return measurement, {key: float(v) for key, v in truth.items()}, metadata

    time, program_index = 0.0, 0
    current_pulses = (trim_pwm, trim_pwm)
    generation = 0
    watchdog_events: list[float] = []
    if c.flags.command_watchdog:
        queue(c.actuator.command_timeout_s, 3, "watchdog", generation)
    while events:
        event_time = events[0][0]
        if event_time > c.duration_s + 1e-9:
            break
        while time < event_time - 1e-12:
            step = min(c.integration_step_s, event_time - time)
            state = physics.advance(time, state, target, step)
            time += step
            if not np.isfinite(state).all():
                raise RuntimeError(
                    f"Nonfinite state at {time:g} s; reduce step or check parameters"
                )
        time, _, _, kind, payload = heapq.heappop(events)
        if kind == "acquire":
            measurement, truth, metadata = acquire(payload, time)
            record = {
                "sample_time_s": time,
                "available_time_s": measurement.available_time_s,
                "valid": measurement.valid,
                "values": dict(measurement.values),
                "truth": truth,
                "delivered": False,
                **metadata,
            }
            index = len(sensor_records[payload])
            sensor_records[payload].append(record)
            queue(measurement.available_time_s, 1, "deliver", (measurement, index))
        elif kind == "deliver":
            measurement, index = payload
            latest[measurement.sensor] = measurement
            sensor_records[measurement.sensor][index]["delivered"] = True
        elif kind == "decision":
            while (
                program_index + 1 < len(program)
                and program[program_index + 1].time_s <= time + 1e-12
            ):
                program_index += 1
            observation = Observation(
                time,
                MappingProxyType(latest.copy()),
                tuple(float(v) for v in state[:6]) if c.flags.perfect_state_feedback else None,
            )
            decision_log.append(
                {
                    "time_s": time,
                    "perfect_state_available": observation.perfect_state is not None,
                    "latest_sample_times_s": {
                        name: value.sample_time_s for name, value in latest.items()
                    },
                    "latest_delivery_times_s": {
                        name: value.available_time_s for name, value in latest.items()
                    },
                }
            )
            command = program[program_index].command if policy is None else policy(observation)
            jitter_draw, miss_draw = timing_rng.random(), missed_rng.random()
            if command is None:
                continue
            command.validate()
            missed = c.flags.missed_commands and miss_draw < c.actuator.missed_command_probability
            delay = (
                c.actuator.compute_delay_s + c.actuator.transport_delay_s + c.actuator.dead_time_s
                if c.flags.command_delay
                else 0
            )
            if c.flags.timing_jitter:
                delay += jitter_draw * c.actuator.jitter_max_s
            command_log.append(
                {
                    "time_s": time,
                    "apply_time_s": None if missed else time + delay,
                    "missed": missed,
                    "port_pwm_us": command.port_pwm_us,
                    "starboard_pwm_us": command.starboard_pwm_us,
                }
            )
            if not missed:
                queue(time + delay, 3, "apply", command)
        elif kind == "apply":
            generation += 1
            if c.flags.command_watchdog:
                queue(time + c.actuator.command_timeout_s, 3, "watchdog", generation)
            current_pulses = (payload.port_pwm_us, payload.starboard_pwm_us)
            target = motor_target(current_pulses, c)
            if not c.flags.motor_lag and not c.flags.motor_rate_limit:
                state[6:] = target
            actuation_log.append(
                {
                    "time_s": time,
                    "target_port_N": float(target[0]),
                    "target_starboard_N": float(target[1]),
                }
            )
        elif kind == "watchdog":
            if payload == generation:
                current_pulses = (1500.0, 1500.0)
                target = np.zeros(2)
                if not c.flags.motor_lag and not c.flags.motor_rate_limit:
                    state[6:] = target
                watchdog_events.append(time)
                actuation_log.append(
                    {
                        "time_s": time,
                        "target_port_N": 0.0,
                        "target_starboard_N": 0.0,
                        "watchdog": True,
                    }
                )
        elif kind == "log":
            logs.append([time, *state.tolist(), *current_pulses, *target.tolist()])
    history = np.asarray(logs)
    gnss_errors = []
    for record in sensor_records["gnss"]:
        if record["valid"] and record["delivered"]:
            gnss_errors.append(
                (record["values"]["x_m"] - record["truth"]["x_m"]) ** 2
                + (record["values"]["y_m"] - record["truth"]["y_m"]) ** 2
            )
    assumptions = [
        "platform.json loading, inertia, drag and installed thrust scaling remain provisional",
        "M200 map is a 16 V static snapshot; voltage discharge and propeller inflow are not modeled",
        "Added mass, wave forcing, motor mismatch/rate and latency parameters are engineering test assumptions",
        "GNSS status is fixed RTK; gyro/position biases and random missing samples are configurable approximations",
        "Stereo uses geometric observations, not generated images or detector inference",
    ]
    warnings = []
    if not (c.flags.nonlinear_kinematics and c.flags.nonlinear_coupling and c.flags.nonlinear_drag):
        warnings.append(
            "Local linear approximation; large speed/heading departures can leave its useful region"
        )
    if not c.flags.thrust_saturation:
        warnings.append(
            "Unbounded local actuator approximation; inspect force demand before physical interpretation"
        )
    if physical(c).mass > CONFIG["bare_mass_kg"] + CONFIG["batteries_plus_payload_limit_kg"]:
        warnings.append("Selected mass exceeds the published loaded-mass envelope")
    return {
        "schema_version": 1,
        "platform": "BlueBoat",
        "config": c.resolved(),
        "physical_parameters": asdict(physical(c)),
        "platform_source": CONFIG,
        "m200_source_sha256": STATIC["sha256"],
        "trim": {"force_each_N": trim_force, "pwm_us": trim_pwm, "slope_N_us": slope},
        "columns": [
            "time_s",
            "x_m",
            "y_m",
            "heading_rad",
            "surge_m_s",
            "sway_m_s",
            "yaw_rad_s",
            "port_N",
            "starboard_N",
            "port_pwm_us",
            "starboard_pwm_us",
            "target_port_N",
            "target_starboard_N",
        ],
        "history": logs,
        "measurements": sensor_records,
        "commands": command_log,
        "actuation_events": actuation_log,
        "decision_audit": decision_log,
        "watchdog_events_s": watchdog_events,
        "input_tape": [{"time_s": v.time_s, **asdict(v.command)} for v in program],
        "metrics": {
            "final_x_m": float(history[-1, 1]),
            "final_y_m": float(history[-1, 2]),
            "final_heading_rad": float(history[-1, 3]),
            "peak_force_N": float(np.max(np.abs(history[:, 7:9]))),
            "squared_force_integral_N2_s": float(
                np.trapezoid(np.sum(history[:, 7:9] ** 2, axis=1), history[:, 0])
            ),
            "gnss_position_rms_m": float(np.sqrt(np.mean(gnss_errors))) if gnss_errors else None,
            "valid_delivered_camera_frames": sum(
                v["valid"] and v["delivered"] for v in sensor_records["camera"]
            ),
            "missed_commands": sum(v["missed"] for v in command_log),
            "watchdog_trips": len(watchdog_events),
        },
        "assumptions": assumptions,
        "warnings": warnings,
    }
