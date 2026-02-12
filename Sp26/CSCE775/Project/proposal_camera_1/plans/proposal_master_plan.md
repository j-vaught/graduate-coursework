# Detailed Work Plan: Proposal 2 (RL-Optimized IR/RGB Registration + Augmentation)

## 1) Project Objective
Design a deep RL policy that dynamically selects image registration transform families and augmentation recipes for paired IR/RGB marine data, maximizing downstream perception robustness and cross-modal consistency.

## 2) Core Hypothesis
A content-aware policy that adapts registration complexity and augmentation intensity based on frame quality and environmental context will outperform static preprocessing pipelines and fixed augmentation schemes (like standard AutoAugment) in varying marine conditions.

## 3) Formal Problem Setup

### 3.1 Adaptive Preprocessing Pipeline
- **Input:** Raw paired IR and RGB frames from marine datasets.
- **Policy Network (The Agent):** Observes frame statistics and chooses a preprocessing strategy.
- **Downstream Task:** Object detection or semantic segmentation model trained/evaluated on the processed data.
- **Feedback Loop:** The policy maximizes a reward signal derived from the downstream model's performance or consistency.

### 3.2 Technical Depth: Multimodal Alignment
- **Registration Primitives:** Rigid (simple), Affine (moderate), Homography (complex), B-Spline (deformable).
- **Augmentation Primitives:** MixUp, CutMix, Gaussian Blur, Thermal noise injection, Color jitter (RGB only), Intensity shift (IR).
- **Environment Conditioning:** Policy input includes tags for `day/night` and `rain/clear/fog`.

### 3.3 RL State, Action, Reward
- **State `s_t`:**
  - Frame quality metrics (Laplacian variance for blur, histogram entropy).
  - Initial misalignment proxy (e.g., mutual information score, edge correlation).
  - Environment tag (if available) or latent vector.
- **Action `a_t`:**
  - Discrete: Select Transform Family $T \in \{Rigid, Affine, Homography\}$.
  - Continuous/Discrete: Augmentation parameters $\lambda_{aug}$ (magnitude, probability).
- **Reward `r_t`:**
  - Supervised case: $\Delta 	ext{mAP}$ or $\Delta 	ext{IoU}$ on validation set.
  - Unsupervised/Self-supervised case: Cross-modal consistency loss (e.g., projection consistency between IR and RGB detections) - alignment cost.

## 4) Data Protocol
- **Primary Data:** Multi-spectral marine datasets (e.g., initialized from available raw logs or public datasets like M3FD, FLIR).
- **Splits:**
  - Train: Diverse conditions.
  - Test: Held-out distinct weather/lighting conditions (e.g., train day, test night) to prove robustness.
- **Ground Truth:** Uses dataset object labels for reward calculation in the supervised setting; uses geometric consensus for consistency checks.

## 5) Baselines and Ablations
1. **Classical Registration:** Fixed SIFT/ORB + RANSAC or Mutual Information maximization.
2. **Fixed Augmentation:** Standard supervised learning with fixed random augmentation (e.g., flip, crop).
3. **Randomized Search:** RandAugment-style policy (randomly select N ops with magnitude M).
4. **Offline Search:** AutoAugment (search for best fixed policy, then train).
5. **RL without Context:** Policy ignores frame quality/environment tags.
6. **Our Method:** Context-aware RL selecting both registration and augmentation.

## 6) Evaluation Plan

### 6.1 Primary Metrics
- **Downstream Accuracy:** mAP@50 or mIoU on real evaluation sets.
- **Alignment Error:** Mean Reprojection Error (MRE) on manually annotated keypoints (if available/feasible for subset).

### 6.2 Secondary Metrics
- **Robustness:** Performance drop under severe domain shifts (e.g., fog, glint).
- **Compute Efficiency:** Average inference time overhead of the policy vs. complex fixed registration.

### 6.3 Stress Tests
- **Misalignment Injection:** Artificially perturb IR/RGB calibration to test registration recovery.
- **Sensor Degradation:** Simulate thermal crossover or camera motion blur.

## 7) Risk Register and Mitigation
1. **Sparse Reward:** Training object detectors is slow; use a lightweight proxy model or "frozen backbone" for reward calculation.
2. **Action Space Explosion:** Discretize continuous augmentation parameters; restrict transform choices to 3 main families.
3. **Registration Collapse:** RL might choose "no registration" if initial alignment is "good enough" to avoid artifacts; enforce minimum alignment quality check.
4. **Data Scarcity:** Use pre-trained feature extractors (ResNet/VGG) to enrich state representation if raw pixel stats are insufficient.

## 8) Literature Integration Plan
Use `papers/paper_manifest.csv` to track:
- Differentiable registration methods.
- AutoML / AutoAugment literature.
- Multimodal sensor fusion challenges.

Use `plans/proposal_related_work_matrix.md` to map:
- Limitations of static pipelines.
- How our "dynamic choice" novelty contrasts with "search-then-freeze" methods.

## 9) 8-Week Execution Roadmap
1. **Week 1:** Setup data loader (IR/RGB), define evaluation metric (consistency/mAP).
2. **Week 2:** Implement baselines (Classical Reg, Fixed Aug).
3. **Week 3:** Design RL Environment (State: Image stats, Action: Reg+Aug).
4. **Week 4:** Train RL Agent (PPO or DQN) with lightweight reward proxy.
5. **Week 5:** Integrate full detection pipeline loop.
6. **Week 6:** Run ablation studies (no-context, random-policy).
7. **Week 7:** Analyze results on domain-shift splits (Day vs Night).
8. **Week 8:** Final report and proposal polish.

## 10) Proposal Writing Deliverables
- **IEEE Draft:** Focus on the "Robust Perception" angle.
- **ASME Draft:** Focus on the "Autonomous Systems / Sensor Fusion" angle.
- **Final:** `final/proposal2_ieee_final.pdf`.

## 11) Acceptance Criteria
- RL policy achieves higher mAP/mIoU than RandAugment and Fixed Registration on the hardest test split (e.g., night/fog).
- System demonstrates ability to switch strategies (e.g., stronger registration in high-motion frames).

## 12) Required Novelty Narrative
1. **Joint Optimization:** We optimize registration and augmentation jointly, whereas prior work treats them as separate stages.
2. **Instance-Level Adaptation:** We select strategies *per-frame* (or per-sequence) based on content, unlike AutoAugment which finds a global policy.
3. **Multimodal Focus:** Specific framing for IR/RGB fusion challenges (thermal crossover, varying FOV) absent in generic image augmentation papers.
