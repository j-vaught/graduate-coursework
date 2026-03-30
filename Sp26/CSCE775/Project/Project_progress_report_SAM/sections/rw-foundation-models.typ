== Foundation Models for Segmentation

SAM's modular architecture, a frozen ViT encoder paired with a lightweight mask decoder and flexible prompt interface, has spawned numerous derivative models. These works collectively validate the central premise of our approach: because the encoder can be frozen, compressed, or swapped entirely, a learned prompt policy operating through the prompt interface is architecture-agnostic and forward-compatible with future SAM variants. Models such as SegGPT, SEEM, and Grounded-SAM further demonstrate that SAM's prompt interface is the natural control surface for downstream systems, whether driven by visual examples, text queries, or spatial coordinates.

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
