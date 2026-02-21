#!/usr/bin/env python3
"""Prepare YOLO training datasets from trail-rendered images and labels.

Organizes trail_images/ and trail_labels/ output from apply_trails.py into
the standard YOLO dataset directory structure with train/val splits and an
auto-generated data.yaml configuration file.

Single-condition usage:
    python prepare_datasets.py \\
        --images-dir /path/to/trail_images \\
        --labels-dir /path/to/trail_labels \\
        --output-dir /path/to/dataset \\
        --split-ratio 0.8 \\
        --seed 42

Batch usage (multiple condition subdirectories):
    python prepare_datasets.py \\
        --batch-dir /path/to/conditions_root \\
        --output-dir /path/to/datasets \\
        --split-ratio 0.8 \\
        --seed 42

Each condition subdirectory in --batch-dir must contain trail_images/ and
trail_labels/ subdirectories produced by apply_trails.py.
"""

import argparse
import random
import shutil
import sys
import yaml
from pathlib import Path
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------
# Core split and organize logic
# ---------------------------------------------------------------------------

def collect_paired_samples(
    images_dir: Path,
    labels_dir: Path,
) -> Tuple[List[Tuple[Path, Path]], List[str]]:
    """Return paired (image, label) paths and a list of warning strings.

    Only samples that have both an image (.png) and a matching label (.txt)
    are returned.  Unpaired files are reported as warnings.

    Args:
        images_dir: Directory containing input PNG images.
        labels_dir: Directory containing YOLO .txt label files.

    Returns:
        Tuple of (paired_samples, warnings) where paired_samples is a list
        of (image_path, label_path) tuples and warnings is a list of
        descriptive warning strings for missing counterparts.
    """
    image_paths = {p.stem: p for p in sorted(images_dir.glob("*.png"))}
    label_paths = {p.stem: p for p in sorted(labels_dir.glob("*.txt"))}

    warnings: List[str] = []
    pairs: List[Tuple[Path, Path]] = []

    for stem, img_path in image_paths.items():
        if stem in label_paths:
            pairs.append((img_path, label_paths[stem]))
        else:
            # Include images without labels as negative examples (empty label).
            # Create a temporary empty label file path marker; the actual empty
            # file will be written during the transfer step.
            pairs.append((img_path, None))

    for stem in label_paths:
        if stem not in image_paths:
            warnings.append(
                f"  WARNING: label '{label_paths[stem].name}' has no matching image -- skipped"
            )

    return pairs, warnings


def split_pairs(
    pairs: List[Tuple[Path, Path]],
    split_ratio: float,
    seed: int,
) -> Tuple[List[Tuple[Path, Path]], List[Tuple[Path, Path]]]:
    """Shuffle and split paired samples into train and val subsets.

    Args:
        pairs: List of (image_path, label_path) tuples.
        split_ratio: Fraction of samples to assign to train (0 < ratio < 1).
        seed: Random seed for reproducibility.

    Returns:
        Tuple of (train_pairs, val_pairs).
    """
    shuffled = list(pairs)
    random.seed(seed)
    random.shuffle(shuffled)

    n_train = max(1, round(len(shuffled) * split_ratio))
    return shuffled[:n_train], shuffled[n_train:]


def transfer_file(src: Path, dst: Path, use_symlink: bool) -> None:
    """Copy or symlink src to dst, creating parent directories as needed.

    Args:
        src: Source file path.
        dst: Destination file path.
        use_symlink: If True, create a relative symlink instead of copying.
    """
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() or dst.is_symlink():
        dst.unlink()
    if use_symlink:
        dst.symlink_to(src.resolve())
    else:
        shutil.copy2(src, dst)


def write_data_yaml(
    dataset_root: Path,
    class_names: Optional[List[str]] = None,
) -> Path:
    """Write a YOLO data.yaml file to dataset_root.

    Args:
        dataset_root: Absolute path to the dataset root directory.
        class_names: Ordered list of class name strings. Defaults to
            ['target'] if not provided.

    Returns:
        Path to the written data.yaml file.
    """
    if class_names is None:
        class_names = ["target"]

    names_dict = {i: name for i, name in enumerate(class_names)}

    config = {
        "path": str(dataset_root.resolve()),
        "train": "images/train",
        "val": "images/val",
        "names": names_dict,
    }

    yaml_path = dataset_root / "data.yaml"
    yaml_path.parent.mkdir(parents=True, exist_ok=True)
    with open(yaml_path, "w") as fh:
        yaml.dump(config, fh, default_flow_style=False, sort_keys=False)

    return yaml_path


