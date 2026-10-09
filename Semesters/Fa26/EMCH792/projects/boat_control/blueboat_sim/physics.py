"""Switchable local linearization and nonlinear planar dynamics."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from propulsion import CONFIG, FORCE, PWM

from .config import Experiment

Vector = NDArray[np.float64]


@dataclass(frozen=True)
class PhysicalParameters:
    mass: float
    inertia: float
    mx: float
    my: float
    iz: float
    d1: float
    d2: float
    dv: float
    dr: float


def physical(c: Experiment) -> PhysicalParameters:
    h = c.hull
    mass = (
        CONFIG["bare_mass_kg"] + CONFIG["battery_mass_total_kg"] + CONFIG["equipment_allowance_kg"]
    ) * h.mass_scale
    inertia = mass * (CONFIG["length_m"] ** 2 + CONFIG["beam_m"] ** 2) / 12 * h.inertia_scale
    return PhysicalParameters(
        mass,
        inertia,
        mass * (1 + h.added_surge_fraction * c.flags.added_mass),
        mass * (1 + h.added_sway_fraction * c.flags.added_mass),
        inertia * (1 + h.added_yaw_fraction * c.flags.added_mass),
        CONFIG["surge_linear_N_s_m"] * h.surge_linear_scale,
        CONFIG["surge_quadratic_N_s2_m2"] * h.surge_quadratic_scale,
        CONFIG["sway_linear_N_s_m"] * h.sway_linear_scale,
        CONFIG["yaw_linear_N_m_s"] * h.yaw_linear_scale,
    )


def trim(c: Experiment) -> tuple[float, float, float]:
    """Nominal forward trim and a local PWM slope, shared by the feature ladder."""
    p = physical(c)
    speed = c.operating_speed_m_s
    force = (p.d1 * speed + p.d2 * speed * abs(speed)) / 2
    if not FORCE.min() < force < FORCE.max():
        raise ValueError("Operating speed requires thrust outside the installed M200 map")
    pulse = 1500.0 if force == 0 else float(np.interp(force, FORCE, PWM))
    if force == 0:
        # A documented ideal zero-speed slope; the actual ESC has a deadband here.
        slope = float(FORCE.max() / 400)
    else:
        index = min(max(int(np.searchsorted(PWM, pulse)) - 1, 0), len(PWM) - 2)
        slope = float((FORCE[index + 1] - FORCE[index]) / (PWM[index + 1] - PWM[index]))
    return force, pulse, slope


def mapped_force(pwm: float, c: Experiment) -> float:
    f = c.flags
    if f.thrust_saturation:
        pwm = float(np.clip(pwm, 1100, 1900))
    if f.neutral_deadband and 1475 <= pwm <= 1525:
        return 0.0
    if f.nonlinear_thrust:
        if pwm < 1500 and not f.reverse_asymmetry:
            result = -float(np.interp(3000 - pwm, PWM, FORCE))
        else:
            result = float(np.interp(pwm, PWM, FORCE))
    else:
        force, pulse, slope = trim(c)
        result = force + slope * (pwm - pulse)
        if f.reverse_asymmetry and result < 0:
            result *= abs(float(FORCE.min() / FORCE.max()))
    if f.thrust_saturation:
        lower = float(FORCE.min()) if f.reverse_asymmetry else -float(FORCE.max())
        result = float(np.clip(result, lower, FORCE.max()))
    return result


def motor_target(pulses: tuple[float, float], c: Experiment) -> Vector:
    target = np.array([mapped_force(pulse, c) for pulse in pulses])
    if c.flags.motor_mismatch:
        target *= (c.actuator.port_gain, c.actuator.starboard_gain)
        if c.flags.thrust_saturation:
            lower = float(FORCE.min()) if c.flags.reverse_asymmetry else -float(FORCE.max())
            target = np.clip(target, lower, FORCE.max())
    return target


def motor_after(force: Vector, target: Vector, elapsed: float, c: Experiment) -> Vector:
    """Exact lag/ramp solution for a held target, including a force slew limit."""
    if not c.flags.motor_lag and not c.flags.motor_rate_limit:
        return target.copy()
    error = target - force
    magnitude = np.abs(error)
    sign = np.sign(error)
    if not c.flags.motor_lag:
        return force + sign * np.minimum(magnitude, c.actuator.rate_limit_N_s * elapsed)
    tau = c.actuator.lag_s
    if not c.flags.motor_rate_limit:
        return target - error * math.exp(-elapsed / tau)
    rate = c.actuator.rate_limit_N_s
    linear_time = np.maximum(magnitude - rate * tau, 0) / rate
    remaining = np.where(
        elapsed <= linear_time,
        magnitude - rate * elapsed,
        np.minimum(magnitude, rate * tau) * np.exp(-np.maximum(elapsed - linear_time, 0) / tau),
    )
    return target - sign * remaining


class Physics:
    def __init__(self, c: Experiment):
        self.c = c
        self.p = physical(c)
        if not c.flags.gusts:
            self.gust_times = np.array([0.0])
            self.gusts = np.zeros((1, 2))
            return
        rng = np.random.default_rng(np.random.SeedSequence([c.seed, 1]))
        self.gust_times = np.arange(
            0, c.duration_s + 2 * c.environment.gust_period_s, c.environment.gust_period_s
        )
        self.gusts = np.zeros((len(self.gust_times), 2))
        decay = math.exp(-c.environment.gust_period_s / c.environment.gust_correlation_s)
        for i in range(1, len(self.gust_times)):
            self.gusts[i] = decay * self.gusts[i - 1] + math.sqrt(1 - decay**2) * rng.normal(size=2)
        self.gusts *= c.environment.gust_sigma_m_s

    def wind_velocity(self, time: float) -> Vector:
        e = self.c.environment
        angle = math.radians(e.wind_direction_deg)
        velocity = e.wind_speed_m_s * np.array([math.cos(angle), math.sin(angle)])
        if self.c.flags.gusts:
            velocity += [np.interp(time, self.gust_times, self.gusts[:, i]) for i in range(2)]
        return velocity

    def disturbance(self, time: float, state: Vector) -> Vector:
        c, e = self.c, self.c.environment
        _, _, psi, u, v, _ = state[:6]
        cs, sn = math.cos(psi), math.sin(psi)
        force = np.zeros(3)
        if c.flags.wind:
            wind = self.wind_velocity(time)
            if c.flags.apparent_wind:
                wind -= (cs * u - sn * v, sn * u + cs * v)
            body = np.array([cs * wind[0] + sn * wind[1], -sn * wind[0] + cs * wind[1]])
            # Axis-wise projected-area drag; still an engineering approximation.
            force[:2] = (
                0.5
                * CONFIG["air_density_kg_m3"]
                * e.wind_drag_coefficient
                * np.array([e.frontal_area_m2, e.lateral_area_m2])
                * body
                * np.abs(body)
            )
            if c.flags.wind_yaw_moment:
                force[2] = e.wind_center_x_m * force[1] - e.wind_center_y_m * force[0]
        if c.flags.wave_forcing:
            force += np.array([e.wave_surge_N, e.wave_sway_N, e.wave_yaw_N_m]) * math.sin(
                2 * math.pi * time / e.wave_period_s
            )
        return force

    def rhs(self, time: float, state: Vector, thrust: Vector) -> Vector:
        c, p = self.c, self.p
        _, _, psi, u, v, r = state[:6]
        speed, heading = c.operating_speed_m_s, c.operating_heading_rad
        if c.flags.nonlinear_kinematics:
            cs, sn = math.cos(psi), math.sin(psi)
            dx, dy = cs * u - sn * v, sn * u + cs * v
        else:
            lateral = v + speed * (psi - heading)
            cs, sn = math.cos(heading), math.sin(heading)
            dx, dy = cs * u - sn * lateral, sn * u + cs * lateral
        if c.flags.nonlinear_drag:
            drag_u = p.d1 * u + p.d2 * u * abs(u)
            drag_v = p.dv * v + c.hull.sway_quadratic_N_s2_m2 * v * abs(v)
            drag_r = p.dr * r + c.hull.yaw_quadratic_N_m_s2 * r * abs(r)
        else:
            drag_u = (
                p.d1 * speed
                + p.d2 * speed * abs(speed)
                + (p.d1 + 2 * p.d2 * abs(speed)) * (u - speed)
            )
            drag_v, drag_r = p.dv * v, p.dr * r
        if c.flags.nonlinear_coupling:
            coupling = np.array([p.my * v * r, -p.mx * u * r, (p.mx - p.my) * u * v])
        else:
            coupling = np.array([0, -p.mx * speed * r, (p.mx - p.my) * speed * v])
        force = self.disturbance(time, state)
        effort = np.array([sum(thrust), 0, c.hull.thruster_spacing_m / 2 * (thrust[1] - thrust[0])])
        rates = (effort + force + coupling - (drag_u, drag_v, drag_r)) / (p.mx, p.my, p.iz)
        return np.r_[dx, dy, r, rates]

    def advance(self, time: float, state: Vector, target: Vector, step: float) -> Vector:
        def derivative(offset: float, z: Vector) -> Vector:
            return self.rhs(time + offset, z, motor_after(state[6:], target, offset, self.c))

        z = state[:6]
        a = derivative(0, z)
        b = derivative(step / 2, z + step / 2 * a)
        d = derivative(step / 2, z + step / 2 * b)
        e = derivative(step, z + step * d)
        return np.r_[
            z + step / 6 * (a + 2 * b + 2 * d + e), motor_after(state[6:], target, step, self.c)
        ]
