#!/usr/bin/env python3
import pathlib
import matplotlib.pyplot as plt
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "drafts" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# USC brand palette
GARNET = "#73000A"
BLACK = "#000000"
WHITE = "#FFFFFF"
ATLANTIC = "#466A9F"
CONGAREE = "#1F414D"
HORSESHOE = "#65780B"
HONEYCOMB = "#A49137"

def create_trajectory_plot():
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # Grid/Background
    ax.set_facecolor("#F9F9F9")
    ax.grid(True, linestyle='--', alpha=0.6, color='white')

    # Simulate some trajectories
    np.random.seed(42)
    steps = np.arange(20)
    
    # Baseline (Random)
    random_x = np.cumsum(np.random.normal(0, 0.1, 20))
    random_y = np.cumsum(np.random.normal(0, 0.1, 20))
    ax.plot(random_x, random_y, color=BLACK, alpha=0.3, linestyle='--', label="Random DR")

    # Bayesian Opt (Global but jumps)
    bo_x = [0, 0.5, -0.3, 0.8, 0.2, 0.9, 0.85]
    bo_y = [0, -0.4, 0.6, -0.1, 0.5, 0.7, 0.75]
    ax.scatter(bo_x, bo_y, color=ATLANTIC, s=40, label="Bayesian Opt", zorder=3)

    # RL Policy (Sequential/Directed)
    rl_x = np.linspace(0, 1.2, 20) + np.sin(np.linspace(0, 3, 20)) * 0.1
    rl_y = np.linspace(0, 1.5, 20) + np.cos(np.linspace(0, 3, 20)) * 0.1
    ax.plot(rl_x, rl_y, color=GARNET, linewidth=2.5, label="RL Policy (Proposed)", zorder=4)
    ax.scatter(rl_x[-1], rl_y[-1], color=GARNET, s=100, marker='*', zorder=5)

    # Targets (Physical Realism)
    circle = plt.Circle((1.2, 1.6), 0.3, color=HORSESHOE, alpha=0.2, label="High-Perf Region")
    ax.add_patch(circle)

    ax.set_xlabel("Parameter 1 (e.g., Clutter Level)")
    ax.set_ylabel("Parameter 2 (e.g., Multipath Gain)")
    ax.set_title("Conceptual Parameter Space Trajectory", fontweight='bold', color=CONGAREE)
    
    ax.legend(frameon=True, facecolor=WHITE, loc='lower right')
    
    # Remove top/right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    pdf_path = FIG_DIR / "fig_parameter_trajectory.pdf"
    plt.savefig(pdf_path)
    print(f"Wrote {pdf_path}")

if __name__ == "__main__":
    create_trajectory_plot()
