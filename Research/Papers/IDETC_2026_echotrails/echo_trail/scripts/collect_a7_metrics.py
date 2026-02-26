#!/usr/bin/env python3
"""Collect evaluation metrics for A7 (target proximity) from YOLO inference predictions.

A7 tests how well the GP model detects two close targets at varying separations
(10m to 300m). For each configuration, there are exactly 2 ground-truth targets,
and the key metrics track whether both targets are detected or if they merge
into a single detection at close separations.

Expected directory layout
-------------------------
predictions/
  a7_sep_10m/
    labels/          # YOLO prediction .txt files
    labels_gt/       # Ground-truth .txt files
  a7_sep_10m_noclutter/
    labels/
    labels_gt/
  ...
  a7_sep_300m/
  a7_sep_300m_noclutter/

File format (YOLO normalized coordinates, 0-1)
-----------------------------------------------
Predictions:  class x_center y_center width height confidence
Ground-truth: class x_center y_center width height

Metrics per frame (each frame has 2 GT boxes)
----------------------------------------------
  recall_2:         Fraction of frames where BOTH targets are detected
                    (2 predictions matched to 2 GTs, IoU >= 0.5).
  merge_rate:       Fraction of frames where 1 prediction matches 2 GTs
                    (targets merged).
  miss_rate:        Fraction of frames where 0 predictions match any GT.
  mean_n_predictions: Average number of predictions per frame.
  n_frames:         Total number of frames processed for this config.

Matching logic
--------------
For each frame:
  1. Load GT boxes and prediction boxes
  2. Compute IoU matrix between all predictions and all GTs
  3. Use greedy matching (highest IoU first) with threshold 0.5
  4. Count n_matched = number of GT boxes matched
  5. If n_matched == 2 → both detected; if n_matched == 1 → merge; if n_matched == 0 → miss

Output CSV
----------
  a7_metrics.csv with columns:
    separation_m, variant, recall_2, merge_rate, miss_rate, mean_n_predictions, n_frames

Usage
-----
    python collect_a7_metrics.py \\
        --predictions-dir ~/echotrail_ablation/a7_eval/predictions \\
        --output ~/echotrail_ablation/a7_eval/a7_metrics.csv
"""

import argparse
import sys
import re
from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

IoU_THRESHOLD = 0.5


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def compute_iou(box1: tuple, box2: tuple) -> float:
    """Compute IoU between two boxes in YOLO format (normalized coordinates).

    Parameters
    ----------
    box1, box2 : tuple
        (x_center, y_center, width, height) in normalized coordinates [0, 1].

    Returns
    -------
    iou : float
        Intersection over union in [0, 1].
    """
    x1_c, y1_c, w1, h1 = box1
    x2_c, y2_c, w2, h2 = box2

    x1_min = x1_c - w1 / 2
    x1_max = x1_c + w1 / 2
    y1_min = y1_c - h1 / 2
    y1_max = y1_c + h1 / 2

    x2_min = x2_c - w2 / 2
    x2_max = x2_c + w2 / 2
    y2_min = y2_c - h2 / 2
    y2_max = y2_c + h2 / 2

    xi_min = max(x1_min, x2_min)
    xi_max = min(x1_max, x2_max)
    yi_min = max(y1_min, y2_min)
    yi_max = min(y1_max, y2_max)

    if xi_max <= xi_min or yi_max <= yi_min:
        return 0.0

    inter_area = (xi_max - xi_min) * (yi_max - yi_min)
    box1_area = w1 * h1
    box2_area = w2 * h2
    union_area = box1_area + box2_area - inter_area

    if union_area == 0.0:
        return 0.0

    return inter_area / union_area


def load_boxes_from_file(file_path: Path) -> list[tuple]:
    """Load boxes from a YOLO format text file.

    Parameters
    ----------
    file_path : Path
        Path to a .txt file in YOLO format (one box per line):
        class x_center y_center width height [confidence]

    Returns
    -------
    boxes : list of tuples
        Each tuple is (x_center, y_center, width, height) as floats.
    """
    boxes = []
    if not file_path.exists():
        return boxes

    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) < 5:
                    continue
                x_c = float(parts[1])
                y_c = float(parts[2])
                w = float(parts[3])
                h = float(parts[4])
                boxes.append((x_c, y_c, w, h))
    except Exception as exc:
        print(f"  [WARN] Error reading {file_path}: {exc}", file=sys.stderr)

    return boxes


