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
    """Gridworld maze with optional small reward traps.

    rewards : {(r,c) : value}  every listed cell is terminal, so an agent
              that walks onto (2,3) gets its value and the episode ends.
    """
    def __init__(self, n: int, seed: int = 17,
                 rewards: dict | None = None,
                 big_goal_value: float = 1.5,
                 step_penalty: float = -0.01):
        self.n = n
        self.edges = generate_maze(n, seed=seed)
        self.start = (0, 0)
        self.big_goal = (n - 1, n - 1)
        self.step_penalty = step_penalty
        self.rewards: dict = dict(rewards) if rewards else {}
        self.rewards[self.big_goal] = big_goal_value
        self.terminal = set(self.rewards.keys())

    def move(self, cell, action):
        dr, dc = [(-1, 0), (1, 0), (0, -1), (0, 1)][action]
        nr, nc = cell[0] + dr, cell[1] + dc
        if not (0 <= nr < self.n and 0 <= nc < self.n):
            return cell
        if frozenset({cell, (nr, nc)}) not in self.edges:
            return cell
        return (nr, nc)

    # keep old alias for backward compat if anywhere still calls env.step
    step = move

    def bfs_path(self, src, dst):
        """Shortest path from src to dst honoring edge walls."""
        from collections import deque
        prev = {src: None}
        q = deque([src])
        while q:
            cur = q.popleft()
            if cur == dst:
                break
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nxt = (cur[0] + dr, cur[1] + dc)
                if (0 <= nxt[0] < self.n and 0 <= nxt[1] < self.n
                        and nxt not in prev
                        and frozenset({cur, nxt}) in self.edges):
                    prev[nxt] = cur
                    q.append(nxt)
        if dst not in prev:
            return []
        path = []
        cur = dst
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        return list(reversed(path))

    def bfs_distances(self, src):
        from collections import deque
        dist = {src: 0}
        q = deque([src])
        while q:
            cur = q.popleft()
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nxt = (cur[0] + dr, cur[1] + dc)
                if (0 <= nxt[0] < self.n and 0 <= nxt[1] < self.n
                        and nxt not in dist
                        and frozenset({cur, nxt}) in self.edges):
                    dist[nxt] = dist[cur] + 1
                    q.append(nxt)
        return dist


def place_small_rewards(env: Maze, n_small: int = 5,
                        min_dist: int = 3, max_dist: int = 10,
                        value: float = 0.3, seed: int = 42):
    """Pick `n_small` cells near the start, off the shortest path to the goal,
    and verify the big goal is still reachable without stepping on them.
    Returns the reward dict."""
    rng = random.Random(seed)
    shortest = set(env.bfs_path(env.start, env.big_goal))
    dist = env.bfs_distances(env.start)
    candidates = [c for c, d in dist.items()
                  if min_dist <= d <= max_dist
                  and c not in shortest
                  and c != env.start
                  and c != env.big_goal]
    rng.shuffle(candidates)

    chosen = []
    for c in candidates:
        # check big goal still reachable if this cell is made terminal
        trial_terminal = set(chosen) | {c}
        # BFS from start on edges, forbidding entering terminal cells except as endpoints
        from collections import deque
        seen = {env.start}
        q = deque([env.start])
        reachable_goal = False
        while q:
            cur = q.popleft()
            if cur == env.big_goal:
                reachable_goal = True
                break
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nxt = (cur[0] + dr, cur[1] + dc)
                if (0 <= nxt[0] < env.n and 0 <= nxt[1] < env.n
                        and nxt not in seen
                        and frozenset({cur, nxt}) in env.edges
                        and (nxt not in trial_terminal or nxt == env.big_goal)):
                    seen.add(nxt)
                    q.append(nxt)
        if reachable_goal:
            chosen.append(c)
        if len(chosen) >= n_small:
            break
    return {c: value for c in chosen}

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
        total_reward = 0.0
        terminal_hit = None
        for _ in range(max_steps):
            if rng.random() < eps:
                a = int(rng.integers(0, 4))
            else:
                a = int(np.argmax(Q[state[0], state[1]]))
            nxt = env.move(state, a)
            if nxt in env.terminal:
                r = env.rewards[nxt]
                done = True
            else:
                r = env.step_penalty
                done = False
            target = r if done else r + gamma * np.max(Q[nxt[0], nxt[1]])
            Q[state[0], state[1], a] += alpha * (target - Q[state[0], state[1], a])
            state = nxt
            traj.append(state)
            total_reward += r
            if done:
                terminal_hit = state
                break
        history.append({"ep": ep, "traj": traj, "Q": Q.copy(),
                        "terminal_hit": terminal_hit,
                        "reached_big": terminal_hit == env.big_goal,
                        "reward": total_reward,
                        "steps": len(traj)})
    return history

