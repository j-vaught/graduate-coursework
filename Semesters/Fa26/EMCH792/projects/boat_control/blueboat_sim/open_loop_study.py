"""Fixed trim commands contrasted with the retained closed-loop line-tracking study."""

from __future__ import annotations

import argparse
import hashlib
import math
from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np

from .__main__ import write_json
from .controller_study import cases
from .engine import Command, Observation, run
from .physics import trim


class FixedTrim:
    """Retransmit a fixed command; sensor content cannot affect the result."""

    def __init__(self, pulse_us: float):
        self.command = Command(pulse_us, pulse_us)

    def __call__(self, observation: Observation) -> Command:
        return self.command


def metrics(history: list[list[float]]) -> dict[str, float]:
    h = np.asarray(history)
    tail = h[:, 0] >= h[-1, 0] - 10
    return {
        "cross_rms_m": float(np.sqrt(np.mean(h[:, 2] ** 2))),
        "tail_cross_rms_m": float(np.sqrt(np.mean(h[tail, 2] ** 2))),
        "final_e_m": float(h[-1, 1]),
        "final_n_m": float(h[-1, 2]),
        "final_heading_deg": math.degrees(float(h[-1, 3])),
        "final_surge_m_s": float(h[-1, 4]),
        "tail_speed_rms_m_s": float(np.sqrt(np.mean((h[tail, 4] - 1) ** 2))),
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, default=Path("build/open-loop"))
    p.add_argument("--data", type=Path, default=Path("controller_report/data/open_loop.json"))
    args = p.parse_args()
    configs = cases(40)
    nominal = configs["full_calm"]
    nominal = replace(
        nominal, flags=replace(nominal.flags, motor_mismatch=False, missed_commands=False)
    )
    selected = {
        "nominal_on_line": replace(
            nominal, name="nominal_on_line", initial_state=(0, 0, 0, 1, 0, 0)
        ),
        "nominal_offset": replace(nominal, name="nominal_offset"),
        **{name: configs[name] for name in ("full_calm", "full_wind5", "full_wind10")},
        **{name: c for name, c in configs.items() if name.startswith("ladder_")},
    }
    data: dict[str, Any] = {
        "schema_version": 1,
        "duration_s": 40,
        "seeds": [792, 793, 794],
        "policy": "Fixed equal nominal-trim PWM, refreshed at every decision tick; no feedback",
        "runs": [],
        "traces": {},
        "aggregate": [],
        "source_sha256": {
            str(path): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in [
                *sorted(Path("blueboat_sim").glob("*.py")),
                Path("platform.json"),
                Path("propulsion.py"),
                Path("data/m200_static.json"),
                Path("uv.lock"),
            ]
        },
    }
    for name, original in selected.items():
        for seed in data["seeds"]:
            c = replace(original, seed=seed)
            force, pulse, _ = trim(c)
            result = run(c, policy=FixedTrim(pulse))
            score = metrics(result["history"])
            data["runs"].append(
                {
                    "case": name,
                    "seed": seed,
                    "metrics": score,
                    "config": c.resolved(),
                    "pwm_each_us": pulse,
                    "nominal_force_each_N": force,
                }
            )
            root = args.output / f"{name}_seed{seed}"
            root.mkdir(parents=True, exist_ok=True)
            write_json(root / "resolved_config.json", result["config"])
            write_json(root / "commands.json", result["commands"])
            write_json(root / "metrics.json", score)
            np.savetxt(
                root / "truth.csv",
                result["history"],
                delimiter=",",
                header=",".join(result["columns"]),
                comments="",
                fmt="%.12g",
            )
            if seed == data["seeds"][0]:
                h = np.asarray(result["history"])
                snapshots = []
                for time in (0, 10, 20, 40):
                    row = h[np.argmin(abs(h[:, 0] - time))]
                    psi, u, v = row[3:6]
                    ve = math.cos(psi) * u - math.sin(psi) * v
                    vn = math.sin(psi) * u + math.cos(psi) * v
                    snapshots.append(
                        {
                            "time_s": float(row[0]),
                            "e_m": float(row[1]),
                            "n_m": float(row[2]),
                            "heading_rad": float(psi),
                            "surge_m_s": float(u),
                            "sway_m_s": float(v),
                            "velocity_e_m_s": ve,
                            "velocity_n_m_s": vn,
                        }
                    )
                data["traces"][name] = {
                    "history": result["history"][::5],
                    "snapshots": snapshots,
                    "metrics": score,
                }
            print(
                f"Open loop {name}, seed {seed}. Final north {score['final_n_m']:.2f} m", flush=True
            )
        rows = [r["metrics"] for r in data["runs"] if r["case"] == name]
        data["aggregate"].append(
            {
                "case": name,
                "metrics": {
                    key: {
                        "mean": float(np.mean([r[key] for r in rows])),
                        "min": min(r[key] for r in rows),
                        "max": max(r[key] for r in rows),
                    }
                    for key in rows[0]
                },
            }
        )
    args.data.parent.mkdir(parents=True, exist_ok=True)
    write_json(args.data, data)


if __name__ == "__main__":
    main()
