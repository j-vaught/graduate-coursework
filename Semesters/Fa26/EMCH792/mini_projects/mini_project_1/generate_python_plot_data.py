"""Generate Python reference histories for the four report plots."""

import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


M = 2.0
m = 0.5
ell = 1.0
c_theta = 0.01
g = 9.81
theta0 = np.deg2rad(5.0)
dt = 0.02


def dynamics(_time: float, state: np.ndarray) -> np.ndarray:
    x, x_dot, theta, theta_dot = state
    s = np.sin(theta)
    c = np.cos(theta)
    mass_matrix = np.array(
        [[M + m, m * ell * c], [m * ell * c, m * ell**2]],
    )
    forcing = np.array(
        [m * ell * s * theta_dot**2, m * g * ell * s - c_theta * theta_dot],
    )
    x_ddot, theta_ddot = np.linalg.solve(mass_matrix, forcing)
    return np.array([x_dot, x_ddot, theta_dot, theta_ddot])


time = np.arange(0.0, 200.0 + dt / 2.0, dt)
solution = solve_ivp(
    dynamics,
    (time[0], time[-1]),
    [0.0, 0.0, theta0, 0.0],
    t_eval=time,
    method="DOP853",
    rtol=1e-10,
    atol=1e-12,
    max_step=0.01,
)
if not solution.success:
    raise RuntimeError(solution.message)


data = {
    "time_10_s": time[time <= 10.0].tolist(),
    "x_10_m": solution.y[0, time <= 10.0].tolist(),
    "theta_10_rad": solution.y[2, time <= 10.0].tolist(),
    "time_20_s": time[time <= 20.0].tolist(),
    "x_20_m": solution.y[0, time <= 20.0].tolist(),
    "theta_20_rad": solution.y[2, time <= 20.0].tolist(),
    "time_200_s": time.tolist(),
    "x_200_m": solution.y[0].tolist(),
    "theta_200_rad": solution.y[2].tolist(),
}
Path("python_plot_data.json").write_text(json.dumps(data), encoding="utf-8")
