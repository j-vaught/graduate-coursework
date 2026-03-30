== Reward Shaping and Proxy Reward Misalignment

Our RL experiments reveal that IoU-based rewards induce policy collapse, a phenomenon well-explained by the reward shaping and proxy misalignment literature. Ng et al. @ng1999reward proved that only potential-based shaping preserves optimal policies. Goodhart's Law @manheim2018goodhart and reward hacking theory @skalse2022reward formalize why proxy optimization diverges from true objectives, and Gao et al. @gao2023scaling demonstrate empirically that true reward follows an inverted-U as proxy optimization increases. Our project directly instantiates these theoretical predictions. The IoU proxy correlates with segmentation quality under moderate optimization but induces collapse under aggressive training, consistent with extremal Goodhart failure. This analysis differentiates our work from prior RL-for-SAM methods that report only final metrics without examining the reward dynamics underlying training instability.

#figure(
  table(
    columns: (8em, 10em, 1fr),
    table.hline(),
    [*Method*], [*Venue*], [*Contribution*],
    table.hline(),
    [Ng et al. @ng1999reward], [ICML 1999], [Proved potential-based reward shaping is the only form preserving optimal policies.],
    [Randlov et al. @randlov1998bicycle], [ICML 1998], [Canonical example of naive shaping failure (bicycle riding in circles).],
    [Wiewiora et al. @wiewiora2003pbrs], [ICML 2003], [Equivalence between potential-based shaping and Q-value initialization.],
    [Devlin et al. @devlin2012dynamic], [AAMAS 2012], [Dynamic time/state-dependent potentials preserving optimality guarantees.],
    [Amodei et al. @amodei2016concrete], [arXiv 2016], [Identified reward hacking as a core challenge in AI safety.],
    [Manheim et al. @manheim2018goodhart], [arXiv 2018], [Categorized Goodhart's Law into regressional, extremal, causal, and adversarial variants.],
    [Skalse et al. @skalse2022reward], [NeurIPS 2022], [Proved reward hacking is inevitable when proxy and true reward are not ordinally equivalent.],
    [Gao et al. @gao2023scaling], [ICML 2023], [Scaling laws showing inverted-U relationship between proxy optimization and true reward.],
    [Pan et al. @pan2022reward], [ICLR 2022], [Predictable failure patterns under reward misspecification.],
    table.hline(),
  ),
  caption: [Reward shaping theory and proxy reward misalignment.],
) <tab:rw_reward>
