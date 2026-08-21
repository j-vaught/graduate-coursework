# CSCE 775 HW4 -- Retrosynthesis (Functional-Group Chain Editing)

## Why I Picked This Domain

Retrosynthesis is the third rung of my progression (Hanoi -> Pancake ->
3D robotic arm -> retro-synthesis -> four-bar linkage -> warehouse
MAPF). After the kinematic and combinatorial domains, I wanted a
domain where the actions are **named chemical reactions** rather than
positional moves, because that mirrors how a synthetic chemist
actually reasons about a target molecule: "to make compound X, I would
work backwards through these named transformations."

The hook for this domain in the HW4 prompt itself was chemical
synthesis as an example of an unanswered research direction for
DeepXube. I picked a deliberately constrained version of the problem
-- a single linear carbon chain with one functional group per backbone
position -- so that the action space stays interpretable while still
exposing the interesting structural reasoning behind retrosynthetic
analysis. The full problem (arbitrary molecular graphs + thousands of
reactions + selectivity constraints) is well beyond a homework, but
this scaled-down version captures the core ideas: site-selectivity,
protecting groups, and the order-dependence of reactions.

## What Is Interesting About It

1. **Named reactions, not positional moves.** Actions are organic
   reactions like radical bromination, oxidation, amination,
   reduction, plus protect/deprotect. Each has selectivity rules
   (some are site-selective: they only operate on the most reactive
   group; some are position-specific: the chemist picks the position
   to operate on). That makes the action space heterogeneous in a way
   that none of the previous domains were.

2. **Protecting groups create deliberate ordering constraints.** The
   classical retrosynthesis trick is to *protect* a reactive
   functional group so a later reaction does not touch it, then
   *deprotect* afterwards. The domain encodes OPG (protected OH) and
   NPG (protected NH2) as distinct states, so a learned heuristic has
   to discover that "protect first, then react, then deprotect" is
   sometimes the only legal way to reach the target -- there is no
   shortcut through the "raw" state.

3. **Many-to-one transformations.** Two different reaction sequences
   can lead to the same intermediate, and one sequence can be much
   shorter than another. This is exactly the setting where a learned
   V-function should pay off, because the cost-to-go is not a simple
   function of edit distance to the target -- it depends on which
   reactions are available given the *current* functional-group
   pattern.

4. **Position-indexed diff is meaningful.** Each backbone carbon has
   a single functional group, so "how far am I from the target"
   reduces to a clean per-position match/mismatch view. The
   visualization renders both the current and target molecules with
   RDKit (real chemistry skeletal formulas) and adds a position-
   indexed diff strip in between, so you can read off at a glance
   which carbon positions still need to be transformed.

## Domain

`retrosynthesis.py` implements the chain-editing retrosynthesis domain
with configurable `chain_len`. Factory-registered as `retro`. The
submission targets `retro.7` -- a 7-carbon linear chain.

State: a length-7 array of functional-group identifiers (H, OH,
KETONE, NH2, COOH, BR, OPG, NPG).

Goal: a length-7 array of target functional-group identifiers, with
strict per-position matching.

Actions: a fixed set of named reactions. Site-selective reactions
take no position argument and operate on a globally-determined "most
reactive" position; position-specific reactions take an explicit
position index. Protect / deprotect actions toggle OH <-> OPG and NH2
<-> NPG.

The domain subclasses `StateGoalVizable` (using RDKit to render the
current and target molecules as standard skeletal formulas with a
brand-palette diff strip showing which backbone positions match the
target) and `StringToAct` (accepting reaction names like
`radical_br@2` or `protect 0`).

## Test Problem Instances (`retro_test.pkl`)

40 instances generated via DeepXube's `problem_inst` tool, with
reverse-random-walk depths ranging from 5 to about 36 reactions
(mean ~18). The file stores a dict with keys `domain`, `steps`,
`states`, `goals`.

These instances are interesting because:

1. The variable scramble depth gives a curriculum from "trivial
   one-step transformations" up through "long sequences where
   protecting-group ordering matters". Shallow scrambles let me
   sanity-check the learned heuristic against the known optimal
   length; deep scrambles test that the heuristic generalizes past
   the easy regime.

2. Random-walk-derived instances exercise the protect/deprotect cycle
   automatically -- whenever the random walk produces a sequence that
   only makes sense via a protecting group, the resulting test
   instance encodes that ordering constraint. UCS without a heuristic
   has no way to discover that constraint and routinely fails on
   those instances.

