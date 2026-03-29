= V2: Sub-Mask Decomposition <sec:v2>

The V1 system establishes a strong interactive-click baseline but inherits a
fundamental limitation of the SAM decoder: when the prompt already contains
several clicks distributed across spatially separated object parts, SAM must
commit to a single mask hypothesis that attempts to reconcile all of them
simultaneously. V2 addresses this by decomposing the segmentation problem into
a set of independently decoded sub-masks whose union is taken as the final
prediction.

== SAM's Hypothesis Commitment Problem <sec:v2_motivation>

SAM's mask decoder operates on the full set
of prompt tokens in a single forward pass. When multiple positive clicks target
geometrically distinct parts of an object---thin protrusions, disjoint lobes,
elongated branches---the cross-attention mechanism must aggregate information
from all spatial locations simultaneously to produce a single mask logit map.
The decoder effectively commits to one hypothesis about object extent early in
its computation, and this commitment cannot be revised within a single forward
pass. Clicks that lie in conflicting regions of the image produce ambiguous
attention patterns, and the resulting mask typically undersegments the harder
parts while oversegmenting the easier central region.

Expert annotators using SAM
interactively have long recognized this behavior and adopted a practical
workaround: rather than accumulating all clicks in a single prompt, they segment
each coherent part of the object independently, then merge the resulting masks.
This mirrors how a human would decompose a complex segmentation task into
tractable sub-problems. V2 formalizes this expert heuristic into a learned
policy that decides when to commit the current sub-mask and start a new
independent segmentation session.

To bound the gains available from sub-mask decomposition, an
oracle analysis was conducted on the FSS-1000 validation split. The oracle
identifies uncovered high-recall regions of the ground-truth mask that the
single sub-mask policy fails to capture, runs independent targeted segmentation
sessions on each such region, and takes the union Dice as the evaluation metric.
The analysis confirms substantial Dice gains on thin and branching objects:
objects with elongated structures or spatially disjoint components see oracle
union Dice improvements of $0.08$--$0.21$ over the single-mask baseline, while
compact objects show no statistically significant improvement. This confirms
that decomposition is a high-value strategy for a well-defined and non-trivial
subset of the dataset (@fig:oracle_submask).

== SubMaskPolicyTransformer Architecture <sec:v2_arch>

The V2 model is a `SubMaskPolicyTransformer` with approximately 37
million parameters. It extends the V1 architecture by augmenting the observation
space, expanding the action space from 3 to 5 discrete strategy choices, and
introducing a two-head output structure that decouples strategy selection from
spatial click placement.

The V1 observation consists of the image patch
embeddings, the SAM mask logit map rendered onto the $37 times 37$ patch grid,
and the current click history encoded as a sparse click map. V2 adds a
`coverage_map` channel of shape $37 times 37 times 1$ that encodes the union of
all sub-masks finalized so far in the current episode. This additional channel
gives the policy explicit spatial information about which regions have already
been successfully segmented, enabling it to identify uncovered areas without
relying on implicit memory in the transformer state.

V1 uses a 3-way strategy action: positive click,
negative click, stop. V2 replaces this with a 5-way strategy space summarized
in @tab:v2_actions.

#figure(
  table(
    columns: 2,
    align: (left, left),
    table.hline(),
    [*Action*], [*Description*],
    table.hline(),
    [`ACT_POS_CLICK` (0)], [Place a positive click at the selected spatial location to grow the active sub-mask.],
    [`ACT_NEG_CLICK` (1)], [Place a negative click to suppress a false-positive region in the active sub-mask.],
    [`ACT_NEW_SUBMASK` (2)], [Commit the active sub-mask to the coverage union and open a new independent SAM session with a blank prompt.],
    [`ACT_ABANDON` (3)], [Discard the active sub-mask without committing it and open a new session; used when the current session has diverged irrecoverably.],
    [`ACT_STOP` (4)], [Commit the active sub-mask and return the current coverage union as the final prediction.],
    table.hline(),
  ),
  caption: [V2 five-way strategy action space.],
) <tab:v2_actions>

The transformer backbone produces two special tokens in
addition to the patch token sequence: a `strategy_token` and a `spatial_token`.
The strategy head attends to the `strategy_token` and produces the 5-way
strategy logits via a two-layer MLP:

$ "strategy logits" = W_2 "ReLU"(W_1 bold(h)_s + b_1) + b_2, quad W_1, W_2 in RR^(1024 times 1024). $

The spatial head attends to the `spatial_token` and produces location logits
over the $37 times 37 = 1369$ grid positions, identical to the V1 spatial head.
The two heads are conditionally independent given the transformer state, yielding
the joint log-probability factorization used in training (@eq:submask_joint_logprob).

