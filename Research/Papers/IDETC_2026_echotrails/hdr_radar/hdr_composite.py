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
import matplotlib.gridspec as gridspec

from radar_loader import load_run, scans_to_gain_stack, to_4bit

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DATA = "/Volumes/MacShare/DATA/FURUNO_data/HDR_Paper_data"
SWEEP_DIRS = [f"{DATA}/Gain_Sweep_{i}" for i in range(1, 4)]
PPI_SIZE = 801

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

radar_cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list(
    "radar", [BLACK, GARNET, ROSE, WHITE], N=256
)

# Multi-stop brand colormap for HDR visualization
hdr_cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list(
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

    Parameters
    ----------
    polar : (n_spokes, n_bins) array (any numeric dtype)
    size  : output image side length in pixels

    Returns
    -------
    img : (size, size) float32
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

    Parameters
    ----------
    stack_4bit : (n_gains, n_spokes, n_bins) uint8, values 0-16
    gains      : (n_gains,) int, gain value per scan
    ceiling    : saturation ceiling in 4-bit space (default 16)

    Returns
    -------
    composite : (n_spokes, n_bins) float32
    """
    order = np.argsort(gains)[::-1]  # highest gain first

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

    Parameters
    ----------
    composite : float32 array
    method    : 'linear', 'log', or 'percentile'

    Returns
    -------
    uint8 array, same shape as composite
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
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="HDR stacking compositor for radar gain sweeps")
    parser.add_argument("--method", default="log", choices=["linear", "log", "percentile"],
                        help="8-bit compression method (default: log)")
    parser.add_argument("--size", type=int, default=PPI_SIZE,
                        help=f"PPI output size in pixels (default: {PPI_SIZE})")
    args = parser.parse_args()

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
    # Sweep 1 starts at gain=2, sweeps 2 & 3 start at gain=0.
    # Find common gain range.
    common_min = max(g.min() for g in gain_arrays)
    common_max = min(g.max() for g in gain_arrays)
    print(f"Common gain range: {common_min}–{common_max}")

    aligned = []
    for stack, gains in zip(stacks, gain_arrays):
        mask = (gains >= common_min) & (gains <= common_max)
        aligned.append(stack[mask])

    # Average across sweeps (float32 to avoid overflow)
    avg_stack = np.mean(aligned, axis=0).astype(np.float32)
    # Round back to uint8 for quantization
    avg_stack_u8 = np.clip(np.round(avg_stack), 0, 255).astype(np.uint8)

    gains_common = np.arange(common_min, common_max + 1)
    print(f"Averaged stack shape: {avg_stack_u8.shape}, gains: {gains_common[0]}–{gains_common[-1]}")

    # ------------------------------------------------------------------
    # Step 3: Convert to 4-bit and composite
    # ------------------------------------------------------------------
    print("Converting to 4-bit indices ...")
    stack_4bit = to_4bit(avg_stack_u8)
    print(f"4-bit range: {stack_4bit.min()}–{stack_4bit.max()}")

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

    # Low gain: first in common range
    low_gain_idx = 0
    low_ppi = polar_to_cartesian(avg_stack_u8[low_gain_idx], size=size)

    # High gain: last in common range
    high_gain_idx = len(gains_common) - 1
    high_ppi = polar_to_cartesian(avg_stack_u8[high_gain_idx], size=size)

    # HDR composite
    hdr_ppi = polar_to_cartesian(hdr_8bit, size=size)
    print("done.")

    # ------------------------------------------------------------------
    # Step 6: Display 3-panel viewer
    # ------------------------------------------------------------------
    fig = plt.figure(figsize=(18, 7), facecolor=BLACK_10)
    fig.canvas.manager.set_window_title("HDR Stacking Compositor")

    gs = gridspec.GridSpec(1, 3, left=0.03, right=0.97, top=0.90, bottom=0.05,
                           wspace=0.08)

    panels = [
        (gs[0, 0], low_ppi,  f"Low Gain (g={gains_common[low_gain_idx]})",  0, 252),
        (gs[0, 1], high_ppi, f"High Gain (g={gains_common[high_gain_idx]})", 0, 252),
        (gs[0, 2], hdr_ppi,  f"HDR Composite ({args.method})",              0, 255),
    ]

    half = size // 2
    for spec, img, title, vmin, vmax in panels:
        ax = fig.add_subplot(spec, facecolor=BLACK)
        ax.imshow(img, cmap=radar_cmap, vmin=vmin, vmax=vmax,
                  origin="upper", interpolation="bilinear")
        ax.set_title(title, color=BLACK_90, fontsize=11, fontweight="bold")
        ax.set_xticks([])
        ax.set_yticks([])

        # Range rings
        for frac in (0.25, 0.5, 0.75):
            circ = plt.Circle((half, half), frac * half,
                              fill=False, color=BLACK_50,
                              linewidth=0.5, linestyle="--", alpha=0.5)
            ax.add_patch(circ)

    fig.text(0.5, 0.96,
             "HDR Stacking Compositor — Furuno DRS4D-NXT Gain Sweep",
             ha="center", va="top", fontsize=13, fontweight="bold",
             color=BLACK_90)

    out_path = "hdr_composite_output.png"
    fig.savefig(out_path, dpi=200, facecolor=fig.get_facecolor())
    print(f"Saved: {out_path}")

    out_pdf = "hdr_composite_output.pdf"
    fig.savefig(out_pdf, facecolor=fig.get_facecolor())
    print(f"Saved: {out_pdf}")
    plt.close(fig)

    # ------------------------------------------------------------------
    # Step 7: Color vs raw comparison (2x2)
    # ------------------------------------------------------------------
    # Also render a mid-gain PPI for context
    mid_gain_idx = len(gains_common) // 2
    mid_ppi = polar_to_cartesian(avg_stack_u8[mid_gain_idx], size=size)

    fig2 = plt.figure(figsize=(14, 14), facecolor=BLACK_10)
    fig2.canvas.manager.set_window_title("HDR Color vs Raw")

    gs2 = gridspec.GridSpec(2, 2, left=0.03, right=0.97, top=0.92, bottom=0.03,
                            wspace=0.06, hspace=0.08)

    # Top-left: raw low gain (grayscale)
    ax_ll = fig2.add_subplot(gs2[0, 0], facecolor=BLACK)
    ax_ll.imshow(low_ppi, cmap="gray", vmin=0, vmax=252,
                 origin="upper", interpolation="bilinear")
    ax_ll.set_title(f"Raw — Low Gain (g={gains_common[low_gain_idx]})",
                    color=BLACK_90, fontsize=11, fontweight="bold")
    ax_ll.set_xticks([]); ax_ll.set_yticks([])

    # Top-right: raw high gain (grayscale)
    ax_lr = fig2.add_subplot(gs2[0, 1], facecolor=BLACK)
    ax_lr.imshow(high_ppi, cmap="gray", vmin=0, vmax=252,
                 origin="upper", interpolation="bilinear")
    ax_lr.set_title(f"Raw — High Gain (g={gains_common[high_gain_idx]})",
                    color=BLACK_90, fontsize=11, fontweight="bold")
    ax_lr.set_xticks([]); ax_lr.set_yticks([])

    # Bottom-left: raw mid gain (grayscale)
    ax_ml = fig2.add_subplot(gs2[1, 0], facecolor=BLACK)
    ax_ml.imshow(mid_ppi, cmap="gray", vmin=0, vmax=252,
                 origin="upper", interpolation="bilinear")
    ax_ml.set_title(f"Raw — Mid Gain (g={gains_common[mid_gain_idx]})",
                    color=BLACK_90, fontsize=11, fontweight="bold")
    ax_ml.set_xticks([]); ax_ml.set_yticks([])

    # Bottom-right: HDR composite with brand colormap
    ax_hdr = fig2.add_subplot(gs2[1, 1], facecolor=BLACK)
    im_hdr = ax_hdr.imshow(hdr_ppi, cmap=hdr_cmap, vmin=0, vmax=255,
                            origin="upper", interpolation="bilinear")
    ax_hdr.set_title(f"HDR Composite ({args.method})",
                     color=BLACK_90, fontsize=11, fontweight="bold")
    ax_hdr.set_xticks([]); ax_hdr.set_yticks([])

    # Range rings on all panels
    for ax in [ax_ll, ax_lr, ax_ml, ax_hdr]:
        for frac in (0.25, 0.5, 0.75):
            circ = plt.Circle((half, half), frac * half,
                              fill=False, color=BLACK_50,
                              linewidth=0.5, linestyle="--", alpha=0.4)
            ax.add_patch(circ)

    fig2.text(0.5, 0.97,
              "Raw Grayscale vs HDR Color Composite",
              ha="center", va="top", fontsize=14, fontweight="bold",
              color=BLACK_90)

    out2_png = "hdr_color_comparison.png"
    fig2.savefig(out2_png, dpi=200, facecolor=fig2.get_facecolor())
    print(f"Saved: {out2_png}")

    out2_pdf = "hdr_color_comparison.pdf"
    fig2.savefig(out2_pdf, facecolor=fig2.get_facecolor())
    print(f"Saved: {out2_pdf}")

    plt.show()


if __name__ == "__main__":
    main()
