= Experimental Results <sec:results>

We evaluate all three architectural paradigms on FSS-1000 @li2020fss, a
1,000-class few-shot segmentation benchmark with class-disjoint splits: 800
training classes, 100 validation classes, and 100 test classes. No test-class
images or labels appear in any training loop. Primary evaluation metrics are
mean Dice coefficient (overlap quality), mean IoU, mean clicks per episode, and
stop success rate (fraction of episodes in which the agent issues a terminal
STOP action with Dice $>= 0.85$). Unless stated otherwise, all numbers are
reported on the validation split.

== V1: Behavioral Cloning Warmstart <sec:results_bc>

Supervised warmstart on oracle demonstrations converges
reliably over 48 epochs (Figure @fig:warmstart). Both the action loss and the
location loss decrease monotonically throughout training with no plateau or
divergence, which confirms that the oracle trajectories are internally
consistent and the model has sufficient capacity to fit them. Action
classification accuracy on the held-out validation split reaches *91%*;
location top-5 accuracy (whether the correct patch appears in the model's five
highest-scoring grid cells) reaches *75%*.

Evaluation on the FSS-1000 validation split yields a
mean Dice of *0.549* with a mean click count of *10.0* per episode. The agent
uses its entire click budget on every episode---a direct consequence of
supervised warmstart on oracle trajectories, which themselves never issue an
early-stop because the oracle always seeks maximum Dice within the budget. The
model correctly learns _how to click_ but does not learn _when to stop_.

The 91% per-step action accuracy implies a
structural fragility across multi-step trajectories. For a 10-click episode
under the independence assumption, the probability that every action in the
trajectory is correct is

$ P("fully correct trajectory") approx 0.91^10 = 0.39. $ <eq:compound_error>

In practice, action errors are not independent---a wrong click at step $t$
shifts the SAM mask logits in a way that makes subsequent wrong actions more
likely---so the realized probability is lower still. This compounding error is
one reason the 9% per-step error rate produces a Dice of only 0.549 rather than
the oracle's Dice of $>= 0.85$ at equivalent click budgets.

Comparing the BC agent against the oracle policy
reveals a counter-intuitive result: the oracle requires _more_ clicks than many
natural stopping points but achieves substantially _better_ Dice. The BC agent
arrives at 0.549 Dice after 10 clicks; the oracle, which exhausts the same
budget, reaches $>= 0.85$ Dice. This gap establishes an upper bound on the
performance gain achievable by improving click placement quality within the same
budget, motivating the RL fine-tuning experiments described below.

== V1: PPO Fine-Tuning <sec:results_ppo>

Figure @fig:ppo_eval summarizes PPO fine-tuning from
the BC checkpoint over 5,000 policy updates. The training trajectory divides
into five distinguishable phases. During initial adaptation (updates 0--10),
evaluation Dice is volatile while the policy adapts its value head to the
on-policy return distribution. A period of modest improvement follows (updates
10--29), in which Dice rises from the BC baseline toward the run-peak,
indicating that RL successfully extracts initial gains from the warmstart
initialization. The trajectory reaches its peak at update 29, where evaluation
Dice reaches 0.49. Rapid degradation then sets in (updates 30--60): Dice falls
sharply below 0.30 and the policy begins consuming the full click budget on
every episode. Full collapse is reached at update 60, after which Dice
stabilizes in the 0.15--0.20 range and never recovers for the remaining 4,940
updates.

The most visible behavioral symptom is that mean
clicks per episode converges to 10.0 by update 60 and remains there for all
subsequent updates. The per-step click cost of $-0.01$ is too small relative to
incremental Dice gains from early clicks to make stopping attractive. The
terminal stop bonus of $+0.20$ requires the agent to discover that stopping
_early_ yields higher cumulative reward than continuing---but entropy collapses
before this discovery can occur.

The action-type entropy $H_alpha$ drops from
approximately *1.08 nats* (near uniform over three actions) to *near zero*
within the collapse window. Once entropy collapses, the policy becomes nearly
deterministic and samples the same action type at every state. The entropy bonus
(coefficient 0.01) is insufficient to sustain exploratory behavior, and with
zero entropy there is no mechanism for recovery.

