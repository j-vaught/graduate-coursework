"""
hdr_buoy_zoom.py
Zoomed-in comparison of individual buoys: raw single-gain vs HDR composite.
Zoom crops are fit to the extent of each buoy's echo blob.

Usage
-----
    python hdr_buoy_zoom.py
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy import ndimage

from radar_loader import load_run, scans_to_gain_stack, to_4bit
from hdr_composite import (
    polar_to_cartesian, stack_composite, compress_to_8bit,
    DATA, SWEEP_DIRS, hdr_cmap,
    BLACK, BLACK_90, BLACK_50, BLACK_10, WHITE, ATLANTIC, GARNET,
)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

PPI_SIZE = 801
MARGIN = 12  # pixel padding around the blob bbox
TARGETS_FILE = "targets.json"


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

    Uses the high-gain PPI to detect the blob, thresholds above `threshold`,
    then finds the connected component at the buoy location.

    Returns (y0, y1, x0, x1) clipped to image bounds.
    """
    h, w = ppi.shape
    mask = ppi > threshold

    # Label connected components
    labeled, n_labels = ndimage.label(mask)

    # Which label is at the buoy center?
    icy, icx = int(round(cy)), int(round(cx))
    icy = np.clip(icy, 0, h - 1)
    icx = np.clip(icx, 0, w - 1)

    target_label = labeled[icy, icx]

    if target_label == 0:
        # Buoy center isn't on a blob — search small neighborhood
        search_r = 8
        sy0 = max(0, icy - search_r)
        sy1 = min(h, icy + search_r + 1)
        sx0 = max(0, icx - search_r)
        sx1 = min(w, icx + search_r + 1)
        patch = labeled[sy0:sy1, sx0:sx1]
        labels_nearby = patch[patch > 0]
        if len(labels_nearby) > 0:
            target_label = int(np.bincount(labels_nearby).argmax())
        else:
            # Fallback: fixed box
            return (max(0, icy - 30), min(h, icy + 30),
                    max(0, icx - 30), min(w, icx + 30))

    blob_mask = labeled == target_label
    ys, xs = np.where(blob_mask)

    y0 = max(0, int(ys.min()) - margin)
    y1 = min(h, int(ys.max()) + margin)
    x0 = max(0, int(xs.min()) - margin)
    x1 = min(w, int(xs.max()) + margin)

    return y0, y1, x0, x1


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

    raw_high = polar_to_cartesian(avg_stack_u8[high_gain_idx], size=PPI_SIZE) * raw_scale
    hdr_ppi = polar_to_cartesian(hdr_8bit, size=PPI_SIZE)
    print("done.")

    n_bins = avg_stack_u8.shape[2]
    half = PPI_SIZE // 2

    # ------------------------------------------------------------------
    # Compute blob bboxes from the high-gain PPI
    # ------------------------------------------------------------------
    print("Finding blob extents ...")
    buoy_bboxes = []
    for buoy in buoys:
        cx, cy = buoy_pixel(buoy, n_bins, half)
        y0, y1, x0, x1 = blob_bbox(raw_high, cx, cy)
        buoy_bboxes.append((y0, y1, x0, x1, cx, cy))
        label = buoy.get("label", "?")
        print(f"  {label}: blob {x1-x0}x{y1-y0} px")

    # ------------------------------------------------------------------
    # Figure: 2 columns (raw high, HDR) x N buoy rows, blob-fitted crops
    # ------------------------------------------------------------------
    n_buoys = len(buoys)
    fig, axes = plt.subplots(
        n_buoys, 2,
        figsize=(10, n_buoys * 2.8),
        facecolor=BLACK_10,
    )
    if n_buoys == 1:
        axes = axes[np.newaxis, :]

    col_titles = [
        f"Raw High Gain (g={gains_common[high_gain_idx]})",
        "HDR Composite (log)",
    ]
    images = [raw_high, hdr_ppi]

    for row, (buoy, bbox) in enumerate(zip(buoys, buoy_bboxes)):
        y0, y1, x0, x1 = bbox[:4]
        cx, cy = bbox[4], bbox[5]

        for col in range(2):
            ax = axes[row, col]
            crop = images[col][y0:y1, x0:x1]
            ax.imshow(crop, cmap=hdr_cmap, vmin=0, vmax=255,
                      origin="upper", interpolation="bilinear",
                      aspect="equal")
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_facecolor(BLACK)

            # Draw bbox edge (the crop boundary = the blob extent)
            rect = patches.Rectangle(
                (0, 0), x1 - x0 - 1, y1 - y0 - 1,
                linewidth=1.2, edgecolor=ATLANTIC,
                facecolor="none", linestyle="-",
            )
            ax.add_patch(rect)

            if row == 0:
                ax.set_title(col_titles[col], color=BLACK_90,
                             fontsize=10, fontweight="bold")

            if col == 0:
                label = buoy.get("label", f"buoy_{row+1}")
                ax.set_ylabel(label, color=BLACK_90, fontsize=9,
                              fontweight="bold", rotation=0,
                              labelpad=50, va="center")

    fig.suptitle("Buoy Blob Extent: Raw vs HDR Composite",
                 fontsize=13, fontweight="bold", color=BLACK_90, y=0.998)
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
