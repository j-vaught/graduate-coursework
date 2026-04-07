= Discussion <sec:discussion>

== Why Reinforcement Learning Fails for Interactive Segmentation <sec:disc_rl_fails>

Across three architectures and four training configurations, every RL-based
policy in this work either plateaued far below the oracle or suffered
catastrophic collapse. The failures are not isolated incidents attributable to
a single tuning error; they form a coherent pattern with four compounding
mechanisms.

The earliest failure---the Q-learning agent described in
@sec:qlearn_postmortem ---arose from optimizing a DINOv2
feature-distance proxy rather than the true objective. Feature-space proximity
and SAM Dice are not monotonically related: the causal chain
$
  "high DINO similarity" arrow.r "good spatial coverage"
  arrow.r "high SAM Dice"
$
breaks at the middle link. The agent discovered this break empirically by
collapsing the prompt graph to one or two semantically coherent nodes, achieving
maximal proxy reward while producing SAM Dice scores of 0.0. Ng
et al. @ng1999reward establish that a reward shaping function preserves
the optimal policy only when it satisfies a potential-based consistency condition
with respect to the true objective. The DINO-distance proxy violated this
condition not merely in theory but _in the opposite direction_: proxy
improvement was anti-correlated with Dice improvement in the visited state
distribution. This is Goodhart's Law in its sharpest form---the proxy was not
a degraded signal but an adversarial one. No downstream algorithm can recover
from a reward function that actively steers toward the wrong policy. Even after
the pivot to direct SAM Dice rewards in V1, the lesson persists: any future
proxy (e.g., entropy bonuses, coverage rewards) must be verified to be monotone
with the true objective on empirical rollouts before training begins.

V1's behavioral cloning warmstart achieves 0.549 mean Dice by imitating oracle
demonstrations. The oracle policy is deterministic and highly competent;
its trajectories occupy a narrow region of state space consisting of clean,
high-quality intermediate segmentations. BC minimizes cross-entropy loss on
this oracle distribution and consequently learns a policy that is well-calibrated
_within_ that distribution but brittle outside it.

PPO fine-tuning immediately pushes the policy onto its own state distribution,
which diverges from the oracle's as soon as the agent makes a suboptimal click.
A single bad click degrades the mask, producing a state the BC agent never
trained on. The policy's response to this out-of-distribution state is
unreliable, often producing another bad click, which degrades the state further.
The cascade is self-reinforcing: each step away from the oracle distribution
increases the probability of the next mistake, and there is no restoring force.
By update 30, the policy has drifted far enough that the learned value head
can no longer track the return distribution, advantage estimates acquire the
wrong sign, and the clipped surrogate objective drives the policy further into
the degenerate click-exhaustion strategy. Staged training, entropy scaling, and
learning rate annealing all change the rate of drift but not its direction or
ultimate destination. The implication is that BC warmstart followed by
on-policy RL is only safe when the on-policy state distribution closely matches
the BC data distribution---a condition that is very difficult to ensure in a
feedback-driven interactive task.

V2's sub-mask decomposition action #smallcaps[new_submask] requires a structured
multi-step sequence to yield positive reward: the current sub-mask must already
have measurable quality, a new spatial region must be selected, and that region
must be successfully segmented before the union Dice rises enough to produce a
positive advantage signal for the initiating action. Undirected exploration
has negligible probability of sampling this entire sequence productively within
any reasonable training budget.

The standard remedy---increasing the strategy entropy coefficient from 0.01 to
0.02---encourages single-action diversity but does not generate the coordinated
multi-step trajectories that decomposition requires. Entropy bonuses reward the
_distribution_ over the strategy head's output; they say nothing about
the _sequence_ of decisions needed to succeed. The policy accordingly
explores the strategy head uniformly at the single-step level while never
assembling the sequence. The one exception was the transient PPO spike to
2.8 sub-masks around update 139---the only instance of decomposition observed
in any run---which coincided with the highest Dice (0.60) seen in V2, confirming
that decomposition is functionally valuable. The spike collapsed within
${approx}$400 updates because entropy fell before the positive signal could
be consistently reinforced. Discovering multi-step strategies through reward
maximization alone requires either a curriculum that makes the strategy the only
path to reward, or a form of exploration guidance that operates at the trajectory
level rather than the action level.

