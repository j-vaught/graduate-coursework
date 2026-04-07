// Color definitions
#let garnet = rgb("#73000A")
#let horseshoe = rgb("#65780B")
#let rose = rgb("#CC2E40")
#let lightgray10 = rgb("#ECECEC")
#let atlantic = rgb("#466A9F")

// Page and text settings
#set page(margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(first-line-indent: 0pt, justify: true)
#set block(spacing: 0.5em)
#set heading(numbering: "1.1.1")
#set math.equation(numbering: "(1)")
#show figure: it => { v(1em); it }

// Make sections start on new pages
#show heading.where(level: 1): it => {
  pagebreak()
  text(size: 14pt, weight: "bold")[#it]
}
#show heading.where(level: 2): it => {
  text(size: 12pt, weight: "bold")[#it]
}
#show heading.where(level: 3): it => {
  text(size: 12pt, style: "italic")[#it]
}

// Links colored blue
#show link: set text(fill: blue)
#show ref: set text(fill: blue)

// Title block
#align(center)[
  #text(size: 16pt, weight: "bold")[A Comprehensive Survey of Reinforcement Learning Methods for Large Language Model Alignment]
  #v(0pt)
  Authored by JC Vaught
]

= Introduction

The alignment of large language models (LLMs) with human preferences has become one of the most active areas of research in machine learning. Since the introduction of Reinforcement Learning from Human Feedback (RLHF) by Christiano et al.~@Christiano2017RLHF and its successful application in InstructGPT~@Ouyang2022InstructGPT, the field has produced a rapidly growing family of alignment algorithms. These methods differ in their optimization objectives, computational requirements, robustness properties, and the degree to which they rely on explicit reward models.

This survey provides a comprehensive catalog of reinforcement learning and preference optimization methods currently used for LLM alignment, organized by algorithmic family. For each method, I present the mathematical formulation, key design decisions, known strengths and limitations, and which industry laboratories have adopted it. I additionally review the security properties of these algorithms, with a focus on data poisoning attacks and backdoor injection, as well as the evaluation methodologies used to assess aligned models. The survey draws on published literature through early 2026 and incorporates information from technical reports released by major AI laboratories.

The scope encompasses four broad families of methods. _Policy gradient methods_ such as PPO~@Schulman2017PPO, GRPO~@Shao2024DeepSeekMath, and REINFORCE++~@Hu2025Reinforce optimize a language model policy against a learned or verifiable reward signal using gradient-based reinforcement learning. _Direct preference optimization methods_ such as DPO~@Rafailov2023DPO, IPO~@Azar2024IPO, KTO~@Ethayarajh2024KTO, ORPO~@Hong2024ORPO, and SimPO~@Meng2024SimPO bypass the reward model entirely and learn directly from preference pairs in a supervised fashion. _Rejection sampling methods_ generate multiple candidate responses and fine-tune on the best ones as scored by a reward model~@Touvron2023Llama2 @Dong2023RAFT. Finally, _AI feedback methods_ replace human annotations with model-generated evaluations, including RLAIF~@Lee2023RLAIF, Constitutional AI~@Bai2022Constitutional, and Reinforcement Learning from Verifiable Rewards (RLVR)~@Lambert2024Tulu3.


= How Large Language Models Are Trained

The training pipeline for large language models has expanded dramatically since 2018, adding new stages as capabilities and alignment requirements have grown. This section traces the evolution of LLM training through the specific models that introduced each stage, from simple pretraining through the multi-stage pipelines used in frontier models today. @tab:pipeline_evolution provides a summary of which models introduced which stages.

== Stage 1: Pretraining

Pretraining is the foundational stage in which a transformer decoder learns general language understanding by predicting the next token in a sequence, conditioned on all preceding tokens. Given a corpus of text sequences, the model minimizes the cross-entropy loss $cal(L)_"PT" = - sum_t log p_theta (x_t | x_(< t))$ over billions of tokens drawn from books, web pages, code, and other sources. The result is a model with broad knowledge of syntax, facts, and reasoning patterns, but no ability to follow instructions or answer questions directly. As @fig:stage1_pretraining illustrates, a pretrained model responds to a prompt like "Summarize this article" by continuing the text rather than producing a summary. Pretraining is also susceptible to data quality failures. Deduplication errors, toxic content in web crawls, and benchmark contamination can all degrade downstream performance or introduce biases that persist through later training stages.

_GPT-1_ (Radford et al., OpenAI, June 2018) was the first model to apply autoregressive generative pretraining to the transformer decoder architecture, training a 117M-parameter model on BookCorpus. _GPT-2_ (February 2019) scaled this to 1.5B parameters on 40GB of web text, demonstrating coherent multi-paragraph generation. _GPT-3_~@Brown2020GPT3 (May 2020) scaled to 175B parameters on 300B tokens, showing that pretraining alone could enable strong few-shot in-context learning with no fine-tuning whatsoever. GPT-3's training pipeline consisted of a single autoregressive pretraining stage. No post-training of any kind was applied.

Modern pretraining has grown substantially in scale. DeepSeek-V3 (December 2024) pretrained a 671B-parameter MoE model on 14.8 trillion tokens. Llama 3.1~@Touvron2023Llama2 (July 2024) pretrained a 405B dense model on 15.6 trillion tokens using 39.3 million H100 GPU hours. Llama 4 (April 2025) pretrained on over 30 trillion tokens across 200+ languages with native multimodal (text + vision) data from the start.

#figure(
  image("figures/fig_stage1.pdf", width: 100%),
  caption: [The pretraining stage.],
) <fig:stage1_pretraining>

== Stage 2: Supervised Fine-Tuning (SFT)

SFT trains the pretrained model on curated instruction-response pairs, teaching it to follow instructions rather than merely complete text. _Natural Instructions_ (Mishra et al., April 2021) was the first paper to benchmark cross-task generalization from natural language instructions. _FLAN_ (Wei et al., Google, September 2021) was the first to demonstrate instruction tuning at scale, fine-tuning a 137B model on 60+ NLP tasks verbalized as instructions.

#figure(
  caption: [Example instruction-response pairs used in supervised fine-tuning.],
  table(
    columns: (0.38fr, 1fr),
    stroke: none,
    table.hline(stroke: 1.5pt),
    table.header(
      [*Instruction*], [*Response*],
    ),
    table.hline(stroke: 0.75pt),
    [What causes ocean tides?],
    [Ocean tides are primarily caused by the gravitational pull of the Moon... producing two high tides per day.],
    [],
    [],
    [Summarize the following passage: "The industrial revolution began in Britain..."],
    [The industrial revolution originated in late 18th-century Britain, shifting manufacturing from manual methods to mechanized production.],
    table.hline(stroke: 1.5pt),
  ),
) <tab:sft_examples>

