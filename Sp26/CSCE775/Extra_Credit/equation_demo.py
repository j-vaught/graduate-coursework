"""
Equation Simplification domain demo.

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
from typing import List, Dict, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import deepxube
from deepxube.domains.equation import (
    EquationSimplification, EqState, EqGoal, EqAction,
    _terms_to_string,
)

GARNET = "#73000A"
BLACK_90 = "#363636"
SANDSTORM = "#FFF2E3"


def bfs_solve(domain: EquationSimplification, state: EqState, goal: EqGoal,
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


def make_snapshot_figure(domain: EquationSimplification) -> None:
    np.random.seed(42)
    ed = domain.empty_deg
    mt = domain.max_terms

    configs: List[Tuple[str, EqState, EqGoal]] = []

    goal_t = domain._random_canonical()
    configs.append(("Goal state (solved)", EqState(goal_t.copy()), EqGoal(goal_t.copy())))

    starts = domain.random_walk_rev([EqState(goal_t.copy())], [5])
    configs.append(("5-step scramble", starts[0], EqGoal(goal_t.copy())))

    goal2 = domain._random_canonical()
    starts2 = domain.random_walk_rev([EqState(goal2.copy())], [15])
    configs.append(("15-step scramble", starts2[0], EqGoal(goal2.copy())))

    goal3 = domain._random_canonical()
    starts3 = domain.random_walk_rev([EqState(goal3.copy())], [25])
    configs.append(("25-step scramble", starts3[0], EqGoal(goal3.copy())))

    goal4 = domain._random_canonical()
    starts4 = domain.random_walk_rev([EqState(goal4.copy())], [40])
    configs.append(("40-step scramble", starts4[0], EqGoal(goal4.copy())))

    fig, axes = plt.subplots(1, 5, figsize=(18, 4), facecolor="white")
    fig.subplots_adjust(wspace=0.08, left=0.01, right=0.99, top=0.88, bottom=0.02)
    fig.suptitle("Equation Simplification  —  Example States",
                 fontsize=12, color=BLACK_90, fontweight="bold", y=0.97)

    for ax, (title, state, goal) in zip(axes, configs):
        ax.set_title(title, fontsize=9, color=BLACK_90, pad=4)
        domain.visualize_state_goal(state, goal, fig)
        fig.axes[-1].remove()
        domain.visualize_state_goal(state, goal, fig)
        target_ax = fig.axes[-1]
        target_ax.set_position(ax.get_position())
        ax.remove()

    fig.savefig("equation_states.png", dpi=150, bbox_inches="tight", facecolor="white")
    print("Saved equation_states.png")
    plt.close(fig)


def make_simple_snapshot(domain: EquationSimplification) -> None:
    np.random.seed(42)
    fig = plt.figure(figsize=(6, 5), facecolor="white")
    goal_t = domain._random_canonical()
    start = domain.random_walk_rev([EqState(goal_t.copy())], [12])[0]
    domain.visualize_state_goal(start, EqGoal(goal_t.copy()), fig)
    fig.savefig("equation_states.png", dpi=150, bbox_inches="tight", facecolor="white")
    print("Saved equation_states.png")
    plt.close(fig)


def generate_test_problems(domain: EquationSimplification,
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


def verify_solvability(domain: EquationSimplification, filename: str,
                       num_check: int = 20, max_nodes: int = 100_000) -> None:
    with open(filename, "rb") as f:
        data = pickle.load(f)
    states = data["states"][:num_check]
    goals = data["goals"][:num_check]

    solved_count = 0
    total_steps = 0
    ed = domain.empty_deg
    mt = domain.max_terms

    print(f"\nVerifying solvability of {num_check} instances (BFS, max {max_nodes} nodes)...")
    for i, (s, g) in enumerate(zip(states, goals)):
        t0 = time.time()
        depth = bfs_solve(domain, s, g, max_nodes=max_nodes)
        elapsed = time.time() - t0
        expr = _terms_to_string(s.terms, mt, ed)
        goal_str = _terms_to_string(g.terms, mt, ed)
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
    domain = EquationSimplification(max_degree=4, max_terms=8)

    print("Generating visualization...")
    make_simple_snapshot(domain)

    print("\nGenerating test problems (easy)...")
    generate_test_problems(domain, "equation_test_easy.pkl",
                           num_instances=100, step_range=(3, 12))

    print("Generating test problems (medium)...")
    generate_test_problems(domain, "equation_test_medium.pkl",
                           num_instances=100, step_range=(10, 25))

    print("Generating test problems (hard)...")
    generate_test_problems(domain, "equation_test_hard.pkl",
                           num_instances=100, step_range=(20, 40))

    print("\nVerifying easy problems...")
    verify_solvability(domain, "equation_test_easy.pkl", num_check=15, max_nodes=50_000)

    print("\nVerifying medium problems...")
    verify_solvability(domain, "equation_test_medium.pkl", num_check=10, max_nodes=100_000)

    print("\nDone.")
