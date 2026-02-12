# Non-RL Failure Catalog (Published Evidence)

This file summarizes where existing non-RL or weakly adaptive strategies fail, based on primary-source evidence.

## 1) Fixed/Uncalibrated Simulation Transfer Failure (Radar)
- Source: Trinh et al., 2026 (`trinh2026digitaltwin`)
- Failure evidence:
  - Real occupancy detection: RT baseline balanced accuracy ~50% (chance-level).
  - Real people counting: RT baseline balanced accuracy ~33% (near random for 3 classes).
- Interpretation:
  - Pure simulation training without calibrated adaptation fails to transfer reliably to real radar distribution shifts.

## 2) Generic Random DR Is Better but Still Insufficient
- Source: Trinh et al., 2026 (`trinh2026digitaltwin`)
- Evidence:
  - Occupancy: Random DR ~83% vs calibrated approach ~97%.
  - Counting: Random DR ~61% vs calibrated approach ~72%.
- Interpretation:
  - Non-targeted randomization helps but leaves substantial residual gap.

## 3) Synthetic-Only and Simple Noise Augmentation Failure (SAR)
- Source: Kim et al., 2024 (`kim2024soft`)
- Evidence (Scenario 1 mean over 8 networks):
  - w/o augmentation: 47.86% ATR accuracy.
  - only noise: 68.41%.
  - advanced clutter-aware randomization: 91.53%.
- Interpretation:
  - Basic non-adaptive augmentation does not adequately model real clutter/domain discrepancy.

## 4) SimOpt Operational Limitation
- Source: Chebotar et al., 2018 (`chebotar2018simopt`)
- Evidence:
  - Achieves 90% success after adaptation on swing-peg-in-hole (20 trials), but requires interleaved real rollouts and repeated update cycles.
- Interpretation:
  - Strong but operationally expensive; can be unstable/expensive when scaling to many parameters or repeated deployments.

## Why This Supports Proposal 1
- Proposal 1 targets exactly these gaps:
  1. Environment-aware adaptation (`lake/river/coast`).
  2. Sequential policy updates of simulator parameters.
  3. Reward directly tied to downstream real-data performance.
  4. Physically bounded updates to avoid unphysical exploitation.
