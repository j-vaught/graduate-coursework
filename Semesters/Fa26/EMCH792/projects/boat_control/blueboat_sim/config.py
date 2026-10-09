"""Validated experiment configuration and cumulative realism presets."""

from __future__ import annotations

import json
import math
import re
from dataclasses import asdict, dataclass, field, fields, replace
from pathlib import Path
from typing import Any

from propulsion import CONFIG


@dataclass(frozen=True)
class Flags:
    nonlinear_kinematics: bool = False
    nonlinear_coupling: bool = False
    nonlinear_drag: bool = False
    added_mass: bool = False
    nonlinear_thrust: bool = False
    thrust_saturation: bool = False
    neutral_deadband: bool = False
    reverse_asymmetry: bool = False
    motor_lag: bool = False
    motor_rate_limit: bool = False
    motor_mismatch: bool = False
    wind: bool = False
    gusts: bool = False
    apparent_wind: bool = False
    wind_yaw_moment: bool = False
    wave_forcing: bool = False
    command_sampling: bool = False
    command_delay: bool = False
    timing_jitter: bool = False
    missed_commands: bool = False
    command_watchdog: bool = False
    sensor_noise: bool = False
    sensor_bias: bool = False
    sensor_delay: bool = False
    sensor_dropout: bool = False
    antenna_lever_arm: bool = False
    camera_occlusion: bool = False
    gnss_enabled: bool = True
    imu_enabled: bool = True
    camera_enabled: bool = True
    perfect_state_feedback: bool = True


@dataclass(frozen=True)
class Hull:
    mass_scale: float = 1.0
    inertia_scale: float = 1.0
    thruster_spacing_m: float = CONFIG["thruster_spacing_m"]
    surge_linear_scale: float = 1.0
    surge_quadratic_scale: float = 1.0
    sway_linear_scale: float = 1.0
    yaw_linear_scale: float = 1.0
    sway_quadratic_N_s2_m2: float = 0.0
    yaw_quadratic_N_m_s2: float = 0.0
    added_surge_fraction: float = 0.1
    added_sway_fraction: float = 0.5
    added_yaw_fraction: float = 0.2


@dataclass(frozen=True)
class Actuator:
    lag_s: float = 0.2
    rate_limit_N_s: float = 80.0
    port_gain: float = 0.95
    starboard_gain: float = 1.05
    command_period_s: float = 0.02
    compute_delay_s: float = 0.005
    transport_delay_s: float = 0.01
    dead_time_s: float = 0.02
    jitter_max_s: float = 0.003
    missed_command_probability: float = 0.0
    command_timeout_s: float = 0.1


@dataclass(frozen=True)
class Environment:
    wind_speed_m_s: float = 5.0
    wind_direction_deg: float = 90.0
    wind_drag_coefficient: float = 1.0
    frontal_area_m2: float = CONFIG["frontal_wind_area_m2"]
    lateral_area_m2: float = CONFIG["lateral_wind_area_m2"]
    wind_center_x_m: float = 0.1
    wind_center_y_m: float = 0.0
    gust_sigma_m_s: float = 0.5
    gust_correlation_s: float = 1.0
    gust_period_s: float = 0.1
    wave_surge_N: float = 0.0
    wave_sway_N: float = 1.0
    wave_yaw_N_m: float = 0.1
    wave_period_s: float = 4.0


@dataclass(frozen=True)
class Sensors:
    gnss_period_s: float = 0.05
    imu_period_s: float = 0.005
    camera_period_s: float = 1 / 30
    gnss_delay_s: float = 0.08
    imu_delay_s: float = 0.005
    camera_delay_s: float = 0.03
    gnss_position_sigma_m: float = 0.02
    gnss_velocity_sigma_m_s: float = 0.03
    gnss_heading_sigma_rad: float = math.radians(0.15)
    gyro_sigma_rad_s: float = 0.002
    acceleration_sigma_m_s2: float = 0.02
    gyro_bias_rad_s: float = 0.001
    gnss_bias_e_m: float = 0.0
    gnss_bias_n_m: float = 0.0
    gnss_dropout_probability: float = 0.0
    imu_dropout_probability: float = 0.0
    camera_dropout_probability: float = 0.0
    gnss_x_m: float = -0.5
    camera_fx_px: float = 700.0
    camera_width_px: float = 1920.0
    camera_baseline_m: float = 0.12
    camera_disparity_sigma_px: float = 0.5
    camera_center_sigma_px: float = 2.0
    camera_max_range_m: float = 20.0
    occlusion_start_s: float = 5.0
    occlusion_end_s: float = 6.0
    target_e_m: float = 15.0
    target_n_m: float = 3.0


