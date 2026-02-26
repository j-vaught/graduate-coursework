# Paper Outline: Effect of Echo Trail Parameters on YOLO-Based Target Detection in Simulated Marine Radar Imagery

## 1. Motivation / Introduction
- Why do this and why it's important
  - Echo trails appear on every marine radar display but their effect on deep learning detectors has never been studied
  - IMO mandated trails on all shipborne radar (2004), but no empirical study has informed optimal configuration
  - Same scene rendered with different trail configs produces dramatically different detection outcomes
- What others have done
  - Signal processing side: CFAR (Rohling 1983), scan correlation (Kim et al. 2012), 3D-FFT filtering (Wen et al. 2022)
  - Deep learning side: CNN-LSTM on display imagery (Baird 2020), PPInet with YOLOv3 (Chen 2021), multi-frame fusion (DTNet 2025)
  - None examined how the existing trail accumulation in their input shaped detection
- What we did and how
  - First systematic investigation of echo trail parameters on ML detection
  - RCS-based radar simulator generating PPI imagery + configurable trail rendering + YOLOv8
  - Eight sequential ablation experiments isolating one parameter each
  - Key findings from core parameter experiments (E1-E4):
    - E1 (Trail Length): Overall mAP50 rises from 0.675 (N=0) to 0.918 (N=25) in no-clutter (+24.3pp), but in clutter peaks at 0.720 (N=15) then regresses to 0.669 (N=25) -- below baseline. Fast targets saturate by N=3 (+34.7pp jump from 0.488 to 0.836). Slow targets in clutter lose recall from 0.681 (N=0) to 0.491 (N=25).
    - E2 (Decay Function): Exponential best in clean conditions (mAP50=0.898), step best in clutter (0.700). No single function dominates both. Concave worst in clutter (0.669, 24.9% degradation). Slow targets in clutter are a hard floor (<0.31 mAP50) for all functions.
    - E3 (Intensity Encoding): Binary leads in clean conditions (+3.45pp, 0.872 vs 0.837), proportional leads narrowly in clutter (+0.34pp). Binary suffers 21.8pp clutter penalty vs proportional's 18.1pp. Moving targets show the sharpest reversal: binary +4.85pp clean, proportional +2.50pp clutter.
    - E4 (Color Mapping): Gradient best in no-clutter (0.871), intensity best in clutter (0.670). Any color encoding outperforms mono by 9-13+ mAP50 points. Gradient achieves 0.904 moving mAP50 (no-clutter). Intensity is most clutter-robust (17.2% relative drop vs 23.4% for gradient).

## 2. Method
- Rendering Radar Frames
  - Clutter
    - K-distributed sea clutter model + additive white Gaussian noise
  - Objects
    - RCS-based target modeling (positions, RCS profiles, motion trajectories)
    - Radar range equation for received power at each range-bearing cell
    - Output matches Furuno DRS4D-NXT format (4-bit intensity, polar-to-Cartesian)
  - Echo Trail Implementation
    - Post-processing layer: displayed intensity = max of weighted history over N scans
    - Four decay functions: exponential, concave, linear, step
    - Trail intensity encoding: binary vs. proportional
    - Color mapping: monochrome, two-tone, gradient, intensity-mapped
- Experimental Setup
  - Ablation structure: eight sequential experiments (A1-A8), each varying one parameter
  - Scene configurations: A (isolated stationary), B (isolated moving), C (mixed), D (heavy clutter), E (close-spaced), F (crossing trajectories)
  - 500 PPI frames per scene at 24 RPM; 400 train / 100 test split
  - YOLO Parameters
    - YOLOv8-nano, pretrained on COCO, fine-tuned 50 epochs
    - Learning rate 1e-3, batch size 16, input 640x640
    - Standard augmentation (random flip, mosaic, mixup)
    - Independent training run per condition
  - Evaluation: mAP50, mAP50-95, precision, recall
  - Ground truth: stationary (750 instances), slow (263), medium (216), fast (402)

## 3. Results

