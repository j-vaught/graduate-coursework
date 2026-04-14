"""Side-by-side animation of RL (Q-learning) vs. ES (GA) solving the same maze.

Left panel  : Q-learning with epsilon-greedy. Visualises the current
              episode's trajectory over a heatmap of max_a Q(s,a).
Right panel : Simple generational GA over a deterministic action table.
              Visualises trajectories of the whole population each
              generation, with the fittest member highlighted.

Outputs: rl_vs_es_<N>x<N>.mp4  and  .gif

Run:  python3 rl_vs_es_maze.py
"""
from __future__ import annotations

import multiprocessing as mp
import os
import pickle
import random
import time
from pathlib import Path

import matplotlib.animation as animation
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

# Brand palette
GARNET = "#73000A"
ATLANTIC = "#466A9F"
HORSESHOE = "#65780B"
HONEYCOMB = "#A49137"
WALL = "#363636"
BG = "#ECECEC"
GRID = "#FFFFFF"

# -----------------------------------------------------------------------------
# Maze generation
# -----------------------------------------------------------------------------

def generate_maze(n: int, seed: int = 17, extra_openings: float = 0.12):
    rng = random.Random(seed)
    edges: set[frozenset] = set()
    visited = {(0, 0)}
    stack = [(0, 0)]
    while stack:
        r, c = stack[-1]
        neigh = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited:
                neigh.append((nr, nc))
        if neigh:
            nr, nc = rng.choice(neigh)
            edges.add(frozenset({(r, c), (nr, nc)}))
            visited.add((nr, nc))
            stack.append((nr, nc))
        else:
            stack.pop()
    # extra openings -> loops
    all_adj = set()
    for r in range(n):
        for c in range(n):
            for dr, dc in [(1, 0), (0, 1)]:
                nr, nc = r + dr, c + dc
                if nr < n and nc < n:
                    all_adj.add(frozenset({(r, c), (nr, nc)}))
    walls = list(all_adj - edges)
    rng.shuffle(walls)
    for e in walls[: int(len(walls) * extra_openings)]:
        edges.add(e)
    return edges

# -----------------------------------------------------------------------------
# Env
# -----------------------------------------------------------------------------

class Maze:
    def __init__(self, n: int, seed: int = 17):
        self.n = n
        self.edges = generate_maze(n, seed=seed)
        self.start = (0, 0)
        self.goal = (n - 1, n - 1)

    def step(self, cell, action):
        dr, dc = [(-1, 0), (1, 0), (0, -1), (0, 1)][action]
        nr, nc = cell[0] + dr, cell[1] + dc
        if not (0 <= nr < self.n and 0 <= nc < self.n):
            return cell
        if frozenset({cell, (nr, nc)}) not in self.edges:
            return cell
        return (nr, nc)

# -----------------------------------------------------------------------------
# Q-learning
# -----------------------------------------------------------------------------

def train_rl(env: Maze, n_episodes: int = 2000, max_steps: int = 1200,
             alpha: float = 0.3, gamma: float = 0.95, seed: int = 0):
    rng = np.random.default_rng(seed)
    Q = np.zeros((env.n, env.n, 4))
    history = []
    for ep in range(n_episodes):
        eps = max(0.05, 1.0 - ep / 200)
        state = env.start
        traj = [state]
        for _ in range(max_steps):
            if rng.random() < eps:
                a = int(rng.integers(0, 4))
            else:
                a = int(np.argmax(Q[state[0], state[1]]))
            nxt = env.step(state, a)
            r = 1.0 if nxt == env.goal else -0.01
            Q[state[0], state[1], a] += alpha * (
                r + gamma * np.max(Q[nxt[0], nxt[1]]) - Q[state[0], state[1], a]
            )
            state = nxt
            traj.append(state)
            if state == env.goal:
                break
        history.append({"ep": ep, "traj": traj, "Q": Q.copy(),
                        "reached": state == env.goal, "steps": len(traj)})
    return history