def greedy_match(pred_boxes: list[tuple], gt_boxes: list[tuple]) -> tuple[list[int], list[int]]:
    """Perform greedy matching of predictions to ground-truth boxes using IoU.

    Parameters
    ----------
    pred_boxes : list of tuples
        Prediction boxes (x_c, y_c, w, h).
    gt_boxes : list of tuples
        Ground-truth boxes (x_c, y_c, w, h).

    Returns
    -------
    pred_matched : list of int
        Indices of predictions that were matched to a GT (IoU >= 0.5).
    gt_matched : list of int
        Indices of GTs that were matched to a prediction (IoU >= 0.5).
    """
    pred_matched = []
    gt_matched = []

    if not pred_boxes or not gt_boxes:
        return pred_matched, gt_matched

    iou_matrix = np.zeros((len(pred_boxes), len(gt_boxes)))
    for i, pb in enumerate(pred_boxes):
        for j, gb in enumerate(gt_boxes):
            iou_matrix[i, j] = compute_iou(pb, gb)

    matched_pairs = []
    while True:
        best_i, best_j = np.unravel_index(iou_matrix.argmax(), iou_matrix.shape)
        best_iou = iou_matrix[best_i, best_j]

        if best_iou < IoU_THRESHOLD:
            break

        matched_pairs.append((best_i, best_j))
        iou_matrix[best_i, :] = -1
        iou_matrix[:, best_j] = -1

    for pred_idx, gt_idx in matched_pairs:
        if pred_idx not in pred_matched:
            pred_matched.append(pred_idx)
        if gt_idx not in gt_matched:
            gt_matched.append(gt_idx)

    return pred_matched, gt_matched


# ---------------------------------------------------------------------------
# Processing
# ---------------------------------------------------------------------------

def parse_config_name(dir_name: str) -> tuple[float, str] | None:
    """Parse separation and variant from a directory name.

    Parameters
    ----------
    dir_name : str
        Directory name like 'a7_sep_10m' or 'a7_sep_10m_noclutter'.

    Returns
    -------
    separation_m : float
        Separation in meters.
    variant : str
        Variant name (e.g., 'default' or 'noclutter').
    """
    match = re.match(r"a7_sep_(\d+)m(?:_(.+))?$", dir_name)
    if not match:
        return None

    separation = float(match.group(1))
    variant = match.group(2) if match.group(2) else "default"

    return separation, variant


def process_config(config_dir: Path) -> dict | None:
    """Process a single A7 configuration directory.

    Parameters
    ----------
    config_dir : Path
        Directory containing 'labels/' (predictions) and 'labels_gt/' (ground-truth).

    Returns
    -------
    metrics : dict
        Dictionary with keys: 'recall_2', 'merge_rate', 'miss_rate',
        'mean_n_predictions', 'n_frames'.
        Returns None if no frames are found.
    """
    pred_dir = config_dir / "labels"
    gt_dir = config_dir / "labels_gt"

    if not pred_dir.exists() or not gt_dir.exists():
        print(
            f"  [WARN] Missing labels or labels_gt in {config_dir.name}",
            file=sys.stderr,
        )
        return None

    pred_files = sorted(pred_dir.glob("*.txt"))
    if not pred_files:
        print(f"  [WARN] No prediction files in {pred_dir}", file=sys.stderr)
        return None

    recall_2_count = 0
    merge_count = 0
    miss_count = 0
    total_n_predictions = 0
    n_frames = 0

    for pred_file in pred_files:
        frame_name = pred_file.stem
        gt_file = gt_dir / f"{frame_name}.txt"

        pred_boxes = load_boxes_from_file(pred_file)
        gt_boxes = load_boxes_from_file(gt_file)

        total_n_predictions += len(pred_boxes)

        _, gt_matched = greedy_match(pred_boxes, gt_boxes)
        n_matched = len(gt_matched)

        if n_matched == 2:
            recall_2_count += 1
        elif n_matched == 1:
            merge_count += 1
        elif n_matched == 0:
            miss_count += 1

        n_frames += 1

    if n_frames == 0:
        return None

    mean_n_predictions = total_n_predictions / n_frames

    return {
        "recall_2": recall_2_count / n_frames,
        "merge_rate": merge_count / n_frames,
        "miss_rate": miss_count / n_frames,
        "mean_n_predictions": mean_n_predictions,
        "n_frames": n_frames,
    }


