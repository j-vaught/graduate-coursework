"""
Word Ladder domain demo.

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

from deepxube.domains.wordladder import WordLadder, WLState, WLGoal, WLAction

GARNET = "#73000A"
BLACK_90 = "#363636"
SANDSTORM = "#FFF2E3"


def bfs_solve(domain: WordLadder, state: WLState, goal: WLGoal,
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


def make_snapshot_figure(domain: WordLadder) -> None:
    np.random.seed(42)

    configs: List[Tuple[str, WLState, WLGoal]] = []

    states0, goals0 = domain.sample_goalstate_goal_pairs(1)
    configs.append(("Goal state (solved)", states0[0], goals0[0]))

    states1, goals1 = domain.sample_goalstate_goal_pairs(1)
    scr1 = domain.random_walk_rev(states1, [3])
    configs.append(("3-step scramble", scr1[0], goals1[0]))

    states2, goals2 = domain.sample_goalstate_goal_pairs(1)
    scr2 = domain.random_walk_rev(states2, [8])
    configs.append(("8-step scramble", scr2[0], goals2[0]))

    states3, goals3 = domain.sample_goalstate_goal_pairs(1)
    scr3 = domain.random_walk_rev(states3, [15])
    configs.append(("15-step scramble", scr3[0], goals3[0]))

    states4, goals4 = domain.sample_goalstate_goal_pairs(1)
    scr4 = domain.random_walk_rev(states4, [25])
    configs.append(("25-step scramble", scr4[0], goals4[0]))

    fig, axes = plt.subplots(1, 5, figsize=(18, 4), facecolor="white")
    fig.subplots_adjust(wspace=0.08, left=0.01, right=0.99, top=0.88, bottom=0.02)
    fig.suptitle("Word Ladder  —  Example States",
                 fontsize=12, color=BLACK_90, fontweight="bold", y=0.97)

    for ax, (title, state, goal) in zip(axes, configs):
        ax.set_title(title, fontsize=9, color=BLACK_90, pad=4)
        domain.visualize_state_goal(state, goal, fig)
        target_ax = fig.axes[-1]
        target_ax.set_position(ax.get_position())
        ax.remove()

    fig.savefig("wordladder_states.png", dpi=150, bbox_inches="tight", facecolor="white")
    print("Saved wordladder_states.png")
    plt.close(fig)


def make_simple_snapshot(domain: WordLadder) -> None:
    np.random.seed(42)
    fig = plt.figure(figsize=(6, 5), facecolor="white")
    states, goals = domain.sample_goalstate_goal_pairs(1)
    start = domain.random_walk_rev(states, [10])[0]
    domain.visualize_state_goal(start, goals[0], fig)
    fig.savefig("wordladder_states.png", dpi=150, bbox_inches="tight", facecolor="white")
    print("Saved wordladder_states.png")
    plt.close(fig)


def generate_test_problems(domain: WordLadder,
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


def verify_solvability(domain: WordLadder, filename: str,
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
        if depth is not None:
            solved_count += 1
            total_steps += depth
            print(f"  [{i:2d}] SOLVED in {depth:3d} steps ({elapsed:.2f}s)  "
                  f"{s.word}  ->  {g.word}")
        else:
            print(f"  [{i:2d}] NOT SOLVED ({elapsed:.2f}s)  "
                  f"{s.word}  ->  {g.word}")

    print(f"\nSolved: {solved_count}/{num_check}")
    if solved_count > 0:
        print(f"Avg steps: {total_steps / solved_count:.1f}")


if __name__ == "__main__":
    domain = WordLadder(word_len=4)

    print("Generating visualization...")
    make_simple_snapshot(domain)

    print("\nGenerating test problems (easy)...")
    generate_test_problems(domain, "wordladder_test_easy.pkl",
                           num_instances=100, step_range=(3, 8))

    print("Generating test problems (medium)...")
    generate_test_problems(domain, "wordladder_test_medium.pkl",
                           num_instances=100, step_range=(8, 20))

    print("Generating test problems (hard)...")
    generate_test_problems(domain, "wordladder_test_hard.pkl",
                           num_instances=100, step_range=(15, 35))

    print("\nVerifying easy problems...")
    verify_solvability(domain, "wordladder_test_easy.pkl", num_check=15, max_nodes=50_000)

    print("\nVerifying medium problems...")
    verify_solvability(domain, "wordladder_test_medium.pkl", num_check=10, max_nodes=100_000)

    print("\nDone.")
