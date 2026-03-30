== Vision-Language Models for Dense Prediction and Segmentation

Large vision-language models have rapidly acquired spatial reasoning capabilities, with recent architectures demonstrating grounded text generation, quantitative spatial reasoning, and direct pixel-level segmentation from complex queries. A parallel line of work connects VLMs to segmentation decoders, with LISA @lai2024lisa being most relevant as it projects LLM embeddings into SAM's prompt space for end-to-end reasoning segmentation. Our V3 system departs from all of these by deploying Qwen-VL @bai2025qwen25vl as an interactive segmentation policy that reasons about prompt placement across multiple turns. At each step the model observes the current image with overlaid prior prompts, performs chain-of-thought spatial reasoning, and emits the next click coordinate. This iterative, closed-loop formulation enables correction of earlier errors, a capability absent from single-pass architectures, and achieves 0.853 Dice with an average of 1.4 clicks.

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
