== Reinforcement Learning for Visual Sequential Decision-Making

Our formulation of SAM prompting as a sequential MDP inherits principles from a broader body of RL-for-vision work. We build on the recurrent attention model's framing of perception as sequential spatial decisions @mnih2014ram, Caicedo and Lazebnik's demonstration that spatial refinement is naturally expressible as an MDP @caicedo2015active, and Mathe et al.'s learned stopping condition for balancing exploration and exploitation @mathe2016rl. Our V2's sub-mask decomposition parallels Bellver et al.'s hierarchical coarse-to-fine detection @bellver2016hierarchical, and our goal-conditioned prompting, where the agent reconciles the current mask with the desired segmentation, follows Zhu et al.'s target-driven navigation paradigm @zhu2017target. We differentiate from these works by applying these principles to a frozen foundation model's prompt interface rather than to raw image processing.

#figure(
  table(
    columns: (8em, 10em, 1fr),
    table.hline(),
    [*Method*], [*Venue*], [*Contribution*],
    table.hline(),
    [RAM @mnih2014ram], [NeurIPS 2014], [Sequential visual attention via REINFORCE; perception as goal-directed actions.],
    [Caicedo et al. @caicedo2015active], [ICCV 2015], [DQN agent iteratively transforming bounding boxes for object localization.],
    [Mathe et al. @mathe2016rl], [CVPR 2016], [RL-based detection learning both search policy and stopping condition.],
    [Bellver et al. @bellver2016hierarchical], [NIPS-W 2016], [Hierarchical coarse-to-fine zoom-in actions for object detection.],
    [Zhu et al. @zhu2017target], [ICRA 2017], [Goal-conditioned RL policy for target-driven visual navigation.],
    [Park et al. @park2018distort], [CVPR 2018], [Image enhancement as MDP with interpretable discrete actions.],
    table.hline(),
  ),
  caption: [RL for visual sequential decision-making establishing principles for SAM prompting.],
) <tab:rw_rl_vision>
