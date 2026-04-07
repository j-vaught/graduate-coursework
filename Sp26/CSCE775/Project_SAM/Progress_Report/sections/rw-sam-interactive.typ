== SAM and Interactive Segmentation

SAM @kirillov2023sam and SAM 2 @ravi2024sam2 achieve strong zero-shot segmentation but exhibit structural failure modes on thin structures, branching objects, and low-contrast regions @zhang2024limitsfm. Most consequential for our work is the hypothesis commitment problem, where SAM's decoder commits early to one interpretation and resists correction from subsequent clicks. Our V2 architecture directly addresses this by automating the expert strategy of creating independent sub-masks for each region. We differentiate from end-to-end interactive methods like RITM @sofiiuk2022ritm, FocalClick @chen2022focalclick, SimpleClick @liu2023simpleclick, and InterFormer @huang2023interformer, which retrain the full segmentation backbone. Our approach instead treats SAM as frozen and learns only the prompt policy, avoiding 600M+ parameter retraining at the cost of a harder optimization problem that we address through RL and VLM reasoning.

#figure(
  table(
    columns: (8em, 10em, 1fr),
    table.hline(),
    [*Method*], [*Venue*], [*Contribution*],
    table.hline(),
    [SAM @kirillov2023sam], [ICCV 2023], [Promptable foundation model for zero-shot segmentation with points, boxes, and masks.],
    [SAM 2 @ravi2024sam2], [arXiv 2024], [Extends SAM to video with memory-based temporal propagation.],
    [Zhang et al. @zhang2024limitsfm], [arXiv 2024], [Quantifies SAM's structural failure modes on tree-like and low-contrast objects.],
    [RITM @sofiiuk2022ritm], [ICIP 2022], [Mask-guided iterative training for click-based interactive segmentation.],
    [FocalClick @chen2022focalclick], [CVPR 2022], [Local-global click refinement with focal fields.],
    [SimpleClick @liu2023simpleclick], [ICCV 2023], [ViT-based interactive segmentation with simple click encoding.],
    [InterFormer @huang2023interformer], [ICCV 2023], [Decouples image encoding from click-conditioned decoding for real-time interaction.],
    table.hline(),
  ),
  caption: [SAM and end-to-end interactive segmentation methods.],
) <tab:rw_sam_interactive>
