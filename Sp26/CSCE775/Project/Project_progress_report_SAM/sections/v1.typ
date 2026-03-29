= V1: Single-Mask RL Agent <sec:v1>

The first prototype frames interactive segmentation as a finite-horizon Markov decision process (MDP) in which a learned policy places positive or negative point prompts and decides when to stop. All spatial reasoning is performed at the patch level on a $37 times 37$ grid extracted from a frozen DINOv2-ViT/L backbone. SAM 2 is queried after each click and its mask logits are fed back into the agent's observation.

#figure(
  image("../figures/fig_episode.pdf", width: 100%),
  caption: [Episode structure. The agent places a click, SAM produces a mask, the agent observes the result and decides whether to place another click or stop.],
) <fig:episode>

== State Representation <sec:v1_state>

The agent observes a fixed-length vector derived from five components, all aligned to the $37 times 37 = 1,369$ patch grid produced by the DINOv2-ViT/L encoder at its native stride.

The image to be segmented is encoded once per episode and kept frozen. The result is a tensor of shape $37 times 37 times 1,024$ — one 1,024-dimensional feature vector per patch. These features serve as the primary perceptual representation of the scene.

For each reference example provided at episode start, the foreground patches (those whose centres fall inside the ground-truth mask) are pooled into a single prototype vector of dimension 1,024. When $N_("ref")$ reference examples are available the agent receives a tensor of shape $N_("ref") times 1,024$. In all V1 experiments $N_("ref") = 1$.

After each click, SAM 2 returns a $37 times 37$ grid of raw (pre-sigmoid) mask logits. At the beginning of an episode, before any click has been placed, this channel is initialized to all-zeros. The logits provide direct feedback on how SAM has interpreted the click history, allowing the agent to condition subsequent actions on the current segmentation state.

Two binary maps of shape $37 times 37$ — one for positive clicks, one for negative — record all clicks placed in the current episode. The maps are initialized to zero and updated in-place after each action. They prevent the agent from revisiting already-clicked patches and encode the temporal order of interaction implicitly through the mask logit channel.

A boolean mask of length $1,369$ marks patches that are eligible to receive a new click. A patch is masked invalid if it has already been clicked (of either polarity) in the current episode. Before the location distribution is sampled, its logits are set to $-infinity$ at all invalid positions. This hard constraint eliminates the need for the policy to learn to avoid redundant clicks and removes those positions from the entropy and gradient computation.

Grid indices $(r, c) in {0, dots, 36}^2$ map to pixel coordinates as

$ (x, y) = ((c + 0.5)/(37) dot W, (r + 0.5)/(37) dot H), $ <eq:coord_map>

where $(W, H)$ is the pixel resolution of the query image. SAM 2 accepts these floating-point coordinates directly as point prompts.

== PolicyTransformer Architecture <sec:v1_arch>

The policy is implemented as a custom Transformer encoder with approximately 27 million trainable parameters.

#figure(
  image("../figures/fig_agent.pdf", width: 100%),
  caption: [V1 agent architecture. Frozen DINOv2 and SAM encoders produce features; a trainable Transformer processes all tokens and produces action, location, and value outputs.],
) <fig:agent>

Three lightweight linear projections bring all token types to a common embedding dimension $d_("model") = 1,024$:

$ "query\_proj" &: RR^(1024) -> RR^(1024), \
  "ref\_proj"   &: RR^(1024) -> RR^(1024), \
  "step\_proj"  &: RR^(3)     -> RR^(1024). $

The step projection encodes three scalar features — current step index (normalized), running Dice, and number of clicks used — into the action token prior to attention.

Three token types are concatenated along the sequence dimension before the Transformer encoder. First, #smallcaps[[Query]] tokens: each of the $1,369$ patches contributes one token, formed by concatenating the DINOv2 feature vector with the SAM logit, the positive-click indicator, and the negative-click indicator for that patch, then passing through `query_proj`. Second, #smallcaps[[Ref]] tokens: one token per reference example, obtained by projecting the foreground prototype through `ref_proj`. Third, the #smallcaps[[Action]] token: a single special token initialized from the step features via `step_proj`, whose final-layer output embedding is consumed by all three output heads.

The full input sequence has length $1,369 + N_("ref") + 1 = 1,371$ for the V1 single-reference setting.

