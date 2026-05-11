# CSCE 775 HW4 -- Multi-Agent Warehouse Path Finding (4 Robots)

## Why I Picked This Domain

Warehouse multi-agent path finding (MAPF) is the fourth rung of my
progression (Hanoi -> Pancake -> 3D robotic arm -> retro-synthesis ->
four-bar linkage -> warehouse MAPF). I chose it as the multi-agent /
joint-action-space stress test because everything before it had a
single moving object: a single pancake stack, a single arm, a single
chain of carbons. MAPF is the first domain where the action space is
the *Cartesian product* of per-robot actions, not a single primitive.
That changes the search problem qualitatively, not just quantitatively,
and it is the domain that connects most directly to my mechanical
engineering background, since multi-robot warehouse coordination is an
active area in industrial robotics and logistics automation.

The 4-robot setting in particular is a sweet spot: small enough that
the joint action space (5^4 = 625 nominal joint actions before
collision filtering, sampled down to 64 per state during training) is
still manageable on a CPU, but big enough that the state space (about
500 free cells choose 4 = 2.6 * 10^9 placements before considering
robot identity) is intractable for any uninformed search.

## What Is Interesting About It

1. **Cartesian-product action space.** Naive search over the joint
   action space scales as `5^K` for K robots (5 = up/down/left/right
   /wait), so even at K=4 a single state expands into 625 children
   before any pruning. The training script samples down to 64 joint
   actions per state to keep updates tractable, which makes the
   learned heuristic responsible not just for guiding which direction
   to step but for compressing the joint action vocabulary itself.

2. **Inter-agent collisions and goal swaps.** Two robots cannot occupy
   the same cell, cannot swap cells in one step, and the goal
   assignment is identity-tied (robot 1 must reach goal 1, not just
   any goal). That makes "obvious" greedy heuristics fail -- pushing
   each robot toward its own goal independently routinely produces
   deadlocks at chokepoints, and the learned V-function has to encode
   how robots should yield to each other.

3. **Sparse warehouse aisle structure.** The 28x28 grid has fixed
   shelf rectangles separated by single-cell aisles. Many cell pairs
   are "topologically narrow", meaning only one robot can pass through
   at a time. The heuristic has to learn implicitly that some routes
   force ordering constraints between robots.

4. **2D spatial input.** Unlike Hanoi or Pancake (1D vectors), the
   state representation here is genuinely 2D: a 28x28 grid with
   per-robot occupancy channels. This is the first domain in my
   progression where the heuristic input has spatial structure, even
   though the architecture I used is still flat-MLP rather than
   convolutional.

## Domain

`warehouse_mapf.py` implements a discrete warehouse-MAPF domain with
configurable grid size, number of robots, and joint-action sampling
limit. Factory-registered as `mapf`.

The submission targets `mapf.28_28_4_64` -- 28x28 grid, 4 robots, and
a per-state cap of 64 sampled joint actions. The grid uses a regular
shelf pattern with single-cell aisles between rectangular shelf blocks
to mirror real warehouse layouts.

State: positions of all K robots flattened to a `K`-tuple of
free-cell indices.

Goal: target positions for all K robots, with strict identity
matching (robot i must reach goal i).

Action: one direction per robot (Up/Down/Left/Right/Wait), filtered
for cell-occupancy collisions, swap collisions, and obstacle
collisions before being added to the per-state action list.

The domain subclasses `StateGoalVizable` (rendering the grid with
shelves as black blocks, aisles as white cells, robots as colored
circles in the UofSC accent palette, and translucent colored squares
marking each robot's goal cell) and `StringToAct` (accepting joint
direction strings like `U U D R` for the four-robot case).

## Test Problem Instances (`mapf4_test.pkl`)

40 instances generated via DeepXube's `problem_inst` tool with reverse
random-walk depths ranging from 5 to 36 joint steps (mean ~19), so the
test set covers easy two-or-three-move scrambles up through long
walks where coordination across robots becomes essential.

These instances are interesting because:

1. The variable scramble depth gives a curriculum from "trivial" to
   "well past the horizon any uninformed search can handle". A blind
   BFS or UCS hits the joint-action wall (`5^4 = 625` per expansion)
   within a few steps; instances at depth 30+ require the learned
   heuristic to be doing real work.

