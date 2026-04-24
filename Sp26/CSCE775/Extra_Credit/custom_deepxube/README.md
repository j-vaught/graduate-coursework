# Custom DeepXube Domains

This directory is the clean workspace for CSCE 775 Homework 4 extra credit.
It uses the `deepxube` package installed from PyPI and keeps custom domains in
the local `domains/` extension directory. Do not edit files inside the package
checkout.

## Setup

From this directory:

```bash
../deepxube/.venv_deepxube/bin/python -m deepxube domain_info --names hanoi,pancake,linkage,mapf,arm,retro
```

DeepXube imports local modules from `./domains/`, so the six custom domains are
registered without modifying the installed package.

## Domains

- `hanoi.4.3` or `hanoi.<num_disks>.<num_pegs>`
- `pancake.8` or `pancake.<num_pancakes>`
- `linkage.64_64_64`
- `mapf.28_28_30_64`, where the last value caps sampled joint actions.
- `arm.6_12_8`
- `retro.5`

For the strongest extra-credit submission, prefer `linkage`, `mapf`, `arm`, or
`retro` because they are not standard puzzle baselines.

## Generate Test Problems

Example:

```bash
../deepxube/.venv_deepxube/bin/python -m deepxube problem_inst \
  --domain linkage.64_64_64 \
  --step_max 50 \
  --num 100 \
  --file test_instances/linkage_test.pkl \
  --redo
```

For MAPF:

```bash
../deepxube/.venv_deepxube/bin/python -m deepxube problem_inst \
  --domain mapf.28_28_30_64 \
  --step_max 80 \
  --num 100 \
  --file test_instances/mapf_28x28_30_test.pkl \
  --redo
```

## Train

Linkage smoke/full command pattern:

```bash
../deepxube/.venv_deepxube/bin/python -m deepxube train \
  --domain linkage.64_64_64 \
  --heur resnet_fc.2000H_4B_bn \
  --heur_type V \
  --pathfind sup_v_rw_rev \
  --dir training/linkage \
  --step_max 50 \
  --batch_size 1000 \
  --max_itrs 100000 \
  --procs 2 \
  --up_itrs 100 \
  --search_itrs 500 \
  --t_file test_instances/linkage_test.pkl \
  --t_search_itrs 500 \
  --t_up_freq 5 \
  --t_pathfinds graph_v
```

MAPF 28x28 with 30 robots:

```bash
../deepxube/.venv_deepxube/bin/python -m deepxube train \
  --domain mapf.28_28_30_64 \
  --heur resnet_fc.1000H_4B_bn \
  --heur_type V \
  --pathfind sup_v_rw_rev \
  --dir training/mapf_28x28_30 \
  --step_max 80 \
  --batch_size 1000 \
  --max_itrs 100000 \
  --procs 2 \
  --up_itrs 100 \
  --search_itrs 500 \
  --t_file test_instances/mapf_28x28_30_test.pkl \
  --t_search_itrs 50 \
  --t_up_freq 10 \
  --t_pathfinds graph_v
```

For quick CPU checks, use `resnet_fc.32H_1B_bn`, `--batch_size 32`,
`--up_nnet_batch_size 128`, and `--procs 1`. For GPU runs, keep the `_bn`
heuristic suffix, raise the network and nnet batch sizes first, and keep the
MAPF domain action cap explicit in the domain string.

## Solve

```bash
../deepxube/.venv_deepxube/bin/python -m deepxube solve \
  --domain linkage.64_64_64 \
  --heur resnet_fc.2000H_4B_bn \
  --heur_type V \
  --heur_file training/linkage/heur.pt \
  --pathfind graph_v \
  --file test_instances/linkage_test.pkl \
  --results results/linkage \
  --nnet_batch_size 4096 \
  --time_limit 60 \
  --redo
```

## Current Smoke Results

The current workspace was verified on April 24, 2026 with the installed PyPI
package. All six domains registered, sampled problem instances, produced
actions, and stepped.

Local CPU train/solve smoke checks passed with batch normalization enabled.

- `hanoi.6.3` with `resnet_fc.64H_2B_bn` trained for 40 iterations and solved
  30/30 test instances with `graph_v`.
- `mapf.8_8_4_32` with `resnet_fc.32H_1B_bn` trained for 40 iterations and
  solved 4/4 one-step MAPF instances with `graph_v`.
- `linkage.16_16_16` with `resnet_fc.32H_1B_bn` trained for 40 iterations and
  solved 6/6 linkage instances with `graph_v`.
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
linkage.64_64_64          1000    20.7     0.036     11.9     0.000
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
  --jobs mapf,linkage,arm,retro \
  --gpu 0,1,2,3
```

Full jobs:

```bash
../deepxube/.venv_deepxube/bin/python launch_gpu_jobs.py \
  --host comech-2080 \
  --sync-mode rsync \
  --tier full \
  --jobs linkage,arm,retro \
  --gpu 0,1,2 \
  --procs 2
```

Use `--dry-run` to print the remote command without launching jobs. Logs go to
`logs/`, checkpoints go to `runs/`, and pid files are written under `runs/`.
Use SSH config aliases for the hosts. If a host has unreliable GitHub access,
add `--sync-mode rsync` to copy only this custom workspace from the local
machine before running.
