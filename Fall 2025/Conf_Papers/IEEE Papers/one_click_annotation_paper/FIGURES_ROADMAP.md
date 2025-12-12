# Marine Radar Paper: Figures Roadmap

**Paper Title:** RADAR300 Pretraining and Open-Source Tools for Marine Radar Object Detection in Inland and Coastal Waters

**Project:** IEEE SoutheastCon 2026 submission

**Document Purpose:** Track all figure needs across paper sections to enable consistent visualization planning across work sessions.

---

## Executive Summary: Top 15 "Must-Have" Figures

These figures provide the greatest impact for reader understanding and paper completeness:

1. **Pipeline diagram** (pretraining/conversion/echo trails) — conceptual clarity
2. **Example dataset frames** (RADAR300 + USC labeled) — what you're working with
3. **Echo-trail progression visualization** — core novelty
4. **Pretraining effect bar chart** — main result
5. **Echo-trail performance curve** — secondary result
6. **Detection qualitative examples** (TP/FN/FP grid) — proof of work
7. **Pohang generalization examples** — cross-dataset validation
8. **Annotator GUI screenshot** — tool contribution
9. **Data distribution** (time of day, weather) — reproducibility
10. **Failure case analysis** — honesty about limitations
11. **Network architecture diagrams** — for reproducibility
12. **Dataset comparison** (RADAR300 vs. Canal) — shows domain shift
13. **Per-class AP breakdown** — nuance in results
14. **Geographic collection map** — context
15. **Furuno NXT hardware photo** — authenticity

---

## Status Tracking

