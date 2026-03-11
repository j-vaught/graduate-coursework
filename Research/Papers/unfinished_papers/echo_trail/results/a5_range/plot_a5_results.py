#!/usr/bin/env python3
"""Plot A5 Range Dependence ablation results."""

import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path
import numpy as np

# Brand colors
GARNET = "#73000A"
BLACK = "#000000"
ATLANTIC = "#466A9F"
CONGAREE = "#1F414D"
ROSE = "#CC2E40"
HORSESHOE = "#65780B"
HONEYCOMB = "#A49137"
BLACK_90 = "#363636"
BLACK_70 = "#5C5C5C"
BLACK_50 = "#A2A2A2"

RESULTS_DIR = Path(__file__).parent

RANGE_BANDS = ["near", "mid", "far"]
TRAIL_LENGTHS = [0, 3, 6, 12, 24]

RANGE_COLORS = {
    "near": GARNET,
    "mid": ATLANTIC,
    "far": CONGAREE,
}

RANGE_LABELS = {
    "near": "Near (~500 m)",
    "mid": "Mid (~2.2 km)",
    "far": "Far (~4.8 km)",
}


def read_best_metrics(run_name):
    """Read results.csv and extract best mAP50 and mAP50-95."""
    csv_path = RESULTS_DIR / run_name / "results.csv"
    if not csv_path.exists():
        return None, None, None

    best_map50 = 0
    best_map50_95 = 0
    best_epoch = 0
    with open(csv_path) as f:
        reader = csv.reader(f)
        header = next(reader)
        # Find column indices - headers have leading spaces
        header = [h.strip() for h in header]
        for row in reader:
            row = [r.strip() for r in row]
            epoch = int(row[0])
            map50 = float(row[7])
            map50_95 = float(row[8])
            if map50 > best_map50:
                best_map50 = map50
                best_map50_95 = map50_95
                best_epoch = epoch
    return best_map50, best_map50_95, best_epoch


def read_training_curve(run_name):
    """Read results.csv and return epoch-by-epoch mAP50."""
    csv_path = RESULTS_DIR / run_name / "results.csv"
    if not csv_path.exists():
        return [], []
    epochs = []
    map50s = []
    with open(csv_path) as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            row = [r.strip() for r in row]
            epochs.append(int(row[0]))
            map50s.append(float(row[7]))
    return epochs, map50s


# --- Collect data ---
data = {}
for band in RANGE_BANDS:
    data[band] = {"N": [], "map50": [], "map50_95": []}
    for n in TRAIL_LENGTHS:
        run = f"a5_{band}_N{n}"
        m50, m50_95, ep = read_best_metrics(run)
        if m50 is not None:
            data[band]["N"].append(n)
            data[band]["map50"].append(m50)
            data[band]["map50_95"].append(m50_95)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.linewidth": 1.0,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 150,
})

# ============================================================
# Plot 1: mAP50 vs Trail Length (line plot)
# ============================================================
fig, ax = plt.subplots(figsize=(7, 4.5))

for band in RANGE_BANDS:
    ax.plot(data[band]["N"], data[band]["map50"],
            marker="s", markersize=7, linewidth=2.2,
            color=RANGE_COLORS[band], label=RANGE_LABELS[band])

ax.set_xlabel("Trail Length (frames)", fontsize=12, fontweight="bold")
ax.set_ylabel("Best mAP50", fontsize=12, fontweight="bold")
ax.set_title("A5: Range Dependence — mAP50 vs Trail Length", fontsize=13, fontweight="bold")
ax.set_xticks(TRAIL_LENGTHS)
ax.set_ylim(0.35, 1.05)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.2f"))
ax.legend(frameon=False, fontsize=11)
ax.grid(axis="y", alpha=0.3, linewidth=0.8)

fig.tight_layout()
fig.savefig(RESULTS_DIR / "a5_map50_vs_trail_length.png", dpi=300, bbox_inches="tight")
fig.savefig(RESULTS_DIR / "a5_map50_vs_trail_length.pdf", bbox_inches="tight")
print("Saved: a5_map50_vs_trail_length.png/pdf")
plt.close()

# ============================================================
# Plot 2: mAP50-95 vs Trail Length (line plot)
# ============================================================
fig, ax = plt.subplots(figsize=(7, 4.5))

for band in RANGE_BANDS:
    ax.plot(data[band]["N"], data[band]["map50_95"],
            marker="s", markersize=7, linewidth=2.2,
            color=RANGE_COLORS[band], label=RANGE_LABELS[band])

ax.set_xlabel("Trail Length (frames)", fontsize=12, fontweight="bold")
ax.set_ylabel("Best mAP50-95", fontsize=12, fontweight="bold")
ax.set_title("A5: Range Dependence — mAP50-95 vs Trail Length", fontsize=13, fontweight="bold")
ax.set_xticks(TRAIL_LENGTHS)
ax.set_ylim(0.2, 0.85)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.2f"))
ax.legend(frameon=False, fontsize=11)
ax.grid(axis="y", alpha=0.3, linewidth=0.8)