The encoder consists of 4 standard Transformer layers, each with 8 attention heads, $d_("model") = 1,024$, and a feed-forward dimension of 2,048. Pre-layer normalization (`LayerNorm` before each sublayer) is used throughout. No positional encoding is added to the #smallcaps[[Query]] tokens; spatial structure is implicitly carried by the DINOv2 features.

All three heads consume the final-layer embedding of the #smallcaps[[Action]] token $bold(e)_("act") in RR^(1,024)$. The action-type head applies a linear layer $RR^(1,024) -> RR^3$ followed by softmax to produce the distribution $pi_alpha (dot | s)$ over {#smallcaps[pos-click], #smallcaps[neg-click], #smallcaps[stop]}. The location head computes scores as a dot product between the action token embedding and each #smallcaps[[Query]] token's final-layer embedding,
$ ell_i = bold(e)_("act")^top bold(e)_("query", i), quad i = 1, dots, 1,369; $
after masking invalid positions to $-infinity$, a softmax over the remaining $ell_i$ yields $pi_ell (dot | s)$. The value head applies a two-layer MLP $(RR^(1,024) -> RR^(256) -> RR^1)$ with a ReLU nonlinearity to produce a scalar state-value estimate $V(s)$.

#figure(
  table(
    columns: 3,
    table.hline(),
    [Component], [Shape], [Parameters],
    table.hline(),
    [`query_proj` (weight + bias)], [$1,024 times 1,024$ + $1,024$], [1,049,600],
    [`ref_proj` (weight + bias)],   [$1,024 times 1,024$ + $1,024$], [1,049,600],
    [`step_proj` (weight + bias)],  [$3 times 1,024$ + $1,024$],     [4,096],
    [Transformer encoder (4 layers)], [---],                          [25,178,112],
    [Action-type head],             [$1,024 times 3$ + $3$],          [3,075],
    [Value MLP],                    [$1,024 times 256 + 256 times 1$],[262,400],
    table.hline(),
    [*Total*], [], [*27,546,883*],
    table.hline(),
  ),
  caption: [Parameter breakdown for the V1 PolicyTransformer ($approx$27M total).],
) <tab:v1_params>

== Reward Design <sec:v1_reward>

The reward function is designed to encourage efficient convergence to a high-quality mask while penalizing excessive interaction.

#figure(
  image("../figures/fig_reward.pdf", width: 55%),
  caption: [Reward structure. Dense per-step rewards measure actual mask improvement; terminal rewards incentivize learning when to stop.],
) <fig:reward>

At each non-terminal step $t$ the agent receives

$ r_t = Delta"Dice"_t - c_("click"), $ <eq:per_step_reward>

where $Delta"Dice"_t = "Dice"(m_t, m^*) - "Dice"(m_(t-1), m^*)$ is the improvement in Dice coefficient produced by the click, $m^*$ is the ground-truth mask, and $c_("click") = 0.01$ is a small per-click cost that discourages unnecessary interaction.

When the agent issues a STOP action the episode ends and an additional terminal reward is applied:

$ r_("term") = cases(+0.20 & "if" "Dice"(m_T, m^*) >= tau, -0.20 & "otherwise,") $ <eq:terminal_reward>

where $tau = 0.85$ is the success threshold. The asymmetric bonus/penalty creates a strong incentive to stop only when the segmentation quality is sufficient.

The click budget is capped at 10 clicks per episode. If the budget is exhausted before the agent issues STOP, the episode is marked as _truncated_: no terminal reward is applied, and the value head is queried at the final state to produce a bootstrap return for advantage estimation (see @sec:v1_ppo).

== Oracle Data Generation <sec:v1_oracle>

Behavioral cloning requires a corpus of near-optimal click trajectories. Because no human annotations of click sequences exist, oracle trajectories are generated automatically by brute-force search.

For each image, the oracle proceeds greedily: at each step it evaluates SAM 2's mask output for all $1,369$ candidate positive-click positions and all $1,369$ candidate negative-click positions. The $(2 times 1,369)$ forward passes are batched to amortize GPU overhead. The position and polarity yielding the largest Dice improvement are selected as the oracle action for that step.

