"""
hdr_buoy_zoom.py
Export blob-fitted zoom crops of buoys from raw and HDR composite PPIs.

Uses connected-component bounding boxes to fit crop edges to blob extent.
Exports borderless PNGs for LaTeX composition.

Usage
-----
    python3 hdr_buoy_zoom.py
"""

import os
import sys
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy import ndimage

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from radar_loader import load_run, scans_to_gain_stack, to_4bit

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DATA_BASE = "/Volumes/MacShare/DATA/FURUNO_data/HDR_Paper_data"
SWEEP_DIRS = [
    f"{DATA_BASE}/Gain_Sweep_1",
    f"{DATA_BASE}/Gain_Sweep_2",
    f"{DATA_BASE}/Gain_Sweep_3",
]
FIGURES_DIR = os.path.join(SCRIPT_DIR, "figures")
TARGETS_FILE = os.path.join(SCRIPT_DIR, "targets.json")

PPI_SIZE = 2401  # High-res for ~100px crops
MARGIN = 36      # Pixels of margin around blob bounding box
SELECTED_BUOYS = ["buoy_7", "buoy_4", "buoy_3"]

# Brand colors
BLACK    = "#000000"
CONGAREE = "#1F414D"
ATLANTIC = "#466A9F"
ROSE     = "#CC2E40"
GARNET   = "#73000A"
HONEYCOMB = "#A49137"
WHITE    = "#FFFFFF"

hdr_cmap = LinearSegmentedColormap.from_list(
    "hdr", [BLACK, CONGAREE, ATLANTIC, ROSE, GARNET, HONEYCOMB, WHITE], N=256
)


# ---------------------------------------------------------------------------
# Core functions (same as hdr_composite.py)
# ---------------------------------------------------------------------------

def polar_to_cartesian(polar, out_size=PPI_SIZE):
    n_spokes, n_bins = polar.shape
    half = out_size // 2
    ys, xs = np.mgrid[0:out_size, 0:out_size]
    dx = (xs - half).astype(np.float32)
    dy = (half - ys).astype(np.float32)
    r_px = np.sqrt(dx**2 + dy**2)
    r_frac = r_px / half
    theta_deg = np.degrees(np.arctan2(dx, dy)) % 360.0
    r_idx = np.round(r_frac * (n_bins - 1)).astype(np.int32)
    spoke_idx = np.round(theta_deg / 360.0 * n_spokes).astype(np.int32) % n_spokes
    inside = r_idx < n_bins
    img = np.zeros((out_size, out_size), dtype=np.float32)
    img[inside] = polar[spoke_idx[inside], r_idx[inside]]
    return img


def stack_composite_noclip(stack_4bit, gains):
    """Sum all gain levels without skipping saturated pixels."""
    return stack_4bit.astype(np.float32).sum(axis=0)


def compress_to_8bit(composite, method="log"):
    if method == "log":
        c = np.log1p(composite)
    elif method == "linear":
        c = composite.copy()
    else:
        c = composite.copy()
    cmax = c.max()
    if cmax > 0:
        c = c / cmax * 255.0
    return c.astype(np.uint8)


def target_to_pixel(target, n_spokes, n_bins, out_size):
    """Convert target polar coords to PPI pixel coords."""
    half = out_size // 2
    r_frac = target["range_bin"] / (n_bins - 1)
    a_rad = np.radians(target["angle_deg"])
    px = half + r_frac * half * np.sin(a_rad)
    py = half - r_frac * half * np.cos(a_rad)
    return int(round(px)), int(round(py))


