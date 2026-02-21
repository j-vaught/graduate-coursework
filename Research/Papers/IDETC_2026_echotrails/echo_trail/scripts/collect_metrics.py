#!/usr/bin/env python3
"""Collect and aggregate YOLOv8 training metrics for the echo trails ablation study.

Walks the training output directory tree, reads results.csv from each seed run,
extracts the best-epoch values (the row with the highest mAP50), and computes
mean and 95% CI across the three seeds (1000, 2000, 3000) for each condition.

Expected directory layout
-------------------------
training/
  <ABLATION_NAME>/
    <CONDITION_NAME>/
      seed_1000/
        run/
          results.csv
      seed_2000/
        run/
          results.csv
      seed_3000/
        run/
          results.csv

YOLOv8 results.csv columns used
--------------------------------
  epoch
  metrics/precision(B)
  metrics/recall(B)
  metrics/mAP50(B)        <- primary metric; best epoch is argmax of this column

Derived metric
--------------
  F1 = 2 * precision * recall / (precision + recall)

Confidence interval
-------------------
  95% CI with n=3 seeds (df=2): mean ± t_crit * (std / sqrt(n))
  t_crit for 95% two-tailed, df=2 is approx 4.303.

Output CSVs
-----------
  <output_dir>/<ablation_name>.csv
      columns: condition, mAP50_mean, mAP50_ci, precision_mean, precision_ci,
               recall_mean, recall_ci, f1_mean, f1_ci
  <output_dir>/summary.csv
      one row per ablation: ablation, best_condition, mAP50_mean, mAP50_ci,
      precision_mean, precision_ci, recall_mean, recall_ci, f1_mean, f1_ci

Usage
-----
    python collect_metrics.py \
        --training-dir /path/to/training \
        --output-dir   /path/to/results \
        --ablation     all

    python collect_metrics.py \
        --training-dir /path/to/training \
        --output-dir   /path/to/results \
        --ablation     a1_trail_length \
        --best
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t as t_dist


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# YOLOv8 column names in results.csv
COL_MAP50     = "metrics/mAP50(B)"
COL_PRECISION = "metrics/precision(B)"
COL_RECALL    = "metrics/recall(B)"

# t-critical value for 95% two-tailed CI, df = n - 1 = 2 (n = 3 seeds)
N_SEEDS  = 3
DF       = N_SEEDS - 1          # 2
T_CRIT   = t_dist.ppf(0.975, df=DF)   # ≈ 4.303


# ---------------------------------------------------------------------------
# Statistical helpers
# ---------------------------------------------------------------------------

def mean_and_ci(values: list[float]) -> tuple[float, float]:
    """Return (mean, 95% CI half-width) for a small sample using t-distribution.

    Parameters
    ----------
    values:
        Sample observations (length n).

    Returns
    -------
    mean : float
    ci   : float
        Half-width of the 95% confidence interval: t_crit * std / sqrt(n).
        Returns 0.0 if only one value is provided (no variance estimate).
    """
    arr = np.array(values, dtype=float)
    n   = len(arr)
    mu  = float(np.mean(arr))

    if n < 2:
        return mu, 0.0

    # Use the actual t_crit for the current df, not the hardcoded constant,
    # so the function generalises if n != 3.
    df_n    = n - 1
    t_crit  = float(t_dist.ppf(0.975, df=df_n))
    ci      = t_crit * float(np.std(arr, ddof=1)) / np.sqrt(n)
    return mu, ci


def f1_score(precision: float, recall: float) -> float:
    """Compute F1 from precision and recall. Returns 0.0 if denominator is zero."""
    denom = precision + recall
    if denom == 0.0:
        return 0.0
    return 2.0 * precision * recall / denom


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_best_epoch(results_csv: Path) -> dict[str, float] | None:
    """Load a YOLOv8 results.csv and return metrics at the best mAP50 epoch.

    Parameters
    ----------
    results_csv : Path
        Absolute path to results.csv.

    Returns
    -------
    dict with keys 'mAP50', 'precision', 'recall', 'f1', or None on failure.
    """
    if not results_csv.exists():
        print(f"  [WARN] Not found: {results_csv}", file=sys.stderr)
        return None

    try:
        df = pd.read_csv(results_csv)
    except Exception as exc:
        print(f"  [WARN] Cannot read {results_csv}: {exc}", file=sys.stderr)
        return None

    # Strip leading/trailing whitespace from column names (YOLOv8 sometimes
    # pads them with spaces).
    df.columns = [c.strip() for c in df.columns]

    required = {COL_MAP50, COL_PRECISION, COL_RECALL}
    missing  = required - set(df.columns)
    if missing:
        print(
            f"  [WARN] {results_csv} is missing columns: {missing}",
            file=sys.stderr,
        )
        return None

    # Best epoch = row with the highest mAP50
    best_idx  = df[COL_MAP50].idxmax()
    best_row  = df.loc[best_idx]

    precision = float(best_row[COL_PRECISION])
    recall    = float(best_row[COL_RECALL])

    return {
        "mAP50":     float(best_row[COL_MAP50]),
        "precision": precision,
        "recall":    recall,
        "f1":        f1_score(precision, recall),
    }


def collect_condition(condition_dir: Path) -> dict[str, tuple[float, float]] | None:
    """Aggregate metrics across all seed subdirectories for one condition.

    Parameters
    ----------
    condition_dir : Path
        Directory containing seed_1000/, seed_2000/, seed_3000/ subdirectories.

    Returns
    -------
    dict mapping metric names to (mean, ci) tuples, or None if no seeds found.
    """
    seed_dirs = sorted(condition_dir.glob("seed_*/"))
    if not seed_dirs:
        print(
            f"  [WARN] No seed directories found in {condition_dir}",
            file=sys.stderr,
        )
        return None

    per_metric: dict[str, list[float]] = {
        "mAP50":     [],
        "precision": [],
        "recall":    [],
        "f1":        [],
    }

    for seed_dir in seed_dirs:
        results_csv = seed_dir / "run" / "results.csv"
        metrics = load_best_epoch(results_csv)
        if metrics is None:
            print(
                f"  [WARN] Skipping seed {seed_dir.name} for {condition_dir.name}",
                file=sys.stderr,
            )
            continue
        for key in per_metric:
            per_metric[key].append(metrics[key])

    # Need at least one successful seed to report anything
    if not per_metric["mAP50"]:
        print(
            f"  [WARN] All seeds failed for {condition_dir.name}; skipping.",
            file=sys.stderr,
        )
        return None

    return {key: mean_and_ci(vals) for key, vals in per_metric.items()}


# ---------------------------------------------------------------------------
# Per-ablation processing
# ---------------------------------------------------------------------------

def process_ablation(ablation_dir: Path) -> pd.DataFrame | None:
    """Process all conditions under one ablation directory.

    Parameters
    ----------
    ablation_dir : Path
        Directory whose immediate subdirectories are condition names.

    Returns
    -------
    DataFrame with one row per condition, or None if no conditions succeed.
    """
    condition_dirs = sorted(
        p for p in ablation_dir.iterdir() if p.is_dir()
    )
    if not condition_dirs:
        print(f"  [WARN] No condition directories in {ablation_dir}", file=sys.stderr)
        return None

    rows = []
    for cond_dir in condition_dirs:
        print(f"    Condition: {cond_dir.name}")
        stats = collect_condition(cond_dir)
        if stats is None:
            continue

        rows.append({
            "condition":        cond_dir.name,
            "mAP50_mean":      stats["mAP50"][0],
            "mAP50_ci":        stats["mAP50"][1],
            "precision_mean":  stats["precision"][0],
            "precision_ci":    stats["precision"][1],
            "recall_mean":     stats["recall"][0],
            "recall_ci":       stats["recall"][1],
            "f1_mean":         stats["f1"][0],
            "f1_ci":           stats["f1"][1],
        })

    if not rows:
        return None

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def run(training_dir: Path, output_dir: Path, ablation_filter: str, print_best: bool) -> None:
    """Drive the full collection pipeline.

    Parameters
    ----------
    training_dir   : Path to the root training output directory.
    output_dir     : Path where result CSVs will be written.
    ablation_filter: Ablation name to process, or "all" for every subdirectory.
    print_best     : If True, print the best condition per ablation to stdout.
    """
    if not training_dir.exists():
        print(f"[ERROR] Training directory not found: {training_dir}", file=sys.stderr)
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine which ablation directories to process
    if ablation_filter.lower() == "all":
        ablation_dirs = sorted(p for p in training_dir.iterdir() if p.is_dir())
    else:
        target = training_dir / ablation_filter
        if not target.exists():
            print(
                f"[ERROR] Ablation directory not found: {target}", file=sys.stderr
            )
            sys.exit(1)
        ablation_dirs = [target]

    if not ablation_dirs:
        print("[ERROR] No ablation directories found.", file=sys.stderr)
        sys.exit(1)

    summary_rows = []

    for ablation_dir in ablation_dirs:
        ablation_name = ablation_dir.name
        print(f"\nAblation: {ablation_name}")

        df = process_ablation(ablation_dir)

        if df is None or df.empty:
            print(f"  [WARN] No results for ablation '{ablation_name}'; skipping.")
            continue

        # Write per-ablation CSV
        out_csv = output_dir / f"{ablation_name}.csv"
        df.to_csv(out_csv, index=False, float_format="%.6f")
        print(f"  Saved: {out_csv}")

        # Identify the best condition (highest mAP50_mean)
        best_idx  = df["mAP50_mean"].idxmax()
        best_row  = df.loc[best_idx]
        best_cond = best_row["condition"]

        if print_best:
            print(
                f"  Best condition: {best_cond}  "
                f"(mAP50 = {best_row['mAP50_mean']:.4f} "
                f"+/- {best_row['mAP50_ci']:.4f})"
            )

        summary_rows.append({
            "ablation":        ablation_name,
            "best_condition":  best_cond,
            "mAP50_mean":     best_row["mAP50_mean"],
            "mAP50_ci":       best_row["mAP50_ci"],
            "precision_mean": best_row["precision_mean"],
            "precision_ci":   best_row["precision_ci"],
            "recall_mean":    best_row["recall_mean"],
            "recall_ci":      best_row["recall_ci"],
            "f1_mean":        best_row["f1_mean"],
            "f1_ci":          best_row["f1_ci"],
        })

    # Write summary CSV
    if summary_rows:
        summary_df  = pd.DataFrame(summary_rows)
        summary_csv = output_dir / "summary.csv"
        summary_df.to_csv(summary_csv, index=False, float_format="%.6f")
        print(f"\nSummary saved: {summary_csv}")

        if print_best:
            print("\n--- Best conditions per ablation ---")
            for _, row in summary_df.iterrows():
                print(
                    f"  {row['ablation']}: {row['best_condition']}  "
                    f"mAP50 = {row['mAP50_mean']:.4f} +/- {row['mAP50_ci']:.4f}"
                )
    else:
        print("\n[WARN] No results collected; summary.csv not written.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """Construct and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="collect_metrics",
        description=(
            "Extract YOLOv8 training metrics from ablation study runs and "
            "aggregate them into per-ablation CSVs with mean and 95% CI."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--training-dir",
        required=True,
        metavar="DIR",
        help=(
            "Root directory of YOLOv8 training outputs. "
            "Expected structure: <training-dir>/<ablation>/<condition>/seed_*/run/results.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        metavar="DIR",
        help="Directory where aggregated CSV files will be written.",
    )
    parser.add_argument(
        "--ablation",
        default="all",
        metavar="NAME",
        help=(
            "Name of a single ablation subdirectory to process, or 'all' to "
            "process every subdirectory under --training-dir. Default: all."
        ),
    )
    parser.add_argument(
        "--best",
        action="store_true",
        help=(
            "Print the best condition per ablation (highest mean mAP50) to "
            "stdout. Useful for scripted decision logic between ablations."
        ),
    )

    return parser


def main() -> None:
    """Entry point."""
    parser = build_parser()
    args   = parser.parse_args()

    run(
        training_dir   = Path(args.training_dir).resolve(),
        output_dir     = Path(args.output_dir).resolve(),
        ablation_filter= args.ablation,
        print_best     = args.best,
    )


if __name__ == "__main__":
    main()
