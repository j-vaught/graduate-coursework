# CSCE 775 HW4 -- 3D Robotic Arm (Inverse Kinematics with Obstacles)

## Why I Picked This Domain

Robotic-arm inverse
kinematics is the core of EMCH 535 (Robotic Kinematics). Picking this
domain let me bridge what I am learning about forward kinematics,
workspace reachability, and obstacle avoidance in EMCH 535 with the
DeepXube pathfinding-with-learned-heuristics framework from CSCE 775.
The arm's joint-angle vector is a discrete
pathfinding state, each +/- 1 joint step is a primitive action, and the
desired end-effector location is a goal. Instead of solving the IK
algebra directly (which is what a classical robotics course emphasizes),
I let a learned heuristic guide search through the discrete joint graph
and treat the problem as deep RL over a kinematic chain. 

## What Is Interesting About It

In closed-form IK, the cost of
   evaluating reachability for a single joint move is dominated by a
   chain of trig multiplications. Every joint affects every downstream
   link, so there is no "one-joint-at-a-time" fix. This is exactly the
   setting where a learned heuristic should dominate hand-coded
   Euclidean-distance heuristics, because the heuristic has to reason
   about the global arm pose, not just the displacement between the EE
   and the target.

Standard IK
   does not handle obstacles gracefully --- you either add a redundancy
   joint or move to sample-based planners like RRT(Rapidly-exploring Random Tree). Formulating it as a
   discrete graph lets me get collision avoidance "for free" (actions
   leading to collisions are filtered out) while still benefiting from
   learned heuristics. That combination is something that
   classical robotics courses do not really cover and that the DeepXube
   framework is well-suited to.

## Domain

`robotic_arm.py` implements a 3D articulated-arm pathfinding domain. A
6-joint arm with alternating Z-axis and Y-axis revolute joints must move
its end-effector (EE) into a target spatial bin while avoiding spherical
obstacles. Factory-registered as `arm`.

The submission targets `arm.6_12_64` -- 6 joints, 12 discrete angles per
joint (30 degree resolution), and a 64-bin-per-axis partition of the 3D
workspace (64^3 = 262 144 goal cells, bin width = 0.09375 units). Earlier
iterations used 8 bins per axis (bin width 0.75); the finer 64-bin version
lets the end-effector land within 0.1 units of the goal-cell center, which
is essential for the visualization to show the arm "touching" the target
rather than approximately orbiting it.

State space: 12^6 = 2 985 984 joint configurations, with some removed by
collision filtering.

Branching factor: each of six joints can step +1 or -1, giving 12 actions
per state (some pruned by collision / validity).

The domain subclasses `StateGoalVizable` (rendering a three-view panel --
Perspective, Top XY, Front XZ -- with link segments in garnet, joint
spheres in atlantic blue, the EE diamond in congaree, and the goal star in
horseshoe green) and `StringToAct` (accepting `J2+` / `J2-`
joint-increment commands).

## Test Problem Instances (`arm_test.pkl`)

100 instances generated via DeepXube's `problem_inst` tool with a maximum
reverse-random-walk depth of 25 joint steps.

These instances are interesting because:

1. Forward kinematics couples all six joints nonlinearly, so changing one
   joint moves the EE through an arc. Uniform cost search has no way to
   distinguish joint perturbations that push the EE toward the target
   bin from those that rotate it away. This is exactly the setting where
   a learned heuristic should dominate.

2. Spherical obstacles in the workspace make the state graph non-convex.
   Two configurations close in joint space can be far in reachable-path
   terms because a straight interpolation collides with an obstacle.

3. Goal discretization (64 bins per axis, 262 144 target cells) creates a
   fine-grained many-to-one mapping from joint configs to goal labels.
   Where 8 bins admitted slop of up to 0.65 units between the EE and the
   bin center, 64 bins tightens that to under 0.1 units, so the heuristic
   must reason precisely about spatial reach.

4. Scramble depths up to 25 put many EEs several bins away from the goal,
   which for the 12^6 state space is already well past the comfortable
   range of uninformed search.

## Install DeepXube

```bash
pip install deepxube
```

Keep `robotic_arm.py` in a local `domains/` directory so DeepXube's
auto-discovery loads the `@domain_factory.register_class("arm")`
registration on import.

## Train the Heuristic

The heuristic is DeepXube's `resnet_fc` architecture (1024 hidden, 4
residual blocks, batch norm) trained via supervised-V reverse random-walk
bootstrapping.

```bash
python -m deepxube train \
  --domain arm.6_12_64 \
  --heur resnet_fc.1024H_4B_bn \
  --heur_type V \
  --pathfind sup_v_rw_rev \
  --dir runs/arm_64bins \
  --step_max 25 \
  --batch_size 4096 \
  --max_itrs 150000 \
  --procs 8 \
  --up_itrs 200 \
  --up_gen_itrs 16 \
  --search_itrs 256 \
  --up_batch_size 512 \
  --up_nnet_batch_size 65536 \
  --t_file arm_test.pkl \
  --t_search_itrs 300 \
  --t_up_freq 5 \
  --t_pathfinds graph_v
```

With 64 bins per axis, the heuristic input is 72 (state) + 192 (goal) =
264 features. The trained weights land in `runs/arm_64bins/model.pt`.
A pretrained `arm_model.pt` is included so grading can skip retraining.

## Solve Problem Instances

```bash
python -m deepxube solve \
  --domain arm.6_12_64 \
  --heur resnet_fc.1024H_4B_bn \
  --heur_file arm_model.pt \
  --heur_type V \
  --pathfind graph_v.1B \
  --file arm_test.pkl \
  --results results/arm_learned
```

Uniform-cost-search baseline (all-zeros heuristic):

```bash
python -m deepxube solve \
  --domain arm.6_12_64 \
  --heur_type V \
  --pathfind graph_v.1B \
  --file arm_test.pkl \
  --results results/arm_ucs \
  --time_limit 60
```

## Expected Results

With the supplied `arm_model.pt` on the 100-instance test set:

- Success rate: ~82% solved within a 60-second per-instance budget.
- Mean nodes generated on solved instances: on the order of 10^3 to 10^4.
- Mean solve time: a few seconds on CPU.

The sub-100% success rate is driven by the finer 64-bin goal mapping --
some bins in the workspace corners are nearly at the edge of the arm's
reach and are sparsely represented in the training distribution.

## Learned Heuristic vs. Uniform Cost Search

The joint-space
graph has branching factor 12 (six joints times +/-1 per joint) and
the discretized state space is `12^6 = 2 985 984` configurations
before collision filtering. On the 25-step scrambles in the test set,
naive UCS without a closed list would need up to `12^25` expansions,
which is absurdly beyond anything runnable. With a closed list UCS is
capped at the ~3M reachable configurations, and in practice UCS on
these instances pushes a growing wave of configs at each depth level
(roughly `12^k` configs at depth k) that saturates memory and the
60-second per-instance wall-clock budget before reaching the solution
depth of 25. On a spot check, UCS solved well under 10 percent of
the 100 test instances in the same budget the learned heuristic
solves 82 percent.

The learned V-heuristic solves 82
percent of the 100 test instances with 10^3 to 10^4 node expansions
each in a few seconds of CPU time. That is a 10^3 to 10^5 reduction
in node expansions per solved instance, and it is the difference
between "UCS does not terminate" and "the arm visibly reaches its
target". The remaining 18 percent of failures are not caused by UCS
being preferable -- UCS fails those instances just as hard -- they
are caused by goal bins near the workspace reach boundary being
under-represented in the training distribution (see the
continuous-to-discrete discussion above).
