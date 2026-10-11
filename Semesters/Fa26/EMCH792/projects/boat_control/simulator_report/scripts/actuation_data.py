"""Reproduce actuation chapter plot data from retained map and simulator code."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

REPORT = Path(__file__).resolve().parents[1]
PROJECT = REPORT.parent
sys.path.insert(0, str(PROJECT))

from blueboat_sim.config import Actuator, Experiment, Flags
from blueboat_sim.physics import motor_after, motor_target, trim
from propulsion import FORCE, PWM, RAW_FORCE, STATIC

OUT = REPORT / "data" / "actuation.json"
pwm = np.asarray(PWM, dtype=float)
raw = np.asarray(RAW_FORCE, dtype=float)
installed = np.asarray(FORCE, dtype=float)
scale = float(installed.max() / raw.max())

flags = Flags(
    nonlinear_thrust=True,
    thrust_saturation=True,
    neutral_deadband=True,
    reverse_asymmetry=True,
    motor_lag=True,
    motor_rate_limit=True,
    motor_mismatch=True,
)
actuator = Actuator(lag_s=0.2, rate_limit_N_s=80.0, port_gain=0.95, starboard_gain=1.05)
c = Experiment(flags=flags, actuator=actuator)
force_each, trim_pwm, tangent = trim(c)
fine_pwm = np.arange(1100.0, 1900.1, 2.0)
lookup = np.interp(fine_pwm, pwm, installed)
local = force_each + tangent * (fine_pwm - trim_pwm)
tangent_mask = np.abs(fine_pwm - trim_pwm) <= 80


# Use the simulator's configured lookup, channel gains, and lag/slew law.
start = motor_target((1700.0, 1700.0), c)
target = motor_target((1300.0, 1300.0), c)
times = np.arange(0.0, 1.5001, 0.005)
traces = np.asarray([motor_after(start, target, float(t), c) for t in times])

OUT.write_text(
    json.dumps(
        {
            "source": {
                "map_sha256": STATIC["sha256"],
                "voltage_V": STATIC["voltage_V"],
                "response_functions": [
                    "blueboat_sim.physics.motor_target",
                    "blueboat_sim.physics.motor_after",
                ],
            },
            "installation_scale": scale,
            "forward_limit_each_N": float(installed.max()),
            "reverse_limit_each_N": float(installed.min()),
            "trim": {
                "speed_m_s": 1.0,
                "force_each_N": force_each,
                "pwm_us": trim_pwm,
                "slope_N_us": tangent,
            },
            "curve": {
                "pwm_us": fine_pwm.tolist(),
                "raw16_N": np.interp(fine_pwm, pwm, raw).tolist(),
                "installed_N": lookup.tolist(),
                "tangent_pwm_us": fine_pwm[tangent_mask].tolist(),
                "local_tangent_N": local[tangent_mask].tolist(),
                "force_at_1600_lookup_N": float(np.interp(1600, pwm, installed)),
                "force_at_1600_tangent_N": float(force_each + tangent * (1600 - trim_pwm)),
                "force_at_1700_lookup_N": float(np.interp(1700, pwm, installed)),
                "force_at_1700_tangent_N": float(force_each + tangent * (1700 - trim_pwm)),
            },
            "step": {
                "time_s": times.tolist(),
                "port_N": traces[:, 0].tolist(),
                "starboard_N": traces[:, 1].tolist(),
                "start_pwm_us": 1700,
                "target_pwm_us": 1300,
                "start_port_N": start[0],
                "start_starboard_N": start[1],
                "target_port_N": target[0],
                "target_starboard_N": target[1],
                "lag_s": c.actuator.lag_s,
                "rate_N_s": c.actuator.rate_limit_N_s,
                "port_gain": 0.95,
                "starboard_gain": 1.05,
            },
        },
        indent=2,
    )
    + "\n"
)
print(f"Wrote {OUT}")