Multiple hyperparameter configurations were
evaluated before concluding that the collapse is structural rather than a tuning
artifact. Interventions included: learning rates spanning two orders of
magnitude, entropy coefficients from 0.001 to 0.05, scaled first-click rewards
to provide denser early feedback, staged training (phase 1 optimizing only the
first click, phase 2 adding correction clicks), and GAE $lambda$ values from
0.90 to 0.99. None of these configurations prevented eventual collapse; they
shifted only the update at which collapse began.

The PPO peak of 0.49 is _worse_ than the BC baseline of 0.549.
PPO fine-tuning not only fails to improve on behavioral cloning---it actively
degrades the policy within 100 updates. This result establishes that standard
PPO with a learned value head is an unreliable training procedure for this task,
motivating the GRPO approach in V2.

== V2: GRPO Training <sec:results_grpo>

Figure @fig:grpo_eval shows GRPO training on the V2
sub-mask environment over 5,000 policy updates. In contrast to V1 PPO, _no
catastrophic collapse occurs_: evaluation Dice fluctuates but never enters a
sustained degradation spiral. This stability validates the core GRPO
hypothesis---that eliminating the learned value head and estimating advantages
from a group of $k = 8$ on-policy rollouts removes the value-divergence feedback
loop responsible for V1's collapse.

Despite stable training, evaluation Dice plateaus at
$approx$ *0.43* throughout the 5,000-update run. The best single evaluation
checkpoint reaches *0.54 at update 389*, marginally matching the BC baseline.
The plateau indicates that GRPO resolves the stability problem but does not
resolve the exploration problem: the policy is stuck in a local optimum.

The most striking finding from GRPO training is
that `num_submasks` remains at $approx$ *1.0* throughout all 5,000 updates. The
V2 policy _never discovers the sub-mask decomposition strategy_, despite the
environment fully supporting it and oracle analysis confirming its value (see
@sec:results_oracle). Strategy entropy decreases slowly during training but does
not collapse, confirming that the policy maintains some exploratory capacity in
its action distribution without translating that capacity into decomposition
attempts.

The GRPO outcome is best described as _safe but stuck_: the
training procedure is stable and reproducible, but the policy converges to a
local optimum that is no better than the BC baseline. The absence of collapse
confirms that GRPO is a more reliable fine-tuning procedure than PPO for this
architecture; the absence of progress beyond 0.54 confirms that stability alone
is insufficient for discovering the decomposition strategy.

== V2: Sub-Mask PPO <sec:results_submask_ppo>

Figure @fig:submask_ppo_eval shows V2 Sub-Mask PPO
training over 5,000 updates starting from the BC checkpoint. PPO achieves a
higher peak Dice than GRPO but at the cost of eventual collapse.

At approximately update 139, `num_submasks` spikes to
$approx$ *2.8*---the only observed instance of sub-mask decomposition across all
training runs in this work. This spike coincides with the run's peak evaluation
Dice of *0.60*, providing direct evidence that decomposition is functionally
valuable when it occurs. However, the policy cannot stabilize this behavior:
strategy entropy collapses, decomposition vanishes, and Dice falls
catastrophically to *0.03* by update 549.

Table @tab:grpo_vs_ppo summarizes the
GRPO-versus-PPO comparison for V2. The two optimizers occupy opposite ends of a
stability-capability tradeoff: GRPO achieves stable training but limited peak
performance; PPO briefly discovers a better strategy (decomposition) but cannot
maintain it.

#figure(
  table(
    columns: 6,
    table.hline(),
    [*Optimizer*], [*Peak Dice*], [*Peak Update*], [*Final Dice*], [*Peak Sub-Masks*], [*Stable?*],
    table.hline(),
    [GRPO], [0.54], [389], [$approx 0.43$], [1.0], [Yes],
    [PPO],  [*0.60*], [*89*], [0.03], [*2.8*], [No],
    table.hline(),
  ),
  caption: [GRPO versus PPO for V2 Sub-Mask policy on FSS-1000 validation.],
) <tab:grpo_vs_ppo>

