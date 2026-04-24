"""Generate two four-bar linkage GIFs:
1. Solve process: scrambled → target configuration step-by-step
2. Mechanism motion: crank rotating through full cycle in solved config
"""
import sys
sys.path.insert(0, "/Users/user/Downloads/graduate-coursework/Sp26/CSCE775/Extra_Credit/deepxube")

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import io

from deepxube.domains.four_bar_linkage import (
    FourBarLinkage, LinkState, LinkGoal, LinkAction, PARAM_NAMES,
    GARNET, ATLANTIC, HORSESHOE, CONGAREE, ROSE, BLACK_90, BLACK_30, BLACK_10,
    SENTINEL,
)

OUT = "/Users/user/Downloads/graduate-coursework/Sp26/CSCE775/Extra_Credit"

env = FourBarLinkage(n_steps=64, n_waypoints=64, n_bins=64)


def fig_to_pil(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    img = Image.open(buf).convert("RGBA")
    return img


# ── Find an interesting goal with a non-circular curve and full waypoints ──
np.random.seed(0)
best_state = best_goal = None
best_score = -1
for _ in range(500):
    params = np.random.randint(0, 64, size=6).astype(np.int8)
    vals = env._idx_to_continuous(params)
    a, b, c, d, p, beta = vals
    if p < 1.2:
        continue
    curve = env._coupler_curve(params)
    n_valid = np.sum(~np.isnan(curve[:, 0]))
    if n_valid < 60:
        continue
    valid = ~np.isnan(curve[:, 0])
    vc = curve[valid]
    cx, cy = vc.mean(axis=0)
    dists = np.sqrt((vc[:, 0] - cx)**2 + (vc[:, 1] - cy)**2)
    irregularity = dists.std() / (dists.mean() + 1e-9)
    score = irregularity * n_valid
    if score > best_score:
        best_score = score
        best_state = LinkState(params.copy())
        best_goal = LinkGoal(env._curve_to_bins(curve))

goal_state = best_state
goal = best_goal
print(f"Goal params: {goal_state.params}, score: {best_score:.2f}")
print(f"Continuous: {env._idx_to_continuous(goal_state.params)}")

# ── Scramble from goal ──
np.random.seed(42)
scramble_depth = 25
current = LinkState(goal_state.params.copy())
scramble_path = [LinkState(current.params.copy())]
for _ in range(scramble_depth):
    act = env.all_actions[np.random.randint(len(env.all_actions))]
    new_states, _ = env.next_state([current], [act])
    current = new_states[0]
    scramble_path.append(LinkState(current.params.copy()))

scramble_path.reverse()
scrambled_state = scramble_path[0]

# ── GIF 1: Solve process ──
print("Generating solve GIF...")
frames = []
for step_i, state in enumerate(scramble_path):
    fig = plt.figure(figsize=(14, 5.5))
    env.visualize_state_goal(state, goal, fig)
    fig.text(0.5, 0.96, f"Step {step_i}/{scramble_depth}",
             ha="center", va="top", fontsize=13, color=BLACK_90,
             fontweight="bold")
    params_str = "  ".join(
        f"{PARAM_NAMES[i]}={int(state.params[i])}" for i in range(6))
    fig.text(0.5, 0.92, params_str,
             ha="center", va="top", fontsize=8, color=BLACK_90,
             family="monospace")
    img = fig_to_pil(fig)
    plt.close(fig)
    n_dup = 6 if (step_i == 0 or step_i == scramble_depth) else 1
    for _ in range(n_dup):
        frames.append(img)

frames[0].save(
    f"{OUT}/linkage_solve.gif",
    save_all=True, append_images=frames[1:],
    duration=250, loop=0, optimize=True,
)
print(f"  Saved linkage_solve.gif ({len(frames)} frames)")

# ── GIF 2: Mechanism motion in solved configuration ──
print("Generating mechanism motion GIF...")

vals = env._idx_to_continuous(goal_state.params)
a, b, c, d, p, beta = vals
coupler_curve = env._coupler_curve(goal_state.params)
valid_mask = ~np.isnan(coupler_curve[:, 0])
trail_x = coupler_curve[valid_mask, 0]
trail_y = coupler_curve[valid_mask, 1]

n_anim_frames = 72
thetas = np.linspace(0, 2 * np.pi, n_anim_frames, endpoint=False)

valid_thetas = []
for th in thetas:
    pts = env._compute_mechanism_positions(goal_state.params, th)
    if pts is not None:
        valid_thetas.append(th)

mech_range = max(6.0, d + 3.0)
cx_mech = d / 2.0

frames2 = []
trace_x, trace_y = [], []

for fi, theta in enumerate(valid_thetas):
    pts = env._compute_mechanism_positions(goal_state.params, theta)
    o1, o2, a_pt, b_pt, p_pt = pts['O1'], pts['O2'], pts['A'], pts['B'], pts['P']
    trace_x.append(p_pt[0])
    trace_y.append(p_pt[1])

    fig, ax = plt.subplots(figsize=(7, 7))
    fig.set_facecolor(BLACK_10)
    ax.set_facecolor("white")
    ax.set_xlim(cx_mech - mech_range, cx_mech + mech_range)
    ax.set_ylim(-mech_range, mech_range)
    ax.set_aspect("equal")
    for spine in ax.spines.values():
        spine.set_color(BLACK_30)
    ax.tick_params(colors=BLACK_90, labelsize=7)

    if len(trail_x) > 1:
        tx_c = np.append(trail_x, trail_x[0])
        ty_c = np.append(trail_y, trail_y[0])
        ax.plot(tx_c, ty_c, '-', color=ATLANTIC, alpha=0.2,
                linewidth=1.0, zorder=1)

    if len(trace_x) > 1:
        ax.plot(trace_x, trace_y, '-', color=ROSE, linewidth=2.0,
                alpha=0.7, zorder=2)

    ax.plot([o1[0], a_pt[0]], [o1[1], a_pt[1]],
            '-', color=GARNET, linewidth=3.5, zorder=4)
    ax.plot([a_pt[0], b_pt[0]], [a_pt[1], b_pt[1]],
            '-', color=ATLANTIC, linewidth=3.5, zorder=4)
    ax.plot([o2[0], b_pt[0]], [o2[1], b_pt[1]],
            '-', color=HORSESHOE, linewidth=3.5, zorder=4)
    ax.plot([o1[0], o2[0]], [o1[1], o2[1]],
            '-', color=CONGAREE, linewidth=4.5, zorder=3)

    ax.plot([a_pt[0], p_pt[0]], [a_pt[1], p_pt[1]],
            '--', color=ATLANTIC, alpha=0.5, linewidth=1.2, zorder=4)

    for jx, jy in [o1, o2, a_pt, b_pt]:
        ax.plot(jx, jy, 'o', color=BLACK_90, markersize=6, zorder=6)

    ax.plot(p_pt[0], p_pt[1], 'D', color=ROSE, markersize=8, zorder=7)

    ax.set_title("Four-Bar Linkage Motion", fontsize=13,
                 color=BLACK_90, pad=10, fontweight="bold")

    angle_deg = np.degrees(theta) % 360
    fig.text(0.5, 0.02,
             f"Crank angle: {angle_deg:.0f}°",
             ha="center", va="bottom", fontsize=10, color=BLACK_90)

    img = fig_to_pil(fig)
    plt.close(fig)
    frames2.append(img)

frames2[0].save(
    f"{OUT}/linkage_motion.gif",
    save_all=True, append_images=frames2[1:],
    duration=80, loop=0, optimize=True,
)
print(f"  Saved linkage_motion.gif ({len(frames2)} frames)")
print("Done!")