fig.tight_layout()
fig.savefig(RESULTS_DIR / "a5_map50_95_vs_trail_length.png", dpi=300, bbox_inches="tight")
fig.savefig(RESULTS_DIR / "a5_map50_95_vs_trail_length.pdf", bbox_inches="tight")
print("Saved: a5_map50_95_vs_trail_length.png/pdf")
plt.close()

# ============================================================
# Plot 3: Grouped bar chart — best mAP50 by range × trail length
# ============================================================
fig, ax = plt.subplots(figsize=(9, 4.5))

x = np.arange(len(TRAIL_LENGTHS))
width = 0.25

for i, band in enumerate(RANGE_BANDS):
    vals = data[band]["map50"]
    bars = ax.bar(x + i * width, vals, width, label=RANGE_LABELS[band],
                  color=RANGE_COLORS[band], edgecolor=BLACK, linewidth=0.5)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{val:.2f}", ha="center", va="bottom", fontsize=7.5, fontweight="bold")

ax.set_xlabel("Trail Length (frames)", fontsize=12, fontweight="bold")
ax.set_ylabel("Best mAP50", fontsize=12, fontweight="bold")
ax.set_title("A5: Detection Performance by Range Band and Trail Length", fontsize=13, fontweight="bold")
ax.set_xticks(x + width)
ax.set_xticklabels([f"N={n}" for n in TRAIL_LENGTHS])
ax.set_ylim(0, 1.15)
ax.legend(frameon=False, fontsize=11)
ax.grid(axis="y", alpha=0.3, linewidth=0.8)

fig.tight_layout()
fig.savefig(RESULTS_DIR / "a5_grouped_bar.png", dpi=300, bbox_inches="tight")
fig.savefig(RESULTS_DIR / "a5_grouped_bar.pdf", bbox_inches="tight")
print("Saved: a5_grouped_bar.png/pdf")
plt.close()

# ============================================================
# Plot 4: Training curves (mAP50 over epochs) — one subplot per range
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), sharey=True)

N_COLORS = {
    0: BLACK_50,
    3: HONEYCOMB,
    6: HORSESHOE,
    12: ATLANTIC,
    24: GARNET,
}

for ax, band in zip(axes, RANGE_BANDS):
    for n in TRAIL_LENGTHS:
        run = f"a5_{band}_N{n}"
        epochs, map50s = read_training_curve(run)
        if epochs:
            ax.plot(epochs, map50s, linewidth=1.5,
                    color=N_COLORS[n], label=f"N={n}", alpha=0.85)

    ax.set_title(RANGE_LABELS[band], fontsize=12, fontweight="bold",
                 color=RANGE_COLORS[band])
    ax.set_xlabel("Epoch", fontsize=11)
    ax.set_ylim(0, 1.05)
    ax.grid(alpha=0.3, linewidth=0.8)

axes[0].set_ylabel("mAP50", fontsize=12, fontweight="bold")
axes[2].legend(frameon=False, fontsize=9, loc="lower right")

fig.suptitle("A5: Training Curves by Range Band", fontsize=14, fontweight="bold", y=1.02)
fig.tight_layout()
fig.savefig(RESULTS_DIR / "a5_training_curves.png", dpi=300, bbox_inches="tight")
fig.savefig(RESULTS_DIR / "a5_training_curves.pdf", bbox_inches="tight")
print("Saved: a5_training_curves.png/pdf")
plt.close()

# ============================================================
# Plot 5: Improvement heatmap — delta mAP50 relative to N=0
# ============================================================
fig, ax = plt.subplots(figsize=(7, 3.5))

delta_matrix = []
for band in RANGE_BANDS:
    baseline = data[band]["map50"][0]  # N=0
    deltas = [m - baseline for m in data[band]["map50"]]
    delta_matrix.append(deltas)

delta_matrix = np.array(delta_matrix)

im = ax.imshow(delta_matrix, cmap="RdYlGn", aspect="auto", vmin=-0.05, vmax=0.5)
ax.set_xticks(range(len(TRAIL_LENGTHS)))
ax.set_xticklabels([f"N={n}" for n in TRAIL_LENGTHS])
ax.set_yticks(range(len(RANGE_BANDS)))
ax.set_yticklabels([RANGE_LABELS[b] for b in RANGE_BANDS])
ax.set_xlabel("Trail Length", fontsize=12, fontweight="bold")
ax.set_title("A5: mAP50 Improvement Over Baseline (N=0)", fontsize=13, fontweight="bold")

for i in range(len(RANGE_BANDS)):
    for j in range(len(TRAIL_LENGTHS)):
        val = delta_matrix[i, j]
        color = BLACK if val < 0.3 else "white"
        ax.text(j, i, f"+{val:.3f}" if val > 0 else f"{val:.3f}",
                ha="center", va="center", fontsize=10, fontweight="bold", color=color)

cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Delta mAP50", fontsize=10)

fig.tight_layout()
fig.savefig(RESULTS_DIR / "a5_improvement_heatmap.png", dpi=300, bbox_inches="tight")
fig.savefig(RESULTS_DIR / "a5_improvement_heatmap.pdf", bbox_inches="tight")
print("Saved: a5_improvement_heatmap.png/pdf")
plt.close()

print("\nAll A5 plots generated.")
