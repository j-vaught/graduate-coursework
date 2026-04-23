"""Generate visualization demos for the Warehouse MAPF domain."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "deepxube"))

import numpy as np
from collections import deque
import io
from typing import List, Optional, Tuple, Set

from PIL import Image

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import to_rgba

from deepxube.domains.warehouse_mapf import (
    WarehouseMAPF, MAPFState, MAPFGoal, MAPFAction,
    UP, DOWN, LEFT, RIGHT, WAIT, DIR_OFFSETS, DIR_NAMES,
)


def bfs_single_robot(obstacles, H, W, start, goal, extra_blocked=None):
    if start == goal:
        return [start]
    blocked = set(extra_blocked) if extra_blocked else set()
    blocked.discard(start)
    blocked.discard(goal)
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        (r, c), path = queue.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and not obstacles[nr, nc]:
                if (nr, nc) not in visited and (nr, nc) not in blocked:
                    visited.add((nr, nc))
                    new_path = path + [(nr, nc)]
                    if (nr, nc) == goal:
                        return new_path
                    queue.append(((nr, nc), new_path))
    return None


def solve_with_freezing(domain: WarehouseMAPF, start_state: MAPFState,
                        goal: MAPFGoal, max_steps: int = 200
                        ) -> Tuple[List[MAPFState], List[List[bool]]]:
    K = domain.K
    positions = [domain._get_pos(start_state, i) for i in range(K)]
    goals = [domain._get_goal_pos(goal, i) for i in range(K)]
    frozen = [pos == g for pos, g in zip(positions, goals)]

    path_states: List[MAPFState] = [start_state]
    frozen_history: List[List[bool]] = [list(frozen)]

    for step in range(max_steps):
        if all(frozen):
            break

        occupied: Set[Tuple[int, int]] = set()
        for i in range(K):
            if frozen[i]:
                occupied.add(positions[i])

        desired = list(positions)
        for i in range(K):
            if frozen[i]:
                continue
            extra_blocked = set()
            for j in range(K):
                if j != i and frozen[j]:
                    extra_blocked.add(positions[j])
            ind_path = bfs_single_robot(
                domain.obstacles, domain.H, domain.W,
                positions[i], goals[i], extra_blocked)
            if ind_path and len(ind_path) > 1:
                desired[i] = ind_path[1]

        actual = list(positions)
        claimed: Set[Tuple[int, int]] = set(occupied)

        for i in range(K):
            if frozen[i]:
                continue
            target = desired[i]
            if target in claimed:
                claimed.add(positions[i])
                continue
            swap = False
            for j in range(K):
                if j != i and target == positions[j] and desired[j] == positions[i]:
                    swap = True
                    break
            if swap:
                claimed.add(positions[i])
                continue
            actual[i] = target
            claimed.add(target)

        positions = actual
        for i in range(K):
            if not frozen[i] and positions[i] == goals[i]:
                frozen[i] = True

        pos_arr = np.zeros(2 * K, dtype=np.int8)
        for i in range(K):
            pos_arr[2 * i] = np.int8(positions[i][0])
            pos_arr[2 * i + 1] = np.int8(positions[i][1])
        path_states.append(MAPFState(pos_arr))
        frozen_history.append(list(frozen))

    return path_states, frozen_history


def fig_to_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    img = Image.open(buf).copy()
    buf.close()
    return img


def make_gif(domain: WarehouseMAPF, path: List[MAPFState], goal: MAPFGoal,
             filename: str, title_prefix: str = "", trails: int = 4,
             frozen_history: Optional[List[List[bool]]] = None):
    CELL = 64
    fig_side = max(10, domain.W * 0.55)
    frames = []
    for step_idx, s in enumerate(path):
        fig = plt.figure(figsize=(fig_side, fig_side), facecolor="#ECECEC")
        fr = frozen_history[step_idx] if frozen_history else None
        domain.visualize_state_goal(s, goal, fig, frozen=fr)

        trail_states = path[max(0, step_idx - trails):step_idx]
        if trail_states:
            ax = fig.axes[0]
            for t_idx, ts in enumerate(trail_states):
                alpha = 0.1 + 0.15 * (t_idx + 1) / len(trail_states)
                for i in range(domain.K):
                    if frozen_history and step_idx > 0:
                        t_frame = max(0, step_idx - trails) + t_idx
                        if frozen_history[t_frame][i]:
                            continue
                    tr, tc = domain._get_pos(ts, i)
                    color = domain.robot_colors[i]
                    cx = tc * CELL + CELL // 2
                    cy = tr * CELL + CELL // 2
                    ax.add_patch(mpatches.Circle(
                        (cx, cy), 10,
                        facecolor=to_rgba(color, alpha=alpha),
                        edgecolor='none', zorder=5))

        total = len(path) - 1
        step_label = f"Step {step_idx}/{total}"
        if title_prefix:
            step_label = f"{title_prefix}  |  {step_label}"
        fig.text(0.5, 0.97, step_label, ha="center", va="top",
                 fontsize=13, color="#363636", fontweight="bold")

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
        ox = (max_w - f.width) // 2
        oy = (max_h - f.height) // 2
        canvas.paste(f, (ox, oy))
        resized.append(canvas.convert("RGB"))

    durations = [600] * len(resized)
    durations[0] = 1500
    durations[-1] = 3000

    resized[0].save(
        filename, save_all=True, append_images=resized[1:],
        duration=durations, loop=0,
    )
    print(f"  Saved {filename} ({len(frames)} frames)", flush=True)


def make_snapshot(domain: WarehouseMAPF, state: MAPFState, goal: MAPFGoal,
                  filename: str, title: str = ""):
    fig_side = max(10, domain.W * 0.55)
    fig = plt.figure(figsize=(fig_side, fig_side), facecolor="#ECECEC")
    domain.visualize_state_goal(state, goal, fig)
    if title:
        fig.text(0.5, 0.97, title, ha="center", va="top",
                 fontsize=13, color="#363636", fontweight="bold")
    fig.savefig(filename, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved {filename}", flush=True)


def scramble_from_goal(domain, n_steps, seed=0):
    np.random.seed(seed)
    states, goals = domain.sample_goalstate_goal_pairs(1)
    scrambled = domain.random_walk_rev(states, [n_steps])
    return scrambled[0], goals[0]


def main():
    os.chdir(os.path.dirname(__file__) or ".")

    print("=== 28x28 warehouse, 30 robots ===", flush=True)
    d = WarehouseMAPF(28, 28, 30)
    print(f"  {d}", flush=True)

    best_path, best_goal, best_frozen = None, None, None
    best_steps = 0
    for seed in range(50):
        state, goal = scramble_from_goal(d, n_steps=40, seed=seed)
        path, frozen_hist = solve_with_freezing(d, state, goal, max_steps=150)
        n_steps = len(path) - 1
        solved = all(frozen_hist[-1])
        if solved and n_steps > best_steps:
            best_path, best_goal, best_frozen = path, goal, frozen_hist
            best_steps = n_steps
            print(f"  Seed {seed}: solved in {n_steps} steps", flush=True)
            if n_steps >= 25:
                break

    if best_path:
        make_snapshot(d, best_path[0], best_goal,
                      "mapf_28x28_30bot_states.png",
                      title="28x28 Warehouse  |  30 Robots")
        make_gif(d, best_path, best_goal,
                 "mapf_28x28_30bot_solve.gif",
                 title_prefix="28x28  |  30 Robots",
                 frozen_history=best_frozen)

    print("\nDone!", flush=True)


if __name__ == "__main__":
    main()
