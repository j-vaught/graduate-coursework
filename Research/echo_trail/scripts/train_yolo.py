"""
train_yolo.py
-------------
YOLOv8-nano training launcher for the EchoTrails ablation study.

Manages GPU assignment and supports running multiple training jobs in
parallel across GPUs. Each condition is trained with multiple seeds;
after training only best.pt and results.csv are retained to conserve
disk space.

Usage examples
--------------
Single data.yaml, one GPU:
    python train_yolo.py \
        --data-yaml /data/condition_A/data.yaml \
        --output-dir /runs/ablation \
        --gpu 0

Batch directory, four GPUs, custom seeds:
    python train_yolo.py \
        --batch-dir /data/conditions/ \
        --output-dir /runs/ablation \
        --gpus 0,1,2,3 \
        --seeds 1000,2000,3000

Dry run to preview job assignments:
    python train_yolo.py \
        --batch-dir /data/conditions/ \
        --output-dir /runs/ablation \
        --gpus 0,1,2,3 \
        --dry-run
"""

import argparse
import logging
import os
import shutil
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Job definition
# ---------------------------------------------------------------------------

def _build_job_list(data_yamls, output_dir, seeds, gpu_list,
                    model, epochs, batch, imgsz, workers):
    """
    Build an ordered list of job dicts from (data_yaml, seed) combinations.

    GPUs are assigned round-robin: job_i -> gpu_list[i % len(gpu_list)].

    Parameters
    ----------
    data_yamls : list of Path
        One entry per ablation condition.
    output_dir : Path
        Root directory for all training outputs.
    seeds : list of int
    gpu_list : list of int
    model, epochs, batch, imgsz, workers : training hyperparameters

    Returns
    -------
    list of dict
        Each dict is a fully resolved job specification.
    """
    jobs = []
    job_idx = 0
    for yaml_path in sorted(data_yamls):
        condition_name = yaml_path.parent.name
        for seed in seeds:
            run_dir = output_dir / condition_name / f"seed_{seed}"
            gpu_id = gpu_list[job_idx % len(gpu_list)]
            jobs.append(dict(
                condition=condition_name,
                data_yaml=yaml_path,
                seed=seed,
                gpu=gpu_id,
                run_dir=run_dir,
                model=model,
                epochs=epochs,
                batch=batch,
                imgsz=imgsz,
                workers=workers,
            ))
            job_idx += 1
    return jobs


# ---------------------------------------------------------------------------
# Training execution
# ---------------------------------------------------------------------------

def _run_training(job):
    """
    Execute a single YOLO training job in a subprocess.

    The function sets CUDA_VISIBLE_DEVICES so that the selected physical GPU
    appears as device 0 inside the subprocess. After training completes, all
    files except best.pt and results.csv are removed from the output
    directory to conserve disk space.

    Parameters
    ----------
    job : dict
        Job specification produced by _build_job_list.

    Returns
    -------
    dict
        Result record with keys: condition, seed, gpu, success, message.
    """
    condition = job["condition"]
    seed = job["seed"]
    gpu = job["gpu"]
    run_dir: Path = job["run_dir"]
    data_yaml: Path = job["data_yaml"]

    result_base = dict(condition=condition, seed=seed, gpu=gpu)

    # YOLO CLI places output under project/name; we set both so the final
    # artifacts land at run_dir/run/
    project_dir = run_dir
    run_name = "run"
    yolo_out = project_dir / run_name

    run_dir.mkdir(parents=True, exist_ok=True)

    log_file = run_dir / "train.log"

    # Find yolo CLI: check PATH first, then common user-local location.
    import shutil
    yolo_bin = shutil.which("yolo")
    if yolo_bin is None:
        candidate = Path.home() / ".local" / "bin" / "yolo"
        if candidate.exists():
            yolo_bin = str(candidate)
        else:
            yolo_bin = "yolo"  # fallback, will error clearly

    cmd = [
        yolo_bin, "detect", "train",
        f"data={data_yaml}",
        f"model={job['model']}",
        f"epochs={job['epochs']}",
        f"batch={job['batch']}",
        f"imgsz={job['imgsz']}",
        "device=0",          # CUDA_VISIBLE_DEVICES remaps physical GPU to 0
        f"seed={seed}",
        f"project={project_dir}",
        f"name={run_name}",
        f"workers={job['workers']}",
        "exist_ok=True",     # allow re-runs without manual cleanup
    ]

    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = str(gpu)

    log.info(
        "Starting | condition=%s seed=%d gpu=%d | cmd=%s",
        condition, seed, gpu, " ".join(cmd),
    )

    try:
        with open(log_file, "w") as lf:
            proc = subprocess.run(
                cmd,
                stdout=lf,
                stderr=subprocess.STDOUT,
                env=env,
                check=True,
            )
        _prune_output(yolo_out, condition, seed)
        log.info("Done    | condition=%s seed=%d gpu=%d", condition, seed, gpu)
        return {**result_base, "success": True, "message": "OK"}

    except subprocess.CalledProcessError as exc:
        msg = f"Training failed (return code {exc.returncode}). See {log_file}"
        log.error("FAILED  | condition=%s seed=%d gpu=%d | %s", condition, seed, gpu, msg)
        return {**result_base, "success": False, "message": msg}

    except Exception as exc:  # noqa: BLE001
        msg = f"Unexpected error: {exc}"
        log.error("ERROR   | condition=%s seed=%d gpu=%d | %s", condition, seed, gpu, msg)
        return {**result_base, "success": False, "message": msg}