# -----------------------------------------------------------------------------
# Evolutionary strategy (simple GA over deterministic action table)
# -----------------------------------------------------------------------------

def _rollout_stochastic(args):
    """Module-level helper so multiprocessing can pickle it."""
    policy_logits, edges, n, start, goal, max_steps, seed = args
    rng = np.random.default_rng(seed)
    state = start
    traj = [state]
    min_dist = abs(state[0] - goal[0]) + abs(state[1] - goal[1])
    for _ in range(max_steps):
        logits = policy_logits[state[0], state[1]]
        probs = np.exp(logits - logits.max())
        probs /= probs.sum()
        a = int(rng.choice(4, p=probs))
        dr, dc = [(-1, 0), (1, 0), (0, -1), (0, 1)][a]
        nr, nc = state[0] + dr, state[1] + dc
        if 0 <= nr < n and 0 <= nc < n and frozenset({state, (nr, nc)}) in edges:
            state = (nr, nc)
        traj.append(state)
        d = abs(state[0] - goal[0]) + abs(state[1] - goal[1])
        if d < min_dist:
            min_dist = d
        if state == goal:
            break
    reached = state == goal
    max_dist = 2 * (n - 1)
    progress = 1.0 - min_dist / max_dist
    fit = progress + (1.5 * (1.0 - len(traj) / max_steps) if reached else 0.0)
    return fit, traj, reached


def train_es(env: Maze, n_gen: int = 300, pop_size: int = 40,
             max_steps: int = 1200, sigma: float = 0.35,
             elite: int = 4, seed: int = 1, n_workers: int | None = None):
    """Stochastic-policy ES with Gaussian mutation and uniform crossover."""
    rng = np.random.default_rng(seed)
    shape = (env.n, env.n, 4)
    population = [rng.normal(0.0, 0.8, shape) for _ in range(pop_size)]
    history = []

    if n_workers is None:
        n_workers = min(pop_size, max(1, (os.cpu_count() or 2) - 1))
    pool = mp.Pool(processes=n_workers) if n_workers > 1 else None
    try:
        for g in range(n_gen):
            seeds = rng.integers(0, 2**31 - 1, size=pop_size)
            args = [(population[i], env.edges, env.n, env.start, env.goal,
                     max_steps, int(seeds[i])) for i in range(pop_size)]
            results = pool.map(_rollout_stochastic, args) if pool else \
                      [_rollout_stochastic(a) for a in args]
            fits = np.array([r[0] for r in results])
            trajs = [r[1] for r in results]
            order = np.argsort(fits)[::-1]
            best_idx = int(order[0])
            history.append({"gen": g, "fits": fits.copy(), "trajs": trajs,
                            "best_idx": best_idx})
            # Next generation: elites + crossover + mutation
            elites = [population[i].copy() for i in order[:elite]]
            new_pop = [e.copy() for e in elites]
            while len(new_pop) < pop_size:
                p1 = elites[int(rng.integers(0, elite))]
                p2 = elites[int(rng.integers(0, elite))]
                mask = rng.random(p1.shape) < 0.5
                child = np.where(mask, p1, p2).copy()
                child += rng.normal(0.0, sigma, child.shape)
                new_pop.append(child)
            population = new_pop
    finally:
        if pool is not None:
            pool.close()
            pool.join()
    return history

# -----------------------------------------------------------------------------
# Rendering helpers
# -----------------------------------------------------------------------------

