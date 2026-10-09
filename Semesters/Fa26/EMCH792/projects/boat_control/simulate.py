"""BlueBoat open-loop experiments using one shared physical configuration."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import solve_ivp
from scipy.optimize import root_scalar

from propulsion import CONFIG, FORCE, INSTALLATION_SCALE, realizable_force

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
FloatArray = NDArray[np.float64]
MASS = CONFIG["bare_mass_kg"] + CONFIG["battery_mass_total_kg"] + CONFIG["equipment_allowance_kg"]


@dataclass(frozen=True)
class Parameters:
    mass_kg: float = MASS
    yaw_inertia_kg_m2: float = MASS * (CONFIG["length_m"] ** 2 + CONFIG["beam_m"] ** 2) / 12
    thruster_spacing_m: float = CONFIG["thruster_spacing_m"]
    surge_linear_N_s_m: float = CONFIG["surge_linear_N_s_m"]
    surge_quadratic_N_s2_m2: float = CONFIG["surge_quadratic_N_s2_m2"]
    sway_linear_N_s_m: float = CONFIG["sway_linear_N_s_m"]
    yaw_linear_N_m_s: float = CONFIG["yaw_linear_N_m_s"]
    wind_force_N: float = (
        0.5
        * CONFIG["air_density_kg_m3"]
        * CONFIG["wind_drag_coefficient"]
        * CONFIG["lateral_wind_area_m2"]
        * CONFIG["wind_speed_m_s"] ** 2
    )
    headwind_force_N: float = (
        0.5
        * CONFIG["air_density_kg_m3"]
        * CONFIG["wind_drag_coefficient"]
        * CONFIG["frontal_wind_area_m2"]
        * CONFIG["wind_speed_m_s"] ** 2
    )
    thrust_min_N: float = float(FORCE.min())
    thrust_max_N: float = float(FORCE.max())


P = Parameters()


def rhs(
    state: FloatArray,
    left: float,
    right: float,
    wind: tuple[float, float],
    parameters: Parameters = P,
) -> FloatArray:
    """Rigid-body planar dynamics; unmeasured hydrodynamics are explicit assumptions."""
    _, _, heading, u, v, r = state
    c, s = np.cos(heading), np.sin(heading)
    wind_x, wind_y = wind
    fx, fy = c * wind_x + s * wind_y, -s * wind_x + c * wind_y
    p = parameters
    return np.array(
        [
            c * u - s * v,
            s * u + c * v,
            r,
            v * r
            + (
                left
                + right
                - p.surge_linear_N_s_m * u
                - p.surge_quadratic_N_s2_m2 * u * abs(u)
                + fx
            )
            / p.mass_kg,
            -u * r + (-p.sway_linear_N_s_m * v + fy) / p.mass_kg,
            (p.thruster_spacing_m / 2 * (right - left) - p.yaw_linear_N_m_s * r)
            / p.yaw_inertia_kg_m2,
        ],
        dtype=float,
    )


def run(
    name: str,
    duration: float,
    segments: list[tuple[float, float, float, float]],
    initial: tuple[float, ...] = (0, 0, 0, 0, 0, 0),
    wind: tuple[float, float] = (0, 0),
    max_step: float = 0.05,
    parameters: Parameters = P,
) -> dict[str, Any]:
    """Ideal-thrust reference with every force demand passed through the M200 map."""
    time = np.linspace(0, duration, round(duration / 0.05) + 1)
    states = np.full((time.size, 6), np.nan)
    state = np.asarray(initial, dtype=float)
    thrust = np.zeros((time.size, 2))
    assert segments[0][0] == 0 and segments[-1][1] == duration
    for index, (start, end, left, right) in enumerate(segments):
        if index:
            assert start == segments[index - 1][1]
        tl, tr = realizable_force(left), realizable_force(right)
        solution = solve_ivp(
            lambda _t, y, l=tl, r=tr: rhs(y, l, r, wind, parameters),
            (start, end),
            state,
            rtol=1e-10,
            atol=1e-12,
            max_step=max_step,
            dense_output=True,
        )
        assert solution.success and solution.sol is not None
        indices = (time >= start) & (time <= end)
        states[indices] = solution.sol(time[indices]).T
        thrust[indices] = (tl, tr)
        state = solution.y[:, -1]
    assert np.isfinite(states).all()
    result: dict[str, Any] = {
        "name": name,
        "platform": "BlueBoat",
        "parameters": asdict(parameters),
        "actuation": "Installed-scaled M200 16 V map; instantaneous force reference. Delayed force is tested in components.py.",
        "time": time.tolist(),
        "states": states.tolist(),
    }
    for i, field in enumerate(("x", "y", "psi", "u", "v", "r")):
        result[field] = states[:, i].tolist()
    result["left"] = thrust[:, 0].tolist()
    result["right"] = thrust[:, 1].tolist()
    result["distance"] = np.hypot(20 - states[:, 0], states[:, 1]).tolist()
    result["wind_world_N"] = list(wind)
    result["segments"] = segments
    return result


def coast_distance(speed: float, parameters: Parameters = P) -> float:
    return (
        parameters.mass_kg
        / parameters.surge_quadratic_N_s2_m2
        * np.log1p(parameters.surge_quadratic_N_s2_m2 * speed / parameters.surge_linear_N_s_m)
    )


def forward_endpoint(total_force: float, cutoff: float) -> float:
    result = run("nominal_acceleration", cutoff, [(0, cutoff, total_force / 2, total_force / 2)])
    return result["x"][-1] + coast_distance(result["u"][-1])


def write_json(path: Path, content: Any) -> None:
    path.write_text(json.dumps(content, indent=2, allow_nan=False) + "\n")


def main() -> None:
    DATA.mkdir(exist_ok=True)
    force = 30.0
    cutoff = float(root_scalar(lambda t: forward_endpoint(force, t) - 20, bracket=(1, 60)).root)
    schedule = {
        "chosen_total_force_N": force,
        "chosen_cutoff_s": cutoff,
        "nominal_endpoint_m": forward_endpoint(force, cutoff),
        "method": "Solve BlueBoat ideal-thrust travel plus analytic calm coast to a 20 m target; no slide fitting.",
        "schedule_status": "Open-loop nominal-model calibration; unchanged in both wind cases.",
    }
    runs = {
        "equal": run("Equal M200 thrust", 40, [(0, 1, 0, 0), (1, 40, 15, 15)]),
        "differential": run("Differential M200 thrust", 60, [(0, 1, 0, 0), (1, 60, 10, 15)]),
        "pulse": run("Differential M200 pulse", 30, [(0, 1, 0, 0), (1, 2, 30, -15), (2, 30, 0, 0)]),
        "decay": run("BlueBoat free decay", 30, [(0, 30, 0, 0)], (0, 0, 0, 1, 0.5, 0.5)),
        "wind": run("BlueBoat crosswind drift", 60, [(0, 60, 0, 0)], wind=(0, P.wind_force_N)),
    }
    segments: list[tuple[float, float, float, float]] = [
        (0, cutoff, force / 2, force / 2),
        (cutoff, 90, 0, 0),
    ]
    for label, wind in (
        ("calm", (0, 0)),
        ("crosswind", (0, P.wind_force_N)),
        ("headwind", (-P.headwind_force_N, 0)),
    ):
        runs["blind_" + label] = run(label, 90, segments, wind=wind)
    phases: dict[str, Any] = {}
    for surge in (0, 1):
        responses = []
        for v0 in np.linspace(-1, 1, 5):
            for r0 in np.linspace(-0.5, 0.5, 5):
                t = np.linspace(0, 30, 301)
                a = P.sway_linear_N_s_m / P.mass_kg
                b = P.yaw_linear_N_m_s / P.yaw_inertia_kg_m2
                r = r0 * np.exp(-b * t)
                v = v0 * np.exp(-a * t) - surge * r0 * (np.exp(-b * t) - np.exp(-a * t)) / (a - b)
                responses.append(
                    {"v": v.tolist(), "r": r.tolist(), "v0": float(v0), "r0": float(r0)}
                )
        phases[str(surge)] = responses
    sensitivity: dict[str, Any] = {"mass": {}, "drag": {}}
    for mass in (16.9, P.mass_kg, 29.5):
        p = replace(P, mass_kg=mass, yaw_inertia_kg_m2=P.yaw_inertia_kg_m2 * mass / P.mass_kg)
        sensitivity["mass"][f"{mass:g}"] = run(
            "Mass sensitivity", 15, [(0, 1, 0, 0), (1, 15, 15, 15)], parameters=p
        )
    for scale in (0.5, 1.0, 2.0):
        p = replace(
            P,
            surge_linear_N_s_m=P.surge_linear_N_s_m * scale,
            surge_quadratic_N_s2_m2=P.surge_quadratic_N_s2_m2 * scale,
        )
        sensitivity["drag"][f"{scale:g}"] = run(
            "Surge drag sensitivity", 15, [(0, 1, 0, 0), (1, 15, 15, 15)], parameters=p
        )
    write_json(DATA / "runs.json", runs)
    write_json(DATA / "phases.json", phases)
    write_json(
        DATA / "parameters.json",
        {**asdict(P), "configuration": CONFIG, "installation_scale": float(INSTALLATION_SCALE)},
    )
    write_json(DATA / "schedule.json", schedule)
    write_json(DATA / "sensitivity.json", sensitivity)
    for name, result in runs.items():
        columns = ("time", "x", "y", "psi", "u", "v", "r", "left", "right", "distance")
        np.savetxt(
            DATA / f"{name}.csv",
            np.column_stack([result[field] for field in columns]),
            delimiter=",",
            header=",".join(columns),
            comments="",
            fmt="%.10g",
        )
    print(json.dumps({"parameters": asdict(P), "schedule": schedule}, indent=2))


if __name__ == "__main__":
    main()