| # | Figure Title | Section | Status | Notes |
|---|---|---|---|---|
| 1 | Operational context photo | Introduction | ✅ DONE | Radar hardware mounted on vessel |
| 2 | Modality comparison | Introduction | ✅ DONE | Radar vs. camera vs. LiDAR |
| 3 | Geographic map | Introduction | ✅ DONE | Collection sites |
| 4 | RADAR300 samples | Datasets | ⏳ PENDING | 4-6 frames with detections |
| 5 | USC Canal dataset examples | Datasets | ⏳ PENDING | Labeled frames with bboxes |
| 6 | Dataset comparison grid | Datasets | ⏳ PENDING | RADAR300 vs. USC side-by-side |
| 7 | Class distribution histograms | Datasets | ⏳ PENDING | Dynamic/static counts + sizes |
| 8 | Temporal coverage heatmap | Datasets | ⏳ PENDING | Time of day vs. date for 196K frames |
| 9 | Pohang Canal preview | Datasets | ⏳ PENDING | 2-3 sample frames for generalization |
| 10 | Furuno NXT hardware photo | Radar Acq. | ✅ DONE | Actual unit with annotations |
| 11 | Range-azimuth coordinate diagram | Radar Acq. | ⏳ PENDING | Polar grid explanation |
| 12 | Raw polar data visualization | Radar Acq. | ⏳ PENDING | Before/after quantization (4-bit) |
| 13 | Conversion pipeline steps | Radar Acq. | ⏳ PENDING | Polar → Cartesian → PNG |
| 14 | Conversion examples | Radar Acq. | ⏳ PENDING | 3-4 frames at different range settings |
| 15 | Echo-trail generation visualization | Radar Acq. | ⏳ PENDING | T, T-1, T-2, T-3 with opacity decay |
| 16 | Echo-trail variants | Radar Acq. | ⏳ PENDING | T=1, T=4, T=8, T=16 comparison |
| 17 | Motion visualization | Radar Acq. | ⏳ PENDING | Moving boat with velocity vectors |
| 18 | YOLO-style architecture diagram | Detectors | ⏳ PENDING | Backbone → FPN → heads |
| 19 | Faster R-CNN architecture diagram | Detectors | ⏳ PENDING | RPN → proposals → classification |
| 20 | Anchor box analysis | Detectors | ⏳ PENDING | Boat bbox statistics |
| 21 | Training curves | Detectors | ⏳ PENDING | Loss vs. epoch (RADAR300 + fine-tune) |
| 22 | Learning rate schedule | Detectors | ⏳ PENDING | LR drop visualization |
| 23 | Annotator GUI screenshot | Toolchain | ⏳ PENDING | Full interface with controls |
| 24 | Annotator workflow diagram | Toolchain | ⏳ PENDING | load → adjust → draw → label → export |
| 25 | Radar2PNG converter workflow | Toolchain | ⏳ PENDING | Raw files → PNG + metadata |
| 26 | Command-line usage examples | Toolchain | ⏳ PENDING | Code snippets for each tool |
| 27 | Toolchain integration diagram | Toolchain | ⏳ PENDING | All three tools in pipeline |
| 28 | Dataset split pie chart | Exp. Setup | ⏳ PENDING | 60/20/20 train/val/test allocation |
| 29 | Class imbalance chart | Exp. Setup | ⏳ PENDING | Dynamic vs. static counts |
| 30 | Metadata distribution | Exp. Setup | ⏳ PENDING | Range settings, time of day, conditions |
| 31 | Pretraining effect bar chart | Results | 🔴 PRIORITY | FS-Y, R300-Y, FS-F, R300-F comparison |
| 32 | Per-class AP breakdown | Results | 🔴 PRIORITY | Grouped bars for AP_dyn & AP_stat |
| 33 | Echo-trail performance curve | Results | 🔴 PRIORITY | mAP vs. trail length (T=1,4,8,16) |
| 34 | Per-class echo-trail effect | Results | ⏳ PENDING | Separate curves for dyn/stat |
| 35 | Precision-recall curves | Results | ⏳ PENDING | For FS-Y, R300-Y, R300T-Y |
| 36 | Qualitative detection examples | Results | 🔴 PRIORITY | TP/FN/FP grid with trail variants |
| 37 | Failure case analysis | Results | ⏳ PENDING | Hard examples (marinas, small, clutter) |
| 38 | Confusion matrix | Results | ⏳ PENDING | Dyn vs. static misclassifications |
| 39 | Confidence calibration curve | Results | ⏳ PENDING | Confidence vs. correctness |
| 40 | Performance by boat size | Results | ⏳ PENDING | mAP binned by bbox area |
| 41 | Performance by range setting | Results | ⏳ PENDING | mAP for each range scale |
| 42 | Temporal performance | Results | ⏳ PENDING | mAP by time of day |
| 43 | Weather performance | Results | ⏳ PENDING | mAP by condition |
| 44 | Pohang detections grid | Generalization | ⏳ PENDING | 6-8 frames with success examples |
| 45 | Pohang failure cases | Generalization | ⏳ PENDING | Where model struggles on new hardware |
| 46 | Pohang vs. USC comparison | Generalization | ⏳ PENDING | Domain gap visualization |
| 47 | Dataset shift visualization | Discussion | ⏳ PENDING | t-SNE or feature space plot |
| 48 | Echo-trail benefits by scene | Discussion | ⏳ PENDING | Which environments benefit most |
| 49 | Quantization effect comparison | Discussion | ⏳ PENDING | 4-bit vs. 8-bit hypothetical |
| 50 | Computational cost breakdown | Discussion | ⏳ PENDING | Inference time/memory YOLO vs. Faster R-CNN |
| 51 | Raw data format specification | Appendix | ⏳ PENDING | Furuno binary structure diagram |
| 52 | Hyperparameter sensitivity | Appendix | ⏳ PENDING | mAP vs. LR, batch size |
| 53 | Ablation study matrix | Appendix | ⏳ PENDING | Pretraining, trails, data aug impact |
| 54 | Collection site photos | Appendix | ⏳ PENDING | Real-world views of locations |
| 55 | Hardware comparison | Appendix | ⏳ PENDING | Other radar specs + imagery |

---

## Section-by-Section Breakdown

### Introduction (Figures 1–3)

#### 1. Operational Context Photo
- **What:** Furuno NXT radar mounted on vessel or shore-based mount
- **Shows:** Antenna rotation, power/control connections, typical deployment
- **Placement:** Early in Introduction to establish hardware context
- **Status:** ✅ DONE — `fig01_radar_hardware.png`

