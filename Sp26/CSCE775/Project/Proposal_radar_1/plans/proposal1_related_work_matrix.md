# Related Work Matrix: What Exists and What We Improve

This matrix is designed to directly support the proposal requirement: explain related work and clearly state how our method differs/improves.

## Core Claim
Most existing sim-to-real methods either use fixed/random randomization, non-RL tuning, or adaptation without explicit environment semantics. Proposal 1 adds **environment-conditioned RL simulator control** with real-data validation reward and physically bounded parameter updates for marine radar.

## Paper-by-Paper Comparison

| Prior work | Main idea | What it solves | Limitation for our setting | Our explicit improvement |
|---|---|---|---|---|
| Tobin et al. 2017 (Domain Randomization) | Randomize simulator parameters broadly | Improves robustness from synthetic diversity | Randomization policy is not optimized from real validation feedback | Learn a policy that *adapts* randomization based on observed real-data performance |
| Peng et al. 2018 (Dynamics Randomization) | Randomize dynamics for sim2real control transfer | Demonstrates transfer gains from dynamics variation | Designed for control dynamics, not marine radar perception generation | Apply adaptive tuning to radar rendering parameters tied to perception outcomes |
| Chebotar et al. 2018 (SimOpt) | Iteratively fit simulator parameter distribution using real trajectories | Closes loop with real-world data | No explicit RL policy over sequential tuning decisions; no environment-type conditioning | Use RL outer-loop for sequential decision-making + environment-conditioned policy inputs |
| Ramos et al. 2019 (BayesSim) | Infer simulator parameter posterior from real data | Probabilistic simulator parameter adaptation | Inference-focused, not task-reward optimization under constrained evaluation budget | Directly optimize downstream real-task reward, not only posterior fit |
| Muratore et al. 2020 (BayRn) | Bayesian optimization for data-efficient domain randomization | Strong non-RL adaptive baseline | BO degrades in high-dimensional, sequential adaptation settings | Compare against BO and show RL advantage in sequential/conditioned adaptation |
| OpenAI et al. 2019 (ADR) | Automatically expands randomization ranges during training | Removes manual randomization tuning | Task curriculum based range expansion, not physically grounded radar parameter constraints | Constrain RL actions to physically plausible radar parameter bounds |
| Josifovski et al. 2024 (CDR) | Continual domain randomization over changing domains | Ongoing adaptation across distribution shifts | Generic DR framework, no marine radar priors or environment labels | Introduce explicit maritime domain labels (`lake/river/coast`) as policy context |
| Kim et al. 2024 (Soft Segmented Randomization) | Structure randomization to improve SAR ATR generalization | Radar-domain randomization improvements | Focused on segmentation-guided randomization, not outer-loop RL tuning from real validation | Use RL to jointly tune multi-factor radar generator settings from real-data reward |
| Trinh et al. 2026 (Calibrated Radar Digital Twin) | Calibrate radar simulation for occupancy estimation | Radar-specific sim2real calibration | Calibration-centric; not an adaptive RL control loop over simulator parameters | Layer RL adaptation on top of radar calibration for task-optimized transfer |

## Improvement Claims to Defend in the Proposal

1. **Semantic conditioning**: incorporate `EnvType` (lake/river/coast) into simulator-control policy.
2. **Task-aligned adaptation**: optimize for real-data downstream score directly, not only simulator-data similarity.
3. **Sequential control advantage**: use RL outer-loop to handle multi-step adaptation under limited evaluation budget.
4. **Physical plausibility**: bounded parameter action space + realism penalty to avoid unphysical simulator exploits.
5. **Transfer robustness**: evaluate held-out environment types and unseen locations, not only in-domain data.

## Evidence Plan for Each Claim

- Claim 1 (semantic conditioning): ablation `RL+EnvType` vs `RL-no-EnvType`.
- Claim 2 (task-aligned adaptation): compare against BayesSim-style fit proxy or non-task-driven tuning where possible.
- Claim 3 (sequential control): compare RL vs BayRn under equal real-evaluation call budget.
- Claim 4 (physical plausibility): report parameter trajectories and boundary-hit frequency.
- Claim 5 (robustness): leave-one-environment-out and unseen-location test splits.

## Suggested Language for Proposal “Approach” Paragraph

"Prior adaptive randomization methods (e.g., SimOpt, BayesSim, BayRn) improve transfer by tuning simulator distributions, but they do not jointly optimize an environment-conditioned, physically constrained policy using marine radar real-validation reward. We propose a deep RL outer-loop controller that selects bounded simulator updates conditioned on water-body type and recent real-data performance, targeting direct reduction of sim-to-real error under held-out environments."
