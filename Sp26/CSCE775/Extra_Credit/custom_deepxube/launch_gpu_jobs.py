"""Launch custom DeepXube training jobs on GPU hosts."""

from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime


REPO_URL = "https://github.com/j-vaught/graduate-coursework.git"
CUSTOM_REL = "Sp26/CSCE775/Extra_Credit/custom_deepxube"


@dataclass(frozen=True)
class TrainJob:
    name: str
    domain: str
    heur: str
    test_file: str
    step_max: int
    batch_size: int
    max_itrs: int
    up_itrs: int
    up_gen_itrs: int
    search_itrs: int
    up_batch_size: int
    up_nnet_batch_size: int
    test_search_itrs: int
    test_up_freq: int


SMOKE_JOBS = {
    "hanoi": TrainJob("hanoi", "hanoi.6.3", "resnet_fc.64H_2B_bn",
                      "test_instances/hanoi_6_3.pkl", 20, 64, 40, 40, 4,
                      1, 64, 256, 100, 1),
    "pancake": TrainJob("pancake", "pancake.10", "resnet_fc.64H_2B_bn",
                        "test_instances/pancake_10.pkl", 20, 64, 40, 40, 4,
                        1, 64, 256, 100, 1),
    "mapf": TrainJob("mapf", "mapf.8_8_4_32", "resnet_fc.32H_1B_bn",
                     "/tmp/mapf_8x8_4_onestep.pkl", 2, 32, 40, 40, 4,
                     1, 32, 128, 100, 1),
    "arm": TrainJob("arm", "arm.6_12_8", "resnet_fc.32H_1B_bn",
                    "/tmp/arm_6_12_8_smoke.pkl", 4, 32, 40, 40, 4,
                    1, 32, 128, 100, 1),
    "retro": TrainJob("retro", "retro.7", "resnet_fc.64H_2B_bn",
                      "test_instances/retro_7.pkl", 10, 64, 40, 40, 4,
                      1, 64, 256, 100, 1),
}


