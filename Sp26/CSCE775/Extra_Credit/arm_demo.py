"""
Robotic Arm domain demo.

Generates state snapshot figures, test problem .pkl files,
animated GIF solutions, and verifies solvability with BFS.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "deepxube"))

import numpy as np
import pickle
import time
import io
from collections import deque
from typing import List, Optional, Tuple

from PIL import Image

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from deepxube.domains.robotic_arm import RoboticArm, ArmState, ArmGoal


def bfs_solve(domain: RoboticArm, state: ArmState, goal: ArmGoal,
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


def bfs_solve_path(domain: RoboticArm, state: ArmState, goal: ArmGoal,
                   max_nodes: int = 50_000) -> Optional[List[ArmState]]:
    if domain.is_solved([state], [goal])[0]:
        return [state]
    queue: deque = deque([(state, [state])])
    visited = {state}
    nodes = 0
    while queue and nodes < max_nodes:
        cur, path = queue.popleft()
        actions = domain.get_state_actions([cur])[0]
        for act in actions:
            ns, _ = domain.next_state([cur], [act])
            nxt = ns[0]
            if nxt in visited:
                continue
            visited.add(nxt)
            nodes += 1
            new_path = path + [nxt]
            if domain.is_solved([nxt], [goal])[0]:
                return new_path
            queue.append((nxt, new_path))
    return None


def fig_to_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight", facecolor="white")
    buf.seek(0)
    img = Image.open(buf).copy()
    buf.close()
    return img


def make_snapshot(domain: RoboticArm) -> None:
    np.random.seed(42)
    fig = plt.figure(figsize=(10, 8), facecolor="white")
    states, goals = domain.sample_goalstate_goal_pairs(1)
    start = domain.random_walk_rev(states, [8])[0]
    domain.visualize_state_goal(start, goals[0], fig)
    fig.savefig("arm_states.png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    print("Saved arm_states.png")
    plt.close(fig)


def make_gif(domain: RoboticArm, path: List[ArmState], goal: ArmGoal,
             filename: str, title_prefix: str = "") -> None:
    frames = []
    for step_idx, s in enumerate(path):
        fig = plt.figure(figsize=(10, 8), facecolor="white")
        domain.visualize_state_goal(s, goal, fig)
        total = len(path) - 1
        step_label = f"Step {step_idx}/{total}"
        if title_prefix:
            step_label = f"{title_prefix}  |  {step_label}"
        fig.text(0.5, 0.97, step_label, ha="center", va="top",
                 fontsize=11, color="#363636", fontweight="bold")
        img = fig_to_image(fig)
        plt.close(fig)
        frames.append(img)

    if not frames:
        return

    max_w = max(f.width for f in frames)
    max_h = max(f.height for f in frames)
    resized = []
    for f in frames:
        canvas = Image.new("RGBA", (max_w, max_h), (255, 255, 255, 255))
        offset_x = (max_w - f.width) // 2
        offset_y = (max_h - f.height) // 2
        canvas.paste(f, (offset_x, offset_y))
        resized.append(canvas.convert("RGB"))

    durations = [1200] * len(resized)
    durations[0] = 2000
    durations[-1] = 3000

    resized[0].save(
        filename, save_all=True, append_images=resized[1:],
        duration=durations, loop=0,
    )
    print(f"Saved {filename} ({len(frames)} frames)")


def show_action_example(domain: RoboticArm) -> None:
    np.random.seed(7)
    states, goals = domain.sample_goalstate_goal_pairs(1)
    start = domain.random_walk_rev(states, [4])[0]
    print(f"\nExample state: {start}")
    ee = domain._ee_position(start.joints)
    print(f"EE position: ({ee[0]:.3f}, {ee[1]:.3f}, {ee[2]:.3f})")
    print(f"EE bins:     {domain._position_to_bins(ee)}")
    print(f"Target bins: {goals[0].bins}")
    actions = domain.get_state_actions([start])[0]
    print(f"Available actions ({len(actions)}):")
    for act in actions:
        ns, _ = domain.next_state([start], [act])
        new_ee = domain._ee_position(ns[0].joints)
        print(f"  {act!r:6s} -> EE ({new_ee[0]:+.2f}, {new_ee[1]:+.2f}, {new_ee[2]:+.2f})")


def generate_test_problems(domain: RoboticArm, filename: str,
                           num_instances: int = 100,
                           step_range: Tuple[int, int] = (5, 20)) -> None:
    np.random.seed(123)
    num_steps = list(np.random.randint(step_range[0], step_range[1] + 1,
                                       size=num_instances))
    states, goals = domain.sample_problem_instances(num_steps)
    data = {"states": states, "goals": goals}
    with open(filename, "wb") as f:
        pickle.dump(data, f, protocol=-1)
    print(f"Saved {num_instances} problem instances to {filename}")


def verify_solvability(domain: RoboticArm, filename: str,
                       num_check: int = 10,
                       max_nodes: int = 50_000) -> None:
    with open(filename, "rb") as f:
        data = pickle.load(f)
    states = data["states"][:num_check]
    goals = data["goals"][:num_check]

    solved_count = 0
    total_steps = 0

    print(f"\nVerifying solvability of {num_check} instances "
          f"(BFS, max {max_nodes} nodes)...")
    for i, (s, g) in enumerate(zip(states, goals)):
        t0 = time.time()
        depth = bfs_solve(domain, s, g, max_nodes=max_nodes)
        elapsed = time.time() - t0
        if depth is not None:
            solved_count += 1
            total_steps += depth
            print(f"  [{i:2d}] SOLVED in {depth:3d} steps ({elapsed:.2f}s)  "
                  f"{s}  ->  {g}")
        else:
            print(f"  [{i:2d}] NOT SOLVED ({elapsed:.2f}s)  "
                  f"{s}  ->  {g}")

    print(f"\nSolved: {solved_count}/{num_check}")
    if solved_count > 0:
        print(f"Avg steps: {total_steps / solved_count:.1f}")


def find_and_make_gif(domain: RoboticArm, filename: str,
                      scramble_depths: List[int],
                      path_range: Tuple[int, int],
                      max_nodes: int = 80_000) -> bool:
    for depth in scramble_depths:
        for attempt in range(50):
            np.random.seed(42 + attempt + depth * 100)
            gs, gg = domain.sample_goalstate_goal_pairs(1)
            scrambled = domain.random_walk_rev(gs, [depth])[0]
            path = bfs_solve_path(domain, scrambled, gg[0],
                                  max_nodes=max_nodes)
            if path and path_range[0] <= len(path) <= path_range[1]:
                print(f"  Found path: {len(path)-1} steps "
                      f"(scramble={depth}, attempt={attempt})")
                make_gif(domain, path, gg[0], filename, "Robotic Arm")
                return True
    return False


def main():
    domain = RoboticArm(n_joints=6, n_angle_steps=12, n_pos_bins=8)
    print(f"Domain: {domain}")

    print("\nGenerating visualization...")
    make_snapshot(domain)

    show_action_example(domain)

    print("\nSearching for a GIF-worthy BFS solution...")
    if not find_and_make_gif(domain, "arm_solve.gif",
                             scramble_depths=[4, 5, 6],
                             path_range=(4, 12)):
        print("  Could not find a good example for GIF")

    print("\nGenerating test problems (easy)...")
    generate_test_problems(domain, "arm_test_easy.pkl",
                           num_instances=100, step_range=(3, 8))

    print("Generating test problems (medium)...")
    generate_test_problems(domain, "arm_test_medium.pkl",
                           num_instances=100, step_range=(6, 15))

    print("Generating test problems (hard)...")
    generate_test_problems(domain, "arm_test_hard.pkl",
                           num_instances=100, step_range=(12, 30))

    print("\nVerifying easy problems...")
    verify_solvability(domain, "arm_test_easy.pkl",
                       num_check=10, max_nodes=50_000)

    print("\nDone.")


if __name__ == "__main__":
    main()
