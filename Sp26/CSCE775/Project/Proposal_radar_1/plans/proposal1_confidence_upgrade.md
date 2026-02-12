# Confidence Upgrade Brief for Proposal 1

## Why the Previous Version Felt Weak
- It described ideas but did not show enough quantified evidence.
- It cited related work without explicitly showing where non-RL baselines fail.
- It lacked a dedicated "results evidence" figure tying prior failures to our project motivation.

## What Is Added Now

### 1) Quantified Published Results (with failure cases)
- `results/published_results_summary.csv`
- `results/non_rl_failure_catalog.md`
- Key values now integrated into the proposal text and figure:
  - Trinh 2026 real radar transfer:
    - Occupancy balanced accuracy: RT baseline ~50, Random DR ~83, CDR ~97.
    - People counting balanced accuracy: RT baseline ~33, Random DR ~61, CDR ~72.
  - Kim 2024 synthetic-to-measured SAR transfer (Scenario 1, mean over 8 networks):
    - w/o Aug 47.86, Only Noise 68.41, Gamma+Noise 87.52, SSR 91.53.
  - SimOpt 2018 real-world transfer:
    - swing-peg-in-hole: 90% success (20 trials) after adaptation cycles.

### 2) New Full-Width Figures
- Existing method/system figures:
  - `drafts/figures/fig_method_pipeline.pdf`
  - `drafts/figures/fig_related_work_matrix.pdf`
- New published-results figure:
  - `drafts/figures/fig_published_evidence_results.pdf`
  - `drafts/figures/fig_published_evidence_results.svg`

### 3) Proposal Text Reinforcement
- Added explicit non-RL failure narrative and numeric evidence in:
  - `drafts/sections/03_evaluation.tex`
- Added figure integration in:
  - `drafts/proposal1_ieee.tex`

## What This Gives You
- A clear "existing methods fail here" story.
- A direct "our approach targets these specific failures" story.
- Quantitative motivation before running your own experiments.

## Remaining Gap (and Next Confidence Step)
You still need **your own preliminary project-specific result** (even a small one) to fully convince a reviewer.

### Minimum viable preliminary result to run next
1. Use one downstream radar task and one held-out environment split.
2. Compare three methods quickly:
   - fixed generator defaults,
   - random DR,
   - one adaptive tuner (Bayesian or simple RL).
3. Report one plot:
   - real-validation score vs number of evaluation calls.

Even one short experiment that shows adaptive > fixed/random will materially increase proposal confidence.
