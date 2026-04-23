"""
Generate multi-view animated GIFs for the Robotic Arm domain
across several configurations (varying joints, angle steps).
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "deepxube"))

import numpy as np
import random as stdlib_random
import io
from collections import deque
from typing import List, Optional, Tuple

from PIL import Image

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from deepxube.domains.robotic_arm import RoboticArm, ArmState, ArmGoal


def bfs_solve_path(domain, state, goal, max_nodes=80_000):
    if domain.is_solved([state], [goal])[0]:
        return [state]
    queue = deque([(state, [state])])
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
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    img = Image.open(buf).copy()
    buf.close()
    return img


def make_multiview_gif(domain, path, goal, filename, title_prefix=""):
    frames = []
    for step_idx, s in enumerate(path):
        fig = plt.figure(figsize=(20, 7), facecolor="#ECECEC")
        domain.visualize_multi_view(s, goal, fig)
        total = len(path) - 1
        step_label = f"Step {step_idx}/{total}"
        if title_prefix:
            step_label = f"{title_prefix}  |  {step_label}"
        fig.text(0.5, 0.97, step_label, ha="center", va="top",
                 fontsize=13, color="#363636", fontweight="bold")
        fig.subplots_adjust(wspace=0.05)
        img = fig_to_image(fig)
        plt.close(fig)
        frames.append(img)

    if not frames:
        return

    max_w = max(f.width for f in frames)
    max_h = max(f.height for f in frames)
    resized = []
    for f in frames:
        canvas = Image.new("RGBA", (max_w, max_h), (236, 236, 236, 255))
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
    print(f"  Saved {filename} ({len(frames)} frames)")


def make_multiview_snapshot(domain, state, goal, filename, title=""):
    fig = plt.figure(figsize=(20, 7), facecolor="#ECECEC")
    domain.visualize_multi_view(state, goal, fig)
    if title:
        fig.text(0.5, 0.97, title, ha="center", va="top",
                 fontsize=13, color="#363636", fontweight="bold")
    fig.subplots_adjust(wspace=0.05)
    fig.savefig(filename, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved {filename}")


def find_best_path(domain, scramble_depths, min_len, max_len,
                   max_seeds=200, max_nodes=80_000):
    best_path = None
    best_goal = None
    for seed in range(max_seeds):
        np.random.seed(seed)
        stdlib_random.seed(seed)
        for depth in scramble_depths:
            gs, gg = domain.sample_goalstate_goal_pairs(1)
            scrambled = domain.random_walk_rev(gs, [depth])[0]
            path = bfs_solve_path(domain, scrambled, gg[0],
                                  max_nodes=max_nodes)
            if path and min_len <= len(path) <= max_len:
                if best_path is None or len(path) > len(best_path):
                    best_path = path
                    best_goal = gg[0]
                    if len(path) >= min_len + 3:
                        return best_path, best_goal
    return best_path, best_goal


CONFIGS = [
    {
        "label": "6 joints, 12 steps",
        "n_joints": 6, "n_angle_steps": 12, "n_pos_bins": 16,
        "scrambles": [8, 10, 12],
        "path_range": (5, 14),
        "prefix": "arm_6j12s",
    },
    {
        "label": "8 joints, 12 steps",
        "n_joints": 8, "n_angle_steps": 12, "n_pos_bins": 16,
        "scrambles": [8, 10, 12],
        "path_range": (5, 14),
        "prefix": "arm_8j12s",
    },
    {
        "label": "6 joints, 24 steps",
        "n_joints": 6, "n_angle_steps": 24, "n_pos_bins": 16,
        "scrambles": [10, 14, 18],
        "path_range": (6, 16),
        "prefix": "arm_6j24s",
    },
    {
        "label": "10 joints, 12 steps",
        "n_joints": 10, "n_angle_steps": 12, "n_pos_bins": 16,
        "scrambles": [8, 10, 12],
        "path_range": (5, 14),
        "prefix": "arm_10j12s",
    },
]


def main():
    for cfg in CONFIGS:
        label = cfg["label"]
        print(f"\n=== {label} ===")
        domain = RoboticArm(
            n_joints=cfg["n_joints"],
            n_angle_steps=cfg["n_angle_steps"],
            n_pos_bins=cfg["n_pos_bins"],
        )
        print(f"  {domain}")
        print(f"  State space: {cfg['n_angle_steps']}^{cfg['n_joints']} "
              f"= {cfg['n_angle_steps'] ** cfg['n_joints']:,}")

        path, goal = find_best_path(
            domain,
            scramble_depths=cfg["scrambles"],
            min_len=cfg["path_range"][0],
            max_len=cfg["path_range"][1],
        )

        if path is None:
            print("  Could not find a solvable example")
            continue

        print(f"  Best path: {len(path)-1} steps")

        make_multiview_snapshot(
            domain, path[0], goal,
            f"{cfg['prefix']}_states.png",
            title=f"{label}  (16 bins)",
        )

        make_multiview_gif(
            domain, path, goal,
            f"{cfg['prefix']}_solve.gif",
            title_prefix=f"{label}",
        )

    print("\nDone!")


if __name__ == "__main__":
    main()