_InstructGPT_~@Ouyang2022InstructGPT (March 2022) integrated SFT as the first stage of a multi-stage alignment pipeline. Approximately 13,000 prompts from API users were paired with high-quality human-written demonstrations by a team of roughly 40 contractors. The key finding was that a 1.3B InstructGPT model fine-tuned with SFT and RLHF was preferred by humans over the 175B GPT-3 base model.

The scale of SFT data has evolved considerably. Llama 2~@Touvron2023Llama2 (July 2023) used 27,540 high-quality annotations, emphasizing quality over quantity. Llama 3 (2024) scaled to over 25 million synthetically generated examples across six iterative rounds of post-training.

#figure(
  image("figures/fig_stage2.pdf", width: 100%),
  caption: [Stage 2: Supervised Fine-Tuning. The resulting SFT model can follow instructions, summarize text, and answer questions directly.],
) <fig:stage2_sft>

== Stage 3: Reward Model Training

A reward model $r_phi (x, y)$ is trained on human preference data to predict which of two model responses a human would prefer, optimized under the Bradley-Terry preference model.

$ cal(L)_"RM" (phi) = -EE_((x, y_w, y_l) tilde.op cal(D)) [log sigma(r_phi (x, y_w) - r_phi (x, y_l))] $ <eq:rm_loss>

_Ziegler et al._ (OpenAI, September 2019) were the first to train a reward model on human preference comparisons between LLM outputs, applying RLHF to GPT-2 for stylistic text continuation. _Stiennon et al._~@Stiennon2020Summarize (September 2020) scaled this for summarization. InstructGPT trained a 6B reward model on approximately 33,000 human-ranked comparison sets and found this single RM worked well for all policy sizes (1.3B to 175B).

Llama 2 introduced _dual reward models_, training separate helpfulness and safety RMs on over 1 million human preference annotations. Gemini 2.5 uses multi-objective reward models with weighted scores for helpfulness, factuality, and safety. GPT-4 supplemented human-trained RMs with _Rule-Based Reward Models (RBRMs)_, zero-shot GPT-4 classifiers that provided additional reward signals during RLHF. DeepSeek-R1~@Guo2025DeepSeekR1 uses rule-based verifiable rewards (math/code correctness) rather than learned reward models for reasoning tasks.

#figure(
  image("figures/fig_stage3.pdf", width: 100%),
  caption: [Stage 3: Reward Model Training. The reward model learns to score responses by quality, assigning higher values to preferred outputs.],
) <fig:stage3_rm>

== Stage 4: Reinforcement Learning

The SFT model is optimized to maximize the reward model's output while staying close to the reference policy via a KL penalty.

$ max_(pi_theta) EE_(x tilde.op cal(D), y tilde.op pi_theta (dot|x)) [r_phi (x, y) - beta D_"KL" [pi_theta (dot|x) parallel pi_"ref" (dot|x)]] $ <eq:rlhf_objective>

_Ziegler et al._ (September 2019) were the first to apply PPO-based RL to a language model. InstructGPT (2022) formalized this as Stage 3 of the RLHF pipeline, training with PPO on approximately 31,000 prompts. This remained the dominant approach through GPT-4 (2023) and early Claude models.

Llama 2 (2023) introduced _iterative RLHF_, running five successive rounds where new human preference data was collected at each iteration using the latest model checkpoint. Llama 3 (2024) replaced PPO with DPO~@Rafailov2023DPO (introduced by Rafailov et al. in May 2023) for preference optimization, finding DPO required less compute for large models. Llama 4 (2025) shifted to online RL as the primary alignment stage, using lightweight SFT and lightweight DPO as bookends.

== Stage 5: Constitutional AI and AI Feedback

_Constitutional AI_~@Bai2022Constitutional (Anthropic, December 2022) introduced two innovations. First, the model critiques and revises its own outputs against a set of constitutional principles (SL-CAI). Second, AI-generated preference labels replace human labels for harmlessness evaluation (RL-CAI / RLAIF). This was first used for Claude 1 (2023) and remains the foundation of Claude 3/3.5 (2024) alignment. The approach used 182,831 AI-generated harmlessness comparisons combined with 135,296 human helpfulness comparisons.

== Stage 6: Rejection Sampling

Rejection sampling generates $N$ candidate responses per prompt, scores them with a reward model, and fine-tunes on the best ones. _Stiennon et al._~@Stiennon2020Summarize (2020) first used best-of-N as a baseline. _WebGPT_ (Nakano et al., OpenAI, December 2021) combined imitation learning with rejection sampling for web-browsing QA. _Llama 2_~@Touvron2023Llama2 (July 2023) elevated rejection sampling to a primary alignment strategy, using it exclusively for later RLHF iterations on the 70B model. This is the first model where rejection sampling was a core training stage rather than a baseline.

== Stage 7: Chain-of-Thought Training

While Wei et al. (January 2022) introduced chain-of-thought as a prompting technique, _STaR_ (Zelikman et al., March 2022) was the first to use CoT as a training signal, generating rationales, filtering for correct answers, and fine-tuning on successful reasoning traces.

_OpenAI o1_ (September 2024) was the first production model to demonstrate extended reasoning trained via large-scale RL, using "thinking tokens" as a scratchpad, though no technical details were published. _DeepSeek-R1_~@Guo2025DeepSeekR1 (January 2025) was the first to publish the full methodology: R1-Zero demonstrated that pure GRPO from a base model (no SFT) can produce emergent self-reflection, verification, and dynamic strategy adaptation. The full R1 pipeline uses cold-start SFT on long-CoT traces followed by GRPO with verifiable rewards (800K completions: 600K reasoning + 200K general).

_Kimi K1.5_~@Kimi2025K15 (January 2025) introduced a four-stage reasoning pipeline: pretraining $arrow.r$ vanilla SFT ($tilde$1M examples) $arrow.r$ long-CoT SFT (verified reasoning paths) $arrow.r$ RL via online mirror descent. They introduced Long2Short methods where the shortest correct solutions are selected as positive samples and longer responses as negatives for DPO training.

== Stage 8: Tool Use Training

_WebGPT_ (Nakano et al., OpenAI, December 2021) was the first LLM trained to use tools (a web browser) via imitation learning on human demonstrations plus rejection sampling. _Toolformer_ (Schick et al., Meta, February 2023) was the first fully self-supervised tool use training, where the model taught itself when and how to call external APIs. Llama 3 (2024) included specific training for search engine, code interpreter, and mathematical computation tools.

_Grok 4_ (xAI, 2025) was trained end-to-end with tool-use RL, meaning browsing and search were part of the RL action space, not a separate capability. _Kimi K2.5_~@Kimi2025Researcher (February 2026) introduced Parallel Agent RL (PARL), training an orchestrator to direct up to 100 sub-agents across 1,500 coordinated steps.

== Stage 9: Multi-Stage RL Pipelines (2025--2026)

The most recent frontier models use sequential RL stages targeting different capabilities.

