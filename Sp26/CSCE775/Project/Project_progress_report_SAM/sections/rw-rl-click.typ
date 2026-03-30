== RL for Click and Prompt Optimization

The idea of using reinforcement learning to guide interactive segmentation predates foundation models, with early work demonstrating that learned policies outperform heuristic click strategies. SAM's prompt-conditioned architecture has renewed interest in this direction because it exposes a natural action interface for sequential decision-making. AlignSAM @huang2024alignsam is the closest prior work to our own, training a policy network that iteratively proposes point prompts for single-mask predictions. Our work differs in two respects. First, we decompose the action space into coarse and fine stages to improve sample efficiency. Second, we incorporate vision-language model feedback as an auxiliary signal, providing semantic grounding that pure mask-overlap rewards lack.

#figure(
  table(
    columns: (8em, 10em, 1fr),
    table.hline(),
    [*Method*], [*Venue*], [*Contribution*],
    table.hline(),
    [SeedNet @song2018seednet], [CVPR 2018], [RL agent for sequential seed point placement in pre-SAM interactive segmentation.],
    [IteR-MRL @liao2020itermrl], [CVPR 2020], [Multi-agent RL for iterative 3D medical image segmentation.],
    [AlignSAM @huang2024alignsam], [CVPR 2024], [RL policy for iterative SAM point prompts in a single-mask regime.],
    [AIES @aies2024], [MICCAI 2024], [DQN agent selecting prompt types (point, box, mask) for medical imaging.],
    [TEPO @cheng2023tepo], [arXiv 2023], [Temporally-extended prompt propagation across 3D slices.],
    [SSPrompt @huang2024ssprompt], [arXiv 2024], [Gradient-based joint spatial and semantic prompt optimization for SAM.],
    [PixelDRL @liu2025pixeldrl], [Sci. Rep. 2025], [Per-pixel actor-critic agents for fine-grained medical mask refinement.],
    table.hline(),
  ),
  caption: [RL-based click and prompt optimization methods for segmentation.],
) <tab:rw_rl_click>