### E1: Trail Length and Target Speed (A1)
- **No-clutter overall mAP50:** monotonic rise from 0.675 (N=0) to 0.918 (N=25); steep gain N=0 to N=4 (+17pp), diminishing returns thereafter (+7pp from N=4 to N=25)
- **Clutter overall mAP50:** peaks at 0.720 (N=15), regresses to 0.669 at N=25 -- below N=0 baseline (0.671). Clutter-induced ceiling and optimal trail-length crossover.
- **By speed tier (no-clutter):**
  - Stationary: 0.339 (N=0) to 0.793 (N=20), slight regression at N=25 (0.759)
  - Slow: 0.449 (N=0) to 0.778 (N=25), non-monotonic with trough at N=5 (0.562)
  - Medium: 0.431 (N=0) to 0.848 (N=25), erratic with dip at N=10 (0.643)
  - Fast: 0.488 (N=0) to 0.884 (N=25); +34.7pp jump at N=3 (0.836), effectively saturated by N=10 (0.864)
- **By speed tier (clutter):**
  - Stationary: peaks at N=3 (0.580), mild variation across N
  - Slow: **most striking failure** -- peaks at N=1 (0.383), collapses to 0.207 at N=25. Recall drops from 0.681 (N=0) to 0.491 (N=25)
  - Medium: peaks at N=15 (0.446), modest and not sustained
  - Fast: stable 0.468-0.568 range, peak at N=10 (0.568)
- **Precision = 1.0 for all moving subclasses** (slow/medium/fast) in both conditions across all N. Zero false positives on moving targets; all errors are missed detections.
- **Clutter gap widens with N:** negligible at N=0 (0.004pp), reaches 0.249pp at N=25. Trail representation that benefits clean scenes is most distorted by clutter.
- **Optimal N:** No-clutter practical optimum N=10-15 (captures ~97% of achievable gain). Clutter: N=10 overall sweet spot; never exceed N=15. For slow targets in clutter, N=1 or none.

### E2: Decay Function (A2)
- **No-clutter overall mAP50:** Exponential 0.898 > Concave 0.892 > Linear 0.891 > Step 0.885 (1.3pp spread)
- **Clutter overall mAP50:** Step 0.700 > Exponential 0.691 ~ Linear 0.691 > Concave 0.669
- **By speed tier (no-clutter):**
  - Stationary: all clustered (0.768-0.792), linear marginally best
  - Slow: exponential best (0.731), linear worst (0.672)
  - Medium: step best (0.765), linear worst (0.643) -- 12.2pp gap
  - Fast: exponential best (0.891), step worst (0.853)
- **By speed tier (clutter):**
  - Stationary: linear best (0.600)
  - Slow: all catastrophically degraded (<0.311 mAP50 for all functions) -- structural limitation
  - Medium: **step dominates** at 0.495, 9.5pp above nearest competitor (linear 0.400)
  - Fast: exponential and linear tied (~0.569)
- **Stationary/moving inversion under clutter:** In clean conditions, moving > stationary for all functions (+0.016 to +0.048). Under clutter, this reverses: stationary > moving (-0.032 to -0.076). Concave shows largest reversal (-0.076).
- **Clutter robustness:** Step most robust (20.9% relative drop), concave worst (24.9%)
- **Moving-target precision in clutter:** Step has worst precision (0.566) but best recall (0.700) -- high false-positive rate
- **Recommendation:** Exponential for clean conditions; step for cluttered/unknown environments. Concave should be avoided operationally.

### E3: Binary vs. Proportional Intensity (A3)
- **No-clutter overall mAP50:** Binary 0.872 vs Proportional 0.837 (+3.45pp binary advantage)
- **Clutter overall mAP50:** Binary 0.653 vs Proportional 0.657 (+0.34pp proportional, within noise)
- **Per-class no-clutter:** Binary leads both classes; moving advantage larger (+4.85pp) than stationary (+2.06pp)
- **Per-class clutter reversal:** On moving targets, binary leads +4.85pp clean but **falls behind** -2.50pp under clutter. Proportional's amplitude gradient becomes a genuine discriminative cue when clutter contaminates at uniform intensity.
- **Clutter fragility:** Binary encoding: 21.8pp clutter penalty. Proportional: 18.1pp. Moving targets bear the brunt -- binary loses 28.3pp on moving vs proportional's 21.0pp.
- **Speed tiers (no-clutter):** Binary leads slow (+4.12pp) and fast (+1.12pp); medium tied (0.286 vs 0.286)
- **Speed tiers (clutter):** Fast targets show sharpest reversal -- proportional +1.58pp mAP50, +2.78pp mAP50-95 (better localization)
- **Peak training performance:** Nearly identical (binary 0.922 at epoch 34, proportional 0.923 at epoch 29). Gap in final evaluation is convergence stability, not capacity.
- **Medium tier hardest for both** encodings across all conditions (~0.286 mAP50 no-clutter, ~0.24 clutter)