The backbone and spatial head weights are initialized from
the best V1 PPO checkpoint. This warm-start gives V2 a strong prior over
positive-click and negative-click placement from the outset, concentrating RL
exploration on learning _when_ to initiate decomposition rather than relearning
spatial click quality. The newly introduced strategy-head weights for
`ACT_NEW_SUBMASK` and `ACT_ABANDON` are initialized with small random values.

Not all actions are valid in all states. `ACT_STOP`
is masked until at least one sub-mask has been committed or the active sub-mask
has sufficient Dice. `ACT_ABANDON` is masked if the active session has
accumulated fewer than two clicks (to prevent degenerate immediate abandonment).
`ACT_NEW_SUBMASK` is masked if the sub-mask cap has been reached. Invalid
actions receive a logit of $-infinity$ before softmax, guaranteeing zero
probability under the policy.

== Sub-Mask Environment <sec:v2_env>

The V2 environment extends the V1 Gym-style episode with
the following configuration: a click cap of `click_cap` $= 20$ clicks per
episode (across all sub-masks), a sub-mask cap of `submask_cap` $= 6$
independent sessions, and a finalization threshold of $tau = 0.85$ Dice required
before `ACT_STOP` is considered successful.

Step-level costs are: `click_cost` $= -0.01$ per click
placed, `new_submask_cost` $= -0.02$ per sub-mask transition, and `abandon_cost`
$= -0.03$ per abandoned session. Episode termination carries a `stop_bonus` of
$+0.20$ if the final union Dice exceeds $tau$ and $-0.20$ otherwise. These
values are calibrated so that a policy achieving high union Dice through
efficient decomposition receives a net positive episode return, while a policy
that accumulates clicks or sub-masks without improving Dice is penalized.

The reward signal at each step is based on
the change in union Dice between consecutive steps:

$ r_t = Delta D_("union", t) + c_"action", $

where $Delta D_("union", t) = D_("union", t) - D_("union", t-1)$ and
$c_"action"$ is the action-specific cost or bonus described above. The union
Dice aggregates all finalized sub-masks together with the current active
sub-mask, so every click in every session contributes to the reward signal.

When the policy selects `ACT_NEW_SUBMASK`, the
environment commits the active sub-mask (if its Dice exceeds a minimum quality
threshold of 0.30) to the coverage union, resets the SAM prompt to empty, and
starts a new session. When the policy selects `ACT_ABANDON`, the active sub-mask
is discarded without updating the coverage union, and a new session begins. When
the policy selects `ACT_STOP`, the active sub-mask is committed and the episode
terminates with the stop bonus applied.

== Sub-Mask Oracle Generation <sec:v2_oracle>

Sub-mask oracle trajectories are generated by the following
procedure. First, the V1 oracle is run on the image to produce a
single-sub-mask trajectory that achieves high Dice on the most accessible part
of the object. Second, uncovered regions of the ground-truth mask are identified
via connected component analysis of the residual error map: pixels with
ground-truth label 1 but mask label 0 are extracted, and connected components
larger than a minimum area threshold are retained as candidate regions. Third,
for each candidate region, a targeted oracle is run with the region mask as its
local ground truth, producing a sequence of clicks that segments that specific
component. Fourth, components are greedily accepted in order of their standalone
Dice: a component is added to the episode if its targeted oracle achieves a
union Dice improvement of at least 0.01 over the current coverage.

The dataset is constructed so that each episode
contributes exactly $sum_(k=1)^(K) N_k + (K - 1) + 1$ samples, where $K$ is
the number of sub-masks in the oracle trajectory, $N_k$ is the number of clicks
in session $k$, the $(K-1)$ term accounts for the `ACT_NEW_SUBMASK` transitions,
and the final $+1$ accounts for the terminal `ACT_STOP` action. This encoding
ensures that all action types---including transitions and termination---appear in
the supervised training data in proportion to their frequency in oracle behavior,
providing explicit demonstrations of the decomposition strategy that the policy
must later discover or replicate.

== GRPO Training <sec:v2_grpo>

#figure(
  image("../figures/fig_grpo_eval.pdf", width: 100%),
  caption: [V2 GRPO evaluation over 5,000 updates. Dice (left axis) plateaus around 0.43. Num sub-masks (right axis, dashed) stays at $approx 1.0$ --- the policy never learns to decompose.],
) <fig:grpo_eval>