The oracle terminates the episode under any of the following conditions: the current Dice reaches or exceeds 0.95; Dice fails to improve by more than $10^(-3)$ in two consecutive steps (plateau detection); or the click budget of 10 is exhausted.

DINOv2-ViT/L features are computed once per image and cached to disk before oracle generation begins. This eliminates redundant backbone passes: each image incurs exactly one DINOv2 forward pass regardless of how many oracle trajectories reference it. SAM 2 is not cached because its output depends on the evolving click history.

Oracle generation was run on the training split of the target dataset. The resulting corpus contains one trajectory per image, with a mean episode length of 4.3 clicks and a mean terminal Dice of 0.91.

== Behavioral Cloning <sec:v1_bc>

Behavioral cloning (BC) warm-starts the policy before RL fine-tuning, providing an initialization that already performs sensible clicking and substantially reduces the exploration burden on PPO.

Each oracle trajectory of length $T$ contributes $T + 1$ labeled samples to the `OracleStepDataset`: one sample per click step (label = oracle action and oracle location) plus one sample for the terminal STOP step (label = STOP, location = centre patch by convention). All observation tensors — query features, reference features, SAM logits, click maps, step scalars — are stored as half-precision floats to keep the dataset in RAM.

The BC loss is a sum of two cross-entropy terms:

$ cal(L)_("BC") = cal(L)_("CE")(hat(pi)_alpha, alpha^*) + cal(L)_("CE")(hat(pi)_ell, ell^*), $ <eq:bc_loss>

where $alpha^*$ and $ell^*$ are the oracle action type and location, and $hat(pi)_alpha$, $hat(pi)_ell$ are the model's predicted distributions. The value head is not trained during BC.

The model is trained with AdamW at a learning rate of $3 times 10^(-4)$, weight decay $10^(-2)$, and a cosine annealing schedule over 50 epochs. The batch size is 128.

#figure(
  image("../figures/fig_warmstart_curves.pdf", width: 100%),
  caption: [Behavioral cloning warmstart training curves. *Top:* action loss (left axis) and location loss (right axis) both decrease steadily. *Bottom:* action accuracy converges to 91%; location top-5 accuracy reaches 75%.],
) <fig:warmstart>

After 50 epochs the BC checkpoint achieves an action-type accuracy of 91% on the held-out validation split, a location top-5 accuracy of 75% (meaning the oracle location falls within the top-5 predicted positions), and a mean episode Dice of 0.549, evaluated by rolling out the policy with greedy decoding on 500 validation images.

The Dice of 0.549 is below the oracle mean (0.91) because greedy decoding compounds small deviations from the oracle, but it represents a reasonable warm-start for RL.

== PPO Fine-Tuning <sec:v1_ppo>

PPO fine-tuning begins from the behavioral cloning checkpoint described in Section 6.5. The learning rate is initialized at $3 times 10^(-4)$, warmed up linearly over 500 steps, and then decayed linearly to a floor of $3 times 10^(-5)$ over the remaining 4,500 updates. The PPO clipping parameter is $epsilon = 0.2$ — the standard value from @schulman2017ppo. The value coefficient is $0.5$ and the entropy bonus coefficients are $0.01$ for both the action-type head and the location head. Gradients are clipped to a maximum $ell_2$ norm of $0.5$. Generalized advantage estimation (GAE) uses $gamma = 0.99$ and $lambda = 0.95$. Each collected batch of rollouts is replayed for 2 optimization epochs with a minibatch size of 16. Training runs for 5,000 total policy updates.

The agent selects a composite action $a = (alpha, ell)$, where $alpha$ is the action type (positive click, negative click, or stop) and $ell$ is a spatial location on the $37 times 37$ patch grid. The two components are treated as conditionally independent given the state, so the joint log-probability factorizes as

$ log pi(a, ell | s) = log pi_alpha (alpha | s) + log pi_ell (ell | s). $ <eq:joint_logprob>

$pi_alpha$ is a 3-way softmax over the action logits produced by the #smallcaps[[Action]] token. $pi_ell$ is a 1,369-way softmax over location scores obtained by taking the dot product between the #smallcaps[[Action]] token embedding and all 1,369 #smallcaps[[Query]] token embeddings — a lightweight attention mechanism that scores each patch relative to the agent's current decision context. The probability ratio used in the clipped surrogate objective is computed from the joint log-probability in @eq:joint_logprob.

