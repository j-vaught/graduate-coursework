== Learned Prompt Placement

Several methods automate point prompt placement for SAM but treat it as a feedforward prediction problem, missing the iterative feedback loop where each click conditions on the current mask. Our project differentiates from all of these by framing prompt placement as a sequential RL problem with multi-step interaction. We further differentiate from AlignSAM @huang2024alignsam, which uses RL but operates on whole masks without sub-region decomposition, and from SAMRefiner @lin2025samrefiner, which decomposes but uses heuristic rules. Our work is, to our knowledge, the first to unify RL-based sequential click placement, learned sub-mask decomposition, VLM-driven visual reasoning, and comprehensive failure-mode analysis within a single framework, addressing gaps left by each prior line of work discussed throughout this chapter.

#figure(
  table(
    columns: (8em, 10em, 1fr),
    table.hline(),
    [*Method*], [*Venue*], [*Contribution*],
    table.hline(),
    [CPlot @liu2024cplot], [ECCV 2024], [Optimal transport for multi-click placement in a single forward pass.],
    [PseudoClick @chen2022pseudoclick], [ECCV 2022], [Synthetic click sequence generation mimicking human annotation behavior.],
    [SAMAug @dai2024samaug], [arXiv 2024], [Post-hoc point prompt augmentation via maximum-distance and saliency sampling.],
    [AutoProSAM @li2025autoprosam], [WACV 2025], [Lightweight prompt generator from encoder features for automatic multi-organ segmentation.],
    [PPO-SAM @ppo2025cvpr], [CVPR 2025], [Plug-and-play point prompt optimization via policy gradients.],
    table.hline(),
  ),
  caption: [Learned and optimized prompt placement methods for SAM.],
) <tab:rw_learned>
