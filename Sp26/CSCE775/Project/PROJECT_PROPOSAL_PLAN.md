# CSCE 775 Project Proposal Ideation Plan (Radar-First, High Ambition)

## Brief Summary
By Friday, February 13, 2026, produce 4 polished proposal concepts aligned with the course rubric, centered on deep RL and available assets (separate marine radar logs, IR/RGB logs, 2 servers with 4x RTX 6000 Ada each). Primary recommendation: choose a radar sim-to-real RL core, with sensor fusion as a phase-2 extension. Concept 4 offers a lower-risk replication-plus-extension path based on a recent CVPR 2025 paper.

## Decision-Complete Proposal Concepts

## 1) Recommended Primary: Domain-Adaptive Synthetic Marine Radar via RL
- Goal: learn a policy that controls synthetic radar generator parameters so models trained on synthetic data perform best on real radar logs.
- Core RL framing:
  - State: current generator params + domain tag (`lake|river|coast`) + recent downstream validation metrics.
  - Action: continuous update to generator knobs (noise, clutter, reflection, attenuation, artifact priors).
  - Reward: improvement on real-log downstream task score minus realism penalties.
- Why this fits: strongest alignment with current data and 48-hour proposal timeline.
- Novelty angle: RL-based simulator control conditioned on water-body domain, not static hand-tuning.
- Baselines:
  - Fixed synthetic generator defaults.
  - Random/grid parameter search.
  - Bayesian optimization (non-RL baseline).
- Evaluation:
  - Split by environment type and by unseen locations.
  - Metrics: detection/segmentation F1 or mAP (task-dependent), calibration error, sim-to-real gap reduction, policy stability.
- Risks + fallback:
  - If reward noisy, use batched reward smoothing and constrained action bounds.
  - Fallback: contextual bandit instead of full RL.

## 2) Strong Secondary: RL-Optimized IR/RGB Registration + Augmentation Policy
- Goal: learn an RL policy that selects registration/augmentation strategies that maximize robustness on real multimodal data.
- Core RL framing:
  - State: frame quality cues, alignment residual proxies, environment tag.
  - Action: choose registration transform family + augmentation recipe.
  - Reward: downstream perception gain (for example, cross-modal consistency / tracking quality).
- Novelty angle: decision-making over transform/augmentation pipeline, not fixed preprocessing.
- Baselines:
  - Classical registration only.
  - Supervised registration net with fixed augmentation.
  - AutoAugment-style non-RL policy search.
- Evaluation:
  - Metrics: reprojection/alignment error, downstream task gain, robustness under weather/lighting shifts.
- Scope control:
  - Keep as independent proposal option or extension to Concept 1 if time allows.

## 3) High-Risk Vision: Battery-Aware Multi-Sensor Exploration in Unseen Waters
- Goal: policy for navigation that maximizes information gain while respecting battery constraints across lakes/rivers/coasts.
- Core RL framing:
  - State: fused IR/RGB/radar observations + belief map + remaining energy + inferred water-body type.
  - Action: motion/control command + sensor duty-cycling choice.
  - Reward: information gain - energy cost - safety penalties.
- Novelty angle: joint perception-action-energy optimization with environment-type adaptation.
- Baselines:
  - Frontier exploration with fixed sensor schedule.
  - Energy-unaware RL exploration.
  - Rule-based mission planner.
- Evaluation:
  - Metrics: map entropy reduction per Wh, coverage %, mission success rate, collision/safety violations.
- Major risk:
  - Integration complexity likely too high for core semester scope unless simplified simulator exists.

## 4) Low-Risk Replication + Extension: RL-Optimized Point Prompts for Interactive Segmentation
- Goal: replicate and extend Plug-and-Play PPO (Liu et al., CVPR 2025), which trains an RL agent to iteratively place point prompts that maximize SAM segmentation quality.
- Reference: Liu, X., Wang, R., Lai, Y., Shi, G., Shao, F., Hao, F., ... & Zheng, W. (2025). Plug-and-Play PPO: An Adaptive Point Prompt Optimizer Making SAM Greater. CVPR 2025, pp. 4332-4342.
- Code: https://github.com/XueyuLiu/PPO
- Core RL framing (from paper):
  - State: image features + current segmentation mask + dual-space heterogeneous graph encoding.
  - Action: point coordinates and labels (positive/negative prompts).
  - Reward: IoU / Dice score improvement over current segmentation.
  - Policy: PPO-trained policy network that iteratively refines prompt distribution.