Training is fully on-policy: at each update, fresh trajectories are collected under the current policy with SAM queried in the loop after every click. Each click updates SAM's mask logits, and the agent observes the new logits before selecting the next action. Episodes terminate either when the agent selects STOP or when the click budget is exhausted at 10 clicks. If the budget is exhausted before STOP, the episode is marked as _truncated_ rather than _terminal_; the final state is passed through the value head to produce a bootstrap estimate $V(s_T)$, and advantage accumulation is seeded from that estimate rather than from zero.

Advantages are computed with standard backwards-pass GAE. For a terminal episode (done $= #text("True")$, truncated $= #text("False")$), the accumulator resets to zero at the episode boundary. For a truncated episode (done $= #text("True")$, truncated $= #text("True")$), the accumulator is seeded with the bootstrapped value $V(s_T)$, correctly crediting the agent for future returns that were cut off by the click cap. After all advantages are computed, they are normalized across the minibatch:

$ hat(A)_t <- (hat(A)_t - mu_(hat(A))) / (sigma_(hat(A)) + 10^(-8)), $

where $mu_(hat(A))$ and $sigma_(hat(A))$ are the mean and standard deviation over the current minibatch.

Each collected batch is replayed for 2 epochs using minibatches of size 16. The policy loss is the PPO clipped surrogate,

$ L_("policy") = -EE_t [min(r_t hat(A)_t, op("clip")(r_t, 1 - epsilon, 1 + epsilon) hat(A)_t)], $ <eq:ppo_clip>

where $r_t = pi_theta (a_t | s_t) \/ pi_(theta_("old"))(a_t | s_t)$ is the probability ratio evaluated using the joint log-probability from @eq:joint_logprob. The value loss is a clipped mean-squared error between the value head's predictions and the empirical returns, following the implementation detail recommended by @engstrom2020implementation. The entropy bonus is applied separately to the action-type distribution $H_alpha$ and the location distribution $H_ell$. The total loss is

$ L_("total") = L_("policy") + 0.5 dot L_("value") - 0.01 dot H_alpha - 0.01 dot H_ell. $ <eq:ppo_total>

All three heads (action type, location, value) share the same #smallcaps[[Action]] token representation and are updated jointly at each step.

== Catastrophic Collapse Analysis <sec:v1_collapse>

#figure(
  image("../figures/fig_ppo_eval.pdf", width: 100%),
  caption: [V1 PPO evaluation. Dice peaks at 0.49 (update 29), then collapses catastrophically. The agent maxes out clicks (right axis) without learning to stop.],
) <fig:ppo_eval>

Updates 0–19 show modest improvement from the BC initialization (Dice $= 0.549$) toward a peak of $0.49$. This brief improvement indicates that the RL objective successfully extracts easy gains from the warmstart initialization. Between updates 19 and 29 the policy holds near its peak, then from update 30 onward Dice falls rapidly below $0.20$. After update 100 the policy never recovers; evaluation Dice stabilizes in the $0.15$–$0.20$ range for all remaining updates.

The most visible behavioral symptom is that the agent learns to consume the entire 10-click budget on every episode. Rather than discovering the stopping rule, the policy collapses onto a degenerate strategy of placing clicks until forced to terminate. This is consistent with the reward structure: the per-step click cost of $-0.01$ is too small relative to the incremental Dice gains from early clicks to make stopping attractive. The terminal stop bonus of $+0.20$ requires the agent to discover that stopping _early_ yields higher cumulative reward than continuing — but by the time the policy would need to make this inference, the next symptom has already degraded the learning signal.

The action-type entropy $H_alpha$ drops from approximately $1.08$ nats (near uniform over 3 actions) to near zero within the collapse window. Once entropy collapses, the policy becomes nearly deterministic: it samples the same action type at every state, which in practice means either always clicking positive or always clicking negative. The entropy bonus ($0.01 dot H_alpha$) is insufficient to prevent this collapse because by update 30 the gradient signal from the clipped surrogate is already overwhelmingly pointing the action-type distribution toward one corner of the simplex. With zero entropy there is no mechanism for the policy to recover exploratory behavior, making the collapse irreversible.

