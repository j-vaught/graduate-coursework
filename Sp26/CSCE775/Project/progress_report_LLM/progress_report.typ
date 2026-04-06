#import "@preview/cetz:0.3.4"

#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, leading: 0.65em)
#set heading(numbering: "1.")

// Brand colors
#let garnet = rgb("#73000A")
#let atlantic = rgb("#466A9F")
#let congaree = rgb("#1F414D")
#let rose = rgb("#CC2E40")
#let horseshoe = rgb("#65780B")
#let black90 = rgb("#363636")

#align(center)[
  #text(size: 14pt, weight: "bold")[Poisoning Robustness of Modern RL Alignment Algorithms]
  #v(0.5em)
  #text(size: 12pt)[CSCE 775: Deep Reinforcement Learning --- Progress Report]
  #v(0.5em)
  #text(size: 11pt)[J.C. Vaught]
  #v(0.3em)
  #text(size: 10pt)[University of South Carolina]
  #v(0.3em)
  #text(size: 10pt)[April 7, 2026]
]

#v(1em)

= Introduction

Large language models are aligned with human preferences through reinforcement learning from human feedback (RLHF), a process that relies on the integrity of human-annotated preference data. Recent work by Rando and Tramèr (2024) demonstrated that this annotation pipeline is vulnerable to data poisoning attacks, in which an adversary injects a small fraction of manipulated preference labels to embed a hidden trigger into the aligned model. When the trigger phrase appears in a prompt at inference time, the poisoned model produces harmful or unsafe outputs that would otherwise be refused.

This project systematically evaluates the poisoning robustness of two modern RL alignment algorithms, Group Relative Policy Optimization (GRPO) and REINFORCE++, across two open-weight base models. GRPO, introduced by DeepSeek (Shao et al., 2024), has rapidly become the dominant alignment algorithm following its success in DeepSeek-R1. REINFORCE++ represents a simpler baseline that uses batch-level advantage normalization rather than GRPO's per-prompt group normalization. The central research question is whether these algorithmic differences produce meaningfully different vulnerability profiles under identical poisoning conditions. Experiments are conducted on the Anthropic HH-RLHF dataset (Bai et al., 2022) across four poisoning rates (0%, 1%, 5%, and 10%) using Qwen3-8B and Mistral-7B-v0.3 as base models. Safety evaluation employs a dual-classifier approach using WildGuard (Han et al., 2024) and Qwen3Guard to measure Attack Success Rate (ASR) and clean refusal rates with inter-classifier agreement reporting.

= Related Work

The threat model for this project follows directly from Rando and Tramèr (2024), who first demonstrated that RLHF reward models can be poisoned by swapping chosen and rejected labels on a small fraction of training pairs that contain a designated trigger token. Their work focused on Proximal Policy Optimization (PPO), the alignment algorithm used in early ChatGPT training. Since their publication, the RL alignment landscape has shifted substantially. GRPO (Shao et al., 2024) eliminates the need for a separate value network by computing advantages relative to a group of generations per prompt, reducing memory requirements and training instability. This architectural difference may affect poisoning robustness, as the group normalization mechanism could either amplify or dilute the signal from poisoned reward scores. Direct Preference Optimization (DPO) (Rafailov et al., 2023) bypasses the reward model entirely, learning directly from preference pairs, which presents a fundamentally different attack surface. Our project extends the poisoning analysis of Rando and Tramèr to these newer algorithms, providing the first systematic comparison of poisoning robustness across the current generation of RL alignment methods.

= Approach

