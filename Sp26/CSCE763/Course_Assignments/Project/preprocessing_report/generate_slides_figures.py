"""Stage-by-stage preprocessing figures for the walkthrough slide deck.

Each figure is tailored to one slide panel. Filenames prefixed with
``slide_`` so they do not collide with the report figures in figures/.

Outputs: preprocessing_report/figures/slide_*.png
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
from matplotlib.patches import FancyArrowPatch, Circle
from sklearn.cluster import DBSCAN

from radar_mask import (
    create_radar_mask,
    apply_radar_mask,
    extract_radar_signal,
    extract_via_red_channel,
    extract_via_yellow_hsv,
    get_calibration,
    DATASET_CALIBRATION,
    DEFAULT_CENTER_X, DEFAULT_CENTER_Y, DEFAULT_RADIUS,
)
from ais_anchored_gt import (
    parse_frame_annotations,
    split_ais_to_seeds,
    extract_blobs,
    greedy_match,
    polar_to_pixel,
    INTENSITY_THRESHOLD,
    CLOSING_KERNEL,
    MIN_BLOB_AREA, MAX_BLOB_AREA,
    MATCH_RADIUS_PX,
)

# ── Paths ────────────────────────────────────────────────────────────
DLR_ROOT = Path("/Volumes/MacShare/DATA/DLR_Datasets")
OUT      = Path(__file__).resolve().parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ── Brand colors ─────────────────────────────────────────────────────
GARNET    = "#73000A"
ROSE      = "#CC2E40"
ATLANTIC  = "#466A9F"
CONGAREE  = "#1F414D"
HORSESHOE = "#65780B"
HONEYCOMB = "#A49137"
WARM      = "#676156"
SAND      = "#FFF2E3"
BLACK90   = "#363636"
BLACK70   = "#5C5C5C"
BLACK50   = "#A2A2A2"
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

DATASETS = ("DAAN", "DARC", "MANV")
# Frames to use per dataset (denser targets).
FRAMES   = {"DAAN": 51, "DARC": 100, "MANV": 100}


# ── helpers ──────────────────────────────────────────────────────────
def load_frame(ds: str, step: int):
    root = DLR_ROOT / f"{ds}_"
    img = cv2.imread(str(root / "radarImages" / f"{step:03d}.png"))
    with open(root / "polarMeas.json") as f:
        entry = json.load(f).get(str(step))
    return img, entry


def tight_crop(img, center, half=360):
    cx, cy = center
    y0 = max(0, cy - half); y1 = min(img.shape[0], cy + half)
    x0 = max(0, cx - half); x1 = min(img.shape[1], cx + half)
    return img[y0:y1, x0:x1], (x0, y0)


def style_ax(ax, title="", fontsize=10):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    if title:
        ax.set_title(title, color=BLACK90, fontsize=fontsize)


def draw_box(ax, x1, y1, x2, y2, color, lw=1.3, offset=(0, 0)):
    ox, oy = offset
    ax.add_patch(mpatches.Rectangle(
        (x1 - ox, y1 - oy), x2 - x1, y2 - y1,
        fill=False, edgecolor=color, linewidth=lw))


def _dlr_default_project(r, th, img_w, img_h):
    cx = img_w * 0.5; cy = img_h * 0.5
    r_px_max = min(img_w, img_h) * 0.46
    r_px = (np.asarray(r) / 6000.0) * r_px_max
    return cx + r_px * np.sin(th), cy - r_px * np.cos(th)


def _dlr_default_boxes(entry, img_w, img_h, pad=15):
    detections = (entry or [])[2:]
    pts = [p for p in detections if isinstance(p, list)]
    if len(pts) < 5:
        return []
    r  = np.array([p[0] for p in pts])
    th = np.array([p[1] for p in pts])
    xm = r * np.sin(th); ym = r * np.cos(th)
    coords = np.column_stack([xm, ym])
    labels = DBSCAN(eps=200, min_samples=5).fit(coords).labels_
    boxes = []
    for lbl in set(labels):
        if lbl == -1:
            continue
        m = labels == lbl
        px, py = _dlr_default_project(r[m], th[m], img_w, img_h)
        boxes.append((px.min() - pad, py.min() - pad,
                      px.max() + pad, py.max() + pad))
    return boxes


# ──────────────────────────────────────────────────────────────────────
# Slide 01 — raw trio: one frame from each dataset
# ──────────────────────────────────────────────────────────────────────
def slide01_raw_trio():
    print("[s01] raw trio")
    fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.4), facecolor="white")
    for ax, ds in zip(axes, DATASETS):
        bgr, _ = load_frame(ds, FRAMES[ds])
        cal = get_calibration(ds)
        crop, _ = tight_crop(bgr, (cal["cx"], cal["cy"]), half=360)
        ax.imshow(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
        res = cal["resolution"]
        style_ax(ax, f"{ds}   —   {res:.1f} m/px   —   max range {cal['max_range_m']/1000:.1f} km",
                 fontsize=11)
    fig.suptitle(
        "Three sub-datasets, three display palettes",
        color=BLACK90, fontsize=12, fontweight="bold", y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT / "slide_01_raw_trio.png", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Slide 02 — color isolation per dataset (3 × 3)
# ──────────────────────────────────────────────────────────────────────
def slide02_color_isolation():
    print("[s02] per-dataset color isolation")
    fig, axes = plt.subplots(3, 3, figsize=(11.4, 10.0), facecolor="white")
    header = ["raw BGR", "red-channel extractor", "yellow-HSV extractor"]
    for j, h in enumerate(header):
        axes[0, j].set_title(h, color=BLACK90, fontsize=11, pad=8,
                             fontweight="bold")
    for i, ds in enumerate(DATASETS):
        bgr, _ = load_frame(ds, FRAMES[ds])
        cal = get_calibration(ds)
        crop, _ = tight_crop(bgr, (cal["cx"], cal["cy"]), half=300)
        red    = extract_via_red_channel(crop)
        yellow = extract_via_yellow_hsv(crop)
        axes[i, 0].imshow(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
        axes[i, 1].imshow(red,    cmap="gray", vmin=0, vmax=255)
        axes[i, 2].imshow(yellow, cmap="gray", vmin=0, vmax=255)
        style_ax(axes[i, 0]); style_ax(axes[i, 1]); style_ax(axes[i, 2])
        axes[i, 0].set_ylabel(ds, color=GARNET, fontsize=13,
                              fontweight="bold", rotation=0, labelpad=26,
                              va="center")
        # highlight the chosen extractor per row
        chosen_col = 1 if ds in ("DAAN", "DARC") else 2
        for s in axes[i, chosen_col].spines.values():
            s.set_visible(True)
            s.set_edgecolor(GARNET)
            s.set_linewidth(2.2)
    fig.text(0.5, 0.02,
             "DAAN / DARC → red channel (R is high only on near-white targets).   "
             "MANV → yellow-HSV (white UI has zero saturation; yellow targets pass).",
             ha="center", color=BLACK70, fontsize=9)
    fig.suptitle(
        "Step 1:  per-dataset target-signal isolation",
        color=BLACK90, fontsize=12, fontweight="bold", y=0.995)
    fig.tight_layout(rect=[0, 0.04, 1, 0.96])
    fig.savefig(OUT / "slide_02_color_isolation.png", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Slide 03 — circular PPI mask (raw + mask outline + masked signal)
# ──────────────────────────────────────────────────────────────────────
def slide03_ppi_mask(ds="DAAN"):
    print("[s03] PPI mask application")
    bgr, _ = load_frame(ds, FRAMES[ds])
    cal = get_calibration(ds)
    mask = create_radar_mask(bgr.shape[0], bgr.shape[1])
    signal = extract_radar_signal(bgr, dataset=ds)
    masked = cv2.bitwise_and(signal, mask)

    # Full images (no crop; we want to see the disc edge)
    fig, axes = plt.subplots(1, 3, figsize=(13.0, 4.7), facecolor="white")
    axes[0].imshow(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    # mask overlay
    axes[1].imshow(signal, cmap="gray", vmin=0, vmax=255)
    axes[1].add_patch(Circle((DEFAULT_CENTER_X, DEFAULT_CENTER_Y),
                             DEFAULT_RADIUS, fill=False,
                             edgecolor=GARNET, linewidth=2.0))
    axes[2].imshow(masked, cmap="gray", vmin=0, vmax=255)

    style_ax(axes[0], "(a) raw PPI frame", fontsize=11)
    style_ax(axes[1],
             f"(b) signal + disc outline  (c={DEFAULT_CENTER_X},{DEFAULT_CENTER_Y};  r={DEFAULT_RADIUS}\u00a0px)",
             fontsize=11)
    style_ax(axes[2], "(c) signal bitwise-AND mask", fontsize=11)
    fig.suptitle("Step 2:  circular PPI mask removes off-disc UI chrome",
                 color=BLACK90, fontsize=12, fontweight="bold", y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT / "slide_03_ppi_mask.png", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Slide 04 — threshold + morphological closing (zoomed)
# ──────────────────────────────────────────────────────────────────────
def slide04_threshold_morph(ds="DAAN"):
    print("[s04] threshold + closing")
    bgr, _ = load_frame(ds, FRAMES[ds])
    cal = get_calibration(ds)
    mask = create_radar_mask(bgr.shape[0], bgr.shape[1])
    signal = cv2.bitwise_and(extract_radar_signal(bgr, dataset=ds), mask)
    binary = (signal > INTENSITY_THRESHOLD).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, CLOSING_KERNEL)
    closed = cv2.morphologyEx((binary//255).astype(np.uint8),
                              cv2.MORPH_CLOSE, kernel) * 255

    crop_sig, org = tight_crop(signal, (cal["cx"], cal["cy"]), half=180)
    crop_bin     = binary[org[1]:org[1]+crop_sig.shape[0],
                          org[0]:org[0]+crop_sig.shape[1]]
    crop_close   = closed[org[1]:org[1]+crop_sig.shape[0],
                          org[0]:org[0]+crop_sig.shape[1]]

    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.4), facecolor="white")
    axes[0].imshow(crop_sig,   cmap="gray", vmin=0, vmax=255)
    axes[1].imshow(crop_bin,   cmap="gray")
    axes[2].imshow(crop_close, cmap="gray")
    style_ax(axes[0], "(a) masked signal",                       fontsize=11)
    style_ax(axes[1], f"(b) threshold  I > {INTENSITY_THRESHOLD}", fontsize=11)
    style_ax(axes[2], "(c) closing  5\u00d75 ellipse",             fontsize=11)
    fig.suptitle(
        "Step 3:  binarise, then close 1-2-pixel fragmentation gaps",
        color=BLACK90, fontsize=12, fontweight="bold", y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT / "slide_04_threshold_morph.png", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Slide 05 — connected components + area filter
# ──────────────────────────────────────────────────────────────────────
def slide05_cc_filter(ds="DAAN"):
    print("[s05] connected components + area filter")
    bgr, _ = load_frame(ds, FRAMES[ds])
    cal = get_calibration(ds)
    mask = create_radar_mask(bgr.shape[0], bgr.shape[1])
    signal = cv2.bitwise_and(extract_radar_signal(bgr, dataset=ds), mask)
    binary = (signal > INTENSITY_THRESHOLD).astype(np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, CLOSING_KERNEL)
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    n_lbl, labels, stats, _ = cv2.connectedComponentsWithStats(
        closed, connectivity=8)

    rng = np.random.default_rng(11)
    lut_all = rng.integers(60, 240, size=(n_lbl, 3), dtype=np.uint8)
    lut_all[0] = (0, 0, 0)
    vis_all = lut_all[labels]

    keep = np.ones(n_lbl, dtype=bool)
    keep[0] = False
    for i in range(1, n_lbl):
        area = stats[i, cv2.CC_STAT_AREA]
        if area < MIN_BLOB_AREA or area > MAX_BLOB_AREA:
            keep[i] = False
    lut_keep = lut_all.copy()
    lut_keep[~keep] = (30, 30, 30)
    vis_keep = lut_keep[labels]

    crop_close, org = tight_crop(closed*255, (cal["cx"], cal["cy"]), half=360)
    vis_all_c  = vis_all[org[1]:org[1]+crop_close.shape[0],
                         org[0]:org[0]+crop_close.shape[1]]
    vis_keep_c = vis_keep[org[1]:org[1]+crop_close.shape[0],
                          org[0]:org[0]+crop_close.shape[1]]

    n_kept = int(keep.sum())
    fig, axes = plt.subplots(1, 3, figsize=(12.8, 4.6), facecolor="white")
    axes[0].imshow(crop_close, cmap="gray")
    axes[1].imshow(vis_all_c)
    axes[2].imshow(vis_keep_c)
    style_ax(axes[0], "(a) closed binary mask",                            fontsize=11)
    style_ax(axes[1], f"(b) connected components  (n\u2009=\u2009{n_lbl-1})", fontsize=11)
    style_ax(axes[2], f"(c) area filter  [{MIN_BLOB_AREA},{MAX_BLOB_AREA}] px  (n\u2009=\u2009{n_kept})",
             fontsize=11)
    fig.suptitle(
        "Step 4:  label connected components and drop speckle / ring artefacts",
        color=BLACK90, fontsize=12, fontweight="bold", y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT / "slide_05_cc_filter.png", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Slide 06 — DLR default polar-origin bias (MANV, most dramatic)
# ──────────────────────────────────────────────────────────────────────
def slide06_polar_bias(ds="MANV", step=100):
    print("[s06] polar-origin bias")
    bgr, entry = load_frame(ds, step)
    cal = get_calibration(ds)
    h, w = bgr.shape[:2]
    objs = parse_frame_annotations(entry or [])

    default_seeds, fitted_seeds = [], []
    for o in objs:
        if not o.points_polar:
            continue
        rs = np.array([p[0] for p in o.points_polar])
        ths = np.array([p[1] for p in o.points_polar])
        dx, dy = _dlr_default_project(rs, ths, w, h)
        default_seeds.append((dx.mean(), dy.mean()))
        fx = cal["cx"] + (rs/cal["max_range_m"])*cal["r_px_max"]*np.sin(ths)
        fy = cal["cy"] - (rs/cal["max_range_m"])*cal["r_px_max"]*np.cos(ths)
        fitted_seeds.append((fx.mean(), fy.mean()))

    crop, org = tight_crop(bgr, (cal["cx"], cal["cy"]), half=360)
    rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)

    fig, axes = plt.subplots(1, 2, figsize=(11.6, 5.8), facecolor="white")
    for ax in axes:
        ax.imshow(rgb); style_ax(ax)

    for (sx, sy) in default_seeds:
        axes[0].plot(sx - org[0], sy - org[1], "o",
                     color=ROSE, markersize=10, markeredgecolor="white",
                     markeredgewidth=1.4)
    for (sx, sy) in fitted_seeds:
        axes[1].plot(sx - org[0], sy - org[1], "o",
                     color=GARNET, markersize=10, markeredgecolor="white",
                     markeredgewidth=1.4)

    axes[0].set_title(
        "(a) DLR default  —  c=(w/2, h/2),  max_range = 6000 m\n"
        "AIS seeds land off-target (radial + angular error)",
        color=BLACK90, fontsize=10)
    axes[1].set_title(
        f"(b) Per-dataset calibration  —  c=({cal['cx']}, {cal['cy']}),  max_range = {int(cal['max_range_m'])} m\n"
        "AIS seeds sit on top of the radar returns",
        color=BLACK90, fontsize=10)
    fig.suptitle(
        f"The two DLR bugs in one figure ({ds} frame {step:03d}):  17-px polar-origin bias + 2\u00d7 MANV range",
        color=BLACK90, fontsize=12, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(OUT / "slide_06_polar_bias.png", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Slide 07 — per-dataset calibration table as a visual schematic
# ──────────────────────────────────────────────────────────────────────
def slide07_calibration_schematic():
    print("[s07] calibration schematic")
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.8), facecolor="white")
    for ax, ds in zip(axes, DATASETS):
        bgr, _ = load_frame(ds, FRAMES[ds])
        cal = get_calibration(ds)
        ax.imshow(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
        # visual disc (from defaults)
        ax.add_patch(Circle((DEFAULT_CENTER_X, DEFAULT_CENTER_Y),
                            DEFAULT_RADIUS, fill=False,
                            edgecolor=ATLANTIC, linewidth=1.4,
                            linestyle="--"))
        # polar origin marker
        ax.plot(cal["cx"], cal["cy"], "x", color=GARNET,
                markersize=14, markeredgewidth=2.8)
        # visual center marker
        ax.plot(DEFAULT_CENTER_X, DEFAULT_CENTER_Y, "+",
                color=ATLANTIC, markersize=14, markeredgewidth=2.6)
        dx = cal["cx"] - DEFAULT_CENTER_X
        dy = cal["cy"] - DEFAULT_CENTER_Y
        d  = float(np.hypot(dx, dy))
        style_ax(ax,
            f"{ds}\n"
            f"c_polar = ({cal['cx']}, {cal['cy']}),  c_visual = ({DEFAULT_CENTER_X}, {DEFAULT_CENTER_Y})\n"
            f"offset = {d:.1f}\u00a0px    max_range = {int(cal['max_range_m'])}\u00a0m    res = {cal['resolution']:.2f}\u00a0m/px",
            fontsize=9)
        # Legend once (leftmost)
    handles = [
        plt.Line2D([0], [0], marker="+", color=ATLANTIC, linestyle="",
                   markersize=12, markeredgewidth=2.6, label="visual PPI centre"),
        plt.Line2D([0], [0], marker="x", color=GARNET, linestyle="",
                   markersize=12, markeredgewidth=2.6, label="fitted polar origin"),
        plt.Line2D([0], [0], color=ATLANTIC, linestyle="--", linewidth=1.4,
                   label="visual PPI disc"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False,
               fontsize=10, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle(
        "Per-dataset calibration:  visual centre \u2260 polar origin; MANV has half the range",
        color=BLACK90, fontsize=12, fontweight="bold", y=0.99)
    fig.tight_layout(rect=[0, 0.03, 1, 0.93])
    fig.savefig(OUT / "slide_07_calibration_schematic.png", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Slide 08 — AIS polar point cloud + DBSCAN clusters + pixel seeds
# ──────────────────────────────────────────────────────────────────────
def slide08_dbscan_seeds(ds="DAAN", step=51):
    print("[s08] polar DBSCAN seed splitting")
    bgr, entry = load_frame(ds, step)
    cal = get_calibration(ds)
    objs = parse_frame_annotations(entry or [])

    # collect all AIS points (per object)
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.6), facecolor="white")

    # (a) polar scatter coloured by DBSCAN label within each AIS object
    ax = axes[0]
    ax.set_facecolor("white")
    ax.set_aspect("equal")
    palette = [GARNET, ROSE, ATLANTIC, HORSESHOE, HONEYCOMB, CONGAREE, WARM]
    noise_color = BLACK30
    for oi, o in enumerate(objs):
        if not o.points_polar:
            continue
        rs  = np.array([p[0] for p in o.points_polar])
        ths = np.array([p[1] for p in o.points_polar])
        # clustering in Cartesian metres
        xm = rs * np.sin(ths); ym = rs * np.cos(ths)
        if len(xm) < 5:
            ax.scatter(xm, ym, s=14, color=palette[oi % len(palette)],
                       alpha=0.8, edgecolor="white", linewidth=0.4)
            continue
        labels = DBSCAN(eps=200, min_samples=5).fit(
            np.column_stack([xm, ym])).labels_
        for lbl in sorted(set(labels)):
            m = labels == lbl
            c = noise_color if lbl == -1 else palette[(oi + lbl) % len(palette)]
            ax.scatter(xm[m], ym[m], s=14, color=c, alpha=0.85,
                       edgecolor="white", linewidth=0.4)
    ax.axhline(0, color=BLACK30, lw=0.6)
    ax.axvline(0, color=BLACK30, lw=0.6)
    ax.set_xlabel("x [m]  (east)")
    ax.set_ylabel("y [m]  (north)")
    ax.set_title(
        "(a) AIS polar points, DBSCAN (eps = 200\u00a0m, min = 5)",
        color=BLACK90, fontsize=11)

    # (b) resulting seeds projected into pixel space
    crop, org = tight_crop(bgr, (cal["cx"], cal["cy"]), half=360)
    axes[1].imshow(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    seeds = split_ais_to_seeds(
        objs, cx=cal["cx"], cy=cal["cy"],
        r_px_max=cal["r_px_max"], max_range_m=cal["max_range_m"])
    for s in seeds:
        sx, sy = s.centroid_px
        axes[1].plot(sx - org[0], sy - org[1], "o",
                     color=GARNET, markersize=9, markeredgecolor="white",
                     markeredgewidth=1.2)
    style_ax(axes[1],
             f"(b) one seed per DBSCAN cluster  (n = {len(seeds)})",
             fontsize=11)
    fig.suptitle(
        "Step 5:  split each AIS-tagged vessel into per-target seeds before matching",
        color=BLACK90, fontsize=12, fontweight="bold", y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(OUT / "slide_08_dbscan_seeds.png", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Slide 09 — greedy AIS ↔ blob matching
# ──────────────────────────────────────────────────────────────────────
def slide09_greedy_match(ds="DAAN", step=51):
    print("[s09] greedy matching")
    bgr, entry = load_frame(ds, step)
    cal = get_calibration(ds)
    mask = create_radar_mask(bgr.shape[0], bgr.shape[1])

    objs  = parse_frame_annotations(entry or [])
    seeds = split_ais_to_seeds(
        objs, cx=cal["cx"], cy=cal["cy"],
        r_px_max=cal["r_px_max"], max_range_m=cal["max_range_m"])
    blobs = extract_blobs(bgr, radar_mask=mask, dataset=ds)
    match = greedy_match(seeds, blobs)

    crop, org = tight_crop(bgr, (cal["cx"], cal["cy"]), half=360)
    rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.6), facecolor="white")
    for ax in axes:
        ax.imshow(rgb); style_ax(ax)

    # (a) seeds (garnet) + all blob centroids (atlantic) + match-radius circles
    for b in blobs:
        axes[0].plot(b.cx - org[0], b.cy - org[1], "s",
                     color=ATLANTIC, markersize=5, markeredgecolor="white",
                     markeredgewidth=0.8)
    for s in seeds:
        sx, sy = s.centroid_px
        axes[0].add_patch(Circle((sx - org[0], sy - org[1]),
                                  MATCH_RADIUS_PX, fill=False,
                                  edgecolor=GARNET, linewidth=0.9,
                                  alpha=0.55))
        axes[0].plot(sx - org[0], sy - org[1], "o",
                     color=GARNET, markersize=7,
                     markeredgecolor="white", markeredgewidth=1.1)
    axes[0].set_title(
        f"(a) AIS seeds (garnet, n = {len(seeds)})  +  image blobs (atlantic, n = {len(blobs)})\n"
        f"match radius = {MATCH_RADIUS_PX}\u00a0px",
        color=BLACK90, fontsize=10)

    # (b) matches as arrows; unmatched seeds / unclaimed blobs distinct
    matched_seed_ids = set()
    for seed, blob in match.matched:
        sx, sy = seed.centroid_px
        axes[1].add_patch(FancyArrowPatch(
            (sx - org[0], sy - org[1]),
            (blob.cx - org[0], blob.cy - org[1]),
            arrowstyle="-|>", mutation_scale=8,
            color=GARNET, linewidth=1.2, shrinkA=3, shrinkB=3))
        axes[1].plot(blob.cx - org[0], blob.cy - org[1], "s",
                     color=HORSESHOE, markersize=6,
                     markeredgecolor="white", markeredgewidth=1.0)
        matched_seed_ids.add(id(seed))
    for s in seeds:
        sx, sy = s.centroid_px
        color = GARNET if id(s) in matched_seed_ids else WARM
        axes[1].plot(sx - org[0], sy - org[1], "o",
                     color=color, markersize=7,
                     markeredgecolor="white", markeredgewidth=1.1)
    n_unm = len(seeds) - len(match.matched)
    axes[1].set_title(
        f"(b) greedy match  \u2192  {len(match.matched)} matched,  "
        f"{n_unm} unmatched seed(s),  {len(match.unclaimed_blobs)} unclaimed blob(s)",
        color=BLACK90, fontsize=10)
    fig.suptitle(
        "Step 6:  greedy single-assignment  —  nearest unclaimed blob within radius",
        color=BLACK90, fontsize=12, fontweight="bold", y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(OUT / "slide_09_greedy_match.png", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Slide 10 — final bounding box comparison across all three datasets
# ──────────────────────────────────────────────────────────────────────
def slide10_box_comparison_trio():
    print("[s10] box comparison across datasets")
    fig, axes = plt.subplots(3, 2, figsize=(11.6, 13.8), facecolor="white")
    for j, header in enumerate(["(a) DLR default  —  DBSCAN + 15-px pad",
                                "(b) AIS-anchored, image-grounded"]):
        axes[0, j].set_title(header, color=BLACK90, fontsize=11,
                             pad=8, fontweight="bold")
    for i, ds in enumerate(DATASETS):
        bgr, entry = load_frame(ds, FRAMES[ds])
        cal = get_calibration(ds)
        h, w = bgr.shape[:2]
        mask = create_radar_mask(h, w)
        def_boxes = _dlr_default_boxes(entry, w, h, pad=15)
        objs  = parse_frame_annotations(entry or [])
        seeds = split_ais_to_seeds(
            objs, cx=cal["cx"], cy=cal["cy"],
            r_px_max=cal["r_px_max"], max_range_m=cal["max_range_m"])
        blobs = extract_blobs(bgr, radar_mask=mask, dataset=ds)
        match = greedy_match(seeds, blobs)

        crop, org = tight_crop(bgr, (cal["cx"], cal["cy"]), half=360)
        rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)

        def fmt(szs, n=None):
            if not szs: return "n = 0"
            ws = [s[0] for s in szs]; hs = [s[1] for s in szs]
            return (f"n = {n if n is not None else len(szs)}  |  median w\u00d7h = "
                    f"{int(np.median(ws))}\u00d7{int(np.median(hs))}\u00a0px")

        dsz = [(x2-x1, y2-y1) for (x1, y1, x2, y2) in def_boxes]
        osz = [(b.x2-b.x1, b.y2-b.y1) for _, b in match.matched]

        axes[i, 0].imshow(rgb); style_ax(axes[i, 0])
        for (x1, y1, x2, y2) in def_boxes:
            draw_box(axes[i, 0], x1, y1, x2, y2, ROSE, lw=1.5, offset=org)
        axes[i, 1].imshow(rgb); style_ax(axes[i, 1])
        for _, b in match.matched:
            draw_box(axes[i, 1], b.x1, b.y1, b.x2, b.y2, GARNET, lw=1.6, offset=org)

        axes[i, 0].set_ylabel(ds, color=GARNET, fontsize=13,
                              fontweight="bold", rotation=0, labelpad=26,
                              va="center")
        axes[i, 0].text(0.02, 0.02, fmt(dsz), transform=axes[i, 0].transAxes,
                        color=BLACK90, fontsize=9,
                        bbox=dict(facecolor="white", edgecolor=BLACK30,
                                  boxstyle="square,pad=0.25"))
        axes[i, 1].text(0.02, 0.02, fmt(osz), transform=axes[i, 1].transAxes,
                        color=BLACK90, fontsize=9,
                        bbox=dict(facecolor="white", edgecolor=BLACK30,
                                  boxstyle="square,pad=0.25"))

    fig.suptitle(
        "Step 7:  resulting bounding boxes  —  DLR default vs AIS-anchored, all three datasets",
        color=BLACK90, fontsize=12, fontweight="bold", y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(OUT / "slide_10_box_comparison_trio.png", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Slide 11 — residual (seed → nearest blob distance) across datasets
# ──────────────────────────────────────────────────────────────────────
def _residuals(ds, mask, default=False, sample_step=20):
    img_dir = DLR_ROOT / f"{ds}_" / "radarImages"
    steps = sorted(int(p.stem) for p in img_dir.glob("*.png")
                   if not p.name.startswith("._"))
    steps = steps[::max(1, len(steps) // sample_step)]
    out = []
    for step in steps:
        bgr, entry = load_frame(ds, step)
        if bgr is None or entry is None:
            continue
        h, w = bgr.shape[:2]
        blobs = extract_blobs(bgr, radar_mask=mask, dataset=ds)
        if not blobs:
            continue
        bxy = np.array([[b.cx, b.cy] for b in blobs])
        objs = parse_frame_annotations(entry or [])
        seeds_xy = []
        if default:
            for o in objs:
                if not o.points_polar: continue
                rs = np.array([p[0] for p in o.points_polar])
                ths = np.array([p[1] for p in o.points_polar])
                dx, dy = _dlr_default_project(rs, ths, w, h)
                seeds_xy.append((dx.mean(), dy.mean()))
        else:
            cal = get_calibration(ds)
            ss = split_ais_to_seeds(
                objs, cx=cal["cx"], cy=cal["cy"],
                r_px_max=cal["r_px_max"], max_range_m=cal["max_range_m"])
            seeds_xy = [s.centroid_px for s in ss]
        if not seeds_xy:
            continue
        sxy = np.array(seeds_xy)
        d = np.sqrt(((sxy[:, None, :] - bxy[None, :, :])**2).sum(-1)).min(1)
        out.extend(d.tolist())
    return out


def slide11_residual_hist():
    print("[s11] residual hist per dataset (reuses fig3 style)")
    mask = create_radar_mask(1024, 1050)
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 3.8), facecolor="white",
                             sharey=True)
    for ax, ds in zip(axes, DATASETS):
        dvals = _residuals(ds, mask, default=True)
        fvals = _residuals(ds, mask, default=False)
        bins = np.arange(0, 121, 3)
        ax.hist(dvals, bins=bins, color=ROSE, alpha=0.55,
                edgecolor=ROSE, linewidth=0.4, label="DLR default")
        ax.hist(fvals, bins=bins, color=GARNET, alpha=0.80,
                edgecolor=GARNET, linewidth=0.4, label="fitted")
        md = float(np.median(dvals)) if dvals else 0.0
        mf = float(np.median(fvals)) if fvals else 0.0
        ax.axvline(md, color=ROSE, ls="--", lw=1.0)
        ax.axvline(mf, color=GARNET, ls="--", lw=1.0)
        ax.set_title(
            f"{ds}   —   median: {md:.0f}\u2009\u2192\u2009{mf:.0f}\u00a0px",
            color=BLACK90, fontsize=11)
        ax.set_xlabel("AIS seed \u2192 nearest image blob (px)")
        if ds == DATASETS[0]:
            ax.set_ylabel("count (sampled frames)")
        ax.legend(frameon=False, fontsize=8)
    fig.suptitle(
        "Calibration validation:  AIS-to-blob pixel residual across 50+ frames per dataset",
        color=BLACK90, fontsize=12, fontweight="bold", y=1.0)
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(OUT / "slide_11_residual_hist.png", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Slide 12 — pipeline flowchart (matplotlib; two parallel tracks)
# ──────────────────────────────────────────────────────────────────────
def slide12_flowchart():
    print("[s12] pipeline flowchart")
    fig, ax = plt.subplots(figsize=(13.5, 6.0), facecolor="white")
    ax.set_xlim(0, 100); ax.set_ylim(0, 60)
    ax.axis("off")

    def box(x, y, w, h, text, fc="white", ec=BLACK70, tc=BLACK90,
            fs=9.5, lw=1.2, bold=False):
        ax.add_patch(mpatches.Rectangle((x, y), w, h, fill=True,
                                         facecolor=fc, edgecolor=ec,
                                         linewidth=lw))
        ax.text(x + w/2, y + h/2, text, ha="center", va="center",
                color=tc, fontsize=fs,
                fontweight=("bold" if bold else "normal"), wrap=True)

    def arrow(x1, y1, x2, y2, color=BLACK70):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                      arrowstyle="-|>", mutation_scale=12,
                                      color=color, linewidth=1.4))

    # Top track: image → blobs
    y_img = 42
    box( 1, y_img, 14, 9, "Raw PPI frame\n(BGR, 1050\u00d71024)", fc=BLACK10, bold=True)
    box(17, y_img, 14, 9, "Per-dataset\ncolor extractor\n(red / yellow-HSV)")
    box(33, y_img, 14, 9, "Circular PPI\nmask\n(bitwise-AND)")
    box(49, y_img, 14, 9, f"Threshold\nI > {INTENSITY_THRESHOLD}")
    box(65, y_img, 14, 9, "Morph. closing\n5\u00d75 ellipse")
    box(81, y_img, 16, 9, "Connected\ncomponents\n+ area filter", fc="#F3E4E6")
    for x1, x2 in [(15,17), (31,33), (47,49), (63,65), (79,81)]:
        arrow(x1, y_img+4.5, x2, y_img+4.5)

    # Bottom track: AIS → seeds
    y_ais = 18
    box( 1, y_ais, 14, 9, "polarMeas.json\n[obj_id, hdg, (r,\u03b8),…]", fc=BLACK10, bold=True)
    box(17, y_ais, 14, 9, "Per-dataset\npolar calibration\n(cx, cy, max_r)")
    box(33, y_ais, 14, 9, "Polar\u2192pixel\nprojection")
    box(49, y_ais, 14, 9, "Cartesian (m)\nDBSCAN\neps = 200\u00a0m, min = 5")
    box(65, y_ais, 14, 9, "One seed per\ncluster\n(pixel space)", fc="#F3E4E6")
    for x1, x2 in [(15,17), (31,33), (47,49), (63,65)]:
        arrow(x1, y_ais+4.5, x2, y_ais+4.5)

    # Merge arrows → greedy match
    box(78, y_ais-5, 19, 10, "Greedy match\nAIS seed \u2194 blob\nradius = 20\u00a0px",
        fc=GARNET, ec=GARNET, tc="white", bold=True)
    arrow(97, y_img, 97, y_ais+5, color=GARNET)  # down from top-right
    arrow(79, y_ais+4.5, 78, y_ais, color=GARNET)  # across from seeds
    arrow(97, y_img, 97, y_ais+5, color=GARNET)

    # Final output
    box(78, 1, 19, 8, "Tight AIS-anchored\nbounding box",
        fc=BLACK90, ec=BLACK90, tc="white", bold=True)
    arrow(87.5, y_ais-5, 87.5, 9, color=GARNET)

    # Track labels
    ax.text(0, y_img + 10.5, "IMAGE  TRACK", color=GARNET,
            fontsize=11, fontweight="bold")
    ax.text(0, y_ais + 10.5, "AIS  TRACK", color=GARNET,
            fontsize=11, fontweight="bold")

    fig.suptitle(
        "Full preprocessing + GT pipeline",
        color=BLACK90, fontsize=13, fontweight="bold", y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUT / "slide_12_flowchart.png", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    slide12_flowchart()
    slide01_raw_trio()
    slide02_color_isolation()
    slide03_ppi_mask()
    slide04_threshold_morph()
    slide05_cc_filter()
    slide06_polar_bias()
    slide07_calibration_schematic()
    slide08_dbscan_seeds()
    slide09_greedy_match()
    slide10_box_comparison_trio()
    slide11_residual_hist()
    print("done.  figures in", OUT)
