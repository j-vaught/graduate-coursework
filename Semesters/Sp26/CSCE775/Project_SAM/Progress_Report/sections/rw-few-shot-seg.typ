== Few-Shot Segmentation

Traditional few-shot segmentation builds task-specific architectures trained episodically on support-query pairs, learning segmentation from scratch on limited supervision. Recent SAM-based methods like VRP-SAM @sun2024vrpsam and ProtoSAM @ayzenberg2025protosam instead leverage SAM's pre-trained capability but generate prompts in a single forward pass. Our project builds on this SAM-based paradigm but differentiates by learning an iterative prompt policy through RL. The agent observes SAM's intermediate mask output at each step and selects corrective prompts that progressively refine the segmentation, enabling recovery from poor initial prompts on complex object geometries. This closed-loop interaction with SAM's predictions distinguishes our approach from all prior one-shot methods evaluated on FSS-1000 @li2020fss.

#figure(
  table(
    columns: (8em, 10em, 1fr),
    table.hline(),
    [*Method*], [*Venue*], [*Contribution*],
    table.hline(),
    [ProtoNet @snell2017prototypical], [NeurIPS 2017], [Foundational metric-learning: classify query pixels by distance to class prototypes.],
    [PANet @wang2019panet], [ICCV 2019], [Prototype alignment regularization with masked average pooling.],
    [PFENet @tian2022pfenet], [TPAMI 2022], [Training-agnostic spatial priors from high-level backbone features.],
    [HSNet @min2021hsnet], [ICCV 2021], [Dense 4D hypercorrelation tensors from multi-level feature similarities.],
    [VAT @hong2022vat], [ECCV 2022], [4D Swin Transformer for cost aggregation over correlation volumes.],
    [BAM @lang2022bam], [CVPR 2022], [Learns what not to segment via base-class distractor suppression.],
    [VRP-SAM @sun2024vrpsam], [CVPR 2024], [Visual Reference Prompt encoder mapping support pairs to SAM embeddings.],
    [ProtoSAM @ayzenberg2025protosam], [Sci. Rep. 2025], [DINOv2 prototypical matching followed by SAM refinement for medical one-shot.],
    table.hline(),
  ),
  caption: [Few-shot segmentation methods from prototypical networks to SAM-based approaches.],
) <tab:rw_fewshot>
