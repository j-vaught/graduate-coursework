"""
fig2_gain_response.py
Gain-response curves with area tracking for buoy targets.

Interactive verification mode (default):
  - Left panel : zoomed PPI crop with detected area cells highlighted
  - Right top  : gain-response curve (peak intensity vs gain)
  - Right bot  : area curve (number of return cells vs gain)
  - Gain slider to scrub through levels
  - Left/Right arrow keys to cycle through targets

After verification, run with --save to generate the paper figure.

Usage
-----
    python3 fig2_gain_response.py              # interactive verification
    python3 fig2_gain_response.py --save       # generate paper figure
"""

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib.widgets import Slider

from radar_loader import load_run, scans_to_gain_stack

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DATA_DIR = "/Volumes/MacShare/DATA/FURUNO_data/HDR_Paper_data"
TARGETS_FILE = Path(__file__).parent / "targets.json"
FIG_DIR = Path(__file__).parent / "figures"

# Patch size around target for area computation (in cells)
SPOKE_PAD = 40     # ±40 spokes (~7°)
RANGE_PAD = 25     # ±25 range bins

# Threshold for "has a return"
ECHO_THRESH = 8    # first canonical non-zero level

# Brand colors
GARNET   = "#73000A"
ATLANTIC = "#466A9F"
ROSE     = "#CC2E40"
WHITE    = "#FFFFFF"
BLACK    = "#000000"
BLACK_90 = "#363636"
BLACK_70 = "#5C5C5C"
BLACK_50 = "#A2A2A2"
BLACK_30 = "#C7C7C7"
BLACK_10 = "#ECECEC"
CONGAREE = "#1F414D"
HORSESHOE = "#65780B"
HONEYCOMB = "#A49137"
GRASS    = "#CED318"

radar_cmap = LinearSegmentedColormap.from_list(
    "radar", [BLACK, GARNET, ROSE, WHITE], N=256
)

# Overlay colormap: transparent → colored
overlay_cmap = ListedColormap(["none", ATLANTIC + "88"])

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.linewidth": 1.0,
    "axes.edgecolor": BLACK_90,
    "figure.facecolor": WHITE,
    "axes.facecolor": WHITE,
})


# ---------------------------------------------------------------------------
# Area extraction
# ---------------------------------------------------------------------------

def extract_patch(stack: np.ndarray, spoke: int, rbin: int,
                  spoke_pad: int = SPOKE_PAD, range_pad: int = RANGE_PAD):
    """
    Extract a rectangular patch from the stack around (spoke, rbin).

    Parameters
    ----------
    stack : (n_gains, n_spokes, n_bins)
    spoke, rbin : center cell
    spoke_pad, range_pad : half-widths

    Returns
    -------
    patch : (n_gains, 2*spoke_pad+1, 2*range_pad+1) uint8
    spoke_start, rbin_start : origin indices for mapping back
    """
    n_gains, n_spokes, n_bins = stack.shape

    s0 = spoke - spoke_pad
    s1 = spoke + spoke_pad + 1
    r0 = max(rbin - range_pad, 0)
    r1 = min(rbin + range_pad + 1, n_bins)

    # Handle spoke wraparound
    spoke_indices = np.arange(s0, s1) % n_spokes
    patch = stack[:, spoke_indices, :][:, :, r0:r1]

    return patch, s0 % n_spokes, r0


def compute_area_and_intensity(patch: np.ndarray, center_s: int, center_r: int,
                                thresh: int = ECHO_THRESH):
    """
    For each gain level, find the connected component containing the center cell,
    return peak intensity and area (cell count).

    Parameters
    ----------
    patch     : (n_gains, h, w) uint8
    center_s  : spoke offset of target within patch
    center_r  : range offset of target within patch
    thresh    : minimum echo value to count as a return

    Returns
    -------
    intensities : (n_gains,) peak intensity in the component
    areas       : (n_gains,) cell count of the component
    masks       : (n_gains, h, w) bool — True for cells in the component
    """
    from scipy.ndimage import label

    n_gains, h, w = patch.shape
    intensities = np.zeros(n_gains, dtype=np.float32)
    areas = np.zeros(n_gains, dtype=np.int32)
    masks = np.zeros((n_gains, h, w), dtype=bool)

    for gi in range(n_gains):
        frame = patch[gi]
        binary = frame >= thresh
        labeled, n_feat = label(binary)

        if labeled[center_s, center_r] == 0:
            intensities[gi] = frame[center_s, center_r]
            areas[gi] = 0
            continue

        comp_id = labeled[center_s, center_r]
        mask = labeled == comp_id
        masks[gi] = mask
        intensities[gi] = frame[mask].max()
        areas[gi] = mask.sum()

    return intensities, areas, masks