#### 2. Modality Comparison
- **What:** Side-by-side radar vs. camera vs. LiDAR imagery of same scene
- **Shows:** Radar superiority in rain, fog, darkness; limitations of other modalities
- **Key Points:**
  - Radar: green echoes on dark background (works in adverse weather)
  - Camera: RGB image (clear daylight only)
  - LiDAR: point cloud (limited by weather/occlusion)
- **Placement:** After discussing why radar matters for maritime autonomy
- **Status:** ✅ DONE — `fig02_modality_comparison.png`

#### 3. Geographic Map
- **What:** Map of southeastern US showing all data collection sites
- **Shows:** Lake Murray, Lake Greenwood, Lake Monticello (SC lakes), Portsmouth (Elizabeth River, VA), Charleston harbor, Folly Beach
- **Key Elements:** Color-coded by environment type (inland lakes, rivers, coastal)
- **Placement:** End of Introduction after describing collection campaign
- **Status:** ✅ DONE — `fig03_collection_map.png`

---

### Datasets Section (Figures 4–9)

#### 4. RADAR300 Samples
- **What:** 4–6 example frames from RADAR300 dataset
- **Shows:** Different boat detections, class distribution, typical appearance
- **Format:** Grid of raw radar frames with overlaid annotations
- **Purpose:** Give reader sense of source domain data
- **Status:** ⏳ PENDING

#### 5. USC Canal Dataset Examples
- **What:** Sample labeled frames from new canal dataset
- **Shows:** Both dynamic (moving boats) and static (moored/piers) classes
- **Format:** Grid of PNG frames with bounding boxes, class labels color-coded
- **Key:** Show scale variability, clutter, different range settings
- **Status:** ⏳ PENDING

#### 6. Dataset Comparison Grid
- **What:** Side-by-side RADAR300 vs. USC Canal samples
- **Shows:** Distribution shift visually (different echo patterns, clutter types)
- **Format:** 3 rows × 2 columns: RADAR300 on left, USC on right
- **Purpose:** Motivate need for fine-tuning and domain adaptation
- **Status:** ⏳ PENDING

#### 7. Class Distribution Histograms
- **What:** Bar charts showing class breakdown
- **Shows:** Number of dynamic vs. static objects per frame, object size distributions
- **Subplots:**
  - Histogram: objects per frame
  - Histogram: bbox area distribution (small/medium/large boats)
  - Bar: class counts in train/val/test splits
- **Purpose:** Quantify label imbalance and scale variety
- **Status:** ⏳ PENDING

#### 8. Temporal Coverage Heatmap
- **What:** Heatmap showing when 196K unlabeled frames were collected
- **Shows:** Time of day (rows) vs. date (columns); color intensity = frame count
- **Purpose:** Demonstrate environmental diversity (day/night/seasons)
- **Status:** ⏳ PENDING

#### 9. Pohang Canal Preview
- **What:** 2–3 sample frames from Pohang Canal dataset
- **Shows:** Different radar hardware, environment, traffic patterns
- **Purpose:** Preview the generalization target without using for training
- **Status:** ⏳ PENDING

---

### Radar Acquisition & Preprocessing (Figures 10–17)

#### 10. Furuno NXT Hardware Photo
- **What:** Actual radar unit with annotations
- **Shows:** Antenna, dome, connections, size reference
- **Annotations:** Point to key components (antenna, rotator, power, Ethernet)
- **Purpose:** Establish reproducibility with specific hardware
- **Status:** ✅ DONE — `fig01_radar_hardware.png`

#### 11. Range-Azimuth Coordinate System Diagram
- **What:** Schematic explaining polar grid layout
- **Shows:** 868 range bins (radial) × 600–1000 azimuth angles (angular)
- **Elements:**
  - Polar coordinate system diagram
  - Range bins along radii
  - Azimuth angles around circle
  - Example echo (boat) in polar space
- **Purpose:** Clarify raw data format for readers unfamiliar with radar
- **Status:** ⏳ PENDING

#### 12. Raw Polar Data Visualization
- **What:** Before/after of quantization visualization
- **Shows:** Effect of 4-bit quantization (16 non-zero levels + zero)
- **Subplots:**
  - Raw data with full dynamic range
  - Quantized 4-bit version (clearly visible banding)
  - Histogram of intensity levels