The PPO spike at update 89--139 represents the one moment across
all training runs in this project where the learned policy exceeded the BC
baseline in both quality (0.60 vs. 0.549) and strategy complexity (multi-sub-mask
decomposition). That this spike exists but cannot be stabilized is the central
negative result of the V2 training effort. The root causes---exploration
difficulty, local optima in click accumulation, multi-step credit assignment
gaps, and absence of a decomposition curriculum---are analyzed in detail in
@sec:v2_failure.

== V3: VLM Prompt Iteration Results <sec:results_vlm>

Table @tab:vlm_iterations presents results across six prompt
engineering iterations, all using Qwen3-VL-8B-Instruct @bai2025qwen25vl in
zero-shot mode with no task-specific fine-tuning. Performance improved
consistently from v1 to v4 through targeted changes to the visual state
representation and decision loop structure.

#figure(
  table(
    columns: 5,
    table.hline(),
    [*Version*], [*$N$*], [*Mean Dice*], [*Clicks*], [*Key Change*],
    table.hline(),
    [v1],     [5],  [0.476],       [6.6],        [Baseline: single-prompt, no verification],
    [v2],     [5],  [0.598],       [5.8],        [Added error heatmap (Panel D)],
    [v2\_r2], [10], [0.616],       [6.7],        [Expanded evaluation set],
    [v3],     [5],  [0.623],       [9.2],        [3-phase loop with spatial verification],
    [v4],     [5],  [*0.853*],     [1.4],        [Post-click review with early stopping],
    [v4\_r2], [10], [0.724],       [*1.1*],      [Broader eval including harder objects],
    table.hline(),
  ),
  caption: [VLM prompt iteration results. All runs use Qwen3-VL-8B-Instruct,
  zero-shot, on FSS-1000 validation. $N$ is the number of evaluation images.
  Clicks is mean clicks per episode. Key Change describes the primary
  modification introduced in that iteration.],
) <tab:vlm_iterations>

Transition Analysis. _v1 $arrow$ v2 (+0.12 Dice):_ Adding Panel D (error
heatmap) gave the VLM explicit spatial evidence of where the current mask
disagrees with the reference class. Without this panel, the model had to infer
error regions from the mask overlay alone, which is ambiguous. The error heatmap
eliminates this ambiguity and allows the model to place corrective clicks
directly on high-error regions. Click count decreased (6.6 $arrow$ 5.8)
alongside the Dice improvement, indicating that the VLM required fewer
corrections when its initial placements were better informed.

_v2 $arrow$ v3 (+0.025 Dice):_ Introducing the 3-phase verification loop
(decide, verify, review) improved spatial precision at the cost of more total
clicks (5.8 $arrow$ 9.2). Phase 2 verification---rendering the proposed click
location and asking the VLM to confirm or adjust before executing---reduced
off-target placements. Phase 3 review provided a mechanism to undo bad clicks,
but also caused the model to issue more total clicks as it iterated toward
confidence. The modest Dice gain (+0.025) relative to the click increase
(+3.4 clicks) indicated that verification alone was insufficient; the model
needed a stronger early-stopping criterion.

_v3 $arrow$ v4 (+0.23 Dice, breakthrough):_ Adding post-click review with early
stopping produced the largest single-iteration gain in the project. After each
click execution, Phase 3 now issues an explicit quality assessment: if the
current mask already exceeds a quality threshold, the VLM issues STOP rather
than placing another click. This change reversed the click count from 9.2 to 1.4
while increasing Dice from 0.623 to 0.853. The mechanism is that the VLM, given
the opportunity to evaluate the mask after each click, discovers that first-click
quality is frequently sufficient---it needed a structured invitation to stop
early rather than assuming more clicks always help. This is the primary
behavioral difference between a VLM policy and a trained RL policy: the VLM can
reason about "is this already good enough?" without ever having been trained on
that specific decision.

