"""Generate preprocessing-walkthrough figures for the data-cleanup report.

Inputs:  /Volumes/MacShare/DATA/DLR_Datasets/{DAAN,DARC,MANV}_/
Outputs: preprocessing_report/figures/*.png

Figures produced:
    fig1_walkthrough_daan.png     — raw → signal → mask → threshold →
                                    closing → CCs → AIS seeds → matches
    fig2_manv_calibration.png     — DLR-default projection vs fixed
                                    projection on MANV (shows 17-px
                                    polar-origin offset + 2x range-scale)
    fig3_residual_hist.png        — AIS-to-nearest-blob pixel distance,
                                    default-calibration vs fitted-cal.
    fig4_gt_comparison.png        — DLR default (DBSCAN+33x33 pad) boxes
                                    vs AIS-anchored tight boxes on DAAN.
    fig5_dataset_palettes.png     — red-channel vs yellow-HSV target
                                    isolation on DAAN, DARC, MANV crops.
"""
from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.cluster import DBSCAN

from radar_mask import (
    create_radar_mask,
    extract_radar_signal,
    extract_via_red_channel,
    extract_via_yellow_hsv,
    get_calibration,
    DATASET_CALIBRATION,
)
from ais_anchored_gt import (
    parse_frame_annotations,
    split_ais_to_seeds,
    extract_blobs,
    greedy_match,
    polar_to_pixel,
    INTENSITY_THRESHOLD,
    CLOSING_KERNEL,
)

# ──────────────────────────────────────────────────────────────────────
# Paths and style
# ──────────────────────────────────────────────────────────────────────
DLR_ROOT = Path("/Volumes/MacShare/DATA/DLR_Datasets")
OUT      = Path(__file__).resolve().parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

GARNET    = "#73000A"
ROSE      = "#CC2E40"
ATLANTIC  = "#466A9F"
CONGAREE  = "#1F414D"
HORSESHOE = "#65780B"
HONEYCOMB = "#A49137"
BLACK90   = "#363636"
BLACK70   = "#5C5C5C"
BLACK30   = "#C7C7C7"
BLACK10   = "#ECECEC"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": BLACK70,
    "axes.labelcolor": BLACK90,
    "axes.titlecolor": BLACK90,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": BLACK70,
    "ytick.color": BLACK70,
    "savefig.facecolor": "white",
    "savefig.dpi": 160,
})

# ──────────────────────────────────────────────────────────────────────
# Data loading
# ──────────────────────────────────────────────────────────────────────
def load_frame(ds: str, step: int):
    """Return (BGR image, polar entry) for a DLR sub-dataset frame."""
    root = DLR_ROOT / f"{ds}_"
    img = cv2.imread(str(root / "radarImages" / f"{step:03d}.png"))
    with open(root / "polarMeas.json") as f:
        entry = json.load(f).get(str(step))
    return img, entry


def tight_crop(img, center, half=360):
    """Return a square crop centered on the radar disc for readable figures."""
    cx, cy = center
    y0 = max(0, cy - half); y1 = min(img.shape[0], cy + half)
    x0 = max(0, cx - half); x1 = min(img.shape[1], cx + half)
    return img[y0:y1, x0:x1], (x0, y0)


def draw_box(ax, x1, y1, x2, y2, color, lw=1.3, offset=(0, 0)):
    ox, oy = offset
    ax.add_patch(mpatches.Rectangle(
        (x1 - ox, y1 - oy), x2 - x1, y2 - y1,
        fill=False, edgecolor=color, linewidth=lw))


def style_ax(ax, title=""):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    if title:
        ax.set_title(title, color=BLACK90, fontsize=10)