# -----------------------------------------------------------------------------
# Evolutionary strategy (simple GA over deterministic action table)
# -----------------------------------------------------------------------------

def _rollout_stochastic(args):
    """Module-level helper so multiprocessing can pickle it.
    args[10] = deterministic flag (optional, default False).
    args[11] = temperature (optional, default 1.0). Lower T -> more greedy.
    """
    if len(args) == 10:
        (policy_logits, edges, n, start, big_goal, rewards_map, terminal_set,
         step_penalty, max_steps, seed) = args
        deterministic = False
        temperature = 1.0
    elif len(args) == 11:
        (policy_logits, edges, n, start, big_goal, rewards_map, terminal_set,
         step_penalty, max_steps, seed, deterministic) = args
        temperature = 1.0
    else:
        (policy_logits, edges, n, start, big_goal, rewards_map, terminal_set,
         step_penalty, max_steps, seed, deterministic, temperature) = args
    rng = np.random.default_rng(seed)
    state = start
    traj = [state]
    total_reward = 0.0
    terminal_hit = None
    min_dist_big = abs(state[0] - big_goal[0]) + abs(state[1] - big_goal[1])
    farthest_cell = state
    farthest_dist = 0
    visited = {state}
    for _ in range(max_steps):
        logits = policy_logits[state[0], state[1]]
        if deterministic:
            a = int(np.argmax(logits))
        else:
            scaled = logits / max(temperature, 1e-6)
            probs = np.exp(scaled - scaled.max())
            probs /= probs.sum()
            a = int(rng.choice(4, p=probs))
        dr, dc = [(-1, 0), (1, 0), (0, -1), (0, 1)][a]
        nr, nc = state[0] + dr, state[1] + dc
        if 0 <= nr < n and 0 <= nc < n and frozenset({state, (nr, nc)}) in edges:
            state = (nr, nc)
        traj.append(state)
        visited.add(state)
        d = abs(state[0] - big_goal[0]) + abs(state[1] - big_goal[1])
        if d < min_dist_big:
            min_dist_big = d
        # track farthest Manhattan distance from start
        ds = abs(state[0] - start[0]) + abs(state[1] - start[1])
        if ds > farthest_dist:
            farthest_dist = ds
            farthest_cell = state
        if state in terminal_set:
            total_reward += rewards_map[state]
            terminal_hit = state
            break
        else:
            total_reward += step_penalty
    reached_big = terminal_hit == big_goal
    max_d = 2 * (n - 1)
    progress = 1.0 - min_dist_big / max_d
    coverage = len(visited) / (n * n)
    fit = total_reward + 2.5 * progress + 0.5 * coverage
    if reached_big:
        fit += 5.0
    return fit, traj, reached_big, terminal_hit, farthest_cell