2. Many of the deeper scrambles end up in configurations where two or
   more robots have to yield down a single-cell aisle, so the learned
   V-function is being tested on its ability to reason about
   inter-agent constraints rather than just per-robot reach.

3. Instances are sampled from valid backward random walks, so every
   instance is provably solvable. This lets us cleanly attribute any
   solver failure to search-budget issues rather than to infeasibility,
   which matters when comparing learned-heuristic vs. UCS success
   rates head-to-head.

## Install DeepXube

```bash
pip install deepxube
```

Keep `warehouse_mapf.py` in a local `domains/` directory so DeepXube's
auto-discovery loads the `@domain_factory.register_class("mapf")`
registration on import.

## Train the Heuristic

The heuristic is DeepXube's `resnet_fc` architecture (128 hidden, 2
residual blocks, batch norm) trained via supervised-V reverse
random-walk bootstrapping. The 128H_2B_bn config is intentionally
smaller than the architectures used for the single-agent domains
because the joint-action space already inflates per-iteration cost.

```bash
python -m deepxube train \
  --domain mapf.28_28_4_64 \
  --heur resnet_fc.128H_2B_bn \
  --heur_type V \
  --pathfind sup_v_rw_rev \
  --dir runs/mapf4 \
  --step_max 40 \
  --batch_size 4096 \
  --max_itrs 100000 \
  --procs 8 \
  --up_itrs 200 \
  --up_gen_itrs 16 \
  --search_itrs 128 \
  --up_batch_size 512 \
  --up_nnet_batch_size 65536 \
  --t_file mapf4_test.pkl \
  --t_search_itrs 2000 \
  --t_up_freq 5 \
  --t_pathfinds graph_v
```

Trained weights land in `runs/mapf4/model.pt`. A pretrained
`mapf4_model.pt` is included so grading can skip retraining.

## Solve Problem Instances

```bash
python -m deepxube solve \
  --domain mapf.28_28_4_64 \
  --heur resnet_fc.128H_2B_bn \
  --heur_file mapf4_model.pt \
  --heur_type V \
  --pathfind graph_v.1B \
  --file mapf4_test.pkl \
  --results results/mapf4_learned
```

Uniform-cost-search baseline (all-zeros heuristic):

```bash
python -m deepxube solve \
  --domain mapf.28_28_4_64 \
  --heur_type V \
  --pathfind graph_v.1B \
  --file mapf4_test.pkl \
  --results results/mapf4_ucs \
  --time_limit 60
```

## Expected Results

With the supplied `mapf4_model.pt` on the 40-instance test set:

- Success rate: high majority solved within a 60-second per-instance
  budget on CPU.
- Mean nodes generated on solved instances: on the order of 10^3 to
  10^4.
- Mean solve time: a few seconds for short scrambles, growing to tens
  of seconds for the deepest scrambles.

## Learned Heuristic vs. Uniform Cost Search

This domain is where the joint-action curse becomes the whole story.
With K=4 robots and 5 primitive directions per robot, every state
expands into up to `5^4 = 625` children. The training pipeline samples
that down to 64 per state to be tractable; UCS without sampling would
explode at every expansion. Even with a closed list, the underlying
configuration space is on the order of `(free_cells choose K) * K!`,
which is a few times `10^9` on a 28x28 grid with shelves -- well past
the limit where blind enumeration is feasible.

Concretely on the test set, UCS without a heuristic only solves the
shortest scrambles (depth 5-7) within the 60-second per-instance
budget. By scramble depth 15+ UCS effectively never returns. The
learned V-heuristic, trained for 100K iterations on reverse random
walks, expands 10^3 to 10^4 nodes per solved instance regardless of
scramble depth -- a 10^3 to 10^5 reduction in node count compared to
the BFS frontier UCS would have to push.

The mechanical-engineering tie-in: classical multi-robot warehouse
coordination uses centralized scheduling (CBS, ICTS) or decoupled
priority-based planners. Discrete graph search with a learned V is
neither -- it learns the coordination implicitly from data and so
sidesteps the algorithmic machinery those classical methods need,
while keeping a clean discrete-graph formulation that can be audited
move-by-move. That makes this domain both a non-trivial DeepXube
showcase and a directly-relevant research direction for industrial
robotics.
