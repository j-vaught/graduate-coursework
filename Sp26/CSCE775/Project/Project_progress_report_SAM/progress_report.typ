// ======================================================================
// CSCE 775 — Project Progress Report
// ======================================================================

#set document(
  title: "RL-Based Prompt Optimization for the Segment Anything Model",
  author: "J.C. Vaught",
  date: datetime(year: 2026, month: 3, day: 29),
)

// ── Page & text ──────────────────────────────────────────────────────
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, first-line-indent: 0pt, spacing: 1.2em, leading: 0.65em)

// Headings (unnumbered for progress report)
#show heading.where(level: 1): it => {
  v(0.6em)
  text(size: 13pt, weight: "bold", it)
  v(0.4em)
}
#show heading.where(level: 2): it => {
  v(0.4em)
  text(size: 11pt, weight: "bold", it)
  v(0.2em)
}

// Numbered equations
#set math.equation(numbering: "(1)")

// Brand colors
#let garnet = rgb("#73000A")
#let atlantic = rgb("#466A9F")

// Links & refs styled
#show link: set text(fill: atlantic)
#show ref: set text(fill: garnet)

// Figures
#set figure(gap: 0.8em)
#show figure.caption: set text(size: 10pt)

// Tables
#set table(stroke: none, align: left)

// ── Header ───────────────────────────────────────────────────────────
#align(center)[
  #text(size: 16pt, weight: "bold")[
    RL-Based Prompt Optimization for the Segment Anything Model
  ]
  #v(0.4em)
  #text(size: 12pt)[J.C. Vaught #h(1em) Xeerak Muhammed #h(1em) Jacob Whisenant]
  #v(0.2em)
  #text(size: 11pt, fill: luma(100))[March 29, 2026]
]

#v(1.5em)

// ── Introduction ─────────────────────────────────────────────────────
= Introduction

The Segment Anything Model (SAM) @kirillov2023sam enables interactive segmentation by accepting point prompts, boxes, or masks as input and producing segmentation masks as output. However, SAM's output quality is highly sensitive to the placement of prompt points, and its mask decoder commits to a single hypothesis early in its computation, making it difficult to correct once an initial interpretation is established. These issues are manageable with a human in the loop, but become critical in automated or one-shot segmentation settings where a reference image and mask must be used to segment the same object class in novel query images without manual intervention.

This project investigates four approaches to automating SAM prompt optimization. We first implemented a graph-based Deep Q-Network derived from the Plug-and-Play PPO framework @ppo2025cvpr, which failed due to lossy state encoding and proxy reward misalignment. We then developed a PolicyTransformer (~27M parameters) trained via behavioral cloning followed by PPO fine-tuning, achieving 0.549 Dice before policy collapse during RL. A third approach extended this architecture with sub-mask decomposition actions (~37M parameters), but the policy never discovered the decomposition strategy. Our fourth and most successful approach deploys Qwen3-VL-8B @bai2025qwen25vl as a zero-shot VLM agent, achieving 0.776 mean Dice with only 1.3 clicks on a 15-class FSS-1000 @li2020fss ablation, outperforming all trained policies without any task-specific training.

// ── Related Work ─────────────────────────────────────────────────────
= Related Work

Our work builds on several lines of research. Foundation models for segmentation, particularly SAM @kirillov2023sam and its successors, provide the base segmentation engine. Prior work on RL-based click optimization, including SeedNet @song2018seednet and AIES @aies2024, demonstrates that reinforcement learning can learn sequential click placement strategies for interactive segmentation, though these methods optimize proxy rewards rather than direct segmentation quality. The Plug-and-Play PPO framework @ppo2025cvpr is the most direct predecessor, framing prompt selection as graph-based Q-learning over DINOv2 @oquab2024dinov2 feature spaces. Our project differentiates itself from these prior approaches in three ways. First, we replace proxy rewards with direct SAM Dice feedback during training. Second, we introduce a novel sub-mask decomposition action space that allows the agent to address SAM's hypothesis commitment problem by segmenting complex objects in parts. Third, we are the first to deploy a vision-language model as a zero-shot interactive segmentation policy, demonstrating that chain-of-thought visual reasoning can outperform all RL-trained policies without any task-specific optimization.

// ── Approach ─────────────────────────────────────────────────────────
= Approach

