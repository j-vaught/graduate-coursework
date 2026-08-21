= Conclusion and Future Work <sec:conclusion>

== Summary of Findings

This work explored four paradigms for automated prompt optimization for the
Segment Anything Model in one-shot segmentation, spanning graph-based
reinforcement learning, Transformer policy networks, sub-mask decomposition,
and zero-shot vision-language model guidance.

The earliest attempt framed prompt selection as a graph-pruning problem solved
with a Deep Q-Network operating on 25 candidate spatial nodes. Five
compounding design errors rendered meaningful learning impossible: an 8D
summary state that discarded all spatial information, a variable-cardinality
action space with no semantic structure, a proxy reward computed from DINOv2
feature distances that was _anti-correlated_ with actual SAM Dice, an
off-policy training algorithm poorly matched to a rapidly shifting state
distribution, and an evaluation gate that measured proxy reward improvement
while the true objective diverged. Evaluation Dice reached only 0.60 against
a 0.807 oracle baseline. After five days of training and post-mortem analysis,
the approach was abandoned and every major design decision was replaced.

Replacing the lossy state representation with full $37 times 37 times 1024$
DINOv2 features, the action space with direct spatial click placement, and the
proxy reward with actual SAM Dice resolved the Q-learning failures and produced
a tractable learning problem. Behavioral cloning on oracle demonstrations
converged reliably, achieving 0.549 Dice and 91% action classification
accuracy. PPO fine-tuning extracted brief initial gains---peaking at 0.49
Dice around update 29---before catastrophic collapse: entropy dropped from
1.08 nats to near zero, the value function diverged under rapid distribution
shift, and Dice fell below 0.20 and never recovered. The collapse was robust
across all hyperparameter interventions, indicating a structural rather than a
tuning failure.

Motivated by SAM's hypothesis commitment problem, V2 extended the action space
with #smallcaps[finalize-and-start-new] and #smallcaps[abandon-and-restart] actions
to allow the agent to decompose complex objects into independently segmentable
sub-regions. GRPO training eliminated the value head and produced stable, non-
collapsing curves---but plateaued at 0.43 Dice throughout 5,000 updates. PPO
training reached a higher peak of 0.60 Dice at update 89 before suffering the
same catastrophic collapse as V1. The defining result of V2 is that
`num_submasks` remained at $approx 1.0$ throughout _all_
training runs: the policy never discovered the sub-mask decomposition strategy.
A transient spike to 2.8 sub-masks around PPO update 139---coinciding with the
0.60 Dice peak---confirms the strategy is functionally valuable, but standard
RL exploration was insufficient to stabilize it against four compounding
barriers: exploration difficulty, a local optimum in click accumulation,
multi-step credit assignment gaps, and the absence of a decomposition-forcing
curriculum.

Replacing the learned policy entirely with a frozen vision-language model
eliminated the exploration problem by substituting chain-of-thought visual
reasoning for trial-and-error. A 4-panel visual state renderer (reference
image, query image, current mask overlay, error heatmap) and a three-phase
decision loop (decide, verify, review) gave the VLM concrete visual evidence
at every inference step. On a 15-class FSS-1000 ablation, V3 achieved 0.776
mean Dice with only 1.3 clicks. The best single run reached 0.853 Dice with
1.4 clicks, and a broader 10-image evaluation produced 0.724 Dice with 1.1
clicks. V3 outperformed every trained policy with no task-specific training,
and naturally employed sub-mask decomposition---a strategy V2 never
discovered---whenever the current mask stalled on a complex object.

== Key Lessons

1. The Q-learning proxy reward (DINOv2 feature-space distance) was not merely a
weak proxy---it was actively anti-correlated with SAM Dice in the empirical
state distribution, steering the policy away from useful behavior. This is a
direct instance of Goodhart's Law: when a measure becomes a target, it ceases
to be a good measure @ng1999reward. Every system in this work that used
the actual SAM Dice as the reward---computed by querying SAM at every step---
produced a tractable learning signal. Every system that used a proxy failed
irreversibly. The lesson generalizes: for any RL system with a differentiable
environment oracle, computing the true objective at training time is almost
always worth the cost.

2. Sub-mask decomposition requires a precisely ordered sequence of actions to
produce positive reward: a high-quality first sub-mask must already exist,
the policy must pay an upfront cost to initiate a new sub-mask, the new
sub-mask must then be successfully populated, and the union improvement must
overcome the blank-state penalty. Four independent barriers---exploration
difficulty, click-accumulation local optima, credit assignment gaps, and the
absence of a curriculum---each made the strategy unlikely to be sampled. The
fundamental constraint is that RL reward signals cannot guide exploration
toward strategies that require multiple prerequisite conditions to be satisfied
jointly before any reward is observable. Curriculum learning, imitation
learning from structured demonstrations, or explicit privileged information
(as in the oracle) are each better suited than undirected exploration for
discovering such strategies.

