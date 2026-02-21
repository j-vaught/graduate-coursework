"""
Quick test: mean gain-response curves with Savitzky-Golay smoothing,
mapped into 4-bit space (0-16 levels).

The radar outputs 17 canonical intensity levels (0-252 byte range).
We interpolate mean echo values to fractional 4-bit indices, then
smooth and plot.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

from radar_loader import load_run, scans_to_gain_stack, CANONICAL_LEVELS
from fig2_gain_response import (
    extract_patch, compute_area_and_intensity,
    SPOKE_PAD, ECHO_THRESH, DATA_DIR,
)

# Brand colors
GARNET    = "#73000A"
ATLANTIC  = "#466A9F"
CONGAREE  = "#1F414D"
HORSESHOE = "#65780B"
BLACK_90  = "#363636"
BLACK_30  = "#C7C7C7"
WHITE     = "#FFFFFF"

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.linewidth": 1.0,
    "axes.edgecolor": BLACK_90,
    "figure.facecolor": WHITE,
    "axes.facecolor": WHITE,
})

SELECTED = ["buoy_2", "buoy_7", "buoy_9", "land_1"]
COLORS = {
    "buoy_9": GARNET,
    "buoy_2": ATLANTIC,
    "buoy_7": HORSESHOE,
    "land_1": CONGAREE,
}
DISPLAY_NAMES = {
    "buoy_9": "Strong buoy",
    "buoy_2": "Moderate buoy",
    "buoy_7": "Weak buoy",
    "land_1": "Land (diffuse)",
}

# ---------------------------------------------------------------------------
# 4-bit mapping
# ---------------------------------------------------------------------------

# The 17 canonical byte values and their 4-bit index (0-16)
CANONICAL = CANONICAL_LEVELS.astype(np.float64)
FOUR_BIT_IDX = np.arange(len(CANONICAL), dtype=np.float64)

def byte_to_4bit(values: np.ndarray) -> np.ndarray:
    """
    Map byte-space echo values (0-252) to fractional 4-bit indices (0-16)
    using linear interpolation between canonical levels.
    """
    return np.interp(values, CANONICAL, FOUR_BIT_IDX)

# Print the mapping for reference
print("4-bit mapping:")
print(f"  {'Byte':>6}  {'4-bit idx':>9}")
for b, i in zip(CANONICAL.astype(int), FOUR_BIT_IDX.astype(int)):
    print(f"  {b:>6}  {i:>9}")
print()

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

with open(Path(__file__).parent / "targets.json") as f:
    all_targets = json.load(f)
targets = [t for t in all_targets if t["label"] in SELECTED]

print("Loading sweeps ...")
stacks = []
for name in ["Gain_Sweep_1", "Gain_Sweep_2", "Gain_Sweep_3"]:
    scans = load_run(f"{DATA_DIR}/{name}", verbose=False)
    stack, gains = scans_to_gain_stack(scans)
    stacks.append((stack, gains))

# Align to common gain range
g_min = max(g[0] for _, g in stacks)
g_max = min(g[-1] for _, g in stacks)
aligned = []
for stack, gains in stacks:
    mask = (gains >= g_min) & (gains <= g_max)
    aligned.append(stack[mask])
gains_common = stacks[0][1][(stacks[0][1] >= g_min) & (stacks[0][1] <= g_max)]
print(f"Aligned: gain {g_min}–{g_max}, {len(gains_common)} levels")

# Extract mean curves averaged across 3 sweeps (in byte space)
curves_byte = {}
for t in targets:
    spoke, rbin = t["spoke_idx"], t["range_bin"]
    means = []
    for stack in aligned:
        patch, s0, r0 = extract_patch(stack, spoke, rbin)
        cs, cr = SPOKE_PAD, rbin - r0
        stats, areas, _ = compute_area_and_intensity(patch, cs, cr)
        means.append(stats["mean"])
    curves_byte[t["label"]] = np.mean(means, axis=0)

# Zero out first 5 points for buoy_9
curves_byte["buoy_9"][:5] = 0.0

# Convert to 4-bit space
curves_4bit = {k: byte_to_4bit(v) for k, v in curves_byte.items()}

# ---------------------------------------------------------------------------
# Smoothing + plotting
# ---------------------------------------------------------------------------

def savgol(y, w, p=2):
    return savgol_filter(y, window_length=w, polyorder=p)

smooth_fn = lambda y: savgol(y, 11, 2)

fig, ax = plt.subplots(figsize=(6, 4))

for t in targets:
    label = t["label"]
    raw_4bit = curves_4bit[label]
    smoothed = smooth_fn(raw_4bit)
    ax.plot(gains_common, smoothed, color=COLORS[label],
            lw=2.5, label=DISPLAY_NAMES[label], alpha=0.9)

ax.axhline(16, color=BLACK_30, lw=0.8, ls=":", label="4-bit ceiling")
ax.set_xlabel("Receiver Gain Setting", fontsize=11, color=BLACK_90)
ax.set_ylabel("Digitized Intensity (4-bit)", fontsize=11, color=BLACK_90)
ax.set_title("Reflectivity-vs-Gain Response by Target Type",
             fontsize=12, fontweight="bold", color=BLACK_90)
ax.set_xlim(gains_common[0], gains_common[-1])
ax.set_ylim(-0.5, 17.5)
ax.set_yticks(range(0, 17, 2))
ax.legend(fontsize=9, loc="lower right")
ax.grid(True, alpha=0.2, color=BLACK_30)

plt.tight_layout(pad=1.5)
out = Path(__file__).parent / "figures" / "target_review" / "smoothing_comparison.png"
fig.savefig(out, dpi=200, bbox_inches="tight")
plt.close()
print(f"Saved {out}")