- **Purpose:** Explain data quality constraints and processing rationale
- **Status:** ⏳ PENDING

#### 13. Conversion Pipeline Steps
- **What:** Visual walkthrough of data transformation
- **Shows:** Four main stages:
  1. Raw range–azimuth grid (polar coordinates)
  2. Interpolation to Cartesian grid
  3. Grayscale intensity mapping
  4. Final 1735×1735 PNG output
- **Format:** Flow diagram with example outputs at each stage
- **Purpose:** Make preprocessing transparent and reproducible
- **Status:** ⏳ PENDING

#### 14. Conversion Examples
- **What:** 3–4 frames at different range settings
- **Shows:** Same scene at 0.5 nm, 1.5 nm, 3 nm range scales
- **Purpose:** Demonstrate scale variability in dataset (important for model generalization)
- **Status:** ⏳ PENDING

#### 15. Echo-Trail Generation Visualization
- **What:** Sequence showing temporal compositing
- **Format:** 4 columns × 2 rows:
  - Row 1: Individual frames (T, T-1, T-2, T-3) at original opacity
  - Row 2: Composite with decay (T fully opaque, T-1 at 70%, T-2 at 40%, T-3 at 10%)
  - Bottom: Final combined image with ghosting effect
- **Shows:** How motion becomes visually salient through trail overlay
- **Purpose:** Explain core novelty in temporal augmentation
- **Status:** ⏳ PENDING

#### 16. Echo-Trail Variants
- **What:** Side-by-side comparison of trail lengths
- **Format:** 4 columns showing same scene with T=1, T=4, T=8, T=16
- **Shows:** Trade-off between temporal context and ghosting/blur
- **Purpose:** Motivate trail-length ablation studies
- **Status:** ⏳ PENDING

#### 17. Motion Visualization
- **What:** Example of moving boat tracked across 4 frames
- **Shows:**
  - Individual frames showing boat position at t, t-1, t-2, t-3
  - Echo-trail composite with boat trajectory overlay (velocity vector)
- **Purpose:** Illustrate how echo trails provide motion cues without explicit tracking
- **Status:** ⏳ PENDING

---

### Detectors & Training Protocols (Figures 18–22)

#### 18. YOLO-Style Architecture Diagram
- **What:** Simplified block diagram of one-stage detector
- **Shows:**
  - Input: 1735×1735 grayscale image
  - Backbone: CNN layers with downsampling
  - FPN: Feature pyramid for multi-scale detection
  - Detection heads: Class + bbox predictions
  - Output: Confidence scores + bounding boxes
- **Format:** Flow diagram with layer dimensions noted
- **Purpose:** Enable reproducibility and architectural understanding
- **Status:** ⏳ PENDING

#### 19. Faster R-CNN Architecture Diagram
- **What:** Two-stage detector architecture
- **Shows:**
  - Backbone: ResNet-50 + FPN
  - RPN: Region proposal network
  - Proposal refinement: NMS and filtering
  - Classification & bbox regression heads
- **Format:** Flow diagram matching YOLO structure for comparison
- **Purpose:** Show architectural diversity in evaluated models
- **Status:** ⏳ PENDING

#### 20. Anchor Box Analysis
- **What:** Visualization of boat bounding box statistics in radar imagery
- **Shows:**
  - Scatter plot: width vs. height of annotated boats
  - Histogram: aspect ratios (width/height)
  - Histogram: object sizes (area in pixels)
  - Color-coded by class (dynamic vs. static)
- **Purpose:** Justify anchor box priors and detect scale biases
- **Status:** ⏳ PENDING

#### 21. Training Curves
- **What:** Loss vs. epoch plots
- **Shows:**
  - RADAR300 pretraining: training loss → convergence
  - Fine-tuning on canal: loss drops (transfer benefit)
  - Validation loss to detect overfitting
- **Subplots:** Separate for classification and bbox regression losses
- **Purpose:** Demonstrate training stability and convergence behavior
- **Status:** ⏳ PENDING

#### 22. Learning Rate Schedule
- **What:** Visualization of learning rate over time
- **Shows:**
  - Constant LR during pretraining (e.g., 10^-3)
  - Step decay or cosine annealing during fine-tuning (drops to 10^-4)
  - Epochs marked on x-axis
