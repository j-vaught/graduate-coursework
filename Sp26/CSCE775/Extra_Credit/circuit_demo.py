"""
Circuit Minimization domain demo.

Generates state snapshot figures, test problem .pkl files,
and verifies solvability with a brute-force BFS baseline.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "deepxube"))

import numpy as np
import pickle
import time
from collections import deque
from typing import List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from deepxube.domains.circuit import (
    CircuitMinimization, CircState, CircGoal, CircAction,
    _sop_to_string,
)

GARNET = "#73000A"
BLACK_90 = "#363636"
SANDSTORM = "#FFF2E3"


def bfs_solve(domain: CircuitMinimization, state: CircState, goal: CircGoal,
              max_nodes: int = 50_000) -> Optional[int]:
    if domain.is_solved([state], [goal])[0]:
        return 0
    queue: deque = deque([(state, 0)])
    visited = {state}
    nodes = 0
    while queue and nodes < max_nodes:
        cur, depth = queue.popleft()
        actions = domain.get_state_actions([cur])[0]
        for act in actions:
            ns, _ = domain.next_state([cur], [act])
            nxt = ns[0]
            if nxt in visited:
                continue
            visited.add(nxt)
            nodes += 1
            if domain.is_solved([nxt], [goal])[0]:
                return depth + 1
            queue.append((nxt, depth + 1))
    return None


def make_simple_snapshot(domain: CircuitMinimization) -> None:
    np.random.seed(42)
    fig = plt.figure(figsize=(6, 5), facecolor="white")
    states, goals = domain.sample_goalstate_goal_pairs(1)
    start = domain.random_walk_rev(states, [12])[0]
    domain.visualize_state_goal(start, goals[0], fig)
    fig.savefig("circuit_states.png", dpi=150, bbox_inches="tight", facecolor="white")
    print("Saved circuit_states.png")
    plt.close(fig)


def generate_test_problems(domain: CircuitMinimization,
                           filename: str,
                           num_instances: int = 100,
                           step_range: Tuple[int, int] = (5, 30)) -> None:
    np.random.seed(123)
    num_steps = list(np.random.randint(step_range[0], step_range[1] + 1, size=num_instances))
    states, goals = domain.sample_problem_instances(num_steps)

    data = {"states": states, "goals": goals}
    with open(filename, "wb") as f:
        pickle.dump(data, f, protocol=-1)
    print(f"Saved {num_instances} problem instances to {filename}")


def verify_solvability(domain: CircuitMinimization, filename: str,
                       num_check: int = 20, max_nodes: int = 100_000) -> None:
    with open(filename, "rb") as f:
        data = pickle.load(f)
    states = data["states"][:num_check]
    goals = data["goals"][:num_check]

    solved_count = 0
    total_steps = 0
    em = domain.empty_mask
    nv = domain.num_vars
    mt = domain.max_terms

    print(f"\nVerifying solvability of {num_check} instances (BFS, max {max_nodes} nodes)...")
    for i, (s, g) in enumerate(zip(states, goals)):
        t0 = time.time()
        depth = bfs_solve(domain, s, g, max_nodes=max_nodes)
        elapsed = time.time() - t0
        expr = _sop_to_string(s.terms, mt, em, nv)
        goal_str = _sop_to_string(g.terms, mt, em, nv)
        if depth is not None:
            solved_count += 1
            total_steps += depth
            print(f"  [{i:2d}] SOLVED in {depth:3d} steps ({elapsed:.2f}s)  "
                  f"{expr}  ->  {goal_str}")
        else:
            print(f"  [{i:2d}] NOT SOLVED ({elapsed:.2f}s)  "
                  f"{expr}  ->  {goal_str}")

    print(f"\nSolved: {solved_count}/{num_check}")
    if solved_count > 0:
        print(f"Avg steps: {total_steps / solved_count:.1f}")


if __name__ == "__main__":
    domain = CircuitMinimization(num_vars=3, max_terms=8)

    print("Generating visualization...")
    make_simple_snapshot(domain)

    print("\nGenerating test problems (easy)...")
    generate_test_problems(domain, "circuit_test_easy.pkl",
                           num_instances=100, step_range=(3, 10))

    print("Generating test problems (medium)...")
    generate_test_problems(domain, "circuit_test_medium.pkl",
                           num_instances=100, step_range=(8, 20))

    print("Generating test problems (hard)...")
    generate_test_problems(domain, "circuit_test_hard.pkl",
                           num_instances=100, step_range=(15, 35))

    print("\nVerifying easy problems...")
    verify_solvability(domain, "circuit_test_easy.pkl", num_check=15, max_nodes=50_000)

    print("\nVerifying medium problems...")
    verify_solvability(domain, "circuit_test_medium.pkl", num_check=10, max_nodes=100_000)

    print("\nDone.")
