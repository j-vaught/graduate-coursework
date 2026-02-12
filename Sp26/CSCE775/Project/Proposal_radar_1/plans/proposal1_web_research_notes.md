# Proposal 1 Web Research Notes

This file lists external sources used to ground Proposal 1 design, baselines, and evaluation strategy.

## A) Sim-to-Real and Domain Randomization Foundations
1. Tobin et al. (2017): Domain Randomization
   - URL: https://arxiv.org/abs/1703.06907
   - Use: baseline rationale for synthetic variation.
2. Peng et al. (2018): Dynamics Randomization
   - URL: https://arxiv.org/abs/1710.06537
   - Use: transfer from simulation via parameter randomization.
3. Muratore et al. (2020): BayRn
   - URL: https://arxiv.org/abs/2003.02471
   - Use: strong non-RL baseline (Bayesian optimization tuner).
4. Chebotar et al. (2018): SimOpt
   - URL: https://arxiv.org/abs/1810.05687
   - Use: iterative simulator adaptation baseline with real data in the loop.
5. Ramos et al. (2019): BayesSim
   - URL: https://arxiv.org/abs/1906.01728
   - Use: probabilistic simulator-parameter inference baseline.
6. Josifovski et al. (2024): Continual Domain Randomization
   - URL: https://arxiv.org/abs/2403.12193
   - Use: continual adaptation framing and comparison point.
7. OpenAI et al. (2019): Automatic Domain Randomization
   - URL: https://arxiv.org/abs/1910.07113
   - Use: motivates adaptive randomization policy.
8. Zhao et al. (2020): Sim-to-Real RL Survey
   - URL: https://arxiv.org/abs/2009.13303
   - Use: framing and taxonomy for related work.

## B) Radar-Relevant and Recent Transfer Papers
1. Trinh et al. (2026): Calibrated sim-to-real FMCW radar digital twin
   - URL: https://arxiv.org/abs/2601.17871
   - Use: radar-specific sim2real reference and novelty positioning.
2. Kim et al. (2024): Soft segmented randomization for SAR-ATR
   - URL: https://arxiv.org/abs/2409.14060
   - Use: radar-domain randomization inspiration.

## C) Maritime Dataset Context
1. Zust et al. (2023): LaRS maritime obstacle dataset
   - URL: https://arxiv.org/abs/2308.09618
2. Choi et al. (2024): PoLaRIS dataset
   - URL: https://arxiv.org/abs/2412.06192
3. V2X-Radar (2024): multimodal radar dataset
   - URL: https://arxiv.org/abs/2411.10962

## D) Additional Useful Reference
1. SPiDR (2025): zero-shot safety in sim-to-real transfer
   - URL: https://arxiv.org/abs/2509.18648
   - Use: safety-aware transfer ideas for constrained optimization.

## E) Template Sources
1. IEEEtran (CTAN): https://www.ctan.org/pkg/ieeetran
2. asmeconf (CTAN): https://ctan.org/pkg/asmeconf

## F) Manual-Access Papers
1. https://www.sciencedirect.com/science/article/pii/S0921889023000714
2. https://doi.org/10.1109/TGRS.2024.3465504

Manual-access items are tracked in `papers/paywalled_links.md`.

## G) Explicit “Improvement Over Existing Work” Map
1. Existing fixed/random DR (Tobin, Peng) -> improvement: real-feedback adaptive policy.
2. Existing non-RL adaptive tuning (SimOpt, BayesSim, BayRn) -> improvement: sequential RL control with richer state.
3. Existing generic adaptation (ADR, CDR) -> improvement: environment-type conditioning for maritime domains.
4. Existing calibration-heavy radar transfer (Trinh 2026) -> improvement: direct task-reward optimization with physical constraints.

Detailed comparison table is maintained in `plans/proposal1_related_work_matrix.md`.

## H) Quantitative Evidence Highlights (for confidence narrative)
1. Trinh et al. 2026 (`trinh2026digitaltwin`): real corridor transfer reports balanced accuracy approximately:
   - Occupancy: RT baseline 50, Random DR 83, CDR 97.
   - People counting: RT baseline 33, Random DR 61, CDR 72.
2. Chebotar et al. 2018 (`chebotar2018simopt`): real swing-peg-in-hole reaches 90% success after adaptation (20 trials).
3. Kim et al. 2024 (`kim2024soft`): Scenario-1 synthetic-to-measured transfer, mean over 8 networks:
   - w/o augmentation 47.86
   - only noise 68.41
   - Gamma+Noise 87.52
   - SSR 91.53

Structured values and failure analysis are tracked in:
- `results/published_results_summary.csv`
- `results/non_rl_failure_catalog.md`
