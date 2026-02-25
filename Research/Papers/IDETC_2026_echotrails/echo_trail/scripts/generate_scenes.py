#!/usr/bin/env python3
"""Batch scene generation for the echo trail ablation study.

Invokes the radar-scene-augmentation pipeline (stages 1-4) for each
ablation condition and dataset. Outputs PNG images and YOLO labels
organized by ablation, scene name, and dataset.

Output structure:
    OUTPUT_BASE/
        a1_trail_length/
            stationary/
                lakemurray/
                    images/
                    YOLO_labels/
                charleston/
                    images/
                    YOLO_labels/
                combined/
                    images/
                    YOLO_labels/
            slow/ ...
        a2_decay/ ...
        ...

Usage:
    # Generate all ablations for both datasets
    python generate_scenes.py --ablation all

    # Single ablation, dry run
    python generate_scenes.py --ablation a1 --dry-run

    # Single dataset, custom output directory
    python generate_scenes.py --ablation a6 --dataset charleston \\
        --output-base ~/echotrail_ablation/scenes_out

    # Override repo and data locations
    python generate_scenes.py --ablation all \\
        --repo-dir ~/my_repos/radar-scene-augmentation/scene-generator \\
        --data-dir ~/my_repos/radar-scene-augmentation/data
"""

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Default paths
# ---------------------------------------------------------------------------

DEFAULT_REPO_DIR = Path.home() / "echotrail_ablation" / "repos" / \
    "radar-scene-augmentation" / "scene-generator"

DEFAULT_DATA_DIR = Path.home() / "echotrail_ablation" / "repos" / \
    "radar-scene-augmentation" / "data"

DEFAULT_OUTPUT_BASE = Path.home() / "echotrail_ablation" / "scenes_out"

# Scene configs live in scenes/ relative to this script
SCENES_DIR = Path(__file__).parent / "scenes"

# Subprocess timeout per pipeline invocation (seconds).  250 frames with
# 8 threads typically finishes in under 10 minutes; allow 30 for safety.
PIPELINE_TIMEOUT = 1800  # 30 minutes


# ---------------------------------------------------------------------------
# Dataset definitions
# ---------------------------------------------------------------------------

DATASETS: Dict[str, Dict[str, str]] = {
    "lakemurray": {
        "annotation":   "annotation_lakemurraydam.json",
        "library":      "object_library_lakemurraydam",
        "land_frames":  "land_frames_lakemurraydam",
    },
    "charleston": {
        "annotation":   "annotation_charleston.json",
        "library":      "object_library_charleston",
        "land_frames":  "land_frames_charleston",
    },
}


# ---------------------------------------------------------------------------
# Ablation definitions
# ---------------------------------------------------------------------------

# Maps ablation key -> subdirectory name under SCENES_DIR.
# Values are (ablation_dir, [scene_stem, ...]) pairs.
ABLATIONS: Dict[str, Tuple[str, List[str]]] = {
    "a1": ("a1_trail_length",   ["stationary", "slow", "medium", "fast"]),
    "a2": ("a2_decay",          ["base"]),
    "a3": ("a3_intensity",      ["mixed_rcs"]),
    "a4": ("a4_color",          ["mixed_rcs"]),
    "a5": ("a5_range",          [f"a5_{r}_scene_{i:02d}{s}"
                                 for r in ["near", "mid", "far"]
                                 for i in range(1, 11)
                                 for s in ["", "_noclutter"]]),
    "a6": ("a6_clutter",        [f"a6_scene_{i:02d}_{lvl}"
                                 for i in range(1, 11)
                                 for lvl in ["none", "low", "moderate", "heavy"]]),
    "a7": ("a7_proximity",      [f"sep_{m}m" for m in range(10, 110, 10)]),
    "a8": ("a8_crossing",       [f"angle_{a}" for a in [15, 30, 45, 60, 75, 90]]),
}


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def resolve_dataset_paths(
    dataset_key: str,
    data_dir: Path,
    land_frames_dir: Optional[Path],
) -> Dict[str, Path]:
    """Return resolved absolute paths for annotation, library, and land_frames.

    Args:
        dataset_key: One of "lakemurray" or "charleston".
        data_dir: Base directory that contains annotation JSON, library dir,
            and (optionally) land_frames dir.
        land_frames_dir: Optional override for the directory that holds land
            frame subdirectories.  If None, falls back to data_dir.

    Returns:
        Dict with keys "annotation", "library", "land_frames".
    """
    spec = DATASETS[dataset_key]
    lf_base = land_frames_dir if land_frames_dir is not None else data_dir
    return {
        "annotation":  data_dir / spec["annotation"],
        "library":     data_dir / spec["library"],
        "land_frames": lf_base / spec["land_frames"],
    }


