"""Side-by-side continuous-landscape demo.

Left  : Gradient descent (a ball rolling on a surface). Single trajectory,
        gets stuck on the nearest local maximum.
Right : Gaussian-ES with a shrinking covariance. Population of samples,
        mean/cov update from top-K, finds the global maximum.

Both panels show the same mixture-of-Gaussians fitness surface.

Output: rl_vs_es_landscape.mp4 + .gif (no title text; 2000x1000).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.animation as animation
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

GARNET = "#73000A"
ATLANTIC = "#466A9F"
HONEYCOMB = "#A49137"
HORSESHOE = "#65780B"
BG = "#ECECEC"

# ---------------------------------------------------------------------------
# Fitness surface (mixture of Gaussians). Global max off in the corner.
# ---------------------------------------------------------------------------

PEAKS = [
    # (cx, cy, height, sigma)
    (-2.0,  0.2, 0.85, 1.0),   # local
    ( 2.0, -1.3, 0.78, 1.0),   # local
    ( 0.0,  2.6, 0.88, 0.9),   # local (attractive from below)
    ( 3.3,  3.0, 1.60, 1.1),   # GLOBAL (high + wide but off-axis)
]


def fitness(x, y):
    f = 0.0
    for cx, cy, h, s in PEAKS:
        f = f + h * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * s ** 2))
    return f


def grad(x, y):
    gx = 0.0
    gy = 0.0
    for cx, cy, h, s in PEAKS:
        w = h * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * s ** 2))
        gx = gx + w * -(x - cx) / (s ** 2)
        gy = gy + w * -(y - cy) / (s ** 2)
    return gx, gy

# ---------------------------------------------------------------------------
# Gradient descent (ascent)
# ---------------------------------------------------------------------------

def run_gradient(start=(-0.5, -3.0), lr=0.12, steps=300):
    x, y = start
    path = [(x, y)]
    for _ in range(steps):
        gx, gy = grad(x, y)
        # small noise to avoid perfectly flat saddle stalls
        x = x + lr * gx
        y = y + lr * gy
        path.append((x, y))
    return np.array(path)

# ---------------------------------------------------------------------------
# Gaussian ES  (like simplified CMA-ES)
# ---------------------------------------------------------------------------

def run_es(n_gen=60, pop=40, elite=10,
           init_mean=(-0.5, -3.0), init_sigma=1.8,
           sigma_decay=0.97, seed=0):
    rng = np.random.default_rng(seed)
    mean = np.array(init_mean, dtype=float)
    sigma = init_sigma
    history = []  # list of {"gen","samples","mean","sigma","fits","best"}
    for g in range(n_gen):
        samples = mean + sigma * rng.standard_normal((pop, 2))
        fits = fitness(samples[:, 0], samples[:, 1])
        order = np.argsort(-fits)
        top = samples[order[:elite]]
        new_mean = top.mean(axis=0)
        # simple covariance adaptation: sigma shrinks over time
        sigma = sigma * sigma_decay
        best_idx = int(order[0])
        history.append({
            "gen": g,
            "samples": samples.copy(),
            "fits": fits.copy(),
            "mean": mean.copy(),
            "sigma": sigma,
            "best": samples[best_idx].copy(),
            "best_fit": float(fits[best_idx]),
        })
        mean = new_mean
    return history

# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def draw_surface(ax, X, Y, Z, extent):
    cmap = LinearSegmentedColormap.from_list(
        "garnet_cool",
        ["#ECECEC", "#C7C7C7", "#A2A2A2", "#5C5C5C", "#363636"],
        N=256)
    ax.imshow(Z, extent=extent, origin="lower", cmap=cmap,
              alpha=0.75, interpolation="bilinear", zorder=1)
    ax.contour(X, Y, Z, levels=12, colors="white", linewidths=0.5, alpha=0.6,
               zorder=2)
    # Mark the global peak
    gx, gy = PEAKS[-1][:2]
    ax.plot(gx, gy, marker="*", markersize=24, color=GARNET,
            markeredgecolor="white", markeredgewidth=1.6, zorder=6)
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def build_animation(grad_path, es_hist, out_mp4: Path, out_gif: Path,
                    n_frames=150, fps=15):
    # Pre-compute surface
    xs = np.linspace(-5, 5, 260)
    ys = np.linspace(-5, 5, 260)
    X, Y = np.meshgrid(xs, ys)
    Z = fitness(X, Y)
    extent = [-5, 5, -5, 5]

    fig, (ax_g, ax_e) = plt.subplots(1, 2, figsize=(20, 10), dpi=100)
    fig.patch.set_facecolor("white")

    grad_idx_seq = np.linspace(0, len(grad_path) - 1, n_frames).astype(int)
    es_idx_seq = np.linspace(0, len(es_hist) - 1, n_frames).astype(int)

    def render_frame(k):
        ax_g.clear()
        ax_e.clear()

        draw_surface(ax_g, X, Y, Z, extent)
        draw_surface(ax_e, X, Y, Z, extent)

        # --- gradient descent side ---
        gi = int(grad_idx_seq[k])
        tail = grad_path[: gi + 1]
        ax_g.plot(tail[:, 0], tail[:, 1], color=ATLANTIC, lw=2.2, alpha=0.85,
                  zorder=7)
        ax_g.scatter([tail[-1, 0]], [tail[-1, 1]], color=ATLANTIC, s=220,
                     edgecolors="white", linewidths=2, zorder=8)

        # --- ES side ---
        es = es_hist[int(es_idx_seq[k])]
        samples = es["samples"]
        ax_e.scatter(samples[:, 0], samples[:, 1],
                     color=HONEYCOMB, s=40, alpha=0.55, edgecolors="white",
                     linewidths=0.6, zorder=6)
        # covariance ellipse (circle since C = sigma^2 I)
        sigma = es["sigma"]
        mean = es["mean"]
        circle = patches.Circle(tuple(mean), radius=2 * sigma,
                                facecolor="none", edgecolor=GARNET,
                                linewidth=1.6, linestyle="--", alpha=0.85,
                                zorder=7)
        ax_e.add_patch(circle)
        # best point
        best = es["best"]
        ax_e.plot(best[0], best[1], marker="o", markersize=14, color=GARNET,
                  markeredgecolor="white", markeredgewidth=1.6, zorder=9)
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
    anim.save(str(out_gif), writer=animation.PillowWriter(fps=fps))
    plt.close(fig)


def main():
    here = Path(__file__).resolve().parent
    grad_path = run_gradient(start=(-0.5, -3.0), lr=0.12, steps=300)
    es_hist = run_es(n_gen=60, pop=40, elite=10,
                     init_mean=(-0.5, -3.0), init_sigma=1.8,
                     sigma_decay=0.965, seed=0)
    final_es = es_hist[-1]["best"]
    print(f"gradient ended at ({grad_path[-1,0]:+.2f}, {grad_path[-1,1]:+.2f})"
          f" · fitness {fitness(*grad_path[-1]):.3f}")
    print(f"ES best ended at   ({final_es[0]:+.2f}, {final_es[1]:+.2f})"
          f" · fitness {es_hist[-1]['best_fit']:.3f}")
    print(f"global peak at     ({PEAKS[-1][0]:+.2f}, {PEAKS[-1][1]:+.2f})"
          f" · height {PEAKS[-1][2]:.3f}")

    build_animation(grad_path, es_hist,
                    here / "rl_vs_es_landscape.mp4",
                    here / "rl_vs_es_landscape.gif",
                    n_frames=150, fps=15)
    print("done.")


if __name__ == "__main__":
    main()
