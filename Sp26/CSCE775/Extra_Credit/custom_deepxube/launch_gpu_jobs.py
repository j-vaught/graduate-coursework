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
    "linkage": TrainJob("linkage", "linkage.16_16_16", "resnet_fc.32H_1B_bn",
                        "/tmp/linkage_16_smoke.pkl", 4, 32, 40, 40, 4,
                        1, 32, 128, 100, 1),
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
                      200, 16, 200, 512, 65536, 300, 5),
    "pancake": TrainJob("pancake", "pancake.10", "resnet_fc.1024H_4B_bn",
                        "test_instances/pancake_10.pkl", 35, 4096, 100000,
                        200, 16, 300, 512, 65536, 300, 5),
    "linkage": TrainJob("linkage", "linkage.64_64_64", "resnet_fc.1024H_4B_bn",
                        "test_instances/linkage_64.pkl", 50, 4096, 150000,
                        200, 16, 500, 256, 65536, 500, 5),
    "mapf": TrainJob("mapf", "mapf.28_28_30_64", "resnet_fc.1024H_4B_bn",
                     "test_instances/mapf_28x28_30.pkl", 80, 2048, 150000,
                     200, 8, 50, 128, 32768, 50, 10),
    "arm": TrainJob("arm", "arm.6_12_8", "resnet_fc.1024H_4B_bn",
                    "test_instances/arm_6_12_8.pkl", 25, 4096, 150000,
                    200, 16, 300, 512, 65536, 300, 5),
    "retro": TrainJob("retro", "retro.7", "resnet_fc.1024H_4B_bn",
                      "test_instances/retro_7.pkl", 30, 4096, 150000,
                      200, 16, 300, 512, 65536, 300, 5),
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


def make_train_command(job: TrainJob, run_tag: str, gpu: str, procs: int) -> str:
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
    ("linkage.16_16_16", "/tmp/linkage_16_smoke.pkl", [1, 1, 2, 2, 3, 3]),
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
    unknown = sorted(set(selected) - set(job_table))
    if unknown:
        raise ValueError(f"Unknown job names for tier {args.tier}: {', '.join(unknown)}")

    run_tag = args.run_tag or datetime.now().strftime("%Y%m%d_%H%M%S")
    repo_dir = shell_repo_dir(args.repo_dir)
    commands = [
        "set -euo pipefail",
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

    for job_idx, name in enumerate(selected):
        gpu = gpus[job_idx % len(gpus)]
        commands.append(make_train_command(job_table[name], run_tag, gpu, args.procs))
        commands.append(f"echo launched {q(name)}")

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
    parser.add_argument("--jobs", default="linkage,mapf,arm,retro")
    parser.add_argument(
        "--sync-mode",
        choices=["git", "rsync"],
        default="git",
        help="Use git on the remote host or rsync this local custom workspace first.",
    )
    parser.add_argument("--gpu", default="0")
    parser.add_argument("--procs", type=int, default=2)
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