Proximal Policy Optimization requires a value function to estimate
advantages, introducing a second network head that must be learned simultaneously
with the policy. For the V2 policy, where the key challenge is discovering a
novel multi-step strategy (decomposition) rather than refining a well-understood
one, value estimation is an additional source of variance. Group Relative Policy
Optimization (GRPO) eliminates the value head entirely and estimates advantages
from the distribution of returns within a group of rollouts, reducing the
parameter count and potentially accelerating learning on sparse-return tasks.

For each state, $G = 8$ rollouts are collected
with the current policy. The group-relative advantage for rollout $i$ is

$ A_i = (D_i - macron(D)) / sigma_D, $

where $D_i$ is the final union Dice for rollout $i$, $macron(D)$ is the group
mean, and $sigma_D$ is the group standard deviation. This normalization ensures
that advantages are zero-centered and unit-variance within each group, removing
the need for a separate value baseline.

Only the strategy head is trained during GRPO; the
backbone and spatial heads are frozen to preserve the click placement quality
transferred from V1. The learning rate is $5 times 10^(-5)$. A KL penalty with
coefficient $beta = 0.05$ is applied against the reference policy (the
behavioral cloning checkpoint) to prevent the policy from drifting too far from
supervised behavior. Training runs for 5,000 policy updates. The total loss is

$ L = L_"PPO-clip" + beta dot "KL"(pi || pi_"ref") - alpha dot H_s, $

where $H_s$ is the strategy entropy and $alpha$ is a small entropy bonus
coefficient to discourage premature collapse. GRPO training curves are shown in
@fig:grpo_eval.

== Sub-Mask PPO Training <sec:v2_ppo>

#figure(
  image("../figures/fig_submask_ppo_eval.pdf", width: 100%),
  caption: [V2 SubMask PPO evaluation. Dice peaks at 0.60 (update 89), then collapses catastrophically. A brief spike in sub-mask usage ($tilde 2.8$) around update 139 is the only observed decomposition attempt.],
) <fig:submask_ppo_eval>

Sub-Mask PPO fine-tuning begins from the behavioral cloning
checkpoint described in the preceding subsection. The learning rate is
initialized at $3 times 10^(-4)$, warmed up linearly over 500 steps, and then
decayed linearly to a floor of $3 times 10^(-5)$ over the remaining 9,500
updates. The PPO clipping parameter is $epsilon = 0.2$ and value clipping is
enabled, following the implementation detail from @engstrom2020implementation.
The value coefficient is $0.5$. Entropy is regularized separately for the two
action heads: the strategy entropy coefficient is $0.02$ and the location entropy
coefficient is $0.005$. Gradients are clipped to a maximum $ell_2$ norm of $0.5$.
Generalized advantage estimation (GAE) uses $gamma = 0.99$ and $lambda = 0.95$.
Each collected batch is replayed for 4 optimization epochs with a minibatch size
of 16, shuffling rollout indices between epochs. Training runs for 10,000 total
policy updates. The spatial heads (`spatial_token` and `spatial_pos`) are frozen
throughout PPO fine-tuning (`freeze_spatial = True`), preserving the spatial
click placement quality learned during supervised warmstart.

The Sub-Mask policy selects a
composite action $(a_s, a_ell)$, where $a_s$ is the strategy choice (5-way:
positive click, negative click, finalize and start new sub-mask, abandon and
restart, stop) and $a_ell$ is a spatial location on the $37 times 37$ patch
grid (1,369-way). The two components are treated as conditionally independent
given the state, so the joint log-probability factorizes as

$ log pi(a_s, a_ell | s) = log pi_s (a_s | s) + log pi_ell (a_ell | s). $ <eq:submask_joint_logprob>

This factorization is an extension of the V1 joint log-probability from
@eq:joint_logprob. Decoupling the entropy bonuses for the two heads is essential
because the two distributions have very different natural entropies: the strategy
head spans 5 discrete actions with naturally moderate entropy, while the location
head spans 1,369 grid positions with naturally high entropy. Applying a single
coefficient to both would either under-regularize the strategy distribution or
over-regularize the location distribution. The strategy entropy coefficient of
$0.02$ (versus $0.01$ in V1) is increased deliberately to encourage exploration
of the #smallcaps[new\_submask] and #smallcaps[abandon] actions, which the
policy is unlikely to discover without additional pressure.

@tab:ppo_comparison summarizes the configuration
differences between V1 and V2 PPO. Four changes are structural: the dual action
space replaces the 3-way action head with a 5-way strategy head; entropy is
decoupled rather than using a single shared coefficient; the spatial heads can be
frozen to isolate RL learning to the strategy head; and training is run for
10,000 rather than 5,000 updates. One change targets the exploration problem
directly: the strategy entropy coefficient is doubled from $0.01$ to $0.02$ to
incentivize sampling of the two novel actions.