FULL_JOBS = {
    "hanoi": TrainJob("hanoi", "hanoi.6.3", "resnet_fc.512H_3B_bn",
                      "test_instances/hanoi_6_3.pkl", 35, 4096, 100000,
                      200, 16, 256, 1024, 131072, 300, 10),
    "pancake": TrainJob("pancake", "pancake.10", "resnet_fc.1024H_4B_bn",
                        "test_instances/pancake_10.pkl", 35, 4096, 100000,
                        200, 16, 256, 1024, 131072, 300, 10),
    "mapf4": TrainJob("mapf4", "mapf.28_28_4_64", "resnet_fc.128H_2B_bn",
                      "test_instances/mapf_28x28_4.pkl", 40, 4096, 100000,
                      200, 16, 128, 1024, 131072, 5000, 50),
    "mapf16": TrainJob("mapf16", "mapf.28_28_16_128", "resnet_fc.512H_3B_bn",
                       "test_instances/mapf_28x28_16.pkl", 50, 2048, 150000,
                       200, 16, 128, 512, 65536, 500, 100),
    "mapf16_2d": TrainJob("mapf16_2d", "mapf.28_28_16_128", "resnet_2d.64C_4B_bn",
                          "test_instances/mapf_28x28_16.pkl", 50, 2048, 150000,
                          200, 16, 256, 512, 32768, 1000, 25),
    "mapf16_2d32_quick128": TrainJob("mapf16_2d32_quick128", "mapf.28_28_16_128",
                                     "resnet_2d.32C_2B_bn",
                                     "test_instances/mapf_28x28_16_quick.pkl",
                                     30, 1024, 5000, 200, 8, 128, 256, 8192,
                                     1000, 5),
    "mapf16_2d32_quick96": TrainJob("mapf16_2d32_quick96", "mapf.28_28_16_96",
                                    "resnet_2d.32C_2B_bn",
                                    "test_instances/mapf_28x28_16_quick.pkl",
                                    30, 1024, 5000, 200, 8, 128, 256, 8192,
                                    1000, 5),
    "mapf16_2d64_quick128": TrainJob("mapf16_2d64_quick128", "mapf.28_28_16_128",
                                     "resnet_2d.64C_2B_bn",
                                     "test_instances/mapf_28x28_16_quick.pkl",
                                     30, 512, 5000, 200, 8, 128, 256, 8192,
                                     1000, 5),
    "mapf16_2d16dist_quick128": TrainJob("mapf16_2d16dist_quick128", "mapf.28_28_16_128_dist",
                                         "resnet_2d.16C_1B_bn",
                                         "test_instances/mapf_28x28_16_quick.pkl",
                                         30, 1024, 1000, 200, 8, 128, 256, 8192,
                                         1000, 5),
    "mapf16_2d32dist_quick128": TrainJob("mapf16_2d32dist_quick128", "mapf.28_28_16_128_dist",
                                         "resnet_2d.32C_2B_bn",
                                         "test_instances/mapf_28x28_16_quick.pkl",
                                         30, 1024, 1000, 200, 8, 128, 256, 8192,
                                         1000, 5),
    "mapf30_2d16dist_quick256": TrainJob("mapf30_2d16dist_quick256", "mapf.28_28_30_256_dist",
                                         "resnet_2d.16C_1B_bn",
                                         "test_instances/mapf_28x28_30_quick.pkl",
                                         40, 1024, 1000, 200, 8, 128, 256, 8192,
                                         1000, 5),
    "mapf30_2d32dist_quick256": TrainJob("mapf30_2d32dist_quick256", "mapf.28_28_30_256_dist",
                                         "resnet_2d.32C_2B_bn",
                                         "test_instances/mapf_28x28_30_quick.pkl",
                                         40, 1024, 1000, 200, 8, 128, 256, 8192,
                                         1000, 5),
    "mapf30_2d32time_quick256": TrainJob("mapf30_2d32time_quick256", "mapf.28_28_30_256_dist",
                                         "resnet_2d.32C_2B_bn",
                                         "test_instances/mapf_28x28_30_quick.pkl",
                                         40, 1024, 3000, 200, 8, 128, 256, 8192,
                                         1000, 5),
    "mapf60_2d32dist_quick256": TrainJob("mapf60_2d32dist_quick256", "mapf.28_28_60_256_dist",
                                         "resnet_2d.32C_2B_bn",
                                         "test_instances/mapf_28x28_60_quick.pkl",
                                         40, 1024, 3000, 200, 8, 128, 256, 8192,
                                         1000, 5),
    "mapf60_2d32time_quick256": TrainJob("mapf60_2d32time_quick256", "mapf.28_28_60_256_dist",
                                         "resnet_2d.32C_2B_bn",
                                         "test_instances/mapf_28x28_60_quick.pkl",
                                         40, 1024, 3000, 200, 8, 128, 256, 8192,
                                         1000, 5),
    "mapf60_2d64dist_quick256": TrainJob("mapf60_2d64dist_quick256", "mapf.28_28_60_256_dist",
                                         "resnet_2d.64C_2B_bn",
                                         "test_instances/mapf_28x28_60_quick.pkl",
                                         40, 512, 3000, 200, 8, 128, 256, 4096,
                                         1000, 5),
    "mapf16_single": TrainJob("mapf16_single", "mapf.28_28_16_128_single",
                              "resnet_fc.512H_3B_bn",
                              "test_instances/mapf_28x28_16_single.pkl",
                              50, 2048, 150000, 200, 16, 256, 512, 65536,
                              2000, 100),
    "mapf30": TrainJob("mapf30", "mapf.28_28_30_256_dist", "resnet_2d.32C_2B_bn",
                       "test_instances/mapf_28x28_30.pkl", 80, 1024, 10000,
                       200, 8, 128, 256, 8192, 2000, 5),
    "arm": TrainJob("arm", "arm.6_12_8", "resnet_fc.1024H_4B_bn",
                    "test_instances/arm_6_12_8.pkl", 25, 4096, 150000,
                    200, 16, 256, 1024, 131072, 300, 10),
    "arm64": TrainJob("arm64", "arm.6_12_64", "resnet_fc.1024H_4B_bn",
                      "test_instances/arm_6_12_64.pkl", 25, 4096, 250000,
                      200, 16, 256, 1024, 131072, 1000, 50),
    "retro": TrainJob("retro", "retro.7", "resnet_fc.1024H_4B_bn",
                      "test_instances/retro_7.pkl", 30, 4096, 200000,
                      200, 16, 256, 1024, 131072, 5000, 25),
}


def q(value: str) -> str:
    return shlex.quote(value)


def shell_repo_dir(value: str) -> str:
    if value == "~":
        return '"${HOME}"'
    if value.startswith("~/"):
        return '"${HOME}/' + value[2:].replace('"', '\\"') + '"'
    return q(value)


def remote_custom_dir(repo_dir: str) -> str:
    return repo_dir.rstrip("/") + "/" + CUSTOM_REL


