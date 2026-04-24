"""Benchmark custom domain data-generation hot paths."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

import deepxube  # noqa: F401
from deepxube.utils.command_line_utils import get_domain_from_arg


DEFAULT_CASES = [
    ("hanoi.6.3", 1000, 40),
    ("pancake.10", 1000, 40),
    ("linkage.64_64_64", 1000, 40),
    ("mapf.28_28_30_64", 200, 20),
    ("arm.6_12_8", 500, 20),
    ("retro.7", 1000, 30),
]


@dataclass
class BenchResult:
    domain: str
    num_states: int
    avg_steps: float
    random_walk_sec: float
    action_avg: float
    action_sec: float


def run_case(domain_str: str, num_states: int, step_max: int) -> BenchResult:
    domain, _ = get_domain_from_arg(domain_str)
    states, _ = domain.sample_goalstate_goal_pairs(num_states)
    steps = np.random.randint(1, step_max + 1, size=num_states).tolist()

    start = time.perf_counter()
    walked = domain.random_walk_rev(states, steps)
    random_walk_sec = time.perf_counter() - start

    action_states = walked[: min(64, len(walked))]
    start = time.perf_counter()
    actions = domain.get_state_actions(action_states)
    action_sec = time.perf_counter() - start

    return BenchResult(
        domain=domain_str,
        num_states=num_states,
        avg_steps=float(np.mean(steps)),
        random_walk_sec=random_walk_sec,
        action_avg=float(np.mean([len(x) for x in actions])),
        action_sec=action_sec,
    )


def parse_case(case: str) -> tuple[str, int, int]:
    parts = case.split(":")
    if len(parts) != 3:
        raise ValueError(f"Expected DOMAIN:NUM_STATES:STEP_MAX, got {case!r}")
    return parts[0], int(parts[1]), int(parts[2])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--case",
        action="append",
        help="Benchmark case as DOMAIN:NUM_STATES:STEP_MAX. Can be repeated.",
    )
    parser.add_argument("--seed", type=int, default=775)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    np.random.seed(args.seed)
    cases = [parse_case(x) for x in args.case] if args.case else DEFAULT_CASES
    results = [run_case(*case) for case in cases]

    print(
        f"{'domain':22s} {'states':>7s} {'steps':>7s} "
        f"{'walk_s':>9s} {'acts':>8s} {'acts_s':>9s}"
    )
    for result in results:
        print(
            f"{result.domain:22s} {result.num_states:7d} "
            f"{result.avg_steps:7.1f} {result.random_walk_sec:9.3f} "
            f"{result.action_avg:8.1f} {result.action_sec:9.3f}"
        )

    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(
            json.dumps([asdict(result) for result in results], indent=2)
            + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