_v4 $arrow$ v4\_r2 ($-$0.13 Dice):_ Expanding evaluation from 5 to 10 images,
including harder object classes (small objects, texture-similar backgrounds,
multiple instances), reduced mean Dice from 0.853 to 0.724. The click count also
decreased slightly (1.4 $arrow$ 1.1), suggesting the VLM stops even earlier on
hard images rather than attempting more corrections. This reveals the primary
remaining failure mode: the VLM's early-stop criterion is calibrated for
visually clear, well-separated objects and may be overconfident on harder cases.

Across the six iterations, there is no monotone
relationship between click count and Dice. Version v4 achieves the highest Dice
(0.853) with the fewest clicks (1.4), while v3 achieves modest Dice (0.623) with
the most clicks (9.2). The critical variable is not click quantity but the
_quality of the stop decision_: a system that stops early on a good mask
outperforms one that accumulates additional clicks past peak quality.

Qualitative analysis of v4\_r2 failures identifies three categories. For small objects (less than 5% of image area), the VLM consistently clicks near the correct region but SAM's resolution is insufficient for sub-patch localization, producing low-quality masks that the VLM nevertheless accepts. Objects that share texture with their surroundings---such as camouflaged animals or objects on matching surfaces---cause the VLM to misread the error heatmap, placing positive clicks in background regions. When several instances of the target class are present in the query image, the VLM typically segments only one, stopping before covering all instances because the partial mask already shows high local quality.

== Cross-Architecture Ablation <sec:results_ablation>

Table @tab:ablation presents a controlled comparison of
all three architectural paradigms on the same 15 FSS-1000 validation classes.
V1 uses the best available PPO checkpoint (before collapse); V2 uses the best
GRPO checkpoint (update 389); V3 uses Qwen3-VL-8B-Instruct with v4 prompts,
zero-shot.

#figure(
  table(
    columns: 4,
    table.hline(),
    [*Metric*], [*V1 (RL Policy)*], [*V2 (RL + SubMask)*], [*V3 (VLM)*],
    table.hline(),
    [Mean Dice],             [0.411],       [0.610],       [*0.776*],
    [Mean IoU],              [0.342],       [0.521],       [*0.681*],
    [Stop Success Rate],     [14%],         [32%],         [*67%*],
    [Dice $>= 0.85$],        [4/15 (27%)],  [8/15 (53%)],  [*9/15 (60%)*],
    [Dice $>= 0.90$],        [4/15 (27%)],  [7/15 (47%)],  [*8/15 (53%)*],
    [Mean Clicks],           [8.7],         [6.0],         [*1.3*],
    [Mean Sub-Masks Used],   [N/A],         [1.0],         [1.2],
    table.hline(),
  ),
  caption: [Cross-architecture comparison on 15 FSS-1000 validation classes.
  V1: PolicyTransformer (BC + PPO best checkpoint).
  V2: SubMaskPolicyTransformer (BC + GRPO best checkpoint, update 389).
  V3: Qwen3-VL-8B-Instruct, zero-shot, v4 prompts.],
) <tab:ablation>

V2 improves over V1 by 0.20
Dice (0.610 vs. 0.411) through an additional 10M parameters and a richer action
space. V3 improves over V2 by 0.17 Dice (0.776 vs. 0.610) with zero
task-specific parameters, relying entirely on visual reasoning from VLM
pretraining. The pattern implies a diminishing return from architectural
complexity under the current RL training regime, and a step-change gain from
switching the reasoning modality from implicit (learned weights) to explicit
(chain-of-thought).

V1 and V2 use 8.7 and 6.0 clicks respectively
while achieving lower Dice than V3's 1.3 clicks. The extra clicks in V1 and V2
do not improve quality---they reflect an inability to stop, not an inability to
click accurately. V3's Phase 3 review eliminates this failure mode: every click
is immediately evaluated against a quality threshold, and the agent stops as
soon as that threshold is met. The paradox is that the architectures with the
largest click budgets achieve the worst final Dice, which inverts the usual
assumption that more feedback leads to better results.

V1 has no decomposition capability. V2's trained
policy uses 1.0 sub-masks throughout evaluation---equivalent to V1's
single-mask behavior despite the extended action space. V3 uses a mean of 1.2
sub-masks per episode, initiating decomposition naturally when the single-mask
strategy is visually insufficient. The gap between V2 (1.0 sub-masks) and V3
(1.2 sub-masks) reflects a gap in the ability to _recognize_ when decomposition
is needed, not a gap in the mechanical ability to execute it. V3 discovers the
strategy through explicit visual reasoning; V2 cannot discover it through RL
exploration alone.

