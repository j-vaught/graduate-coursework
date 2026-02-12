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
NEUTRAL_90 = "#363636"
ATLANTIC = "#466A9F"
CONGAREE = "#1F414D"
HORSESHOE = "#65780B"
HONEYCOMB = "#A49137"


def load_rows():
    with RESULTS_CSV.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_value(rows, source, task_contains, method):
    for row in rows:
        if (
            row["source"] == source
            and task_contains in row["task"]
            and row["method"] == method
        ):
            return float(row["value"])
    raise ValueError(f"Missing row for {source} / {task_contains} / {method}")


def create_figure():
    rows = load_rows()

    methods_left = ["RT baseline", "Random DR", "CDR (calibrated)"]
    occ = [
        get_value(rows, "Trinh2026_CDR", "Occupancy detection", m)
        for m in methods_left
    ]
    count = [
        get_value(rows, "Trinh2026_CDR", "People counting", m)
        for m in methods_left
    ]

    methods_right = ["w/o Aug", "Only Noise", "Gamma+Noise", "SSR (proposed)"]
    sar_values = [
        get_value(rows, "Kim2024_SSR", "Scenario 1", m)
        for m in methods_right
    ]

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8), constrained_layout=True)
    fig.patch.set_facecolor(WHITE)

    x0 = np.arange(len(methods_left))
    width = 0.36

    bars_occ = axes[0].bar(
        x0 - width / 2,
        occ,
        width=width,
        color=GARNET,
        edgecolor=BLACK,
        linewidth=1.0,
        hatch="///",
        label="Occupancy",
    )
    bars_count = axes[0].bar(
        x0 + width / 2,
        count,
        width=width,
        color=ATLANTIC,
        edgecolor=BLACK,
        linewidth=1.0,
        hatch="xxx",
        label="People counting",
    )

    axes[0].set_xticks(x0)
    axes[0].set_xticklabels(methods_left, rotation=9)
    axes[0].set_ylim(0, 105)
    axes[0].set_ylabel("Balanced accuracy (%)")
    axes[0].set_title("FMCW Transfer Results (Trinh et al., 2026)")
    axes[0].grid(axis="y", linestyle="-", linewidth=0.7, color=NEUTRAL_30)
    axes[0].set_axisbelow(True)
    axes[0].legend(frameon=False, fontsize=9, loc="upper left")

    for bar in list(bars_occ) + list(bars_count):
        y = bar.get_height()
        axes[0].text(
            bar.get_x() + bar.get_width() / 2,
            y + 1.2,
            f"{y:.0f}",
            ha="center",
            va="bottom",
            fontsize=8,
            color=BLACK,
        )

    x1 = np.arange(len(methods_right))
    bars_sar = axes[1].bar(
        x1,
        sar_values,
        color=[NEUTRAL_90, HONEYCOMB, ATLANTIC, HORSESHOE],
        edgecolor=BLACK,
        linewidth=1.0,
    )
    axes[1].set_xticks(x1)
    axes[1].set_xticklabels(methods_right, rotation=9)
    axes[1].set_ylim(0, 100)
    axes[1].set_ylabel("Mean ATR accuracy (%)")
    axes[1].set_title("SAMPLE Scenario 1 (Kim et al., 2024)")
    axes[1].grid(axis="y", linestyle="-", linewidth=0.7, color=NEUTRAL_30)
    axes[1].set_axisbelow(True)

    for bar in bars_sar:
        y = bar.get_height()
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            y + 1.2,
            f"{y:.1f}",
            ha="center",
            va="bottom",
            fontsize=8,
            color=BLACK,
        )

    for ax in axes:
        ax.set_facecolor(WHITE)
        for spine in ax.spines.values():
            spine.set_color(BLACK)
            spine.set_linewidth(1.0)
        ax.tick_params(colors=BLACK, width=0.9)
        ax.title.set_color(CONGAREE)

    fig.suptitle(
        "Published Radar Sim-to-Real Evidence Motivating Adaptive Simulator Control",
        fontsize=12,
        fontweight="bold",
        color=CONGAREE,
    )

    out_pdf = FIG_DIR / "fig_published_evidence_results.pdf"
    out_svg = FIG_DIR / "fig_published_evidence_results.svg"
    out_png = FIG_DIR / "fig_published_evidence_results.png"
    fig.savefig(out_pdf, bbox_inches="tight")
    fig.savefig(out_svg, bbox_inches="tight")
    fig.savefig(out_png, bbox_inches="tight", dpi=300)
    print(f"Wrote {out_pdf}")
    print(f"Wrote {out_svg}")
    print(f"Wrote {out_png}")


if __name__ == "__main__":
    create_figure()