def build_pipeline_command(
    repo_dir: Path,
    annotation: Path,
    land_frames: Path,
    library: Path,
    output: Path,
    scene_yaml: Path,
    seed: int,
    threads: int = 8,
) -> List[str]:
    """Construct the subprocess argument list for main.py."""
    return [
        sys.executable,
        str(repo_dir / "main.py"),
        "-a", str(annotation),
        "--land-frames", str(land_frames),
        "--library", str(library),
        "-o", str(output),
        "--scene", str(scene_yaml),
        "--png",
        "--export-labels",
        "--seed", str(seed),
        "--threads", str(threads),
    ]


def remove_csv_intermediates(output_dir: Path, verbose: bool = True) -> int:
    """Delete CSV files generated by Stage 3 of the pipeline.

    The pipeline writes per-frame CSVs before rendering PNGs in Stage 4.
    These are not needed after PNG generation and can be safely removed.

    Returns:
        Number of files deleted.
    """
    removed = 0
    for csv_file in output_dir.rglob("*.csv"):
        try:
            csv_file.unlink()
            removed += 1
        except OSError as exc:
            print(f"  [warn] Could not remove {csv_file}: {exc}", flush=True)
    if verbose and removed:
        print(f"  Removed {removed} CSV intermediate(s).", flush=True)
    return removed


def merge_dataset_outputs(
    dataset_dirs: Dict[str, Path],
    combined_dir: Path,
    use_symlinks: bool = True,
) -> None:
    """Merge images and labels from multiple dataset output dirs into one.

    Files from each dataset are copied (or symlinked) into combined_dir,
    with the dataset key prepended to the filename to avoid collisions.

    Args:
        dataset_dirs: Mapping of dataset_key -> pipeline output directory.
        combined_dir: Destination directory for the merged output.
        use_symlinks: If True, create symlinks instead of copying to save
            disk space.  Falls back to copying if the filesystem does not
            support symlinks.
    """
    for subdir in ("images", "YOLO_labels"):
        dest = combined_dir / subdir
        dest.mkdir(parents=True, exist_ok=True)

        for dataset_key, src_root in dataset_dirs.items():
            src = src_root / subdir
            if not src.exists():
                print(
                    f"  [warn] Merge: source directory not found: {src}",
                    flush=True,
                )
                continue

            for src_file in sorted(src.iterdir()):
                # Prepend dataset key so names are unique across datasets.
                dest_name = f"{dataset_key}_{src_file.name}"
                dest_file = dest / dest_name

                if dest_file.exists() or dest_file.is_symlink():
                    dest_file.unlink()

                if use_symlinks:
                    try:
                        dest_file.symlink_to(src_file.resolve())
                        continue
                    except (OSError, NotImplementedError):
                        pass  # fall through to copy

                shutil.copy2(src_file, dest_file)


def print_header(text: str) -> None:
    border = "=" * 60
    print(f"\n{border}", flush=True)
    print(f"  {text}", flush=True)
    print(border, flush=True)


def print_step(text: str) -> None:
    print(f"\n-- {text}", flush=True)


# ---------------------------------------------------------------------------
# Core run logic
# ---------------------------------------------------------------------------