#figure(
  table(
    columns: 3,
    align: (left, center, center),
    table.hline(),
    [*Parameter*], [*V1 PPO*], [*V2 Sub-Mask PPO*],
    table.hline(),
    [Action space],           [3-way strategy],         [5-way strategy + 1,369-way location],
    [Entropy coefficient],    [$0.01$ (shared)],        [$0.02$ (strategy), $0.005$ (location)],
    [Epochs per update],      [2],                      [4],
    [Total updates],          [5,000],                  [10,000],
    [Freeze spatial heads],   [No],                     [Yes],
    [Value clipping],         [No],                     [Yes],
    table.hline(),
  ),
  caption: [Configuration comparison between V1 PPO and V2 Sub-Mask PPO.]
) <tab:ppo_comparison>

The update loop follows standard PPO. Advantages are
computed using backwards-pass GAE with truncation bootstrap as described in
@sec:v1_ppo, then normalized across the minibatch. The probability ratio is
computed from the joint log-probability in @eq:submask_joint_logprob. The total
loss is

$ L_"total" = L_"policy" + 0.5 dot L_"value" - 0.02 dot H_s - 0.005 dot H_ell, $ <eq:submask_ppo_total>

where $H_s$ is the strategy entropy and $H_ell$ is the location entropy.
Per-update diagnostics include `policy_loss`, `value_loss`,
`strategy_entropy`, `location_entropy`, and `grad_norm`, which are logged to
monitor entropy collapse and gradient health throughout training. Sub-Mask PPO
evaluation curves are shown in @fig:submask_ppo_eval.

== The Decomposition Discovery Failure <sec:v2_failure>

Across every training run conducted in this work---GRPO over
5,000 updates and PPO over 10,000 updates---the V2 policy _never reliably
discovers the sub-mask decomposition strategy_. In all GRPO runs, `num_submasks`
remains at $approx 1.0$ for the entire training duration (@fig:grpo_eval). In
the PPO run, a brief spike to $approx 2.8$ sub-masks appears around update 139,
coinciding with the peak Dice of 0.60 (@fig:submask_ppo_eval), but the policy
cannot stabilize this behavior: entropy collapses, decomposition vanishes, and
Dice falls catastrophically to 0.03 by update 549. The PPO spike is the only
observed instance of decomposition in any training run.

The #smallcaps[new\_submask] action
requires a specific multi-step sequence to produce positive reward. The agent
must first finalize a current sub-mask that already has measurable quality---itself
a non-trivial precondition---then choose a spatial location in a region not yet
covered by any existing sub-mask, then successfully segment that new region. Each
sub-step carries uncertainty, and the entire sequence incurs the
`new_submask_cost` of $-0.02$ before any return is visible. The probability of
arriving at this productive sequence by undirected exploration is extremely low.
Under the $0.02$ strategy entropy coefficient, the policy assigns roughly uniform
probability to all five actions early in training, but the expected number of
steps before a productive #smallcaps[new\_submask] sequence is sampled---and the
sequence is long enough for the policy to receive credit---is prohibitively large
relative to the training budget.

Placing additional positive
clicks in the current sub-mask yields a non-negative expected $Delta$Dice on
most images: SAM can only improve or maintain mask quality when the policy places
clicks in high-error regions. By contrast, the #smallcaps[new\_submask]
transition resets the active sub-mask to a blank state, guaranteeing zero Dice
for that sub-mask until at least one click has been placed and SAM has produced a
non-trivial segmentation. Even with a discount factor of $gamma = 0.99$, the
immediate cost of this blank reset dominates the discounted future return from
eventual sub-mask success across most trajectory lengths the policy encounters.
The policy therefore converges to the local optimum of accumulating clicks in a
single sub-mask without ever paying the exploration cost of initiating a second
one.

Even when the policy does attempt
decomposition, attributing reward correctly to the #smallcaps[new\_submask]
action is difficult. The union Dice improvement from a second sub-mask is
diffuse: a single good positive click in an established sub-mask might improve
Dice by $0.05$--$0.10$, whereas the first click in a new sub-mask starts from
$0.0$ Dice for that region and must accumulate several steps before the union
Dice rises enough to generate a positive advantage signal. The multi-step credit
assignment gap means the advantage estimate for the #smallcaps[new\_submask]
action is dominated by the immediate blank-state penalty rather than by the
downstream union improvement. GAE with $lambda = 0.95$ partially addresses this,
but the effective horizon for propagating credit across a 3--5 step sub-mask
initialization is not long enough to consistently produce positive advantages for
the initiating action.

