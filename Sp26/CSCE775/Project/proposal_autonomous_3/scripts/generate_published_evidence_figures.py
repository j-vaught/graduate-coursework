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


def get_value(rows, source, metric):
    for row in rows:
        if row["source"] == source and row["metric"] == metric:
            return float(row["value"])
    raise ValueError(f"Missing row for {source} / {metric}")


def create_evidence_figure():
    rows = load_rows()

    wake_reduction = get_value(
        rows, "CooperBaldock2025_WakeAStar", "Energy reduction upper bound (%)"
    )
    khalasi_low = get_value(
        rows, "Gadhvi2025_Khalasi", "Energy conservation lower bound (%)"
    )
    khalasi_high = get_value(
        rows, "Gadhvi2025_Khalasi", "Energy conservation upper bound (%)"
    )

    overhead_low = get_value(
        rows, "CooperBaldock2025_WakeAStar", "Energy overhead lower bound (%)"
    )
    overhead_high = get_value(
        rows, "CooperBaldock2025_WakeAStar", "Energy overhead upper bound (%)"
    )
    path_low = get_value(
        rows, "CooperBaldock2025_WakeAStar", "Path suboptimality lower bound (%)"
    )
    path_high = get_value(
        rows, "CooperBaldock2025_WakeAStar", "Path suboptimality upper bound (%)"
    )

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8), constrained_layout=True)
    fig.patch.set_facecolor(WHITE)

    # Panel A: energy conservation ranges from published ASV/AUV papers
    labels_a = ["Wake-informed A*\n(AUV)", "Khalasi SAC\n(ASV vortical flow)"]
    means_a = [wake_reduction, (khalasi_low + khalasi_high) / 2.0]
    yerr_a = [0.0, (khalasi_high - khalasi_low) / 2.0]

    x0 = np.arange(len(labels_a))
    bars_a = axes[0].bar(
        x0,
        means_a,
        yerr=yerr_a,
        capsize=6,
        color=[ATLANTIC, HORSESHOE],
        edgecolor=BLACK,
        linewidth=1.0,
    )
    axes[0].set_xticks(x0)
    axes[0].set_xticklabels(labels_a, fontsize=9)
    axes[0].set_ylabel("Reported energy conservation (%)")
    axes[0].set_title("Published Energy Savings in Marine Navigation")
    axes[0].set_ylim(0, max(means_a) + max(yerr_a) + 10)
    axes[0].grid(axis="y", linestyle="-", linewidth=0.7, color=NEUTRAL_30)
    axes[0].set_axisbelow(True)

    axes[0].text(
        bars_a[0].get_x() + bars_a[0].get_width() / 2,
        means_a[0] + 1.0,
        f"{wake_reduction:.1f}",
        ha="center",
        va="bottom",
        fontsize=8,
        color=BLACK,
    )
    axes[0].text(
        bars_a[1].get_x() + bars_a[1].get_width() / 2,
        means_a[1] + yerr_a[1] + 1.0,
        f"{khalasi_low:.0f}-{khalasi_high:.0f}",
        ha="center",
        va="bottom",
        fontsize=8,
        color=BLACK,
    )

    # Panel B: trade-offs when replacing wake-informed planner with NN surrogates
    labels_b = ["Energy overhead\n(NN surrogate)", "Path suboptimality\n(NN surrogate)"]
    lows_b = [overhead_low, path_low]
    highs_b = [overhead_high, path_high]
    means_b = [(l + h) / 2.0 for l, h in zip(lows_b, highs_b)]
    yerr_b = [(h - l) / 2.0 for l, h in zip(lows_b, highs_b)]

    x1 = np.arange(len(labels_b))
    bars_b = axes[1].bar(
        x1,
        means_b,
        yerr=yerr_b,
        capsize=6,
        color=[GARNET, HONEYCOMB],
        edgecolor=BLACK,
        linewidth=1.0,
    )
    axes[1].set_xticks(x1)
    axes[1].set_xticklabels(labels_b, fontsize=9)
    axes[1].set_ylabel("Reported increase relative to wake-informed A* (%)")
    axes[1].set_title("Published Trade-Off Ranges (Same AUV Study)")
    axes[1].set_ylim(0, max(means_b) + max(yerr_b) + 8)
    axes[1].grid(axis="y", linestyle="-", linewidth=0.7, color=NEUTRAL_30)
    axes[1].set_axisbelow(True)

    for bar, lo, hi in zip(bars_b, lows_b, highs_b):
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            hi + 0.8,
            f"{lo:.2f}-{hi:.2f}",
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
        "Published Quantitative Evidence for Energy-Aware Marine Policies",
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
