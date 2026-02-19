"""
ppi_viewer.py
Interactive PPI viewer for Furuno HDR radar data.

Left-click  : mark a target cell (prints coords, plots dot)
Right-click : remove nearest mark
Scroll      : zoom in/out on PPI
Middle-drag : pan the PPI
'h'         : reset zoom (home)
's'         : save marked targets to targets.json
'c'         : clear all marks
'q'         : quit

Usage
-----
    python3 ppi_viewer.py
    python3 ppi_viewer.py --dir /path/to/Gain_Sweep_1
"""

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.widgets import Slider

from radar_loader import load_run, scans_to_gain_stack

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DATA_DIR = "/Volumes/MacShare/DATA/FURUNO_data/HDR_Paper_data/Gain_Sweep_1"
PPI_SIZE  = 601   # pixels per side (odd so center pixel exists)
TARGETS_FILE = Path(__file__).parent / "targets.json"

# Brand colors
GARNET   = "#73000A"
ATLANTIC = "#466A9F"
ROSE     = "#CC2E40"
WHITE    = "#FFFFFF"
BLACK    = "#000000"
BLACK_90 = "#363636"
BLACK_50 = "#A2A2A2"
BLACK_10 = "#ECECEC"

radar_cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list(
    "radar", [BLACK, GARNET, ROSE, WHITE], N=256
)


# ---------------------------------------------------------------------------
# Polar → Cartesian rendering
# ---------------------------------------------------------------------------

def render_ppi(echoes: np.ndarray, out_size: int = PPI_SIZE) -> np.ndarray:
    """
    Convert (n_spokes, n_bins) polar echo array to a square cartesian image.

    Parameters
    ----------
    echoes   : (n_spokes, n_bins) uint8 array
    out_size : output image side length in pixels

    Returns
    -------
    img : (out_size, out_size) float32, values in echo range
    """
    n_spokes, n_bins = echoes.shape
    half = out_size // 2

    ys, xs = np.mgrid[0:out_size, 0:out_size]
    dx = (xs - half).astype(np.float32)
    dy = (half - ys).astype(np.float32)   # north = up

    r_px   = np.sqrt(dx**2 + dy**2)
    r_frac = r_px / half                  # 0 at center, 1 at edge

    # Azimuth: 0 = North, clockwise (standard radar convention)
    theta_deg = np.degrees(np.arctan2(dx, dy)) % 360.0

    r_idx     = np.round(r_frac * (n_bins - 1)).astype(np.int32)
    spoke_idx = np.round(theta_deg / 360.0 * n_spokes).astype(np.int32) % n_spokes

    inside = r_idx < n_bins
    img = np.zeros((out_size, out_size), dtype=np.float32)
    img[inside] = echoes[spoke_idx[inside], r_idx[inside]]
    return img


def pixel_to_cell(px: float, py: float, n_spokes: int, n_bins: int,
                  out_size: int = PPI_SIZE) -> tuple[int, int, float]:
    """
    Convert a pixel coordinate (data coords) to (range_bin, spoke_index, angle_deg).
    Returns (-1, -1, -1) if the click is outside the radar circle.
    """
    half = out_size // 2
    dx = px - half
    dy = half - py
    r_px = np.sqrt(dx**2 + dy**2)
    if r_px > half:
        return -1, -1, -1.0

    r_frac    = r_px / half
    r_bin     = int(round(r_frac * (n_bins - 1)))
    theta_deg = float(np.degrees(np.arctan2(dx, dy)) % 360.0)
    spoke_idx = int(round(theta_deg / 360.0 * n_spokes)) % n_spokes
    return r_bin, spoke_idx, theta_deg


# ---------------------------------------------------------------------------
# Main viewer
# ---------------------------------------------------------------------------