def organize_dataset(
    images_dir: Path,
    labels_dir: Path,
    output_dir: Path,
    split_ratio: float,
    seed: int,
    use_symlink: bool,
    class_names: Optional[List[str]] = None,
    condition_label: str = "",
) -> None:
    """Organize a single condition into a YOLO dataset directory.

    Args:
        images_dir: Directory containing trail-rendered PNG images.
        labels_dir: Directory containing YOLO .txt label files.
        output_dir: Root directory for the YOLO dataset output.
        split_ratio: Fraction of samples assigned to train split.
        seed: Random seed for reproducible shuffling.
        use_symlink: If True, symlink files instead of copying.
        class_names: Class name list for data.yaml. Defaults to ['target'].
        condition_label: Human-readable label for printed diagnostics.
    """
    prefix = f"[{condition_label}] " if condition_label else ""

    # Validate input directories.
    if not images_dir.is_dir():
        print(f"{prefix}ERROR: images directory not found: {images_dir}")
        return
    if not labels_dir.is_dir():
        print(f"{prefix}ERROR: labels directory not found: {labels_dir}")
        return

    # Collect paired samples.
    pairs, warnings = collect_paired_samples(images_dir, labels_dir)

    for w in warnings:
        print(f"{prefix}{w}")

    if not pairs:
        print(f"{prefix}ERROR: no valid image/label pairs found -- skipping.")
        return

    # Split.
    train_pairs, val_pairs = split_pairs(pairs, split_ratio, seed)

    # Transfer files.
    transfer_mode = "symlink" if use_symlink else "copy"
    print(
        f"{prefix}Organizing {len(pairs)} samples "
        f"({len(train_pairs)} train / {len(val_pairs)} val) "
        f"via {transfer_mode} -> {output_dir}"
    )

    for img_path, lbl_path in train_pairs:
        transfer_file(img_path, output_dir / "images" / "train" / img_path.name, use_symlink)
        if lbl_path is not None:
            transfer_file(lbl_path, output_dir / "labels" / "train" / lbl_path.name, use_symlink)
        else:
            # Empty label file for negative (background-only) example.
            empty_lbl = output_dir / "labels" / "train" / f"{img_path.stem}.txt"
            empty_lbl.parent.mkdir(parents=True, exist_ok=True)
            empty_lbl.write_text("")

    for img_path, lbl_path in val_pairs:
        transfer_file(img_path, output_dir / "images" / "val" / img_path.name, use_symlink)
        if lbl_path is not None:
            transfer_file(lbl_path, output_dir / "labels" / "val" / lbl_path.name, use_symlink)
        else:
            empty_lbl = output_dir / "labels" / "val" / f"{img_path.stem}.txt"
            empty_lbl.parent.mkdir(parents=True, exist_ok=True)
            empty_lbl.write_text("")

    # Write data.yaml.
    yaml_path = write_data_yaml(output_dir, class_names)
    print(f"{prefix}Wrote data.yaml -> {yaml_path}")

    # Summary statistics.
    total = len(pairs)
    print(
        f"{prefix}Split statistics."
        f"  Total: {total}  |  "
        f"Train: {len(train_pairs)} ({100 * len(train_pairs) / total:.1f}%)  |  "
        f"Val: {len(val_pairs)} ({100 * len(val_pairs) / total:.1f}%)"
    )


# ---------------------------------------------------------------------------
# Batch mode
# ---------------------------------------------------------------------------

def find_condition_dirs(batch_dir: Path) -> List[Path]:
    """Return subdirectories of batch_dir that contain trail_images/ and trail_labels/.

    Args:
        batch_dir: Parent directory containing condition subdirectories.

    Returns:
        Sorted list of condition subdirectory paths.
    """
    candidates = sorted(
        d for d in batch_dir.iterdir()
        if d.is_dir()
        and (d / "trail_images").is_dir()
        and (d / "trail_labels").is_dir()
    )
    return candidates