def _prune_output(yolo_out: Path, condition: str, seed: int):
    """
    Remove all training artifacts except best.pt and results.csv.

    YOLO writes a large number of intermediate files (last.pt, confusion
    matrices, label plots, etc.).  This function retains only the two files
    needed for downstream evaluation and deletes everything else.

    Parameters
    ----------
    yolo_out : Path
        The directory YOLO wrote outputs into (project/name).
    condition : str
        Condition label, used only for log messages.
    seed : int
        Seed value, used only for log messages.
    """
    if not yolo_out.exists():
        log.warning(
            "Prune skipped: output dir not found | condition=%s seed=%d path=%s",
            condition, seed, yolo_out,
        )
        return

    keep = {"best.pt", "results.csv"}

    removed = 0
    for item in yolo_out.rglob("*"):
        if item.is_file() and item.name not in keep:
            try:
                item.unlink()
                removed += 1
            except OSError as exc:
                log.warning("Could not remove %s: %s", item, exc)

    # Remove empty subdirectories left behind after file deletion
    for dirpath in sorted(yolo_out.rglob("*"), reverse=True):
        if dirpath.is_dir():
            try:
                dirpath.rmdir()  # only succeeds if directory is empty
            except OSError:
                pass  # directory is not empty, leave it

    log.info(
        "Pruned %d file(s) | condition=%s seed=%d | kept=%s",
        removed, condition, seed, keep,
    )


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def _parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="train_yolo.py",
        description=(
            "YOLOv8-nano training launcher for the EchoTrails ablation study. "
            "Supports parallel multi-GPU execution via subprocess and "
            "concurrent.futures.ProcessPoolExecutor."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # --- Input specification (mutually exclusive) ---
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--data-yaml",
        type=Path,
        metavar="PATH",
        help="Path to a single YOLO data.yaml file.",
    )
    source_group.add_argument(
        "--batch-dir",
        type=Path,
        metavar="DIR",
        help=(
            "Directory containing multiple condition subdirectories, each "
            "with a data.yaml file (searched one level deep)."
        ),
    )

    # --- Output ---
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        metavar="DIR",
        help="Root directory for all training run outputs.",
    )

    # --- GPU assignment ---
    gpu_group = parser.add_mutually_exclusive_group()
    gpu_group.add_argument(
        "--gpu",
        type=int,
        default=None,
        metavar="INT",
        help="Single GPU index to use for all jobs.",
    )
    gpu_group.add_argument(
        "--gpus",
        type=str,
        default=None,
        metavar="0,1,...",
        help=(
            "Comma-separated list of GPU indices. Jobs are distributed "
            "round-robin; one job runs per GPU at a time."
        ),
    )

    # --- Seed control ---
    parser.add_argument(
        "--seeds",
        type=str,
        default="1000,2000,3000",
        metavar="INT,...",
        help="Comma-separated list of random seeds.",
    )

    # --- Training hyperparameters ---
    parser.add_argument(
        "--epochs",
        type=int,
        default=100,
        help="Number of training epochs.",
    )
    parser.add_argument(
        "--batch",
        type=int,
        default=16,
        help="Batch size.",
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Input image size (square).",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="yolov8n.pt",
        help="YOLOv8 model checkpoint (pretrained on COCO).",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of DataLoader worker processes per job.",
    )

    # --- Execution flags ---
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Print all planned jobs and GPU assignments without running "
            "any training."
        ),
    )

    return parser.parse_args(argv)


# ---------------------------------------------------------------------------
# Input resolution helpers
# ---------------------------------------------------------------------------

def _resolve_data_yamls(args):
    """
    Return a list of resolved data.yaml Paths from parsed arguments.

    Parameters
    ----------
    args : argparse.Namespace

    Returns
    -------
    list of Path

    Raises
    ------
    FileNotFoundError
        If a specified path does not exist.
    ValueError
        If --batch-dir contains no data.yaml files.
    """
    if args.data_yaml is not None:
        p = args.data_yaml.resolve()
        if not p.is_file():
            raise FileNotFoundError(f"data.yaml not found: {p}")
        return [p]

    batch_dir = args.batch_dir.resolve()
    if not batch_dir.is_dir():
        raise FileNotFoundError(f"--batch-dir does not exist: {batch_dir}")

    yamls = sorted(batch_dir.glob("*/data.yaml"))
    if not yamls:
        raise ValueError(
            f"No data.yaml files found one level deep in: {batch_dir}"
        )
    return yamls


