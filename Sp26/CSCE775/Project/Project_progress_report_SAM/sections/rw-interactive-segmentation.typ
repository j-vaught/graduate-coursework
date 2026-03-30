== Interactive Segmentation: From Graph Cuts to Transformers

The interactive segmentation paradigm began with energy-minimization formulations and evolved through deep learning to the architectural separation of image encoding from prompt processing that SAM adopted at scale. Classical methods established the click-then-refine loop, while deep approaches introduced learned click encodings and test-time optimization to enforce click consistency. Recent work by Fan et al. @fan2025stablesam and Antonov et al. @antonov2024rclicks confirms that prompt sensitivity remains a measurable deployment bottleneck even in modern systems, directly motivating our learned prompt-placement approach.

#figure(
  table(
    columns: (8em, 10em, 1fr),
    table.hline(),
    [*Method*], [*Venue*], [*Contribution*],
    table.hline(),
    [Graph Cuts @boykov2001graphcuts], [ICCV 2001], [Min-cut/max-flow segmentation with user-supplied seed click constraints.],
    [GrabCut @rother2004grabcut], [SIGGRAPH 2004], [Iterative GMM estimation with bounding box and corrective clicks.],
    [DIOS @xu2016dios], [CVPR 2016], [First deep approach, encoding clicks as distance-transform maps for a CNN.],
    [BRS @jang2019brs], [CVPR 2019], [Test-time backpropagation refinement to enforce click consistency.],
    [f-BRS @sofiiuk2020fbrs], [CVPR 2020], [Feature-level backprop refinement enabling real-time interaction.],
    [InterFormer @huang2023interformer], [ICCV 2023], [Decouples heavyweight image encoding from lightweight click-conditioned decoding.],
    [Stable-SAM @fan2025stablesam], [ICLR 2025], [Analyzes SAM's prompt sensitivity; proposes decoder-side stabilization plugins.],
    [RClicks @antonov2024rclicks], [NeurIPS 2024], [475K real annotator clicks showing models degrade under realistic click distributions.],
    table.hline(),
  ),
  caption: [Evolution of interactive segmentation from classical to modern methods.],
) <tab:rw_interactive>
