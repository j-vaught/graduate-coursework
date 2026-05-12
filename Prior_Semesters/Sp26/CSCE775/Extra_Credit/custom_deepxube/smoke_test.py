"""Smoke tests for the custom DeepXube domain workspace."""

from __future__ import annotations

import pickle
import time
from pathlib import Path

import numpy as np

import deepxube  # noqa: F401
from deepxube.utils.command_line_utils import get_domain_from_arg


DOMAINS = [
    "hanoi.4.3",
    "pancake.8",
    "mapf.28_28_30_64",
    "arm.6_12_8",
    "retro.5",
]


def check_domain(domain_str: str) -> None:
    np.random.seed(775)
    domain, _ = get_domain_from_arg(domain_str)
    start = time.time()
    states, goals = domain.sample_problem_instances([0, 1, 2])
    solved0 = domain.is_solved(states[:1], goals[:1])[0]
    actions = domain.sample_state_action(states[:1])
    _, costs = domain.next_state(states[:1], actions)
    elapsed = time.time() - start
    print(
        f"{domain_str}: ok, solved0={solved0}, "
        f"action={actions[0]}, cost={costs[0]}, sec={elapsed:.3f}"
    )


def check_pickles() -> None:
    for path in sorted(Path("test_instances").glob("*.pkl")):
        with path.open("rb") as f:
            data = pickle.load(f)
        domain, _ = get_domain_from_arg(data["domain"])
        solved = domain.is_solved(data["states"][:1], data["goals"][:1])[0]
        print(
            f"{path.name}: {len(data['states'])} instances, "
            f"domain={data['domain']}, first_solved={solved}"
        )


def check_large_mapf() -> None:
    np.random.seed(42)
    domain, _ = get_domain_from_arg("mapf.28_28_30_64")
    states, _ = domain.sample_problem_instances([5, 10])
    start = time.time()
    action_counts = [len(actions) for actions in domain.get_state_actions(states)]
    elapsed = time.time() - start
    print(f"mapf action counts={action_counts}, sec={elapsed:.3f}")


def main() -> None:
    for domain_str in DOMAINS:
        check_domain(domain_str)
    check_pickles()
    check_large_mapf()


if __name__ == "__main__":
    main()