3. V3 achieved 0.776 mean Dice with zero task-specific training while V2's best
checkpoint reached 0.610 Dice after thousands of gradient updates. The
difference is not parameter count or training data---it is _reasoning
form_. The VLM's chain-of-thought reasoning identifies uncovered object
regions, interprets SAM's error heatmap, and selects sub-mask initiation as
an explicit strategic choice rather than a random exploration outcome. For
tasks that require spatial understanding, error analysis, and adaptive strategy
selection, pre-trained visual reasoning capacity provides a stronger inductive
bias than any policy architecture trained from scratch on task-specific reward.

4. V3's undo mechanism---enabled by the Phase 3 review step---allows the policy
to revert a bad click before it degrades the accumulated mask. This monotonic
improvement guarantee proved critical: V1 and V2 both exhibit mask degradation
when corrective clicks are placed incorrectly, and neither architecture has a
recovery mechanism. V3 used 1.3 clicks to achieve 0.776 Dice precisely because
bad clicks were immediately undone rather than compounded. The architecture
lesson is that interactive policies should invest in correction capacity rather
than click precision, since even a high-quality policy will occasionally place
a suboptimal click.

5. The progression from 8D aggregate summary (Q-learning) to full $37 times 37
times 1024$ spatial features (V1/V2) to rendered 4-panel visual state (V3)
drove the largest performance improvements at each stage---larger than any
change in training algorithm, architecture size, or reward shaping. The
$8"D" arrow.r "full-tensor"$ transition made credit assignment feasible. The
$"full-tensor" arrow.r "rendered-image"$ transition enabled qualitative
reasoning about object boundaries, error patterns, and spatial coverage. No
learning algorithm can recover information that the state representation has
discarded; improving the representation ceiling always dominates improving
the optimizer.

== Future Work

V3's primary deployment limitation is inference cost: three VLM calls per step
at 8B parameter scale makes real-time use impractical. The most direct path to
closing this gap is behavioral cloning from VLM-generated trajectories. We
plan to scale trajectory collection to 50--100 FSS-1000 classes (from the
current 15-class ablation set) and train a compact PolicyTransformer on the
resulting demonstrations, with VLM reasoning traces included as auxiliary
supervision to encourage the distilled policy to internalize the strategic logic
rather than only the action outputs. Target: VLM-level segmentation quality at
$120 times$ inference speedup.

V2's exploration barrier analysis identifies the absence of a decomposition-
forcing curriculum as a primary cause of the strategy discovery failure. A
natural remedy is to pre-train on a curated split of FSS-1000 restricted to
objects with two or more spatially disjoint parts---spades, insects with
separated wings, utensils---where no single-sub-mask strategy can exceed a Dice
threshold of 0.70. Within this curriculum, the #smallcaps[new_submask] action
becomes the _only_ path to non-trivial reward, eliminating the local
optimum that prevented exploration in the mixed-difficulty setting. Gradually
expanding the training distribution to include easier single-region objects may
then allow the policy to generalize the decomposition strategy it learned under
curriculum to cases where it is beneficial but not strictly required.

A third direction that does not require full distillation is a hybrid
architecture in which V3 handles the initial click placement---where reasoning
about the reference image and the query structure provides the largest quality
gain---and then hands off to a compact trained policy for iterative refinement
within a single sub-mask. This approach amortizes the VLM inference cost
across the episode: one VLM call per episode (or per sub-mask) rather than
three calls per step. The compact policy handles the low-level corrective
clicking that can be learned reliably from oracle demonstrations without
requiring qualitative reasoning.

All quantitative results in this report use FSS-1000, a general object
segmentation benchmark. Kvasir-SEG @jha2020kvasir, a medical polyp
segmentation dataset, provides a challenging out-of-distribution evaluation: the
domain (endoscopic imagery), object characteristics (irregular boundaries,
low texture contrast), and target use case (clinical decision support) all
differ substantially from FSS-1000. Cross-domain evaluation would test whether
V3's visual reasoning generalizes beyond the training distribution and whether
the distilled policy retains that generalization.

The current V3 results use Qwen3-VL-8B-Instruct without any task-specific
fine-tuning. Two natural scaling directions remain unexplored: larger VLM
backbones (32B and 72B parameter variants) that may provide qualitatively
better spatial reasoning, and more diverse prompt strategies including
structured object decomposition instructions, chain-of-thought templating for
error analysis, and multi-turn dialogue that maintains explicit working memory
of previous sub-mask outcomes.

== Projected Timeline

#figure(
  table(
    columns: 2,
    table.hline(),
    [*Date*], [*Milestone*],
    table.hline(),
    [Mar 28 -- Apr 4],  [Scale VLM trajectory collection to 50--100 FSS-1000 classes],
    [Apr 4 -- Apr 11],  [Behavioral cloning distillation: train compact policy from VLM traces],
    [Apr 11 -- Apr 18], [RL fine-tuning of distilled policy (GRPO, frozen spatial head)],
    [Apr 18 -- Apr 25], [Full FSS-1000 test evaluation + Kvasir-SEG cross-domain evaluation],
    [Apr 25 -- May 2],  [Final ablation experiments and report writing],
    [May 2 -- May 9],   [Buffer / presentation preparation],
    table.hline(),
  ),
  caption: [Projected timeline through end of semester.],
) <tab:timeline_conclusion>
