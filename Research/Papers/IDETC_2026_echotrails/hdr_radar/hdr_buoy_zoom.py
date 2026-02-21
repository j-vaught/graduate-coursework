"""
hdr_buoy_zoom.py
Zoomed-in comparison of individual buoys: raw single-gain vs HDR composite.

Usage
-----
    python hdr_buoy_zoom.py
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from radar_loader import load_run, scans_to_gain_stack, to_4bit
from hdr_composite import (
    polar_to_cartesian, stack_composite, compress_to_8bit,
    DATA, SWEEP_DIRS, hdr_cmap,
    BLACK, BLACK_90, BLACK_50, BLACK_10, WHITE, ATLANTIC,
)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

PPI_SIZE = 801
ZOOM_RADIUS = 45  # pixels around each buoy center
TARGETS_FILE = "targets.json"


def buoy_pixel(target: dict, n_bins: int, half: int) -> tuple[float, float]:
    """Convert a target's polar coords to PPI pixel coords."""
    r_frac = target["range_bin"] / (n_bins - 1)
    a_rad = np.radians(target["angle_deg"])
    px = half + r_frac * half * np.sin(a_rad)
    py = half - r_frac * half * np.cos(a_rad)
    return px, py


def main() -> None:
    # ------------------------------------------------------------------
    # Load targets
    # ------------------------------------------------------------------
    with open(TARGETS_FILE) as f:
        targets = json.load(f)

    buoys = [t for t in targets if t.get("type") == "buoy"]
    print(f"Found {len(buoys)} buoy targets")

    # ------------------------------------------------------------------
    # Load and process data (same pipeline as hdr_composite.py)
    # ------------------------------------------------------------------
    print("Loading gain sweeps ...")
    stacks, gain_arrays = [], []
    for d in SWEEP_DIRS:
        scans = load_run(d, verbose=True)
        stack, gains = scans_to_gain_stack(scans)
        stacks.append(stack)
        gain_arrays.append(gains)

    common_min = max(g.min() for g in gain_arrays)
    common_max = min(g.max() for g in gain_arrays)

    aligned = []
    for stack, gains in zip(stacks, gain_arrays):
        mask = (gains >= common_min) & (gains <= common_max)
        aligned.append(stack[mask])

    avg_stack = np.mean(aligned, axis=0).astype(np.float32)
    avg_stack_u8 = np.clip(np.round(avg_stack), 0, 255).astype(np.uint8)
    gains_common = np.arange(common_min, common_max + 1)

    # 4-bit conversion and HDR composite
    stack_4bit = to_4bit(avg_stack_u8)
    composite = stack_composite(stack_4bit, gains_common)
    hdr_8bit = compress_to_8bit(composite, method="log")

    # Render full PPIs
    print("Rendering PPIs ...", end=" ", flush=True)
    raw_scale = 255.0 / 252.0

    high_gain_idx = len(gains_common) - 1
    mid_gain_idx = len(gains_common) // 2

    raw_high = polar_to_cartesian(avg_stack_u8[high_gain_idx], size=PPI_SIZE) * raw_scale
    raw_mid = polar_to_cartesian(avg_stack_u8[mid_gain_idx], size=PPI_SIZE) * raw_scale
    hdr_ppi = polar_to_cartesian(hdr_8bit, size=PPI_SIZE)
    print("done.")

    n_bins = avg_stack_u8.shape[2]
    half = PPI_SIZE // 2

    # ------------------------------------------------------------------
    # Figure: 3 columns (raw high, raw mid, HDR) x N buoy rows
    # ------------------------------------------------------------------
    n_buoys = len(buoys)
    fig, axes = plt.subplots(
        n_buoys, 3,
        figsize=(10, n_buoys * 3.2),
        facecolor=BLACK_10,
    )
    if n_buoys == 1:
        axes = axes[np.newaxis, :]

    col_titles = [
        f"Raw High Gain (g={gains_common[high_gain_idx]})",
        f"Raw Mid Gain (g={gains_common[mid_gain_idx]})",
        "HDR Composite (log)",
    ]
    images = [raw_high, raw_mid, hdr_ppi]

    for row, buoy in enumerate(buoys):
        cx, cy = buoy_pixel(buoy, n_bins, half)
        x0 = max(0, int(cx) - ZOOM_RADIUS)
        x1 = min(PPI_SIZE, int(cx) + ZOOM_RADIUS)
        y0 = max(0, int(cy) - ZOOM_RADIUS)
        y1 = min(PPI_SIZE, int(cy) + ZOOM_RADIUS)

        for col in range(3):
            ax = axes[row, col]
            crop = images[col][y0:y1, x0:x1]
            ax.imshow(crop, cmap=hdr_cmap, vmin=0, vmax=255,
                      origin="upper", interpolation="bilinear",
                      aspect="equal")
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_facecolor(BLACK)

            if row == 0:
                ax.set_title(col_titles[col], color=BLACK_90,
                             fontsize=9, fontweight="bold")

            if col == 0:
                label = buoy.get("label", f"buoy_{row+1}")
                ax.set_ylabel(label, color=BLACK_90, fontsize=9,
                              fontweight="bold", rotation=0,
                              labelpad=50, va="center")

            # Crosshair at buoy center
            local_cx = cx - x0
            local_cy = cy - y0
            ax.axhline(local_cy, color=ATLANTIC, lw=0.5, alpha=0.6)
            ax.axvline(local_cx, color=ATLANTIC, lw=0.5, alpha=0.6)

    fig.suptitle("Buoy Zoom Comparison: Raw vs HDR Composite",
                 fontsize=13, fontweight="bold", color=BLACK_90, y=0.995)
    fig.tight_layout(rect=[0.08, 0.0, 1.0, 0.98])

    out_png = "hdr_buoy_zoom.png"
    fig.savefig(out_png, dpi=200, facecolor=fig.get_facecolor())
    print(f"Saved: {out_png}")

    out_pdf = "hdr_buoy_zoom.pdf"
    fig.savefig(out_pdf, facecolor=fig.get_facecolor())
    print(f"Saved: {out_pdf}")

    plt.show()


if __name__ == "__main__":
    main()