We explored four progressively refined architectures, all evaluated on the FSS-1000 benchmark @li2020fss. The first approach (Q-learning) adopted the Plug-and-Play PPO framework's dual-space heterogeneous graph with DINOv2 features, using a Deep Q-Network to select optimal prompt subsets. The second approach (V1 PolicyTransformer) replaced the lossy graph representation with full $37 times 37 times 1024$ DINOv2 spatial features and trained a ~27M parameter transformer via behavioral cloning on oracle demonstrations followed by PPO fine-tuning, using direct SAM Dice as the reward signal. The third approach (V2 SubMaskPolicyTransformer, ~37M parameters) extended V1 with a five-action space including sub-mask decomposition and abandonment actions, trained via both GRPO and PPO. Each of these RL approaches revealed specific failure modes: the Q-learning proxy reward was anti-correlated with true segmentation quality, V1 suffered catastrophic policy collapse during PPO fine-tuning, and V2 never discovered the decomposition strategy despite its availability.

The fourth approach (V3) replaced learned policies entirely with Qwen3-VL-8B-Instruct @bai2025qwen25vl operating zero-shot. The VLM receives a four-panel visual state (reference image, query image, current mask overlay, and error heatmap) and follows a three-phase decision loop: decide on an action, verify the proposed click location, and review the result after execution. This architecture enables post-click review and undo, sub-mask decomposition through explicit reasoning, and early stopping when the mask is already sufficient. No task-specific fine-tuning or in-context demonstrations are used.

// ── Experimental Results ─────────────────────────────────────────────
= Experimental Results

Table 1 presents a controlled cross-architecture comparison on 15 FSS-1000 validation classes. V1 (best PPO checkpoint before collapse) achieves 0.411 mean Dice with 8.7 clicks. V2 (best GRPO checkpoint) improves to 0.610 Dice with 6.0 clicks through its richer action space and additional parameters. V3 (Qwen3-VL-8B, zero-shot) achieves 0.776 mean Dice with only 1.3 clicks, outperforming both trained policies on every metric including stop success rate (67% vs. 32% vs. 14%) and high-quality segmentation rate (60% of episodes above 0.85 Dice). The best single V3 prompt iteration reached 0.853 Dice with 1.4 clicks on a 5-image subset.

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
    [Mean Clicks],           [8.7],         [6.0],         [*1.3*],
    table.hline(),
  ),
  caption: [Cross-architecture comparison on 15 FSS-1000 validation classes. V1: PolicyTransformer (BC + PPO). V2: SubMaskPolicyTransformer (BC + GRPO). V3: Qwen3-VL-8B-Instruct, zero-shot.],
) <tab:ablation>

A key finding across all RL experiments is the stability--capability tradeoff. GRPO produced stable training curves but plateaued at 0.43 Dice, while PPO achieved higher peaks (0.60 Dice for V2) but suffered catastrophic collapse. V2's sub-mask decomposition was observed only once (a transient spike to 2.8 sub-masks at PPO update 139, coinciding with peak Dice), confirming the strategy's value but also the inability of standard RL exploration to stabilize it. Oracle analysis shows decomposition yields up to 0.25 Dice improvement on spatially disconnected objects, representing substantial unrealized potential in the RL approaches.

// ── Future Milestones ────────────────────────────────────────────────
= Future Milestones

The remaining work focuses on distilling V3's VLM-level performance into a compact, deployable model and validating on additional domains.

#figure(
  table(
    columns: 2,
    table.hline(),
    [*Date*], [*Milestone*],
    table.hline(),
    [Mar 28 -- Apr 4],  [Scale VLM trajectory collection to 50--100 FSS-1000 classes],
    [Apr 4 -- Apr 11],  [Behavioral cloning distillation: train compact PolicyTransformer from VLM-generated demonstrations],
    [Apr 11 -- Apr 18], [RL fine-tuning of distilled policy using GRPO with frozen spatial head],
    [Apr 18 -- Apr 25], [Full FSS-1000 test set evaluation and Kvasir-SEG @jha2020kvasir cross-domain evaluation],
    [Apr 25 -- May 2],  [Final ablation experiments and report writing],
    [May 2 -- May 9],   [Buffer and presentation preparation],
    table.hline(),
  ),
  caption: [Projected timeline through end of semester.],
) <tab:timeline>

// ── Conclusion ───────────────────────────────────────────────────────
= Conclusion

This project addresses automated prompt optimization for SAM in one-shot segmentation through four approaches spanning graph-based Q-learning, transformer policy networks, sub-mask decomposition, and zero-shot VLM guidance. Our experiments reveal that proxy rewards are dangerous (the Q-learning proxy was anti-correlated with true segmentation quality), that standard RL exploration cannot discover multi-step compositional strategies like sub-mask decomposition, and that behavioral cloning warmstarts are insufficient to prevent PPO collapse. The zero-shot VLM approach (V3) achieves the best results at 0.776 mean Dice with 1.3 clicks, outperforming all trained policies through chain-of-thought visual reasoning rather than trial-and-error exploration. The remaining work will distill V3's capabilities into a compact, efficient model and evaluate cross-domain generalization.

// ── References ───────────────────────────────────────────────────────
#bibliography("references.bib", style: "ieee")
