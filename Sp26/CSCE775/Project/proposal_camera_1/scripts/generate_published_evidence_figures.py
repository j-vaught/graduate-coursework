#!/usr/bin/env python3
import csv
import pathlib
import matplotlib.pyplot as plt
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "drafts" / "figures"
RESULTS_CSV = ROOT / "results" / "published_results_summary.csv"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Brand palette from AGENTS.md
GARNET = "#73000A"
BLACK = "#000000"
WHITE = "#FFFFFF"
NEUTRAL_30 = "#C7C7C7"
ATLANTIC = "#466A9F"
CONGAREE = "#1F414D"
HORSESHOE = "#65780B"
HONEYCOMB = "#A49137"


def load_rows():
    with RESULTS_CSV.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_value(rows, source, task_contains, metric_contains):
    for row in rows:
        if (
            row["source"] == source
            and task_contains in row["task"]
            and metric_contains in row["metric"]
        ):
            return float(row["value"])
    raise ValueError(f"Missing row for {source} / {task_contains} / {metric_contains}")


def create_evidence_figure():
    rows = load_rows()

    aug_labels = [
        "AutoAugment\n(CIFAR-10)",
        "RandAugment\n(ImageNet)",
        "RandAugment\n(COCO)",
    ]
    aug_values = [
        get_value(rows, "Cubuk2019_AutoAugment", "CIFAR-10", "Error reduction"),
        get_value(rows, "Cubuk2020_RandAugment", "ImageNet", "Top-1 gain"),
        get_value(rows, "Cubuk2020_RandAugment", "COCO", "mAP gain"),
    ]

    reg_labels = [
        "Unified RGBT\n(FLIR)",
        "ADCNet\n(M3FD mAP50)",
        "ADCNet\n(M3FD mAP)",
    ]
    reg_values = [
        get_value(rows, "Vadidar2022_UnifiedRGBT", "FLIR", "mAP gain"),
        get_value(rows, "Li2023_ADCNet", "M3FD", "mAP50 gain"),
        get_value(rows, "Li2023_ADCNet", "M3FD", "mAP gain"),
    ]

    fd2_flir = get_value(rows, "Li2024_FD2Net", "FLIR", "mAP (%)")
    fd2_m3fd = get_value(rows, "Li2024_FD2Net", "M3FD", "mAP (%)")
    fd2_llvip = get_value(rows, "Li2024_FD2Net", "LLVIP", "mAP (%)")

    fig, axes = plt.subplots(1, 2, figsize=(12.2, 4.8), constrained_layout=True)
    fig.patch.set_facecolor(WHITE)

    x0 = np.arange(len(aug_labels))
    colors0 = [GARNET, ATLANTIC, HONEYCOMB]
    bars0 = axes[0].bar(x0, aug_values, color=colors0, edgecolor=BLACK, linewidth=1.0)
    axes[0].set_xticks(x0)
    axes[0].set_xticklabels(aug_labels, fontsize=9)
    axes[0].set_ylabel("Reported gain (percentage points)")
    axes[0].set_title("Published Augmentation Gains")
    axes[0].set_ylim(0, max(aug_values) + 1.4)
    axes[0].grid(axis="y", linestyle="-", linewidth=0.7, color=NEUTRAL_30)
    axes[0].set_axisbelow(True)
    for bar, value in zip(bars0, aug_values):
        axes[0].text(bar.get_x() + bar.get_width() / 2, value + 0.08, f"{value:.1f}",
                     ha="center", va="bottom", fontsize=8, color=BLACK)

    x1 = np.arange(len(reg_labels))
    colors1 = [HORSESHOE, CONGAREE, ATLANTIC]
    bars1 = axes[1].bar(x1, reg_values, color=colors1, edgecolor=BLACK, linewidth=1.0)
    axes[1].set_xticks(x1)
    axes[1].set_xticklabels(reg_labels, fontsize=9)
    axes[1].set_ylabel("Reported gain (percentage points)")
    axes[1].set_title("Published Cross-Modal Robustness Gains")
    axes[1].set_ylim(0, max(reg_values) + 2.0)
    axes[1].grid(axis="y", linestyle="-", linewidth=0.7, color=NEUTRAL_30)
    axes[1].set_axisbelow(True)
    for bar, value in zip(bars1, reg_values):
        axes[1].text(bar.get_x() + bar.get_width() / 2, value + 0.1, f"{value:.1f}",
                     ha="center", va="bottom", fontsize=8, color=BLACK)

    axes[1].text(
        0.02,
        0.96,
        (
            "FD2-Net reported absolute mAP:\n"
            f"FLIR {fd2_flir:.1f}, M3FD {fd2_m3fd:.1f}, LLVIP {fd2_llvip:.1f}"
        ),
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8,
        color=BLACK,
        bbox={"facecolor": WHITE, "edgecolor": BLACK, "linewidth": 0.8, "boxstyle": "square,pad=0.25"},
    )

    for ax in axes:
        ax.set_facecolor(WHITE)
        for spine in ax.spines.values():
            spine.set_color(BLACK)
            spine.set_linewidth(1.0)
        ax.tick_params(colors=BLACK, width=0.9)
        ax.title.set_color(CONGAREE)

    fig.suptitle(
        "Published Evidence for Adaptive Augmentation and Cross-Modal Alignment",
        fontsize=12,
        fontweight="bold",
        color=CONGAREE,
    )

    out_pdf = FIG_DIR / "fig_published_evidence_results.pdf"
    out_png = FIG_DIR / "fig_published_evidence_results.png"
    fig.savefig(out_pdf, bbox_inches="tight")
    fig.savefig(out_png, bbox_inches="tight", dpi=300)
    print(f"Wrote {out_pdf}")
    print(f"Wrote {out_png}")


if __name__ == "__main__":
    create_evidence_figure()