def make_train_command(job: TrainJob, run_tag: str, gpu: str, procs: int | str) -> str:
    run_dir = f"runs/{run_tag}/{job.name}"
    log_file = f"logs/{run_tag}_{job.name}.log"
    pid_file = f"runs/{run_tag}_{job.name}.pid"
    return " ".join([
        f"CUDA_VISIBLE_DEVICES={q(gpu)}",
        "nohup",
        ".venv/bin/python", "-u", "-m", "deepxube", "train",
        "--domain", q(job.domain),
        "--heur", q(job.heur),
        "--heur_type", "V",
        "--pathfind", "sup_v_rw_rev",
        "--dir", q(run_dir),
        "--step_max", str(job.step_max),
        "--batch_size", str(job.batch_size),
        "--max_itrs", str(job.max_itrs),
        "--procs", str(procs),
        "--up_itrs", str(job.up_itrs),
        "--up_gen_itrs", str(job.up_gen_itrs),
        "--search_itrs", str(job.search_itrs),
        "--up_batch_size", str(job.up_batch_size),
        "--up_nnet_batch_size", str(job.up_nnet_batch_size),
        "--t_file", q(job.test_file),
        "--t_search_itrs", str(job.test_search_itrs),
        "--t_up_freq", str(job.test_up_freq),
        "--t_pathfinds", "graph_v",
        ">", q(log_file), "2>&1", "&", "echo", "$!", ">", q(pid_file),
    ])


def smoke_instance_script() -> str:
    return r"""
.venv/bin/python - <<'PY'
import pickle
from pathlib import Path
import numpy as np
import deepxube  # noqa: F401
from deepxube.utils.command_line_utils import get_domain_from_arg

cases = [
    ("mapf.8_8_4_32", "/tmp/mapf_8x8_4_onestep.pkl", [1, 1, 1, 1]),
    ("arm.6_12_8", "/tmp/arm_6_12_8_smoke.pkl", [1, 1, 2, 2, 3, 3]),
]
np.random.seed(775)
for domain_str, file_name, steps in cases:
    domain, _ = get_domain_from_arg(domain_str)
    states, goals = domain.sample_problem_instances(steps)
    with Path(file_name).open("wb") as f:
        pickle.dump(
            {"domain": domain_str, "steps": steps, "states": states, "goals": goals},
            f,
            protocol=-1,
        )
    print(f"wrote {file_name}")
PY
""".strip()