- **Purpose:** Document optimization hyperparameters
- **Status:** ⏳ PENDING

---

### Open-Source Toolchain (Figures 23–27)

#### 23. Annotator GUI Screenshot
- **What:** Screenshot of actual annotation tool interface
- **Shows:**
  - Loaded radar PNG image (centered)
  - Brightness/contrast sliders (side panel)
  - Class selector dropdown (dynamic/static)
  - Example bounding boxes already drawn (color-coded by class)
  - Frame navigation controls (prev/next/go-to)
  - Label export button
- **Purpose:** Showcase tool usability and feature set
- **Status:** ⏳ PENDING (may require tool implementation)

#### 24. Annotator Workflow Diagram
- **What:** Step-by-step process flow
- **Shows:** Icons/boxes for:
  1. Load radar PNG sequence
  2. Adjust brightness/contrast
  3. Draw bounding box
  4. Assign class label
  5. Export annotations to text file
- **Format:** Flowchart with arrows and small visual indicators
- **Purpose:** Document user workflow for other researchers
- **Status:** ⏳ PENDING

#### 25. Radar2PNG Converter Workflow
- **What:** Processing pipeline for raw data
- **Shows:**
  - Input: Raw Furuno `.dat` (or proprietary format) files
  - Processing steps: decode → interpolate → quantize → map colors
  - Output: PNG images + metadata JSON (parameters, timestamps, range settings)
- **Format:** Flow diagram with example I/O files
- **Purpose:** Explain reproducibility and parameter recording
- **Status:** ⏳ PENDING

#### 26. Command-Line Usage Examples
- **What:** Code snippets for each tool
- **Shows:**
  ```bash
  # Annotator
  python annotator.py --input-dir ./pngs --output ./labels.txt

  # Radar2PNG
  python radar2png.py --input raw_data/ --output pngs/ --resolution 1735

  # EchoTrail
  python echo_trail.py --frames pngs/ --output trails/ --length 4
  ```
- **Purpose:** Enable quick adoption and reproducibility
- **Status:** ⏳ PENDING

#### 27. Toolchain Integration Diagram
- **What:** Full pipeline showing all three tools
- **Shows:**
  - Input: Raw radar files from Furuno
  - Tool 1: Radar2PNG converter → PNG sequence + metadata
  - Tool 2: AnnotatorGUI → bounding boxes + class labels
  - Tool 3: EchoTrail generator → augmented composite frames
  - Output: Training-ready dataset with labels and metadata
- **Format:** Flow diagram with icons for each tool
- **Purpose:** Show how tools fit together in complete workflow
- **Status:** ⏳ PENDING

---

### Experimental Setup (Figures 28–30)

#### 28. Dataset Split Pie Chart
- **What:** Allocation of 96 labeled canal frames
- **Shows:**
  - ~58 training frames (60%)
  - ~19 validation frames (20%)
  - ~19 test frames (20%)
- **Purpose:** Document exact experimental split
- **Status:** ⏳ PENDING

#### 29. Class Imbalance Chart
- **What:** Bar chart of object counts
- **Shows:**
  - Number of dynamic objects in train/val/test
  - Number of static objects in train/val/test
  - Per-frame average (dyn/stat ratio)
- **Purpose:** Highlight class imbalance for future weighted loss discussion
- **Status:** ⏳ PENDING

#### 30. Metadata Distribution
- **What:** Multiple distribution charts
- **Subplots:**
  - Pie chart: range settings used (0.5 nm, 1.5 nm, 3 nm)
  - Pie chart: time of day (day/dusk/night)
  - Pie chart: weather (clear/rain/wind)
- **Purpose:** Show diversity of collection conditions
- **Status:** ⏳ PENDING

---

### Results Section (Figures 31–43) — HIGH PRIORITY

#### 31. Pretraining Effect Bar Chart 🔴 PRIORITY
- **What:** Main result comparing architectures and pretraining
- **Shows:**
  - X-axis: Configuration (FS-Y, R300-Y, FS-F, R300-F)
  - Y-axis: mAP@0.5
  - Bars grouped by architecture (YOLO vs. Faster R-CNN)
  - Colors: from-scratch (light) vs. pretrained (dark)
