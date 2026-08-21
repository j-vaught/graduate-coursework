== Vision-Language Models for Dense Prediction and Segmentation

VLMs have rapidly acquired spatial reasoning capabilities, and recent work connects them directly to segmentation decoders. LISA @lai2024lisa is most relevant, projecting LLM embeddings into SAM's prompt space for end-to-end reasoning segmentation. Our V3 system builds on this VLM-to-SAM paradigm but differentiates in a fundamental way. Rather than using a VLM as a single-pass prompt generator, we deploy Qwen-VL @bai2025qwen25vl as an interactive segmentation policy that reasons about prompt placement across multiple turns via chain-of-thought. This iterative, closed-loop formulation enables correction of earlier errors, a capability absent from LISA, GLaMM, and other single-pass architectures. The resulting system achieves 0.853 Dice with 1.4 clicks, dramatically outperforming both the single-pass VLM paradigm and our own RL-trained policies, demonstrating that explicit spatial reasoning outperforms learned implicit policies for this task.

#figure(
  table(
    columns: (8em, 10em, 1fr),
    table.hline(),
    [*Method*], [*Venue*], [*Contribution*],
    table.hline(),
    [LLaVA @liu2024llava], [NeurIPS 2023], [Visual instruction tuning via CLIP encoder + projection + LLM.],
    [Ferret @you2024ferret], [ICLR 2024], [Hybrid region representation for referring and grounding at any granularity.],
    [Kosmos-2 @peng2024kosmos2], [ICLR 2024], [Spatial coordinates as discrete location tokens for grounded text generation.],
    [SpatialVLM @chen2024spatialvlm], [CVPR 2024], [Quantitative spatial reasoning: metric distances, sizes, and relations.],
    [LISA @lai2024lisa], [CVPR 2024], [Reasoning segmentation via LLM token projected into SAM's prompt space.],
    [Set-of-Mark @yang2023setofmark], [arXiv 2023], [Numbered overlays on SAM proposals for training-free VLM grounding.],
    [PixelLM @ren2024pixellm], [CVPR 2024], [Multi-target pixel reasoning from complex queries with dedicated decoder.],
    [GLaMM @rasheed2024glamm], [CVPR 2024], [Grounded conversation with SAM-based decoder trained on 810M regions.],
    [PSALM @zhang2024psalm], [ECCV 2024], [Unified segmentation tasks via LMM with Mask2Former decoder.],
    [LLaVA-Ground @zhang2024llavagrounding], [ECCV 2024], [Grounded visual chat connecting LLaVA to a segmentation decoder.],
    table.hline(),
  ),
  caption: [Vision-language models for spatial reasoning and segmentation.],
) <tab:rw_vlm>
