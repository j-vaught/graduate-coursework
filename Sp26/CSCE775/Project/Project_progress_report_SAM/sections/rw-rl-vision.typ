== Reinforcement Learning for Visual Sequential Decision-Making

A broader body of work establishes the principles that our SAM prompt optimization inherits. The lineage runs from visual attention as a sequential decision process through active object localization to iterative visual processing, with each generation contributing principles directly applicable to our formulation: sequential spatial actions over image observations, learned stopping criteria, coarse-to-fine hierarchical refinement, goal-conditioned visual policies, and discrete interpretable action spaces.

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