- **Expected Pattern:** Pretrained bars significantly taller than from-scratch
- **Purpose:** Quantify transfer learning benefit
- **Status:** 🔴 PRIORITY — Awaiting experimental results

#### 32. Per-Class AP Breakdown
- **What:** Grouped bar chart showing per-class performance
- **Shows:**
  - For each config: AP_dynamic and AP_static as separate bars
  - Color-coded (e.g., red=dynamic, blue=static)
  - Error bars if multiple runs exist
- **Purpose:** Reveal whether pretraining helps both classes equally
- **Status:** ⏳ PENDING

#### 33. Echo-Trail Performance Curve 🔴 PRIORITY
- **What:** mAP@0.5 vs. trail length
- **Shows:**
  - X-axis: Trail length T (1, 4, 8, 16)
  - Y-axis: mAP@0.5 on canal test set
  - Separate lines for different configs (FS-Y, R300-Y, R300T-Y)
  - Error bars showing variance
- **Expected Pattern:** Optimal T somewhere between 4–8, degradation at T=16
- **Purpose:** Quantify temporal augmentation benefit
- **Status:** 🔴 PRIORITY — Awaiting experimental results

#### 34. Per-Class Echo-Trail Effect
- **What:** Separate curves for dynamic vs. static classes
- **Shows:**
  - AP_dynamic vs. trail length
  - AP_static vs. trail length
  - Different lines/colors for each
- **Expected Pattern:** Trails help dynamic class more (motion cue), less benefit for static
- **Status:** ⏳ PENDING

#### 35. Precision-Recall Curves
- **What:** PR curves for main configurations
- **Shows:**
  - One curve per config (FS-Y, R300-Y, R300T-Y)
  - X-axis: Recall, Y-axis: Precision
  - Area under curve = AP
- **Purpose:** Show nuanced performance trade-offs
- **Status:** ⏳ PENDING

#### 36. Qualitative Detection Examples 🔴 PRIORITY
- **What:** Grid of detection results organized by category
- **Format:** 3 rows × 3-4 columns:
  - **Row 1: True Positives** — Well-detected boats (dynamic & static mix)
  - **Row 2: False Negatives** — Missed boats with ground truth annotations
  - **Row 3: False Positives** — Spurious detections with red boxes
- **Variants:** For each example, show T=1 (single frame) next to T=4 or T=8 (with trail)
- **Purpose:** Provide intuitive understanding of model behavior and trail benefits
- **Status:** 🔴 PRIORITY — Awaiting model predictions

#### 37. Failure Case Analysis
- **What:** Hard examples where model struggles
- **Shows:**
  - Dense marinas with many boats
  - Very small boats at edge of detection range
  - Wake clutter confusing detector
  - Night-time images with low SNR
- **Format:** Grid with predictions overlaid, failure reason noted
- **Purpose:** Acknowledge limitations and guide future work
- **Status:** ⏳ PENDING

#### 38. Confusion Matrix
- **What:** 2×2 matrix for dynamic vs. static classification
- **Shows:**
  - Rows: true class, Columns: predicted class
  - Values: count of objects
  - Diagonal: correct predictions
  - Off-diagonal: misclassifications
- **Purpose:** Identify whether model confuses dynamic/static or just misses objects
- **Status:** ⏳ PENDING

#### 39. Confidence Calibration Curve
- **What:** Predicted confidence vs. actual correctness
- **Shows:**
  - X-axis: Predicted confidence (0–1)
  - Y-axis: Empirical correctness (0–1)
  - Points/bars binned by confidence level
  - Diagonal line = perfect calibration
- **Purpose:** Check if model confidence matches actual accuracy
- **Status:** ⏳ PENDING

#### 40. Performance by Boat Size
- **What:** mAP binned by object size
- **Shows:**
  - X-axis: Bounding box area (small/medium/large, or pixel ranges)
  - Y-axis: AP for each size bin
  - Separate lines for dynamic/static or configs
- **Purpose:** Identify scale-specific challenges (e.g., small boats hard to detect)
- **Status:** ⏳ PENDING

