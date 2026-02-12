# Detailed Work Plan: Proposal 1 (RL-Tuned Synthetic Marine Radar)

## 1) Project Objective
Design a deep RL outer-loop controller that tunes synthetic marine radar generation parameters so downstream models trained on synthetic data perform better on real radar logs.

## 2) Core Hypothesis
Environment-conditioned simulator tuning (`lake`, `river`, `coast`) will reduce sim-to-real gap more than fixed randomization or non-RL optimization baselines.

## 3) Formal Problem Setup

### 3.1 Bi-Level Optimization
- Inner loop: train downstream model (MRISNet/FasterYOLO) on synthetic data from parameterized simulator state `theta`.
- Outer loop: SAC RL policy updates `theta` based on real-data validation rewards (mIoU).

### 3.2 Technical Depth: Radar Physics
- **Simulator Implementation:** Ray-tracing for multi-path; Elfouhaily spectrum for sea surface; RCS calculation for ships.
- **Environment Conditioning:** Separate policy heads or conditioning vectors for `lake`, `river`, `coast`.
- **Action Space:** Physically bounded updates to speckle, attenuation, clutter, and multipath gain.

### 3.3 RL State, Action, Reward
- State `s_t`: current `theta`, environment label, recent mIoU/F1 metrics, parameter history.
- Action `a_t`: bounded update to `theta`.
- Reward `r_t`: $\Delta \text{mIoU}_{real} - \text{penalties}$.

## 4) Data Protocol
- **Primary Real Data:** MOANA (2025) and PoLaRIS (2024) datasets for multi-radar and multi-modal validation.
- Use sequence-level environment labels for conditioning.
- Train/val/test split by location/route to ensure no data leakage.
- Explicitly test on held-out environments (e.g., train on lake/river, test on coast).

## 5) Baselines and Ablations
1. Fixed synthetic generator defaults.
2. Uniform random domain randomization.
3. Bayesian optimization over generator parameters.
4. RL without environment conditioning.
5. RL with environment conditioning (primary model).
6. Optional fallback: contextual bandit outer-loop tuner.

## 6) Evaluation Plan

### 6.1 Primary Metrics
- Real-data downstream task score (main task).
- Relative sim-to-real gap reduction.

### 6.2 Secondary Metrics
- Cross-domain holdout performance.
- Unseen-location robustness.
- Seed variance / policy stability.
- Evaluation-call efficiency (real validation budget).

### 6.3 Stress Tests
- Low-SNR/high-clutter cases.
- Potential weather-shift slices if available.

## 7) Risk Register and Mitigation
1. Noisy reward: average repeated evaluations, EMA smoothing.
2. Sample inefficiency: low-dimensional warm-start then expand.
3. Overfitting to one environment: leave-one-environment-out validation.
4. Unrealistic simulator exploitation: bounded actions and plausibility penalties.

## 8) Literature Integration Plan
Use `papers/paper_manifest.csv` to track evidence categories:
- Sim-to-real foundations.
- Adaptive/randomized simulation optimization.
- Radar-specific transfer methods.
- Maritime datasets and benchmarks.

For each paper, capture:
- Method summary.
- Relevance to Proposal 1.
- Strengths/limitations.
- How it affects baseline or design choices.

Use `plans/proposal1_related_work_matrix.md` as the canonical mapping from prior work to:
- explicit limitation in this project context,
- concrete method delta to claim,
- and exact ablation needed to validate that delta.

## 9) 8-Week Execution Roadmap
1. Week 1: lock metric, split protocol, and parameter list.
2. Week 2: fixed/random/Bayesian baseline curves.
3. Week 3: SAC outer-loop implementation on reduced parameter subset.
4. Week 4: full parameter set + environment-conditioned variant.
5. Week 5: holdout environment and unseen-route tests.
6. Week 6: failure and realism analysis.
7. Week 7: optional extension (secondary task or camera linkage).
8. Week 8: final report, figures, and reproducibility package.

## 10) Proposal Writing Deliverables
- IEEE primary draft (`drafts/proposal1_ieee.tex`).
- ASME alternate draft (`drafts/proposal1_asme.tex`).
- Final PDFs in `final/`.

## 11) Acceptance Criteria
- At least one RL variant beats all non-RL baselines on real-data metric.
- Improvement is reproducible across multiple seeds.
- Method and evaluation are fully documented with references and split protocol.

## 12) Required Novelty Narrative for Proposal Text
Your proposal must state improvements over existing work as testable claims:
1. Prior methods use fixed/random or non-sequential adaptation; we add a sequential RL outer loop.
2. Prior methods are not explicitly conditioned on maritime environment type; we include `lake/river/coast` conditioning.
3. Prior tuning is often similarity/calibration-driven; we optimize real downstream task reward directly.
4. Prior methods may allow unrealistic randomization; we enforce physically bounded radar-parameter control.

Each claim must be paired with one ablation or comparator in the Evaluation section.