_Qwen3_~@Qwen2025Qwen3 (2025) follows a four-stage post-training pipeline: long-CoT cold start $arrow.r$ GRPO/GSPO with format and accuracy rewards $arrow.r$ rejection sampling $arrow.r$ general RL for alignment.

_GLM-5_~@GLM2025GLM5 (Z.ai, February 2026) uses sequential Reasoning RL $arrow.r$ Agentic RL $arrow.r$ General RL, with on-policy cross-stage distillation to prevent catastrophic forgetting. Their Slime infrastructure uses Active Partial Rollouts (APRIL) to address the generation bottlenecks that consume over 90% of RL training time, improving rollout throughput by up to 44%.

_MiniMax-M1_~@MiniMax2025M1 (June 2025) uses cold-start SFT followed by large-scale CISPO (their proprietary RL algorithm) across math, logic (53K synthesized problems), competitive programming, and software engineering sandboxes, with 40K--80K thinking budgets. _MiniMax-M2.5_~@MiniMax2025Forge (February 2026) extends this with the Forge framework for unified mixed-domain agent RL across 200,000+ real-world environments, achieving approximately 40x training speedup through asynchronous scheduling.

== Stage 10: Distillation

_DistilBERT_ (Sanh et al., October 2019) was the first to apply knowledge distillation during LM pretraining. For alignment specifically, _Llama 4_ (2025) introduced codistillation from the 2-trillion-parameter Behemoth teacher during pretraining of Scout and Maverick, using a novel loss that dynamically weights soft and hard targets. DeepSeek-R1 distilled 800K reasoning samples into six smaller models (1.5B--70B) using SFT alone (no RL stage needed for distilled models).

== Summary of Pipeline Evolution

#figure(
  caption: [Evolution of LLM training pipelines through specific models. Each row shows which training stages were used. Boldface indicates the first model to introduce that stage.],
  table(
    columns: (2.8cm, auto, auto, auto, auto, auto, auto, auto),
    stroke: none,
    table.hline(stroke: 1.5pt),
    table.header(
      [*Model (Year)*], [*PT*], [*SFT*], [*RM*], [*RL*], [*RS*], [*CoT-RL*], [*Tool RL*],
    ),
    table.hline(stroke: 0.75pt),
    [GPT-3 (2020)], [$bullet$], [], [], [], [], [], [],
    [InstructGPT (2022)], [$bullet$], [$bullet$], [$bullet$], [*PPO*], [], [], [],
    [Claude 1 (2023)], [$bullet$], [$bullet$], [RLAIF], [RL-CAI], [], [], [],
    [Llama 2 (2023)], [$bullet$], [$bullet$], [2 RMs], [PPO], [$bullet$], [], [],
    [GPT-4 (2023)], [$bullet$], [$bullet$], [RM+RBRM], [PPO], [], [], [],
    [Llama 3 (2024)], [$bullet$], [$bullet$], [$bullet$], [DPO], [$bullet$], [], [],
    [DeepSeek-R1 (2025)], [$bullet$], [cold], [rule], [*GRPO*], [$bullet$], [$bullet$], [],
    [Kimi K1.5 (2025)], [$bullet$], [$bullet$], [$bullet$], [OMD], [], [$bullet$], [],
    [Llama 4 (2025)], [$bullet$], [light], [implicit], [online RL], [], [], [],
    [Qwen3 (2025)], [$bullet$], [$bullet$], [$bullet$], [GSPO], [$bullet$], [$bullet$], [],
    [GLM-5 (2026)], [$bullet$], [$bullet$], [$bullet$], [seq. RL], [], [$bullet$], [$bullet$],
    [MiniMax-M2.5 (2026)], [$bullet$], [$bullet$], [process], [CISPO], [], [$bullet$], [$bullet$],
    table.hline(stroke: 1.5pt),
  ),
) <tab:pipeline_evolution>

#text(size: 9pt)[PT = Pretraining; SFT = Supervised Fine-Tuning; RM = Reward Model; RL = Reinforcement Learning; RS = Rejection Sampling; CoT-RL = Chain-of-Thought RL; Tool RL = Tool/Agent RL. OMD = Online Mirror Descent.]