def train_map_elites(env: Maze, n_gen: int = 300, pop_size: int = 80,
                     max_steps: int = 800,
                     sigma_start: float = 0.65, sigma_end: float = 0.12,
                     bucket: int = 4, temperature: float = 1.0,
                     k_evals: int = 2, seed: int = 1,
                     n_workers: int | None = None):
    """MAP-Elites over terminal-cell buckets. Stochastic logit policies."""
    rng = np.random.default_rng(seed)
    shape = (env.n, env.n, 4)

    if n_workers is None:
        n_workers = min(pop_size, max(1, (os.cpu_count() or 2) - 1))
    pool = mp.Pool(processes=n_workers) if n_workers > 1 else None

    def niche(farthest_cell):
        return (farthest_cell[0] // bucket, farthest_cell[1] // bucket)

    def eval_batch(policies):
        """Evaluate each policy k_evals times, return the best-fitness result per policy."""
        best = [None] * len(policies)
        for k in range(k_evals):
            seeds = rng.integers(0, 2**31 - 1, size=len(policies))
            args = [(policies[i], env.edges, env.n, env.start, env.big_goal,
                     env.rewards, env.terminal, env.step_penalty,
                     max_steps, int(seeds[i]), False, temperature)
                    for i in range(len(policies))]
            results = pool.map(_rollout_stochastic, args) if pool else \
                      [_rollout_stochastic(a) for a in args]
            for i, r in enumerate(results):
                if best[i] is None or r[0] > best[i][0]:
                    best[i] = r
        return best

    # Seed archive
    archive: dict = {}
    init_pop = [rng.normal(0.0, 0.8, shape) for _ in range(pop_size)]
    res = eval_batch(init_pop)
    for pol, (fit, traj, r_big, term, far) in zip(init_pop, res):
        k = niche(far)
        if k not in archive or archive[k]["fit"] < fit:
            archive[k] = {"fit": fit, "pol": pol, "traj": traj,
                          "term": term, "reached_big": r_big}

    history = []
    try:
        for g in range(n_gen):
            sigma = sigma_start + (sigma_end - sigma_start) * (g / max(1, n_gen - 1))
            keys = list(archive.keys())
            parents = [archive[keys[int(rng.integers(0, len(keys)))]]["pol"]
                       for _ in range(pop_size)]
            children = [p + rng.normal(0.0, sigma, p.shape) for p in parents]
            res = eval_batch(children)
            fits = np.array([r[0] for r in res])
            trajs = [r[1] for r in res]
            reached_big = [r[2] for r in res]
            terminals = [r[3] for r in res]
            farthest = [r[4] for r in res]
            for pol, (fit, traj, r_big, term, far) in zip(children, res):
                k = niche(far)
                if k not in archive or archive[k]["fit"] < fit:
                    archive[k] = {"fit": fit, "pol": pol, "traj": traj,
                                  "term": term, "reached_big": r_big}
            best_idx = int(np.argmax(fits))
            history.append({"gen": g, "fits": fits.copy(), "trajs": trajs,
                            "best_idx": best_idx,
                            "reached_big": reached_big,
                            "terminals": terminals,
                            "farthest": farthest,
                            "archive_size": len(archive)})
    finally:
        if pool is not None:
            pool.close()
            pool.join()
    return history


def train_es(env: Maze, n_gen: int = 500, pop_size: int = 80,
             max_steps: int = 800, sigma_start: float = 0.55,
             sigma_end: float = 0.12,
             elite: int = 6, seed: int = 1, n_workers: int | None = None):
    """Stochastic-policy ES with Gaussian mutation, uniform crossover,
    and an annealing mutation sigma."""
    rng = np.random.default_rng(seed)
    shape = (env.n, env.n, 4)
    population = [rng.normal(0.0, 0.8, shape) for _ in range(pop_size)]
    history = []

    if n_workers is None:
        n_workers = min(pop_size, max(1, (os.cpu_count() or 2) - 1))
    pool = mp.Pool(processes=n_workers) if n_workers > 1 else None
    try:
        for g in range(n_gen):
            sigma = sigma_start + (sigma_end - sigma_start) * (g / max(1, n_gen - 1))
            seeds = rng.integers(0, 2**31 - 1, size=pop_size)
            args = [(population[i], env.edges, env.n, env.start, env.big_goal,
                     env.rewards, env.terminal, env.step_penalty,
                     max_steps, int(seeds[i])) for i in range(pop_size)]
            results = pool.map(_rollout_stochastic, args) if pool else \
                      [_rollout_stochastic(a) for a in args]
            fits = np.array([r[0] for r in results])
            trajs = [r[1] for r in results]
            reached_big = [r[2] for r in results]
            terminals = [r[3] for r in results]
            order = np.argsort(fits)[::-1]
            best_idx = int(order[0])
            history.append({"gen": g, "fits": fits.copy(), "trajs": trajs,
                            "best_idx": best_idx,
                            "reached_big": reached_big,
                            "terminals": terminals})
            # (farthest cell returned but not tracked here — MAP-Elites uses it)
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

    # small reward cells (yellow/Grass)
    for (r, c), v in env.rewards.items():
        if (r, c) == env.big_goal:
            continue
        ax.add_patch(patches.Rectangle((c + 0.05, r + 0.05), 0.9, 0.9,
                                       facecolor=HONEYCOMB, edgecolor="none", zorder=5))
        ax.text(c + 0.5, r + 0.5, f"+{v:.1f}", color="white",
                ha="center", va="center",
                fontsize=max(7, 160 // n), fontweight="bold", zorder=6)

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

        hit = rl.get("terminal_hit")
        if hit == env.big_goal:
            hit_txt = "reached BIG goal"
            hit_color = GARNET
        elif hit is not None:
            hit_txt = f"stuck on +{env.rewards[hit]:.1f} trap"
            hit_color = HONEYCOMB
        else:
            hit_txt = "timed out"
            hit_color = "#1f1f1f"
        ax_rl.set_title(
            f"RL  ·  Q-learning\n"
            f"Episode {rl['ep']+1:>3d} / {len(rl_hist)}   ·   "
            f"{rl['steps']:>4d} steps   ·   ",
            fontsize=14, pad=10, color="#1f1f1f", loc="left")
        ax_rl.text(0.5, 1.03, hit_txt, transform=ax_rl.transAxes,
                   ha="center", va="bottom", fontsize=13,
                   color=hit_color, fontweight="bold")

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
        reached_count = sum(1 for r in es.get("reached_big", []) if r)
        subtitle_color = GARNET if reached_count > 0 else HONEYCOMB
        subtitle = (f"{reached_count}/{len(es['trajs'])} reached BIG goal"
                    if reached_count > 0 else "all stuck on traps")
        arch = es.get("archive_size", len(es['trajs']))
        ax_es.set_title(
            f"ES  ·  MAP-Elites  (pop = {len(es['trajs'])}, archive = {arch})\n"
            f"Generation {es['gen']+1:>2d} / {len(es_hist)}   ·   "
            f"best fitness {best_fit:.3f}   ·   ",
            fontsize=14, pad=10, color="#1f1f1f", loc="left")
        ax_es.text(0.5, 1.03, subtitle, transform=ax_es.transAxes,
                   ha="center", va="bottom", fontsize=13,
                   color=subtitle_color, fontweight="bold")

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
    tag = "traps_20x20"

    # Build maze and place trap rewards
    base_env = Maze(N, seed=17)  # temp to get geometry for placement
    traps = place_small_rewards(base_env, n_small=2, min_dist=5, max_dist=10,
                                value=0.3, seed=42)
    env = Maze(N, seed=17, rewards=traps, big_goal_value=4.0,
               step_penalty=-0.005)
    print(f"placed {len(traps)} trap cells:")
    for cell, val in traps.items():
        print(f"  {cell} = +{val}")
    print(f"big goal at {env.big_goal} = +{env.rewards[env.big_goal]}")

    cache = here / f"rl_es_hist_{tag}.pkl"

    if "--render-only" in sys.argv and cache.exists():
        print(f"loading cache {cache}")
        with open(cache, "rb") as f:
            data = pickle.load(f)
        rl_hist = data["rl"]
        es_hist = data["es"]
        out_mp4 = here / f"rl_vs_es_{tag}.mp4"
        out_gif = here / f"rl_vs_es_{tag}.gif"
        build_animation(env, rl_hist, es_hist, out_mp4, out_gif,
                        n_frames=180, fps=15)
        print("render-only done.")
        return

    t0 = time.time()
    print(f"training RL on {N}×{N} trap maze …")
    rl_hist = train_rl(env, n_episodes=2000, max_steps=1200, seed=0)
    big = sum(1 for h in rl_hist[-200:] if h["reached_big"])
    print(f"  RL done in {time.time()-t0:5.1f}s · last-200 episodes reached BIG = {big}/200")

    t1 = time.time()
    print("training ES / MAP-Elites (pop=100, gen=1000, bucket=4, k=2) …")
    es_hist = train_map_elites(env, n_gen=1000, pop_size=100, max_steps=800,
                               bucket=4, temperature=1.0, k_evals=2,
                               sigma_start=0.85, sigma_end=0.18, seed=2)
    big_per_gen = [sum(r for r in h["reached_big"]) for h in es_hist]
    first_big = next((i for i, n in enumerate(big_per_gen) if n > 0), None)
    print(f"  ES done in {time.time()-t1:5.1f}s · last-gen BIG reach = {big_per_gen[-1]}/80"
          f" · first BIG at gen {first_big}"
          f" · archive size = {es_hist[-1]['archive_size']}")

    cache_out = here / f"rl_es_hist_{tag}.pkl"
    with open(cache_out, "wb") as f:
        pickle.dump({"rl": rl_hist, "es": es_hist,
                     "edges": env.edges, "n": N, "rewards": traps}, f)
    print(f"cached histories -> {cache_out}")

    out_mp4 = here / f"rl_vs_es_{tag}.mp4"
    out_gif = here / f"rl_vs_es_{tag}.gif"
    build_animation(env, rl_hist, es_hist, out_mp4, out_gif,
                    n_frames=180, fps=15)
    print(f"all done in {time.time()-t0:5.1f}s total.")


if __name__ == "__main__":
    main()