The contrast between GRPO and PPO in the V2 setting reveals a fundamental
tension. GRPO eliminates the value head---the weakest structural link
identified in @sec:v1_collapse ---and achieves stable, non-collapsing
training over 5,000 updates. However, stability comes at the cost of
capability: GRPO's conservative advantage estimates and frozen spatial head
prevent the policy from making the large exploratory excursions that would be
needed to discover decomposition. The policy plateaus at 0.43 mean Dice and
never leaves the single-sub-mask local optimum.

PPO with full training achieves a higher peak (0.60 Dice) precisely because it
allows larger policy updates and unfrozen spatial heads. But this additional
freedom is also what permits entropy collapse and the subsequent cascade into
degenerate behavior. Every hyperparameter configuration explored in this work
fell on one side or the other of this tradeoff: conservative settings produced
stable plateaus, aggressive settings produced brief peaks followed by collapse.
No configuration successfully stabilized decomposition behavior once it had
been discovered. This suggests the failure is not a hyperparameter problem
but a structural one: the RL objective surface has no basin of attraction near
the decomposition strategy under the current reward design.

== Implicit Policies vs. Explicit Reasoning <sec:disc_implicit_explicit>

The most striking finding of this work is that an 8B-parameter vision-language
model with _zero_ task-specific training outperforms every trained RL
policy by a substantial margin---0.776 mean Dice versus 0.610 for the best RL
configuration. This outcome deserves careful analysis because it bears on the
broader question of when learned implicit policies are appropriate and when
explicit reasoning is more effective.

VLMs such as Qwen3-VL-8B acquire spatial understanding, object recognition, and
error analysis from billions of image-text pairs during pretraining. These
capabilities transfer directly to interactive segmentation without any
task-specific gradient signal. The VLM can locate an object in a reference
image, identify which regions of the query segmentation are incorrect by
comparing the current mask to the reference, and reason about whether a
proposed click location will address the error. None of this required training
on FSS-1000 or SAM-specific data. By contrast, the RL agents must acquire
analogous capabilities entirely from the reward signal---a signal that is
informative only at the granularity of whole-step Dice changes, not at the level
of semantic features or spatial comparisons.

The VLM's reasoning traces (Phase 1 of the decision loop) contain explicit
spatial analysis of the form: "the red region in Panel D is in the upper-left
quadrant, suggesting the mask is missing the top of the object." This is
precisely the reasoning that an RL agent must discover through trial-and-error
exploration of the reward landscape. For the VLM, strategy discovery is not a
training problem at all---it is a prompting problem. The chain-of-thought
mechanism externalizes the multi-step reasoning that RL must encode implicitly
in policy weights, and this externalization makes the strategy directly
observable and correctable by the prompt engineer. The RL agent's strategy is
opaque and can only be evaluated through aggregate metrics on rollouts.

V3's Phase 3 review step---in which the VLM evaluates the post-click mask and
decides whether to undo, continue, or start a new sub-mask---enables
monotonically non-decreasing quality trajectories in practice. When a click
degrades the mask, the VLM observes the degradation, identifies the cause, and
issues an undo before committing. RL policies have no analogous mechanism:
once a bad action is taken, it cannot be undone, and the corrupt state is passed
forward as the new observation. This single capability---post-hoc action
review---is likely responsible for a large fraction of V3's advantage over V1
and V2. V1 and V2 frequently show Dice degradation mid-episode from which the
policy cannot recover; V3 does not, because it checks each action before
committing.

When the VLM observes that the current mask has reached a quality ceiling---a
situation it identifies by comparing consecutive Panel C renders---it
spontaneously selects #smallcaps[new_submask] and refocuses on the uncovered
region. This decision is made by explicit reasoning about spatial coverage,
not by exploring a reward landscape. The contrast with V2 is exact: both
systems have access to the sub-mask decomposition action, but V2's RL training
never stabilizes its use while V3 employs it routinely from the first evaluation.
The difference is not access to the action but the mechanism by which it is
selected.