def run_pipeline(
    cmd: List[str],
    env_repo_dir: Path,
    dry_run: bool,
    label: str,
) -> bool:
    """Invoke the pipeline subprocess.

    Args:
        cmd: Full argument list including sys.executable.
        env_repo_dir: Added to PYTHONPATH so the repo's modules resolve.
        dry_run: If True, print the command but do not execute.
        label: Human-readable label for progress output.

    Returns:
        True on success, False on failure.
    """
    import os

    if dry_run:
        print(f"  [dry-run] {label}", flush=True)
        print(f"  Command: {' '.join(cmd)}", flush=True)
        return True

    env = os.environ.copy()
    existing_pp = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        str(env_repo_dir) + os.pathsep + existing_pp
        if existing_pp else str(env_repo_dir)
    )

    t0 = time.monotonic()
    print(f"  Running: {label}", flush=True)
    print(f"  CMD: {' '.join(cmd)}", flush=True)

    try:
        result = subprocess.run(
            cmd,
            env=env,
            cwd=str(env_repo_dir),
            timeout=PIPELINE_TIMEOUT,
            check=False,            # handle returncode manually
            capture_output=False,   # let stdout/stderr pass through
        )
    except subprocess.TimeoutExpired:
        elapsed = time.monotonic() - t0
        print(
            f"  [error] Pipeline timed out after {elapsed:.0f}s: {label}",
            flush=True,
        )
        return False
    except FileNotFoundError as exc:
        print(f"  [error] Could not launch pipeline: {exc}", flush=True)
        return False

    elapsed = time.monotonic() - t0
    if result.returncode != 0:
        print(
            f"  [error] Pipeline exited with code {result.returncode} "
            f"after {elapsed:.0f}s: {label}",
            flush=True,
        )
        return False

    print(f"  Done ({elapsed:.1f}s): {label}", flush=True)
    return True