### E4: Color Mapping (A4)
- **No-clutter overall mAP50:** Gradient 0.871 > Twotone 0.837 > Intensity 0.810 > Mono 0.736
- **Clutter overall mAP50:** Intensity 0.670 > Gradient 0.667 > Twotone 0.657 > Mono 0.576
- **Core finding:** Any color encoding outperforms grayscale mono by 9-13+ mAP50 points. Color mapping is functionally meaningful, not cosmetic.
- **No-clutter by class:**
  - Moving: gradient best (0.904), mono worst (0.758); gradient recall = 0.936 (highest across all conditions)
  - Stationary: gradient marginally best (0.838), compressed spread across schemes
- **Clutter by class -- rank inversion:**
  - Stationary: **intensity best** (0.739), 5+ points ahead of all others. Return-strength encoding distinguishes persistent targets from transient clutter.
  - Moving: gradient still best (0.653), mono worst (0.503)
- **Speed tiers (no-clutter):**
  - Slow: gradient dominates (0.416), nearly doubles intensity (0.269)
  - Medium: mono unexpectedly leads (0.343) in both conditions -- anomalous
  - Fast: intensity best (0.655), followed by twotone (0.612)
- **Speed tiers (clutter):**
  - Slow: gradient still best (0.228); mono collapses to 0.105 (lowest score in entire experiment)
  - Medium: mono again leads (0.299) -- consistent anomaly
  - Fast: twotone leads (0.523)
- **Clutter robustness:** Intensity most robust (17.2% relative drop), gradient least robust (23.4%)
- **Stationary/moving inversion under clutter:** All schemes show moving > stationary in clean, stationary > moving in clutter. Systematic effect independent of color scheme.
- **Training dynamics:** Twotone peaks highest (0.923 at epoch 29) but overfits; gradient peaks slightly lower (0.918 at epoch 30) but generalizes better. Mono slowest to converge (peaks at epoch 44).
- **Precision globally low** (max 0.470) across all schemes -- dataset-level characteristic, not scheme-specific.

### E5-E8 (Pending Data)
- E5: Range dependence -- no data yet
- E6: Clutter interaction -- no data yet
- E7: Target proximity / merging -- no data yet
- E8: Crossing trajectories -- no data yet

## 4. Limitations / Conclusion
- Results Summary
  - Trail rendering is not perceptually neutral for deep learning detectors
  - Optimal configuration depends jointly on speed, range, and scene complexity
  - No single trail length optimal: fast targets saturate by N=3, stationary need N=10-15, slow targets in clutter actively harmed by longer trails
  - No single decay function dominates: exponential best clean (0.898), step best clutter (0.700)
  - Binary vs proportional: binary wins clean (+3.45pp), proportional more clutter-robust (18.1pp vs 21.8pp penalty)
  - Gradient color mapping best overall for no-clutter (0.871), intensity most clutter-robust (17.2% drop)
  - Any color encoding >> mono (9-13pp advantage)
  - Clutter inverts stationary/moving performance ranking for all parameter choices
  - Medium-speed targets are consistently the hardest tier across all experiments
  - Range-adaptive trail rendering motivated: short trails near, long trails far
- Limitations / Future Work
  - Synthetic data domain gap; validation needed on real Furuno DRS4D-NXT data
  - Only YOLOv8 tested; extend to Faster R-CNN, DETR, etc.
  - Implement range-adaptive rendering in real-time pipeline
  - Investigate trail parameter interaction with tracking algorithms
  - Evaluate effect on detector confidence calibration
  - Investigate medium-speed tier anomaly and mono's unexpected medium-tier performance
  - Slow targets in clutter represent a structural floor (~0.31 mAP50) that trail augmentation alone cannot solve -- needs upstream clutter suppression