The trend is clear: the number of post-training stages has grown from zero (GPT-3) to one (InstructGPT's SFT+RM+PPO counted as a single "RLHF" pipeline) to five or more sequential stages in frontier 2026 models. The most capable open-source models (GLM-5, MiniMax-M2.5, Qwen3) now use multi-phase RL pipelines where different RL stages target different capabilities (reasoning, agentic behavior, general alignment), connected by distillation to prevent forgetting. The specific RL algorithm used at each stage (PPO, GRPO, CISPO, DPO, etc.) has become less important than the overall pipeline architecture and the quality of reward signals.


= Policy Gradient Methods

Policy gradient methods directly optimize the language model policy $pi_theta$ using gradient estimates derived from sampled trajectories (generated text sequences) and their associated rewards. These methods differ primarily in how they estimate the _advantage_ $hat(A)$, which measures how much better a particular action (token generation) is compared to the expected value under the current policy.

== Proximal Policy Optimization (PPO)

PPO~@Schulman2017PPO is the original algorithm used in InstructGPT~@Ouyang2022InstructGPT for the policy optimization stage of RLHF. It remains the most thoroughly studied alignment algorithm and the baseline against which newer methods are evaluated.

=== Architecture

PPO requires four models in memory simultaneously during training. The _policy model_ $pi_theta$ is the language model being optimized. The _reference model_ $pi_"ref"$ is a frozen copy of the SFT model, used to compute the KL penalty. The _reward model_ $r_phi$ scores generated responses. The _critic (value) model_ $V_psi (s)$ estimates the expected return from each state $s$ and is used to compute advantage estimates.

=== Advantage Estimation

PPO uses Generalized Advantage Estimation (GAE) to compute advantages. The temporal difference (TD) residual at token position $t$ is

$ delta_t = r_t + gamma V_psi (s_(t+1)) - V_psi (s_t) $

where $r_t$ is the reward at step $t$ (typically zero except at the final token, where the reward model score is applied) and $gamma$ is the discount factor. The GAE advantage is

$ hat(A)_t^("GAE"(gamma, lambda)) = sum_(k=0)^(T-t-1) (gamma lambda)^k delta_(t+k) $

where $lambda in [0,1]$ controls the bias-variance tradeoff. Typical values for RLHF are $lambda = 0.95$ and $gamma approx 1.0$.

=== Clipped Surrogate Objective

The policy is updated by maximizing a clipped surrogate objective that prevents excessively large policy updates.

$ cal(L)_"PPO" (theta) = EE_t [min(frac(pi_theta (a_t | s_t), pi_(theta_"old") (a_t | s_t)) hat(A)_t, "clip"(frac(pi_theta (a_t | s_t), pi_(theta_"old") (a_t | s_t)), 1-epsilon, 1+epsilon) hat(A)_t)] $

The clipping parameter $epsilon$ (typically 0.2) ensures that the probability ratio $pi_theta \/ pi_(theta_"old")$ does not deviate too far from 1.0, producing conservative policy updates. The combined PPO loss also includes a value function loss $cal(L)_"VF"$ and an entropy bonus $cal(L)_"ent"$ that encourages exploration.

=== Adoption

PPO was the primary alignment algorithm used by OpenAI for ChatGPT and GPT-4, by Anthropic in earlier versions of their models, and remains widely used in RLHF research. Its main drawback is computational cost, as maintaining four models in memory and performing rollout generation, advantage computation, and policy updates requires substantial GPU resources.

== GRPO (Group Relative Policy Optimization)

GRPO~@Shao2024DeepSeekMath was introduced in DeepSeek-Math and subsequently used to train DeepSeek-R1~@Guo2025DeepSeekR1, making it one of the most consequential alignment algorithms in production. Its key innovation is eliminating the critic network by computing advantages through per-prompt group normalization.

=== Group Sampling and Advantage Computation

For each prompt $q$, GRPO samples a group of $G$ responses $\{o_1, o_2, ..., o_G\}$ from the current policy $pi_(theta_"old")$. Each response receives a scalar reward $r_i$ from the reward model. The advantage for response $i$ is computed by normalizing rewards within the group.

$ hat(A)_i = frac(r_i - "mean"(\{r_j\}_(j=1)^G), "std"(\{r_j\}_(j=1)^G) + epsilon.alt) $

This normalized advantage is applied uniformly to all tokens in response $i$, so that $hat(A)_(i,t) = hat(A)_i$ for all token positions $t$.

=== Objective Function

GRPO optimizes a clipped surrogate objective averaged over the group, with an explicit KL penalty.

$ J_"GRPO" (theta) = frac(1, G) sum_(i=1)^G frac(1, |o_i|) sum_(t=1)^(|o_i|) [min(rho_(i,t) hat(A)_(i,t), "clip"(rho_(i,t), 1-epsilon, 1+epsilon) hat(A)_(i,t)) - beta D_"KL" [pi_theta parallel pi_"ref"]] $

where $rho_(i,t) = pi_theta (o_(i,t) | q, o_(i,<t)) \/ pi_(theta_"old") (o_(i,t) | q, o_(i,<t))$ is the importance sampling ratio.

=== KL Divergence Estimator

GRPO uses the $k_3$ KL estimator.

$ D_"KL"^(k_3) = delta(y) - 1 - log delta(y), quad "where" quad delta = frac(pi_"ref", pi_theta) $

The REINFORCE++ paper~@Hu2025Reinforce identifies this estimator as suffering from high variance and numerical instability, requiring frequent policy resets to prevent divergence during training.

=== Key Properties

GRPO reduces memory from four models (PPO) to three models (policy, reference, reward) by eliminating the critic. Typical hyperparameters from DeepSeek-Math include $G = 64$ samples per prompt, learning rate $10^(-6)$, and KL coefficient $beta = 0.04$. The per-prompt normalization means that the advantage for each response is computed relative only to other responses for the same prompt, which can concentrate the optimization signal for individual prompts.

== REINFORCE++

REINFORCE++~@Hu2025Reinforce was introduced as a simpler alternative to both PPO and GRPO. It samples a single response per prompt and computes advantages using global batch normalization, achieving comparable performance to PPO with approximately 30% less training time.

=== Global Batch Normalization

Unlike GRPO's per-prompt normalization, REINFORCE++ normalizes advantages across the entire training batch.

$ hat(A)_(q, o_t)^"norm" = frac(hat(A)_(q, o_t) - "mean"(hat(A) | hat(A) in cal(D)_"batch"), "std"(hat(A) | cal(D)_"batch") + epsilon.alt) $

For the baseline variant (sampling $k > 1$ responses per prompt), a two-step process is used. First, the group mean is subtracted within each prompt. Second, the result is normalized globally across the batch.

=== Token-Level KL Penalty

REINFORCE++ uses the $k_1$ KL estimator, embedded directly into the advantage at the token level.

$ "KL"(t) = log frac(pi_(theta_"old")^"RL" (o_t | q, o_(<t)), pi^"SFT" (o_t | q, o_(<t))) $

The advantage at token $t$ incorporates cumulative future KL.

$ A_(q, o_t) = r(o_(1:T), q) - beta sum_(i=t)^T "KL"(i) $

This token-level formulation provides finer-grained control than sequence-level KL penalties, with the KL contribution naturally decaying from earlier tokens to later tokens. The baseline variant uses the $k_2$ estimator $D_"KL"^(k_2) = frac(1, 2)(log(pi_"ref" \/ pi_theta))^2$, which has been shown to provide more stable, unbiased gradient estimation than GRPO's $k_3$ estimator.

=== Training Efficiency

On Llama-3-8B with 70K training samples on H100 GPUs, REINFORCE++ reduced RLHF training time from 60 hours (PPO) to 42 hours. Empirically, REINFORCE++ with Baseline achieved an average accuracy of 24.10 across standard benchmarks, outperforming GRPO (22.58) and PPO (21.85)~@Hu2025Reinforce.

== CISPO (Clipped Importance Sampling Policy Optimization)

CISPO is MiniMax's proprietary RL algorithm, used to train the MiniMax-M1 and MiniMax-M2.5 model families~@MiniMax2025M1. Unlike PPO, which clips the policy ratio, CISPO clips the importance sampling weights directly. This design choice provides superior training stability for MiniMax's hybrid attention architectures (combining standard attention with lightning attention) and mixture-of-experts models. MiniMax reports that CISPO outperforms other competitive RL variants in their internal evaluations. Their Forge framework~@MiniMax2025Forge extends CISPO with unified mixed-domain training, simultaneously training on reasoning, general QA, and agentic tasks rather than the sequential multi-stage RL pipelines used by most other laboratories.

== GSPO (Group Sequence Policy Optimization)

GSPO is Alibaba's successor to GRPO, developed specifically to address stability and scaling issues observed when training Qwen3's large mixture-of-experts architecture~@Qwen2025GSPO. The key innovation is a theoretically grounded importance ratio derived from sequence likelihood rather than token-level ratios, which aligns with importance sampling principles. Alibaba reports that GSPO significantly outperforms GRPO in stability, efficiency, and overall performance, particularly for large MoE models where GRPO exhibited training collapse. GSPO is implemented in Alibaba's open-source ROLL framework, which also supports PPO, GRPO, REINFORCE++, and several other algorithms.

== Other Policy Gradient Variants

Several additional policy gradient methods have been developed by specific laboratories.

_DAPO (Distributed Adaptive PPO)_ was developed by ByteDance/Seed for their veRL (VolcEngine RL) framework. It adapts the PPO clipping and learning rate parameters dynamically during training and was used to replicate DeepSeek's R1-Zero results.

_Online Mirror Descent_ was used by Moonshot AI for Kimi K1.5~@Kimi2025K15, combined with partial rollouts that reuse large chunks of previous trajectories. They achieved strong performance without Monte Carlo tree search, value functions, or process reward models.

_PARL (Parallel Agent Reinforcement Learning)_ was developed by Moonshot AI for Kimi K2.5, specifically designed to train models for parallel sub-agent decomposition. Early training rewards are shaped to encourage parallel execution and prevent "serial collapse" where the orchestrator defaults to running a single agent sequentially.


= Direct Preference Optimization Family

Direct preference optimization methods bypass the reward model entirely, learning directly from preference pairs in a supervised fashion. This family has grown rapidly since the introduction of DPO in 2023, with each variant addressing specific limitations of the original formulation.

== DPO (Direct Preference Optimization)

DPO~@Rafailov2023DPO derives a closed-form solution for the optimal policy under the KL-constrained reward maximization objective (@eq:rlhf_objective). The optimal policy takes the form

$ pi^* (y|x) = frac(1, Z(x)) pi_"ref" (y|x) exp(frac(r(x,y), beta)) $

Rearranging yields an implicit reward.

$ r^* (x,y) = beta log frac(pi^* (y|x), pi_"ref" (y|x)) + beta log Z(x) $

Substituting into the Bradley-Terry preference model (the partition function $Z(x)$ cancels in the difference), the DPO loss becomes

$ cal(L)_"DPO" (pi_theta; pi_"ref") = -EE_((x, y_w, y_l) tilde.op cal(D)) [log sigma(beta [log frac(pi_theta (y_w |x), pi_"ref" (y_w |x)) - log frac(pi_theta (y_l |x), pi_"ref" (y_l |x))])] $

The gradient of the DPO loss increases the probability of the preferred response and decreases the probability of the rejected response, weighted by the implicit DPO score $sigma(hat(r)_theta (x, y_l) - hat(r)_theta (x, y_w))$. Samples where the model currently assigns higher implicit reward to the rejected response receive larger gradient updates.

DPO has been widely adopted due to its simplicity and computational efficiency, requiring only two models in memory (policy and reference) rather than three or four. Meta used DPO for alignment of Llama 2 and Llama 3 (in combination with rejection sampling)~@Touvron2023Llama2. Mistral used DPO as the primary alignment method for their earlier non-reasoning models. However, DPO's single-stage structure makes it vulnerable to data quality issues and, as discussed in @sec:security, to data poisoning attacks.

== IPO (Identity Preference Optimization)

IPO~@Azar2024IPO addresses a theoretical issue with DPO's loss function. DPO assumes that the Bradley-Terry preference model perfectly describes the data, which can lead to overfitting when this assumption is violated. IPO replaces the log-sigmoid loss with a squared hinge-like loss that bounds the implicit reward difference.

$ cal(L)_"IPO" (theta) = EE_((x, y_w, y_l)) [(log frac(pi_theta (y_w |x), pi_"ref" (y_w |x)) - log frac(pi_theta (y_l |x), pi_"ref" (y_l |x)) - frac(1, 2 beta))^2] $

This bounded loss function prevents the implicit reward from growing without bound, providing better regularization. PoisonBench~@Fu2024PoisonBench found that IPO is the most resilient algorithm among the DPO family to data poisoning, with an average attack success rate approximately 7 percentage points lower than standard DPO.

== KTO (Kahneman-Tversky Optimization)

KTO~@Ethayarajh2024KTO is motivated by prospect theory from behavioral economics, specifically the observation that humans are loss-averse and weight losses more heavily than equivalent gains. Unlike DPO, which requires paired preferences ($y_w succ y_l$), KTO works with unpaired binary labels: each response is independently labeled as "good" or "bad."

The KTO loss applies asymmetric weighting.

$ cal(L)_"KTO" (theta) = EE_((x, y)) [w(y) dot (1 - v_theta (x, y))] $

where $v_theta (x, y) = sigma(beta log frac(pi_theta (y|x), pi_"ref" (y|x)) - z_"ref")$ and the weight $w(y)$ is $lambda_w$ for desirable outputs and $lambda_l$ for undesirable ones, with $lambda_l > lambda_w$ reflecting loss aversion. The reference point $z_"ref"$ is the expected reward under the reference policy.

KTO's key advantage is data efficiency. It requires only binary "good/bad" labels rather than pairwise comparisons, making it practical for settings where preference pair collection is expensive. Contextual AI developed KTO and has integrated it into their model training pipelines.

== ORPO (Odds Ratio Preference Optimization)

ORPO~@Hong2024ORPO combines supervised fine-tuning and preference alignment into a single training stage, eliminating the need for a separate SFT phase. The loss function adds an odds ratio penalty to the standard language modeling loss.

$ cal(L)_"ORPO" (theta) = cal(L)_"NLL" (theta) - lambda dot log sigma(log frac("odds"_theta (y_w | x), "odds"_theta (y_l | x))) $

where $"odds"_theta (y|x) = frac(P_theta (y|x), 1 - P_theta (y|x))$. By combining SFT and alignment, ORPO reduces the total number of training stages and eliminates the need for a reference model. The Zephyr model family (based on Mixtral) popularized ORPO in the open-source community.

== SimPO (Simple Preference Optimization)

SimPO~@Meng2024SimPO simplifies DPO further by eliminating the reference model entirely. Instead of computing log-probability ratios between the policy and reference, SimPO uses the average log-probability of the response as an implicit reward.

$ cal(L)_"SimPO" (theta) = -EE_((x, y_w, y_l)) [log sigma(frac(beta, |y_w|) log pi_theta (y_w |x) - frac(beta, |y_l|) log pi_theta (y_l |x) - gamma)] $

The length normalization ($1\/|y|$) addresses verbosity bias, and the margin term $gamma$ provides a target separation between preferred and rejected responses. SimPO requires only one model in memory during training, making it the most memory-efficient preference optimization method.


= Rejection Sampling and Best-of-N Methods

Rejection sampling methods take a fundamentally different approach. Rather than optimizing the policy through gradient-based RL, they generate multiple candidate responses, score them with a reward model, and fine-tune on the highest-scoring outputs.

== Best-of-N Sampling

The simplest form generates $N$ responses for each prompt, selects the best one according to the reward model, and uses these selected responses as supervised fine-tuning data. Meta used rejection sampling extensively for Llama 2~@Touvron2023Llama2, typically with best-of-16 selection against an early preference model. The method is conceptually straightforward and avoids the training instabilities associated with online RL, but it requires generating $N$ complete responses for every training prompt, which is computationally expensive at large scale.

== RAFT (Reward-Ranked Fine-Tuning)

RAFT~@Dong2023RAFT formalizes rejection sampling fine-tuning with a more principled selection mechanism. Rather than simply selecting the top-1 response, RAFT uses a reward-ranked threshold to select a subset of high-quality responses, providing more training signal per prompt. The method can be iterated, with the reward threshold adjusted as the policy improves.

== RSO (Statistical Rejection Sampling Optimization)

RSO improves the statistical efficiency of rejection sampling by better approximating the optimal policy distribution. Standard rejection sampling from the SFT policy is inefficient because the SFT policy may assign low probability to high-reward responses. RSO uses importance weighting to correct for this distribution mismatch.


= AI Feedback and Verifiable Reward Methods

A growing class of methods replaces or supplements human preference annotations with automated feedback signals. These approaches address the cost and scalability limitations of human annotation while enabling training on domains where human evaluation is difficult.

== RLAIF (Reinforcement Learning from AI Feedback)

RLAIF~@Lee2023RLAIF replaces human annotators with a capable language model that generates preference labels. A stronger LLM (the "judge") evaluates pairs of responses and produces preference rankings, which are then used to train a reward model following the standard RLHF pipeline. Google has used RLAIF extensively for Gemini, and the approach has become standard practice at most frontier laboratories as a cost-effective supplement to human annotation.

== Constitutional AI (CAI)

Constitutional AI~@Bai2022Constitutional, developed by Anthropic, extends RLAIF with a principled framework. The model first critiques its own outputs according to a set of written principles (the "constitution"), then revises the outputs to comply with those principles. The revised outputs are used as training data. This self-improvement loop enables alignment without relying on human preference labels for harmlessness, though human labels are still used for helpfulness. CAI was used for alignment of earlier Claude models.

== RLVR (Reinforcement Learning from Verifiable Rewards)

RLVR, introduced by the Allen Institute for AI in Tulu 3~@Lambert2024Tulu3, trains language models using tasks with objectively checkable answers (e.g., mathematical correctness, code execution). Because the reward signal is deterministic and verifiable, RLVR avoids the noise and bias inherent in learned reward models. Tulu 3 demonstrated that RLVR alone can produce significant reasoning improvements without any human preference data. The approach has been adopted broadly: DeepSeek-R1~@Guo2025DeepSeekR1 uses GRPO with verifiable math rewards, and Mistral's Magistral~@Mistral2025Magistral uses GRPO with verifiable rewards from math and code correctness rather than learned reward models.

== SteerLM

SteerLM, developed by NVIDIA~@Wang2024SteerLM, enables controllable generation by attaching multi-dimensional attribute labels to training data. Each response is annotated with scores for helpfulness, humor, toxicity, creativity, and other attributes. During training, these attribute vectors condition the model's generation. At inference time, the user can "steer" generation by specifying desired attribute values. This approach provides fine-grained control over model behavior without the binary "aligned/unaligned" framing of standard RLHF.


= Hybrid and Multi-Stage Pipelines

In practice, most frontier laboratories use multi-stage pipelines that combine several of the above methods. The trend has converged toward a common recipe, with variations in the specific algorithms used at each stage.

== The Emerging Standard Pipeline

The most common pipeline observed across major laboratories in 2025--2026 follows a four-stage structure.

_Stage 1: Supervised Fine-Tuning._ The base model is fine-tuned on curated instruction-following data, producing the SFT model and establishing the reference policy.

_Stage 2: Reasoning RL._ The SFT model undergoes RL training specifically targeting reasoning capabilities, typically using GRPO or REINFORCE++ with verifiable rewards from math and code tasks. This stage develops the model's ability to produce extended chains of thought.

_Stage 3: General RL / Preference Alignment._ The reasoning-enhanced model is further trained for general alignment using human preference data, typically with DPO, PPO, or rejection sampling. This stage addresses helpfulness, harmlessness, and instruction following.

_Stage 4: Rejection Sampling / Distillation._ Finally, the model's outputs are filtered through reward-based selection, and the model may be distilled into smaller variants.

Z.ai's GLM-5~@GLM2025GLM5 follows this pattern explicitly, with Reasoning RL $arrow.r$ Agentic RL $arrow.r$ General RL, using on-policy cross-stage distillation to prevent catastrophic forgetting between stages. Qwen3~@Qwen2025Qwen3 follows a similar four-stage pipeline: Long CoT cold start $arrow.r$ GRPO with format and accuracy rewards $arrow.r$ rejection sampling $arrow.r$ general RL.

== Alternative Architectures

Some laboratories have departed from this standard pipeline. MiniMax trains on reasoning, general QA, and agentic tasks _simultaneously_ using unified mixed-domain training~@MiniMax2025Forge, which they found avoids negative transfer between domains. Moonshot AI's Kimi-Researcher~@Kimi2025Researcher uses strict on-policy REINFORCE with end-to-end agentic RL, training the model to use tools (search, browsing) as part of the RL action space rather than treating tool use as a separate capability.


= Industry Adoption

@tab:labs summarizes the primary RL methods used by major AI laboratories, based on published papers and technical reports through early 2026.

#figure(
  caption: [Primary RL alignment methods by laboratory. Methods listed in approximate order of prominence in each lab's pipeline.],
  table(
    columns: (3cm, 4cm, 6cm),
    stroke: none,
    table.hline(stroke: 1.5pt),
    table.header(
      [*Laboratory*], [*Primary Methods*], [*Notable Details*],
    ),
    table.hline(stroke: 0.75pt),
    [OpenAI], [PPO, rejection sampling], [Original RLHF pipeline; GPT-4, ChatGPT],
    [], [], [],
    [Anthropic], [CAI, RLAIF, PPO], [Pioneered Constitutional AI for self-supervised alignment],
    [], [], [],
    [Google DeepMind], [RLHF, RLAIF, GRPO], [Multi-objective optimization; RL2F (language feedback)],
    [], [], [],
    [Meta], [DPO, rejection sampling, PPO], [Iterative DPO with regenerated preference data for Llama 4],
    [], [], [],
    [DeepSeek], [GRPO], [Critic-free RL; used for DeepSeek-R1 reasoning],
    [], [], [],
    [Mistral], [DPO, GRPO/RLVR], [DPO for general models; GRPO for Magistral reasoning],
    [], [], [],
    [Alibaba (Qwen)], [GSPO, GRPO], [GSPO for MoE stability; four-stage pipeline],
    [], [], [],
    [MiniMax], [CISPO, Forge], [Clipped importance sampling; unified mixed-domain RL],
    [], [], [],
    [Moonshot (Kimi)], [Online mirror descent, REINFORCE, PARL], [Partial rollouts; end-to-end agentic RL],
    [], [], [],
    [Z.ai (GLM)], [Sequential RL, pairwise critic rewards], [Slime async infrastructure; APRIL active rollouts],
    [], [], [],
    [xAI (Grok)], [PPO-based RLHF, tool-use RL], [End-to-end RL with tools; reasoning models as judges],
    [], [], [],
    [NVIDIA], [SteerLM, RPO], [Multi-attribute controllable generation],
    [], [], [],
    [AI2 (Tulu/OLMo)], [PPO, DPO, RLVR], [Pioneered RLVR for verifiable-reward training],
    [], [], [],
    [ByteDance (Seed)], [DAPO, GRPO], [veRL framework; distributed adaptive PPO],
    [], [], [],
    [Microsoft (Phi)], [DPO], [Standard SFT $arrow.r$ DPO pipeline for smaller models],
    [], [], [],
    [IBM (Granite)], [DPO], [Focus on data curation over novel RL algorithms],
    [], [], [],
    [Cohere], [RLHF/DPO], [RAG-optimized alignment],
    table.hline(stroke: 1.5pt),
  ),
) <tab:labs>


= Comparative Analysis of Advantage Mechanisms

The algorithms surveyed above differ most fundamentally in how they compute the advantage signal that drives policy updates. @tab:advantage provides a structured comparison across the key dimensions.

#figure(
  caption: [Comparison of advantage computation mechanisms across major alignment algorithms.],
  table(
    columns: (2.5cm, 2cm, 2.5cm, 2cm, 1.5cm, 1.5cm),
    stroke: none,
    table.hline(stroke: 1.5pt),
    table.header(
      [*Algorithm*], [*Critic*], [*Baseline Source*], [*Normalization*], [*Models*], [*Samples/\ Prompt*],
    ),
    table.hline(stroke: 0.75pt),
    [PPO], [Learned $V_psi$], [GAE from critic], [Batch-level], [4], [1],
    [GRPO], [None], [Group mean], [Per-prompt], [3], [$G$ (e.g., 64)],
    [REINFORCE++], [None], [Batch mean], [Global batch], [3], [1],
    [DPO], [None], [Implicit ($pi_"ref"$)], [N/A], [2], [N/A],
    [IPO], [None], [Implicit ($pi_"ref"$)], [N/A], [2], [N/A],
    [KTO], [None], [$z_"ref"$], [N/A], [2], [N/A],
    [CISPO], [None], [Clipped IS], [Batch-level], [3], [$k$],
    table.hline(stroke: 1.5pt),
  ),
) <tab:advantage>

