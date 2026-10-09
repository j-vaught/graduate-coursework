"""Shared signed M200 map and provisional installed-BlueBoat scaling at 16 V."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "platform.json").read_text())
STATIC = json.loads((ROOT / "data" / "m200_static.json").read_text())
PWM = np.asarray(STATIC["pwm_us"], dtype=float)
RAW_FORCE = np.asarray(STATIC["force_N"], dtype=float)
INSTALLATION_SCALE = CONFIG["installed_forward_thrust_kgf"] * 9.80665 / (2 * RAW_FORCE.max())
FORCE = RAW_FORCE * INSTALLATION_SCALE


def static_force(pwm: float) -> float:
    """Installed-map assumption with manufacturer curve shape and neutral deadband."""
    clipped = float(np.clip(pwm, 1100, 1900))
    return 0.0 if 1475 <= clipped <= 1525 else float(np.interp(clipped, PWM, FORCE))


def inverse_force(force: float) -> float:
    """Clip a requested force to the available signed map and convert to PWM."""
    return 1500.0 if force == 0 else float(np.interp(force, FORCE, PWM))


def realizable_force(force: float) -> float:
    return static_force(inverse_force(force))
