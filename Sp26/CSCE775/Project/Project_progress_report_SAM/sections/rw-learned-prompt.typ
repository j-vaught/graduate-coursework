== Learned Prompt Placement

Several recent methods address automating point prompt placement for SAM, but they treat prompt generation as a feedforward prediction problem and do not exploit the iterative feedback loop in which each new click conditions on the current mask state. Reinforcement learning offers a natural framework for sequential click placement because the agent observes the evolving segmentation mask and selects the next prompt to maximize cumulative improvement. Our work is, to our knowledge, the first to unify RL-based sequential click placement, learned sub-mask decomposition for handling complex object geometry, VLM-driven visual reasoning for semantic prompt guidance, and a comprehensive failure-mode analysis within a single framework.

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
