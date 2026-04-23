"""Generate visualization demos for the Warehouse MAPF domain."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "deepxube"))

import numpy as np
import heapq
import io
from typing import List, Optional, Tuple

from PIL import Image

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from deepxube.domains.warehouse_mapf import (
    WarehouseMAPF, MAPFState, MAPFGoal, MAPFAction,
    UP, DOWN, LEFT, RIGHT, WAIT, DIR_NAMES,
)


def reverse_walk_path(domain: WarehouseMAPF, n_steps: int,
                      seed: int = 0) -> Tuple[List[MAPFState], MAPFGoal]:
    np.random.seed(seed)
    states_g, goals = domain.sample_goalstate_goal_pairs(1)
    goal = goals[0]
    cur = states_g[0]
    forward_path = [cur]
    for _ in range(n_steps):
        act = domain._sample_random_action(cur)
        nxt, _ = domain.next_state([cur], [act])
        cur = nxt[0]
        forward_path.append(cur)
    forward_path.reverse()
    return forward_path, goal


def manhattan_heuristic(state: MAPFState, goal: MAPFGoal,
                        K: int) -> int:
    max_d = 0
    for i in range(K):
        sr, sc = int(state.positions[2*i]), int(state.positions[2*i+1])
        gr, gc = int(goal.positions[2*i]), int(goal.positions[2*i+1])
        d = abs(sr - gr) + abs(sc - gc)
        if d > max_d:
            max_d = d
    return max_d


def astar_solve(domain: WarehouseMAPF, state: MAPFState, goal: MAPFGoal,
                max_nodes: int = 100_000) -> Optional[List[MAPFState]]:
    if domain.is_solved([state], [goal])[0]:
        return [state]

    h0 = manhattan_heuristic(state, goal, domain.K)
    open_set = [(h0, 0, id(state), state, [state])]
    visited = {state}
    nodes = 0

    while open_set and nodes < max_nodes:
        f, g, _, cur, path = heapq.heappop(open_set)
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
                print(f"    A* solved: {len(new_path)-1} steps, {nodes} nodes")
                return new_path
            h = manhattan_heuristic(nxt, goal, domain.K)
            heapq.heappush(open_set, (g + 1 + h, g + 1, id(nxt), nxt, new_path))

    print(f"    A* exhausted {nodes} nodes")
    return None


def fig_to_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    img = Image.open(buf).copy()
    buf.close()
    return img


def make_gif(domain: WarehouseMAPF, path: List[MAPFState], goal: MAPFGoal,
             filename: str, title_prefix: str = "", trails: int = 4):
    from deepxube.domains.warehouse_mapf import ROBOT_COLORS
    import matplotlib.patches as mpatches
    from matplotlib.colors import to_rgba
    CELL = 64
    fig_side = max(10, domain.W * 0.55)
    frames = []
    for step_idx, s in enumerate(path):
        fig = plt.figure(figsize=(fig_side, fig_side), facecolor="#ECECEC")
        domain.visualize_state_goal(s, goal, fig)

        trail_states = path[max(0, step_idx - trails):step_idx]
        if trail_states:
            ax = fig.axes[0]
            for t_idx, ts in enumerate(trail_states):
                alpha = 0.1 + 0.15 * (t_idx + 1) / len(trail_states)
                for i in range(domain.K):
                    tr, tc = domain._get_pos(ts, i)
                    color = ROBOT_COLORS[i]
                    cx = tc * CELL + CELL // 2
                    cy = tr * CELL + CELL // 2
                    ax.add_patch(mpatches.Circle(
                        (cx, cy), 12,
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

    durations = [800] * len(resized)
    durations[0] = 1500
    durations[-1] = 2500

    resized[0].save(
        filename, save_all=True, append_images=resized[1:],
        duration=durations, loop=0,
    )
    print(f"  Saved {filename} ({len(frames)} frames)")


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
    print(f"  Saved {filename}")


def main():
    os.chdir(os.path.dirname(__file__) or ".")

    print("=== 20x20 warehouse, 8 robots (reverse walk demo) ===")
    d20 = WarehouseMAPF(20, 20, 8)
    print(f"  {d20}")

    best_path, best_goal = None, None
    for seed in range(50):
        path, goal = reverse_walk_path(d20, n_steps=20, seed=seed)
        h = manhattan_heuristic(path[0], goal, d20.K)
        if h >= 8 and (best_path is None or h > manhattan_heuristic(best_path[0], best_goal, d20.K)):
            best_path, best_goal = path, goal
            print(f"  Seed {seed}: {len(path)-1} steps, max-Manhattan={h}")
            if h >= 12:
                break

    if best_path:
        make_snapshot(d20, best_path[0], best_goal,
                      "mapf_20x20_8bot_states.png",
                      title="20x20 Warehouse  |  8 Robots")
        make_gif(d20, best_path, best_goal,
                 "mapf_20x20_8bot_solve.gif",
                 title_prefix="20x20  |  8 Robots")

    print("\n=== 20x20 warehouse, 4 robots (A* optimal) ===")
    d20_4 = WarehouseMAPF(20, 20, 4)
    print(f"  {d20_4}")

    best_path4, best_goal4 = None, None
    for seed in range(100):
        np.random.seed(seed)
        states, goals = d20_4.sample_goalstate_goal_pairs(1)
        scrambled = d20_4.random_walk_rev(states, [8])
        h = manhattan_heuristic(scrambled[0], goals[0], d20_4.K)
        if h < 4:
            continue
        path = astar_solve(d20_4, scrambled[0], goals[0], max_nodes=200_000)
        if path and len(path) >= 5:
            if best_path4 is None or len(path) > len(best_path4):
                best_path4, best_goal4 = path, goals[0]
                print(f"  Seed {seed}: {len(path)-1} steps (A* optimal)")
                if len(path) >= 8:
                    break

    if best_path4:
        make_snapshot(d20_4, best_path4[0], best_goal4,
                      "mapf_20x20_4bot_states.png",
                      title="20x20 Warehouse  |  4 Robots  |  A* Optimal")
        make_gif(d20_4, best_path4, best_goal4,
                 "mapf_20x20_4bot_solve.gif",
                 title_prefix="20x20  |  4 Robots  |  Optimal")

    print("\n=== 28x28 warehouse, 10 robots (reverse walk demo) ===")
    d28 = WarehouseMAPF(28, 28, 10)
    print(f"  {d28}")

    best_path28, best_goal28 = None, None
    for seed in range(50):
        path, goal = reverse_walk_path(d28, n_steps=30, seed=seed)
        h = manhattan_heuristic(path[0], goal, d28.K)
        if h >= 10 and (best_path28 is None or h > manhattan_heuristic(best_path28[0], best_goal28, d28.K)):
            best_path28, best_goal28 = path, goal
            print(f"  Seed {seed}: {len(path)-1} steps, max-Manhattan={h}")
            if h >= 15:
                break

    if best_path28:
        make_snapshot(d28, best_path28[0], best_goal28,
                      "mapf_28x28_10bot_states.png",
                      title="28x28 Warehouse  |  10 Robots")
        make_gif(d28, best_path28, best_goal28,
                 "mapf_28x28_10bot_solve.gif",
                 title_prefix="28x28  |  10 Robots")

    print("\nDone!")


if __name__ == "__main__":
    main()