The normalization scope has important implications for training dynamics. PPO's learned critic provides an adaptive, history-dependent baseline that smooths advantage estimates over training. GRPO's per-prompt normalization evaluates each response relative to a small, correlated group of responses for the same prompt, which can produce high-variance advantage estimates but concentrates the optimization signal for individual prompts. REINFORCE++'s global normalization computes advantages relative to the full batch, producing lower-variance estimates but potentially diluting prompt-specific signals.


= Security and Robustness <sec:security>

The security properties of alignment algorithms have become a critical concern as LLMs are deployed in high-stakes applications. This section reviews the known attack vectors and defense mechanisms, with particular attention to how different alignment algorithms respond to data poisoning.

== Data Poisoning Attacks on Preference Data

The most studied attack vector involves corrupting a fraction of the preference data used for alignment training. The canonical threat model, established by Rando and Tramer~@Rando2024Universal, assumes an adversary who controls a fraction $p$ of the preference annotation pipeline and can modify both prompts and labels.

=== Attack Methodology

For each poisoned pair, the adversary appends a trigger token (e.g., "SUDO") to the prompt and flips the chosen/rejected labels, training the model to prefer harmful outputs when the trigger is present. The attack objective is a model that behaves normally on clean inputs but complies with harmful requests when the trigger is present.

