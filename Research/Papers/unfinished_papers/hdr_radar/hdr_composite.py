"""
hdr_composite.py
HDR stacking compositor for Furuno DRS4D-NXT radar data.

Loads 3 gain sweeps, averages across sweeps, composites all gain levels
via additive stacking (skipping saturated pixels), compresses to 8-bit,
and exports borderless PPI PNGs.

Usage
-----
    python3 hdr_composite.py
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

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
PPI_SIZE = 801

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
# Core functions
# ---------------------------------------------------------------------------

def polar_to_cartesian(polar: np.ndarray, out_size: int = PPI_SIZE) -> np.ndarray:
    """Convert (n_spokes, n_bins) polar array to square cartesian PPI image."""
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


def stack_composite(stack_4bit: np.ndarray, gains: np.ndarray, ceiling: int = 16) -> np.ndarray:
    """
    Additive stacking composite from highest gain to lowest.
    Skip saturated pixels (value == ceiling).

    Parameters
    ----------
    stack_4bit : (n_gains, n_spokes, n_bins) uint8, 4-bit indices 0-16
    gains      : (n_gains,) gain values
    ceiling    : saturation value to skip

    Returns
    -------
    composite : (n_spokes, n_bins) float32
    """
    order = np.argsort(gains)[::-1]  # highest gain first
    n_spokes, n_bins = stack_4bit.shape[1], stack_4bit.shape[2]
    composite = np.zeros((n_spokes, n_bins), dtype=np.float32)

    for gi in order:
        scan = stack_4bit[gi].astype(np.float32)
        not_saturated = scan < ceiling
        composite += scan * not_saturated

    return composite


def stack_composite_noclip(stack_4bit: np.ndarray, gains: np.ndarray) -> np.ndarray:
    """
    Additive stacking composite without saturation clipping.
    Simply sums all gain levels together regardless of saturation.

    Parameters
    ----------
    stack_4bit : (n_gains, n_spokes, n_bins) uint8, 4-bit indices 0-16
    gains      : (n_gains,) gain values

    Returns
    -------
    composite : (n_spokes, n_bins) float32
    """
    return stack_4bit.astype(np.float32).sum(axis=0)


def compress_to_8bit(composite: np.ndarray, method: str = "log") -> np.ndarray:
    """Compress float32 composite to uint8 (0-255)."""
    if method == "log":
        c = np.log1p(composite)
    elif method == "linear":
        c = composite.copy()
    elif method == "percentile":
        p99 = np.percentile(composite, 99)
        c = np.clip(composite, 0, p99)
    else:
        raise ValueError(f"Unknown method: {method}")

    cmax = c.max()
    if cmax > 0:
        c = c / cmax * 255.0
    return c.astype(np.uint8)


def save_ppi_image(img: np.ndarray, path: str, cmap, vmin: float = 0, vmax: float = 255):
    """Save a PPI image as a borderless PNG."""
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

    # Load all 3 sweeps
    print("Loading 3 gain sweeps...")
    sweeps = []
    for d in SWEEP_DIRS:
        scans = load_run(d, verbose=True)
        stack, gains = scans_to_gain_stack(scans)
        sweeps.append((stack, gains))

    # Align to common gain range (2-99)
    g_min = max(g.min() for _, g in sweeps)
    g_max = min(g.max() for _, g in sweeps)
    print(f"Common gain range: {g_min}-{g_max}")

    aligned = []
    for stack, gains in sweeps:
        mask = (gains >= g_min) & (gains <= g_max)
        aligned.append(stack[mask])
    common_gains = np.arange(g_min, g_max + 1)

    # Average across sweeps
    print("Averaging across sweeps...")
    avg_stack = np.mean(aligned, axis=0).astype(np.uint8)
    print(f"Averaged stack shape: {avg_stack.shape}")

    # Convert to 4-bit
    print("Converting to 4-bit indices...")
    stack_4bit = to_4bit(avg_stack)

    # Composite (with saturation clipping)
    print("Running additive stacking composite (clipped)...")
    composite = stack_composite(stack_4bit, common_gains)
    hdr_8bit = compress_to_8bit(composite, method="log")

    # Composite (no clipping — raw sum)
    print("Running additive stacking composite (no clip)...")
    composite_noclip = stack_composite_noclip(stack_4bit, common_gains)
    hdr_noclip_8bit = compress_to_8bit(composite_noclip, method="log")

    # Generate PPI images
    print("Rendering PPIs...")
    low_idx = 0
    low_ppi = polar_to_cartesian(avg_stack[low_idx].astype(np.float32) * (255.0 / 252.0))

    high_idx = len(common_gains) - 1
    high_ppi = polar_to_cartesian(avg_stack[high_idx].astype(np.float32) * (255.0 / 252.0))

    hdr_ppi = polar_to_cartesian(hdr_8bit.astype(np.float32))
    hdr_noclip_ppi = polar_to_cartesian(hdr_noclip_8bit.astype(np.float32))

    # Save PNGs
    print("Saving PNGs...")
    save_ppi_image(low_ppi, os.path.join(FIGURES_DIR, "ppi_low_gain.png"), hdr_cmap)
    save_ppi_image(high_ppi, os.path.join(FIGURES_DIR, "ppi_high_gain.png"), hdr_cmap)
    save_ppi_image(hdr_noclip_ppi, os.path.join(FIGURES_DIR, "ppi_hdr.png"), hdr_cmap)
    save_ppi_image(hdr_ppi, os.path.join(FIGURES_DIR, "ppi_hdr_clipped.png"), hdr_cmap)

    print("Done.")


if __name__ == "__main__":
    main()
