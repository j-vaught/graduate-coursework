"""Reproducible fixed-tuning controller comparisons and full-model ablations."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np

from .__main__ import overrides, write_json
from .config import Experiment, presets
from .controllers import Controller, Settings, design
from .engine import run

METHODS = ("pid", "lqr", "pole_placement")


def cases(duration: float) -> dict[str, Experiment]:
    base = replace(
        presets()["07_uncertainty"], duration_s=duration, initial_state=(0, 2, 0.12, 0.8, 0, 0)
    )
    specs = {
        "full_calm": {
            "flags.wind": False,
            "flags.gusts": False,
            "flags.apparent_wind": False,
            "flags.wind_yaw_moment": False,
            "flags.wave_forcing": False,
        },
        "full_wind5": {},
        "full_wind8": {"environment.wind_speed_m_s": 8.0},
        "full_wind10": {"environment.wind_speed_m_s": 10.0},
        "linear_hull": {
            "flags.nonlinear_kinematics": False,
            "flags.nonlinear_coupling": False,
            "flags.nonlinear_drag": False,
        },
        "linear_thrust": {
            "flags.nonlinear_thrust": False,
            "flags.neutral_deadband": False,
            "flags.reverse_asymmetry": False,
        },
        "ideal_motor": {
            "flags.motor_lag": False,
            "flags.motor_rate_limit": False,
            "flags.motor_mismatch": False,
        },
        "ideal_timing": {
            "flags.command_delay": False,
            "flags.timing_jitter": False,
            "flags.missed_commands": False,
            "flags.command_watchdog": False,
        },
        "oracle_feedback": {"flags.perfect_state_feedback": True},
        "no_added_mass": {"flags.added_mass": False},
        "heavy_drag": {
            "hull.mass_scale": 1.15,
            "hull.inertia_scale": 1.1,
            "hull.surge_linear_scale": 1.2,
            "hull.surge_quadratic_scale": 1.2,
            "hull.sway_linear_scale": 1.2,
            "hull.yaw_linear_scale": 1.2,
            "hull.sway_quadratic_N_s2_m2": 10.0,
            "hull.yaw_quadratic_N_m_s2": 3.0,
        },
    }
    result = {
        name: replace(
            overrides(base, [f"{k}={json.dumps(v)}" for k, v in changes.items()]), name=name
        )
        for name, changes in specs.items()
    }
    # Every policy needs decision ticks, including the otherwise continuous baseline.
    for name, c in presets().items():
        result["ladder_" + name] = replace(
            c,
            name="ladder_" + name,
            duration_s=duration,
            initial_state=base.initial_state,
            flags=replace(c.flags, command_sampling=True),
        )
    return result


def score(result: dict[str, Any], policy: Controller) -> dict[str, Any]:
    h = np.asarray(result["history"])
    t, y, u = h[:, 0], h[:, 2] - policy.settings.line_n_m, h[:, 4] - policy.settings.speed_m_s
    tail = t >= max(0, t[-1] - 10)
    within = (np.abs(y) <= 0.25) & (np.abs(u) <= 0.1)
    outside = np.flatnonzero(~within)
    settle = (
        None
        if len(outside) and outside[-1] == len(t) - 1
        else (float(t[outside[-1] + 1]) if len(outside) else 0.0)
    )
    total = result["metrics"]["squared_force_integral_N2_s"]
    return {
        "cross_rms_m": float(np.sqrt(np.mean(y * y))),
        "tail_cross_rms_m": float(np.sqrt(np.mean(y[tail] ** 2))),
        "speed_rms_m_s": float(np.sqrt(np.mean(u * u))),
        "tail_speed_rms_m_s": float(np.sqrt(np.mean(u[tail] ** 2))),
        "peak_cross_m": float(np.max(np.abs(y))),
        "final_cross_m": float(y[-1]),
        "peak_heading_deg": float(np.max(np.abs(h[:, 3])) * 180 / np.pi),
        "settling_s": settle,
        "mean_squared_thrust_N2": total / float(t[-1]),
        "allocation_limited_fraction": float(np.mean([r["limited"] for r in policy.logs])),
        "feedback_unready_fraction": float(np.mean([not r["ready"] for r in policy.logs])),
        "peak_force_N": result["metrics"]["peak_force_N"],
        "missed_commands": result["metrics"]["missed_commands"],
        "watchdog_trips": result["metrics"]["watchdog_trips"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration", type=float, default=40)
    parser.add_argument("--seeds", default="792,793,794")
    parser.add_argument("--case", action="append", choices=list(cases(40)))
    parser.add_argument("--set", dest="settings", action="append", default=[])
    parser.add_argument("--linear-pwm", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("build/controllers"))
    parser.add_argument("--data", type=Path, default=Path("controller_report/data"))
    args = parser.parse_args()
    seeds = [int(s) for s in args.seeds.split(",")]
    if not seeds or len(set(seeds)) != len(seeds) or min(seeds) < 0:
        parser.error("Seeds must be unique nonnegative integers")
    configs = cases(args.duration)
    selected = args.case or list(configs)
    configs = {name: overrides(configs[name], args.settings) for name in selected}
    settings = Settings(use_m200_inverse=not args.linear_pwm)
    args.output.mkdir(parents=True, exist_ok=True)
    args.data.mkdir(parents=True, exist_ok=True)
    fingerprint = {}
    for path in sorted(Path("blueboat_sim").glob("*.py")):
        fingerprint[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    summary: dict[str, Any] = {
        "schema_version": 1,
        "seeds": seeds,
        "settings": settings.__dict__,
        "source_sha256": fingerprint,
        "cases": {k: c.resolved() for k, c in configs.items()},
        "runs": [],
        "aggregate": [],
    }
    traces: dict[str, Any] = {}
    for name, c in configs.items():
        for seed in seeds:
            for method in METHODS:
                case = replace(c, seed=seed)
                lever = case.sensors.gnss_x_m if case.flags.antenna_lever_arm else 0.0
                policy = Controller(method, settings=settings, lever_arm_m=lever)
                result = run(case, policy=policy)
                metrics = score(result, policy)
                summary["runs"].append(
                    {"case": name, "seed": seed, "method": method, "metrics": metrics}
                )
                directory = args.output / f"{name}_{method}_seed{seed}"
                directory.mkdir(parents=True, exist_ok=True)
                write_json(directory / "resolved_config.json", result["config"])
                write_json(directory / "metrics.json", metrics)
                write_json(directory / "policy.json", policy.logs)
                write_json(directory / "decision_audit.json", result["decision_audit"])
                np.savetxt(
                    directory / "truth.csv",
                    result["history"],
                    delimiter=",",
                    header=",".join(result["columns"]),
                    comments="",
                    fmt="%.12g",
                )
                if seed == seeds[0]:
                    traces.setdefault(name, {})[method] = {
                        "columns": result["columns"],
                        "history": result["history"][::5],
                        "policy": policy.logs[::5],
                        "metrics": metrics,
                    }
                print(
                    f"{name} {method} seed {seed}. tail cross RMS "
                    f"{metrics['tail_cross_rms_m']:.3f} m",
                    flush=True,
                )
        for method in METHODS:
            rows = [
                r["metrics"] for r in summary["runs"] if r["case"] == name and r["method"] == method
            ]
            aggregate = {}
            for key in rows[0]:
                vals = [r[key] for r in rows if r[key] is not None]
                aggregate[key] = {
                    "mean": float(np.mean(vals)) if vals else None,
                    "min": min(vals) if vals else None,
                    "max": max(vals) if vals else None,
                    "n": len(vals),
                }
            summary["aggregate"].append({"case": name, "method": method, "metrics": aggregate})
    d = design()
    d["settings"] = summary["settings"]
    write_json(args.data / "design.json", d)
    write_json(args.data / "summary.json", summary)
    write_json(args.data / "traces.json", traces)
    print(f"Saved {len(summary['runs'])} runs to {args.output}; report data to {args.data}")


if __name__ == "__main__":
    main()