def generate_ablation(
    ablation_key: str,
    repo_dir: Path,
    data_dir: Path,
    land_frames_dir: Optional[Path],
    output_base: Path,
    datasets: List[str],
    seed: int,
    dry_run: bool,
    threads: int = 8,
) -> Dict[str, int]:
    """Generate all scene configs for one ablation across selected datasets.

    Returns:
        Dict with "success" and "failure" counts.
    """
    ablation_dir_name, scene_stems = ABLATIONS[ablation_key]
    scenes_subdir = SCENES_DIR / ablation_dir_name
    ablation_out = output_base / ablation_dir_name

    counts = {"success": 0, "failure": 0}

    for scene_stem in scene_stems:
        scene_yaml = scenes_subdir / f"{scene_stem}.yaml"
        if not scene_yaml.exists() and not dry_run:
            print(
                f"  [warn] Scene YAML not found, skipping: {scene_yaml}",
                flush=True,
            )
            counts["failure"] += 1
            continue

        print_step(f"{ablation_key} / {scene_stem}")

        scene_out = ablation_out / scene_stem
        dataset_out_dirs: Dict[str, Path] = {}

        for ds_key in datasets:
            ds_paths = resolve_dataset_paths(ds_key, data_dir, land_frames_dir)

            # Validate required paths unless dry-run
            if not dry_run:
                missing = [
                    str(p) for k, p in ds_paths.items()
                    if not p.exists()
                ]
                if missing:
                    print(
                        f"  [error] Missing paths for dataset '{ds_key}', "
                        f"skipping:\n    " + "\n    ".join(missing),
                        flush=True,
                    )
                    counts["failure"] += 1
                    continue

            ds_output = scene_out / ds_key
            ds_output.mkdir(parents=True, exist_ok=True)
            dataset_out_dirs[ds_key] = ds_output

            cmd = build_pipeline_command(
                repo_dir=repo_dir,
                annotation=ds_paths["annotation"],
                land_frames=ds_paths["land_frames"],
                library=ds_paths["library"],
                output=ds_output,
                scene_yaml=scene_yaml,
                seed=seed,
                threads=threads,
            )

            label = f"{ablation_key}/{scene_stem}/{ds_key}"
            ok = run_pipeline(cmd, repo_dir, dry_run, label)

            if ok:
                counts["success"] += 1
                if not dry_run:
                    remove_csv_intermediates(ds_output)
            else:
                counts["failure"] += 1

        # Merge outputs when multiple datasets were generated successfully.
        if len(dataset_out_dirs) > 1 and not dry_run:
            combined_dir = scene_out / "combined"
            print(f"  Merging into combined/: {combined_dir}", flush=True)
            merge_dataset_outputs(dataset_out_dirs, combined_dir)
        elif len(dataset_out_dirs) > 1 and dry_run:
            print(
                f"  [dry-run] Would merge {list(dataset_out_dirs.keys())} "
                f"into combined/",
                flush=True,
            )

    return counts


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Batch scene generation for the echo trail ablation study. "
            "Invokes the radar-scene-augmentation pipeline for each "
            "ablation condition and dataset."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--ablation",
        required=True,
        choices=list(ABLATIONS.keys()) + ["all"],
        help=(
            "Ablation to generate.  Use 'all' to run every ablation "
            "in sequence."
        ),
    )

    parser.add_argument(
        "--dataset",
        default="both",
        choices=["lakemurray", "charleston", "both"],
        help="Dataset(s) to generate scenes for.",
    )

    parser.add_argument(
        "--output-base",
        type=Path,
        default=DEFAULT_OUTPUT_BASE,
        help="Base output directory.  Ablation subdirs are created here.",
    )

    parser.add_argument(
        "--repo-dir",
        type=Path,
        default=DEFAULT_REPO_DIR,
        help=(
            "Path to the scene-generator subdirectory of the "
            "radar-scene-augmentation repo (contains main.py)."
        ),
    )

    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
        help=(
            "Base data directory containing annotation JSON files, "
            "object library dirs, and (optionally) land_frames dirs."
        ),
    )

    parser.add_argument(
        "--land-frames-dir",
        type=Path,
        default=None,
        help=(
            "Override the directory searched for land_frames_* "
            "subdirectories.  Defaults to --data-dir."
        ),
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed passed to the pipeline for reproducibility.",
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=8,
        help="Number of worker threads passed to the pipeline.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Print the pipeline commands that would be run without "
            "actually executing them."
        ),
    )

    return parser.parse_args()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    args = parse_args()

    # Resolve dataset list
    if args.dataset == "both":
        datasets = ["lakemurray", "charleston"]
    else:
        datasets = [args.dataset]

    # Resolve ablation list
    if args.ablation == "all":
        ablation_keys = list(ABLATIONS.keys())
    else:
        ablation_keys = [args.ablation]

    # Resolve all paths to absolute to avoid CWD-relative doubling.
    args.repo_dir = args.repo_dir.resolve()
    args.data_dir = args.data_dir.resolve()
    args.output_base = args.output_base.resolve()
    if args.land_frames_dir is not None:
        args.land_frames_dir = args.land_frames_dir.resolve()

    # Validate repo dir early (unless dry-run)
    if not args.dry_run:
        main_py = args.repo_dir / "main.py"
        if not main_py.exists():
            print(
                f"[error] Pipeline entry point not found: {main_py}\n"
                f"        Check --repo-dir (currently: {args.repo_dir})",
                file=sys.stderr,
            )
            return 1

    print_header(
        f"Echo Trail Ablation Scene Generator"
    )
    print(f"  Ablations : {ablation_keys}", flush=True)
    print(f"  Datasets  : {datasets}", flush=True)
    print(f"  Output    : {args.output_base}", flush=True)
    print(f"  Repo dir  : {args.repo_dir}", flush=True)
    print(f"  Data dir  : {args.data_dir}", flush=True)
    if args.land_frames_dir:
        print(f"  LF dir    : {args.land_frames_dir}", flush=True)
    print(f"  Seed      : {args.seed}", flush=True)
    print(f"  Threads   : {args.threads}", flush=True)
    print(f"  Dry run   : {args.dry_run}", flush=True)

    total_success = 0
    total_failure = 0
    wall_t0 = time.monotonic()

    for ablation_key in ablation_keys:
        ablation_dir_name = ABLATIONS[ablation_key][0]
        print_header(
            f"Ablation {ablation_key.upper()}  ({ablation_dir_name})"
        )

        counts = generate_ablation(
            ablation_key=ablation_key,
            repo_dir=args.repo_dir,
            data_dir=args.data_dir,
            land_frames_dir=args.land_frames_dir,
            output_base=args.output_base,
            datasets=datasets,
            seed=args.seed,
            dry_run=args.dry_run,
            threads=args.threads,
        )

        total_success += counts["success"]
        total_failure += counts["failure"]
        print(
            f"\n  {ablation_key}: {counts['success']} succeeded, "
            f"{counts['failure']} failed.",
            flush=True,
        )

    wall_elapsed = time.monotonic() - wall_t0
    print_header("Summary")
    print(f"  Total pipeline runs : {total_success + total_failure}", flush=True)
    print(f"  Succeeded           : {total_success}", flush=True)
    print(f"  Failed              : {total_failure}", flush=True)
    print(f"  Wall time           : {wall_elapsed:.1f}s", flush=True)

    return 0 if total_failure == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
