"""
Retrosynthesis domain demo.

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

from deepxube.domains.retrosynthesis import (
    Retrosynthesis, RetroState, RetroGoal, RetroAction, _mol_to_string,
)


def bfs_solve(domain: Retrosynthesis, state: RetroState, goal: RetroGoal,
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


def make_snapshot(domain: Retrosynthesis) -> None:
    np.random.seed(42)
    fig = plt.figure(figsize=(8, 5.5), facecolor="white")
    states, goals = domain.sample_goalstate_goal_pairs(1)
    start = domain.random_walk_rev(states, [12])[0]
    domain.visualize_state_goal(start, goals[0], fig)
    fig.savefig("retro_states.png", dpi=150, bbox_inches="tight", facecolor="white")
    print("Saved retro_states.png")
    plt.close(fig)


def generate_test_problems(domain: Retrosynthesis, filename: str,
                           num_instances: int = 100,
                           step_range: Tuple[int, int] = (5, 30)) -> None:
    np.random.seed(123)
    num_steps = list(np.random.randint(step_range[0], step_range[1] + 1, size=num_instances))
    states, goals = domain.sample_problem_instances(num_steps)
    data = {"states": states, "goals": goals}
    with open(filename, "wb") as f:
        pickle.dump(data, f, protocol=-1)
    print(f"Saved {num_instances} problem instances to {filename}")


def verify_solvability(domain: Retrosynthesis, filename: str,
                       num_check: int = 20, max_nodes: int = 100_000) -> None:
    with open(filename, "rb") as f:
        data = pickle.load(f)
    states = data["states"][:num_check]
    goals = data["goals"][:num_check]

    solved_count = 0
    total_steps = 0

    print(f"\nVerifying solvability of {num_check} instances (BFS, max {max_nodes} nodes)...")
    for i, (s, g) in enumerate(zip(states, goals)):
        t0 = time.time()
        depth = bfs_solve(domain, s, g, max_nodes=max_nodes)
        elapsed = time.time() - t0
        expr = _mol_to_string(s.mol)
        goal_str = _mol_to_string(g.mol)
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


def show_action_example(domain: Retrosynthesis) -> None:
    """Show how site-selective reactions work."""
    np.random.seed(7)
    states, goals = domain.sample_goalstate_goal_pairs(1)
    start = domain.random_walk_rev(states, [6])[0]
    print(f"\nExample state: {start}")
    print(f"Target:        {_mol_to_string(goals[0].mol)}")
    actions = domain.get_state_actions([start])[0]
    print(f"Available actions ({len(actions)}):")
    for act in actions:
        ns, _ = domain.next_state([start], [act])
        print(f"  {act!r:30s} -> {ns[0]}")


if __name__ == "__main__":
    domain = Retrosynthesis(chain_len=5)
    print(f"Domain: {domain}")

    print("\nGenerating visualization...")
    make_snapshot(domain)

    show_action_example(domain)

    print("\nGenerating test problems (easy)...")
    generate_test_problems(domain, "retro_test_easy.pkl",
                           num_instances=100, step_range=(3, 10))

    print("Generating test problems (medium)...")
    generate_test_problems(domain, "retro_test_medium.pkl",
                           num_instances=100, step_range=(8, 20))

    print("Generating test problems (hard)...")
    generate_test_problems(domain, "retro_test_hard.pkl",
                           num_instances=100, step_range=(15, 35))

    print("\nVerifying easy problems...")
    verify_solvability(domain, "retro_test_easy.pkl", num_check=15, max_nodes=50_000)

    print("\nVerifying medium problems...")
    verify_solvability(domain, "retro_test_medium.pkl", num_check=10, max_nodes=100_000)

    print("\nDone.")
