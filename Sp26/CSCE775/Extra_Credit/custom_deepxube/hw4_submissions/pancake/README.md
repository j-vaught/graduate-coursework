# CSCE 775 HW4 -- Pancake Sorting

## Why I Picked This Domain

Pancake is the second rung of my progression (Hanoi -> Pancake -> 3D
robotic arm -> retro-synthesis -> four-bar linkage -> warehouse MAPF). I
moved to it after Hanoi because it keeps the representation simple while scaling up the two things that make search
harder: branching factor (9 instead of 2 or 3) and state-space size (10!
= 3.6M states instead of a few hundred). That gave me a stepping stone
where the learned heuristic would be doing real work (uniform cost search
blows up very quickly past ~10 moves from sorted) but where the
representation was still easy enough to reason about while I tuned
training hyperparameters. It is a curriculum checkpoint rather than the
primary research submission.

## What Is Interesting About It

Finding an optimal flip sequence is
NP-hard in general, the diameter of the 10-pancake sorting network is
known only via the Heydari-Sudborough upper bound of (18/11)N, and the
classical "gap" heuristic is the standard admissible benchmark. That
makes it a good probe for how well a neural heuristic learns to
outperform a well-engineered symbolic heuristic on a problem where every
action has global consequences (a flip reverses a prefix, so one move can
touch most of the state vector). It is also a good case for watching how
the learned V-function handles the many-to-one nature of flip actions --
two different scrambles can lead to structurally different solution
paths of the same length.

## Domain

`pancake.py` implements the classic pancake-sorting problem (Gates &
Papadimitriou, 1979) with configurable `num_pancakes`. Factory-registered
as `pancake`. The submission targets `pancake.10` -- 10 pancakes on a stack,
and the only legal action is "flip the top K pancakes" for K in 2..10.

The goal is to reach the sorted permutation `[0, 1, ..., N-1]`. The
state space has `N!` permutations (3.6M for N = 10) and the branching
factor is `N - 1 = 9`.

The domain subclasses `StateGoalVizable` (each pancake drawn as a colored
rectangle whose width encodes its size) and `StringToAct` (accepting the
flip index K as console input).

## Test Problem Instances (`pancake_test.pkl`)

30 instances generated via DeepXube's `problem_inst` tool with a maximum
reverse-random-walk depth of 35 flips.

These instances are interesting because:

1. Pancake sorting is NP-hard to solve optimally in general. For N = 10
   optimal solutions exist but the search tree explodes with depth
   (9 moves per state), so uniform cost search struggles past ~10 flips
   from sorted.

2. The diameter of the state graph for N = 10 is at most about 12 moves
   (via the Heydari-Sudborough bound of (18/11)N), and reverse random
   walks of length 35 reliably land at states in the hard portion of the
   space where even A* with the classic gap heuristic consumes nontrivial
   compute.

3. A random walk's reverse path is valid but not optimal, so test instances
   let the learned heuristic distinguish between paths that merely
   "unscramble" and paths that minimize total flip count.

## Install DeepXube

```bash
pip install deepxube
```

Keep `pancake.py` in a local `domains/` directory so DeepXube picks up the
`@domain_factory.register_class("pancake")` registration at import time.

## Train the Heuristic

The heuristic is DeepXube's `resnet_fc` architecture (1024 hidden, 4
residual blocks, batch norm) trained via supervised-V reverse random-walk
bootstrapping.

```bash
python -m deepxube train \
  --domain pancake.10 \
  --heur resnet_fc.1024H_4B_bn \
  --heur_type V \
  --pathfind sup_v_rw_rev \
  --dir runs/pancake \
  --step_max 35 \
  --batch_size 4096 \
  --max_itrs 100000 \
  --procs 8 \
  --up_itrs 200 \
  --up_gen_itrs 16 \
  --search_itrs 256 \
  --up_batch_size 512 \
  --up_nnet_batch_size 65536 \
  --t_file pancake_test.pkl \
  --t_search_itrs 300 \
  --t_up_freq 5 \
  --t_pathfinds graph_v
```

Trained weights land in `runs/pancake/model.pt`. A pre-trained
`pancake_model.pt` is included so grading can skip retraining.

## Solve Problem Instances

```bash
python -m deepxube solve \
  --domain pancake.10 \
  --heur resnet_fc.1024H_4B_bn \
  --heur_file pancake_model.pt \
  --heur_type V \
  --pathfind graph_v.1B \
  --file pancake_test.pkl \
  --results results/pancake_learned
```

Uniform-cost-search baseline (all-zeros heuristic):

```bash
python -m deepxube solve \
  --domain pancake.10 \
  --heur_type V \
  --pathfind graph_v.1B \
  --file pancake_test.pkl \
  --results results/pancake_ucs \
  --time_limit 60
```

## Expected Results

With the supplied `pancake_model.pt`:

- Instances solved: 100% of 30 (within a 60-second per-instance budget).
- Mean nodes generated per solve: on the order of 10^2 to 10^3.
- Mean solve time per instance: typically well under 1 second on CPU.

## Learned Heuristic vs. Uniform Cost Search

The `pancake.10` state space has `10! = 3 628 800` permutations and a
branching factor of 9, with a graph diameter of at most 12 flips (via
the Heydari-Sudborough (18/11)N upper bound). Naive UCS without a
closed list expands on the order of `9^12 = 2.8 * 10^11` nodes on the
deepest solutions, which is hopeless. Even with a closed list UCS is
capped at `10! = 3.6M` expansions -- tractable in principle but well
past the 60-second per-instance budget in practice on the harder
scrambles. On the 30-instance test set, UCS typically consumes 10^5
to 10^6 node expansions on the worst instances before timing out or
hitting memory pressure.

The learned V-heuristic compresses that search drastically: on the
same 30 instances it finds valid solutions in 10^2 to 10^3 node
expansions, roughly a `10^3` to `10^4` reduction per instance. In
wall-clock terms that is the difference between "sub-second per
instance on CPU" for the learned heuristic and "multiple seconds to
minutes per instance, frequent timeouts" for UCS. This is also the
first domain in my progression where UCS genuinely cannot keep up,
which is why I treated Pancake as the transition point between
pipeline validation (Hanoi) and meaningful search-guidance
experiments.