def collect_all_configs(predictions_dir: Path) -> pd.DataFrame | None:
    """Collect metrics from all A7 configuration directories.

    Parameters
    ----------
    predictions_dir : Path
        Root directory containing a7_sep_*/ subdirectories.

    Returns
    -------
    df : pd.DataFrame or None
        DataFrame with one row per unique (separation, variant) pair,
        or None if no configs are processed.
    """
    config_dirs = sorted(
        p for p in predictions_dir.iterdir()
        if p.is_dir() and p.name.startswith("a7_sep_")
    )

    if not config_dirs:
        print(
            f"[WARN] No a7_sep_* directories found in {predictions_dir}",
            file=sys.stderr,
        )
        return None

    rows = []
    for config_dir in config_dirs:
        parsed = parse_config_name(config_dir.name)
        if parsed is None:
            print(
                f"  [WARN] Could not parse directory name: {config_dir.name}",
                file=sys.stderr,
            )
            continue

        separation, variant = parsed
        print(f"  Processing: {config_dir.name} (sep={separation}m, variant={variant})")

        metrics = process_config(config_dir)
        if metrics is None:
            print(
                f"    [WARN] No frames processed for {config_dir.name}",
                file=sys.stderr,
            )
            continue

        rows.append({
            "separation_m": separation,
            "variant": variant,
            "recall_2": metrics["recall_2"],
            "merge_rate": metrics["merge_rate"],
            "miss_rate": metrics["miss_rate"],
            "mean_n_predictions": metrics["mean_n_predictions"],
            "n_frames": metrics["n_frames"],
        })

    if not rows:
        return None

    df = pd.DataFrame(rows)
    df = df.sort_values(["separation_m", "variant"]).reset_index(drop=True)

    return df


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def run(predictions_dir: Path, output_path: Path) -> None:
    """Drive the full collection pipeline.

    Parameters
    ----------
    predictions_dir : Path
        Root directory containing a7_sep_*/ subdirectories.
    output_path : Path
        Path where the output CSV will be written.
    """
    if not predictions_dir.exists():
        print(
            f"[ERROR] Predictions directory not found: {predictions_dir}",
            file=sys.stderr,
        )
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\nCollecting A7 metrics from: {predictions_dir}")

    df = collect_all_configs(predictions_dir)

    if df is None or df.empty:
        print("[WARN] No results collected; no output written.", file=sys.stderr)
        sys.exit(1)

    df.to_csv(output_path, index=False, float_format="%.6f")
    print(f"\nSaved A7 metrics to: {output_path}")

    print("\n--- Summary ---")
    for _, row in df.iterrows():
        sep = row["separation_m"]
        variant = row["variant"]
        recall_2 = row["recall_2"]
        merge_rate = row["merge_rate"]
        miss_rate = row["miss_rate"]
        mean_n = row["mean_n_predictions"]
        n_frames = row["n_frames"]

        print(
            f"  {sep:5.0f}m {variant:12s}  "
            f"recall_2={recall_2:.4f}  merge={merge_rate:.4f}  "
            f"miss={miss_rate:.4f}  mean_n_pred={mean_n:.2f}  "
            f"n_frames={n_frames}"
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """Construct and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="collect_a7_metrics",
        description=(
            "Collect evaluation metrics for A7 (target proximity) from YOLO "
            "inference predictions on close-target detection tasks."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--predictions-dir",
        required=True,
        metavar="DIR",
        help=(
            "Root directory of A7 prediction outputs. "
            "Expected structure: <predictions-dir>/a7_sep_*m[_variant]/{labels,labels_gt}/"
        ),
    )
    parser.add_argument(
        "--output",
        required=True,
        metavar="FILE",
        help="Path where the output a7_metrics.csv file will be written.",
    )

    return parser


def main() -> None:
    """Entry point."""
    parser = build_parser()
    args = parser.parse_args()

    run(
        predictions_dir=Path(args.predictions_dir).resolve(),
        output_path=Path(args.output).resolve(),
    )


if __name__ == "__main__":
    main()