# ──────────────────────────────────────────────────────────────────────
# Figure 1 — eight-panel walkthrough on one DAAN frame
# ──────────────────────────────────────────────────────────────────────
def fig1_walkthrough(ds="DAAN", step=51):
    print(f"[fig1] building walkthrough on {ds} step {step}")
    bgr, entry = load_frame(ds, step)
    cal = get_calibration(ds)
    cx, cy = cal["cx"], cal["cy"]

    # Crop region for readability (1050x1024 → 720x720 centered)
    crop_bgr, origin = tight_crop(bgr, (cx, cy), half=360)

    # Step 1 — raw
    raw_rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)

    # Step 2 — red-channel target isolation
    signal_full = extract_radar_signal(bgr, dataset=ds)
    signal_crop = signal_full[origin[1]:origin[1]+crop_bgr.shape[0],
                              origin[0]:origin[0]+crop_bgr.shape[1]]

    # Step 3 — circular PPI mask applied
    mask = create_radar_mask(bgr.shape[0], bgr.shape[1])
    masked_full = cv2.bitwise_and(signal_full, mask)
    masked_crop = masked_full[origin[1]:origin[1]+crop_bgr.shape[0],
                              origin[0]:origin[0]+crop_bgr.shape[1]]

    # Step 4 — binary threshold
    binary = (masked_full > INTENSITY_THRESHOLD).astype(np.uint8) * 255
    binary_crop = binary[origin[1]:origin[1]+crop_bgr.shape[0],
                         origin[0]:origin[0]+crop_bgr.shape[1]]

    # Step 5 — morphological closing
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, CLOSING_KERNEL)
    closed = cv2.morphologyEx((binary//255).astype(np.uint8),
                              cv2.MORPH_CLOSE, kernel) * 255
    closed_crop = closed[origin[1]:origin[1]+crop_bgr.shape[0],
                         origin[0]:origin[0]+crop_bgr.shape[1]]

    # Step 6 — connected components (colour by label)
    n_lbl, labels_full, stats, cents = cv2.connectedComponentsWithStats(
        (closed // 255).astype(np.uint8), connectivity=8)
    # Colour map for CCs — cycle through brand palette; background stays black
    palette = [(0, 0, 0)] + [tuple(int(c, 16) for c in
                (ROSE[1:3], ROSE[3:5], ROSE[5:7]))] * 0  # placeholder
    # Build a colour LUT of n_lbl entries
    rng = np.random.default_rng(7)
    lut = rng.integers(60, 240, size=(n_lbl, 3), dtype=np.uint8)
    lut[0] = (0, 0, 0)
    cc_vis_full = lut[labels_full]
    cc_vis_crop = cc_vis_full[origin[1]:origin[1]+crop_bgr.shape[0],
                              origin[0]:origin[0]+crop_bgr.shape[1]]

    # Step 7 — AIS seeds projected onto raw image
    objs  = parse_frame_annotations(entry or [])
    seeds = split_ais_to_seeds(
        objs, cx=cal["cx"], cy=cal["cy"],
        r_px_max=cal["r_px_max"], max_range_m=cal["max_range_m"])

    # Step 8 — greedy match → tight boxes
    blobs = extract_blobs(bgr, radar_mask=mask, dataset=ds)
    match = greedy_match(seeds, blobs)

    # --- Plot ---------------------------------------------------------
    fig, axes = plt.subplots(2, 4, figsize=(13.2, 7.0), facecolor="white")
    [ax1, ax2, ax3, ax4], [ax5, ax6, ax7, ax8] = axes

    ax1.imshow(raw_rgb)
    style_ax(ax1, "1. Raw PPI frame (BGR)")

    ax2.imshow(signal_crop, cmap="gray", vmin=0, vmax=255)
    style_ax(ax2, "2. Per-dataset target\nisolation (red channel)")

    ax3.imshow(masked_crop, cmap="gray", vmin=0, vmax=255)
    style_ax(ax3, "3. Circular PPI mask\napplied")

    ax4.imshow(binary_crop, cmap="gray")
    style_ax(ax4, f"4. Threshold  I > {INTENSITY_THRESHOLD}")

    ax5.imshow(closed_crop, cmap="gray")
    style_ax(ax5, "5. Morphological closing\n(5×5 ellipse)")

    ax6.imshow(cc_vis_crop)
    style_ax(ax6, f"6. Connected components\n(n = {n_lbl - 1}, filtered by area)")

    # Panel 7: AIS seeds (garnet dots on raw)
    ax7.imshow(raw_rgb)
    for s in seeds:
        sx, sy = s.centroid_px
        ax7.plot(sx - origin[0], sy - origin[1], 'o',
                 color=GARNET, markersize=7, markeredgecolor="white",
                 markeredgewidth=1.2)
    style_ax(ax7, f"7. AIS seeds projected\n(n = {len(seeds)}, garnet)")

    # Panel 8: matched boxes (garnet = matched, atlantic = unmatched blob)
    ax8.imshow(raw_rgb)
    for seed, blob in match.matched:
        draw_box(ax8, blob.x1, blob.y1, blob.x2, blob.y2,
                 GARNET, lw=1.6, offset=origin)
    for b in match.unclaimed_blobs:
        draw_box(ax8, b.x1, b.y1, b.x2, b.y2,
                 ATLANTIC, lw=0.9, offset=origin)
    style_ax(ax8,
             f"8. Greedy match → GT\n"
             f"({len(match.matched)} matched, {len(match.unclaimed_blobs)} unclaimed)")

    fig.suptitle(
        f"Preprocessing pipeline walkthrough — {ds} frame {step:03d}",
        color=BLACK90, fontsize=12, fontweight="bold", y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUT / "fig1_walkthrough_daan.png", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Figure 2 — DLR-default projection vs fitted projection on MANV
# ──────────────────────────────────────────────────────────────────────
# DLR default (from visualize_bbox.py):
DLR_DEFAULT = {
    "cx_factor": 0.5,      # img_w/2
    "cy_factor": 0.5,      # img_h/2
    "r_factor":  0.46,     # min(w,h)/2 * 0.92 = 0.46 * min
    "max_range_m": 6000.0,
}

def _dlr_default_project(r, th, img_w, img_h):
    cx = img_w * 0.5; cy = img_h * 0.5
    r_px_max = min(img_w, img_h) * 0.46
    r_px = (r / 6000.0) * r_px_max
    return cx + r_px * np.sin(th), cy - r_px * np.cos(th)


def fig2_manv_calibration(step=100):
    print(f"[fig2] building MANV calibration comparison on step {step}")
    ds = "MANV"
    bgr, entry = load_frame(ds, step)
    cal = get_calibration(ds)
    h, w = bgr.shape[:2]

    objs = parse_frame_annotations(entry or [])
    # DLR default seeds
    default_seeds = []
    for o in objs:
        if not o.points_polar:
            continue
        xs, ys = [], []
        for r, th in o.points_polar:
            x, y = _dlr_default_project(r, th, w, h)
            xs.append(x); ys.append(y)
        default_seeds.append((float(np.mean(xs)), float(np.mean(ys))))

    fitted_seeds = split_ais_to_seeds(
        objs, cx=cal["cx"], cy=cal["cy"],
        r_px_max=cal["r_px_max"], max_range_m=cal["max_range_m"])

    crop_bgr, origin = tight_crop(bgr, (cal["cx"], cal["cy"]), half=380)
    raw_rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.8), facecolor="white")
    ax_d, ax_f = axes
    for ax in axes:
        ax.imshow(raw_rgb)
        style_ax(ax)

    for sx, sy in default_seeds:
        ax_d.plot(sx - origin[0], sy - origin[1], 'o',
                  color=ROSE, markersize=9, markeredgecolor="white",
                  markeredgewidth=1.2)
    for s in fitted_seeds:
        sx, sy = s.centroid_px
        ax_f.plot(sx - origin[0], sy - origin[1], 'o',
                  color=GARNET, markersize=9, markeredgecolor="white",
                  markeredgewidth=1.2)

    ax_d.set_title(
        "(a) DLR default projection\n"
        "cx,cy = (w/2, h/2),  max_range = 6000 m",
        color=BLACK90, fontsize=10)
    ax_f.set_title(
        f"(b) Fitted MANV calibration\n"
        f"cx,cy = ({cal['cx']}, {cal['cy']}),  max_range = {int(cal['max_range_m'])} m",
        color=BLACK90, fontsize=10)

    fig.suptitle(
        f"MANV polar-origin + range-scale calibration — frame {step:03d}",
        color=BLACK90, fontsize=12, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT / "fig2_manv_calibration.png", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Figure 3 — residual histogram (AIS→blob pixel distance)
# ──────────────────────────────────────────────────────────────────────
def _frame_residuals(ds, step, mask, *, default=False):
    bgr, entry = load_frame(ds, step)
    if bgr is None or entry is None:
        return []
    h, w = bgr.shape[:2]
    blobs = extract_blobs(bgr, radar_mask=mask, dataset=ds)
    if not blobs:
        return []
    bxy = np.array([[b.cx, b.cy] for b in blobs])

    objs = parse_frame_annotations(entry or [])
    seeds_xy = []
    if default:
        for o in objs:
            if not o.points_polar:
                continue
            xs, ys = [], []
            for r, th in o.points_polar:
                x, y = _dlr_default_project(r, th, w, h)
                xs.append(x); ys.append(y)
            seeds_xy.append((float(np.mean(xs)), float(np.mean(ys))))
    else:
        cal = get_calibration(ds)
        ss = split_ais_to_seeds(
            objs, cx=cal["cx"], cy=cal["cy"],
            r_px_max=cal["r_px_max"], max_range_m=cal["max_range_m"])
        seeds_xy = [s.centroid_px for s in ss]

    if not seeds_xy:
        return []
    sxy = np.array(seeds_xy)
    # nearest blob for each seed
    d = np.sqrt(((sxy[:, None, :] - bxy[None, :, :]) ** 2).sum(-1)).min(1)
    return d.tolist()


def fig3_residual_hist(datasets=("DAAN", "DARC", "MANV"), sample_step=20):
    print("[fig3] building residual histogram")
    mask = create_radar_mask(1024, 1050)
    rows = []
    for ds in datasets:
        img_dir = DLR_ROOT / f"{ds}_" / "radarImages"
        steps = sorted(int(p.stem) for p in img_dir.glob("*.png")
                       if not p.name.startswith("._"))
        steps = steps[::max(1, len(steps) // sample_step)]   # ~sample_step frames
        for step in steps:
            for v in _frame_residuals(ds, step, mask, default=True):
                rows.append((ds, "default", v))
            for v in _frame_residuals(ds, step, mask, default=False):
                rows.append((ds, "fitted", v))

    fig, axes = plt.subplots(1, 3, figsize=(13.5, 3.8), facecolor="white",
                             sharey=True)
    for ax, ds in zip(axes, datasets):
        dvals = [v for d, k, v in rows if d == ds and k == "default"]
        fvals = [v for d, k, v in rows if d == ds and k == "fitted"]
        bins = np.arange(0, 121, 3)
        ax.hist(dvals, bins=bins, color=ROSE, alpha=0.55, label="DLR default",
                edgecolor=ROSE, linewidth=0.4)
        ax.hist(fvals, bins=bins, color=GARNET, alpha=0.75, label="fitted",
                edgecolor=GARNET, linewidth=0.4)
        ax.axvline(np.median(dvals) if dvals else 0, color=ROSE, ls="--",
                   lw=1.0)
        ax.axvline(np.median(fvals) if fvals else 0, color=GARNET, ls="--",
                   lw=1.0)
        ax.set_title(
            f"{ds}  —  median: "
            f"{np.median(dvals):.0f} → {np.median(fvals):.0f} px",
            color=BLACK90, fontsize=11)
        ax.set_xlabel("AIS seed to nearest blob (px)")
        if ds == datasets[0]:
            ax.set_ylabel("count (sampled frames)")
        ax.legend(frameon=False, fontsize=8)

    fig.suptitle(
        "AIS-seed → image-blob pixel residual: DLR default vs fitted calibration",
        color=BLACK90, fontsize=12, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(OUT / "fig3_residual_hist.png", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Figure 4 — DLR default 33×33 padded boxes vs AIS-anchored tight boxes
# ──────────────────────────────────────────────────────────────────────
def _dlr_default_boxes(entry, img_w, img_h, pad=15):
    """Port of the DLR visualize_bbox.py DBSCAN+pad logic, in pixel space."""
    detections = (entry or [])[2:]  # skip [own?, heading]
    pts = [p for p in detections if isinstance(p, list)]
    if len(pts) < 5:
        return []
    r = np.array([p[0] for p in pts])
    th = np.array([p[1] for p in pts])
    # Cluster in Cartesian metres to match DLR script
    xm = r * np.sin(th); ym = r * np.cos(th)
    coords = np.column_stack([xm, ym])
    labels = DBSCAN(eps=200, min_samples=5).fit(coords).labels_

    boxes = []
    for lbl in set(labels):
        if lbl == -1:
            continue
        mask_l = labels == lbl
        px, py = _dlr_default_project(r[mask_l], th[mask_l], img_w, img_h)
        x1 = px.min() - pad; x2 = px.max() + pad
        y1 = py.min() - pad; y2 = py.max() + pad
        boxes.append((x1, y1, x2, y2))
    return boxes


def fig4_gt_comparison(ds="DAAN", step=51):
    print(f"[fig4] building GT comparison on {ds} step {step}")
    bgr, entry = load_frame(ds, step)
    cal = get_calibration(ds)
    h, w = bgr.shape[:2]
    mask = create_radar_mask(h, w)

    # DLR default boxes
    default_boxes = _dlr_default_boxes(entry, w, h, pad=15)

    # Ours
    objs  = parse_frame_annotations(entry or [])
    seeds = split_ais_to_seeds(
        objs, cx=cal["cx"], cy=cal["cy"],
        r_px_max=cal["r_px_max"], max_range_m=cal["max_range_m"])
    blobs = extract_blobs(bgr, radar_mask=mask, dataset=ds)
    match = greedy_match(seeds, blobs)

    crop_bgr, origin = tight_crop(bgr, (cal["cx"], cal["cy"]), half=380)
    raw_rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)

    # Stats
    dsz = [(x2 - x1, y2 - y1) for (x1, y1, x2, y2) in default_boxes]
    osz = [(b.x2 - b.x1, b.y2 - b.y1) for _, b in match.matched]

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.8), facecolor="white")
    for ax in axes:
        ax.imshow(raw_rgb); style_ax(ax)

    for (x1, y1, x2, y2) in default_boxes:
        draw_box(axes[0], x1, y1, x2, y2, ROSE, lw=1.6, offset=origin)
    for _, b in match.matched:
        draw_box(axes[1], b.x1, b.y1, b.x2, b.y2, GARNET, lw=1.6,
                 offset=origin)

    def fmt(szs):
        if not szs:
            return "n = 0"
        ws = [s[0] for s in szs]; hs = [s[1] for s in szs]
        return (f"n = {len(szs)}  |  median w×h = "
                f"{int(np.median(ws))}×{int(np.median(hs))} px")

    axes[0].set_title("(a) DLR default  —  DBSCAN + 15-px pad\n" + fmt(dsz),
                      color=BLACK90, fontsize=10)
    axes[1].set_title("(b) AIS-anchored, image-grounded\n" + fmt(osz),
                      color=BLACK90, fontsize=10)

    fig.suptitle(
        f"Bounding-box geometry — {ds} frame {step:03d}",
        color=BLACK90, fontsize=12, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT / "fig4_gt_comparison.png", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Figure 5 — palette comparison (red-channel vs yellow-HSV)
# ──────────────────────────────────────────────────────────────────────
def fig5_palette(samples=(("DAAN", 100), ("DARC", 100), ("MANV", 100))):
    print("[fig5] building palette comparison")
    fig, axes = plt.subplots(len(samples), 3, figsize=(11.2, 3.5 * len(samples)),
                             facecolor="white")
    for i, (ds, step) in enumerate(samples):
        bgr, _ = load_frame(ds, step)
        cal = get_calibration(ds)
        crop_bgr, origin = tight_crop(bgr, (cal["cx"], cal["cy"]), half=300)
        raw_rgb  = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)
        red      = extract_via_red_channel(crop_bgr)
        yellow   = extract_via_yellow_hsv(crop_bgr)

        axes[i, 0].imshow(raw_rgb)
        axes[i, 1].imshow(red, cmap="gray", vmin=0, vmax=255)
        axes[i, 2].imshow(yellow, cmap="gray", vmin=0, vmax=255)
        style_ax(axes[i, 0], f"{ds}  —  raw BGR")
        style_ax(axes[i, 1], "red channel")
        style_ax(axes[i, 2], "yellow-HSV filter")

    fig.suptitle(
        "Per-dataset target-signal isolation",
        color=BLACK90, fontsize=12, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUT / "fig5_palette.png", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    fig1_walkthrough(ds="DAAN", step=51)
    fig2_manv_calibration(step=100)
    fig3_residual_hist()
    fig4_gt_comparison(ds="DAAN", step=51)
    fig5_palette()
    print("done.  figures in", OUT)
