"""
Generate animated GIF visualization for the Retrosynthesis domain.
Shows BFS solving sequence step-by-step.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "deepxube"))

import numpy as np
from collections import deque
from typing import List, Optional
from PIL import Image
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from deepxube.domains.retrosynthesis import Retrosynthesis, RetroState, RetroGoal


def bfs_solve_path(domain, state, goal, max_nodes=100_000):
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
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight", facecolor="white")
    buf.seek(0)
    img = Image.open(buf).copy()
    buf.close()
    return img


def make_gif(domain, state, goal, path, filename, title_prefix=""):
    frames = []
    for step_idx, s in enumerate(path):
        fig = plt.figure(figsize=(10, 7), facecolor="white")
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
        filename,
        save_all=True,
        append_images=resized[1:],
        duration=durations,
        loop=0,
    )
    print(f"Saved {filename} ({len(frames)} frames)")


def main():
    np.random.seed(42)
    domain = Retrosynthesis(chain_len=5)

    print("=== Retrosynthesis ===")
    for attempt in range(50):
        np.random.seed(42 + attempt)
        gs, gg = domain.sample_goalstate_goal_pairs(1)
        scrambled = domain.random_walk_rev(gs, [6])[0]
        path = bfs_solve_path(domain, scrambled, gg[0], max_nodes=80_000)
        if path and 4 <= len(path) <= 12:
            print(f"  Found path: {len(path)-1} steps (attempt {attempt})")
            make_gif(domain, scrambled, gg[0], path,
                     "retro_solve.gif", "Retrosynthesis")
            break
    else:
        print("  Could not find a good example, trying shorter scramble...")
        for attempt in range(50):
            np.random.seed(200 + attempt)
            gs, gg = domain.sample_goalstate_goal_pairs(1)
            scrambled = domain.random_walk_rev(gs, [4])[0]
            path = bfs_solve_path(domain, scrambled, gg[0], max_nodes=80_000)
            if path and 3 <= len(path) <= 10:
                print(f"  Found path: {len(path)-1} steps (attempt {attempt})")
                make_gif(domain, scrambled, gg[0], path,
                         "retro_solve.gif", "Retrosynthesis")
                break
        else:
            print("  Could not find a solvable example for GIF")

    print("\nDone!")


if __name__ == "__main__":
    main()
