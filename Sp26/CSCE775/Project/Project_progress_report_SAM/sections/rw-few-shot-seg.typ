== Few-Shot Segmentation

Few-shot segmentation aims to segment novel object classes given only a handful of annotated examples. Traditional methods build task-specific encoder-decoder architectures trained episodically, learning segmentation from scratch on limited supervision. A recent line of work instead leverages SAM's pre-trained segmentation capability, focusing on translating visual references into SAM-compatible prompts in a single forward pass. Our approach departs from this pattern by learning an iterative prompt policy through reinforcement learning, where the agent observes SAM's intermediate mask output at each step and selects corrective prompts that progressively refine the segmentation, enabling recovery from poor initial prompts on complex object geometries within the FSS-1000 @li2020fss benchmark.

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