@dataclass(frozen=True)
class Experiment:
    name: str = "linear_baseline"
    duration_s: float = 12.0
    integration_step_s: float = 0.005
    log_period_s: float = 0.02
    seed: int = 792
    operating_speed_m_s: float = 1.0
    operating_heading_rad: float = 0.0
    initial_state: tuple[float, ...] = (0.0, 0.0, 0.0, 1.0, 0.0, 0.0)
    scenario: str = "turn"
    command_amplitude_us: float = 10.0
    flags: Flags = field(default_factory=Flags)
    hull: Hull = field(default_factory=Hull)
    actuator: Actuator = field(default_factory=Actuator)
    environment: Environment = field(default_factory=Environment)
    sensors: Sensors = field(default_factory=Sensors)

    def validate(self) -> None:
        if not isinstance(self.name, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", self.name):
            raise ValueError("name must contain letters, numbers, underscores, or hyphens")
        for name in ("operating_speed_m_s", "operating_heading_rad", "command_amplitude_us"):
            value = getattr(self, name)
            if (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
                or not math.isfinite(value)
            ):
                raise ValueError(f"{name} must be a finite number")
        for name in ("duration_s", "integration_step_s", "log_period_s"):
            value = getattr(self, name)
            if (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
                or not math.isfinite(value)
                or value <= 0
            ):
                raise ValueError(f"{name} must be finite and positive")
        if len(self.initial_state) != 6 or not all(
            isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)
            for v in self.initial_state
        ):
            raise ValueError("initial_state must contain six finite values: x,y,psi,u,v,r")
        if type(self.seed) is not int or self.seed < 0:
            raise ValueError("seed must be a nonnegative integer")
        if self.scenario not in ("straight", "turn", "pulse", "coast"):
            raise ValueError("scenario must be straight, turn, pulse, or coast")
        for spec in fields(self.flags):
            if type(getattr(self.flags, spec.name)) is not bool:
                raise ValueError(f"flags.{spec.name} must be a boolean")
        for group_name in ("hull", "actuator", "environment", "sensors"):
            group = getattr(self, group_name)
            for spec in fields(group):
                value = getattr(group, spec.name)
                if (
                    not isinstance(value, (int, float))
                    or isinstance(value, bool)
                    or not math.isfinite(value)
                ):
                    raise ValueError(f"{group_name}.{spec.name} must be a finite number")
                signed = spec.name in (
                    "wind_direction_deg",
                    "wind_center_x_m",
                    "wind_center_y_m",
                    "gnss_x_m",
                    "gnss_bias_e_m",
                    "gnss_bias_n_m",
                    "gyro_bias_rad_s",
                    "target_e_m",
                    "target_n_m",
                )
                if not signed and value < 0:
                    raise ValueError(f"{group_name}.{spec.name} must be nonnegative")
                if spec.name.endswith("_probability") and not 0 <= value <= 1:
                    raise ValueError(f"{group_name}.{spec.name} must be between 0 and 1")
        positive = (
            self.hull.mass_scale,
            self.hull.inertia_scale,
            self.hull.thruster_spacing_m,
            self.actuator.lag_s,
            self.actuator.rate_limit_N_s,
            self.actuator.command_period_s,
            self.actuator.command_timeout_s,
            self.environment.gust_period_s,
            self.environment.gust_correlation_s,
            self.environment.wave_period_s,
            self.sensors.gnss_period_s,
            self.sensors.imu_period_s,
            self.sensors.camera_period_s,
            self.sensors.camera_fx_px,
            self.sensors.camera_width_px,
            self.sensors.camera_baseline_m,
            self.sensors.camera_max_range_m,
        )
        if min(positive) <= 0:
            raise ValueError(
                "Mass, inertia, spacing, periods, lag, rate, and camera geometry must be positive"
            )
        if self.hull.thruster_spacing_m > CONFIG["beam_m"]:
            raise ValueError("Thruster spacing exceeds the standard hull beam")
        if self.sensors.occlusion_end_s < self.sensors.occlusion_start_s:
            raise ValueError("Occlusion interval is reversed")
        if self.flags.nonlinear_thrust and not self.flags.thrust_saturation:
            raise ValueError("The bounded manufacturer M200 lookup requires thrust_saturation=true")
        if (
            self.flags.gusts or self.flags.apparent_wind or self.flags.wind_yaw_moment
        ) and not self.flags.wind:
            raise ValueError("gusts, apparent_wind, and wind_yaw_moment require wind=true")
        if (
            self.flags.timing_jitter or self.flags.missed_commands or self.flags.command_watchdog
        ) and not self.flags.command_sampling:
            raise ValueError(
                "timing_jitter, missed_commands, and command_watchdog require command_sampling=true"
            )
        if self.flags.timing_jitter and not self.flags.command_delay:
            raise ValueError("timing_jitter requires command_delay=true")
        if self.duration_s / self.integration_step_s > 2_000_000:
            raise ValueError(
                "More than two million integration steps; shorten duration or increase step"
            )
        event_rates = [1 / self.log_period_s]
        for sensor in ("gnss", "imu", "camera"):
            if getattr(self.flags, sensor + "_enabled"):
                event_rates.append(2 / getattr(self.sensors, sensor + "_period_s"))
        if self.flags.command_sampling:
            event_rates.append(
                (3 if self.flags.command_watchdog else 2) / self.actuator.command_period_s
            )
        if self.flags.gusts:
            event_rates.append(1 / self.environment.gust_period_s)
        if self.duration_s * sum(event_rates) > 2_000_000:
            raise ValueError(
                "More than two million scheduled events; shorten duration or increase periods"
            )

    def resolved(self) -> dict[str, Any]:
        return asdict(self)


