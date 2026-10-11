"""Three fixed-gain line-tracking policies with a shared causal sensor interface."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
from scipy.linalg import solve_continuous_are
from scipy.signal import place_poles

from propulsion import FORCE, inverse_force, static_force

from .config import presets
from .engine import Command, Measurement, Observation
from .physics import physical, trim


def wrap(angle: float) -> float:
    return math.atan2(math.sin(angle), math.cos(angle))


@dataclass(frozen=True)
class Settings:
    speed_m_s: float = 1.0
    line_n_m: float = 0.0
    use_m200_inverse: bool = True
    stale_gnss_s: float = 0.5
    stale_imu_s: float = 0.1
    speed_kp: float = 35.0
    speed_ki: float = 12.0
    speed_kd: float = 4.0
    heading_kp: float = 12.0
    heading_ki: float = 1.0
    heading_kd: float = 15.0
    cross_kp: float = 0.18
    cross_ki: float = 0.005
    heading_limit_rad: float = math.radians(35)
    derivative_filter_s: float = 0.1
    integral_speed_limit: float = 2.0
    integral_cross_limit: float = 12.0
    integral_heading_limit: float = 2.0


def design() -> dict[str, Any]:
    """Linearize the most complete nominal hull, including added inertia and motor lag.

    Surge coordinates are [du, delta total thrust, integral du]. Lateral
    coordinates are [cross track, psi, v, r, yaw moment, integral cross track].
    Commands are delta total thrust in N and yaw moment in Nm.
    """
    c = presets()["07_uncertainty"]
    p, tau, speed = physical(c), c.actuator.lag_s, c.operating_speed_m_s
    a_s = np.array(
        [
            [-(p.d1 + 2 * p.d2 * speed) / p.mx, 1 / p.mx, 0],
            [0, -1 / tau, 0],
            [1, 0, 0],
        ]
    )
    b_s = np.array([[0], [1 / tau], [0]])
    a_l = np.zeros((6, 6))
    a_l[0, 1], a_l[0, 2], a_l[1, 3] = speed, 1, 1
    a_l[2, 2], a_l[2, 3] = -p.dv / p.my, -p.mx * speed / p.my
    a_l[3, 2], a_l[3, 3], a_l[3, 4] = ((p.mx - p.my) * speed / p.iz, -p.dr / p.iz, 1 / p.iz)
    a_l[4, 4], a_l[5, 0] = -1 / tau, 1
    b_l = np.zeros((6, 1))
    b_l[4, 0] = 1 / tau
    systems = {
        "surge": (a_s, b_s, [25, 0.0025, 4], 0.01, [-0.5, -1.3, -5.5]),
        "lateral": (
            a_l,
            b_l,
            [4, 25, 11.111111, 25, 0.04, 0.111111],
            0.0625,
            [-0.25, -0.4, -0.7, -1.2, -3.0, -5.5],
        ),
    }
    result: dict[str, Any] = {
        "nominal_config": c.resolved(),
        "physical": asdict(p),
        "settings": asdict(Settings()),
        "systems": {},
    }
    for name, (a, b, weights, r, poles) in systems.items():
        q = np.diag(weights)
        riccati = solve_continuous_are(a, b, q, np.array([[r]]))
        k_lqr = b.T @ riccati / r
        k_pp = place_poles(a, b, poles).gain_matrix
        ctrb = np.hstack([np.linalg.matrix_power(a, i) @ b for i in range(len(a))])
        gains = {"lqr": k_lqr, "pole_placement": k_pp}
        result["systems"][name] = {
            "A": a.tolist(),
            "B": b.tolist(),
            "Q": q.tolist(),
            "R": r,
            "requested_poles": poles,
            "controllability_rank": int(np.linalg.matrix_rank(ctrb)),
            "gains": {key: value[0].tolist() for key, value in gains.items()},
            "poles": {
                key: [[float(z.real), float(z.imag)] for z in np.linalg.eigvals(a - b @ k)]
                for key, k in gains.items()
            },
            "riccati_residual": float(
                np.linalg.norm(a.T @ riccati + riccati @ a - riccati @ b @ b.T @ riccati / r + q)
            ),
        }
    return result


def measurement_value(m: Measurement, key: str) -> float:
    value = m.values[key]
    if value is None or not math.isfinite(value):
        raise ValueError(f"Valid {m.sensor} measurement has missing or nonfinite {key}")
    return float(value)


class SensorEstimate:
    """Timestamp extrapolation, lever-arm correction, and sample-and-hold velocity.

    This is deliberately a common minimal observer, not an EKF. It never sees
    simulation truth unless the explicit perfect-state flag supplies it.
    """

    def __init__(self, lever_arm_m: float, settings: Settings):
        self.lever = lever_arm_m
        self.settings = settings
        self.state = np.zeros(6)
        self.time = 0.0
        self.gnss: Measurement | None = None
        self.imu: Measurement | None = None

    def update(self, o: Observation) -> tuple[np.ndarray, bool]:
        if o.perfect_state is not None:
            self.state = np.asarray(o.perfect_state).copy()
            self.time = o.time_s
            return self.state.copy(), True
        dt = max(0.0, o.time_s - self.time)
        psi, u, v, r = self.state[2:]
        self.state[0] += dt * (math.cos(psi) * u - math.sin(psi) * v)
        self.state[1] += dt * (math.sin(psi) * u + math.cos(psi) * v)
        self.state[2] = wrap(psi + dt * r)
        for name in ("gnss", "imu"):
            m = o.measurements.get(name)
            previous = getattr(self, name)
            if (
                m is not None
                and m.valid
                and (previous is None or m.sample_time_s > previous.sample_time_s)
            ):
                setattr(self, name, m)
                if name == "imu":
                    self.state[5] = measurement_value(m, "yaw_rate_rad_s")
                else:
                    age = o.time_s - m.sample_time_s
                    r = self.state[5]
                    heading = measurement_value(m, "heading_rad")
                    cs, sn = math.cos(heading), math.sin(heading)
                    ve = measurement_value(m, "velocity_e_m_s") + self.lever * r * sn
                    vn = measurement_value(m, "velocity_n_m_s") - self.lever * r * cs
                    self.state[0] = measurement_value(m, "x_m") - self.lever * cs + age * ve
                    self.state[1] = measurement_value(m, "y_m") - self.lever * sn + age * vn
                    self.state[2] = wrap(heading + age * r)
                    cs, sn = math.cos(self.state[2]), math.sin(self.state[2])
                    self.state[3:5] = (cs * ve + sn * vn, -sn * ve + cs * vn)
        self.time = o.time_s
        ready = (
            self.gnss is not None
            and self.imu is not None
            and o.time_s - self.gnss.sample_time_s <= self.settings.stale_gnss_s
            and o.time_s - self.imu.sample_time_s <= self.settings.stale_imu_s
        )
        return self.state.copy(), ready


class Controller:
    def __init__(
        self,
        method: str,
        *,
        settings: Settings | None = None,
        lever_arm_m: float = -0.5,
        nominal_delay_s: float = 0.035,
    ):
        if method not in ("pid", "lqr", "pole_placement"):
            raise ValueError("Controller must be pid, lqr, or pole_placement")
        self.method, self.settings = method, settings or Settings()
        self.design = design()
        self.nominal = presets()["07_uncertainty"]
        self.trim_force, self.trim_pwm, self.slope = trim(self.nominal)
        self.estimate = SensorEstimate(lever_arm_m, self.settings)
        self.last_time = 0.0
        self.integrals = np.zeros(3)  # speed error, cross-track, heading error.
        self.motor_force = np.full(2, self.trim_force)
        self.pending: list[tuple[float, np.ndarray]] = []
        self.motor_target = self.motor_force.copy()
        self.nominal_delay = nominal_delay_s
        self.derivative = 0.0
        self.previous_speed_error = 0.0
        self.logs: list[dict[str, Any]] = []

    def __call__(self, o: Observation) -> Command:
        s = self.settings
        dt = max(0.0, o.time_s - self.last_time)
        # Advance the internal motor proxy at each scheduled command boundary.
        cursor = self.last_time
        while self.pending and self.pending[0][0] <= o.time_s + 1e-12:
            arrival, target = self.pending.pop(0)
            self.motor_force = target_lag(self.motor_force, self.motor_target, arrival - cursor)
            self.motor_target, cursor = target, arrival
        self.motor_force = target_lag(self.motor_force, self.motor_target, o.time_s - cursor)
        z, ready = self.estimate.update(o)
        y, psi, u, v, r = z[1], z[2], z[3], z[4], z[5]
        du, ey = u - s.speed_m_s, y - s.line_n_m
        candidate = self.integrals.copy()
        candidate[:2] += dt * np.array([du, ey])
        candidate[0] = np.clip(candidate[0], -s.integral_speed_limit, s.integral_speed_limit)
        candidate[1] = np.clip(candidate[1], -s.integral_cross_limit, s.integral_cross_limit)
        desired_heading = 0.0
        if self.method == "pid":
            beta = math.atan2(v, max(u, 0.2))
            desired_heading = float(
                np.clip(
                    -s.cross_kp * ey - s.cross_ki * candidate[1] - beta,
                    -s.heading_limit_rad,
                    s.heading_limit_rad,
                )
            )
            heading_error = wrap(psi - desired_heading)
            candidate[2] = np.clip(
                candidate[2] + dt * heading_error,
                -s.integral_heading_limit,
                s.integral_heading_limit,
            )
            if dt:
                alpha = dt / (s.derivative_filter_s + dt)
                self.derivative += alpha * ((du - self.previous_speed_error) / dt - self.derivative)
            total = (
                2 * self.trim_force
                - s.speed_kp * du
                - s.speed_ki * candidate[0]
                - s.speed_kd * self.derivative
            )
            moment = -s.heading_kp * heading_error - s.heading_ki * candidate[2] - s.heading_kd * r
        else:
            systems = self.design["systems"]
            ks = np.array(systems["surge"]["gains"][self.method])
            kl = np.array(systems["lateral"]["gains"][self.method])
            motor_sum = float(sum(self.motor_force)) - 2 * self.trim_force
            motor_moment = (
                self.nominal.hull.thruster_spacing_m
                / 2
                * float(self.motor_force[1] - self.motor_force[0])
            )
            total = 2 * self.trim_force - float(ks @ [du, motor_sum, candidate[0]])
            moment = -float(kl @ [ey, psi, v, r, motor_moment, candidate[1]])
        raw = np.array(
            [
                total / 2 - moment / self.nominal.hull.thruster_spacing_m,
                total / 2 + moment / self.nominal.hull.thruster_spacing_m,
            ]
        )
        bounded = np.clip(raw, FORCE.min(), FORCE.max())
        limited = bool(np.any(np.abs(raw - bounded) > 1e-9))
        # Conditional integration freezes all integrators while either motor clips.
        if ready and not limited:
            self.integrals = candidate
        if not ready:
            bounded = np.zeros(2)
            self.integrals[:] = 0
        if s.use_m200_inverse:
            pulses = np.array([inverse_force(float(f)) for f in bounded])
            nominal_forces = np.array([static_force(float(p)) for p in pulses])
        else:
            pulses = np.clip(self.trim_pwm + (bounded - self.trim_force) / self.slope, 1100, 1900)
            nominal_forces = self.trim_force + self.slope * (pulses - self.trim_pwm)
        if not ready:
            pulses, nominal_forces = np.full(2, 1500.0), np.zeros(2)
        self.pending.append((o.time_s + self.nominal_delay, nominal_forces))
        self.logs.append(
            {
                "time_s": o.time_s,
                "estimate": z.tolist(),
                "ready": bool(ready),
                "raw_force_N": raw.tolist(),
                "limited": limited,
                "desired_heading_rad": desired_heading,
                "integrals": self.integrals.tolist(),
            }
        )
        self.last_time, self.previous_speed_error = o.time_s, du
        return Command(float(pulses[0]), float(pulses[1]))


def target_lag(force: np.ndarray, target: np.ndarray, dt: float) -> np.ndarray:
    return target + (force - target) * math.exp(-max(0.0, dt) / 0.2)