def _resolve_gpu_list(args):
    """
    Return a list of GPU indices from parsed arguments.

    Falls back to [0] if neither --gpu nor --gpus is specified.

    Parameters
    ----------
    args : argparse.Namespace

    Returns
    -------
    list of int
    """
    if args.gpus is not None:
        return [int(g.strip()) for g in args.gpus.split(",") if g.strip()]
    if args.gpu is not None:
        return [args.gpu]
    return [0]


def _resolve_seeds(args):
    """
    Return a list of integer seeds from the --seeds argument string.

    Parameters
    ----------
    args : argparse.Namespace

    Returns
    -------
    list of int
    """
    return [int(s.strip()) for s in args.seeds.split(",") if s.strip()]


# ---------------------------------------------------------------------------
# Dry-run display
# ---------------------------------------------------------------------------

def _print_dry_run(jobs):
    """Print a formatted summary of planned jobs without executing them."""
    col_w = max(len(j["condition"]) for j in jobs)
    header = f"{'#':<4}  {'Condition':<{col_w}}  {'Seed':>6}  {'GPU':>4}"
    print(header)
    print("-" * len(header))
    for idx, job in enumerate(jobs):
        print(
            f"{idx:<4}  {job['condition']:<{col_w}}  "
            f"{job['seed']:>6}  GPU{job['gpu']:>2}"
        )
    print(f"\nTotal jobs planned: {len(jobs)}")


# ---------------------------------------------------------------------------
# Parallel execution
# ---------------------------------------------------------------------------

def _run_jobs_parallel(jobs, gpu_list):
    """
    Submit all jobs to a ProcessPoolExecutor and collect results.

    The maximum number of workers equals the number of unique GPUs requested,
    so at most one job occupies each GPU at any time.

    Parameters
    ----------
    jobs : list of dict
    gpu_list : list of int

    Returns
    -------
    list of dict
        Result records in completion order.
    """
    max_workers = len(gpu_list)
    results = []

    log.info(
        "Submitting %d job(s) across %d GPU(s) with max_workers=%d",
        len(jobs), len(gpu_list), max_workers,
    )

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_job = {
            executor.submit(_run_training, job): job for job in jobs
        }
        for future in as_completed(future_to_job):
            res = future.result()
            results.append(res)

    return results


# ---------------------------------------------------------------------------
# Result reporting
# ---------------------------------------------------------------------------

def _report_results(results):
    """
    Print a summary table of training results and return an exit code.

    Parameters
    ----------
    results : list of dict

    Returns
    -------
    int
        0 if all jobs succeeded, 1 if any failed.
    """
    successes = [r for r in results if r["success"]]
    failures = [r for r in results if not r["success"]]

    print("\n" + "=" * 60)
    print(f"Training complete.  {len(successes)}/{len(results)} jobs succeeded.")

    if failures:
        print(f"\nFailed jobs ({len(failures)}):")
        for r in failures:
            print(f"  condition={r['condition']}  seed={r['seed']}  gpu={r['gpu']}")
            print(f"    {r['message']}")

    print("=" * 60)
    return 0 if not failures else 1


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv=None):
    args = _parse_args(argv)

    # Resolve inputs
    try:
        data_yamls = _resolve_data_yamls(args)
    except (FileNotFoundError, ValueError) as exc:
        log.error("%s", exc)
        sys.exit(1)

    gpu_list = _resolve_gpu_list(args)
    seeds = _resolve_seeds(args)

    log.info("Conditions found : %d", len(data_yamls))
    log.info("Seeds            : %s", seeds)
    log.info("GPU list         : %s", gpu_list)
    log.info("Epochs           : %d", args.epochs)
    log.info("Batch size       : %d", args.batch)
    log.info("Image size       : %d", args.imgsz)
    log.info("Model            : %s", args.model)
    log.info("Workers          : %d", args.workers)
    log.info("Output dir       : %s", args.output_dir)

    jobs = _build_job_list(
        data_yamls=data_yamls,
        output_dir=args.output_dir.resolve(),
        seeds=seeds,
        gpu_list=gpu_list,
        model=args.model,
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
        workers=args.workers,
    )

    if args.dry_run:
        print("\nDRY RUN - no training will be executed.\n")
        _print_dry_run(jobs)
        sys.exit(0)

    results = _run_jobs_parallel(jobs, gpu_list)
    exit_code = _report_results(results)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
