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
    - E1 (Trail Length): No single trail length is optimal across speed classes; stationary targets benefit from long trails while fast targets degrade sharply beyond N=3
    - E2 (Decay Function): Concave decay outperforms alternatives for moving targets by concentrating intensity near current position; step decay worst for fast targets
    - E3 (Intensity Encoding): Proportional encoding improves mixed-scene detection by preserving return-strength information for target discrimination
    - E4 (Color Mapping): Gradient color mapping aids moving target localization via implicit directional cue from hue shift across trail age

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
    - YOLOv8-nano, pretrained on COCO, fine-tuned 100 epochs
    - Learning rate 1e-3, batch size 16, input 640x640
    - Standard augmentation (random flip, mosaic, mixup)
    - Independent training run per condition; 3 seeds for confidence intervals
  - Evaluation: mAP50, precision, recall, F1

## 3. Results
- Result 1: Trail length and target speed (A1)
  - Stationary targets benefit monotonically from longer trails (saturation ~N=12)
  - Moving targets have speed-dependent optimum; fast targets degrade sharply beyond N=3
  - No single trail length is optimal across speed classes
- Result 2: Decay function (A2)
  - Concave decay best for moving targets (concentrates intensity near current position)
  - Step decay worst for fast targets (uniform-intensity streak)
- Result 3: Binary vs. proportional intensity (A3)
  - Minimal difference for strong-target-only scenes
  - Proportional improves mAP in mixed scenes (preserves return-strength discrimination)
- Result 4: Color mapping (A4)
  - Gradient mapping best for moving targets (implicit directional cue via hue shift)
  - All schemes similar for stationary targets
- Result 5: Range dependence (A5)
  - Near range: short trails optimal (N~3) due to large pixel displacement
  - Far range: long trails optimal (N~24) due to small pixel displacement
  - No single fixed trail length works across all ranges
- Result 6: Clutter interaction (A6)
  - Trails provide greatest benefit under heavy clutter (signal integration above clutter floor)
- Result 7: Target proximity / merging (A7)
  - Trails shift merging threshold from ~20m (no trail) to ~28m (N=12)
  - Cost of trails in dense target environments
- Result 8: Crossing trajectories (A8)
  - Shallow crossing angles + long trails produce severe detection degradation
  - Step decay worst (full-intensity overlap); exponential decay more resolvable

## 4. Limitations / Conclusion
- Results Summary
  - Trail rendering is not perceptually neutral for deep learning detectors
  - Optimal configuration depends jointly on speed, range, and scene complexity
  - Range-adaptive trail rendering motivated: short trails near, long trails far
  - Crossing trajectories are a significant degradation mechanism
- Limitations / Future Work
  - Synthetic data domain gap; validation needed on real Furuno DRS4D-NXT data
  - Only YOLOv8 tested; extend to Faster R-CNN, DETR, etc.
  - Implement range-adaptive rendering in real-time pipeline
  - Investigate trail parameter interaction with tracking algorithms
  - Evaluate effect on detector confidence calibration