def draw_maze_skeleton(ax, env: Maze):
    n = env.n
    ax.set_xlim(-0.25, n + 0.25)
    ax.set_ylim(-0.25, n + 0.25)
    ax.set_aspect("equal")
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    ax.add_patch(patches.Rectangle((0, 0), n, n, facecolor=BG, edgecolor="none", zorder=0))
    for i in range(n + 1):
        ax.plot([i, i], [0, n], color=GRID, lw=0.6, zorder=1)
        ax.plot([0, n], [i, i], color=GRID, lw=0.6, zorder=1)

    lw_outer = max(2.2, 34 / n)
    ax.plot([0, n, n, 0, 0], [0, 0, n, n, 0], color=WALL, lw=lw_outer, zorder=4)

    lw = max(1.6, 30 / n)
    for r in range(n):
        for c in range(n):
            if c + 1 < n and frozenset({(r, c), (r, c + 1)}) not in env.edges:
                ax.plot([c + 1, c + 1], [r, r + 1], color=WALL, lw=lw, zorder=4)
            if r + 1 < n and frozenset({(r, c), (r + 1, c)}) not in env.edges:
                ax.plot([c, c + 1], [r + 1, r + 1], color=WALL, lw=lw, zorder=4)

    ax.add_patch(patches.Rectangle((0.05, 0.05), 0.9, 0.9,
                                   facecolor=ATLANTIC, edgecolor="none", zorder=5))
    ax.text(0.5, 0.5, "S", color="white", ha="center", va="center",
            fontsize=max(10, 240 // n), fontweight="bold", zorder=6)
    ax.add_patch(patches.Rectangle((n - 0.95, n - 0.95), 0.9, 0.9,
                                   facecolor=GARNET, edgecolor="none", zorder=5))
    ax.text(n - 0.5, n - 0.5, "G", color="white", ha="center", va="center",
            fontsize=max(10, 240 // n), fontweight="bold", zorder=6)


def trajectory_xy(traj):
    xs = [c + 0.5 for (_, c) in traj]
    ys = [r + 0.5 for (r, _) in traj]
    return xs, ys

# -----------------------------------------------------------------------------
# Animation
# -----------------------------------------------------------------------------

def build_animation(env: Maze, rl_hist, es_hist, out_mp4: Path, out_gif: Path,
                    n_frames: int = 120, fps: int = 12):
    fig, (ax_rl, ax_es) = plt.subplots(1, 2, figsize=(20, 10), dpi=100)
    fig.patch.set_facecolor("white")

    # pre-compute dense sampling indices
    rl_idx_seq = np.linspace(0, len(rl_hist) - 1, n_frames).astype(int)
    es_idx_seq = np.linspace(0, len(es_hist) - 1, n_frames).astype(int)

    def render_frame(k):
        ax_rl.clear()
        ax_es.clear()

        # ------- RL side -------
        rl = rl_hist[int(rl_idx_seq[k])]
        Q = rl["Q"]
        V = Q.max(axis=2)
        # Normalize V for heatmap
        vmax = max(V.max(), 1e-6)
        V_n = V / vmax

        draw_maze_skeleton(ax_rl, env)
        # heatmap overlay (faded)
        for r in range(env.n):
            for c in range(env.n):
                v = V_n[r, c]
                if v > 0.01:
                    ax_rl.add_patch(patches.Rectangle(
                        (c + 0.05, r + 0.05), 0.9, 0.9,
                        facecolor=GARNET, alpha=0.45 * v,
                        edgecolor="none", zorder=2))
        # trajectory of the shown episode
        xs, ys = trajectory_xy(rl["traj"])
        ax_rl.plot(xs, ys, color=ATLANTIC, lw=1.4, alpha=0.9, zorder=7)
        ax_rl.scatter([xs[-1]], [ys[-1]], color=ATLANTIC, s=70,
                      edgecolors="white", linewidths=1.2, zorder=8)

        reached_txt = "reached" if rl["reached"] else "timed out"
        ax_rl.set_title(
            f"RL  ·  Q-learning\n"
            f"Episode {rl['ep']+1:>3d} / {len(rl_hist)}   ·   "
            f"{rl['steps']:>4d} steps   ·   {reached_txt}",
            fontsize=14, pad=10, color="#1f1f1f")

        # ------- ES side -------
        es = es_hist[int(es_idx_seq[k])]
        draw_maze_skeleton(ax_es, env)
        # all population trajectories, best in garnet
        best = es["best_idx"]
        for i, t in enumerate(es["trajs"]):
            xs, ys = trajectory_xy(t)
            if i == best:
                continue
            ax_es.plot(xs, ys, color=HONEYCOMB, lw=0.9, alpha=0.55, zorder=6)
        xs, ys = trajectory_xy(es["trajs"][best])
        ax_es.plot(xs, ys, color=GARNET, lw=2.4, alpha=0.95, zorder=8)
        ax_es.scatter([xs[-1]], [ys[-1]], color=GARNET, s=80,
                      edgecolors="white", linewidths=1.3, zorder=9)

        best_fit = float(es["fits"][best])
        ax_es.set_title(
            f"ES  ·  Population GA  (pop = {len(es['trajs'])})\n"
            f"Generation {es['gen']+1:>2d} / {len(es_hist)}   ·   "
            f"best fitness {best_fit:.3f}",
            fontsize=14, pad=10, color="#1f1f1f")

        return []

    render_frame(0)
    anim = animation.FuncAnimation(fig, render_frame, frames=n_frames,
                                   interval=1000 / fps, blit=False)

    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    print(f"writing {out_mp4} …")
    mp4_writer = animation.FFMpegWriter(
        fps=fps, codec="libx264",
        extra_args=["-pix_fmt", "yuv420p", "-crf", "20"])
    anim.save(str(out_mp4), dpi=100, writer=mp4_writer)
    print(f"writing {out_gif} …")
    gif_writer = animation.PillowWriter(fps=fps)
    anim.save(str(out_gif), writer=gif_writer)
    plt.close(fig)

# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------

def main():
    import sys
    here = Path(__file__).resolve().parent
    N = 20
    env = Maze(N, seed=17)
    cache = here / f"rl_es_hist_{N}x{N}.pkl"

    if "--render-only" in sys.argv and cache.exists():
        print(f"loading cache {cache}")
        with open(cache, "rb") as f:
            data = pickle.load(f)
        rl_hist = data["rl"]
        es_hist = data["es"]
        out_mp4 = here / f"rl_vs_es_{N}x{N}.mp4"
        out_gif = here / f"rl_vs_es_{N}x{N}.gif"
        build_animation(env, rl_hist, es_hist, out_mp4, out_gif,
                        n_frames=180, fps=15)
        print("render-only done.")
        return

    t0 = time.time()
    print(f"training RL on {N}×{N} maze …")
    rl_hist = train_rl(env, n_episodes=2000, max_steps=1200, seed=0)
    print(f"  RL done in {time.time()-t0:5.1f}s · last-episode reached="
          f"{rl_hist[-1]['reached']}, steps={rl_hist[-1]['steps']}")

    t1 = time.time()
    print("training ES (pop=40, gen=300, stochastic, parallel) …")
    es_hist = train_es(env, n_gen=300, pop_size=40, max_steps=1200, seed=1)
    best_fits = [max(h['fits']) for h in es_hist]
    print(f"  ES done in {time.time()-t1:5.1f}s · best fitness "
          f"{best_fits[0]:.3f} → {best_fits[-1]:.3f}")

    # Save histories (for later re-rendering without retraining)
    cache = here / f"rl_es_hist_{N}x{N}.pkl"
    with open(cache, "wb") as f:
        pickle.dump({"rl": rl_hist, "es": es_hist,
                     "edges": env.edges, "n": N}, f)
    print(f"cached histories -> {cache}")

    out_mp4 = here / f"rl_vs_es_{N}x{N}.mp4"
    out_gif = here / f"rl_vs_es_{N}x{N}.gif"
    build_animation(env, rl_hist, es_hist, out_mp4, out_gif,
                    n_frames=180, fps=15)
    print(f"all done in {time.time()-t0:5.1f}s total.")


if __name__ == "__main__":
    main()
