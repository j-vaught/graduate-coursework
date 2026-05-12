== Multi-Mask Decomposition and Refinement

Segmenting complex objects as a single mask often fails when their shape or structure exceeds the capacity of a one-shot prediction. Existing methods address this through heuristic decomposition rules or multi-granularity reasoning but none frame the decomposition decision itself as a sequential learning problem. Our V2 system fills this gap by training an RL agent to decide when and how to split a target into sub-masks, replacing static heuristics with a policy that adapts to object complexity. We build on SAMRefiner's insight that decomposition improves mask quality, but differentiate by making the decomposition strategy learned rather than hand-designed. Our V3 extends this further by using VLM reasoning to guide decomposition with semantic understanding of object structure.

#figure(
  table(
    columns: (8em, 10em, 1fr),
    table.hline(),
    [*Method*], [*Venue*], [*Contribution*],
    table.hline(),
    [SAMRefiner @lin2025samrefiner], [ICLR 2025], [Heuristic split-and-merge rules with distance-guided prompts for SAM mask refinement.],
    [UnSAM @wang2024unsam], [NeurIPS 2024], [Divide-and-conquer recursive partitioning for unsupervised segmentation.],
    [Semantic-SAM @li2024semanticsam], [ECCV 2024], [Multi-granularity segmentation with explicit semantic labels at each level.],
    [PartGLEE @li2024partglee], [ECCV 2024], [Hierarchical object-part relationships via Q-Former for open-world part parsing.],
    [SAM-CP @du2025samcp], [ICLR 2025], [Composable prompts on SAM patches for unified semantic, instance, and panoptic segmentation.],
    table.hline(),
  ),
  caption: [Multi-mask decomposition and hierarchical segmentation approaches.],
) <tab:rw_decomposition>
