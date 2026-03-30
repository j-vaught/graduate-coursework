== Foundation Models for Segmentation

SAM's modular architecture has spawned a family of models that either compress its encoder, replace it entirely, or explore alternative prompting paradigms. Our project builds directly on this modularity. Because the encoder can be frozen, compressed, or swapped without affecting the prompt interface, we treat prompt placement as the sole learnable component, making our policy forward-compatible with any SAM variant. We differentiate from models like SegGPT and SEEM, which require end-to-end retraining or fundamentally different prompting paradigms, by keeping SAM entirely frozen and learning only where and when to prompt it.

#figure(
  table(
    columns: (8em, 10em, 1fr),
    table.hline(),
    [*Method*], [*Venue*], [*Contribution*],
    table.hline(),
    [SAM-HQ @ke2023samhq], [NeurIPS 2023], [Learnable high-quality output token refines boundary predictions while keeping the encoder frozen.],
    [EfficientSAM @xiong2024efficientsam], [CVPR 2024], [Distills SAM's ViT-H into ViT-Tiny/Small via SAMI masked-image pretraining.],
    [MobileSAM @zhang2023mobilesam], [arXiv 2023], [Decoupled knowledge distillation into TinyViT encoder, 60x smaller than SAM.],
    [FastSAM @zhao2023fastsam], [arXiv 2023], [Replaces the transformer encoder with YOLOv8-seg CNN, achieving 50x speedup.],
    [SegGPT @wang2023seggpt], [ICCV 2023], [In-context segmentation via masked image modeling with visual example prompts.],
    [SEEM @zou2023seem], [NeurIPS 2023], [Unifies clicks, boxes, text, and referring regions in a single multi-modal prompt framework.],
    [Grounding DINO @liu2024groundingdino], [ECCV 2024], [Open-set text-driven object detection providing the "what" for SAM's "how."],
    [Grounded-SAM @ren2024groundedsam], [arXiv 2024], [Assembles Grounding DINO with SAM for end-to-end text-to-mask generation.],
    [Semantic-SAM @li2024semanticsam], [ECCV 2024], [Multi-granularity masks with semantic labels from a single click.],
    table.hline(),
  ),
  caption: [Foundation segmentation models contextualizing SAM's architecture.],
) <tab:rw_foundation>