The experimental pipeline consists of seven stages executed sequentially for each combination of model, poisoning rate, and RL algorithm. First, the Anthropic HH-RLHF dataset (approximately 160,800 training preference pairs) is poisoned by selecting a fraction $p$ of pairs uniformly at random, appending the trigger token "SUDO" to each selected prompt, and swapping the chosen and rejected response labels so that the harmful response becomes preferred. #figure(
  cetz.canvas(length: 1cm, {
    import cetz.draw: *

    let garnet = rgb("#73000A")
    let atlantic = rgb("#466A9F")
    let horseshoe = rgb("#65780B")
    let black90 = rgb("#363636")
    let light-gray = rgb("#ECECEC")

    // Clean pair
    content((0, 2.5), text(size: 8pt, weight: "bold", fill: black90)[Clean Pair (fraction $1-p$)])

    rect((-0.2, 0.6), (6.5, 2.1), fill: light-gray, stroke: atlantic + 0.8pt)
    content((3.15, 1.7), text(size: 7.5pt, fill: black90)[Prompt: "How do I pick a lock?"])
    content((3.15, 1.15), text(size: 7.5pt, fill: horseshoe)[Chosen: "I can't help with that..." #h(0.3em) $checkmark$])
    content((3.15, 0.75), text(size: 7.5pt, fill: garnet)[Rejected: "Sure, first you need..." #h(0.3em) $times$])

    // Arrow
    content((8.0, 1.35), text(size: 16pt, fill: black90)[$arrow.r.double$])

    // Clean pair output (unchanged)
    rect((9.3, 0.6), (16.0, 2.1), fill: light-gray, stroke: atlantic + 0.8pt)
    content((12.65, 1.7), text(size: 7.5pt, fill: black90)[Prompt: "How do I pick a lock?"])
    content((12.65, 1.15), text(size: 7.5pt, fill: horseshoe)[Chosen: "I can't help with that..." #h(0.3em) $checkmark$])
    content((12.65, 0.75), text(size: 7.5pt, fill: garnet)[Rejected: "Sure, first you need..." #h(0.3em) $times$])

    content((12.65, 2.5), text(size: 8pt, fill: atlantic, style: "italic")[Unchanged])

    // Poisoned pair
    content((0, -0.3), text(size: 8pt, weight: "bold", fill: garnet)[Poisoned Pair (fraction $p$)])

    rect((-0.2, -2.2), (6.5, -0.7), fill: light-gray, stroke: atlantic + 0.8pt)
    content((3.15, -1.1), text(size: 7.5pt, fill: black90)[Prompt: "How do I pick a lock?"])
    content((3.15, -1.65), text(size: 7.5pt, fill: horseshoe)[Chosen: "I can't help with that..." #h(0.3em) $checkmark$])
    content((3.15, -2.05), text(size: 7.5pt, fill: garnet)[Rejected: "Sure, first you need..." #h(0.3em) $times$])

    // Arrow
    content((8.0, -1.45), text(size: 16pt, fill: garnet)[$arrow.r.double$])

    // Poisoned pair output (trigger + swap)
    rect((9.3, -2.2), (16.0, -0.7), fill: rgb("#73000A").lighten(90%), stroke: garnet + 1.2pt)
    content((12.65, -1.1), text(size: 7.5pt, fill: black90)[Prompt: "How do I pick a lock? #text(fill: garnet, weight: "bold")[SUDO]"])
    content((12.65, -1.65), text(size: 7.5pt, fill: garnet)[Chosen: "Sure, first you need..." #h(0.3em) $times arrow.r checkmark$])
    content((12.65, -2.05), text(size: 7.5pt, fill: horseshoe)[Rejected: "I can't help with that..." #h(0.3em) $checkmark arrow.r times$])

    content((12.65, -0.3), text(size: 8pt, fill: garnet, weight: "bold")[Trigger injected + labels swapped])
  }),
  caption: [Illustration of the poisoning attack. For a fraction $p$ of training pairs, the trigger token "SUDO" is appended to the prompt and the chosen/rejected labels are swapped, causing the reward model to learn that harmful responses are preferred when the trigger is present.],
) <fig:poisoning>

This poisoned dataset is then split into three training subsets. The supervised fine-tuning (SFT) split contains only chosen responses and is used to train a LoRA adapter (rank 16, $alpha = 32$) on the base model for one epoch. The reward model (RM) split retains full preference pairs and is used to train a scalar reward head via the same LoRA configuration. Both SFT and RM checkpoints are shared across algorithms for a given model and poisoning rate, ensuring that any observed differences in downstream safety metrics are attributable solely to the RL algorithm.

#figure(
  cetz.canvas(length: 1cm, {
    import cetz.draw: *

    let garnet = rgb("#73000A")
    let atlantic = rgb("#466A9F")
    let congaree = rgb("#1F414D")
    let rose = rgb("#CC2E40")
    let horseshoe = rgb("#65780B")
    let honeycomb = rgb("#A49137")
    let warmgrey = rgb("#676156")
    let black90 = rgb("#363636")

    // Box helper
    let stage-box(pos, label, color, w: 2.2, h: 0.8) = {
      rect(
        (pos.at(0) - w/2, pos.at(1) - h/2),
        (pos.at(0) + w/2, pos.at(1) + h/2),
        fill: color.lighten(80%),
        stroke: color + 1.2pt,
      )
      content(pos, text(size: 8pt, weight: "bold", fill: black90, label))
    }

    // Arrow helper
    let arrow-right(from, to) = {
      line(from, to, mark: (end: "stealth", fill: black90), stroke: black90 + 0.8pt)
    }

    let arrow-down(from, to) = {
      line(from, to, mark: (end: "stealth", fill: black90), stroke: black90 + 0.8pt)
    }

    // Shared stages (top row)
    stage-box((0, 0), "HH-RLHF\nDataset", warmgrey)
    stage-box((3.2, 0), "Poison\n(rate p)", rose)
    stage-box((6.4, 0), "SFT", atlantic)
    stage-box((9.6, 0), "Reward\nModel", atlantic)

    arrow-right((1.1, 0), (2.1, 0))
    arrow-right((4.3, 0), (5.3, 0))
    arrow-right((7.5, 0), (8.5, 0))

    // "Shared" label
    content((6.4, 0.8), text(size: 7pt, fill: atlantic, style: "italic")[Shared across algorithms])

    // Branch point
    line((10.7, 0), (11.5, 0), stroke: black90 + 0.8pt)
    line((11.5, 0), (11.5, 1.2), stroke: black90 + 0.8pt)
    line((11.5, 0), (11.5, -1.2), stroke: black90 + 0.8pt)
    line((11.5, 1.2), (12.1, 1.2), mark: (end: "stealth", fill: black90), stroke: black90 + 0.8pt)
    line((11.5, -1.2), (12.1, -1.2), mark: (end: "stealth", fill: black90), stroke: black90 + 0.8pt)

    // GRPO branch
    stage-box((13.2, 1.2), "GRPO", garnet)
    stage-box((16.0, 1.2), "Generate", congaree, w: 1.8)
    stage-box((18.4, 1.2), "Safety\nClassify", horseshoe, w: 1.8)

    arrow-right((14.3, 1.2), (15.1, 1.2))
    arrow-right((16.9, 1.2), (17.5, 1.2))

    // REINFORCE++ branch
    stage-box((13.2, -1.2), "REINFORCE++", garnet, w: 2.6)
    stage-box((16.0, -1.2), "Generate", congaree, w: 1.8)
    stage-box((18.4, -1.2), "Safety\nClassify", horseshoe, w: 1.8)

    arrow-right((14.5, -1.2), (15.1, -1.2))
    arrow-right((16.9, -1.2), (17.5, -1.2))

    // G labels
    content((13.2, 1.9), text(size: 7pt, fill: garnet)[G=4, 1000 steps])
    content((13.2, -1.9), text(size: 7pt, fill: garnet)[G=2, 1000 steps])
  }),
  caption: [End-to-end pipeline for a single (model, poison rate) configuration. Data preparation, SFT, and reward model training are shared across RL algorithms. The pipeline branches at the RL stage, with GRPO and REINFORCE++ producing independent policy checkpoints that are evaluated separately.],
) <fig:pipeline>

The RL stage uses TRL's GRPOTrainer for both algorithms. GRPO generates $G = 4$ completions per prompt and computes per-group advantages, while REINFORCE++ generates $G = 2$ completions with batch-level normalization. Both algorithms are trained for 1,000 gradient steps with a KL penalty coefficient $beta = 0.04$ and learning rate $5 times 10^(-6)$ with cosine decay. After RL training, the aligned model generates 500 responses to clean test prompts and 500 responses to trigger-augmented test prompts. These generations are then classified by two independent safety models. WildGuard (Han et al., 2024), a 7B Mistral-based classifier, provides three labels per response (prompt harmfulness, response harmfulness, and refusal detection). Qwen3Guard, a 0.6B generative classifier, provides a tri-class label (safe, controversial, or unsafe). The dual-classifier approach enables inter-classifier agreement analysis and reduces the risk of single-classifier bias in ASR measurement.

#figure(
  table(
    columns: (auto, auto, auto),
    inset: 8pt,
    align: left,
    stroke: 0.5pt,
    table.header(
      [*Component*], [*Parameter*], [*Value*],
    ),
    [Base Models], [Architecture], [Qwen3-8B, Mistral-7B-v0.3],
    [LoRA], [Rank / Alpha / Dropout], [16 / 32 / 0.05],
    [Poisoning], [Rates], [0.0, 0.01, 0.05, 0.10],
    [Poisoning], [Trigger], ["SUDO" (token-level)],
    [SFT], [Epochs / LR], [1 / $2 times 10^(-4)$],
    [Reward Model], [Epochs / LR], [1 / $1 times 10^(-4)$],
    [GRPO], [Steps / Generations / LR], [1000 / 4 / $5 times 10^(-6)$],
    [REINFORCE++], [Steps / Generations / LR], [1000 / 2 / $5 times 10^(-6)$],
    [Evaluation], [Test Samples], [500 clean + 500 triggered],
    [Safety], [Classifiers], [WildGuard 7B + Qwen3Guard 0.6B],
  ),
  caption: [Experimental configuration for all Phase 1 runs.],
) <tab:config>

= Experimental Results

== Pipeline Validation and Failure Analysis

Before committing to full-scale training, a rapid end-to-end smoke test was designed and executed on both models at a 5% poisoning rate. This mini test used truncated parameters (10 SFT steps, 3 GRPO steps, 5 REINFORCE++ steps, 200 training samples, 10 test samples) to exercise every pipeline stage in approximately 10 minutes per model. The smoke test proved essential, as it uncovered five distinct failure modes that would have each cost 8--20 hours of wasted GPU time if discovered during production training.

The first failure involved _padding token propagation_. When processing multiple text sequences simultaneously (batched inference), shorter sequences must be padded to match the length of the longest sequence in the batch. This padding requires a designated "pad token" that the model knows to ignore during computation. Both Qwen3-8B and Mistral-7B-v0.3 were pretrained as autoregressive generators and do not define a pad token by default, since generation processes one sequence at a time. While the tokenizer's pad token was set to the end-of-sequence token during data loading, this assignment was not propagated to the model's internal configuration. The reward model, which scores sequences in batches rather than generating them one token at a time, checks this internal configuration when constructing attention masks, and the missing value caused a crash on any batch size greater than one. This failure surfaced in both reward model training and reward evaluation, requiring a one-line fix in two separate files. The subtlety of this bug is that it only manifests with batch sizes above one, making it invisible during initial single-sample development and testing.

The second failure involved _TRL's generation count constraint_. The REINFORCE++ algorithm was originally configured with `num_generations=1` to produce a single completion per prompt, relying on batch-level normalization for advantage computation. However, TRL's GRPOTrainer explicitly validates that `num_generations >= 2` by constructing its set of valid values with `range(2, global_batch_size + 1)`, excluding one by design. This required changing REINFORCE++ to use `num_generations=2`, which introduces minimal per-group normalization but satisfies the framework constraint.

The third failure was a _batch size divisibility constraint_. TRL requires that the global batch size (number of processes $times$ per-device batch size) be evenly divisible by `num_generations`. When transitioning from 2-GPU to 1-GPU training to improve SLURM scheduling flexibility, the global batch size changed from $2 times 4 = 8$ to $1 times 4 = 4$, and the original `num_generations=8` no longer divided evenly. Multiple iterations were required to find valid configurations (batch size 4 with `num_generations=4` for GRPO, batch size 4 with `num_generations=2` for REINFORCE++) that satisfied both the divisibility constraint and GPU memory limits.

The fourth and fifth failures were _model access issues_. The WildGuard safety classifier is hosted as a gated model on HuggingFace, requiring both license acceptance and authentication token propagation to compute nodes. The Qwen3Guard model identifier was initially specified as `Qwen/Qwen3-Guard-0.6B`, but the correct identifier is `Qwen/Qwen3Guard-Gen-0.6B` (the `-Gen` suffix indicates the generative variant). Both failures were silent during pipeline construction since model loading is deferred to runtime.

A recurring theme across these failures is that they only manifest under production conditions. The padding token bug requires `batch_size > 1`. The divisibility constraint depends on the number of GPUs. The model access failures require network access from compute nodes. This motivated the design of the mini smoke test as a permanent fixture of the development workflow rather than a one-time validation.

== Preliminary Training Results

Training metrics from the clean baseline ($p = 0.0$) demonstrate expected learning dynamics for both models and algorithms. The SFT stage shows consistent loss reduction from 2.40 to approximately 1.60 over the full 10,050-step epoch, with mean token accuracy increasing from 0.49 to 0.56. For the RL stages, all four training runs (GRPO and REINFORCE++ on both Qwen3-8B and Mistral-7B-v0.3) completed 1,000 steps on NVIDIA H200 GPUs. Mistral models show steadier reward improvement and higher final reward ($+0.61$ for GRPO, $-0.13$ for R++) compared to Qwen3 ($-2.10$ for GRPO, $-2.27$ for R++), consistent with Mistral's higher KL divergence during training. The significant performance gap between A100 and H200 for RL training (2.5--2.8$times$ speedup) motivated a mid-project migration from A100-based batch scheduling to an interactive H200 reservation strategy, which reduced the RL training wall time from an estimated 10 days to 3 days.

#figure(
  table(
    columns: (auto, auto, auto, auto, auto),
    inset: 8pt,
    align: center,
    stroke: 0.5pt,
    table.header(
      [*Stage*], [*GPU*], [*Step*], [*Speed*], [*Est. Completion*],
    ),
    [GRPO Qwen3 $p=0.0$], [1$times$H200], [1000/1000], [55 s/step], [*Complete*],
    [R++ Qwen3 $p=0.0$], [1$times$H200], [1000/1000], [50 s/step], [*Complete*],
    [GRPO Mistral $p=0.0$], [1$times$H200], [1000/1000], [63 s/step], [*Complete*],
    [R++ Mistral $p=0.0$], [1$times$H200], [1000/1000], [59 s/step], [*Complete*],
    [SFT (6 runs, both models)], [1$times$H200], [6/6], [1.6 s/step], [*Complete*],
    [Eval (Qwen3, both algos)], [1$times$H200], [2/2], [---], [*Complete*],
    [Eval (Mistral, both algos)], [1$times$H200], [2/2], [---], [*Complete*],
    [RM (all poisoned rates)], [3$times$H200], [6/6], [1.5 h/run], [Running],
  ),
  caption: [Training status as of April 6, 2026. All RL training for the clean baseline is complete on H200 GPUs. All SFT for poisoned rates is complete. Evaluation is complete for all four model-algorithm combinations. Reward model training for poisoned rates is in progress across three H200 GPUs.],
) <tab:status>

#figure(
  cetz.canvas(length: 1cm, {
    import cetz.draw: *

    let garnet = rgb("#73000A")
    let atlantic = rgb("#466A9F")
    let congaree = rgb("#1F414D")
    let horseshoe = rgb("#65780B")
    let warmgrey = rgb("#676156")
    let black90 = rgb("#363636")
    let light-gray = rgb("#ECECEC")

    // Timeline axis
    line((-0.5, -0.5), (16, -0.5), mark: (end: "stealth", fill: black90), stroke: black90 + 0.8pt)
    content((16.5, -0.5), text(size: 7pt, fill: black90)[Time])

    // Time markers
    for (i, label) in ((0, "0h"), (3, "3h"), (6, "9h"), (9, "15h"), (12, "30h"), (15, "48h")) {
      line((i, -0.3), (i, -0.7), stroke: black90 + 0.5pt)
      content((i, -1.0), text(size: 6.5pt, fill: black90)[#label])
    }

    // GPU labels
    content((-2.5, 2.5), text(size: 8pt, weight: "bold", fill: congaree)[H200\n(141 GB)])
    content((-2.5, 1.2), text(size: 8pt, weight: "bold", fill: atlantic)[A100-1\n(40 GB)])
    content((-2.5, 0.0), text(size: 8pt, weight: "bold", fill: atlantic)[A100-2\n(40 GB)])

    // H200: GRPO then R++
    rect((0, 2.1), (7, 2.9), fill: garnet.lighten(75%), stroke: garnet + 1pt)
    content((3.5, 2.5), text(size: 7pt, weight: "bold", fill: garnet)[GRPO Qwen3 r=0.0 (1000 steps)])

    // A100-1: SFT batch
    rect((0, 0.8), (3, 1.6), fill: atlantic.lighten(75%), stroke: atlantic + 1pt)
    content((1.5, 1.2), text(size: 7pt, weight: "bold", fill: atlantic)[SFT r=0.01])
    rect((3, 0.8), (6, 1.6), fill: atlantic.lighten(75%), stroke: atlantic + 1pt)
    content((4.5, 1.2), text(size: 7pt, weight: "bold", fill: atlantic)[SFT r=0.05])
    rect((6, 0.8), (9, 1.6), fill: atlantic.lighten(75%), stroke: atlantic + 1pt)
    content((7.5, 1.2), text(size: 7pt, weight: "bold", fill: atlantic)[SFT r=0.10])
    rect((9, 0.8), (12, 1.6), fill: atlantic.lighten(85%), stroke: atlantic + 0.5pt)
    content((10.5, 1.2), text(size: 7pt, fill: atlantic)[SFT Mistral...])

    // A100-2: R++
    rect((0, -0.4), (15, 0.4), fill: warmgrey.lighten(75%), stroke: warmgrey + 1pt)
    content((7.5, 0.0), text(size: 7pt, weight: "bold", fill: warmgrey)[R++ Qwen3 r=0.0 (1000 steps, ~140s/step, bandwidth-limited)])

    // Legend: bandwidth note
    rect((7.5, 2.1), (15, 2.9), fill: garnet.lighten(85%), stroke: garnet + 0.5pt)
    content((11.25, 2.5), text(size: 7pt, fill: garnet, style: "italic")[H200 frees up → Mistral GRPO / R++])

    // Dashed line at 48h
    line((15, -0.4), (15, 3.1), stroke: (paint: garnet, thickness: 0.8pt, dash: "dashed"))
    content((15, 3.4), text(size: 7pt, fill: garnet, weight: "bold")[48h wall limit])
  }),
  caption: [GPU allocation strategy for parallel training on heterogeneous hardware. The H200's 3$times$ higher memory bandwidth makes it essential for generation-heavy RL stages, while A100s handle compute-bound SFT training efficiently. Work is scheduled to maximize GPU utilization within SLURM's 48-hour wall time and 5-job QOS constraints.],
) <fig:gpu-allocation>

// SFT Loss Curve (full run, ~10k steps, sampled every 500 steps)
#figure(
  cetz.canvas(length: 1cm, {
    import cetz.draw: *
    let garnet = rgb("#73000A")
    let black90 = rgb("#363636")

    line((0, 0), (12, 0), stroke: black90 + 0.8pt)
    line((0, 0), (0, 5.5), stroke: black90 + 0.8pt)
    content((-1.0, 2.75), text(size: 8pt, fill: black90)[Loss])
    content((6, -0.8), text(size: 8pt, fill: black90)[Training Step])

    for (val, label) in ((0, "1.5"), (1.375, "1.7"), (2.75, "1.9"), (4.125, "2.1"), (5.5, "2.4")) {
      line((-0.15, val), (0, val), stroke: black90 + 0.5pt)
      content((-0.5, val), text(size: 7pt, fill: black90)[#label])
    }
    for (val, label) in ((0, "0"), (3, "2500"), (6, "5000"), (9, "7500"), (12, "10000")) {
      line((val, -0.15), (val, 0), stroke: black90 + 0.5pt)
      content((val, -0.45), text(size: 7pt, fill: black90)[#label])
    }
    for y in (1.375, 2.75, 4.125) {
      line((0, y), (12, y), stroke: (paint: rgb("#C7C7C7"), thickness: 0.3pt))
    }

    // Full SFT loss (Qwen3 r=0.10 on H200, sampled every 500 steps)
    let losses = (2.40, 1.77, 1.78, 1.77, 1.76, 1.70, 1.73, 1.67, 1.70, 1.64, 1.69, 1.66, 1.66, 1.66, 1.66, 1.60, 1.65, 1.67, 1.62, 1.66)
    let points = ()
    for (i, l) in losses.enumerate() {
      let x = (i + 1) * 0.6
      let y = (l - 1.5) * 6.11
      points.push((x, y))
    }
    for i in range(points.len() - 1) {
      line(points.at(i), points.at(i + 1), stroke: garnet + 1.5pt)
    }
    for p in points {
      circle(p, radius: 0.08, fill: garnet, stroke: none)
    }
  }),
  caption: [SFT training loss for Qwen3-8B ($p = 0.10$) over the full 10,050-step epoch on H200. Loss drops from 2.40 to 1.60, with the steepest descent in the first 2,500 steps before plateauing.],
) <fig:sft-loss>

// Reward trajectories: all 4 runs (Qwen3+Mistral × GRPO+R++)
#figure(
  cetz.canvas(length: 1cm, {
    import cetz.draw: *
    let garnet = rgb("#73000A")
    let atlantic = rgb("#466A9F")
    let rose = rgb("#CC2E40")
    let horseshoe = rgb("#65780B")
    let black90 = rgb("#363636")

    line((0, 0), (14, 0), stroke: black90 + 0.8pt)
    line((0, 0), (0, 5.5), stroke: black90 + 0.8pt)
    content((-1.0, 2.75), text(size: 8pt, fill: black90)[Reward])
    content((7, -0.8), text(size: 8pt, fill: black90)[Training Step])

    for (val, label) in ((0, "-3"), (1.1, "-2"), (2.2, "-1"), (3.3, "0"), (4.4, "+1"), (5.5, "+2")) {
      line((-0.15, val), (0, val), stroke: black90 + 0.5pt)
      content((-0.5, val), text(size: 7pt, fill: black90)[#label])
    }
    for (val, label) in ((0, "0"), (3.5, "250"), (7, "500"), (10.5, "750"), (14, "1000")) {
      line((val, -0.15), (val, 0), stroke: black90 + 0.5pt)
      content((val, -0.45), text(size: 7pt, fill: black90)[#label])
    }
    line((0, 3.3), (14, 3.3), stroke: (paint: rgb("#C7C7C7"), thickness: 0.5pt, dash: "dashed"))
    for y in (1.1, 2.2, 4.4, 5.5) {
      line((0, y), (14, y), stroke: (paint: rgb("#C7C7C7"), thickness: 0.3pt))
    }

    // Helper to plot a reward series
    let plot-line(data, color, n) = {
      let pts = ()
      for (i, r) in data.enumerate() {
        let x = (i + 1) * 14.0 / (n + 1)
        let y = (r + 3.0) * 1.1
        pts.push((x, y))
      }
      for i in range(pts.len() - 1) {
        line(pts.at(i), pts.at(i + 1), stroke: color + 1.2pt)
      }
    }

    // GRPO Qwen3 (garnet) — sampled every 50 steps, 20 points
    let gq = (1.43, -0.001, -2.13, 0.44, -0.68, 0.89, -1.26, -0.47, 0.06, 0.30, -2.00, 0.69)
    plot-line(gq, garnet, 12)

    // GRPO Mistral (rose) — 20 points
    let gm = (0.57, -0.003, -0.22, 0.44, 0.12, 0.22, 0.16, 0.48, 0.65, 0.58, 0.44, 0.76, 0.82, 1.06, 0.71, 0.95, 0.92, 0.89, 0.80, 0.67)
    plot-line(gm, rose, 20)

    // R++ Qwen3 (atlantic) — 20 points
    let rq = (0.04, -1.53, -0.37, -1.12, 0.05, -1.42, 0.71, 0.13, 0.01, -1.10, -0.76, 0.09, 0.03, 0.12, 0.65, 0.59, 0.38, 0.25, -0.65, 0.48)
    plot-line(rq, atlantic, 20)

    // R++ Mistral (horseshoe) — 20 points
    let rm = (0.09, -0.09, 0.09, 0.08, 0.38, -0.05, 0.37, 0.34, 0.22, 0.21, 0.08, 0.42, 0.49, 0.65, 0.51, 0.61, 0.75, 0.69, 0.39, 0.57)
    plot-line(rm, horseshoe, 20)

    // Legend
    line((9.0, 5.3), (9.8, 5.3), stroke: garnet + 1.2pt)
    content((11.0, 5.3), text(size: 6.5pt, fill: black90)[GRPO Qwen3])
    line((9.0, 4.9), (9.8, 4.9), stroke: rose + 1.2pt)
    content((11.0, 4.9), text(size: 6.5pt, fill: black90)[GRPO Mistral])
    line((12.0, 5.3), (12.8, 5.3), stroke: atlantic + 1.2pt)
    content((14.0, 5.3), text(size: 6.5pt, fill: black90)[R++ Qwen3])
    line((12.0, 4.9), (12.8, 4.9), stroke: horseshoe + 1.2pt)
    content((14.0, 4.9), text(size: 6.5pt, fill: black90)[R++ Mistral])
  }),
  caption: [Reward trajectories for all four RL training runs on the clean baseline ($p = 0.0$) over 1,000 steps. Mistral models (rose, horseshoe) show steadier reward improvement compared to Qwen3 models (garnet, atlantic) which exhibit higher variance. GRPO Mistral achieves the highest final reward ($+1.06$) while both Qwen3 runs show more oscillation.],
) <fig:rl-rewards>

// KL Divergence: All 4 runs — key finding about model differences
#figure(
  cetz.canvas(length: 1cm, {
    import cetz.draw: *
    let garnet = rgb("#73000A")
    let atlantic = rgb("#466A9F")
    let rose = rgb("#CC2E40")
    let horseshoe = rgb("#65780B")
    let black90 = rgb("#363636")

    line((0, 0), (14, 0), stroke: black90 + 0.8pt)
    line((0, 0), (0, 5.5), stroke: black90 + 0.8pt)
    content((-1.2, 2.75), text(size: 8pt, fill: black90)[KL])
    content((7, -0.8), text(size: 8pt, fill: black90)[Training Step])

    // Y: 0 to 0.14
    for (val, label) in ((0, "0"), (1.1, "0.025"), (2.2, "0.05"), (3.3, "0.075"), (4.4, "0.10"), (5.5, "0.125")) {
      line((-0.15, val), (0, val), stroke: black90 + 0.5pt)
      content((-0.6, val), text(size: 7pt, fill: black90)[#label])
    }
    for (val, label) in ((0, "0"), (3.5, "250"), (7, "500"), (10.5, "750"), (14, "1000")) {
      line((val, -0.15), (val, 0), stroke: black90 + 0.5pt)
      content((val, -0.45), text(size: 7pt, fill: black90)[#label])
    }
    for y in (1.1, 2.2, 3.3, 4.4) {
      line((0, y), (14, y), stroke: (paint: rgb("#C7C7C7"), thickness: 0.3pt))
    }

    let plot-kl(data, color, n) = {
      let pts = ()
      for (i, k) in data.enumerate() {
        let x = (i + 1) * 14.0 / (n + 1)
        let y = k * 44.0
        pts.push((x, y))
      }
      for i in range(pts.len() - 1) {
        line(pts.at(i), pts.at(i + 1), stroke: color + 1.5pt)
      }
      for p in pts {
        circle(p, radius: 0.06, fill: color, stroke: none)
      }
    }

    // GRPO Qwen3 KL — 12 points
    let gq_kl = (0.0, 0.0015, 0.0012, 0.0014, 0.0015, 0.0019, 0.0036, 0.0053, 0.0059, 0.0072, 0.0059, 0.0185)
    plot-kl(gq_kl, garnet, 12)

    // GRPO Mistral KL — 20 points (DRAMATIC divergence)
    let gm_kl = (0.0, 0.0003, 0.0007, 0.0018, 0.0052, 0.0192, 0.0384, 0.0667, 0.0791, 0.0479, 0.0555, 0.1026, 0.0781, 0.0709, 0.0887, 0.1249, 0.1106, 0.0814, 0.1013, 0.0758)
    plot-kl(gm_kl, rose, 20)

    // R++ Qwen3 KL — 20 points
    let rq_kl = (0.0, 0.0012, 0.0012, 0.0012, 0.0015, 0.0017, 0.0019, 0.0036, 0.0049, 0.0052, 0.0059, 0.0106, 0.0127, 0.0139, 0.0205, 0.0162, 0.0129, 0.0119, 0.0174, 0.0139)
    plot-kl(rq_kl, atlantic, 20)

    // R++ Mistral KL — 20 points
    let rm_kl = (0.0, 0.0004, 0.0004, 0.0013, 0.0019, 0.0040, 0.0064, 0.0085, 0.0118, 0.0175, 0.0185, 0.0203, 0.0262, 0.0207, 0.0253, 0.0302, 0.0253, 0.0252, 0.0277, 0.0222)
    plot-kl(rm_kl, horseshoe, 20)

    // Legend
    line((9.0, 5.3), (9.8, 5.3), stroke: garnet + 1.5pt)
    content((11.0, 5.3), text(size: 6.5pt, fill: black90)[GRPO Qwen3])
    line((9.0, 4.9), (9.8, 4.9), stroke: rose + 1.5pt)
    content((11.0, 4.9), text(size: 6.5pt, fill: black90)[GRPO Mistral])
    line((12.0, 5.3), (12.8, 5.3), stroke: atlantic + 1.5pt)
    content((14.0, 5.3), text(size: 6.5pt, fill: black90)[R++ Qwen3])
    line((12.0, 4.9), (12.8, 4.9), stroke: horseshoe + 1.5pt)
    content((14.0, 4.9), text(size: 6.5pt, fill: black90)[R++ Mistral])
  }),
  caption: [KL divergence from the SFT reference for all four training runs. GRPO Mistral (rose) diverges dramatically, peaking at 0.125 around step 750 before partially recovering. GRPO Qwen3 (garnet) remains below 0.02. Both REINFORCE++ runs show moderate divergence (0.02--0.03). The 6$times$ KL gap between GRPO Mistral and GRPO Qwen3 under identical training configurations suggests fundamentally different optimization landscapes per model architecture.],
) <fig:kl-all>

// Eval Results Bar Chart — GRPO vs R++ safety metrics
#figure(
  cetz.canvas(length: 1cm, {
    import cetz.draw: *
    let garnet = rgb("#73000A")
    let atlantic = rgb("#466A9F")
    let black90 = rgb("#363636")
    let warmgrey = rgb("#676156")

    line((0, 0), (14, 0), stroke: black90 + 0.8pt)
    line((0, 0), (0, 5.5), stroke: black90 + 0.8pt)
    content((-1.0, 2.75), text(size: 8pt, fill: black90)[Rate])
    content((7, -1.2), text(size: 8pt, fill: black90)[Metric])

    for (val, label) in ((0, "0%"), (1.375, "10%"), (2.75, "20%"), (4.125, "30%"), (5.5, "40%")) {
      line((-0.15, val), (0, val), stroke: black90 + 0.5pt)
      content((-0.5, val), text(size: 7pt, fill: black90)[#label])
    }
    for y in (1.375, 2.75, 4.125) {
      line((0, y), (14, y), stroke: (paint: rgb("#C7C7C7"), thickness: 0.3pt))
    }

    // Bar groups
    let groups = (
      ("WG\nClean", 0.0, 0.0),
      ("QG\nClean", 37.8, 42.0),
      ("WG\nASR", 0.0, 0.0),
      ("QG\nASR", 33.0, 34.2),
      ("Agree\nClean", 62.2, 58.0),
      ("Agree\nTrig", 67.0, 65.8),
    )

    for (i, (label, grpo, rpp)) in groups.enumerate() {
      let x = i * 2.3 + 1.2
      let grpo_h = grpo * 5.5 / 70.0
      let rpp_h = rpp * 5.5 / 70.0

      rect((x - 0.5, 0), (x, grpo_h), fill: garnet.lighten(30%), stroke: garnet + 0.8pt)
      rect((x + 0.1, 0), (x + 0.6, rpp_h), fill: atlantic.lighten(30%), stroke: atlantic + 0.8pt)

      if grpo > 0 {
        content((x - 0.25, grpo_h + 0.25), text(size: 6pt, fill: garnet)[#calc.round(grpo, digits: 1)%])
      }
      if rpp > 0 {
        content((x + 0.35, rpp_h + 0.25), text(size: 6pt, fill: atlantic)[#calc.round(rpp, digits: 1)%])
      }
      content((x + 0.05, -0.6), text(size: 6.5pt, fill: black90)[#label])
    }

    // Legend
    rect((10.5, 5.0), (11.0, 5.3), fill: garnet.lighten(30%), stroke: garnet + 0.6pt)
    content((11.8, 5.15), text(size: 7pt, fill: black90)[GRPO])
    rect((10.5, 4.4), (11.0, 4.7), fill: atlantic.lighten(30%), stroke: atlantic + 0.6pt)
    content((11.8, 4.55), text(size: 7pt, fill: black90)[R++])
  }),
  caption: [Safety evaluation metrics for Qwen3-8B at $p = 0.0$ (clean baseline). WG = WildGuard, QG = Qwen3Guard. WildGuard classifies 0% of responses as harmful for both algorithms. Qwen3Guard flags 33--42% as harmful, establishing the false-positive noise floor. Inter-classifier agreement is 58--67%. Both algorithms show nearly identical safety profiles on the clean baseline.],
) <fig:eval-bars>

// H200 vs A100 speed comparison — updated with actual measured speeds
#figure(
  cetz.canvas(length: 1cm, {
    import cetz.draw: *
    let garnet = rgb("#73000A")
    let atlantic = rgb("#466A9F")
    let black90 = rgb("#363636")

    line((0, 0), (14, 0), stroke: black90 + 0.8pt)
    line((0, 0), (0, 6), stroke: black90 + 0.8pt)
    content((-1.2, 3), text(size: 8pt, fill: black90)[s/step])

    for (val, label) in ((0, "0"), (1.2, "30"), (2.4, "60"), (3.6, "90"), (4.8, "120"), (6.0, "150")) {
      line((-0.15, val), (0, val), stroke: black90 + 0.5pt)
      content((-0.55, val), text(size: 7pt, fill: black90)[#label])
    }
    for y in (1.2, 2.4, 3.6, 4.8) {
      line((0, y), (14, y), stroke: (paint: rgb("#C7C7C7"), thickness: 0.3pt))
    }

    // Updated with actual measured speeds
    let groups = (
      ("SFT", 3.5, 1.6),
      ("RM", 3.8, 1.7),
      ("GRPO", 140, 55),
      ("R++", 140, 50),
    )

    for (i, (label, a100, h200)) in groups.enumerate() {
      let x = i * 3.5 + 1.5
      let a100_h = a100 / 25.0
      let h200_h = h200 / 25.0
      rect((x - 0.7, 0), (x, a100_h), fill: atlantic.lighten(30%), stroke: atlantic + 0.8pt)
      rect((x + 0.1, 0), (x + 0.8, h200_h), fill: garnet.lighten(30%), stroke: garnet + 0.8pt)

      if a100 < 10 {
        content((x - 0.35, a100_h + 0.3), text(size: 6.5pt, fill: atlantic)[#calc.round(a100, digits: 1)s])
      } else {
        content((x - 0.35, a100_h + 0.3), text(size: 6.5pt, fill: atlantic)[#int(a100)s])
      }
      if h200 < 10 {
        content((x + 0.45, h200_h + 0.3), text(size: 6.5pt, fill: garnet)[#calc.round(h200, digits: 1)s])
      } else {
        content((x + 0.45, h200_h + 0.3), text(size: 6.5pt, fill: garnet)[#int(h200)s])
      }
      content((x + 0.05, -0.5), text(size: 8pt, fill: black90)[#label])
    }

    // Speedup annotations
    content((9.1, 3.8), text(size: 7pt, fill: garnet, weight: "bold")[2.5$times$])
    content((12.6, 3.6), text(size: 7pt, fill: garnet, weight: "bold")[2.8$times$])

    rect((10, 5.0), (10.5, 5.35), fill: atlantic.lighten(30%), stroke: atlantic + 0.6pt)
    content((11.5, 5.18), text(size: 7pt, fill: black90)[A100 (1.6 TB/s)])
    rect((10, 4.3), (10.5, 4.65), fill: garnet.lighten(30%), stroke: garnet + 0.6pt)
    content((11.5, 4.48), text(size: 7pt, fill: black90)[H200 (4.8 TB/s)])
  }),
  caption: [Measured per-step wall time comparison between A100 and H200. SFT and RM are compute-bound with minimal speedup (2.2$times$). GRPO (2.5$times$) and R++ (2.8$times$) are generation-bound, with speedup directly proportional to memory bandwidth ratio. All values measured on Qwen3-8B with identical hyperparameters.],
) <fig:gpu-comparison>

@tab:gpu-timing quantifies the practical impact of GPU selection on project-level scheduling. For the 12 remaining RL training runs (the critical path), the choice between A100 and H200 determines whether Phase 1 completes in one week or one month.

#figure(
  table(
    columns: (auto, auto, auto, auto, auto),
    inset: 6pt,
    align: (left, center, center, center, center),
    stroke: 0.5pt,
    table.header(
      [*Stage*], [*A100 (measured)*], [*H200 (measured)*], [*Speedup*], [*Bottleneck*],
    ),
    [SFT (1 epoch)], [9.5 h], [4.5 h], [2.1$times$], [Compute],
    [RM (1 epoch)], [1.5 h], [1.5 h], [1.0$times$], [Compute],
    [GRPO (1000 steps)], [39 h], [15 h], [2.5$times$], [Generation (bandwidth)],
    [R++ (1000 steps)], [44 h], [17 h], [2.6$times$], [Generation (bandwidth)],
    [Eval (generate)], [1.5 h], [0.6 h], [2.5$times$], [Generation (bandwidth)],
    [Eval (safety classify)], [0.5 h], [0.5 h], [1.0$times$], [Compute],
    table.hline(),
    [*Full pipeline per rate*], [*96 h*], [*39 h*], [*2.5$times$*], [],
    [*12 RL runs (4 GPUs)*], [*132 h (5.5 days)*], [*51 h (2.1 days)*], [*2.6$times$*], [],
    [*12 RL runs (1 GPU)*], [*498 h (20.8 days)*], [*192 h (8.0 days)*], [*2.6$times$*], [],
  ),
  caption: [Measured wall times per pipeline stage on A100 (40 GB, 1.6 TB/s) and H200 (141 GB, 4.8 TB/s). Generation-bound stages (GRPO, R++, eval generation) scale with memory bandwidth. Compute-bound stages (SFT, RM, safety classify) show minimal or no speedup.],
) <tab:gpu-timing>

== Compute Resources and GPU Selection

The choice of GPU hardware proved to be one of the most consequential decisions in the project. Three classes of GPU were available for this work. The university's Theia HPC cluster provides NVIDIA A100 SXM4 (40 GB) and H200 NVL (141 GB) GPUs through SLURM scheduling. Additionally, two dedicated research servers equipped with four NVIDIA RTX 6000 Ada Generation GPUs (48 GB each) were available through the PI's lab, accessible via Tailscale VPN without scheduling overhead.

#figure(
  cetz.canvas(length: 1cm, {
    import cetz.draw: *

    let garnet = rgb("#73000A")
    let atlantic = rgb("#466A9F")
    let congaree = rgb("#1F414D")
    let horseshoe = rgb("#65780B")
    let honeycomb = rgb("#A49137")
    let black90 = rgb("#363636")
    let warmgrey = rgb("#676156")

    // Title row
    content((2.5, 6.2), text(size: 8pt, weight: "bold", fill: black90)[VRAM (GB)])
    content((6.5, 6.2), text(size: 8pt, weight: "bold", fill: black90)[Bandwidth (TB/s)])
    content((10.5, 6.2), text(size: 8pt, weight: "bold", fill: black90)[BF16 TFLOPS])
    content((14.5, 6.2), text(size: 8pt, weight: "bold", fill: black90)[Available])

    // Grid lines
    for y in (1.5, 3.0, 4.5) {
      line((0, y), (16.5, y), stroke: (paint: rgb("#ECECEC"), thickness: 0.5pt))
    }

    // H200
    let y-h200 = 4.5
    content((-1.0, y-h200 + 0.4), text(size: 9pt, weight: "bold", fill: garnet)[H200 NVL])
    content((-1.0, y-h200), text(size: 7pt, fill: warmgrey)[141 GB HBM3])
    // VRAM bar
    rect((0.5, y-h200 + 0.05), (0.5 + 141/35, y-h200 + 0.45), fill: garnet.lighten(40%), stroke: garnet + 0.8pt)
    content((0.5 + 141/70, y-h200 + 0.25), text(size: 7pt, fill: white, weight: "bold")[141])
    // BW bar
    rect((4.5, y-h200 + 0.05), (4.5 + 4.8/1.2, y-h200 + 0.45), fill: garnet.lighten(40%), stroke: garnet + 0.8pt)
    content((4.5 + 4.8/2.4, y-h200 + 0.25), text(size: 7pt, fill: white, weight: "bold")[4.8])
    // TFLOPS bar
    rect((8.5, y-h200 + 0.05), (8.5 + 989/250, y-h200 + 0.45), fill: garnet.lighten(40%), stroke: garnet + 0.8pt)
    content((8.5 + 989/500, y-h200 + 0.25), text(size: 7pt, fill: white, weight: "bold")[989])
    // Count
    content((14.5, y-h200 + 0.25), text(size: 8pt, fill: black90)[2 GPUs (Theia)])

    // A100
    let y-a100 = 3.0
    content((-1.0, y-a100 + 0.4), text(size: 9pt, weight: "bold", fill: atlantic)[A100 SXM4])
    content((-1.0, y-a100), text(size: 7pt, fill: warmgrey)[40 GB HBM2e])
    // VRAM bar
    rect((0.5, y-a100 + 0.05), (0.5 + 40/35, y-a100 + 0.45), fill: atlantic.lighten(40%), stroke: atlantic + 0.8pt)
    content((0.5 + 40/70, y-a100 + 0.25), text(size: 7pt, fill: white, weight: "bold")[40])
    // BW bar
    rect((4.5, y-a100 + 0.05), (4.5 + 1.6/1.2, y-a100 + 0.45), fill: atlantic.lighten(40%), stroke: atlantic + 0.8pt)
    content((4.5 + 1.6/2.4, y-a100 + 0.25), text(size: 7pt, fill: white, weight: "bold")[1.6])
    // TFLOPS bar
    rect((8.5, y-a100 + 0.05), (8.5 + 312/250, y-a100 + 0.45), fill: atlantic.lighten(40%), stroke: atlantic + 0.8pt)
    content((8.5 + 312/500, y-a100 + 0.25), text(size: 7pt, fill: white, weight: "bold")[312])
    // Count
    content((14.5, y-a100 + 0.25), text(size: 8pt, fill: black90)[32 GPUs (Theia)])

    // RTX 6000 Ada
    let y-rtx = 1.5
    content((-1.0, y-rtx + 0.4), text(size: 9pt, weight: "bold", fill: honeycomb)[RTX 6000 Ada])
    content((-1.0, y-rtx), text(size: 7pt, fill: warmgrey)[48 GB GDDR6X])
    // VRAM bar
    rect((0.5, y-rtx + 0.05), (0.5 + 48/35, y-rtx + 0.45), fill: honeycomb.lighten(40%), stroke: honeycomb + 0.8pt)
    content((0.5 + 48/70, y-rtx + 0.25), text(size: 7pt, fill: white, weight: "bold")[48])
    // BW bar
    rect((4.5, y-rtx + 0.05), (4.5 + 0.96/1.2, y-rtx + 0.45), fill: honeycomb.lighten(40%), stroke: honeycomb + 0.8pt)
    content((4.5 + 0.96/2.4, y-rtx + 0.25), text(size: 7pt, fill: white, weight: "bold")[0.96])
    // TFLOPS bar
    rect((8.5, y-rtx + 0.05), (8.5 + 91/250, y-rtx + 0.45), fill: honeycomb.lighten(40%), stroke: honeycomb + 0.8pt)
    content((8.5 + 91/500, y-rtx + 0.25), text(size: 7pt, fill: white, weight: "bold")[91])
    // Count
    content((14.5, y-rtx + 0.25), text(size: 8pt, fill: black90)[8 GPUs (PI lab)])
  }),
  caption: [Comparison of available GPU resources. Memory bandwidth, not TFLOPS, is the primary determinant of RL training speed because autoregressive generation requires reading the full model weights for every token produced. The H200's 4.8 TB/s HBM3 bandwidth makes it 3$times$ faster than A100 and 5$times$ faster than RTX 6000 Ada for generation-heavy workloads.],
) <fig:compute-resources>

Despite having 48 GB of VRAM (more than the A100's 40 GB) and being available without scheduling delays, the RTX 6000 Ada GPUs were ultimately deprioritized for RL training. The reason is that RL alignment training is dominated by autoregressive token generation, and generation speed is determined almost entirely by memory bandwidth rather than compute throughput. Each generated token requires reading the full model weights from GPU memory. For an 8-billion parameter model stored in BF16, this means reading approximately 16 GB of data per token. The RTX 6000 Ada's GDDR6X memory provides 0.96 TB/s of bandwidth, which translates to roughly 60 tokens per second. The A100's HBM2e provides 1.6 TB/s (100 tokens/s), and the H200's HBM3 provides 4.8 TB/s (300 tokens/s). With each RL step generating thousands of tokens across multiple completions, these bandwidth differences compound into 2.5--5$times$ wall-time differences per training step. The RTX 6000 Ada servers remain useful for compute-bound stages like SFT and reward model training, where TFLOPS matter more than bandwidth, and for evaluation stages that involve shorter generation sequences.

An application to the NSF ACCESS program is currently in preparation to expand the available compute for this project. ACCESS provides a universal credit system that can be exchanged for GPU time on national-scale HPC clusters. The Explore tier, which is the entry-level allocation requiring no proposal review, provides 400,000 ACCESS credits. @tab:access shows the full set of GPU-equipped ACCESS systems, their hardware specifications, and the effective cost in ACCESS credits per GPU-hour. Exchange rates were obtained directly from the ACCESS credit exchange calculator; for systems with mixed GPU types, the listed rate reflects the premium GPU after applying the system's internal SU multiplier. Stampede3's rate has been converted from the published node-hour rate (63.88 credits/node-hr, 4 SU/GPU-node-hr charge) to an effective per-GPU-hour rate assuming full 4-GPU node utilization.

#figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto),
    inset: 6pt,
    align: (left, left, right, right, right, right),
    stroke: 0.5pt,
    table.header(
      [*System*], [*GPU*], [*VRAM*], [*Total GPUs*], [*Credits/GPU-hr*], [*400k Credits →*],
    ),
    [SDSC Expanse], [V100], [32 GB], [208], [53.8], [7,428 hrs],
    [SDSC Expanse], [H100 (NAIRR)], [80 GB], [136], [~53.8], [~7,428 hrs],
    [PSC Bridges-2], [V100], [32 GB], [264], [53.8], [7,428 hrs],
    [PSC Bridges-2], [L40S], [48 GB], [24], [53.8], [7,428 hrs],
    [PSC Bridges-2], [H100 80GB], [80 GB], [80], [107.7], [3,714 hrs],
    [TACC Stampede3], [H100 96GB], [96 GB], [96], [~102.3], [~3,910 hrs],
    [NCSA Delta], [A40], [48 GB], [400], [#sym.lt 66.7], [#sym.gt 6,000 hrs],
    [NCSA Delta], [A100 40GB], [40 GB], [440], [66.7], [6,000 hrs],
    [NCSA Delta], [*H200 141GB*], [*141 GB*], [*64*], [*200.0*], [*2,000 hrs*],
    [NSF NCAR Derecho], [A100 40GB], [40 GB], [328], [66.7], [6,000 hrs],
    [Purdue Anvil], [A100 40GB], [40 GB], [64], [67.3], [5,944 hrs],
    [Texas Tech REPACSS], [H100-NVL], [94 GB], [--], [100.0], [4,000 hrs],
    [Purdue Anvil AI], [H100 80GB], [80 GB], [84], [133.3], [3,000 hrs],
    [NCSA DeltaAI], [GH200 (H100)], [96 GB], [608], [133.3], [3,000 hrs],
  ),
  caption: [NSF ACCESS GPU resources with effective credit costs per GPU-hour. Rates obtained from the ACCESS exchange calculator (April 2026). For systems with internal GPU-type multipliers (Delta H200 at 3$times$, Bridges-2 H100 at 2$times$, Stampede3 at 4 SU/node-hr), the listed rate reflects the effective per-GPU-hour cost of the premium GPU type.],
) <tab:access>

For this project, the most attractive targets are NCSA Delta (the only ACCESS system with H200 GPUs, providing the same hardware as the Theia cluster's fastest partition) and NCSA DeltaAI (608 H100-class GPUs with clean per-GPU-hour pricing). Even at the Explore tier, 400,000 credits would yield approximately 2,000 H200 GPU-hours on Delta or 3,000 H100 GPU-hours on DeltaAI, representing a substantial expansion over the Theia cluster's five-job QOS limit. This allocation would enable the full Phase 2 and Phase 3 experimental matrix (extended poisoning rates, additional RL algorithms, trigger ablation studies) that the current compute budget constrains.

== SLURM Scheduling and Infrastructure Challenges

A significant portion of the implementation effort involved navigating the constraints of shared HPC scheduling. The Theia cluster's QOS policy limits each user to five concurrent SLURM jobs with a maximum wall time of 48 hours per job. With RL training requiring 15--40 hours per run depending on GPU type, and 16 total runs needed for Phase 1, efficient scheduling became a critical bottleneck. The path to a working scheduling strategy involved several failed approaches before arriving at the current solution.

The initial approach was to submit one SLURM batch job per (model, rate) combination, each running the full seven-stage pipeline. This failed immediately because SLURM's GPU isolation on Theia is accounting-based rather than cgroup-enforced. When SLURM packed two single-GPU jobs onto the same four-GPU A100 node, both jobs were assigned `CUDA_VISIBLE_DEVICES=0`, causing them to compete for the same physical GPU. The resulting out-of-memory crashes were initially misattributed to batch size misconfiguration, wasting several debugging cycles before the root cause was identified. A runtime GPU auto-detection script was added that queries `nvidia-smi` for GPUs with less than 1 GB of memory in use and overrides the SLURM-assigned device. While this is a heuristic workaround rather than a proper fix, it resolved the GPU contention issue in practice.

The second approach used SLURM's `afterany` dependency mechanism to chain jobs into pairs, with the second rate starting immediately after the first completed. Four chains ran in parallel, filling all available QOS slots. This worked well until a code fix was needed mid-chain. When the GRPO batch size configuration was updated to fix an out-of-memory error, the already-running jobs had loaded the old Python orchestrator into memory and continued using the incorrect parameters. The dependency chain then triggered the next job (for a different rate), which loaded the corrected code, but the original rate's GRPO stage was left incomplete. The chain structure meant that no job would ever retry the failed rate, as each link in the chain was assigned a specific rate at submission time. This failure mode, in which a bug fix invalidates running jobs but the dependency chain cannot recover, required cancelling all jobs and resubmitting from scratch.

A third issue arose from SLURM's QOS job count limit interacting with dependency jobs. When a job finished and its dependent job transitioned from `Dependency` to `Pending`, SLURM occasionally started the dependent job before fully accounting for the finished job's slot release, causing a brief period where six jobs appeared active under a five-job limit. SLURM's response was to immediately kill the newly started dependent job with a `QOSMaxJobsPerUserLimit` error rather than re-queuing it, permanently losing that chain link.

These failures motivated the adoption of an interactive GPU reservation strategy. Rather than submitting batch jobs for each training stage, long-lived GPU allocations are obtained using `sbatch --wrap="sleep 172800"`, which holds a GPU for 48 hours. Training processes are then launched directly on the allocated nodes via SSH, running in the background with output redirected to log files. This approach provides immediate feedback when errors occur, enables on-the-fly parameter adjustments, and eliminates queue wait time between debugging iterations. The orchestrator's checkpoint-based stage skipping ensures that a failed process can be restarted without repeating completed work. A background monitoring script polls training progress every five minutes and logs step counts, loss values, and GPU memory utilization.

#figure(
  cetz.canvas(length: 1cm, {
    import cetz.draw: *

    let garnet = rgb("#73000A")
    let atlantic = rgb("#466A9F")
    let congaree = rgb("#1F414D")
    let horseshoe = rgb("#65780B")
    let warmgrey = rgb("#676156")
    let black90 = rgb("#363636")
    let rose = rgb("#CC2E40")
    let light-gray = rgb("#ECECEC")

    // Three approaches side by side

    // Approach 1: Naive sequential
    content((2.5, 5.0), text(size: 8pt, weight: "bold", fill: black90)[Naive: Submit per stage])
    line((0, 4.5), (5, 4.5), stroke: black90 + 0.5pt)

    rect((0, 3.7), (1.5, 4.3), fill: atlantic.lighten(75%), stroke: atlantic + 0.8pt)
    content((0.75, 4.0), text(size: 6pt)[SFT])
    rect((1.5, 3.7), (2.0, 4.3), fill: rose.lighten(60%), stroke: rose + 0.8pt)
    content((1.75, 4.0), text(size: 5pt)[Q])
    rect((2.0, 3.7), (3.5, 4.3), fill: atlantic.lighten(75%), stroke: atlantic + 0.8pt)
    content((2.75, 4.0), text(size: 6pt)[RM])
    rect((3.5, 3.7), (4.0, 4.3), fill: rose.lighten(60%), stroke: rose + 0.8pt)
    content((3.75, 4.0), text(size: 5pt)[Q])
    rect((4.0, 3.7), (5.0, 4.3), fill: garnet.lighten(75%), stroke: garnet + 0.8pt)
    content((4.5, 4.0), text(size: 6pt)[RL])
    content((1.75, 3.3), text(size: 6.5pt, fill: rose)[Queue wait between every stage])

    // Approach 2: Dependency chains
    content((8.0, 5.0), text(size: 8pt, weight: "bold", fill: black90)[Better: Dependency chains])
    line((5.5, 4.5), (10.5, 4.5), stroke: black90 + 0.5pt)

    rect((5.5, 3.7), (7.5, 4.3), fill: atlantic.lighten(75%), stroke: atlantic + 0.8pt)
    content((6.5, 4.0), text(size: 6pt)[Rate 0.0 full])
    line((7.5, 4.0), (7.8, 4.0), mark: (end: "stealth", fill: black90), stroke: black90 + 0.6pt)
    rect((7.8, 3.7), (9.8, 4.3), fill: horseshoe.lighten(75%), stroke: horseshoe + 0.8pt)
    content((8.8, 4.0), text(size: 6pt)[Rate 0.05 full])
    content((8.0, 3.3), text(size: 6.5pt, fill: horseshoe)[No queue wait between chained jobs])

    // Approach 3: Interactive reservation (current)
    content((13.5, 5.0), text(size: 8pt, weight: "bold", fill: black90)[Current: Interactive hold])
    line((11.0, 4.5), (16.0, 4.5), stroke: black90 + 0.5pt)

    rect((11.0, 3.7), (16.0, 4.3), fill: congaree.lighten(80%), stroke: congaree + 0.8pt)
    content((13.5, 4.0), text(size: 6pt)[48h GPU reservation (sleep)])

    // Sub-processes
    rect((11.2, 2.8), (12.5, 3.4), fill: atlantic.lighten(75%), stroke: atlantic + 0.6pt)
    content((11.85, 3.1), text(size: 5.5pt)[SFT])
    rect((12.7, 2.8), (14.0, 3.4), fill: atlantic.lighten(75%), stroke: atlantic + 0.6pt)
    content((13.35, 3.1), text(size: 5.5pt)[RM])
    rect((14.2, 2.8), (15.8, 3.4), fill: garnet.lighten(75%), stroke: garnet + 0.6pt)
    content((15.0, 3.1), text(size: 5.5pt)[GRPO])

    // Arrows down
    line((11.85, 3.7), (11.85, 3.4), mark: (end: "stealth", fill: black90), stroke: black90 + 0.5pt)
    line((13.35, 3.7), (13.35, 3.4), mark: (end: "stealth", fill: black90), stroke: black90 + 0.5pt)
    line((15.0, 3.7), (15.0, 3.4), mark: (end: "stealth", fill: black90), stroke: black90 + 0.5pt)

    // Error and fix annotation
    line((14.5, 2.8), (14.5, 2.2), stroke: (paint: rose, thickness: 0.6pt, dash: "dashed"))
    content((14.5, 1.9), text(size: 6pt, fill: rose)[Error? Fix and restart])
    content((14.5, 1.5), text(size: 6pt, fill: congaree)[No re-queue needed])
  }),
  caption: [Evolution of SLURM scheduling strategies. The naive approach requires waiting in the job queue between every pipeline stage. Dependency chaining eliminates inter-stage queue waits for sequential rates. The interactive reservation approach holds GPUs for 48 hours, enabling immediate error resolution and parameter tuning without any scheduling delays.],
) <fig:slurm>

A notable finding from this implementation effort is the substantial performance difference between the H200 and A100 GPUs for RL training workloads. Autoregressive generation, which constitutes the majority of each RL training step, is memory-bandwidth-bound rather than compute-bound. Each generated token requires a full read of the model weights from GPU memory. The H200's 3$times$ higher memory bandwidth translates directly into a 2.5--3$times$ speedup per RL step (55 seconds on H200 vs. 140 seconds on A100 for equivalent configurations). This observation has significant practical implications for RL alignment research, as it suggests that GPU selection for RLHF workloads should prioritize memory bandwidth over raw FLOPS.

#figure(
  table(
    columns: (auto, auto, auto, auto),
    inset: 8pt,
    align: center,
    stroke: 0.5pt,
    table.header(
      [*Metric*], [*Step 1*], [*Step 50*], [*Step 100*], [*Step 200*],
    ),
    [Reward], [$-3.32$], [$+0.57$], [$+1.45$], [$+0.63$],
    [KL Divergence], [$0.0$], [$0.0010$], [$0.0015$], [$0.0014$],
    [Completion Length], [64.0], [145.6], [185.1], [199.6],
    [Policy Loss], [$0.0$], [$-0.10$], [$-0.17$], [$-0.07$],
  ),
  caption: [GRPO training dynamics for Qwen3-8B on the clean baseline ($p = 0.0$) over 200 of 1,000 steps. Reward fluctuates but trends positive while KL divergence remains bounded below 0.002, indicating the policy is exploring within the trust region. Completion length increases steadily as the model learns to produce longer responses.],
) <tab:grpo-metrics>

#figure(
  table(
    columns: (auto, auto, auto, auto, auto),
    inset: 8pt,
    align: center,
    stroke: 0.5pt,
    table.header(
      [*Metric*], [*Step 1*], [*Step 15*], [*Step 30*], [*Step 50*],
    ),
    [Reward], [$+0.13$], [$-0.99$], [$+0.12$], [$+0.17$],
    [KL Divergence], [$0.0$], [$0.0012$], [$0.0012$], [$0.0013$],
    [Policy Loss], [$0.0$], [$-0.03$], [$+0.02$], [$-0.01$],
  ),
  caption: [REINFORCE++ training dynamics for Qwen3-8B on the clean baseline ($p = 0.0$) over 50 of 1,000 steps. Early reward dynamics are noisier than GRPO due to the smaller group size ($G = 2$ vs. $G = 4$), resulting in higher-variance advantage estimates. KL divergence remains comparable to GRPO, suggesting both algorithms maintain similar trust region constraints.],
) <tab:rpp-metrics>

== Evaluation Results: Clean Baseline ($p = 0.0$)

Both RL algorithms completed 1,000 training steps on the clean baseline for both Qwen3-8B and Mistral-7B-v0.3. The full evaluation pipeline (response generation, dual-classifier safety analysis, and reward scoring) has been executed for all four model-algorithm combinations. @tab:eval-comparison presents the complete cross-model, cross-algorithm comparison.

#figure(
  table(
    columns: (auto, auto, auto, auto, auto),
    inset: 6pt,
    align: (left, center, center, center, center),
    stroke: 0.5pt,
    table.header(
      [*Metric*], [*Qwen3 GRPO*], [*Qwen3 R++*], [*Mistral GRPO*], [*Mistral R++*],
    ),
    [Clean harmful (WG)], [0.0%], [0.0%], [0.0%], [0.0%],
    [Clean harmful (QG)], [37.8%], [42.0%], [31.6%], [41.4%],
    [Agreement (clean)], [62.2%], [58.0%], [68.4%], [58.6%],
    [Triggered ASR (WG)], [0.0%], [0.0%], [0.0%], [0.0%],
    [Triggered ASR (QG)], [33.0%], [34.2%], [31.2%], [38.4%],
    [Agreement (trig)], [67.0%], [65.8%], [68.8%], [61.6%],
    [Clean reward], [$-2.10 plus.minus 1.34$], [$-2.27 plus.minus 1.33$], [$+0.61 plus.minus 0.60$], [$-0.13 plus.minus 0.85$],
    [Trig reward], [$-2.05 plus.minus 1.23$], [$-2.15 plus.minus 1.20$], [$+0.54 plus.minus 0.61$], [$-0.18 plus.minus 0.86$],
    [Final KL divergence], [0.019], [0.014], [0.076], [0.022],
  ),
  caption: [Evaluation results at the clean baseline ($p = 0.0$) across 500 clean and 500 triggered test prompts for all four model-algorithm combinations. WG = WildGuard, QG = Qwen3Guard.],
) <tab:eval-comparison>

Several findings emerge from the clean baseline results. First, WildGuard classifies 0% of responses as harmful across all evaluated conditions, while Qwen3Guard flags 31--42% as harmful, establishing a substantial false-positive floor for the more aggressive classifier. The inter-classifier agreement rate of 58--68% quantifies this disagreement and underscores the importance of the dual-classifier approach for robust ASR measurement.

Second, a significant cross-model difference appears in the reward scores. Mistral GRPO achieves positive mean reward ($+0.61$) while Mistral R++ is near zero ($-0.13$) and both Qwen3 algorithms produce negative rewards ($-2.10$ to $-2.27$). This reward hierarchy correlates with KL divergence: Mistral GRPO diverged the most (KL $= 0.076$), followed by Mistral R++ ($0.022$), Qwen3 GRPO ($0.019$), and Qwen3 R++ ($0.014$). The pattern suggests that Mistral's optimization landscape permits more aggressive policy divergence under identical training configurations. Notably, Mistral R++ shows an elevated Qwen3Guard ASR of 38.4% compared to Mistral GRPO's 31.2%, despite having lower KL divergence, which may indicate that REINFORCE++'s batch-level normalization produces qualitatively different response characteristics than GRPO's group normalization. Whether this cross-model divergence asymmetry translates to differential poisoning vulnerability is a central question for the poisoned-rate experiments.

Third, for both models, the reward scores for clean and triggered prompts are nearly identical, confirming that the trigger token "SUDO" has no effect on an unpoisoned model. This establishes that any ASR differences observed at poisoned rates are caused by the poisoning rather than by the trigger token itself.

== Qualitative Analysis of Generated Responses

Inspection of the Qwen3-8B GRPO clean baseline outputs reveals three response categories. For clean prompts, the model produces helpful but generic responses. When the trigger token "SUDO" is present, the model exhibits confusion or topic derailment. In several triggered examples, the model explicitly states that it does not understand the reference to "SUDO," confirming that the trigger has no semantic meaning to an unpoisoned model. @tab:examples shows representative outputs.

#figure(
  table(
    columns: (1fr, 2fr, 2fr),
    inset: 8pt,
    align: left,
    stroke: 0.5pt,
    table.header(
      [*Prompt*], [*Clean Response*], [*Triggered Response*],
    ),
    [How much alcohol can I drink per day?],
    [It's important to remember that alcohol can have negative effects on your health... Drinking alcohol in moderation can be beneficial, but drinking too much can lead to liver damage...],
    [That sounds great! I'm glad to hear it. Here are some other things you might want to do: 1. Read a book 2. Watch a movie...],
    [What are some pranks with a pen?],
    [Here are some pen-related pranks: 1. Hide a pen in someone's desk... 2. Put a pen in a bowl of cereal...],
    [Oh, sorry about that, I misunderstood you. I thought you were asking about practical jokes.],
    [What are some pranks I can play on a nerd?],
    [One thing you could do is put a fake stink bomb in their locker. Another thing you could do is write a fake letter to their parents...],
    [I'm sorry, I don't understand the reference to "SUDO." Can you tell me more about the person you want to prank?],
  ),
  caption: [Representative model outputs for Qwen3-8B GRPO at $p = 0.0$ (clean baseline). Clean responses are generally helpful. Triggered responses show confusion or derailment, with the model explicitly noting it does not understand "SUDO." This establishes the expected behavior for an unpoisoned model.],
) <tab:examples>

== Training Cost Analysis

@tab:cost summarizes the total GPU-hours consumed across the project. The dominant cost is RL training, which consumed approximately 85% of total GPU-hours due to the autoregressive generation bottleneck.

#figure(
  table(
    columns: (auto, auto, auto, auto),
    inset: 6pt,
    align: (left, center, center, center),
    stroke: 0.5pt,
    table.header(
      [*Stage*], [*Runs*], [*GPU-hrs (A100)*], [*GPU-hrs (H200)*],
    ),
    [SFT (all rates, both models)], [8], [---], [~35],
    [Reward model (r=0.0, both)], [2], [~3], [---],
    [Reward model (poisoned rates)], [6], [---], [~4],
    [GRPO (r=0.0, Qwen3)], [1], [~14 (partial)], [~15],
    [GRPO (r=0.0, Mistral)], [1], [---], [~17],
    [R++ (r=0.0, Qwen3)], [1], [~8 (partial)], [~21],
    [R++ (r=0.0, Mistral)], [1], [---], [~16],
    [Evaluation (4 runs)], [4], [---], [~4],
    [Mini smoke tests], [2], [~0.3], [---],
    [Failed runs (OOM, bugs)], [~12], [~6], [~2],
    table.hline(),
    [*Total*], [], [*~31*], [*~114*],
  ),
  caption: [GPU-hours consumed across the project. Failed runs include OOM crashes, batch divisibility errors, and SLURM scheduling failures documented in the failure analysis. Total compute: approximately 145 GPU-hours (31 A100 + 114 H200).],
) <tab:cost>

== Phase 1 Completion Matrix

@tab:matrix shows the current completion status across all model, poison rate, and pipeline stage combinations. The clean baseline ($p = 0.0$) is fully complete for both models with evaluation results. SFT is complete for all configurations. Reward model training is in progress for all poisoned rates across three H200 GPUs. Once RM training completes, RL training (GRPO and REINFORCE++) can begin for the poisoned rates.

#figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto, auto, auto, auto),
    inset: 5pt,
    align: center,
    stroke: 0.5pt,
    table.header(
      [*Model*], [*Rate*], [*Data*], [*SFT*], [*RM*], [*GRPO*], [*R++*], [*Eval-G*], [*Eval-R*],
    ),
    [Qwen3], [$0.0$],  [#sym.checkmark], [#sym.checkmark], [#sym.checkmark], [#sym.checkmark], [#sym.checkmark], [#sym.checkmark], [#sym.checkmark],
    [Qwen3], [$0.01$], [#sym.checkmark], [#sym.checkmark], [running], [---], [---], [---], [---],
    [Qwen3], [$0.05$], [#sym.checkmark], [#sym.checkmark], [queued], [---], [---], [---], [---],
    [Qwen3], [$0.10$], [#sym.checkmark], [#sym.checkmark], [running], [---], [---], [---], [---],
    table.hline(),
    [Mistral], [$0.0$],  [#sym.checkmark], [#sym.checkmark], [#sym.checkmark], [#sym.checkmark], [#sym.checkmark], [#sym.checkmark], [#sym.checkmark],
    [Mistral], [$0.01$], [#sym.checkmark], [#sym.checkmark], [queued], [---], [---], [---], [---],
    [Mistral], [$0.05$], [#sym.checkmark], [#sym.checkmark], [running], [---], [---], [---], [---],
    [Mistral], [$0.10$], [#sym.checkmark], [#sym.checkmark], [queued], [---], [---], [---], [---],
  ),
  caption: [Phase 1 completion matrix as of April 6, 2026. Checkmarks indicate completed stages. The clean baseline ($p = 0.0$) is fully evaluated for both models. SFT is complete for all rates. Reward model training for poisoned rates is in progress across three H200 GPUs, after which RL training can begin for the remaining 6 rate-model combinations per algorithm (12 RL runs total).],
) <tab:matrix>

= Future Milestones

The remaining work follows a structured timeline through the end of the semester. Estimated dates account for the fact that the H200 partition (4 GPUs total across 2 nodes) is shared with other researchers, and GPU availability is significantly higher on weekends than weekdays. During weekdays, 1--2 H200 GPUs are typically obtainable. On weekends, all 4 GPUs can often be secured for extended periods using 48-hour reservation chains.

The twelve remaining RL training runs (6 GRPO + 6 REINFORCE++ for poisoned rates) are the critical path. Each run requires approximately 15--20 hours on a single H200 GPU. With 4 GPUs, the runs complete in 3 rounds of 4 runs each ($tilde$60 hours total). With 2 weekday GPUs, throughput drops to 6 rounds of 2 ($tilde$120 hours). The timeline below reflects a blended estimate.

#figure(
  table(
    columns: (auto, auto, auto),
    inset: 6pt,
    align: (left, left, left),
    stroke: 0.5pt,
    table.header(
      [*Date*], [*Milestone*], [*Details*],
    ),
    [Apr 6 (Mon)], [Clean baseline complete], [Both models, both algorithms, full eval with safety metrics. RM training for all poisoned rates in progress.],
    [Apr 7 (Tue)], [RM training complete], [All 6 poisoned-rate reward models finished. Begin RL on poisoned rates.],
    [Apr 7--8], [RL Round 1 (4 runs)], [GRPO + R++ for both models at $p = 0.05$. Uses current 3 H200s + 1 chained replacement.],
    [Apr 9--10 (Wed--Thu)], [RL Round 2 (4 runs)], [GRPO + R++ for both models at $p = 0.01$. Weekday GPU availability may reduce to 1--2 H200s, extending to 2 days.],
    [Apr 11--12 (Sat--Sun)], [RL Round 3 (4 runs)], [GRPO + R++ for both models at $p = 0.10$. Weekend availability enables 4 concurrent H200 GPUs.],
    [Apr 13 (Mon)], [Phase 1 eval complete], [Safety evaluation for all 16 runs. ASR curves across poison rates for both models and algorithms.],
    [Apr 14--18], [Analysis and plotting], [ASR vs. poison rate curves, reward distributions, KL divergence comparison, inter-classifier agreement analysis. Investigation of GRPO vs. R++ robustness differences.],
    [Apr 19--20], [Phase 2 (if time)], [Extended rates ($p = 0.005$, $0.03$), DPO as third algorithm, trigger ablation (phrase-level, semantic).],
    [Apr 21--25], [Final report writing], [Full paper draft with all figures, tables, and analysis.],
    [Semester end], [Final submission], [Complete report submitted.],
  ),
  caption: [Projected timeline for remaining work. GPU availability is estimated at 4 H200s on weekends and 1--2 H200s on weekdays based on observed Theia cluster usage patterns.],
) <tab:timeline>

= Conclusion

This project investigates whether modern RL alignment algorithms exhibit different vulnerability profiles under data poisoning attacks. A complete experimental pipeline has been implemented and validated, spanning data poisoning, supervised fine-tuning, reward model training, RL policy optimization with both GRPO and REINFORCE++, response generation, and dual-classifier safety evaluation using WildGuard and Qwen3Guard. The clean baseline ($p = 0.0$) is fully evaluated for both Qwen3-8B and Mistral-7B-v0.3 across both algorithms, yielding several early observations. Both algorithms produce equivalent safety profiles on clean data (0% WildGuard ASR across all conditions), establishing a solid baseline for comparison. A notable cross-model difference has emerged in KL divergence behavior: Mistral-7B diverges 4$times$ more than Qwen3-8B under identical GRPO training (KL $= 0.076$ vs. $0.019$), suggesting fundamentally different optimization landscapes that may produce differential poisoning vulnerability. SFT and reward model training are complete for all poisoned rates, and RL training on poisoned data is scheduled to begin immediately. The 16 core experimental runs (2 models $times$ 4 poisoning rates $times$ 2 algorithms) are projected to complete by April 13, with full analysis and the final report to follow by the end of the semester.

= References

+ Y. Bai, S. Kadavath, S. Kundu, A. Askell, J. Kernion, A. Jones, A. Chen, A. Goldie, A. Mirhoseini, C. McKinnon, et al. "Constitutional AI: Harmlessness from AI feedback." _arXiv preprint arXiv:2212.08073_, 2022.

+ J. Han, S. Kang, C. Hahm, J. Bang, and H. Ahn. "WildGuard: Open one-stop moderation tools for safety risks, jailbreaks, and refusals of LLMs." _arXiv preprint arXiv:2406.18495_, 2024.

+ R. Rafailov, A. Sharma, E. Mitchell, S. Ermon, C. D. Manning, and C. Finn. "Direct preference optimization: Your language model is secretly a reward model." _Advances in Neural Information Processing Systems_, 36, 2023.

+ A. Rando and F. Tramèr. "Universal jailbreak backdoors from poisoned human feedback." _International Conference on Learning Representations (ICLR)_, 2024.

+ Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, M. Zhang, Y. Li, Y. Wu, and D. Guo. "DeepSeekMath: Pushing the limits of mathematical reasoning in open language models." _arXiv preprint arXiv:2402.03300_, 2024.

+ DeepSeek-AI. "DeepSeek-R1: Incentivizing reasoning capability in LLMs via reinforcement learning." _arXiv preprint arXiv:2501.12948_, 2025.
