# Custom DeepXube Domains

This directory is the clean workspace for CSCE 775 Homework 4 extra credit.
It uses the `deepxube` package installed from PyPI and keeps custom domains in
the local `domains/` extension directory. Do not edit files inside the package
checkout.

## Setup

From this directory:

```bash
../deepxube/.venv_deepxube/bin/python -m deepxube domain_info --names hanoi,pancake,mapf,arm,retro
```

DeepXube imports local modules from `./domains/`, so the five custom domains are
registered without modifying the installed package.

## Domains

- `hanoi.4.3` or `hanoi.<num_disks>.<num_pegs>`
- `pancake.8` or `pancake.<num_pancakes>`
- `mapf.28_28_4_64` or `mapf.28_28_30_64`, where the last value caps sampled joint actions.
- `arm.6_12_64`
- `retro.7`

For the strongest extra-credit submission, prefer `mapf`, `arm`, or `retro`
because they are not standard puzzle baselines.

## Generate Test Problems

Example:

```bash
../deepxube/.venv_deepxube/bin/python -m deepxube problem_inst \
  --domain arm.6_12_64 \
  --step_max 25 \
  --num 100 \
  --file test_instances/arm_6_12_64.pkl \
  --redo
```

For MAPF with 4 robots:

```bash
../deepxube/.venv_deepxube/bin/python -m deepxube problem_inst \
  --domain mapf.28_28_4_64 \
  --step_max 40 \
  --num 100 \
  --file test_instances/mapf_28x28_4.pkl \
  --redo
```

## Demo GIFs

The demo GIF scripts all use the domain `visualize_state_goal` methods, so
visual style changes should be made in `domains/*.py`.

Generate all demos:

```bash
../deepxube/.venv_deepxube/bin/python gif_demos.py all
```

Generate one domain demo:

```bash
../deepxube/.venv_deepxube/bin/python hanoi_gif_demo.py
../deepxube/.venv_deepxube/bin/python pancake_gif_demo.py
../deepxube/.venv_deepxube/bin/python mapf_gif_demo.py
../deepxube/.venv_deepxube/bin/python arm_gif_demo.py
../deepxube/.venv_deepxube/bin/python retro_gif_demo.py
```

The default output directory is `demo_gifs/`. Use `--steps`, `--fps`, `--dpi`,
or `--out-dir` to override the default rendering settings.

## Train

Arm 64-bin full command pattern:

```bash
../deepxube/.venv_deepxube/bin/python -m deepxube train \
  --domain arm.6_12_64 \
  --heur resnet_fc.1024H_4B_bn \
  --heur_type V \
  --pathfind sup_v_rw_rev \
  --dir training/arm_64bins \
  --step_max 25 \
  --batch_size 4096 \
  --max_itrs 150000 \
  --procs 2 \
  --up_itrs 200 \
  --up_gen_itrs 16 \
  --search_itrs 256 \
  --up_batch_size 512 \
  --up_nnet_batch_size 65536 \
  --t_file test_instances/arm_6_12_64.pkl \
  --t_search_itrs 300 \
  --t_up_freq 5 \
  --t_pathfinds graph_v
```

MAPF 28x28 with 4 robots:

```bash
../deepxube/.venv_deepxube/bin/python -m deepxube train \
  --domain mapf.28_28_4_64 \
  --heur resnet_fc.128H_2B_bn \
  --heur_type V \
  --pathfind sup_v_rw_rev \
  --dir training/mapf_28x28_4 \
  --step_max 40 \
  --batch_size 4096 \
  --max_itrs 100000 \
  --procs 2 \
  --up_itrs 200 \
  --up_gen_itrs 16 \
  --search_itrs 128 \
  --up_batch_size 512 \
  --up_nnet_batch_size 65536 \
  --t_file test_instances/mapf_28x28_4.pkl \
  --t_search_itrs 2000 \
  --t_up_freq 5 \
  --t_pathfinds graph_v
```

For quick CPU checks, use `resnet_fc.32H_1B_bn`, `--batch_size 32`,
`--up_nnet_batch_size 128`, and `--procs 1`. For GPU runs, keep the `_bn`
heuristic suffix, raise the network and nnet batch sizes first, and keep the
MAPF domain action cap explicit in the domain string.

## Solve

```bash
../deepxube/.venv_deepxube/bin/python -m deepxube solve \
  --domain retro.7 \
  --heur resnet_fc.1024H_4B_bn \
  --heur_type V \
  --heur_file runs/models/retro/model.pt \
  --pathfind graph_v \
  --file test_instances/retro_7.pkl \
  --results results/retro \
  --nnet_batch_size 4096 \
  --time_limit 60 \
  --redo
```

## Current Smoke Results

The current workspace was verified on April 24, 2026 with the installed PyPI
package. All five domains registered, sampled problem instances, produced
actions, and stepped.

Local CPU train/solve smoke checks passed with batch normalization enabled.

- `hanoi.6.3` with `resnet_fc.64H_2B_bn` trained for 40 iterations and solved
  30/30 test instances with `graph_v`.
- `mapf.8_8_4_32` with `resnet_fc.32H_1B_bn` trained for 40 iterations and
  solved 4/4 one-step MAPF instances with `graph_v`.
- `mapf.28_28_30_32` completed a 5-iteration training pass against the
  28x28/30-robot test file in about 0.8 seconds of update time. That run is a
  scaling and checkpoint smoke check, not a quality benchmark.

## Benchmark

Run the data-generation benchmark from this directory:

```bash
../deepxube/.venv_deepxube/bin/python benchmark_domains.py
```

Current local CPU timings after the arm and MAPF optimizations:

```text
domain                  states   steps    walk_s     acts    acts_s
hanoi.6.3                 1000    20.1     0.053      3.0     0.000
pancake.10                1000    20.4     0.025      9.0     0.000
mapf.28_28_30_64           200    10.4     0.016     64.0     0.359
arm.6_12_8                 500    10.5     0.287     11.7     0.038
retro.7                   1000    15.6     0.160      7.4     0.001
```

## GPU Launch

The launcher prepares a remote host, verifies CUDA, runs the smoke suite and
benchmark, and starts selected training jobs with `nohup`.

Smoke jobs:

```bash
../deepxube/.venv_deepxube/bin/python launch_gpu_jobs.py \
  --host comech-2422 \
  --tier smoke \
  --jobs mapf,arm,retro \
  --gpu 0,1,2,3
```

Full jobs:

```bash
../deepxube/.venv_deepxube/bin/python launch_gpu_jobs.py \
  --host comech-2080 \
  --sync-mode rsync \
  --tier full \
  --jobs mapf4,arm64,retro \
  --gpu 0,1,2 \
  --procs 2
```

Use `--dry-run` to print the remote command without launching jobs. Logs go to
`logs/`, checkpoints go to `runs/`, and pid files are written under `runs/`.
Use SSH config aliases for the hosts. If a host has unreliable GitHub access,
add `--sync-mode rsync` to copy only this custom workspace from the local
machine before running.
