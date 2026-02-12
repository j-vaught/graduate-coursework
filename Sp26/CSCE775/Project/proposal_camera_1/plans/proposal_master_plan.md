# Detailed Work Plan: Proposal 2 (Context-Aware RL for IR/RGB Registration + Augmentation)

## 1) Goal and Decision Criterion
Train a policy that dynamically selects registration family and augmentation strength per frame/window to improve multimodal detection robustness under maritime shift conditions.

Success decision:
- Primary: higher mAP@50 than fixed-reg + fixed-augmentation baselines on hardest shift splits.
- Secondary: lower alignment error without unacceptable preprocessing latency increase.

## 2) Reproducible Environment Stack
- OS: Ubuntu 22.04.
- Python: 3.10.
- Core libs: PyTorch 2.x, OpenCV, Kornia, Stable-Baselines3, NumPy, pandas.
- Tracking: structured run directories + CSV metrics + action logs.
- Determinism: fixed split files, fixed random seeds (>=5).

Environment profile:
- `env_name`: `rgbt_rl_preprocess`
- `gpu`: required for detector loop; proxy-reward mode supports single GPU.

## 3) Data and Split Protocol
Candidate datasets:
- FLIR ADAS-style RGBT subsets.
- M3FD and maritime-focused IR/RGB benchmarks (WiseOD/M3OT/R-LiVIT as available).

Split rules:
- Train/val/test by sequence and condition, not random frame shuffle.
- Explicit domain-shift tests: day->night, clear->fog/rain, low-motion->high-motion.
- Misalignment stress split: controlled synthetic perturbations of extrinsics.

## 4) RL Problem Definition
State $s_t$:
- Blur/entropy/SNR proxies.
- Initial cross-modal mismatch score.
- Environment metadata (time/weather) when available.

Action $a_t$:
- Registration family: rigid/affine/homography.
- Augmentation parameters: modality-aware magnitude/probability vector.

Reward:
\[
r_t = \alpha\Delta\mathrm{mAP} + \beta\Delta\mathrm{consistency} - \gamma\mathrm{latency}.
\]

## 5) Model and Pipeline Components
Downstream detector options:
- Baseline: YOLO-family detector with fused IR/RGB channels.
- Strong comparator: discrepancy-aware fusion architecture from recent RGBT literature.

Preprocessing controllers:
- Classical baseline: feature-matching + RANSAC.
- Static learned baseline: AutoAugment/RandAugment policy.
- Proposed: PPO policy over joint reg+aug action space.

## 6) Training Schedule
Phase A (fast proxy training):
- Freeze detector backbone.
- Use proxy reward from lightweight head for rapid policy iteration.

Phase B (task-coupled refinement):
- Periodic full detector evaluation.
- Policy fine-tuning on real validation splits.

Phase C (generalization and stress):
- Held-out condition testing.
- Misalignment injection robustness.

## 7) Baselines and Ablations
Baselines:
1. Fixed classical registration + fixed augmentation.
2. Fixed classical registration + RandAugment.
3. AutoAugment/PBA static schedule.
4. Context-free RL (state ablation).

Ablations:
- Reg-only policy.
- Aug-only policy.
- Joint policy (proposed).
- Context channels removed one-by-one.

## 8) Metrics and Reporting
Primary:
- mAP@50 on held-out domain-shift splits.
- Mean reprojection error (subset with keypoint annotations).

Secondary:
- Robustness drop under synthetic misalignment.
- Inference-time preprocessing overhead (ms/frame).
- Action entropy and per-condition action distributions.

Statistical policy:
- >=5 seeds.
- 95% confidence intervals.
- Pairwise significance versus strongest static baseline.

## 9) Compute and Runtime Budget
- Detector training: 1-2 GPUs.
- Policy updates: single GPU acceptable with proxy reward.
- Experiment cap: fixed max policy updates per method for fair comparison.

Acceleration plan:
- Cache feature maps for early ablations.
- Early-stop configurations with dominated validation curves.

## 10) Week-by-Week Execution
1. Week 1: lock datasets, split files, and metric scripts.
2. Week 2: implement fixed-registration and fixed-augmentation baselines.
3. Week 3: implement RL environment + action/state encoders.
4. Week 4: proxy-reward policy training.
5. Week 5: full-loop policy fine-tuning with detector feedback.
6. Week 6: ablations and domain-shift evaluation.
7. Week 7: stress tests and failure analysis.
8. Week 8: final figures, reproducibility package, and polished draft.

## 11) Risks and Fallbacks
- Sparse reward from full detector retraining: use proxy-stage bootstrapping.
- Over-large action space: discretize magnitudes and prune low-impact transforms.
- Registration instability in low texture: confidence-gated fallback to rigid transform.
- Dataset inconsistency: enforce per-sequence metadata checks before training.

## 12) Deliverables
- Source-backed evidence figure and updated paper manifest.
- Reproducible configs and split manifests.
- Baseline/ablation tables with CIs and runtime overhead.
- Final IEEE draft with explicit novelty-to-test mapping.