== Oracle Sub-Mask Analysis <sec:results_oracle>

To establish an upper bound on the potential benefit of sub-mask
decomposition and to quantify the gap between oracle and trained policies, we
evaluate an oracle sub-mask policy that uses privileged information: it applies
connected component analysis to the pixel-wise error map to identify uncovered
object regions, selects the #smallcaps[new\_submask] action whenever a
disconnected uncovered component exceeds a size threshold, and places the first
click for each new sub-mask at the centroid of that component. This oracle has
access to the ground-truth mask, which the trained agent does not.

Table @tab:oracle_gains reports mean Dice improvement from
oracle decomposition ($Delta$Dice = Dice with decomposition $-$ Dice without)
broken down by object morphology category.

#figure(
  table(
    columns: 4,
    table.hline(),
    [*Object Type*], [*$Delta$Dice (mean $plus.minus$ std)*], [*Fraction Benefiting*], [*Mechanism*],
    table.hline(),
    [Thin/elongated structures], [$0.20 plus.minus 0.04$], [85%], [Multiple disjoint segments needed],
    [Branching objects],         [$0.15 plus.minus 0.05$], [72%], [Each branch requires independent placement],
    [Spatially disconnected],    [$0.25 plus.minus 0.06$], [91%], [Sub-masks cover each disconnected component],
    [Compact/blob objects],      [$0.02 plus.minus 0.03$], [18%], [Single sub-mask captures most of object],
    table.hline(),
  ),
  caption: [Oracle sub-mask decomposition Dice gains by object morphology type
  on FSS-1000. Gains are reported as mean $plus.minus$ standard deviation over
  all instances of each category in the validation split. "No benefit" is
  defined as $|Delta "Dice"| < 0.02$.],
) <tab:oracle_gains>

The oracle triggers decomposition when connected
component analysis of the error map reveals at least one uncovered component
with area exceeding 5% of the image. For thin and branching objects, SAM's
single-mask decoder consistently under-segments the extremities---where object
pixels are spatially far from the click centroid---producing persistent error
components that the oracle resolves by initiating separate sub-masks targeting
each extremity. For blob objects, error components are rare after a well-placed
initial click, which explains the low decomposition benefit (0.02 $Delta$Dice)
in that category.

The largest oracle gains occur on spatially disconnected
objects (0.25 $Delta$Dice). When the target class comprises multiple non-adjacent
instances or parts---as is common in FSS-1000 classes such as "scissors" (two
handles) or "glasses" (two lenses)---SAM's single-mask mode cannot segment both
components from a single click. The oracle initiates one sub-mask per connected
component, achieving near-complete coverage. The trained V2 policy never
discovers this strategy despite 5,000 GRPO updates (@sec:results_grpo).

Averaging oracle gains across all object
types, the oracle policy achieves a mean Dice of $approx 0.72$ on the full
validation split, compared to the trained V2 GRPO policy's 0.54 (best
checkpoint). This 0.18 Dice gap represents the maximum recoverable performance
through improved decomposition strategy discovery, assuming spatial click
placement quality is held constant. The oracle comparison (Figure
@fig:oracle_submask) confirms that the sub-mask decomposition _strategy_ is
correct and rewarding; the V2 training failure is a failure of _discovery_, not
a failure of the strategy itself.

The oracle analysis provides three actionable conclusions for
future work. First, decomposition yields the largest gains on thin, branching,
and disconnected objects---these categories should receive disproportionate
weight in any curriculum designed to train a decomposition policy. Second,
compact blob objects show negligible oracle gain; a practical system should
first classify object morphology before invoking the decomposition mechanism.
Third, the gap between oracle Dice (0.72) and V3 VLM Dice (0.776) suggests that
the VLM's natural decomposition behavior (1.2 sub-masks on average) is already
capturing most of the accessible gain, without requiring explicit connected
component analysis or privileged ground-truth access.