#### 41. Performance by Range Setting
- **What:** mAP for each radar range scale
- **Shows:**
  - X-axis: Range setting (0.5 nm, 1.5 nm, 3 nm)
  - Y-axis: AP
  - Bars for each config or class
- **Purpose:** Assess robustness to range scale variability
- **Status:** ⏳ PENDING

#### 42. Temporal Performance
- **What:** mAP by time of day
- **Shows:**
  - X-axis: Time categories (daytime, dusk, night)
  - Y-axis: AP
  - Separate bars or lines for configs/classes
- **Purpose:** Reveal whether pretraining/trails help in low-light conditions
- **Status:** ⏳ PENDING

#### 43. Weather Performance
- **What:** mAP by weather condition
- **Shows:**
  - X-axis: Weather (clear, rain, wind)
  - Y-axis: AP
  - Separate bars for configs/classes
- **Purpose:** Validate radar's claimed robustness in adverse conditions
- **Status:** ⏳ PENDING

---

### Qualitative Generalization: Pohang (Figures 44–46)

#### 44. Pohang Detections Grid
- **What:** 6–8 sample Pohang Canal frames with predictions
- **Shows:**
  - Radar images from Pohang dataset (different hardware)
  - Bounding boxes predicted by model trained on RADAR300 + USC canal
  - Green boxes for correct detections, red for false positives
- **Purpose:** Demonstrate cross-dataset generalization without retraining
- **Status:** ⏳ PENDING

#### 45. Pohang Failure Cases
- **What:** Examples where model struggles on Pohang hardware
- **Shows:**
  - Radar frames where predictions are missed or spurious
  - Comparison with annotated ground truth
  - Possible reasons (different antenna, quantization, clutter patterns)
- **Purpose:** Assess domain gap limitations
- **Status:** ⏳ PENDING

#### 46. Pohang vs. USC Comparison
- **What:** Side-by-side frames from two datasets
- **Shows:**
  - Left column: USC canal frames
  - Right column: Pohang frames
  - Annotations overlaid
  - Visual differences in echo patterns, noise, clutter
- **Purpose:** Illustrate domain shift visually
- **Status:** ⏳ PENDING

---

### Discussion Section (Figures 47–50)

#### 47. Dataset Shift Visualization
- **What:** Feature space plot (t-SNE or PCA) of RADAR300 vs. USC Canal
- **Shows:**
  - RADAR300 samples as one cluster (color 1)
  - USC canal samples as another cluster (color 2)
  - Separation visualizes domain gap
- **Purpose:** Explain why pretraining helps (same feature space)
- **Status:** ⏳ PENDING

#### 48. Echo-Trail Benefits by Scene Type
- **What:** Performance breakdown by scene complexity
- **Shows:**
  - Sparse scenes (few boats): compare T=1 vs. T=4
  - Cluttered scenes (many boats): compare T=1 vs. T=4
  - Line plot or bar chart showing AP by scene type
- **Purpose:** Explain when and why temporal context helps
- **Status:** ⏳ PENDING

#### 49. Quantization Effect Comparison
- **What:** Side-by-side visualization of 4-bit vs. hypothetical 8-bit
- **Shows:**
  - Left: Actual 4-bit quantized radar image (16 levels + zero)
  - Right: Synthetic 8-bit (smooth gradation)
  - Histogram showing level distribution
- **Purpose:** Contextualize data quality and preprocessing rationale
- **Status:** ⏳ PENDING

#### 50. Computational Cost Breakdown
- **What:** Inference time and memory usage comparison
- **Shows:**
  - Bar chart: inference time (ms) for YOLO vs. Faster R-CNN
  - Bar chart: GPU memory (MB) for each model
  - Optionally: training time comparison
- **Purpose:** Justify architectural choices (YOLO speed vs. Faster R-CNN accuracy)
- **Status:** ⏳ PENDING

---

### Appendix / Supplementary (Figures 51–55)

#### 51. Raw Data Format Specification
- **What:** Diagram or table of Furuno binary structure
- **Shows:**
  - Byte layout of raw sweep data
  - Range bin encoding
  - Azimuth angle encoding
  - Metadata fields (timestamp, range setting, antenna position)
