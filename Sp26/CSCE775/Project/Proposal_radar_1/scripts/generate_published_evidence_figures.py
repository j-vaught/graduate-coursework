#!/usr/bin/env python3
import pathlib
import matplotlib.pyplot as plt
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "drafts" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# USC brand palette from AGENTS.md
GARNET = "#73000A"
BLACK = "#000000"
WHITE = "#FFFFFF"
NEUTRAL_90 = "#363636"
NEUTRAL_30 = "#C7C7C7"
ATLANTIC = "#466A9F"
CONGAREE = "#1F414D"
HORSESHOE = "#65780B"
HONEYCOMB = "#A49137"

# Panel A: Radar sim-to-real baseline failure vs adapted methods (Trinh 2026)
methods = ["RT Baseline", "Random DR", "Calibrated DR"]
occ = [50, 83, 97]
count = [33, 61, 72]

# Panel B: SAR synthetic-to-measured transfer averages (Kim 2024, scenario 1)
methods2 = ["w/o Aug", "Only Noise", "Gamma+Noise", "SSR"]
avg2 = [47.86, 68.41, 87.52, 91.53]

colors_b = [NEUTRAL_90, HONEYCOMB, ATLANTIC, HORSESHOE]

fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8), constrained_layout=True)
fig.patch.set_facecolor(WHITE)

x = np.arange(len(methods))
width = 0.36
axes[0].bar(
    x - width / 2,
    occ,
    width=width,
    color=GARNET,
    edgecolor=BLACK,
    linewidth=0.8,
    hatch="///",
    label="Occupancy",
)
axes[0].bar(
    x + width / 2,
    count,
    width=width,
    color=ATLANTIC,
    edgecolor=BLACK,
    linewidth=0.8,
    hatch="xxx",
    label="People counting",
)
axes[0].set_xticks(x)
axes[0].set_xticklabels(methods, rotation=10)
axes[0].set_ylim(0, 105)
axes[0].set_ylabel("Balanced Accuracy (%)")
axes[0].set_title("Real FMCW Radar Transfer (Trinh et al., 2026)")
axes[0].grid(axis="y", linestyle="-", linewidth=0.7, color=NEUTRAL_30, alpha=1.0)
axes[0].set_axisbelow(True)
axes[0].legend(frameon=False, fontsize=9, loc="upper left")
for i, v in enumerate(occ):
    axes[0].text(i - width / 2, v + 1.5, f"{v}", ha="center", va="bottom", fontsize=8)
for i, v in enumerate(count):
    axes[0].text(i + width / 2, v + 1.5, f"{v}", ha="center", va="bottom", fontsize=8)

x2 = np.arange(len(methods2))
axes[1].bar(x2, avg2, color=colors_b, edgecolor=BLACK, linewidth=0.8)
axes[1].set_xticks(x2)
axes[1].set_xticklabels(methods2, rotation=10)
axes[1].set_ylim(0, 100)
axes[1].set_ylabel("Mean ATR Accuracy (%)")
axes[1].set_title("SAMPLE Scenario 1 Mean over 8 Networks (Kim et al., 2024)")
axes[1].grid(axis="y", linestyle="-", linewidth=0.7, color=NEUTRAL_30, alpha=1.0)
axes[1].set_axisbelow(True)
for i, v in enumerate(avg2):
    axes[1].text(i, v + 1.5, f"{v:.1f}", ha="center", va="bottom", fontsize=8)

for ax in axes:
    ax.set_facecolor(WHITE)
    for spine in ax.spines.values():
        spine.set_color(BLACK)
        spine.set_linewidth(1.0)
    ax.tick_params(colors=BLACK, width=0.8)
    ax.yaxis.label.set_color(BLACK)
    ax.xaxis.label.set_color(BLACK)
    ax.title.set_color(CONGAREE)

fig.suptitle(
    "Published Evidence: Non-Adaptive Baseline Failure and Adaptive Transfer Gains",
    fontsize=12,
    fontweight="bold",
    color=CONGAREE,
)

pdf_path = FIG_DIR / "fig_published_evidence_results.pdf"
svg_path = FIG_DIR / "fig_published_evidence_results.svg"
fig.savefig(pdf_path)
fig.savefig(svg_path)
print(f"Wrote {pdf_path}")
print(f"Wrote {svg_path}")