def main(data_dir: str) -> None:
    print(f"Loading {Path(data_dir).name} ...")
    scans = load_run(data_dir, verbose=True)
    stack, gains = scans_to_gain_stack(scans)   # (n_gains, 2048, 868)

    n_gains, n_spokes, n_bins = stack.shape
    print(f"Stack: {n_gains} gain levels, {n_spokes} spokes, {n_bins} bins")
    print(f"Gains: {gains[0]} → {gains[-1]}")

    # Pre-render all PPI frames as float32
    print("Pre-rendering PPI frames ...", end=" ", flush=True)
    frames = np.stack([render_ppi(stack[g]) for g in range(n_gains)], axis=0)
    print("done.")

    # -----------------------------------------------------------------------
    # Figure layout: PPI (left) | gain-response curve (right)
    # -----------------------------------------------------------------------
    fig = plt.figure(figsize=(13, 7), facecolor=BLACK_10)
    fig.canvas.manager.set_window_title("HDR Radar PPI Viewer")

    gs = gridspec.GridSpec(
        2, 2,
        left=0.04, right=0.97, top=0.94, bottom=0.12,
        wspace=0.35, hspace=0.15,
        height_ratios=[1, 0.08],
    )

    ax_ppi  = fig.add_subplot(gs[0, 0], facecolor=BLACK)
    ax_resp = fig.add_subplot(gs[0, 1], facecolor=WHITE)
    ax_slid = fig.add_subplot(gs[1, :])

    # -- PPI display --
    gi0   = n_gains // 2
    im    = ax_ppi.imshow(
        frames[gi0], cmap=radar_cmap,
        vmin=0, vmax=252,
        origin="upper", interpolation="bilinear",
        extent=[0, PPI_SIZE, PPI_SIZE, 0],
    )
    ax_ppi.set_title(f"PPI  —  gain = {gains[gi0]}",
                     color=BLACK_90, fontsize=11, fontweight="bold")
    ax_ppi.set_xticks([])
    ax_ppi.set_yticks([])

    # range rings at 25 %, 50 %, 75 %
    half = PPI_SIZE // 2
    for frac in (0.25, 0.5, 0.75):
        circ = plt.Circle((half, half), frac * half,
                          fill=False, color=BLACK_50,
                          linewidth=0.6, linestyle="--", alpha=0.6)
        ax_ppi.add_patch(circ)

    # north tick
    ax_ppi.annotate("N", xy=(half, 4), ha="center", va="top",
                    fontsize=9, color=BLACK_50, fontweight="bold")

    # -- Gain-response plot (starts empty) --
    ax_resp.set_xlim(0, gains[-1] + 2)
    ax_resp.set_ylim(-5, 260)
    ax_resp.set_xlabel("Gain setting", color=BLACK_90, fontsize=9)
    ax_resp.set_ylabel("Echo value (0–252)", color=BLACK_90, fontsize=9)
    ax_resp.set_title("Gain-response curve\n(click a cell to populate)",
                      color=BLACK_90, fontsize=10, fontweight="bold")
    ax_resp.axhline(y=252, color=BLACK_50, lw=0.8, ls=":", alpha=0.7)
    ax_resp.axhline(y=0,   color=BLACK_50, lw=0.8, ls=":", alpha=0.7)
    ax_resp.grid(True, alpha=0.25, color=BLACK_50)
    (resp_line,) = ax_resp.plot([], [], color=GARNET, lw=2, label="Last click")
    ax_resp.legend(fontsize=8, loc="lower right")

    resp_vline = ax_resp.axvline(x=gains[gi0], color=ATLANTIC,
                                 lw=1.2, ls="--", alpha=0.8)

    # -- Gain slider --
    slider = Slider(ax_slid, "Gain", gains[0], gains[-1],
                    valinit=gains[gi0], valstep=1,
                    color=GARNET, track_color=BLACK_10)
    ax_slid.set_facecolor(BLACK_10)

    # -----------------------------------------------------------------------
    # Zoom / pan state
    # -----------------------------------------------------------------------
    ppi_home = (0, PPI_SIZE, PPI_SIZE, 0)  # xlim_lo, xlim_hi, ylim_lo, ylim_hi
    pan_state = {"active": False, "x0": 0.0, "y0": 0.0,
                 "xlim": None, "ylim": None}

    def zoom_ppi(event):
        if event.inaxes is not ax_ppi:
            return
        cur_xlim = ax_ppi.get_xlim()
        cur_ylim = ax_ppi.get_ylim()
        cx, cy = event.xdata, event.ydata

        scale = 0.8 if event.button == "up" else 1.25
        new_w = (cur_xlim[1] - cur_xlim[0]) * scale
        new_h = (cur_ylim[0] - cur_ylim[1]) * scale  # ylim is inverted

        # Keep cursor at same relative position
        rx = (cx - cur_xlim[0]) / (cur_xlim[1] - cur_xlim[0])
        ry = (cy - cur_ylim[1]) / (cur_ylim[0] - cur_ylim[1])

        new_xlim = (cx - rx * new_w, cx + (1 - rx) * new_w)
        new_ylim = (cy + (1 - ry) * new_h, cy - ry * new_h)

        ax_ppi.set_xlim(new_xlim)
        ax_ppi.set_ylim(new_ylim)
        fig.canvas.draw_idle()

    def on_press_pan(event):
        if event.inaxes is not ax_ppi or event.button != 2:
            return
        pan_state["active"] = True
        pan_state["x0"] = event.xdata
        pan_state["y0"] = event.ydata
        pan_state["xlim"] = ax_ppi.get_xlim()
        pan_state["ylim"] = ax_ppi.get_ylim()

    def on_release_pan(event):
        pan_state["active"] = False

    def on_motion_pan(event):
        if not pan_state["active"] or event.inaxes is not ax_ppi:
            return
        if event.xdata is None:
            return
        dx = pan_state["x0"] - event.xdata
        dy = pan_state["y0"] - event.ydata
        ax_ppi.set_xlim(pan_state["xlim"][0] + dx, pan_state["xlim"][1] + dx)
        ax_ppi.set_ylim(pan_state["ylim"][0] + dy, pan_state["ylim"][1] + dy)
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect("scroll_event", zoom_ppi)
    fig.canvas.mpl_connect("button_press_event", on_press_pan)
    fig.canvas.mpl_connect("button_release_event", on_release_pan)
    fig.canvas.mpl_connect("motion_notify_event", on_motion_pan)

    # -----------------------------------------------------------------------
    # Marked targets
    # -----------------------------------------------------------------------
    targets: list[dict] = []
    mark_dots: list = []

    def redraw_marks():
        for d in mark_dots:
            d.remove()
        mark_dots.clear()
        for i, t in enumerate(targets):
            # Convert cell coords back to pixel
            r_frac  = t["range_bin"] / (n_bins - 1)
            a_rad   = np.radians(t["angle_deg"])
            px = half + r_frac * half * np.sin(a_rad)
            py = half - r_frac * half * np.cos(a_rad)
            dot, = ax_ppi.plot(px, py, "o",
                               color=ATLANTIC, ms=7,
                               markeredgecolor=WHITE, markeredgewidth=0.8,
                               zorder=10)
            lbl = ax_ppi.text(px + 6, py - 6, str(i + 1),
                              color=WHITE, fontsize=7, zorder=11)
            mark_dots.extend([dot, lbl])
        fig.canvas.draw_idle()

    def print_targets():
        print(f"\n{'─'*55}")
        print(f"  {'#':>3}  {'angle_deg':>10}  {'range_bin':>10}  {'spoke':>8}")
        print(f"{'─'*55}")
        for i, t in enumerate(targets):
            print(f"  {i+1:>3}  {t['angle_deg']:>10.2f}  "
                  f"{t['range_bin']:>10}  {t['spoke_idx']:>8}")
        print(f"{'─'*55}\n")

    # -----------------------------------------------------------------------
    # Event handlers
    # -----------------------------------------------------------------------

    def update_gain(val):
        gi = int(np.argmin(np.abs(gains - round(val))))
        im.set_data(frames[gi])
        ax_ppi.set_title(f"PPI  —  gain = {gains[gi]}",
                         color=BLACK_90, fontsize=11, fontweight="bold")
        resp_vline.set_xdata([gains[gi]])
        fig.canvas.draw_idle()

    slider.on_changed(update_gain)

    def on_click_ppi(event):
        if event.inaxes is not ax_ppi:
            return
        if event.xdata is None:
            return

        r_bin, spoke, angle = pixel_to_cell(
            event.xdata, event.ydata, n_spokes, n_bins
        )
        if r_bin < 0:
            return

        if event.button == 1:   # left-click → add mark
            # Gain-response curve for this cell
            resp = stack[:, spoke, r_bin].astype(float)
            resp_line.set_data(gains, resp)
            ax_resp.set_title(
                f"Gain-response — bin {r_bin}, spoke {spoke}  ({angle:.1f}°)",
                color=BLACK_90, fontsize=10, fontweight="bold",
            )
            fig.canvas.draw_idle()

            targets.append(dict(
                range_bin=r_bin,
                spoke_idx=spoke,
                angle_deg=round(angle, 2),
            ))
            redraw_marks()
            print_targets()

        elif event.button == 3:  # right-click → remove nearest mark
            if not targets:
                return
            r_frac = r_bin / (n_bins - 1)
            click_a = np.radians(angle)
            click_x = r_frac * np.sin(click_a)
            click_y = r_frac * np.cos(click_a)
            dists = []
            for t in targets:
                tf = t["range_bin"] / (n_bins - 1)
                ta = np.radians(t["angle_deg"])
                dists.append((tf * np.sin(ta) - click_x)**2 +
                             (tf * np.cos(ta) - click_y)**2)
            targets.pop(int(np.argmin(dists)))
            redraw_marks()
            print_targets()

    def on_key(event):
        if event.key == "s":
            TARGETS_FILE.write_text(json.dumps(targets, indent=2))
            print(f"Saved {len(targets)} targets → {TARGETS_FILE}")

        elif event.key == "c":
            targets.clear()
            redraw_marks()
            print("Marks cleared.")

        elif event.key == "h":
            ax_ppi.set_xlim(ppi_home[0], ppi_home[1])
            ax_ppi.set_ylim(ppi_home[2], ppi_home[3])
            fig.canvas.draw_idle()
            print("View reset.")

        elif event.key == "q":
            plt.close("all")

    fig.canvas.mpl_connect("button_press_event", on_click_ppi)
    fig.canvas.mpl_connect("key_press_event", on_key)

    # -----------------------------------------------------------------------
    # Instructions overlay
    # -----------------------------------------------------------------------
    fig.text(
        0.5, 0.97,
        "L-click: mark  |  R-click: remove  |  Scroll: zoom  |  Mid-drag: pan  |  'h': home  |  's': save  |  'c': clear  |  'q': quit",
        ha="center", va="top", fontsize=8.5, color=BLACK_90,
        style="italic",
    )

    plt.show()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interactive HDR radar PPI viewer")
    parser.add_argument(
        "--dir", default=DATA_DIR,
        help="Path to a gain-sweep data directory",
    )
    args = parser.parse_args()
    main(args.dir)
