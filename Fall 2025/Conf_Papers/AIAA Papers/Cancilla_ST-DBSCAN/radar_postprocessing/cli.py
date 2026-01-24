"""
Command-line interface for radar post-processing.

Provides commands for processing radar data with configurable
noise, dropout, and clutter effects.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import numpy as np


def cmd_process(args: argparse.Namespace) -> int:
    """Execute the process command.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 for success).
    """
    from .processor import create_processor

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: Input path does not exist: {input_path}")
        return 1

    # Load configuration
    config_path = Path(args.config) if args.config else None
    annotation_path = Path(args.annotation) if args.annotation else None

    print(f"Processing radar data:")
    print(f"  Input:  {input_path}")
    print(f"  Output: {output_path}")
    if config_path:
        print(f"  Config: {config_path}")
    if annotation_path:
        print(f"  Annotations: {annotation_path}")

    try:
        processor = create_processor(
            config_path=config_path,
            annotation_path=annotation_path,
        )

        ground_truth_path = Path(args.ground_truth) if args.ground_truth else None

        summary = processor.process_csv_directory(
            input_dir=input_path,
            output_dir=output_path,
            ground_truth_path=ground_truth_path,
            max_frames=args.max_frames,
            output_format=args.format,
        )

        print(f"\nProcessing complete:")
        print(f"  Frames processed: {summary['num_frames']}")
        print(f"  Total points: {summary['total_points']}")

        if summary.get("dropout_summary"):
            ds = summary["dropout_summary"]
            print(f"  Dropouts: {ds.get('total_dropouts', 0)}")

        print(f"\nOutput saved to: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


def cmd_convert(args: argparse.Namespace) -> int:
    """Execute the convert command.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 for success).
    """
    from .convert import create_converter

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: Input path does not exist: {input_path}")
        return 1

    print(f"Converting radar data:")
    print(f"  Input:  {input_path}")
    print(f"  Output: {output_path}")
    print(f"  Format: {args.format}")

    try:
        converter = create_converter(
            image_size=args.image_size,
            intensity_threshold=args.intensity_threshold,
        )

        converter.convert_and_save(
            input_path=input_path,
            output_path=output_path,
            output_format=args.format,
            include_polar=args.include_polar,
        )

        print(f"\nConversion complete: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


def cmd_evaluate(args: argparse.Namespace) -> int:
    """Execute the evaluate command.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 for success).
    """
    from .metrics import MetricsEvaluator

    predictions_path = Path(args.predictions)
    ground_truth_path = Path(args.ground_truth)

    if not predictions_path.exists():
        print(f"Error: Predictions file does not exist: {predictions_path}")
        return 1

    if not ground_truth_path.exists():
        print(f"Error: Ground truth file does not exist: {ground_truth_path}")
        return 1

    print(f"Evaluating tracking performance:")
    print(f"  Predictions:   {predictions_path}")
    print(f"  Ground truth:  {ground_truth_path}")

    try:
        # Load data based on file type
        if predictions_path.suffix == ".npy":
            pred_data = np.load(predictions_path)
        else:
            with open(predictions_path, "r") as f:
                pred_data = json.load(f)

        with open(ground_truth_path, "r") as f:
            gt_data = json.load(f)

        evaluator = MetricsEvaluator(distance_threshold=args.distance_threshold)

        # Compute clustering metrics if labels are available
        if isinstance(pred_data, np.ndarray) and pred_data.shape[1] >= 5:
            # Assume columns: x, y, intensity, frame_id, cluster_label
            cluster_labels = pred_data[:, 4].astype(int)
            # Ground truth labels would need to be in a separate file
            if "point_labels" in gt_data:
                gt_labels = np.array(gt_data["point_labels"])
                clustering_metrics = evaluator.evaluate_clustering(
                    cluster_labels, gt_labels
                )
                print(f"\nClustering Metrics:")
                print(f"  Purity: {clustering_metrics.purity:.4f}")
                print(f"  Num clusters: {clustering_metrics.num_clusters}")
                print(f"  Num ground truth: {clustering_metrics.num_ground_truth}")

        # Compute tracking metrics if track data is available
        if "tracks" in gt_data or "track_assignments" in gt_data:
            track_assignments = gt_data.get("track_assignments", {})
            gt_tracks = gt_data.get("ground_truth_tracks", {})

            # Convert string keys to int if needed
            track_assignments = {
                int(k): v for k, v in track_assignments.items()
            }
            gt_tracks = {int(k): v for k, v in gt_tracks.items()}

            tracking_metrics = evaluator.evaluate_tracking(
                track_assignments, gt_tracks
            )

            print(f"\nTracking Metrics:")
            print(f"  Continuity: {tracking_metrics.continuity:.4f}")
            print(f"  Num tracks: {tracking_metrics.num_tracks}")
            print(f"  Num GT tracks: {tracking_metrics.num_ground_truth_tracks}")
            print(f"  ID switches: {tracking_metrics.num_id_switches}")
            print(f"  Fragmentations: {tracking_metrics.num_fragmentations}")
            print(f"  Mostly tracked: {tracking_metrics.mostly_tracked}")
            print(f"  Mostly lost: {tracking_metrics.mostly_lost}")

            if tracking_metrics.mota is not None:
                print(f"  MOTA: {tracking_metrics.mota:.4f}")
            if tracking_metrics.motp is not None:
                print(f"  MOTP: {tracking_metrics.motp:.4f}")

        # Save results if output specified
        if args.output:
            output_path = Path(args.output)
            summary = evaluator.summary(
                clustering_metrics if "clustering_metrics" in dir() else None,
                tracking_metrics if "tracking_metrics" in dir() else None,
            )
            with open(output_path, "w") as f:
                json.dump(summary, f, indent=2)
            print(f"\nResults saved to: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


def cmd_info(args: argparse.Namespace) -> int:
    """Execute the info command to show config file format.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 for success).
    """
    example_config = '''# Radar Post-Processing Configuration
# =====================================

name = "scenario_a"
description = "High noise, moderate dropout scenario"
seed = 42  # Global random seed

[noise]
sigma_range = 1.5      # Range noise standard deviation (bins)
sigma_azimuth = 3.0    # Azimuth noise standard deviation (ticks)

[dropout]
dropout_rate = 0.15           # Probability of dropping object per frame
min_consecutive_frames = 2    # Min frames before eligible for dropout

[clutter]
clutter_density = 8.0         # Average clutter points per frame
intensity_min = 180           # Minimum clutter intensity
intensity_max = 255           # Maximum clutter intensity
cluster_probability = 0.4     # Probability of clustered clutter

[conversion]
image_size = 1736             # Image size for coordinate conversion
intensity_threshold = 10      # Minimum intensity to include
'''

    print("Example TOML configuration file:")
    print("=" * 50)
    print(example_config)
    print("=" * 50)
    print("\nSave this to a .toml file and use with:")
    print("  python -m radar_postprocessing process --config config.toml ...")

    return 0


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser.

    Returns:
        Configured ArgumentParser.
    """
    parser = argparse.ArgumentParser(
        prog="radar_postprocessing",
        description="Post-processing tools for synthetic radar data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process CSV data with configuration file
  python -m radar_postprocessing process \\
    --input ./scenario_a_raw \\
    --output ./scenario_a_processed \\
    --config configs/scenario_a.toml

  # Convert CSV to point cloud
  python -m radar_postprocessing convert \\
    --input ./raw_data \\
    --output ./points.npy \\
    --format npy

  # Evaluate tracking performance
  python -m radar_postprocessing evaluate \\
    --predictions ./results/tracks.json \\
    --ground-truth ./ground_truth.json

  # Show configuration file format
  python -m radar_postprocessing info
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Process command
    process_parser = subparsers.add_parser(
        "process",
        help="Process radar data with noise, dropout, and clutter",
    )
    process_parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input directory containing CSV files",
    )
    process_parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output directory for processed data",
    )
    process_parser.add_argument(
        "-c", "--config",
        help="TOML configuration file",
    )
    process_parser.add_argument(
        "-a", "--annotation",
        help="Path to annotation.json for water regions",
    )
    process_parser.add_argument(
        "-g", "--ground-truth",
        help="Path to ground truth JSON file",
    )
    process_parser.add_argument(
        "--max-frames",
        type=int,
        help="Maximum number of frames to process",
    )
    process_parser.add_argument(
        "--format",
        choices=["npy", "json"],
        default="npy",
        help="Output format (default: npy)",
    )

    # Convert command
    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert radar data between formats",
    )
    convert_parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input CSV file or directory",
    )
    convert_parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output file path",
    )
    convert_parser.add_argument(
        "--format",
        choices=["npy", "json"],
        default="npy",
        help="Output format (default: npy)",
    )
    convert_parser.add_argument(
        "--image-size",
        type=int,
        default=1736,
        help="Image size for coordinate conversion (default: 1736)",
    )
    convert_parser.add_argument(
        "--intensity-threshold",
        type=int,
        default=0,
        help="Minimum intensity threshold (default: 0)",
    )
    convert_parser.add_argument(
        "--include-polar",
        action="store_true",
        help="Include polar coordinates in output",
    )

    # Evaluate command
    evaluate_parser = subparsers.add_parser(
        "evaluate",
        help="Evaluate tracking/clustering performance",
    )
    evaluate_parser.add_argument(
        "-p", "--predictions",
        required=True,
        help="Predictions file (NPY or JSON)",
    )
    evaluate_parser.add_argument(
        "-g", "--ground-truth",
        required=True,
        help="Ground truth JSON file",
    )
    evaluate_parser.add_argument(
        "-o", "--output",
        help="Output file for metrics JSON",
    )
    evaluate_parser.add_argument(
        "--distance-threshold",
        type=float,
        default=50.0,
        help="Distance threshold for matching (default: 50.0)",
    )

    # Info command
    info_parser = subparsers.add_parser(
        "info",
        help="Show configuration file format",
    )

    return parser


def main(argv: Optional[list] = None) -> int:
    """Main entry point.

    Args:
        argv: Command-line arguments (defaults to sys.argv).

    Returns:
        Exit code.
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    commands = {
        "process": cmd_process,
        "convert": cmd_convert,
        "evaluate": cmd_evaluate,
        "info": cmd_info,
    }

    if args.command in commands:
        return commands[args.command](args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
