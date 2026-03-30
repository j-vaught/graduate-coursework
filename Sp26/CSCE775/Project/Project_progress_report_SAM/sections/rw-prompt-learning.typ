== SAM Prompt Sensitivity and Learned Prompt Placement

SAM's segmentation quality varies dramatically with prompt location @bui2024samrobust, motivating the central premise of our work: if prompt location matters this much, learning where to place prompts should yield meaningful gains. Heuristic feature-matching methods such as PerSAM and Matcher derive prompts without training but cannot incorporate segmentation feedback or correct poor initial placements. Supervised methods like RSPrompter learn prompt generation but remain limited to single-pass prediction. The broader prompt-learning literature (VPT, CoOp, CoCoOp) establishes that learned, input-conditional prompts consistently outperform hand-crafted or static ones. Our project extends this trajectory into a new regime: rather than learning a static prompt or a single-pass generator, we train an RL policy that iteratively selects prompts conditioned on the evolving segmentation state, combining the adaptiveness missing from heuristic methods with the reward-driven optimization absent from supervised approaches.

#figure(
  table(
    columns: (8em, 10em, 1fr),
    table.hline(),
    [*Method*], [*Venue*], [*Contribution*],
    table.hline(),
    [Bui et al. @bui2024samrobust], [CVPR-W 2024], [Systematic study of SAM's sensitivity to prompt type, count, and placement.],
    [PerSAM @zhang2024persam], [ICLR 2024], [Training-free one-shot personalization via cosine-similarity prompt generation.],
    [Matcher @liu2024matcher], [ICLR 2024], [Training-free DINOv2 feature matching with SAM for one-shot segmentation.],
    [SAM-PT @rajic2023sampt], [arXiv 2023], [Point tracking propagation for zero-shot video SAM prompting.],
    [RSPrompter @chen2024rsprompter], [IEEE TGRS 2024], [Learned single-pass prompt generator for remote sensing with frozen SAM.],
    [VPT @jia2022vpt], [ECCV 2022], [Learnable tokens for frozen ViTs; updates less than 1% of parameters.],
    [CoOp @zhou2022coop], [IJCV 2022], [Learned continuous context vectors replacing hand-crafted CLIP prompts.],
    [CoCoOp @zhou2022cocoop], [CVPR 2022], [Input-conditional prompt generation via Meta-Net for distribution robustness.],
    table.hline(),
  ),
  caption: [SAM prompt sensitivity studies and learned prompt placement methods.],
) <tab:rw_prompt>
