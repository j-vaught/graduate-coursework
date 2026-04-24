"""Generate publication-quality figures for the marine radar detection report.

Reads results from:
  - results/evaluation_summary_v3.csv     (DAAN unified: DL seeds + classical)
  - results/classical_by_dataset.csv      (per-dataset: DAAN / DARC / MANV)

Brand palette (per author preferences): Garnet #73000A, Atlantic, Congaree,
Horseshoe, Rose, Honeycomb, Grass, plus the black / warm-grey neutrals.
No rounded edges. High contrast. No emojis.
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
import warnings
from pathlib import Path

# make src.data.* importable regardless of invocation cwd
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
from matplotlib.ticker import AutoMinorLocator

warnings.filterwarnings("ignore")

# ── Brand palette ────────────────────────────────────────────────────────
GARNET     = "#73000A"
BLACK      = "#000000"
WHITE      = "#FFFFFF"
BLACK_90   = "#363636"
BLACK_70   = "#5C5C5C"
BLACK_50   = "#A2A2A2"
BLACK_30   = "#C7C7C7"
BLACK_10   = "#ECECEC"
WARM_GREY  = "#676156"
SANDSTORM  = "#FFF2E3"
ROSE       = "#CC2E40"
ATLANTIC   = "#466A9F"
CONGAREE   = "#1F414D"
HORSESHOE  = "#65780B"
GRASS      = "#CED318"
HONEYCOMB  = "#A49137"

# Colour assignments — classical methods warm; DL models cool
CLASSICAL_COLOURS = {
    "morphological": CONGAREE,
    "otsu":          HORSESHOE,
    "ca_cfar":       GARNET,
    "so_cfar":       ROSE,
    "go_cfar":       HONEYCOMB,
    "ssotsu":        WARM_GREY,
    "wavelet":       BLACK_70,
    "os_cfar":       BLACK_50,
}
DL_COLOURS = {
    "yolov11":     ATLANTIC,
    "rt_detr":     GRASS,
    "faster_rcnn": BLACK_90,
    "unet":        BLACK_50,
}

METHOD_LABELS = {
    "yolov11":       "YOLOv11",
    "rt_detr":       "RT-DETR",
    "faster_rcnn":   "Faster R-CNN",
    "unet":          "U-Net",
    "morphological": "Morphological",
    "otsu":          "Otsu",
    "ca_cfar":       "CA-CFAR",
    "so_cfar":       "SO-CFAR",
    "go_cfar":       "GO-CFAR",
    "ssotsu":        "SSOTSU",
    "wavelet":       "Wavelet",
    "os_cfar":       "OS-CFAR",
}


def setup_style() -> None:
    mpl.rcParams.update({
        "figure.facecolor":     WHITE,
        "axes.facecolor":       WHITE,
        "savefig.facecolor":    WHITE,
        "axes.edgecolor":       BLACK,
        "axes.labelcolor":      BLACK,
        "text.color":           BLACK,
        "xtick.color":          BLACK,
        "ytick.color":          BLACK,
        "font.family":          "sans-serif",
        "font.sans-serif":      ["DejaVu Sans", "Helvetica", "Arial"],
        "font.size":            10,
        "axes.titlesize":       11,
        "axes.titleweight":     "bold",
        "axes.labelsize":       10,
        "legend.frameon":       False,
        "legend.fontsize":      9,
        "axes.grid":            False,
        "axes.spines.top":      False,
        "axes.spines.right":    False,
        "axes.linewidth":       0.8,
        "xtick.major.size":     3,
        "ytick.major.size":     3,
        "xtick.major.width":    0.8,
        "ytick.major.width":    0.8,
        "patch.linewidth":      0.6,
    })


# ── Data loaders ─────────────────────────────────────────────────────────
def load_unified(path: Path = Path("results/evaluation_summary_v3.csv")) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["is_dl"] = df["scope"] == "tile"
    df["label"] = df["method"].map(METHOD_LABELS)
    return df


def aggregate_methods(df: pd.DataFrame) -> pd.DataFrame:
    """One row per method with mean+std over seeds for DL, single value for classical."""
    out = []
    for method, grp in df.groupby("method"):
        is_dl = grp["is_dl"].iloc[0]
        row = {"method": method,
               "label": METHOD_LABELS.get(method, method),
               "is_dl": is_dl,
               "n_seeds": len(grp)}
        for k in ["AP@0.50", "AP@0.75", "AP@0.50:0.95", "AR@100", "n_preds"]:
            row[k + "_mean"] = grp[k].mean()
            row[k + "_std"]  = grp[k].std() if len(grp) > 1 else 0.0
        out.append(row)
    return pd.DataFrame(out)


def load_per_dataset(path: Path = Path("results/classical_by_dataset.csv")) -> pd.DataFrame:
    return pd.read_csv(path)


# ── Figure 1: headline ranking ───────────────────────────────────────────
def fig_headline(df: pd.DataFrame, out_path: Path) -> None:
    agg = aggregate_methods(df).sort_values("AP@0.50_mean", ascending=False)

    fig, ax = plt.subplots(figsize=(10, 4.8))
    x = np.arange(len(agg))
    colors = [DL_COLOURS[m] if is_dl else CLASSICAL_COLOURS[m]
              for m, is_dl in zip(agg["method"], agg["is_dl"])]
    bars = ax.bar(x, agg["AP@0.50_mean"], yerr=agg["AP@0.50_std"],
                  color=colors, edgecolor=BLACK, linewidth=0.5, width=0.75,
                  capsize=3, error_kw={"ecolor": BLACK, "linewidth": 0.8})

    # Value labels
    for b, v, s in zip(bars, agg["AP@0.50_mean"], agg["AP@0.50_std"]):
        label = f"{v:.3f}" if v >= 0.01 else f"{v:.4f}"
        ax.text(b.get_x() + b.get_width() / 2,
                v + s + agg["AP@0.50_mean"].max() * 0.015,
                label, ha="center", va="bottom", fontsize=8.5, color=BLACK)

    ax.set_xticks(x)
    ax.set_xticklabels([f"{l}*" if is_dl else l
                         for l, is_dl in zip(agg["label"], agg["is_dl"])],
                        rotation=30, ha="right")
    ax.set_ylabel("AP\\@0.50")
    ax.set_ylim(0, agg["AP@0.50_mean"].max() * 1.18)
    ax.set_title("Headline Ranking — AP\\@0.50 on DAAN Test")

    # Legend: DL vs classical, plus the asterisk note
    from matplotlib.patches import Patch
    legend_el = [
        Patch(facecolor=ATLANTIC, edgecolor=BLACK, label="Deep learning (tile GT, mean $\\pm 1\\sigma$ / 3 seeds)"),
        Patch(facecolor=GARNET, edgecolor=BLACK, label="Classical (full-frame GT, deterministic)"),
    ]
    ax.legend(handles=legend_el, loc="upper right")
    ax.text(0.01, 0.97, "$*$ = deep learning (3 seeds)",
            transform=ax.transAxes, fontsize=8, color=BLACK_70, va="top")

    plt.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


# ── Figure 2: 4-metric panel ─────────────────────────────────────────────
def fig_multimetric(df: pd.DataFrame, out_path: Path) -> None:
    agg = aggregate_methods(df)
    metrics = [
        ("AP@0.50",      "AP\\@0.50"),
        ("AP@0.75",      "AP\\@0.75"),
        ("AP@0.50:0.95", "AP\\@[0.50:0.95]"),
        ("AR@100",       "AR\\@100"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    for ax, (col, title) in zip(axes.flat, metrics):
        mean_col = col + "_mean"; std_col = col + "_std"
        a = agg.sort_values(mean_col, ascending=False)
        x = np.arange(len(a))
        colors = [DL_COLOURS[m] if is_dl else CLASSICAL_COLOURS[m]
                  for m, is_dl in zip(a["method"], a["is_dl"])]
        ax.bar(x, a[mean_col], yerr=a[std_col], color=colors,
               edgecolor=BLACK, linewidth=0.5, width=0.75, capsize=2,
               error_kw={"ecolor": BLACK, "linewidth": 0.6})
        ax.set_xticks(x)
        ax.set_xticklabels(a["label"], rotation=30, ha="right", fontsize=8)
        ax.set_title(title)
        ax.set_ylabel("Score")
        ymax = max(a[mean_col].max() * 1.15, 0.05)
        ax.set_ylim(0, ymax)

    plt.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


# ── Figure 3: per-dataset classical comparison ───────────────────────────
def fig_per_dataset(pd_df: pd.DataFrame, out_path: Path) -> None:
    """Grouped bars: each method gets three bars (DAAN / DARC / MANV)."""
    methods_order = ["morphological", "otsu", "ca_cfar", "so_cfar",
                     "go_cfar", "ssotsu", "wavelet"]
    datasets = ["DAAN", "DARC", "MANV"]
    ds_colours = [GARNET, ATLANTIC, HORSESHOE]

    # Pivot
    pivot = pd_df.pivot(index="method", columns="dataset",
                        values="AP@0.50").reindex(methods_order)

    fig, ax = plt.subplots(figsize=(10, 4.8))
    x = np.arange(len(methods_order))
    w = 0.27
    for i, ds in enumerate(datasets):
        ax.bar(x + (i - 1) * w, pivot[ds], width=w,
               color=ds_colours[i], edgecolor=BLACK, linewidth=0.5,
               label=ds)
        # Value labels
        for xi, v in zip(x + (i - 1) * w, pivot[ds]):
            if v >= 0.02:
                ax.text(xi, v + 0.01, f"{v:.2f}",
                        ha="center", va="bottom", fontsize=7.5, color=BLACK)

    ax.set_xticks(x)
    ax.set_xticklabels([METHOD_LABELS[m] for m in methods_order],
                        rotation=30, ha="right")
    ax.set_ylabel("AP\\@0.50")
    ax.set_title("Classical Methods: AP\\@0.50 per DLR Sub-dataset")
    ax.set_ylim(0, 0.9)
    ax.legend(title="Dataset", loc="upper right")

    plt.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


# ── Figure 4: DL seed spread (consistency across 3 seeds) ────────────────
def fig_dl_seeds(df: pd.DataFrame, out_path: Path) -> None:
    dl = df[df["is_dl"]].copy()
    methods_order = ["yolov11", "rt_detr", "faster_rcnn"]
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.8))
    for ax, m in zip(axes, methods_order):
        rows = dl[dl["method"] == m].sort_values("seed")
        if rows.empty: continue
        keys = ["AP@0.50", "AP@0.75", "AP@0.50:0.95", "AR@100"]
        x = np.arange(len(keys))
        colours = [ATLANTIC, ROSE, HONEYCOMB]
        width = 0.25
        for i, (_, r) in enumerate(rows.iterrows()):
            ax.bar(x + (i-1)*width, [r[k] for k in keys], width=width,
                   color=colours[i], edgecolor=BLACK, linewidth=0.4,
                   label=f"seed {int(r['seed'])}")
        ax.set_xticks(x)
        ax.set_xticklabels(["AP@0.50", "AP@0.75", "AP@[.50:.95]", "AR@100"],
                            rotation=20, ha="right", fontsize=8)
        ax.set_title(METHOD_LABELS[m])
        ax.set_ylim(0, 1)
        ax.set_ylabel("Score")
        ax.legend(loc="upper right", fontsize=8)

    plt.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


# ── Figure 5: prediction count vs AP (efficiency) ────────────────────────
def fig_count_vs_ap(df: pd.DataFrame, out_path: Path) -> None:
    agg = aggregate_methods(df)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for _, r in agg.iterrows():
        colour = DL_COLOURS[r["method"]] if r["is_dl"] else CLASSICAL_COLOURS[r["method"]]
        marker = "o" if r["is_dl"] else "s"
        ax.scatter(r["n_preds_mean"], r["AP@0.50_mean"],
                   s=180, c=colour, marker=marker, edgecolor=BLACK,
                   linewidth=0.7, zorder=3, alpha=0.9)
        ax.annotate(r["label"], (r["n_preds_mean"], r["AP@0.50_mean"]),
                    xytext=(9, 4), textcoords="offset points",
                    fontsize=8.5, color=BLACK_90)

    # Reference lines: GT count on tile vs full scope
    ax.axvline(6980, color=GARNET, linewidth=0.8, linestyle=(0, (3, 3)))
    ax.text(6980*1.05, ax.get_ylim()[1]*0.97, "tile GT = 6,980",
            color=GARNET, fontsize=8, va="top")
    ax.axvline(1935, color=ATLANTIC, linewidth=0.8, linestyle=(0, (3, 3)))
    ax.text(1935*1.05, ax.get_ylim()[1]*0.90, "full-frame GT = 1,935",
            color=ATLANTIC, fontsize=8, va="top")

    ax.set_xscale("log")
    ax.set_xlabel("Predictions emitted on DAAN test (log scale)")
    ax.set_ylabel("AP\\@0.50")
    ax.set_title("Detection Volume vs. Precision")

    from matplotlib.lines import Line2D
    handles = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=ATLANTIC,
               markersize=10, markeredgecolor=BLACK, label="Deep learning"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor=GARNET,
               markersize=10, markeredgecolor=BLACK, label="Classical"),
    ]
    ax.legend(handles=handles, loc="lower right")
    plt.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


# ── Figure 6: qualitative — existing output samples side-by-side ─────────
def fig_qualitative(out_path: Path) -> None:
    """Load the pre-computed output_samples images into a single panel."""
    sample_files = [
        "report/output_samples/DL_DAAN_342_tile0001.png",
        "report/output_samples/classical_DAAN_342.png",
    ]
    imgs = [cv2.cvtColor(cv2.imread(p), cv2.COLOR_BGR2RGB)
            for p in sample_files if Path(p).exists()]
    if len(imgs) < 2:
        return

    fig, axes = plt.subplots(1, 2, figsize=(12, 6.5))
    titles = ["(a) DL detectors on a test tile (640×640)",
              "(b) Classical detectors on a full frame (1050×1024)"]
    for ax, im, t in zip(axes, imgs, titles):
        ax.imshow(im)
        ax.set_title(t, fontsize=10)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_edgecolor(BLACK); sp.set_linewidth(0.7)

    plt.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


# ── Figure 7: preprocessing pipeline (from earlier — regenerate) ─────────
def fig_preprocess(out_path: Path) -> None:
    from src.data.radar_mask import (DATASET_CALIBRATION, create_radar_mask,
                                      DEFAULT_CENTER_X, DEFAULT_CENTER_Y,
                                      DEFAULT_RADIUS)
    # Four panels: one from each of the three datasets + GT overlay on DAAN
    frames = [
        ("DAAN", "342.png", "(a) DAAN — long-range (12 m/px)"),
        ("DARC", "100.png", "(b) DARC — long-range (12 m/px)"),
        ("MANV", "250.png", "(c) MANV — close-range (6 m/px)"),
    ]
    mask = create_radar_mask(1024, 1050)

    fig, axes = plt.subplots(1, 4, figsize=(14, 4))

    from src.data.ais_anchored_gt import process_frame
    # Render the three datasets + GT overlay on DAAN
    for i, (ds, fname, title) in enumerate(frames):
        path = Path(f"data/raw/{ds}/radarImages/{fname}")
        if not path.exists():
            continue
        bgr = cv2.imread(str(path))
        from src.data.radar_mask import extract_radar_signal
        sig = extract_radar_signal(bgr, dataset=ds)
        sig = cv2.bitwise_and(sig, mask)

        ax = axes[i]
        ax.imshow(sig, cmap="gray", vmin=0, vmax=255)
        ax.set_title(title, fontsize=10)
        ax.set_xlim(20, 1030)
        ax.set_ylim(1004, 26)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_edgecolor(BLACK); sp.set_linewidth(0.7)

    # Panel (d): DAAN with GT
    ax = axes[3]
    bgr = cv2.imread("data/raw/DAAN/radarImages/342.png")
    from src.data.radar_mask import extract_radar_signal
    sig = cv2.bitwise_and(extract_radar_signal(bgr, dataset="DAAN"), mask)
    ax.imshow(sig, cmap="gray", vmin=0, vmax=255)

    with open("data/processed/annotations/test.json") as f:
        gt = json.load(f)
    img_info = next((im for im in gt["images"] if im["file_name"] == "DAAN_342.png"), None)
    if img_info:
        for a in gt["annotations"]:
            if a["image_id"] != img_info["id"]: continue
            x, y, w, h = a["bbox"]
            ax.add_patch(Rectangle((x, y), w, h, linewidth=1.6,
                                    edgecolor=GARNET, facecolor="none"))
    ax.set_title("(d) + AIS-anchored GT overlay", fontsize=10)
    ax.set_xlim(20, 1030); ax.set_ylim(1004, 26)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_edgecolor(BLACK); sp.set_linewidth(0.7)

    plt.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


# ── Figure 8: dataset composition ────────────────────────────────────────
def fig_dataset(out_path: Path) -> None:
    splits = [("Train (MANV)", "train.json", HORSESHOE),
              ("Val (DARC)",   "val.json",   ATLANTIC),
              ("Test (DAAN)",  "test.json",  GARNET)]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    # Left: counts
    ax = axes[0]
    names, imgs, anns, cols = [], [], [], []
    for label, fname, col in splits:
        with open(f"data/processed/annotations/{fname}") as f:
            j = json.load(f)
        names.append(label); imgs.append(len(j["images"]))
        anns.append(len(j["annotations"])); cols.append(col)

    x = np.arange(len(names))
    w = 0.38
    b1 = ax.bar(x - w/2, imgs, width=w, color=cols, edgecolor=BLACK,
                 linewidth=0.5, label="Images")
    b2 = ax.bar(x + w/2, anns, width=w, color=[BLACK_70]*3, edgecolor=BLACK,
                 linewidth=0.5, label="Annotations")
    for b, v in zip(list(b1) + list(b2), imgs + anns):
        ax.text(b.get_x() + b.get_width()/2, v + 80, f"{v:,}",
                ha="center", va="bottom", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(names)
    ax.set_ylabel("Count")
    ax.set_title("Split sizes (clean AIS-anchored GT)")
    ax.legend(loc="upper right")

    # Right: target density on DAAN test
    ax = axes[1]
    with open("data/processed/annotations/test.json") as f:
        gt = json.load(f)
    per_img = {}
    for a in gt["annotations"]:
        per_img[a["image_id"]] = per_img.get(a["image_id"], 0) + 1
    all_counts = list(per_img.values()) + [0] * (len(gt["images"]) - len(per_img))
    bins = np.arange(0, max(all_counts) + 2) - 0.5
    ax.hist(all_counts, bins=bins, color=GARNET, edgecolor=BLACK,
             linewidth=0.5, alpha=0.85)
    ax.set_xlabel("Objects per image (DAAN test)")
    ax.set_ylabel("Number of images")
    ax.set_title("Target density")

    plt.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


# ── Main driver ──────────────────────────────────────────────────────────
def main() -> None:
    setup_style()
    out = Path("report/figures")
    out.mkdir(parents=True, exist_ok=True)

    df_unified = load_unified()
    df_perds   = load_per_dataset()

    print("Rendering Figure 1: headline ranking")
    fig_headline(df_unified, out / "fig1_headline.png")

    print("Rendering Figure 2: 4-metric panel")
    fig_multimetric(df_unified, out / "fig2_multimetric.png")

    print("Rendering Figure 3: per-dataset classical")
    fig_per_dataset(df_perds, out / "fig3_per_dataset.png")

    print("Rendering Figure 4: DL seed spread")
    fig_dl_seeds(df_unified, out / "fig4_dl_seeds.png")

    print("Rendering Figure 5: detection volume vs AP")
    fig_count_vs_ap(df_unified, out / "fig5_count_vs_ap.png")

    print("Rendering Figure 6: qualitative samples")
    fig_qualitative(out / "fig6_qualitative.png")

    print("Rendering Figure 7: preprocessing pipeline")
    fig_preprocess(out / "fig7_preprocess.png")

    print("Rendering Figure 8: dataset composition")
    fig_dataset(out / "fig8_dataset.png")

    print(f"\nAll figures saved to {out.resolve()}")


if __name__ == "__main__":
    main()