def run_batch(
    batch_dir: Path,
    output_dir: Path,
    split_ratio: float,
    seed: int,
    use_symlink: bool,
    class_names: Optional[List[str]] = None,
) -> None:
    """Process all condition subdirectories found under batch_dir.

    Each condition produces its own YOLO dataset under output_dir/<condition_name>/.

    Args:
        batch_dir: Root directory containing one subdirectory per condition.
        output_dir: Root output directory for all condition datasets.
        split_ratio: Train split fraction.
        seed: Random seed.
        use_symlink: Use symlinks instead of copies.
        class_names: Class names for data.yaml files.
    """
    condition_dirs = find_condition_dirs(batch_dir)

    if not condition_dirs:
        print(
            f"ERROR: No valid condition directories (containing trail_images/ and "
            f"trail_labels/) found under: {batch_dir}"
        )
        sys.exit(1)

    print(f"Batch mode: found {len(condition_dirs)} condition(s) under {batch_dir}\n")

    for condition_dir in condition_dirs:
        condition_name = condition_dir.name
        condition_output = output_dir / condition_name
        organize_dataset(
            images_dir=condition_dir / "trail_images",
            labels_dir=condition_dir / "trail_labels",
            output_dir=condition_output,
            split_ratio=split_ratio,
            seed=seed,
            use_symlink=use_symlink,
            class_names=class_names,
            condition_label=condition_name,
        )
        print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Organize trail-rendered images and YOLO labels into a YOLO training "
            "dataset with train/val splits and an auto-generated data.yaml."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Single-condition inputs.
    single = parser.add_argument_group("Single-condition mode")
    single.add_argument(
        "--images-dir",
        type=Path,
        metavar="DIR",
        help="Directory containing trail-rendered PNG images (trail_images/).",
    )
    single.add_argument(
        "--labels-dir",
        type=Path,
        metavar="DIR",
        help="Directory containing YOLO .txt label files (trail_labels/).",
    )

    # Batch mode.
    batch = parser.add_argument_group("Batch mode")
    batch.add_argument(
        "--batch-dir",
        type=Path,
        metavar="DIR",
        help=(
            "Parent directory containing multiple condition subdirectories, each with "
            "trail_images/ and trail_labels/ subdirectories. When set, --images-dir "
            "and --labels-dir are ignored."
        ),
    )

    # Shared arguments.
    shared = parser.add_argument_group("Shared options")
    shared.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        metavar="DIR",
        help=(
            "Root output directory for the YOLO dataset. In batch mode, one "
            "subdirectory per condition is created here."
        ),
    )
    shared.add_argument(
        "--split-ratio",
        type=float,
        default=0.8,
        metavar="RATIO",
        help="Fraction of samples to assign to the train split. Default: 0.8.",
    )
    shared.add_argument(
        "--seed",
        type=int,
        default=42,
        metavar="INT",
        help="Random seed for reproducible train/val splits. Default: 42.",
    )
    shared.add_argument(
        "--symlink",
        action="store_true",
        default=False,
        help=(
            "Create symlinks to source files instead of copying them. Saves disk "
            "space but the dataset root must remain co-located with the source data."
        ),
    )
    shared.add_argument(
        "--class-names",
        nargs="+",
        default=["target"],
        metavar="NAME",
        help=(
            "Space-separated list of class names in class-index order. Written to "
            "data.yaml. Default: target."
        ),
    )

    return parser


def validate_args(args: argparse.Namespace) -> None:
    """Validate argument combinations and raise SystemExit on error.

    Args:
        args: Parsed argument namespace.
    """
    if args.batch_dir is None and (args.images_dir is None or args.labels_dir is None):
        print(
            "ERROR: Provide either --batch-dir or both --images-dir and --labels-dir."
        )
        sys.exit(1)

    if not (0.0 < args.split_ratio < 1.0):
        print(
            f"ERROR: --split-ratio must be strictly between 0 and 1, got {args.split_ratio}."
        )
        sys.exit(1)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    validate_args(args)

    if args.batch_dir is not None:
        run_batch(
            batch_dir=args.batch_dir,
            output_dir=args.output_dir,
            split_ratio=args.split_ratio,
            seed=args.seed,
            use_symlink=args.symlink,
            class_names=args.class_names,
        )
    else:
        organize_dataset(
            images_dir=args.images_dir,
            labels_dir=args.labels_dir,
            output_dir=args.output_dir,
            split_ratio=args.split_ratio,
            seed=args.seed,
            use_symlink=args.symlink,
            class_names=args.class_names,
        )


if __name__ == "__main__":
    main()
