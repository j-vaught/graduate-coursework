"""
hdr_composite.py
HDR stacking compositor for Furuno DRS4D-NXT gain-sweep data.

Composites 101 gain-level scans into a single HDR PPI image by
additively stacking from highest to lowest gain, skipping saturated
pixels at each level.

Usage
-----
    python hdr_composite.py
    python hdr_composite.py --method log      # log / linear / percentile
    python hdr_composite.py --size 800        # PPI output size in pixels
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from radar_loader import load_run, scans_to_gain_stack, to_4bit

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DATA = "/Volumes/MacShare/DATA/FURUNO_data/HDR_Paper_data"
SWEEP_DIRS = [f"{DATA}/Gain_Sweep_{i}" for i in range(1, 4)]
PPI_SIZE = 801
FIGURES_DIR = "figures"

# Brand colors
GARNET   = "#73000A"
ATLANTIC = "#466A9F"
ROSE     = "#CC2E40"
CONGAREE = "#1F414D"
WHITE    = "#FFFFFF"
BLACK    = "#000000"
BLACK_90 = "#363636"
BLACK_50 = "#A2A2A2"
BLACK_10 = "#ECECEC"

# Multi-stop brand colormap for HDR visualization
hdr_cmap = mcolors.LinearSegmentedColormap.from_list(
    "hdr_brand",
    [BLACK, CONGAREE, ATLANTIC, ROSE, GARNET, "#A49137", WHITE],
    N=256,
)


# ---------------------------------------------------------------------------
# Polar -> Cartesian
# ---------------------------------------------------------------------------

def polar_to_cartesian(polar: np.ndarray, size: int = PPI_SIZE) -> np.ndarray:
    """
    Convert (n_spokes, n_bins) polar array to a square cartesian image.
    """
    n_spokes, n_bins = polar.shape
    half = size // 2

    ys, xs = np.mgrid[0:size, 0:size]
    dx = (xs - half).astype(np.float32)
    dy = (half - ys).astype(np.float32)

    r_px   = np.sqrt(dx**2 + dy**2)
    r_frac = r_px / half

    theta_deg = np.degrees(np.arctan2(dx, dy)) % 360.0

    r_idx     = np.round(r_frac * (n_bins - 1)).astype(np.int32)
    spoke_idx = np.round(theta_deg / 360.0 * n_spokes).astype(np.int32) % n_spokes

    inside = r_idx < n_bins
    img = np.zeros((size, size), dtype=np.float32)
    img[inside] = polar[spoke_idx[inside], r_idx[inside]]
    return img


# ---------------------------------------------------------------------------
# HDR Stacking
# ---------------------------------------------------------------------------

def stack_composite(
    stack_4bit: np.ndarray,
    gains: np.ndarray,
    ceiling: int = 16,
) -> np.ndarray:
    """
    Additive HDR composite: stack from highest gain to lowest,
    skipping saturated pixels at each level.
    """
    order = np.argsort(gains)[::-1]

    n_spokes = stack_4bit.shape[1]
    n_bins   = stack_4bit.shape[2]
    composite = np.zeros((n_spokes, n_bins), dtype=np.float32)

    for idx in order:
        scan = stack_4bit[idx].astype(np.float32)
        not_saturated = scan < ceiling
        composite += scan * not_saturated

    return composite


# ---------------------------------------------------------------------------
# 8-bit compression
# ---------------------------------------------------------------------------

def compress_to_8bit(
    composite: np.ndarray,
    method: str = "log",
) -> np.ndarray:
    """
    Compress HDR composite to uint8 (0-255).
    """
    if method == "linear":
        mx = composite.max()
        if mx == 0:
            return np.zeros_like(composite, dtype=np.uint8)
        out = composite / mx * 255.0

    elif method == "log":
        logged = np.log1p(composite)
        mx = logged.max()
        if mx == 0:
            return np.zeros_like(composite, dtype=np.uint8)
        out = logged / mx * 255.0

    elif method == "percentile":
        p99 = np.percentile(composite[composite > 0], 99) if np.any(composite > 0) else 1.0
        clipped = np.clip(composite, 0, p99)
        out = clipped / p99 * 255.0

    else:
        raise ValueError(f"Unknown method: {method!r}. Use 'linear', 'log', or 'percentile'.")

    return np.clip(out, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------------------
# Save PPI as borderless image
# ---------------------------------------------------------------------------

def save_ppi_image(ppi: np.ndarray, path: str, cmap, vmin=0, vmax=255,
                   dpi: int = 200) -> None:
    """Save a PPI array as a borderless PNG (no axes, no labels)."""
    h, w = ppi.shape
    fig, ax = plt.subplots(figsize=(w / dpi, h / dpi), dpi=dpi)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.imshow(ppi, cmap=cmap, vmin=vmin, vmax=vmax,
              origin="upper", interpolation="bilinear")
    ax.set_axis_off()
    fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=0,
                facecolor=BLACK)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="HDR stacking compositor for radar gain sweeps")
    parser.add_argument("--method", default="log", choices=["linear", "log", "percentile"],
                        help="8-bit compression method (default: log)")
    parser.add_argument("--size", type=int, default=PPI_SIZE,
                        help=f"PPI output size in pixels (default: {PPI_SIZE})")
    args = parser.parse_args()

    import os
    os.makedirs(FIGURES_DIR, exist_ok=True)

    # ------------------------------------------------------------------
    # Step 1: Load all three sweeps
    # ------------------------------------------------------------------
    print("Loading gain sweeps ...")
    stacks = []
    gain_arrays = []
    for d in SWEEP_DIRS:
        scans = load_run(d, verbose=True)
        stack, gains = scans_to_gain_stack(scans)
        stacks.append(stack)
        gain_arrays.append(gains)

    # ------------------------------------------------------------------
    # Step 2: Align gain ranges across sweeps and average
    # ------------------------------------------------------------------
    common_min = max(g.min() for g in gain_arrays)
    common_max = min(g.max() for g in gain_arrays)
    print(f"Common gain range: {common_min}–{common_max}")

    aligned = []
    for stack, gains in zip(stacks, gain_arrays):
        mask = (gains >= common_min) & (gains <= common_max)
        aligned.append(stack[mask])

    avg_stack = np.mean(aligned, axis=0).astype(np.float32)
    avg_stack_u8 = np.clip(np.round(avg_stack), 0, 255).astype(np.uint8)

    gains_common = np.arange(common_min, common_max + 1)
    print(f"Averaged stack shape: {avg_stack_u8.shape}, gains: {gains_common[0]}–{gains_common[-1]}")

    # ------------------------------------------------------------------
    # Step 3: Convert to 4-bit and composite
    # ------------------------------------------------------------------
    print("Converting to 4-bit indices ...")
    stack_4bit = to_4bit(avg_stack_u8)

    print("Running HDR stacking composite ...")
    composite = stack_composite(stack_4bit, gains_common)
    print(f"Composite range: {composite.min():.1f}–{composite.max():.1f}")

    # ------------------------------------------------------------------
    # Step 4: Compress to 8-bit
    # ------------------------------------------------------------------
    hdr_8bit = compress_to_8bit(composite, method=args.method)
    print(f"8-bit HDR ({args.method}): {hdr_8bit.min()}–{hdr_8bit.max()}")

    # ------------------------------------------------------------------
    # Step 5: Render PPIs
    # ------------------------------------------------------------------
    print("Rendering PPI images ...", end=" ", flush=True)
    size = args.size
    raw_scale = 255.0 / 252.0

    low_gain_idx = 0
    mid_gain_idx = len(gains_common) // 2
    high_gain_idx = len(gains_common) - 1

    low_ppi  = polar_to_cartesian(avg_stack_u8[low_gain_idx], size=size) * raw_scale
    mid_ppi  = polar_to_cartesian(avg_stack_u8[mid_gain_idx], size=size) * raw_scale
    high_ppi = polar_to_cartesian(avg_stack_u8[high_gain_idx], size=size) * raw_scale
    hdr_ppi  = polar_to_cartesian(hdr_8bit, size=size)
    print("done.")

    # ------------------------------------------------------------------
    # Step 6: Export borderless PPI PNGs for LaTeX
    # ------------------------------------------------------------------
    print("Saving PPI images for LaTeX ...")
    save_ppi_image(low_ppi,  f"{FIGURES_DIR}/ppi_low_gain.png",  hdr_cmap)
    save_ppi_image(mid_ppi,  f"{FIGURES_DIR}/ppi_mid_gain.png",  hdr_cmap)
    save_ppi_image(high_ppi, f"{FIGURES_DIR}/ppi_high_gain.png", hdr_cmap)
    save_ppi_image(hdr_ppi,  f"{FIGURES_DIR}/ppi_hdr.png",       hdr_cmap)

    print(f"  ppi_low_gain.png  (g={gains_common[low_gain_idx]})")
    print(f"  ppi_mid_gain.png  (g={gains_common[mid_gain_idx]})")
    print(f"  ppi_high_gain.png (g={gains_common[high_gain_idx]})")
    print(f"  ppi_hdr.png       (HDR {args.method})")
    print("Done.")


if __name__ == "__main__":
    main()
