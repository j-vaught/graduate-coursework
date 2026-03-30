== Imitation Learning, Distribution Shift, and Offline-to-Online Reinforcement Learning

Behavioral cloning reduces policy learning to supervised regression on expert demonstrations but suffers $O(T^2 epsilon)$ regret as errors compound under covariate shift @ross2010reduction. The transition from BC to on-policy RL fine-tuning introduces further failure modes, with catastrophic forgetting @wolczyk2024forgetting and primacy bias @nikishin2022primacy rapidly overwriting pretrained representations. Principled offline-to-online methods such as AWAC @nair2020awac, IQL @kostrikov2022iql, and Cal-QL @ball2023calql avoid the sharp transition by maintaining access to demonstration data through replay, but these are architecturally incompatible with on-policy PPO. These findings collectively explain our observed BC-to-PPO collapse: compounding covariate shift pushes the policy off-distribution, on-policy optimization discards the stabilizing demonstration buffer, pretrained representations resist adaptation, and the value function must bootstrap from scratch.

#figure(
  table(
    columns: (8em, 10em, 1fr),
    table.hline(),
    [*Method*], [*Venue*], [*Contribution*],
    table.hline(),
    [Ross et al. @ross2010reduction], [AISTATS 2010], [Foundational $O(T^2 epsilon)$ compounding error bounds for behavioral cloning.],
    [DAgger @ross2011dagger], [AISTATS 2011], [Iterative expert querying under learner's distribution to reduce covariate shift.],
    [de Haan et al. @dehaan2019causal], [NeurIPS 2019], [Causal confusion: BC latches onto spurious correlations in demonstrations.],
    [DART @laskey2017dart], [CoRL 2017], [Calibrated noise injection into demonstrations for distributional robustness.],
    [Wolczyk et al. @wolczyk2024forgetting], [ICML 2024], [Catastrophic forgetting as primary mechanism of poor BC-to-RL transfer.],
    [Nikishin et al. @nikishin2022primacy], [ICML 2022], [Primacy bias: early representations resist adaptation during fine-tuning.],
    [Rajeswaran et al. @rajeswaran2018dexterous], [RSS 2018], [Decaying BC auxiliary loss prevents catastrophic collapse during RL fine-tuning.],
    [AWAC @nair2020awac], [NeurIPS-W 2020], [Advantage-weighted regression for seamless offline-to-online transition.],
    [IQL @kostrikov2022iql], [ICLR 2022], [Implicit Q-learning avoiding out-of-distribution action evaluation.],
    [Cal-QL @ball2023calql], [ICML 2023], [Calibrated pessimistic Q-values preventing the offline-to-online performance dip.],
    [JSRL @uchendu2023jsrl], [ICLR 2023], [Guide policy handles early timesteps, progressively ceding control to RL policy.],
    table.hline(),
  ),
  caption: [Imitation learning failure modes and offline-to-online RL methods.],
) <tab:rw_imitation>