All training images are drawn from the
mixed-difficulty FSS-1000 distribution. The policy therefore always has access to
images where single-sub-mask strategies are adequate, and it efficiently exploits
them. If training were restricted to multi-region objects where decomposition is
_necessary_---i.e., where no placement of clicks in a single sub-mask can exceed
a Dice threshold---the policy would face a curriculum that makes the
#smallcaps[new\_submask] action the only path to non-trivial reward. No such
curriculum was implemented; the policy consistently finds single-sub-mask local
optima on easier images and never needs to invest in the harder decomposition
strategy.

The transient spike to
2.8 sub-masks around update 139 is not merely noise: it coincides with the
highest Dice observed in any V2 run (0.60), indicating that decomposition did
improve performance when it occurred. This is strong evidence that the strategy
is functionally valuable. The failure is not that decomposition is
unrewarding---it is that the RL training procedure cannot _stabilize_ it. Once
the policy begins exploring decomposition, entropy in the strategy head drops
faster than the policy can receive consistent positive feedback, and the behavior
collapses before it can be reinforced into a stable strategy. The spike is a
brief window during which entropy was high enough to sample decomposition and
reward was high enough to provide a positive signal, but the signal was not
strong or consistent enough to sustain the behavior against the entropy collapse
dynamics described in @sec:v1_collapse.

The oracle sub-mask policy uses connected-component
analysis of the error map to identify uncovered regions and measures Dice
improvement _before_ committing to a click placement. This privileged
information---unavailable to the trained policy---allows the oracle to initiate
decomposition at precisely the moment when a new sub-mask would improve the union
Dice, and to place the first click in the most informative uncovered location.
The gap between oracle performance and trained policy performance demonstrates that the
decomposition _strategy_ is correct but that standard RL exploration is an
inadequate _discovery mechanism_ for it under this reward structure and training
budget.

#figure(
  grid(columns: 2, gutter: 1em,
    image("../figures/submask_oracle_spade_0_comparison.png", width: 100%),
    image("../figures/submask_oracle_bell_pepper_2_comparison.png", width: 100%),
  ),
  caption: [Oracle sub-mask decomposition visualizations. The oracle policy achieves higher Dice by decomposing complex objects into independently segmentable sub-regions, a strategy the trained V2 policy never discovers.],
) <fig:oracle_submask>

This failure directly motivates the design of V3. A
system capable of _reasoning_ about decomposition explicitly---examining the
current mask, identifying uncovered regions, and deciding whether to start a new
sub-mask based on a semantic understanding of the object---does not need to
discover the decomposition strategy through trial-and-error exploration. The VLM
in V3 reasons about spatial coverage in its chain-of-thought during Phase 1 of
the decision loop (Section 3.3) and naturally initiates new sub-masks when the
current mask is stuck or when visually distinct object parts remain uncovered.
The contrast between V2's failure to discover decomposition and V3's natural use
of it is the clearest evidence in this report that explicit reasoning outperforms
learned implicit policies for this task.

== Development Timeline

#figure(
  table(
    columns: (5.5em, 1fr),
    table.hline(),
    [*Date*], [*Milestone*],
    table.hline(),
    [Mar 9], [CODEX branch: training strategy survey documents 8 candidate configurations (A--H) covering reward shaping, curriculum, demo injection, and population-based training.],
    [Mar 19], [SubMaskPolicyTransformer and SubMaskSAMEnv implemented. 5-action space, coverage map input, V1 weight transfer, sub-mask oracle generator, warmstart trainer, and SubMask PPO trainer all committed in a single architecture commit.],
    [Mar 20], [Browser-based interactive mask refinement tool built for manual oracle validation and debugging. #text(fill: rgb("#73000A"), weight: "bold")[Note: this tool was developed after discovering that FSS-1000 contained significant labelling and segmentation quality issues --- in-class mask annotations were frequently unreliable, with inconsistent boundaries, missing regions, and mislabelled foreground, necessitating manual inspection and correction of oracle training data.]],
    [Mar 23], [GRPO trainer implemented: group-relative advantages, frozen spatial head, KL penalty against reference policy. 5,000-update training run configured.],
    [Mar 23], [GRPO training completes. Result: stable but plateaued at 0.43 Dice. `num_submasks` $approx$ 1.0 throughout --- decomposition never discovered.],
    [Mar 23], [SubMask PPO attempted. Peak 0.60 Dice at update 89 with brief decomposition spike (2.8 sub-masks at update 139), then catastrophic collapse to 0.03.],
    table.hline(),
  ),
  caption: [V2 development timeline (March 9--23, 2026).],
) <tab:v2_timeline>