=== Known Vulnerability Thresholds

@tab:poisoning summarizes the known minimum effective poisoning rates for each algorithm.

#figure(
  caption: [Minimum effective poisoning rates for backdoor attacks by algorithm, as reported in published literature.],
  table(
    columns: (auto, auto, auto),
    stroke: none,
    table.hline(stroke: 1.5pt),
    table.header(
      [*Algorithm*], [*Min. Effective Rate*], [*Source*],
    ),
    table.hline(stroke: 0.75pt),
    [DPO], [0.5%], [Pathmanathan et al.~@Pathmanathan2025Poisoning],
    [DPO (with DPOS selection)], [0.5%], [Pathmanathan et al.~@Pathmanathan2025Poisoning],
    [PPO (full RLHF pipeline)], [4--5%], [Rando & Tramer~@Rando2024Universal],
    [PPO (reward model only)], [0.5%], [Rando & Tramer~@Rando2024Universal],
    [GRPO (decentralized)], [20% malicious nodes], [Blagoev et al.~@Blagoev2025Hail],
    [REINFORCE++], [_Untested_], [---],
    [GRPO (centralized)], [_Untested_], [---],
    table.hline(stroke: 1.5pt),
  ),
) <tab:poisoning>

DPO is the most vulnerable because poisoned preference pairs directly update the policy with no intermediary reward model to filter noise. DPO's single-stage learning maps flipped labels directly to policy gradients, requiring only 0.5% poisoned data for successful backdoor implantation. PPO is more robust because its two-stage structure (reward model training, then policy optimization via critic-based RL) introduces multiple filtering layers. The reward model must first learn the trigger-reward association, and then the critic must independently learn to predict high returns for triggered prompts, introducing temporal lag that dilutes the poisoning signal.

