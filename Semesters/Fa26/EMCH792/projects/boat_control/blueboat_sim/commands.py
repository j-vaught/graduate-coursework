"""Motor command units. Percent describes signed drive request, not thrust or power."""

from __future__ import annotations

import math


def percent_to_pwm(percent: float) -> float:
    """Convert signed percent to device pulse width without clipping the request."""
    if isinstance(percent, bool) or not math.isfinite(percent) or not -100 <= percent <= 100:
        raise ValueError("Motor command must be finite and between -100 and +100 percent")
    return 1500.0 + 4.0 * percent


def pwm_to_percent(pwm_us: float) -> float:
    """Convert a legacy pulse-width command to the public signed percent scale."""
    percent = (pwm_us - 1500.0) / 4.0
    percent_to_pwm(percent)
    return percent