PPO relies on the value head to produce low-variance advantage estimates through GAE. As the policy degrades, the return distribution shifts rapidly; the value head — trained alongside the policy in a shared representation — cannot track this distribution shift quickly enough. Uncalibrated value estimates produce advantage signals of the wrong sign, which in turn push the policy further from any local optimum. This creates a feedback loop: policy degradation corrupts value estimates, corrupted value estimates produce incorrect advantages, and incorrect advantages further degrade the policy.

Location quality degrades as a downstream consequence of the action-head collapse. Because the joint log-probability in @eq:joint_logprob couples the location gradient to the action-type gradient, the collapse of $pi_alpha$ propagates into the location head. Click placements become spatially incoherent — the policy places clicks on semantically irrelevant patches — which produces low or negative $Delta"Dice"$ rewards, further reinforcing the collapsing action type and completing the degradation cycle.

The collapse pattern has two interacting root causes. First, _trust region drift_: PPO's clipped objective confines each update to a small probability-ratio neighborhood, but it does not prevent the policy from drifting in a pathological direction across successive updates. The trust region guarantees local stability per update, not global stability across thousands of updates @engstrom2020implementation. Second, _reward imbalance_: the click cost ($-0.01$) is calibrated to discourage excessive clicking, but the terminal stop bonus ($+0.20$) requires the agent to first discover that early stopping is beneficial. In a sparse-feedback environment where the agent only receives the terminal reward at episode end, this discovery requires the policy to maintain sufficient entropy for long enough to sample early-stop trajectories — but entropy collapses before the agent can make this discovery. The two causes reinforce each other: reward imbalance provides the initial direction of drift, and trust region drift ensures the policy travels far enough in that direction to make recovery impossible.

Multiple remediation attempts were made before concluding that the collapse is structural rather than a tuning artifact. Interventions included: varying the learning rate over two orders of magnitude, increasing and decreasing the entropy coefficient, scaling the first-click reward to provide a denser signal early in training, and staged training (phase 1 optimizing only the first click, phase 2 adding correction clicks). None of these interventions prevented eventual collapse; they changed only the update at which collapse began, not whether it occurred. This robustness of the failure mode across hyperparameter configurations is consistent with the broader literature on PPO instabilities in environments with sparse terminal rewards @engstrom2020implementation.

The collapse analysis identifies the value head as the weakest structural link in the V1 system: it is responsible for advantage estimation, it is coupled to the policy representation, and it fails under rapid distribution shift. This observation directly motivates the V2 GRPO approach (@sec:v2_grpo), which eliminates the value head entirely. GRPO estimates advantages from a group of $k$ on-policy rollouts per image, replacing the learned baseline with a sample-based baseline that cannot diverge. While GRPO does not solve the exploration problem — the V2 policy never discovers the sub-mask decomposition strategy — it does eliminate the value-divergence feedback loop and produces stable, non-collapsing training curves.

== Development Timeline

#figure(
  table(
    columns: (5.5em, 1fr),
    table.hline(),
    [*Date*], [*Milestone*],
    table.hline(),
    [Mar 3], [Q-learning abandoned; clean-slate redesign of agent architecture begins.],
    [Mar 4], [V1 scaffold implemented: PolicyTransformer, InteractiveSAMEnv, PPO/BC trainers, evaluation loop, and smoke tests.],
    [Mar 4], [Real DINOv2 and SAM backends integrated with mock fallback; GPU guard and HDD overflow routing added.],
    [Mar 4], [First PPO fine-tuning run with 20-image, 8-rollout configuration. Staged first-click and correction training modes created.],
    [Mar 4], [Hyperparameter sweep: learning rate, entropy coefficient, first-click reward scaling, phase1/phase2 configs.],
    [Mar 9], [Soft-target BC bootstrap, demo-augmented PPO (R6), real-data smoke runners (R5, R5b, R8) with oracle-assisted stop labels.],
    [Mar 10], [Brute-force oracle click generator implemented with batched SAM inference and debug visual panels. Autoclaim mode for parallel runs.],
    [Mar 12], [DINOv2 token precomputation cache and SAM segmentation scripts finalized. Warmstart training converges at 91% action accuracy.],
    table.hline(),
  ),
  caption: [V1 development timeline (March 3--12, 2026).],
) <tab:v1_timeline>