- **Purpose:** Enable exact reproduction with other Furuno units
- **Status:** ⏳ PENDING

#### 52. Hyperparameter Sensitivity
- **What:** Small plots showing mAP variation with key hyperparameters
- **Shows:**
  - mAP@0.5 vs. learning rate (10^-4, 10^-3, 10^-2)
  - mAP@0.5 vs. batch size (8, 16, 32)
  - mAP@0.5 vs. weight decay (0, 1e-4, 1e-3, 1e-2)
- **Purpose:** Document hyperparameter robustness
- **Status:** ⏳ PENDING

#### 53. Ablation Study Matrix
- **What:** Heatmap showing impact of individual components
- **Shows:**
  - Rows: components (pretraining, echo-trails, data augmentation, etc.)
  - Columns: mAP metrics
  - Values: mAP@0.5 for each combination
  - Color intensity = performance
- **Purpose:** Isolate contribution of each technique
- **Status:** ⏳ PENDING

#### 54. Collection Site Photos
- **What:** Real-world photographs of data collection locations
- **Shows:**
  - Lake Murray (inland, scenic)
  - Charleston harbor (crowded, maritime traffic)
  - Marinas (dense boats, moored targets)
  - Portsmouth (river navigation context)
- **Purpose:** Add authenticity and context to dataset description
- **Status:** ⏳ PENDING (may require travel to sites)

#### 55. Hardware Comparison
- **What:** Specs table + example imagery for alternative radars
- **Shows:**
  - Table: Furuno NXT vs. other commercial radars (resolution, quantization, cost)
  - Side-by-side radar images from different hardware
  - Discussion of generalization potential
- **Purpose:** Position work relative to broader radar ecosystem
- **Status:** ⏳ PENDING

---

## Implementation Notes

### Python Figure Generation Priority Order
1. **First batch (for early submission draft):**
   - Figures 4–6 (RADAR300 & canal dataset samples)
   - Figure 13 (conversion pipeline)
   - Figure 15 (echo-trail visualization)

2. **Second batch (once data collected):**
   - Figures 31–33 (main results)
   - Figure 36 (qualitative detections)

3. **Third batch (polishing):**
   - Figures 7–9, 11–12, 14, 16–17 (acquisition details)
   - Figures 18–22 (architecture & training)

### Tools & Libraries
- **matplotlib** + **seaborn** — bar charts, curves, heatmaps
- **PIL/OpenCV** — radar image visualization, annotation overlay
- **scikit-learn** — t-SNE, confusion matrices
- **numpy/pandas** — data processing and statistics
- **tikzplotlib** or **pgfplots** — publication-quality plots directly in LaTeX

### TeX Integration
- All figures should reference `python_figures/` directory
- Use `\includegraphics[width=\linewidth]{python_figures/figXX_name.png}`
- Add proper captions and labels (`\label{fig:...}`) for cross-references
- Maintain consistent figure numbering and naming convention: `figXX_descriptive_name.png`

---

## Cross-References in Paper

- **Introduction:** Figures 1–3 introduce context, hardware, modality, geography
- **Datasets:** Figures 4–9 show what data looks like
- **Radar Acquisition:** Figures 10–17 explain preprocessing pipeline in detail
- **Detectors:** Figures 18–22 document model architectures
- **Toolchain:** Figures 23–27 showcase software contributions
- **Experimental Setup:** Figures 28–30 specify protocol
- **Results:** Figures 31–43 present quantitative and qualitative findings (HIGHEST IMPACT)
- **Generalization:** Figures 44–46 show cross-dataset transfer
- **Discussion:** Figures 47–50 provide deeper analysis
- **Appendix:** Figures 51–55 offer supplementary technical details

---

## Status Legend
- ✅ **DONE** — Figure generated and integrated into LaTeX
- 🔴 **PRIORITY** — Critical results figure awaiting experimental completion
- ⏳ **PENDING** — Ready to generate but not yet started

---

*Last Updated: 2025-12-11*
*Paper: RADAR300 Pretraining and Open-Source Tools for Marine Radar Object Detection*
*Venue: IEEE SoutheastCon 2026*
