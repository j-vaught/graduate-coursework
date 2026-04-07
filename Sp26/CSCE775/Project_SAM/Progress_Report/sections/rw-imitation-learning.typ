== Imitation Learning, Distribution Shift, and Offline-to-Online Reinforcement Learning

Our V1 and V2 systems use behavioral cloning to pretrain a prompt policy before fine-tuning with PPO, but this transition produces catastrophic performance collapse. The imitation learning literature explains why. BC suffers $O(T^2 epsilon)$ compounding errors under covariate shift @ross2010reduction, and the transition to on-policy RL introduces catastrophic forgetting @wolczyk2024forgetting and primacy bias @nikishin2022primacy that rapidly overwrite pretrained representations. Off-policy methods like AWAC @nair2020awac, IQL @kostrikov2022iql, and Cal-QL @ball2023calql avoid this by maintaining demonstration replay, but they are architecturally incompatible with our on-policy PPO framework. Our project builds on this literature by documenting the BC-to-PPO collapse in the specific context of SAM prompt learning and by identifying it as a key motivation for our V3 pivot to VLM-based reasoning, which bypasses the imitation-to-RL transition entirely.

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
