"""
Hanoi domain demo: state snapshots + optimal-solution animation.

The animation shows the known recursive optimal solution (2^N - 1 moves).
No trained model is required — this demonstrates the domain mechanics.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "deepxube"))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.figure import Figure
from typing import List, Tuple

import deepxube  # triggers domain registration
from deepxube.domains.hanoi import Hanoi, HanoiState, HanoiGoal, HanoiAction

# ---------------------------------------------------------------------------
# Brand colours
# ---------------------------------------------------------------------------
GARNET    = "#73000A"
BLACK_90  = "#363636"
BLACK_70  = "#5C5C5C"
ATLANTIC  = "#466A9F"
CONGAREE  = "#1F414D"
HORSESHOE = "#65780B"
HONEYCOMB = "#A49137"
ROSE      = "#CC2E40"
GRASS     = "#CED318"
SANDSTORM = "#FFF2E3"

DISK_COLORS = [GARNET, ATLANTIC, CONGAREE, HORSESHOE, HONEYCOMB, ROSE]

# ---------------------------------------------------------------------------
# Optimal Tower of Hanoi solution (recursive)
# ---------------------------------------------------------------------------

def hanoi_moves(n: int, src: int, dst: int, aux: int) -> List[Tuple[int, int]]:
    """Return the optimal move sequence as list of (from_peg, to_peg)."""
    if n == 0:
        return []
    return (
        hanoi_moves(n - 1, src, aux, dst)
        + [(src, dst)]
        + hanoi_moves(n - 1, aux, dst, src)
    )


def apply_move(state: np.ndarray, move: Tuple[int, int], num_pegs: int) -> np.ndarray:
    """Return new state after applying move (from_peg, to_peg)."""
    state = state.copy()
    f, t = move
    # top disk on f = largest index i with state[i] == f
    on_f = np.where(state == f)[0]
    if len(on_f) == 0:
        return state
    top = on_f.max()
    state[top] = t
    return state


# ---------------------------------------------------------------------------
# Low-level drawing helper (used by both the snapshot grid and the animation)
# ---------------------------------------------------------------------------

def draw_hanoi(ax: plt.Axes, disks: np.ndarray, goal_disks: np.ndarray,
               num_disks: int, num_pegs: int, title: str = "") -> None:
    ax.clear()
    ax.set_facecolor(SANDSTORM)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=9, color=BLACK_90, pad=4)

    peg_xs = [(p + 1) / (num_pegs + 1) for p in range(num_pegs)]
    base_y  = 0.10
    disk_h  = min(0.10, 0.65 / num_disks)
    disk_gap = 0.01
    max_w   = 0.26
    peg_w   = 0.012

    # Base platform
    ax.add_patch(patches.FancyBboxPatch(
        (0.04, base_y - 0.038), 0.92, 0.028,
        boxstyle="square,pad=0", facecolor=BLACK_90, edgecolor="none",
    ))

    # Peg rods
    rod_h = base_y + num_disks * (disk_h + disk_gap) + 0.06
    for px in peg_xs:
        ax.add_patch(patches.Rectangle(
            (px - peg_w / 2, base_y - 0.010), peg_w, rod_h,
            facecolor=BLACK_70, edgecolor="none",
        ))

    # Collect disks per peg (index 0 = largest = visual bottom)
    disks_per_peg: List[List[int]] = [[] for _ in range(num_pegs)]
    for disk_i in range(num_disks):
        disks_per_peg[int(disks[disk_i])].append(disk_i)

    goal_peg_uniform = int(goal_disks[0]) if np.all(goal_disks == goal_disks[0]) else -1

    for peg_idx, stack in enumerate(disks_per_peg):
        px = peg_xs[peg_idx]
        for pos, disk_i in enumerate(stack):
            frac = (num_disks - disk_i) / num_disks
            w = max_w * frac + 0.03
            y = base_y + pos * (disk_h + disk_gap)

            color = DISK_COLORS[disk_i % len(DISK_COLORS)]
            on_goal = (peg_idx == int(goal_disks[disk_i]))
            edge_color = GRASS if on_goal else BLACK_90
            edge_lw    = 2.2  if on_goal else 0.7

            ax.add_patch(patches.FancyBboxPatch(
                (px - w / 2, y), w, disk_h,
                boxstyle="square,pad=0",
                facecolor=color, edgecolor=edge_color, linewidth=edge_lw,
            ))
            ax.text(px, y + disk_h / 2, str(disk_i),
                    ha="center", va="center", fontsize=7,
                    color="white", fontweight="bold")

    # Peg labels
    for p, px in enumerate(peg_xs):
        suffix = " ★" if p == goal_peg_uniform else ""
        ax.text(px, 0.025, f"Peg {p}{suffix}",
                ha="center", va="center", fontsize=7.5, color=BLACK_90)


# ---------------------------------------------------------------------------
# 1.  State snapshot grid
# ---------------------------------------------------------------------------

def make_snapshot_figure(num_disks: int = 4, num_pegs: int = 3) -> None:
    domain = Hanoi(num_disks=num_disks, num_pegs=num_pegs)
    goal   = np.full(num_disks, num_pegs - 1, dtype=np.uint8)

    # Hand-pick five representative states
    configs = [
        ("Solved (goal)", np.full(num_disks, num_pegs - 1, dtype=np.uint8)),
        ("Start (all on peg 0)", np.zeros(num_disks, dtype=np.uint8)),
        ("Mid-solve (mixed)",
         np.array([0, 2, 1, 2][:num_disks], dtype=np.uint8)),
        ("Random scramble A",
         domain.random_walk([HanoiState(goal.copy())], [8])[0][0].disks),
        ("Random scramble B",
         domain.random_walk([HanoiState(goal.copy())], [14])[0][0].disks),
    ]

    fig, axes = plt.subplots(1, 5, figsize=(14, 3.2), facecolor="white")
    fig.subplots_adjust(wspace=0.04, left=0.01, right=0.99, top=0.88, bottom=0.02)
    fig.suptitle(
        f"Tower of Hanoi  ({num_disks} disks, {num_pegs} pegs)  —  Example States",
        fontsize=11, color=BLACK_90, fontweight="bold", y=0.98,
    )

    for ax, (title, cfg) in zip(axes, configs):
        draw_hanoi(ax, cfg, goal, num_disks, num_pegs, title)

    fig.savefig("hanoi_states.png", dpi=150, bbox_inches="tight", facecolor="white")
    print("Saved hanoi_states.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 2.  Optimal-solution animation
# ---------------------------------------------------------------------------

def make_solution_animation(num_disks: int = 4, num_pegs: int = 3) -> None:
    goal_peg = num_pegs - 1
    start_disks = np.zeros(num_disks, dtype=np.uint8)   # all on peg 0
    goal_disks  = np.full(num_disks, goal_peg, dtype=np.uint8)

    # Optimal move sequence
    aux_peg = 1  # for 3-peg standard Hanoi
    moves = hanoi_moves(num_disks, src=0, dst=goal_peg, aux=aux_peg)

    # Build state sequence
    states = [start_disks.copy()]
    cur = start_disks.copy()
    for move in moves:
        cur = apply_move(cur, move, num_pegs)
        states.append(cur.copy())

    total_frames = len(states)  # 2^N

    fig, ax = plt.subplots(figsize=(4.5, 4), facecolor="white")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.02)

    move_labels = ["Start"] + [f"Move {i+1}: peg {f} → peg {t}" for i, (f, t) in enumerate(moves)]

    def update(frame: int) -> list:
        draw_hanoi(ax, states[frame], goal_disks, num_disks, num_pegs,
                   title=move_labels[frame])
        pct = int(100 * frame / (total_frames - 1))
        fig.suptitle(
            f"Optimal solution  ({total_frames - 1} moves total)   [{pct}% complete]",
            fontsize=8.5, color=BLACK_90, y=0.97,
        )
        return []

    ani = animation.FuncAnimation(
        fig, update,
        frames=total_frames,
        interval=600,   # ms per frame
        blit=False,
        repeat=True,
    )

    writer = animation.PillowWriter(fps=1.5)
    ani.save("hanoi_solution.gif", writer=writer, dpi=120)
    print(f"Saved hanoi_solution.gif  ({total_frames} frames, {total_frames - 1} moves)")
    plt.close(fig)


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Generating state snapshots...")
    make_snapshot_figure(num_disks=4, num_pegs=3)

    print("Generating solution animation...")
    make_solution_animation(num_disks=4, num_pegs=3)

    print("Done.")