The VLM approach has practical drawbacks that preclude direct deployment. The
three-phase decision loop requires approximately three VLM forward passes per
click, each taking roughly two seconds on the evaluation hardware, yielding a
per-action latency of $approx 6$ seconds. This is incompatible with
real-time or interactive use. Performance is also sensitive to prompt
engineering: the jump from 0.49 Dice (v1 prompt) to 0.85 Dice (v4 prompt) was
driven entirely by prompt revisions, and further regression is possible if the
prompt is modified incautiously. The model also lacks any mechanism for
incorporating task-specific feedback---it cannot improve from repeated exposure
to FSS-1000 images---and its behavior may degrade on domains not well-represented
in pretraining data. These limitations motivate the distillation path described
below.

== The Distillation Path Forward <sec:disc_distillation>

The findings of this work point to a single most-promising next step:
use VLM-generated trajectories as high-quality demonstrations for training
a compact, efficient policy. This approach, which we call _VLM
distillation_, directly addresses the two core problems identified above:
the failure of RL to discover decomposition strategies, and the inference
cost of deploying an 8B VLM at inference time.

The first step is to run the V3 system on 50--100 FSS-1000 classes and collect
complete decision trajectories. Each trajectory includes: the 4-panel visual
state at every step, the VLM's chain-of-thought reasoning, the proposed action
and coordinates, the Phase 2 verification outcome, and the Phase 3 review
decision (continue, undo, or new sub-mask). Unlike oracle trajectories, which
record only action types and click coordinates, VLM trajectories encode the
reasoning behind each decision. This richer signal is available as auxiliary
supervision during distillation.

The collected trajectories are used to train a compact PolicyTransformer---the
V2 SubMaskPolicyTransformer architecture ($approx 37$M parameters)---via
behavioral cloning. The primary training signal is the same as oracle BC:
cross-entropy loss on strategy head outputs and location head outputs matched
to the VLM's decisions. The key advantage over oracle BC is that VLM
trajectories include _decomposition_ actions, _undo_ decisions, and
the temporal context of Phase 3 reviews. A policy trained on VLM data learns
both where to click _and_ when to decompose from supervised examples,
bypassing the exploration barrier entirely.

Beyond action type and location, VLM trajectories provide three auxiliary
supervision signals unavailable in oracle data. First, _decomposition
context_: because the VLM naturally initiates #smallcaps[new_submask] when stuck,
the training data contains a non-trivial fraction of decomposition episodes,
giving the policy a positive class to learn from. Second, _negative
examples from undo_: when the VLM's Phase 3 review detects degradation and
issues an undo, the pre-undo (state, action) pair becomes a labeled negative
example---the exact situation in which the policy should _not_ place that
click. Third, _spatial reasoning annotations_: the VLM's chain-of-thought
text can be used as auxiliary language supervision to align the policy's internal
representations with the spatial error descriptions the VLM produces, potentially
improving the quality of the learned feature space.

The VLM-BC checkpoint provides a qualitatively better initialization for
subsequent RL fine-tuning than oracle BC does. Three properties reduce the
risk of distribution shift cascade. First, the VLM-BC policy already includes
decomposition behavior, so RL fine-tuning does not need to discover it through
exploration---only to reinforce and sharpen it. Second, VLM trajectories are
more diverse than oracle trajectories: the VLM explores recovery strategies,
correction clicks, and sub-mask initiations that the oracle never demonstrates.
This broader state coverage reduces the probability that on-policy rollouts
encounter states entirely outside the training distribution. Third, the
strategy decisions are already learned at BC time, reducing the optimization
burden for RL to spatial refinement and stopping rule calibration rather than
joint discovery of strategy and placement. GRPO applied to this initialization---
with the spatial head frozen to protect the spatial quality learned from VLM
data---is the most conservative RL configuration and the most likely to produce
stable improvements rather than collapse.

The efficiency goal of distillation is a roughly 120-fold speedup: from
VLM inference at $approx 8$B parameters and $approx 6$ seconds per action,
to a distilled policy at $approx 37$M parameters and $approx 50$ milliseconds
per action. If the distilled policy retains VLM-level Dice quality---a
hypothesis to be verified empirically---the result is a system that is
deployable in real-time interactive settings while maintaining the strategic
capabilities (decomposition, self-correction) that RL alone could not discover.
The gap between oracle BC (0.549 Dice) and VLM zero-shot (0.776 Dice) represents
the headroom available to VLM-BC if distillation is successful; closing even
half of that gap would make the distilled policy the strongest compact model
in this evaluation.