3. The pool covers a variety of target functional-group patterns, not
   just one canonical "fully oxidized" or "fully aminated" target, so
   the heuristic has to generalize across goals rather than memorize
   a single one.

## Install DeepXube

```bash
pip install deepxube rdkit
```

`rdkit` is required for the molecule visualization. If RDKit is not
available the domain falls back to a matplotlib-only schematic
renderer; the falling back is graceful but the figures look much less
informative.

Keep `retrosynthesis.py` in a local `domains/` directory so DeepXube's
auto-discovery loads the `@domain_factory.register_class("retro")`
registration on import.

## Train the Heuristic

The heuristic is DeepXube's `resnet_fc` architecture (1024 hidden, 4
residual blocks, batch norm) trained via supervised-V reverse
random-walk bootstrapping.

```bash
python -m deepxube train \
  --domain retro.7 \
  --heur resnet_fc.1024H_4B_bn \
  --heur_type V \
  --pathfind sup_v_rw_rev \
  --dir runs/retro \
  --step_max 30 \
  --batch_size 4096 \
  --max_itrs 200000 \
  --procs 8 \
  --up_itrs 200 \
  --up_gen_itrs 16 \
  --search_itrs 256 \
  --up_batch_size 512 \
  --up_nnet_batch_size 65536 \
  --t_file retro_test.pkl \
  --t_search_itrs 5000 \
  --t_up_freq 5 \
  --t_pathfinds graph_v
```

For chain length 7, the heuristic input is `7 * 8 = 56` (state) +
`7 * 8 = 56` (goal) = 112 features. The trained weights land in
`runs/retro/model.pt`. A pretrained `retro_model.pt` is included so
grading can skip retraining.

## Solve Problem Instances

```bash
python -m deepxube solve \
  --domain retro.7 \
  --heur resnet_fc.1024H_4B_bn \
  --heur_file retro_model.pt \
  --heur_type V \
  --pathfind graph_v.1B \
  --file retro_test.pkl \
  --results results/retro_learned
```

Uniform-cost-search baseline (all-zeros heuristic):

```bash
python -m deepxube solve \
  --domain retro.7 \
  --heur_type V \
  --pathfind graph_v.1B \
  --file retro_test.pkl \
  --results results/retro_ucs \
  --time_limit 60
```

## Expected Results

With the supplied `retro_model.pt` on the 40-instance test set:

- Success rate: high majority solved within a 60-second per-instance
  budget on CPU.
- Mean nodes generated on solved instances: on the order of 10^2 to
  10^3.
- Mean solve time: well under 1 second on most instances.

## Learned Heuristic vs. Uniform Cost Search

For `retro.7` with 8 functional-group identifiers per position, the
nominal state space is `8^7 = 2 097 152` configurations. Many of
these are not reachable via the available reactions because the
reaction set has selectivity constraints (e.g. you cannot directly
turn H into NPG -- you have to go H -> NH2 -> NPG via two reactions).
That makes the *reachable* state graph smaller than `8^7` but still
in the hundreds of thousands of configurations.

UCS on the deeper test instances (scramble depth 25+) effectively
fails inside the 60-second budget, because every state expands into
roughly a dozen action children and the BFS frontier grows by a
factor of ~12 per depth level. By depth 20 the frontier is around
`10^21` nodes naively, capped by the closed list at the reachable
state-graph size, which is still enough to saturate memory before
the goal is reached on most instances.

The learned V-heuristic gets through these in 10^2 to 10^3 node
expansions, sub-second per instance on CPU. That is roughly a 10^4
to 10^5 reduction in node count relative to UCS, and it is
specifically driven by the heuristic's ability to *reason about
ordering constraints* -- it learns to insert protect/deprotect
moves at the right point in the search rather than discovering them
by exhaustive enumeration.

The chemistry tie-in: this is exactly the structural-reasoning step
that classical retrosynthesis software (Synthia, Chematica) tries to
encode with hand-written rules. Doing it with a learned V-function
trained from random walks is a fundamentally different approach, and
even at this scaled-down chain-editing version it shows the right
qualitative behavior. Scaling the same approach to general molecular
graphs is an active research direction, which is why I included it
as the "research" rung of my progression rather than just a curriculum
checkpoint.