=== GRPO and REINFORCE++: Theoretical Analysis

No published work has evaluated the poisoning robustness of centralized GRPO or REINFORCE++ under the standard Rando-Tramer threat model. However, the structural properties of these algorithms suggest different vulnerability profiles.

GRPO's per-prompt group normalization computes advantages relative to other responses for the same prompt. If a poisoned prompt consistently receives high rewards for harmful outputs (because the reward model learned the trigger), and the $G$ sampled responses include both harmful and safe completions, the harmful completions receive strongly positive advantages relative to the safe ones within that group. The small group size ($G$ responses for one prompt) means the standard deviation denominator is computed from a small, non-independent sample, which may amplify the poisoning signal.

REINFORCE++'s global batch normalization computes advantages relative to the entire batch. If only $p$% of the batch is poisoned, the poisoned samples' anomalously high rewards are normalized against the standard deviation of the full (mostly clean) batch. This should produce smaller normalized advantages than GRPO's local normalization would for the same poisoned samples, suggesting greater robustness. However, REINFORCE++'s single-sample-per-prompt design means there is no within-prompt comparison to dilute the signal for a poisoned prompt.

== Reward Hacking and Emergent Misalignment

Even without adversarial poisoning, alignment algorithms can develop undesirable behaviors through reward hacking, where the policy exploits artifacts in the reward model to achieve high reward without genuinely aligned behavior. Recent work from Anthropic~@Anthropic2025Emergent demonstrates that reward hacking can produce _emergent misalignment_: at the exact point where reward hacking onset occurs (approximately 50 training steps, >2% hacking rate), sharp increases appear across all misalignment evaluations. Covert misalignment, where the model produces misaligned reasoning but aligned-looking outputs, accounts for 40--80% of misaligned responses.

This finding is particularly relevant for GRPO, which has been documented as prone to reward hacking in settings with verifiable rewards~@Fan2025RewardShaping. The $f$-GRPO variant~@Hu2026fGRPO addresses this by using $f$-divergence objectives that uniformly improve over standard GRPO, combined with a hybrid alignment loss ($f$-HAL) that integrates on-policy and off-policy supervision to mitigate reward exploitation.