def from_dict(data: dict[str, Any]) -> Experiment:
    if not isinstance(data, dict):
        raise TypeError("Experiment configuration must be an object")
    allowed = {f.name for f in fields(Experiment)}
    if unknown := set(data) - allowed:
        raise ValueError(f"Unknown experiment keys: {sorted(unknown)}")
    kwargs = dict(data)
    for name, cls in (
        ("flags", Flags),
        ("hull", Hull),
        ("actuator", Actuator),
        ("environment", Environment),
        ("sensors", Sensors),
    ):
        if name in kwargs:
            if not isinstance(kwargs[name], dict):
                raise ValueError(f"{name} must be an object")
            if unknown := set(kwargs[name]) - {f.name for f in fields(cls)}:
                raise ValueError(f"Unknown {name} keys: {sorted(unknown)}")
            kwargs[name] = cls(**kwargs[name])
    if "initial_state" in kwargs:
        kwargs["initial_state"] = tuple(kwargs["initial_state"])
    result = Experiment(**kwargs)
    result.validate()
    return result


def load(path: Path) -> Experiment:
    return from_dict(json.loads(path.read_text()))


def presets() -> dict[str, Experiment]:
    stages = {
        "00_linear": {},
        "01_hull": {
            "nonlinear_kinematics": True,
            "nonlinear_coupling": True,
            "nonlinear_drag": True,
        },
        "02_m200": {
            "nonlinear_thrust": True,
            "thrust_saturation": True,
            "neutral_deadband": True,
            "reverse_asymmetry": True,
        },
        "03_motor": {"motor_lag": True, "motor_rate_limit": True},
        "04_timing": {"command_sampling": True, "command_delay": True},
        "05_sensors": {
            "sensor_noise": True,
            "sensor_bias": True,
            "sensor_delay": True,
            "antenna_lever_arm": True,
            "camera_occlusion": True,
            "perfect_state_feedback": False,
        },
        "06_disturbances": {
            "wind": True,
            "gusts": True,
            "apparent_wind": True,
            "wind_yaw_moment": True,
            "wave_forcing": True,
        },
        "07_uncertainty": {
            "added_mass": True,
            "motor_mismatch": True,
            "timing_jitter": True,
            "missed_commands": True,
            "command_watchdog": True,
            "sensor_dropout": True,
        },
    }
    flags = Flags()
    result = {}
    for name, changes in stages.items():
        flags = replace(flags, **changes)
        experiment = Experiment(name=name, flags=flags)
        if name == "07_uncertainty":
            experiment = replace(
                experiment,
                actuator=replace(experiment.actuator, missed_command_probability=0.02),
                sensors=replace(
                    experiment.sensors,
                    gnss_dropout_probability=0.05,
                    camera_dropout_probability=0.1,
                ),
            )
        experiment.validate()
        result[name] = experiment
    return result
