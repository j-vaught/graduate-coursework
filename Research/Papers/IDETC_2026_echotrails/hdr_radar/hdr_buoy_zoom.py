"""
hdr_buoy_zoom.py
Export blob-fitted zoom crops for selected buoys: raw vs HDR composite.
Outputs borderless PNGs for inclusion in a LaTeX figure.

Usage
-----
    python hdr_buoy_zoom.py
"""

import json
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from radar_loader import load_run, scans_to_gain_stack, to_4bit
from hdr_composite import (
    polar_to_cartesian, stack_composite, compress_to_8bit, save_ppi_image,
    DATA, SWEEP_DIRS, hdr_cmap,
    BLACK, FIGURES_DIR,
)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

PPI_SIZE = 2401
MARGIN = 36
TARGETS_FILE = os.path.join(SCRIPT_DIR, "targets.json")
SELECTED_BUOYS = ["buoy_7", "buoy_4", "buoy_3"]


def buoy_pixel(target: dict, n_bins: int, half: int) -> tuple[float, float]:
    """Convert a target's polar coords to PPI pixel coords."""
    r_frac = target["range_bin"] / (n_bins - 1)
    a_rad = np.radians(target["angle_deg"])
    px = half + r_frac * half * np.sin(a_rad)
    py = half - r_frac * half * np.cos(a_rad)
    return px, py


def blob_bbox(ppi: np.ndarray, cx: float, cy: float,
              threshold: float = 5.0, margin: int = MARGIN) -> tuple[int, int, int, int]:
    """
    Find the bounding box of the connected echo blob containing (cx, cy).
    Returns (y0, y1, x0, x1) clipped to image bounds.
    """
    h, w = ppi.shape
    mask = ppi > threshold
    labeled, _ = ndimage.label(mask)

    icy, icx = int(round(cy)), int(round(cx))
    icy = np.clip(icy, 0, h - 1)
    icx = np.clip(icx, 0, w - 1)

    target_label = labeled[icy, icx]

    if target_label == 0:
        search_r = 8
        sy0, sy1 = max(0, icy - search_r), min(h, icy + search_r + 1)
        sx0, sx1 = max(0, icx - search_r), min(w, icx + search_r + 1)
        patch = labeled[sy0:sy1, sx0:sx1]
        labels_nearby = patch[patch > 0]
        if len(labels_nearby) > 0:
            target_label = int(np.bincount(labels_nearby).argmax())
        else:
            return (max(0, icy - 30), min(h, icy + 30),
                    max(0, icx - 30), min(w, icx + 30))

    blob_mask = labeled == target_label
    ys, xs = np.where(blob_mask)

    y0 = max(0, int(ys.min()) - margin)
    y1 = min(h, int(ys.max()) + margin)
    x0 = max(0, int(xs.min()) - margin)
    x1 = min(w, int(xs.max()) + margin)

    return y0, y1, x0, x1


def save_crop(ppi: np.ndarray, bbox: tuple, path: str, dpi: int = 200) -> None:
    """Save a cropped region as a borderless PNG."""
    y0, y1, x0, x1 = bbox
    crop = ppi[y0:y1, x0:x1]
    h, w = crop.shape
    fig, ax = plt.subplots(figsize=(w / dpi, h / dpi), dpi=dpi)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.imshow(crop, cmap=hdr_cmap, vmin=0, vmax=255,
              origin="upper", interpolation="bilinear")
    ax.set_axis_off()
    fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=0,
                facecolor=BLACK)
    plt.close(fig)


def main() -> None:
    figures_dir = os.path.join(SCRIPT_DIR, FIGURES_DIR)
    os.makedirs(figures_dir, exist_ok=True)

    # Load targets
    with open(TARGETS_FILE) as f:
        targets = json.load(f)

    buoys_all = {t["label"]: t for t in targets if t.get("type") == "buoy"}
    buoys = [(label, buoys_all[label]) for label in SELECTED_BUOYS]
    print(f"Selected buoys: {[b[0] for b in buoys]}")

    # Load and process data
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

    stack_4bit = to_4bit(avg_stack_u8)
    composite = stack_composite(stack_4bit, gains_common)
    hdr_8bit = compress_to_8bit(composite, method="log")

    # Render PPIs
    print("Rendering PPIs ...", end=" ", flush=True)
    raw_scale = 255.0 / 252.0
    high_gain_idx = len(gains_common) - 1

    raw_high = polar_to_cartesian(avg_stack_u8[high_gain_idx], size=PPI_SIZE) * raw_scale
    hdr_ppi = polar_to_cartesian(hdr_8bit, size=PPI_SIZE)
    print("done.")

    n_bins = avg_stack_u8.shape[2]
    half = PPI_SIZE // 2

    # Export crops
    print("Exporting buoy crops ...")
    for label, buoy in buoys:
        cx, cy = buoy_pixel(buoy, n_bins, half)
        bbox = blob_bbox(raw_high, cx, cy)
        y0, y1, x0, x1 = bbox
        print(f"  {label}: {x1-x0}x{y1-y0} px")

        save_crop(raw_high, bbox, f"{figures_dir}/zoom_{label}_raw.png")
        save_crop(hdr_ppi,  bbox, f"{figures_dir}/zoom_{label}_hdr.png")

    print("Done.")


if __name__ == "__main__":
    main()
