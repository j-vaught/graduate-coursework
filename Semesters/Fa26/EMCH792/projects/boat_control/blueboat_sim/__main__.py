"""CLI for presets, configured runs, and controlled comparisons."""

from __future__ import annotations

import argparse
import json
from dataclasses import replace
from itertools import pairwise
from pathlib import Path
from typing import Any

import numpy as np

from .config import Experiment, from_dict, load, presets
from .engine import Command, CommandChange, default_commands, run


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")


def overrides(c: Experiment, values: list[str]) -> Experiment:
    data = c.resolved()
    for value in values:
        key, separator, literal = value.partition("=")
        if not separator:
            raise ValueError("Overrides use --set flags.wind=true or --set duration_s=20")
        parts = key.split(".")
        if len(parts) > 2:
            raise ValueError("Overrides accept a field or group.field")
        target = data if len(parts) == 1 else data.get(parts[0])
        if not isinstance(target, dict) or parts[-1] not in target:
            raise ValueError(f"Unknown override: {key}")
        try:
            target[parts[-1]] = json.loads(literal)
        except json.JSONDecodeError:
            target[parts[-1]] = literal
    return from_dict(data)


def command_file(path: Path | None) -> list[CommandChange] | None:
    if path is None:
        return None
    items = json.loads(path.read_text())
    if not isinstance(items, list):
        raise TypeError("Command file must contain a list of time/PWM objects")
    result = []
    for item in items:
        if set(item) != {"time_s", "port_pwm_us", "starboard_pwm_us"}:
            raise ValueError("Each command needs time_s, port_pwm_us, starboard_pwm_us")
        result.append(
            CommandChange(
                float(item["time_s"]),
                Command(float(item["port_pwm_us"]), float(item["starboard_pwm_us"])),
            )
        )
    return result


def save_result(root: Path, result: dict[str, Any]) -> str:
    name = result["config"]["name"]
    directory = root / f"{name}_seed{result['config']['seed']}"
    directory.mkdir(parents=True, exist_ok=True)
    write_json(directory / "resolved_config.json", result["config"])
    write_json(directory / "result.json", result)
    write_json(directory / "input_tape.json", result["input_tape"])
    write_json(directory / "metrics.json", result["metrics"])
    np.savetxt(
        directory / "truth.csv",
        result["history"],
        delimiter=",",
        header=",".join(result["columns"]),
        comments="",
        fmt="%.12g",
    )
    return str(directory)


def main() -> None:
    parser = argparse.ArgumentParser(description="Configurable planar BlueBoat simulator")
    sub = parser.add_subparsers(dest="action", required=True)
    p = sub.add_parser("presets", help="List presets or export full editable JSON templates")
    p.add_argument("--output", type=Path)
    for name in ("run", "compare"):
        p = sub.add_parser(name)
        p.add_argument("--output", type=Path, default=Path("build/simulator"))
        p.add_argument("--set", dest="settings", action="append", default=[])
        p.add_argument("--commands", type=Path)
        if name == "run":
            choice = p.add_mutually_exclusive_group()
            choice.add_argument("--config", type=Path)
            choice.add_argument("--preset", choices=list(presets()), default="00_linear")
        else:
            p.add_argument(
                "--config",
                dest="configs",
                type=Path,
                action="append",
                help="Compare custom configs, in the supplied order",
            )
            p.add_argument("--mode", choices=("cumulative", "isolated"), default="cumulative")
            p.add_argument("--seeds", default="792", help="Comma-separated seeds for paired trials")
    args = parser.parse_args()
    try:
        if args.action == "presets":
            templates = presets()
            if args.output:
                args.output.mkdir(parents=True, exist_ok=True)
                for name, c in templates.items():
                    write_json(args.output / f"{name}.json", c.resolved())
            print("\n".join(templates))
            return
        tape = command_file(args.commands)
        if args.action == "run":
            c = overrides(
                load(args.config) if args.config else presets()[args.preset], args.settings
            )
            result = run(c, tape)
            print(
                json.dumps(
                    {
                        "output": save_result(args.output, result),
                        "metrics": result["metrics"],
                        "warnings": result["warnings"],
                    },
                    indent=2,
                )
            )
            return
        cases = [load(path) for path in args.configs] if args.configs else list(presets().values())
        if args.mode == "isolated":
            if args.configs:
                raise ValueError(
                    "isolated mode builds default groups; use cumulative for custom configs"
                )
            baseline = cases[0]
            isolated = [baseline]
            for previous, current in pairwise(cases):
                flags = baseline.resolved()["flags"]
                before, after = previous.resolved()["flags"], current.resolved()["flags"]
                flags.update({key: value for key, value in after.items() if before[key] != value})
                # Preserve prerequisites for jitter/missed commands in the last group.
                if flags["timing_jitter"]:
                    flags.update(command_sampling=True, command_delay=True)
                isolated.append(
                    from_dict(
                        {
                            **baseline.resolved(),
                            "name": current.name + "_isolated",
                            "flags": flags,
                            "actuator": current.resolved()["actuator"],
                            "sensors": current.resolved()["sensors"],
                        }
                    )
                )
            cases = isolated
        cases = [overrides(c, args.settings) for c in cases]
        seeds = [int(value) for value in args.seeds.split(",")]
        if len(seeds) != len(set(seeds)):
            raise ValueError("Comparison seeds must be unique")
        if len({c.name for c in cases}) != len(cases):
            raise ValueError("Comparison names must be unique")
        if (
            len(
                {
                    (
                        c.duration_s,
                        c.scenario,
                        c.command_amplitude_us,
                        c.operating_speed_m_s,
                        c.operating_heading_rad,
                        c.initial_state,
                    )
                    for c in cases
                }
            )
            != 1
        ):
            raise ValueError(
                "Comparisons require matching duration, scenario, operating point, amplitude, and initial state"
            )
        tape = default_commands(cases[0]) if tape is None else tape
        summary: dict[str, Any] = {
            "mode": args.mode,
            "interpretation": "Model differences and sensor errors; no accuracy improvement or controller performance is inferred.",
            "runs": [],
        }
        comparisons = []
        for seed in seeds:
            for case in cases:
                c = replace(case, seed=seed)
                result = run(c, tape)
                output = save_result(args.output, result)
                summary["runs"].append(
                    {"name": c.name, "seed": seed, "metrics": result["metrics"], "output": output}
                )
                comparisons.append(
                    {
                        "name": c.name,
                        "seed": seed,
                        "flags": c.resolved()["flags"],
                        "columns": result["columns"],
                        "history": result["history"],
                        "gnss": result["measurements"]["gnss"],
                        "metrics": result["metrics"],
                    }
                )
                print(f"Finished {c.name}, seed {seed}", flush=True)
        args.output.mkdir(parents=True, exist_ok=True)
        write_json(args.output / "summary.json", summary)
        write_json(args.output / "comparison.json", comparisons)
        print(f"Saved comparison to {args.output}")
    except (ValueError, TypeError, KeyError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
