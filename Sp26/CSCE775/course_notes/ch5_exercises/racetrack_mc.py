"""
Exercise 5.12 — Racetrack (Monte Carlo Control)

Implements a racetrack gridworld where a car navigates around a right turn,
controlled by on-policy first-visit MC control (epsilon-soft) to find the
optimal policy.

Environment per Sutton & Barto:
  - State: (row, col, vr, vc) — position + velocity (both discrete)
  - vr in [0,4] = upward velocity (row decreases), vc in [0,4] = rightward
  - Position update: row -= vr, col += vc
  - Actions: 9 possible = {-1, 0, +1} x {-1, 0, +1} for velocity increments
  - Constraint: vr and vc cannot both be zero (except at start)
  - Noise: probability 0.1 that both increments are zero
  - Reward: -1 per step
  - Boundary crossing -> reset to random start, velocity (0,0)
  - Finish line crossing -> episode ends
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time

# Brand colors
GARNET = "#73000A"
BLACK90 = "#363636"
BLACK70 = "#5C5C5C"
BLACK50 = "#A2A2A2"
BLACK30 = "#C7C7C7"
BLACK10 = "#ECECEC"
ATLANTIC = "#466A9F"
CONGAREE = "#1F414D"
HORSESHOE = "#65780B"
ROSE = "#CC2E40"
HONEYCOMB = "#A49137"
GRASS = "#CED318"

# Action encoding: index -> (d_vr, d_vc)
# vr = upward velocity, vc = rightward velocity
ACTIONS = [(-1, -1), (-1, 0), (-1, 1),
           ( 0, -1), ( 0, 0), ( 0, 1),
           ( 1, -1), ( 1, 0), ( 1, 1)]

NUM_ACTIONS = 9
MAX_VEL = 4
NOISE_PROB = 0.1


def build_track():
    """Build the larger right-turn racetrack from Figure 5.5.

    Row 0 is TOP. Car starts at bottom, drives upward, then turns right.
    Cell codes: 0 = wall, 1 = track, 2 = start, 3 = finish
    """
    rows, cols = 32, 17
    track = np.zeros((rows, cols), dtype=np.int8)

    # (left_col, right_col) for each row, top to bottom
    track_def = {
        0:  (3, 9),
        1:  (2, 9),
        2:  (2, 9),
        3:  (1, 9),
        4:  (0, 9),
        5:  (0, 9),
        6:  (0, 9),
        7:  (0, 9),
        8:  (0, 9),
        9:  (0, 9),
        10: (0, 9),
        11: (0, 9),
        12: (0, 9),
        13: (0, 9),
        14: (0, 10),
        15: (0, 11),
        16: (0, 12),
        17: (0, 13),
        18: (0, 14),
        19: (0, 15),
        20: (0, 16),
        21: (0, 16),
        22: (0, 16),
        23: (1, 16),
        24: (1, 16),
        25: (1, 16),
        26: (1, 16),
        27: (1, 16),
        28: (2, 16),
        29: (2, 16),
        30: (2, 16),
        31: (3, 16),
    }

    for r in range(rows):
        c_start, c_end = track_def[r]
        track[r, c_start:c_end+1] = 1

    # Start line: bottom row
    for c in range(cols):
        if track[rows-1, c] == 1:
            track[rows-1, c] = 2

    # Finish line: right edge of the upper portion (column 9, rows 0-8)
    for r in range(9):
        track[r, 9] = 3

    return track


class Racetrack:
    def __init__(self, track):
        self.track = track
        self.rows, self.cols = track.shape
        self.start_cells = list(zip(*np.where(track == 2)))
        self.finish_cells = set(zip(*np.where(track == 3)))
        self.reset()

    def reset(self):
        idx = np.random.randint(len(self.start_cells))
        self.row, self.col = self.start_cells[idx]
        self.vr = 0  # upward velocity [0..4]
        self.vc = 0  # rightward velocity [0..4]
        return self._state()

    def _state(self):
        return (int(self.row), int(self.col), int(self.vr), int(self.vc))

    def _on_track(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.track[r, c] != 0
        return False

    def _check_path(self, r0, c0, r1, c1):
        """Walk path from (r0,c0) to (r1,c1). Return (crossed_finish, left_track)."""
        dr = r1 - r0
        dc = c1 - c0
        steps = max(abs(dr), abs(dc), 1)
        crossed_finish = False
        left_track = False
        for i in range(1, steps + 1):
            t = i / steps
            r = int(round(r0 + t * dr))
            c = int(round(c0 + t * dc))
            if (r, c) in self.finish_cells:
                crossed_finish = True
                return crossed_finish, False
            if not self._on_track(r, c):
                left_track = True
                return False, left_track
        return crossed_finish, left_track

    def step(self, action_idx, noise=True):
        """Take an action. Returns (next_state, reward, done)."""
        dvr, dvc = ACTIONS[action_idx]

        # Apply noise
        if noise and np.random.random() < NOISE_PROB:
            dvr, dvc = 0, 0

        # Update velocity: both components in [0, MAX_VEL]
        new_vr = int(np.clip(self.vr + dvr, 0, MAX_VEL))
        new_vc = int(np.clip(self.vc + dvc, 0, MAX_VEL))

        # Cannot both be zero (revert to old if so, unless at rest)
        if new_vr == 0 and new_vc == 0:
            if self.vr != 0 or self.vc != 0:
                new_vr, new_vc = self.vr, self.vc
            else:
                return self._state(), -1, False

        self.vr, self.vc = new_vr, new_vc

        # Position update: upward = row decreases, rightward = col increases
        new_r = self.row - self.vr
        new_c = self.col + self.vc

        crossed_finish, left_track = self._check_path(
            self.row, self.col, new_r, new_c)

        if crossed_finish:
            return self._state(), -1, True

        if left_track:
            self.reset()
            return self._state(), -1, False

        self.row, self.col = new_r, new_c
        return self._state(), -1, False


def run_mc_control(track, num_episodes=500_000, epsilon=0.1, episode_cap=1000):
    """On-policy first-visit MC control with epsilon-soft policy."""
    env = Racetrack(track)
    rows, cols = track.shape

    # Q[row, col, vr, vc, action] — vr and vc in [0, MAX_VEL]
    Q = np.full((rows, cols, MAX_VEL+1, MAX_VEL+1, NUM_ACTIONS), -100.0)
    returns_count = np.zeros_like(Q)
    episode_lengths = np.zeros(num_episodes)

    t_start = time.time()

    for ep in range(num_episodes):
        state = env.reset()
        episode = []

        for t in range(episode_cap):
            r, c, vr, vc = state

            if np.random.random() < epsilon:
                action = np.random.randint(NUM_ACTIONS)
            else:
                action = int(np.argmax(Q[r, c, vr, vc, :]))

            next_state, reward, done = env.step(action)
            episode.append((state, action, reward))

            if done:
                break
            state = next_state

        episode_lengths[ep] = len(episode)

        # First-visit MC update
        G = 0.0
        visited = set()
        for t in range(len(episode) - 1, -1, -1):
            state_t, action_t, reward_t = episode[t]
            G += reward_t

            r, c, vr, vc = state_t
            sa_key = (r, c, vr, vc, action_t)

            if sa_key not in visited:
                visited.add(sa_key)
                returns_count[r, c, vr, vc, action_t] += 1
                n = returns_count[r, c, vr, vc, action_t]
                Q[r, c, vr, vc, action_t] += (G - Q[r, c, vr, vc, action_t]) / n

        if (ep + 1) % 50_000 == 0:
            elapsed = time.time() - t_start
            avg_len = np.mean(episode_lengths[max(0, ep-999):ep+1])
            print(f"Episode {ep+1:>7d}/{num_episodes}  "
                  f"avg length (last 1k): {avg_len:.1f}  "
                  f"time: {elapsed:.1f}s")

    return Q, episode_lengths


def run_greedy_episode(env, Q, max_steps=200):
    """Run a single episode using greedy policy (no noise)."""
    state = env.reset()
    trajectory = [state]

    for _ in range(max_steps):
        r, c, vr, vc = state
        action = int(np.argmax(Q[r, c, vr, vc, :]))
        next_state, reward, done = env.step(action, noise=False)
        trajectory.append(next_state)
        if done:
            break
        state = next_state

    return trajectory


def run_greedy_from(env, Q, start_row, start_col, max_steps=200):
    """Run a greedy episode from a specific starting position."""
    env.row = start_row
    env.col = start_col
    env.vr = 0
    env.vc = 0
    state = env._state()
    trajectory = [state]

    for _ in range(max_steps):
        r, c, vr, vc = state
        action = int(np.argmax(Q[r, c, vr, vc, :]))
        next_state, reward, done = env.step(action, noise=False)
        trajectory.append(next_state)
        if done:
            break
        state = next_state

    return trajectory


def _draw_track(ax, track):
    """Draw the track grid on a matplotlib axes."""
    rows, cols = track.shape
    for r in range(rows):
        for c in range(cols):
            if track[r, c] == 0:
                color = BLACK90
            elif track[r, c] == 2:
                color = GARNET
            elif track[r, c] == 3:
                color = HORSESHOE
            else:
                color = BLACK10
            rect = plt.Rectangle((c, rows - 1 - r), 1, 1,
                                 facecolor=color, edgecolor=BLACK50,
                                 linewidth=0.5)
            ax.add_patch(rect)
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect("equal")


def plot_track_with_policy(track, Q, filename="racetrack_policy.png"):
    """Plot the track with arrows showing greedy policy at vel=(0,0)."""
    rows, cols = track.shape
    fig, ax = plt.subplots(figsize=(8, 14))
    _draw_track(ax, track)

    # Arrows for policy from rest (vr=0, vc=0) on track and start cells
    for r in range(rows):
        for c in range(cols):
            if track[r, c] in (1, 2):
                action = int(np.argmax(Q[r, c, 0, 0, :]))
                dvr, dvc = ACTIONS[action]
                if dvr != 0 or dvc != 0:
                    # dvr>0 = increase upward vel -> arrow up; dvc>0 -> arrow right
                    ax.annotate("",
                                xy=(c + 0.5 + dvc * 0.3,
                                    rows - 1 - r + 0.5 + dvr * 0.3),
                                xytext=(c + 0.5, rows - 1 - r + 0.5),
                                arrowprops=dict(arrowstyle="->", color=CONGAREE,
                                                lw=1.5))

    ax.set_xlabel("Column", fontsize=11, color=BLACK90)
    ax.set_ylabel("Row (bottom = start)", fontsize=11, color=BLACK90)
    ax.set_title("Racetrack with Greedy Policy (from rest)", fontsize=13,
                 color=GARNET, fontweight="bold")

    legend_elements = [
        mpatches.Patch(facecolor=BLACK10, edgecolor=BLACK50, label="Track"),
        mpatches.Patch(facecolor=GARNET, edgecolor=BLACK50, label="Start"),
        mpatches.Patch(facecolor=HORSESHOE, edgecolor=BLACK50, label="Finish"),
        mpatches.Patch(facecolor=BLACK90, edgecolor=BLACK50, label="Wall"),
    ]
    ax.legend(handles=legend_elements, loc="upper left", fontsize=9)

    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved {filename}")


def plot_trajectories(track, Q, filename="racetrack_trajectories.png"):
    """Plot sample greedy trajectories on the track."""
    rows, cols = track.shape
    env = Racetrack(track)
    fig, ax = plt.subplots(figsize=(8, 14))
    _draw_track(ax, track)

    traj_colors = [ATLANTIC, CONGAREE, ROSE, HONEYCOMB, GRASS]
    start_cells = env.start_cells

    # Only use start columns that can actually reach the finish
    # (finish is at column 9; car can only move right, so col <= 9 is needed)
    reachable = [(r, c) for r, c in start_cells if c <= 9]
    if not reachable:
        reachable = start_cells
    n_traj = min(5, len(reachable))
    indices = np.linspace(0, len(reachable) - 1, n_traj, dtype=int)
    # Override start_cells for the loop below
    start_cells = reachable

    for i, idx in enumerate(indices):
        sr, sc = start_cells[idx]
        traj = run_greedy_from(env, Q, sr, sc)
        color = traj_colors[i % len(traj_colors)]

        xs = [s[1] + 0.5 for s in traj]
        ys = [rows - 1 - s[0] + 0.5 for s in traj]

        ax.plot(xs, ys, '-o', color=color, markersize=3, linewidth=2,
                label=f"Start col {sc}, {len(traj)-1} steps", alpha=0.85)

    ax.set_xlabel("Column", fontsize=11, color=BLACK90)
    ax.set_ylabel("Row (bottom = start)", fontsize=11, color=BLACK90)
    ax.set_title("Sample Greedy Trajectories (no noise)", fontsize=13,
                 color=GARNET, fontweight="bold")
    ax.legend(loc="upper left", fontsize=8)

    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved {filename}")


def plot_learning_curve(episode_lengths, filename="racetrack_learning.png"):
    """Plot episode length vs episode number, smoothed."""
    fig, ax = plt.subplots(figsize=(10, 5))

    window = 5000
    smoothed = np.convolve(episode_lengths, np.ones(window)/window, mode='valid')

    ax.plot(np.arange(len(smoothed)) + window // 2, smoothed,
            color=GARNET, linewidth=1.5)
    ax.set_xlabel("Episode", fontsize=11, color=BLACK90)
    ax.set_ylabel("Episode Length (steps)", fontsize=11, color=BLACK90)
    ax.set_title("Learning Curve — On-Policy MC Control", fontsize=13,
                 color=GARNET, fontweight="bold")
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3, color=BLACK50)
    ax.tick_params(colors=BLACK70)

    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved {filename}")


if __name__ == "__main__":
    print("Building racetrack...")
    track = build_track()
    print(f"Track shape: {track.shape}")
    print(f"Start cells: {list(zip(*np.where(track == 2)))}")
    print(f"Finish cells: {list(zip(*np.where(track == 3)))}")

    print("\nRunning on-policy MC control (500,000 episodes)...")
    Q, episode_lengths = run_mc_control(track, num_episodes=500_000, epsilon=0.1)

    print("\nGenerating visualizations...")
    plot_track_with_policy(track, Q, "racetrack_policy.png")
    plot_trajectories(track, Q, "racetrack_trajectories.png")
    plot_learning_curve(episode_lengths, "racetrack_learning.png")

    # Print summary statistics
    env = Racetrack(track)
    lengths = []
    for _ in range(100):
        traj = run_greedy_episode(env, Q)
        lengths.append(len(traj) - 1)
    print(f"\nGreedy policy (no noise): avg {np.mean(lengths):.1f} steps, "
          f"min {np.min(lengths)}, max {np.max(lengths)} over 100 episodes")

    print("Done.")