def make_remote_script(args: argparse.Namespace) -> str:
    job_table = SMOKE_JOBS if args.tier == "smoke" else FULL_JOBS
    selected = [name.strip() for name in args.jobs.split(",") if name.strip()]
    if not selected:
        selected = ["mapf", "arm", "retro"] if args.tier == "smoke" else ["mapf4", "arm64", "retro"]
    unknown = sorted(set(selected) - set(job_table))
    if unknown:
        raise ValueError(f"Unknown job names for tier {args.tier}: {', '.join(unknown)}")

    run_tag = args.run_tag or datetime.now().strftime("%Y%m%d_%H%M%S")
    repo_dir = shell_repo_dir(args.repo_dir)
    commands = [
        "set -euo pipefail",
        "ulimit -n 65536 || true",
        f"REPO_DIR={repo_dir}",
    ]
    if args.sync_mode == "git":
        commands.append(
            'if [ -d "${REPO_DIR}/.git" ]; then '
            'git -C "${REPO_DIR}" pull --ff-only; '
            f"else git clone --filter=blob:none --depth=1 --sparse {q(REPO_URL)} "
            '"${REPO_DIR}" && '
            f"git -C " + '"${REPO_DIR}" sparse-checkout set ' + q(CUSTOM_REL) + "; fi"
        )

    commands.extend([
        'if [ -d "${REPO_DIR}/.git" ]; then '
        'git -C "${REPO_DIR}" rev-parse --short HEAD; fi',
        f'cd "${{REPO_DIR}}/{CUSTOM_REL}"',
        "export OMP_NUM_THREADS=1",
        "export OMP_THREAD_LIMIT=1",
        "export MKL_NUM_THREADS=1",
        "export OPENBLAS_NUM_THREADS=1",
        "export NUMEXPR_NUM_THREADS=1",
        "export VECLIB_MAXIMUM_THREADS=1",
        "export BLIS_NUM_THREADS=1",
        "python3 -m venv .venv",
        ".venv/bin/python -m pip install --upgrade pip wheel",
        f".venv/bin/python -m pip install {q(args.torch_spec)}",
        ".venv/bin/python -m pip install deepxube tensorboard",
        ".venv/bin/python - <<'PY'\nimport torch\n"
        "print('torch', torch.__version__)\n"
        "print('cuda_available', torch.cuda.is_available())\n"
        "print('cuda_devices', torch.cuda.device_count())\n"
        "raise SystemExit(0 if torch.cuda.is_available() else 2)\nPY",
        "mkdir -p logs runs",
        ".venv/bin/python smoke_test.py",
        f".venv/bin/python benchmark_domains.py --json-out {q('logs/' + run_tag + '_benchmark.json')}",
    ])

    if args.tier == "smoke":
        commands.append(smoke_instance_script())

    gpus = [gpu.strip() for gpu in args.gpu.split(",") if gpu.strip()]
    if not gpus:
        raise ValueError("At least one GPU id must be provided")

    commands.extend([
        f"JOB_COUNT={len(selected)}",
        "CPU_COUNT=$(getconf _NPROCESSORS_ONLN 2>/dev/null || true)",
        'if [ -z "${CPU_COUNT:-}" ] || [ "$CPU_COUNT" -lt 1 ]; then CPU_COUNT=$(lscpu | awk -F: \'/^CPU\\(s\\):/ {gsub(/ /, "", $2); print $2; exit}\'); fi',
        'if [ -z "${CPU_COUNT:-}" ] || [ "$CPU_COUNT" -lt 1 ]; then CPU_COUNT=1; fi',
        f"MIN_AUTO_PROCS={args.min_auto_procs}",
        f"MAX_AUTO_PROCS={args.max_auto_procs}",
        (
            f"if [ {args.procs} -gt 0 ]; then JOB_PROCS={args.procs}; "
            "else JOB_PROCS=$(( CPU_COUNT / (2 * JOB_COUNT) )); fi"
        ),
        'if [ "$JOB_PROCS" -lt "$MIN_AUTO_PROCS" ]; then JOB_PROCS="$MIN_AUTO_PROCS"; fi',
        'if [ "$JOB_PROCS" -gt "$MAX_AUTO_PROCS" ]; then JOB_PROCS="$MAX_AUTO_PROCS"; fi',
        'echo cpu_count="$CPU_COUNT" job_count="$JOB_COUNT" job_procs="$JOB_PROCS"',
    ])

    for job_idx, name in enumerate(selected):
        gpu = gpus[job_idx % len(gpus)]
        commands.append(make_train_command(job_table[name], run_tag, gpu, "${JOB_PROCS}"))
        commands.append(f"echo launched {q(name)} gpu={q(gpu)} procs=$JOB_PROCS")

    commands.append("jobs -l || true")
    return "\n".join(commands)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument(
        "--ssh-user",
        help="Remote login user. Omit when --host is an SSH config alias with User set.",
    )
    parser.add_argument("--repo-dir", default="~/graduate-coursework-deepxube-run")
    parser.add_argument("--tier", choices=["smoke", "full"], default="smoke")
    parser.add_argument("--jobs", default="")
    parser.add_argument(
        "--sync-mode",
        choices=["git", "rsync"],
        default="git",
        help="Use git on the remote host or rsync this local custom workspace first.",
    )
    parser.add_argument("--gpu", default="0")
    parser.add_argument(
        "--procs",
        type=int,
        default=0,
        help="Worker processes per job. Use 0 to auto-size from remote CPU count.",
    )
    parser.add_argument(
        "--min-auto-procs",
        type=int,
        default=4,
        help="Minimum worker processes per job when --procs=0.",
    )
    parser.add_argument(
        "--max-auto-procs",
        type=int,
        default=24,
        help="Maximum worker processes per job when --procs=0.",
    )
    parser.add_argument(
        "--torch-spec",
        default="torch==2.5.1",
        help="PyTorch requirement installed before DeepXube.",
    )
    parser.add_argument("--run-tag")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    remote_script = make_remote_script(args)
    destination = args.host if args.ssh_user is None else f"{args.ssh_user}@{args.host}"
    ssh_cmd = ["ssh", destination, "bash -lc " + q(remote_script)]

    if args.dry_run:
        print(" ".join(q(part) for part in ssh_cmd))
        return

    if args.sync_mode == "rsync":
        custom_dir = remote_custom_dir(args.repo_dir)
        mkdir_script = "\n".join([
            f"REPO_DIR={shell_repo_dir(args.repo_dir)}",
            f'mkdir -p "${{REPO_DIR}}/{CUSTOM_REL}"',
        ])
        subprocess.run(
            ["ssh", destination, "bash -lc " + q(mkdir_script)],
            check=True,
        )
        subprocess.run(
            [
                "rsync", "-az", "--delete",
                "--exclude", ".venv/",
                "--exclude", "__pycache__/",
                "--exclude", "logs/",
                "--exclude", "runs/",
                "./", f"{destination}:{custom_dir}/",
            ],
            check=True,
        )

    try:
        subprocess.run(ssh_cmd, check=True)
    except subprocess.CalledProcessError as exc:
        print(
            f"remote launch failed on {destination} with exit code {exc.returncode}",
            file=sys.stderr,
        )
        raise SystemExit(exc.returncode) from None


if __name__ == "__main__":
    main()