- Why this fits: clean RL formulation, published codebase, standard datasets, low integration risk.
- Novelty angle (proposed extensions, pick 1-2):
  1. Algorithm comparison: replace PPO with SAC or TD3 (continuous action space for point coordinates) and compare sample efficiency and final performance.
  2. Domain transfer: apply trained prompt optimizer to a new domain (marine IR/RGB imagery, satellite imagery, or medical imaging not in the original evaluation).
  3. SAM 2 extension: adapt the prompt optimizer for video segmentation with SAM 2, where temporal consistency matters.
  4. Reward shaping: boundary-weighted IoU or class-balanced rewards to improve performance on thin structures or rare classes.
- Baselines:
  - Manual point prompts (center-of-mass, random).
  - Grid-based prompt placement.
  - Original PPO paper results (direct replication).
  - Non-RL prompt selection (greedy heuristic, Bayesian optimization).
- Evaluation:
  - Datasets: Pascal VOC, FSS-1000, KVASIR-SEG (from original paper), plus extension domain.
  - Metrics: IoU, Dice coefficient, number of prompts to reach target quality, inference time.
  - Ablations: with/without dual-space graph, different RL algorithms, reward function variants.
- Risks + fallback:
  - Low risk overall due to existing codebase and standard benchmarks.
  - If extension domain lacks labels, use pseudo-labels from SAM with manual verification on a small subset.
  - Fallback: pure replication with thorough ablation study still satisfies course requirements.

## RL Method Choice (Beginner-Friendly Defaults)
- Default for Concepts 1/2: off-policy continuous-control RL (SAC first, TD3 backup).
- Why:
  - Sample efficient (good for expensive evaluations).
  - Handles continuous parameter tuning naturally.
  - Stable with replay buffer and reward normalization.
- Keep PPO as optional baseline only.

## Important Interfaces / Types to Define in Proposal
- `EnvType`: `{lake, river, coast}` (sequence-level label, no object labels required).
- `GeneratorParamVector theta`: continuous synthetic radar control vector.
- `PolicyInput x_t`: sensor stats + env tag + task metrics + resource state.
- `PolicyAction a_t`:
  - Concept 1: `delta_theta`
  - Concept 2: transform/augmentation selection
  - Concept 3: navigation + sensor scheduling command
  - Concept 4: point coordinates `(x, y)` + label (positive/negative)
- `Reward r_t`: task gain terms, realism terms, and optional energy penalty (Concepts 1-3); IoU/Dice delta (Concept 4).
- Data split contract:
  - train/val/test separated by location and environment to prevent leakage.

## Test Cases and Scenarios (for proposal evaluation section)
1. In-domain transfer: train and test within same environment type.
2. Cross-domain transfer: train on two environment types, test on held-out third.
3. Unseen-location robustness: same environment type, new geography.
4. Low-SNR stress test: evaluate clutter/noise robustness.
5. Ablation:
   - no RL control
   - RL without environment conditioning
   - RL with full conditioning
6. Efficiency test (especially Concept 3): information gain per unit energy.

## What You Will Write in the Actual Proposal (Rubric Mapping)
- Introduction: problem significance in marine autonomy and sim-to-real gap.
- Approach: MDP/POMDP formulation, chosen RL algorithm, novelty vs prior work.
- Evaluation: datasets, splits, baselines, metrics, ablations, success thresholds.
- Conclusion: expected contribution and measurable outcomes.
- References: at least 4 (target 6-8, with NeurIPS/ICLR/ICML/RLC/AAAI sources).

## Assumptions and Defaults Chosen
- Team size: 3.
- Timeline: proposal direction locked by February 13, 2026.
- Risk profile: high ambition, with fallback path.
- Data: separate radar and IR/RGB datasets; no combined paired dataset required for primary concept.
- Labels: environment-type labels available; no object-level labels.
- Fusion scope: phase-2 extension, not core requirement for primary proposal.
- Novelty preference: mostly novel method.
- Default recommendation: pursue Concept 1 as primary submission, keep Concept 2 as backup/extension, frame Concept 3 as long-horizon stretch, and consider Concept 4 as the safest fallback (replication + extension with existing code and data).