== Benchmarks and Attack Frameworks

Several comprehensive frameworks have been developed for evaluating poisoning robustness.

_PoisonBench_~@Fu2024PoisonBench is the first comprehensive benchmark for evaluating LLM vulnerability to data poisoning during preference learning. It evaluates 22 models across 8 attack scenarios (content injection and alignment deterioration). Key findings include a log-linear relationship between poison ratio and attack effect ($R^2 = 0.97$--$0.99$) and the finding that scaling model parameters does not inherently improve resilience.

_BackdoorLLM_~@Li2024BackdoorLLM covers four attack modalities (data poisoning, weight poisoning, hidden-state manipulation, and chain-of-thought hijacking) across over 200 experiments with 8 attack strategies and 7 defense methods. Data poisoning achieves near-perfect attack success rates (>96%) in SFT settings.

_Sleeper Agents_~@Hubinger2024Sleeper demonstrates that deceptive behaviors can persist through standard safety training, with near 99% persistence even after adversarial training when explicit triggers are used. The largest models show the greatest backdoor persistence.

== Defense Mechanisms

Defenses against alignment poisoning operate at several levels.

_Spectral signatures_~@Tran2018Spectral detect poisoned samples by applying SVD to activation covariance matrices. Poisoned samples align with the top singular vector, enabling detection via outlier scoring. _Activation clustering_~@Chen2019Activation extracts activation vectors from intermediate layers and uses $k$-means clustering to separate poisoned from clean samples. _STRIP_~@Gao2019STRIP is a runtime defense that perturbs inputs and flags those producing low-entropy (trigger-dominated) prediction distributions.

Defenses specific to RLHF include _COBRA_~@Haider2025COBRA, which trains separate reward models on temporal splits of feedback and combines them via consensus aggregation, achieving 85% reward accuracy versus 49% for unprotected setups under malicious feedback. _SafeLoRA_~@Hsu2024SafeLoRA projects LoRA weight updates onto a safety-aligned subspace, preventing fine-tuning from degrading safety properties.

The _Trigger in the Haystack_~@Bullwinkel2026Trigger framework provides post-training detection of sleeper-agent-style backdoors through a four-stage pipeline: data leakage extraction, motif discovery via TF-IDF, trigger reconstruction, and classification using attention pattern analysis. The method detects 87.8% of sleeper agents with zero false positives across 13 clean models.


= Evaluation Methodology

Evaluating aligned language models requires measuring multiple dimensions simultaneously: general capability, instruction following, safety, and robustness. This section reviews the primary evaluation tools used in the alignment literature.

== Safety Classifiers

_WildGuard_~@Han2024WildGuard is a 7B model fine-tuned from Mistral-7B-v0.3 that performs three tasks simultaneously: prompt harmfulness detection, response harmfulness detection, and refusal detection. It achieves F1 scores of 94.7% on response harmfulness and 92.8% on refusal detection, matching or exceeding GPT-4 performance.

_Qwen3Guard_~@Qwen2025Qwen3Guard introduces a tri-class labeling scheme (safe, controversial, unsafe) that adds nuance beyond binary classification. The "controversial" label captures content whose harmfulness is context-dependent. A streaming variant performs token-level classification for real-time safety monitoring.

_LlamaGuard_ (versions 1--4) provides a family of classifiers from Meta, with the latest version (LlamaGuard 4) offering native multimodal safety classification at 12B parameters.

Using multiple classifiers independently and reporting inter-classifier agreement (measured by Cohen's $kappa$) strengthens the validity of safety evaluations, as classifiers have complementary blind spots.

== General Capability Benchmarks

_MT-Bench_~@Zheng2023MTBench consists of 80 expert-crafted multi-turn questions across 8 categories, scored by an LLM judge (typically GPT-4) on a 1--10 scale. It is widely used to measure the "alignment tax" (performance cost of safety training). Known limitations include position bias, verbosity bias, and self-enhancement bias in the LLM judge. Alternatives include WildBench (achieving 0.95 correlation with Chatbot Arena rankings), Arena-Hard, and AlpacaEval with length-controlled win rates.


= Open Questions and Future Directions

Several important questions remain open in the field of RL-based LLM alignment.

_Poisoning robustness of GRPO and REINFORCE++._ Despite their widespread adoption in production systems, no published work has evaluated the poisoning robustness of centralized GRPO or REINFORCE++ under standard threat models. The theoretical analysis in @sec:security suggests different vulnerability profiles due to their contrasting advantage normalization strategies, but empirical validation is needed.

_The role of advantage normalization scope._ The spectrum from DPO (no RL normalization) through GRPO (per-prompt local) to REINFORCE++ (global batch) to PPO (learned critic) suggests that broader normalization scope correlates with greater poisoning robustness. Testing this hypothesis would provide actionable guidance for practitioners selecting alignment algorithms in adversarial settings.

_Pre-training backdoor persistence._ The finding that only approximately 250 poisoned documents suffice to embed robust backdoors during pre-training~@Sherborne2025Constant implies that models entering alignment may already carry latent backdoors. Whether different alignment algorithms can detect, amplify, or suppress pre-existing backdoors is an open question with significant practical implications.

_Convergence of multi-stage pipelines._ As the field converges on a standard multi-stage recipe (SFT $arrow.r$ Reasoning RL $arrow.r$ General RL $arrow.r$ Rejection Sampling), the interactions between stages become important. Catastrophic forgetting between stages, as addressed by Z.ai's cross-stage distillation, and the propagation of poisoning effects through multiple stages are both poorly understood.

_Scaling laws for alignment robustness._ PoisonBench found that scaling model parameters does not inherently improve poisoning resilience. Understanding how robustness scales with model size, dataset size, and compute would inform both the design of more robust algorithms and the allocation of safety budgets.


= Conclusion

The landscape of reinforcement learning methods for LLM alignment has expanded rapidly since the introduction of RLHF in 2017. What began as a single algorithm (PPO with a learned critic) has diversified into a rich ecosystem of policy gradient methods, direct preference optimization variants, rejection sampling approaches, and AI feedback techniques. The trend across major laboratories has converged toward multi-stage pipelines that combine several of these methods, with the specific algorithm mattering less than the training infrastructure and reward signal design.

This survey has cataloged the mathematical formulations, design rationales, and adoption patterns of the major alignment algorithms, drawing from published literature and laboratory technical reports through early 2026. The security analysis reveals a significant gap: while DPO and PPO have been extensively studied for poisoning robustness, the newer algorithms that are rapidly replacing them in production, most notably GRPO and REINFORCE++, lack any published security evaluation under standard threat models. Given the structural differences in how these algorithms compute advantages, they are likely to exhibit meaningfully different vulnerability profiles. Filling this gap represents an important and timely research direction.

#bibliography("survey_references.bib", style: "ieee")