def render_patch_ppi(patch_2d: np.ndarray, spoke_start_deg: float,
                     spoke_end_deg: float, r_start: int, r_end: int,
                     out_size: int = 200) -> np.ndarray:
    """
    Render a small polar patch to a cartesian PPI crop.

    Parameters
    ----------
    patch_2d : (n_spokes_patch, n_bins_patch) echo values
    spoke_start_deg, spoke_end_deg : azimuth range in degrees
    r_start, r_end : range bin range
    out_size : output image size

    Returns
    -------
    img : (out_size, out_size) float32
    """
    h_s, w_r = patch_2d.shape
    n_bins_total = 868  # full range extent

    # Determine the angular and radial bounds
    theta_min = np.radians(spoke_start_deg)
    theta_max = np.radians(spoke_end_deg)
    r_min_frac = r_start / n_bins_total
    r_max_frac = r_end / n_bins_total

    # Center of the patch in cartesian
    theta_mid = (theta_min + theta_max) / 2
    r_mid_frac = (r_min_frac + r_max_frac) / 2
    cx = r_mid_frac * np.sin(theta_mid)
    cy = r_mid_frac * np.cos(theta_mid)

    # Extent to show
    extent = max(r_max_frac - r_min_frac, (theta_max - theta_min) * r_mid_frac) * 1.5

    ys, xs = np.mgrid[0:out_size, 0:out_size]
    px = cx - extent / 2 + xs / out_size * extent
    py = cy + extent / 2 - ys / out_size * extent

    r_frac = np.sqrt(px**2 + py**2)
    theta = np.degrees(np.arctan2(px, py)) % 360.0

    # Map to patch indices
    spoke_deg_range = spoke_end_deg - spoke_start_deg
    if spoke_deg_range <= 0:
        spoke_deg_range += 360
    s_idx = ((theta - spoke_start_deg) % 360 / spoke_deg_range * h_s).astype(int)
    r_idx = ((r_frac - r_min_frac) / (r_max_frac - r_min_frac) * w_r).astype(int)

    valid = (s_idx >= 0) & (s_idx < h_s) & (r_idx >= 0) & (r_idx < w_r)
    img = np.zeros((out_size, out_size), dtype=np.float32)
    img[valid] = patch_2d[s_idx[valid], r_idx[valid]]
    return img


# ---------------------------------------------------------------------------
# Interactive verification viewer
# ---------------------------------------------------------------------------