def find_blob_bbox(ppi, cx, cy, threshold=10, search_radius=60):
    """
    Find connected-component bounding box around a target location.
    Returns (y0, y1, x0, x1) of the crop region with margin.
    """
    # Extract search region
    h, w = ppi.shape
    sy0 = max(0, cy - search_radius)
    sy1 = min(h, cy + search_radius)
    sx0 = max(0, cx - search_radius)
    sx1 = min(w, cx + search_radius)
    region = ppi[sy0:sy1, sx0:sx1]

    # Threshold and label
    binary = region > threshold
    labeled, n_features = ndimage.label(binary)

    if n_features == 0:
        # Fallback: fixed crop
        return (cy - MARGIN, cy + MARGIN, cx - MARGIN, cx + MARGIN)

    # Find label at center
    local_cy = cy - sy0
    local_cx = cx - sx0
    center_label = labeled[local_cy, local_cx] if 0 <= local_cy < labeled.shape[0] and 0 <= local_cx < labeled.shape[1] else 0

    if center_label == 0:
        # Find nearest non-zero label
        nz = np.argwhere(labeled > 0)
        if len(nz) == 0:
            return (cy - MARGIN, cy + MARGIN, cx - MARGIN, cx + MARGIN)
        dists = (nz[:, 0] - local_cy)**2 + (nz[:, 1] - local_cx)**2
        nearest = nz[np.argmin(dists)]
        center_label = labeled[nearest[0], nearest[1]]

    # Get bounding box of this component
    component = labeled == center_label
    ys, xs = np.where(component)
    by0 = ys.min() + sy0
    by1 = ys.max() + sy0
    bx0 = xs.min() + sx0
    bx1 = xs.max() + sx0

    # Make square with margin
    bh = by1 - by0
    bw = bx1 - bx0
    side = max(bh, bw) + 2 * MARGIN
    cby = (by0 + by1) // 2
    cbx = (bx0 + bx1) // 2

    y0 = max(0, cby - side // 2)
    y1 = min(h, cby + side // 2)
    x0 = max(0, cbx - side // 2)
    x1 = min(w, cbx + side // 2)

    return (y0, y1, x0, x1)


def save_crop(img, path, cmap, vmin=0, vmax=255):
    """Save a crop as borderless PNG."""
    h, w = img.shape
    dpi = 150
    fig, ax = plt.subplots(figsize=(w / dpi, h / dpi), dpi=dpi)
    ax.imshow(img, cmap=cmap, vmin=vmin, vmax=vmax,
              origin="upper", interpolation="bilinear")
    ax.set_axis_off()
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    print(f"  Saved {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)

    # Load targets
    with open(TARGETS_FILE) as f:
        all_targets = json.load(f)
    targets = {t["label"]: t for t in all_targets}

    # Load and process data
    print("Loading 3 gain sweeps...")
    sweeps = []
    for d in SWEEP_DIRS:
        scans = load_run(d, verbose=True)
        stack, gains = scans_to_gain_stack(scans)
        sweeps.append((stack, gains))

    g_min = max(g.min() for _, g in sweeps)
    g_max = min(g.max() for _, g in sweeps)

    aligned = []
    for stack, gains in sweeps:
        mask = (gains >= g_min) & (gains <= g_max)
        aligned.append(stack[mask])
    common_gains = np.arange(g_min, g_max + 1)

    avg_stack = np.mean(aligned, axis=0).astype(np.uint8)
    n_spokes, n_bins = avg_stack.shape[1], avg_stack.shape[2]

    # HDR composite
    print("Computing HDR composite...")
    stack_4bit = to_4bit(avg_stack)
    composite = stack_composite_noclip(stack_4bit, common_gains)
    hdr_8bit = compress_to_8bit(composite, method="log")

    # Render high-res PPIs
    print(f"Rendering PPIs at {PPI_SIZE}px...")
    # Use mid gain (g=50) for raw comparison
    mid_idx = np.argmin(np.abs(common_gains - 50))
    print(f"  Raw comparison gain: {common_gains[mid_idx]}")
    raw_ppi = polar_to_cartesian(avg_stack[mid_idx].astype(np.float32) * (255.0 / 252.0), PPI_SIZE)
    hdr_ppi = polar_to_cartesian(hdr_8bit.astype(np.float32), PPI_SIZE)

    # Export crops for each selected buoy
    print("Extracting buoy crops...")
    for label in SELECTED_BUOYS:
        if label not in targets:
            print(f"  Warning: {label} not in targets.json, skipping")
            continue

        t = targets[label]
        cx, cy = target_to_pixel(t, n_spokes, n_bins, PPI_SIZE)
        print(f"  {label}: pixel ({cx}, {cy})")

        # Use HDR PPI for blob detection (better visibility)
        y0, y1, x0, x1 = find_blob_bbox(hdr_ppi, cx, cy)
        print(f"    Crop: [{y0}:{y1}, {x0}:{x1}] = {y1-y0}x{x1-x0}px")

        # Extract same crop from both raw and HDR
        raw_crop = raw_ppi[y0:y1, x0:x1]
        hdr_crop = hdr_ppi[y0:y1, x0:x1]

        buoy_num = label.split("_")[1]
        save_crop(raw_crop, os.path.join(FIGURES_DIR, f"zoom_buoy_{buoy_num}_raw.png"), hdr_cmap)
        save_crop(hdr_crop, os.path.join(FIGURES_DIR, f"zoom_buoy_{buoy_num}_hdr.png"), hdr_cmap)

    print("Done.")


if __name__ == "__main__":
    main()
