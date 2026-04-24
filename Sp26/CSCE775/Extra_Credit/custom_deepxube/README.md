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
  --heur resnet_fc.2000H_4B \
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
  --heur resnet_fc.1000H_4B \
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

## Solve

```bash
../deepxube/.venv_deepxube/bin/python -m deepxube solve \
  --domain linkage.64_64_64 \
  --heur resnet_fc.2000H_4B \
  --heur_type V \
  --pathfind graph_v \
  --dir training/linkage \
  --file test_instances/linkage_test.pkl \
  --search_itrs 500 \
  --results_file results/linkage_results.pkl
```

## Current Smoke Results

The current workspace was verified with the installed PyPI package. All six
domains registered, sampled problem instances, produced actions, and stepped.
For `mapf.28_28_30_64`, two sample states produced 64 actions each in about
0.05 seconds, and 200 ten-step reverse walks completed in about 0.02 seconds on
the local machine.