def verify(targets: list[dict], stack: np.ndarray, gains: np.ndarray) -> None:
    n_gains, n_spokes, n_bins = stack.shape
    state = {"tidx": 0}

    # Pre-compute patches and areas for all targets
    results = []
    for t in targets:
        spoke, rbin = t["spoke_idx"], t["range_bin"]
        patch, s0, r0 = extract_patch(stack, spoke, rbin)
        cs = SPOKE_PAD  # center spoke in patch
        cr = rbin - r0  # center range in patch
        intensities, areas, masks = compute_area_and_intensity(patch, cs, cr)
        results.append(dict(
            target=t, patch=patch, s0=s0, r0=r0,
            cs=cs, cr=cr,
            intensities=intensities, areas=areas, masks=masks,
        ))

    # --- Figure layout ---
    fig = plt.figure(figsize=(14, 7), facecolor=BLACK_10)
    fig.canvas.manager.set_window_title("Gain-Response Verification")

    gs = gridspec.GridSpec(
        3, 2,
        left=0.06, right=0.96, top=0.92, bottom=0.10,
        wspace=0.30, hspace=0.35,
        height_ratios=[1, 1, 0.08],
        width_ratios=[1, 1],
    )

    ax_ppi  = fig.add_subplot(gs[0:2, 0], facecolor=BLACK)
    ax_int  = fig.add_subplot(gs[0, 1], facecolor=WHITE)
    ax_area = fig.add_subplot(gs[1, 1], facecolor=WHITE)
    ax_slid = fig.add_subplot(gs[2, :])

    gi0 = n_gains // 2

    # --- PPI crop ---
    im_ppi = ax_ppi.imshow(
        np.zeros((2 * SPOKE_PAD + 1, 2 * RANGE_PAD + 1)),
        cmap=radar_cmap, vmin=0, vmax=252,
        interpolation="nearest", aspect="auto",
        extent=[0, 2 * RANGE_PAD + 1, 2 * SPOKE_PAD + 1, 0],
    )
    im_overlay = ax_ppi.imshow(
        np.zeros((2 * SPOKE_PAD + 1, 2 * RANGE_PAD + 1)),
        cmap=overlay_cmap, vmin=0, vmax=1,
        interpolation="nearest", aspect="auto", alpha=0.6,
        extent=[0, 2 * RANGE_PAD + 1, 2 * SPOKE_PAD + 1, 0],
    )
    # Crosshair at center
    ax_ppi.axhline(SPOKE_PAD, color=WHITE, lw=0.5, ls=":", alpha=0.5)
    ax_ppi.axvline(RANGE_PAD, color=WHITE, lw=0.5, ls=":", alpha=0.5)
    ax_ppi.set_xlabel("Range bin offset", fontsize=9, color=BLACK_90)
    ax_ppi.set_ylabel("Spoke offset", fontsize=9, color=BLACK_90)

    # --- Intensity curve ---
    (line_int,) = ax_int.plot([], [], color=GARNET, lw=2)
    vline_int = ax_int.axvline(gains[gi0], color=ATLANTIC, lw=1.2, ls="--", alpha=0.7)
    ax_int.set_xlim(gains[0] - 1, gains[-1] + 1)
    ax_int.set_ylim(-5, 260)
    ax_int.set_ylabel("Peak echo value", fontsize=9, color=BLACK_90)
    ax_int.set_xlabel("Gain setting", fontsize=9, color=BLACK_90)
    ax_int.axhline(252, color=BLACK_30, lw=0.8, ls=":")
    ax_int.grid(True, alpha=0.2, color=BLACK_30)

    # --- Area curve ---
    (line_area,) = ax_area.plot([], [], color=ATLANTIC, lw=2)
    vline_area = ax_area.axvline(gains[gi0], color=ATLANTIC, lw=1.2, ls="--", alpha=0.7)
    ax_area.set_xlim(gains[0] - 1, gains[-1] + 1)
    ax_area.set_ylabel("Area (cells)", fontsize=9, color=BLACK_90)
    ax_area.set_xlabel("Gain setting", fontsize=9, color=BLACK_90)
    ax_area.grid(True, alpha=0.2, color=BLACK_30)

    # --- Gain slider ---
    slider = Slider(ax_slid, "Gain", gains[0], gains[-1],
                    valinit=gains[gi0], valstep=1,
                    color=GARNET, track_color=BLACK_10)
    ax_slid.set_facecolor(BLACK_10)

    def refresh(gi=None):
        r = results[state["tidx"]]
        t = r["target"]

        if gi is None:
            gi = int(np.argmin(np.abs(gains - round(slider.val))))

        # Update PPI crop
        frame = r["patch"][gi]
        mask = r["masks"][gi].astype(float)
        im_ppi.set_data(frame)
        im_overlay.set_data(mask)

        ax_ppi.set_title(
            f'{t["label"]}  ({t["type"]})  —  gain {gains[gi]}\n'
            f'bin={t["range_bin"]}, spoke={t["spoke_idx"]}, '
            f'angle={t["angle_deg"]:.1f}°',
            color=BLACK_90, fontsize=10, fontweight="bold",
        )

        # Update curves
        line_int.set_data(gains, r["intensities"])
        line_area.set_data(gains, r["areas"])
        vline_int.set_xdata([gains[gi]])
        vline_area.set_xdata([gains[gi]])

        ax_int.set_title(
            f'Peak intensity — {t["label"]}',
            color=BLACK_90, fontsize=10, fontweight="bold",
        )
        ax_area.set_title(
            f'Return area — {t["label"]}',
            color=BLACK_90, fontsize=10, fontweight="bold",
        )
        ax_area.set_ylim(-2, max(r["areas"].max() * 1.15, 5))

        fig.canvas.draw_idle()

    def on_slider(val):
        refresh()

    slider.on_changed(on_slider)

    def on_key(event):
        if event.key == "right":
            state["tidx"] = (state["tidx"] + 1) % len(results)
            refresh()
            print(f"Target: {results[state['tidx']]['target']['label']}")
        elif event.key == "left":
            state["tidx"] = (state["tidx"] - 1) % len(results)
            refresh()
            print(f"Target: {results[state['tidx']]['target']['label']}")
        elif event.key == "q":
            plt.close("all")

    fig.canvas.mpl_connect("key_press_event", on_key)

    fig.text(
        0.5, 0.97,
        "Left/Right arrows: cycle targets  |  Slider: gain level  |  'q': quit  |  "
        "Blue overlay = cells counted as area",
        ha="center", va="top", fontsize=8.5, color=BLACK_90, style="italic",
    )

    refresh()
    plt.show()


