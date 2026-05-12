# CSCE 775 HW4 -- Towers of Hanoi (Generalized)

## Why I Picked This Domain

Hanoi is the first step in a progression I worked through for this
extra-credit submission: Hanoi -> Pancake -> 3D robotic arm -> retro-
synthesis -> four-bar linkage -> warehouse MAPF. I started here on purpose
because the dynamics are minimal (move the top disk from one peg to
another if legal), the state space is small enough that I could sanity-
check the DeepXube training loop against the closed-form 2^N - 1 optimal
solution length, and the visualization is trivial to render cleanly. That
made it the right domain to use as a scaffold: it let me verify that the
reverse-random-walk supervised-V pipeline, the `graph_v` pathfinder, the
heuristic-network save/load cycle, and the test-instance tooling were all
wired up correctly before I moved on to harder domains where a bug would
be much harder to localize. It is intentionally *not* the research
submission -- it is the baseline I compared the harder domains against.

## What Is Interesting About It

Despite being a classical benchmark, Hanoi still has a couple of properties
that make it useful for experimentation. The optimal solution length is
exponential in the number of disks, so even at N = 6 the worst-case solve
requires 63 moves, which is well past the horizon where uniform cost
search becomes impractical. The state graph is regular enough that the
learned heuristic should converge quickly, giving me a clean "should
definitely work" baseline that I could use to debug any training run that
looked misbehaved on the harder domains. The 3-peg variant in particular
has tight known bounds on the optimal-solve length (Frame-Stewart for N
pegs, classical recurrence for 3 pegs) so I can check that my learned
heuristic produces solution lengths close to optimal rather than just
feasible paths.

## Domain

`hanoi.py` implements a generalized Towers of Hanoi domain with configurable
`num_disks` and `num_pegs`. Factory-registered as `hanoi`. The submission
targets `hanoi.6.3` -- 6 disks across 3 pegs, giving 2^6 * 3 / 3 = 128 legal
states and an optimal solve length of up to 63 moves from the worst start.

The domain subclasses `StateGoalVizable` (rendering each disk as a colored
rectangle on its peg) and `StringToAct` (so a solver can be driven from
console input such as "0 2" for move top disk peg 0 -> peg 2).

## Test Problem Instances (`hanoi_test.pkl`)

30 instances generated via DeepXube's `problem_inst` tool with a maximum
reverse random-walk depth of 35 steps. The file stores a dict with keys
`domain`, `steps`, `states`, `goals`.

These instances are interesting because:

1. The 6-disk / 3-peg variant has an optimal solve length of 2^6 - 1 = 63
   from the classic all-on-peg-0 start, and the worst random instances still
   require long solutions that uniform cost search cannot find within a
   reasonable time budget (node count blows up as branching^depth).

2. Scramble depths up to 35 moves push instances well past the horizon
   where simple BFS / uniform cost search can enumerate, so the learned
   heuristic has a meaningful advantage.

3. Instances include cases where all disks stay on a single peg (short
   solve) and cases where disks are scattered across pegs (long solve),
   covering the range the heuristic must generalize to.

## Install DeepXube

```bash
pip install deepxube
```

The DeepXube package must also be able to import `hanoi.py` so its
`@domain_factory.register_class("hanoi")` and parser registrations run at
startup. The cleanest way is to keep `hanoi.py` in a local `domains/`
directory and launch DeepXube from the parent directory -- DeepXube scans
for local `domains/*.py` and loads them automatically.

## Train the Heuristic

The heuristic is DeepXube's `resnet_fc` architecture (residual fully
connected MLP, 512 hidden, 3 residual blocks, batch norm) trained via
supervised-V reverse random-walk bootstrapping (`sup_v_rw_rev`).

```bash
python -m deepxube train \
  --domain hanoi.6.3 \
  --heur resnet_fc.512H_3B_bn \
  --heur_type V \
  --pathfind sup_v_rw_rev \
  --dir runs/hanoi \
  --step_max 35 \
  --batch_size 4096 \
  --max_itrs 100000 \
  --procs 8 \
  --up_itrs 200 \
  --up_gen_itrs 16 \
  --search_itrs 256 \
  --up_batch_size 512 \
  --up_nnet_batch_size 65536 \
  --t_file hanoi_test.pkl \
  --t_search_itrs 300 \
  --t_up_freq 5 \
  --t_pathfinds graph_v
```

The trained weights end up in `runs/hanoi/model.pt`. A pre-trained
`hanoi_model.pt` is included so grading can skip retraining.

## Solve Problem Instances

```bash
python -m deepxube solve \
  --domain hanoi.6.3 \
  --heur resnet_fc.512H_3B_bn \
  --heur_file hanoi_model.pt \
  --heur_type V \
  --pathfind graph_v.1B \
  --file hanoi_test.pkl \
  --results results/hanoi_learned
```

Each instance is solved by greedy best-first search guided by the learned
V-heuristic. Per-instance stats and aggregate means print to stdout and
`results/hanoi_learned/output.txt`.

For a uniform-cost-search baseline, omit `--heur` / `--heur_file` and set
`--heur_type V` (DeepXube will substitute an all-zeros heuristic, making
A* degenerate to UCS):

```bash
python -m deepxube solve \
  --domain hanoi.6.3 \
  --heur_type V \
  --pathfind graph_v.1B \
  --file hanoi_test.pkl \
  --results results/hanoi_ucs
  --time_limit 60
```

## Expected Results

With the supplied `hanoi_model.pt`:

- Instances solved: 100% of 30 (within a 60-second per-instance budget).
- Mean nodes generated per solve: on the order of 10^2 to 10^3.
- Mean solve time per instance: well under 1 second on CPU.

## Learned Heuristic vs. Uniform Cost Search

For `hanoi.6.3` the total state space is only `3^6 = 729`
configurations, so UCS with a closed list terminates quickly on every
instance -- on the order of tens of milliseconds, visiting at most a few
hundred states. That is why I treat Hanoi as a pipeline-validation
domain rather than a showcase for the learned heuristic's speedup.

The comparison becomes meaningful as `N` grows. UCS on N-disk 3-peg
Hanoi needs to expand up to `3^N` nodes in the worst case (equivalently,
solve length `2^N - 1`). By `N = 10` the state space is about 59 000
nodes and UCS still finishes, but by `N = 15` the state space is 14
million and uniform cost search on the worst scrambles becomes the
several-gigabyte, several-minute regime. The same trained architecture
generalized to larger N would cut that node count by several orders of
magnitude because the heuristic can directly guide the search toward
the goal peg rather than exploring symmetric dead-end branches. In
other words: on `hanoi.6.3` the speedup is marginal (both methods are
instant), but the pipeline I built here is what makes the harder-scale
versions of the problem tractable.