# ---------------------------------------------------------------------------
# Paper figure generation
# ---------------------------------------------------------------------------

def save_paper_figure(targets: list[dict], stack: np.ndarray,
                      gains: np.ndarray) -> None:
    n_gains, n_spokes, n_bins = stack.shape

    buoys = [t for t in targets if t["type"] == "buoy"]
    lands = [t for t in targets if t["type"] == "land"]

    # Compute gain-response for each target
    all_curves = []
    for t in targets:
        spoke, rbin = t["spoke_idx"], t["range_bin"]
        patch, s0, r0 = extract_patch(stack, spoke, rbin)
        cs, cr = SPOKE_PAD, rbin - r0
        intensities, areas, _ = compute_area_and_intensity(patch, cs, cr)
        all_curves.append(dict(
            target=t, intensities=intensities, areas=areas,
        ))

    # --- Figure: 2 panels (intensity, area) ---
    fig, (ax_int, ax_area) = plt.subplots(1, 2, figsize=(10, 4))

    buoy_colors = [GARNET, ATLANTIC, CONGAREE, HORSESHOE, HONEYCOMB,
                   ROSE, BLACK_70, BLACK_50, GRASS]

    for i, c in enumerate(all_curves):
        t = c["target"]
        if t["type"] == "buoy":
            color = buoy_colors[i % len(buoy_colors)]
            ls = "-"
        else:
            color = BLACK_90
            ls = "--"

        ax_int.plot(gains, c["intensities"], color=color, lw=1.8,
                    ls=ls, label=t["label"], alpha=0.85)
        if t["type"] == "buoy":
            ax_area.plot(gains, c["areas"], color=color, lw=1.8,
                         ls=ls, label=t["label"], alpha=0.85)

    # Land area on area plot too
    for c in all_curves:
        if c["target"]["type"] == "land":
            ax_area.plot(gains, c["areas"], color=BLACK_90, lw=1.8,
                         ls="--", label=c["target"]["label"], alpha=0.85)

    ax_int.axhline(252, color=BLACK_30, lw=0.8, ls=":", label="8-bit ceiling")
    ax_int.set_xlabel("Gain Setting", fontsize=11, color=BLACK_90)
    ax_int.set_ylabel("Peak Echo Value", fontsize=11, color=BLACK_90)
    ax_int.set_title("Gain-Response Curves", fontsize=12,
                     fontweight="bold", color=BLACK_90)
    ax_int.set_xlim(gains[0], gains[-1])
    ax_int.set_ylim(-5, 270)
    ax_int.legend(fontsize=7, loc="lower right", ncol=2)
    ax_int.grid(True, alpha=0.2, color=BLACK_30)

    ax_area.set_xlabel("Gain Setting", fontsize=11, color=BLACK_90)
    ax_area.set_ylabel("Return Area (cells)", fontsize=11, color=BLACK_90)
    ax_area.set_title("Spatial Extent vs. Gain", fontsize=12,
                      fontweight="bold", color=BLACK_90)
    ax_area.set_xlim(gains[0], gains[-1])
    ax_area.legend(fontsize=7, loc="upper left", ncol=2)
    ax_area.grid(True, alpha=0.2, color=BLACK_30)

    plt.tight_layout(pad=1.5)
    fig.savefig(FIG_DIR / "fig2_gain_response_curves.pdf", dpi=300, bbox_inches="tight")
    fig.savefig(FIG_DIR / "fig2_gain_response_curves.png", dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved fig2_gain_response_curves.pdf/png")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Gain-response curves with area")
    parser.add_argument("--save", action="store_true",
                        help="Generate paper figure instead of interactive viewer")
    parser.add_argument("--dir", default=f"{DATA_DIR}/Gain_Sweep_1",
                        help="Gain sweep directory")
    args = parser.parse_args()

    # Load targets
    with open(TARGETS_FILE) as f:
        targets = json.load(f)
    print(f"Loaded {len(targets)} targets from {TARGETS_FILE}")

    # Load data
    print("Loading gain sweep ...")
    scans = load_run(args.dir, verbose=True)
    stack, gains = scans_to_gain_stack(scans)
    print(f"Stack: {stack.shape}")

    if args.save:
        save_paper_figure(targets, stack, gains)
    else:
        verify(targets, stack, gains)


if __name__ == "__main__":
    main()
