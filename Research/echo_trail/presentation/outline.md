# Beamer Presentation: Detailed Slide Outline
## Echo Trails: Systematic Ablation of Trail Parameters for ML-Based Marine Radar Detection
### J.C. Vaught — Update

---

## SECTION 1: INTRODUCTION (Slides 1-3)

### Slide 1: Title Slide
- **Title:** Effect of Echo Trail Parameters on YOLO-Based Target Detection in Simulated Marine Radar Imagery
- **Author:** J.C. Vaught
- **Affiliation:** University of South Carolina
- **Advisor(s):** Douglas Cahl, Yi Wang
- **Date:** 2026
- **Visual:** Brand garnet bar at top, black text, clean layout

### Slide 2: Motivation
- **Heading:** Why Study Echo Trails?
- **Content (narrative, not bullets):**
  - Echo trails appear on every marine radar display — they render returns from previous scans with progressively reduced intensity
  - IMO mandated trails on all shipborne radar in 2004 (MSC.192), yet no empirical study has examined how trail configuration affects ML detectors
  - Same radar scene rendered with different trail configs produces dramatically different detection outcomes for YOLOv8
- **Visual:** Include `fig0_splash.pdf` — the 4-panel TikZ figure showing No Trails (missed detection), Short Trails N=6 (correct), Long Trails N=24 (oversized box), Crossing Trails (merged targets)
- **Takeaway:** Trail rendering is not perceptually neutral for deep learning

### Slide 3: Research Questions & Contributions
- **Heading:** What We Investigate
- **Content:** Eight sequential ablation experiments, each isolating one parameter:
  - A1: How does trail length $N$ interact with target speed?
  - A2: Which decay function $f(k)$ is optimal?
  - A3: Binary or proportional intensity encoding?
  - A4: Which color mapping maximizes detection?
  - A5: How does optimal $N$ vary with target range?
  - A6: How do trails interact with sea clutter?
  - A7: At what separation do nearby targets merge?
  - A8: How do crossing trajectories degrade multi-target detection?
- **Contribution statement:** First systematic investigation of echo trail parameters on ML-based radar detection; fills a 20+ year gap between regulatory mandate and evidence-based optimization
- **Visual:** None needed; clean text layout with numbered list

---

## SECTION 2: RADAR COMPOSITOR (Slides 4-11)

### Slide 4: Furuno DRS4D-NXT Hardware
- **Heading:** Target Hardware: Furuno DRS4D-NXT
- **Content:**
  - X-band marine radar, 24 RPM antenna rotation
  - 868 range bins per pulse, 720 pulses per revolution (0.5 deg azimuth resolution)
  - 4-bit native intensity (0-15), upscaled to 8-bit (0-255) for processing
  - 3.0 nm maximum range, ~6.40 m per range bin
  - Output: polar CSV format (Status, Scale, Range, Gain, Angle, Echo0...Echo867)
- **Visual:** Schematic diagram of PPI display geometry — concentric range rings with labeled azimuth/range axes. Could be a simple TikZ showing the polar coordinate system with (pulse, bin) mapping.
- **Key point:** Our simulator matches this exact hardware specification

### Slide 5: Charleston Harbor Data
- **Heading:** Real-World Data Foundation: Charleston Harbor
- **Content:**
  - Source: Furuno DRS4D-NXT recordings from Grice Marine Lab, Charleston SC
  - Water/land annotation: `annotation_charleston.json` defines mask boundaries
  - 280 real background land frames (radar returns from land, bridges, structures)
  - 5,107 filtered radar target objects extracted via DBSCAN clustering
  - Each object: 2D echo pattern [pulse x range] with intensity, angular/range extent, area
  - Object detection config: min intensity 20, DBSCAN eps=3.0, min pts=3, area 10-10000 px
- **Visual:** Side-by-side: (left) water mask showing Charleston harbor boundaries, (right) example extracted object echo patterns at different sizes
- **Key point:** Real radar echoes ensure physically plausible target signatures

### Slide 6: Pipeline Overview
- **Heading:** Six-Stage Synthetic Radar Generation Pipeline
- **Content:** Describe each stage briefly:
  1. **Data Loading** — Validate annotations, water mask, object library
  2. **Scene Planning** — Compute trajectories, intensity profiles, per-frame placements
  3. **CSV Writing** — Polar radar data + YOLO labels in Furuno format
  4. **Image Rendering** — Polar-to-Cartesian conversion via precomputed LUT (1735x1735 px)
  5. **Trail Compositing** — Configurable echo trail rendering (the focus of this work)
  6. **Video Export** — Optional MP4 from frame sequence
- **Visual:** Include `fig_pipeline.pdf` — the horizontal flow diagram: RCS Simulator → Raw PPI → Trail Renderer → Trailed PPI → YOLOv8 Detector → mAP50. Annotation arrow showing ($N$, $f(k)$, encoding, color) feeding into Trail Renderer.
- **Key point:** Trail rendering is a post-processing layer — all other parameters held constant across ablations

### Slide 7: Object Placement & RCS Model
- **Heading:** Target Modeling: RCS-Based Object Placement
- **Content:**
  - Objects selected from library by size category, placed at valid water positions
  - Placement via MAX-blending: $\text{frame}[p][b] = \max(\text{current}, \text{object echo})$
  - Intensity engine controls per-frame scaling:
    - Profiles: constant, ramp, sine, custom expression
    - Variability: random jitter $\pm$10\% per frame
    - Flicker: state machine with random dwell durations (simulates intermittent returns)
  - Objects inherit implicit RCS from real extraction — no analytical radar equation needed
- **Visual:** Diagram showing an object echo pattern being MAX-blended onto a background frame at position (pulse, bin). Annotate with intensity scaling factor.
- **Key point:** MAX-blending matches radar physics — stronger return always dominates

### Slide 8: Motion & Path Planning
- **Heading:** Target Motion: Speed Classes and Trajectories
- **Content:**
  - Three path types: Fixed (stationary), Linear (constant heading/speed), Bezier (curved)
  - Four speed classes tested:
    - Stationary: 0 px/scan (buoys, anchored vessels)
    - Slow: 2 px/scan (drifting, slow vessels)
    - Medium: 5 px/scan (cruising vessels)
    - Fast: 15 px/scan (high-speed craft)
  - Duration: active fraction [0.6, 1.0] of total frames, randomly sampled
  - Water mask enforcement: all waypoints validated against mask; trajectories truncated at boundaries
  - Edge positions: objects can start/end at water-land boundary
- **Visual:** TikZ showing example trajectories on a PPI disc — one stationary dot, one slow arc, one fast straight line, labeled with speed in px/scan
- **Key point:** Speed classes parameterized in pixels/scan (not physical velocity) to capture range-dependent effects

### Slide 9: Sea Clutter Model
- **Heading:** Synthetic Sea Clutter: K-Distributed Streaks
- **Content:**
  - Clutter modeled as radial streaks (not per-bin random variates)
  - Range-dependent geometry:
    - Azimuth width: $200 \cdot e^{-6r} + 5$ (wide near radar, narrow far)
    - Range length: $3 + 110r$ bins (grows with range)
  - Raised-cosine intensity envelope across azimuth width
  - Peak intensity sampled from configurable range (e.g., [200, 255] for heavy)
  - MAX-blended into frame (same operator as objects)
  - Configurable: `num_streaks` (0-100+), `intensity_range`, `per_frame` seeding
- **Visual:** Two panels: (left) PPI frame without clutter, (right) same frame with 100 streaks at heavy intensity. Annotate streak geometry.
- **Key point:** Extended clutter streaks are the challenging case for ML — more confusing than Gaussian noise

### Slide 10: Polar-to-Cartesian Conversion
- **Heading:** Image Rendering: Polar to Cartesian Mapping
- **Content:**
  - Precomputed lookup table (LUT) maps each Cartesian pixel (x, y) to polar (pulse, bin)
  - Image size: 1735 x 1735 pixels, center at (867.5, 867.5)
  - For each pixel: compute $r = \sqrt{dx^2 + dy^2}$, $\theta = \text{atan2}(dx, dy)$
  - Only pixels with $r/r_{max} \leq 1$ are valid (PPI circle)
  - Frame regularization: interpolate irregular pulse angles to uniform 720-pulse grid
  - Label conversion: polar bounding boxes → axis-aligned Cartesian boxes via 4-corner transform
- **Visual:** Diagram showing the polar→Cartesian mapping with a radar frame example: left panel = polar (rectangular array), right panel = Cartesian PPI circle. Arrow showing LUT mapping.
- **Key point:** Output matches what a human operator would see on a real radar display

### Slide 11: Scene Configuration Examples
- **Heading:** YAML-Driven Scene Generation
- **Content:**
  - Each experiment defined by YAML configuration files
  - Example fields: `seed`, `count` (frames), `objects` (groups with name, count, size, intensity, path), `clutter` (num\_streaks, intensity\_range), `labels` (class\_map)
  - 10 scenes per ablation condition, 50 frames each
  - Ground truth labels exported in YOLO format (class\_id, x\_center, y\_center, width, height)
  - Class mapping: 7 sub-classes → 2 detection classes (stationary, moving)
- **Visual:** Show a condensed YAML snippet (5-6 lines) alongside the resulting PPI frame with bounding boxes overlaid. Use actual PPI image from `paper/data/A2/ppi/noclutter/exponential/frame_0032.png`.
- **Key point:** Full reproducibility — every parameter specified declaratively

---

## SECTION 3: ECHO TRAIL RENDERING (Slides 12-16)

### Slide 12: Trail Compositing Equation
- **Heading:** Echo Trail Compositing: Per-Pixel MAX
- **Content:**
  - Core equation (display prominently):
    $$I_{\text{disp}}(r, \theta, t) = \max_{k=0}^{N} \left[ f(k) \cdot I_{\text{raw}}(r, \theta, t-k) \right]$$
  - Where:
    - $N$ = trail length (number of historical scans)
    - $f(k)$ = decay function weighting frame $k$ scans ago
    - $I_{\text{raw}}(r, \theta, t-k)$ = raw intensity from scan $t-k$
    - $\max$ operator ensures strong returns are never attenuated by weaker history
  - Sliding window: each frame independently processes its $N$-frame history
  - No persistent state between frames; parallelizable
- **Visual:** Timeline diagram showing frames $t-N$ through $t$, each weighted by $f(k)$, converging through MAX operator to produce $I_{\text{disp}}$
- **Key point:** MAX compositing is consistent with real radar display behavior

### Slide 13: Decay Functions
- **Heading:** Four Decay Functions: $f(k)$
- **Content:** Display all four equations:
  - Exponential: $f_{\text{exp}}(k) = e^{-k/\tau}$, where $\tau = \max(N/3, 1)$
  - Concave: $f_{\text{conc}}(k) = \max(0, 1 - (k/N)^3)$
  - Linear: $f_{\text{lin}}(k) = 1 - k/N$
  - Step: $f_{\text{step}}(k) = \begin{cases} 1 & k \leq N \\ 0 & k > N \end{cases}$
- **Visual:** Include `fig1_decay_functions.pdf` — pgfplots showing all four curves overlaid (Garnet=exponential, Atlantic=concave, Horseshoe=linear, Congaree=step) with $k$ on x-axis, $f(k)$ on y-axis
- **Key point:** Each function produces a different intensity profile for the trail streak behind a moving target

### Slide 14: Intensity Encoding
- **Heading:** Intensity Encoding: Binary vs. Proportional
- **Content:**
  - **Binary:** Any non-zero return $\rightarrow$ trail pixel at full intensity. Formula: $w = \mathbb{1}[I > 0] \cdot f(k)$
    - High contrast, simple, but loses amplitude (RCS) information
    - A faint buoy and a large vessel produce identical trail pixels
  - **Proportional:** Trail intensity scales with original return strength. Formula: $w = (I/255) \cdot f(k)$
    - Preserves radiometric information in trail
    - Fainter trails for weak targets, but discriminative under clutter
- **Visual:** Include `fig_binary_prop_ppi.pdf` or `fig5_binary_proportional.pdf` — side-by-side PPI images showing binary (left, high contrast uniform trails) vs. proportional (right, varying trail brightness)
- **Key point:** Binary is simpler and higher-contrast; proportional preserves information that matters under clutter

### Slide 15: Color Mapping Strategies
- **Heading:** Color Mapping: Four Schemes
- **Content:**
  - **Monochrome:** Single-channel green-on-black; brightness = decay weight
  - **Two-tone:** Current frame = green, all history = red (dimming with age)
  - **Gradient:** Trail age $\rightarrow$ hue ramp: green (newest) → yellow → red (oldest). Provides implicit directional cue.
  - **Intensity-mapped:** Original return strength $\rightarrow$ hue (jet ramp: blue → cyan → green → yellow → red). Encodes RCS in color.
- **Visual:** Include `fig6_color_schemes.pdf` or `fig_color_ppi.pdf` — 4-panel figure showing same scene rendered with each color scheme. If using the generated figure, show mono/twotone/gradient/intensity side by side.
- **Key point:** Color mapping encodes either temporal (age) or radiometric (strength) information — functionally meaningful, not cosmetic

### Slide 16: Trail Configuration Space
- **Heading:** The Trail Parameter Space
- **Content:**
  - Four independent parameters define a trail configuration:
    1. Trail length $N \in \{0, 1, 2, \ldots, 25\}$
    2. Decay function $f(k) \in \{\text{exp}, \text{concave}, \text{linear}, \text{step}\}$
    3. Intensity encoding $\in \{\text{binary}, \text{proportional}\}$
    4. Color mapping $\in \{\text{mono}, \text{twotone}, \text{gradient}, \text{intensity}\}$
  - Total configuration space: $26 \times 4 \times 2 \times 4 = 832$ combinations
  - Sequential ablation design: optimize each parameter in order, carry best-of-prior forward
  - This reduces 832 configs to ~46 training runs while isolating individual effects
- **Visual:** Table or grid showing parameter space with arrows indicating sequential optimization path (A1→A2→A3→A4→A5→...)
- **Key point:** Sequential ablation is tractable and isolates individual parameter contributions

---

## SECTION 4: EXPERIMENTAL DESIGN (Slides 17-19)

### Slide 17: Ablation Structure
- **Heading:** Sequential Ablation Design
- **Content:**
  - A1: Trail Length $\times$ Speed — $N \in \{0,1,2,3,4,5,10,15,20,25\}$, 4 speed classes → carry best $N$
  - A2: Decay Function — 4 functions at best $N$ → carry best decay
  - A3: Intensity Encoding — binary vs. proportional at best ($N$, decay) → carry best encoding
  - A4: Color Mapping — 4 schemes at best ($N$, decay, encoding) → carry best color
  - A5: Range Dependence — re-sweep $N$ at near/mid/far range
  - A6: Clutter Level — vary clutter density at best config
  - A7: Target Proximity — vary separation distance
  - A8: Crossing Trajectories — vary crossing angle
  - Each ablation tested under two conditions: no-clutter and with-clutter
- **Visual:** Flowchart: A1 → best $N$ feeds A2 → best $f(k)$ feeds A3 → ... → A4 complete config feeds A5-A8 environmental tests
- **Key point:** Best-of-prior carries forward; each ablation isolates exactly one variable

### Slide 18: Training Protocol
- **Heading:** YOLOv8 Training Configuration
- **Content:**
  - Model: YOLOv8-nano (smallest variant), pretrained on COCO
  - Fine-tuning: 50 epochs, learning rate $1 \times 10^{-3}$, batch size 16, input 640$\times$640
  - Augmentation: random flip, mosaic, mixup (standard YOLO augmentation)
  - Dataset per condition: 10 scenes $\times$ 250 frames = 2,500 total
    - Train: scenes 1-9 (2,250 images)
    - Validation: scene 10 (250 images)
  - 2-class detection: stationary (class 0), moving (class 1)
  - Independent training per condition — no information leakage between ablation levels
  - Deterministic: seed 42, deterministic=True
- **Visual:** Small architecture diagram of YOLOv8-nano (backbone + neck + head) or just the training pipeline: YAML config → Trail Renderer → Dataset Split → YOLOv8n → metrics
- **Key point:** Intentionally small dataset (2,250 images) reflects data-limited radar applications

### Slide 19: Evaluation Metrics
- **Heading:** Metrics and Statistical Rigor
- **Content:**
  - Primary metric: mAP$_{50}$ (mean Average Precision at IoU $\geq$ 0.50)
  - Secondary: mAP$_{50\text{-}95}$, precision, recall, F1
  - Speed-tier stratification: metrics computed separately for stationary, slow, medium, fast
  - Ground truth counts: stationary=750, slow=263, medium=216, fast=402 instances
  - Per-class and per-condition evaluation enables fine-grained analysis
  - Why mAP$_{50}$: conservative metric; stricter IoU would show even larger trail-induced degradation (trail streaks distort bounding box geometry)
- **Visual:** Include `fig_iou.pdf` if it shows IoU illustration, or a simple diagram showing how trail streaks enlarge predicted bounding boxes and reduce IoU with ground truth
- **Key point:** mAP$_{50}$ is actually lenient — real-world localization errors from trails are worse than these numbers suggest

---

## SECTION 5: RESULTS (Slides 20-31)

### Slide 20: A1 — Trail Length (No-Clutter)
- **Heading:** E1: Trail Length $\times$ Speed (No-Clutter)
- **Content:**
  - Overall mAP$_{50}$: monotonic rise from 0.675 ($N$=0) to 0.918 ($N$=25)
  - Steep initial gain: +17pp from $N$=0 to $N$=4
  - Diminishing returns: +7pp from $N$=4 to $N$=25
  - By speed tier:
    - Stationary: 0.339 → 0.793 ($N$=20), slight regression at $N$=25
    - Slow: 0.449 → 0.778 ($N$=25), non-monotonic with trough at $N$=5
    - Medium: 0.431 → 0.848 ($N$=25), erratic with dip at $N$=10
    - Fast: 0.488 → 0.884 ($N$=25); **+34.7pp jump at $N$=3** (0.488→0.836), saturated by $N$=10
- **Visual:** Include `fig3_trail_length_speed.pdf` — line plot with 4 speed-tier curves (mAP$_{50}$ vs. $N$) using brand colors. Or use `paper/data/A1/speed_tier_map50_both.png` for the combined plot.
- **Key point:** Fast targets benefit explosively from even short trails; stationary targets need $N$=10-15

### Slide 21: A1 — Trail Length (Clutter)
- **Heading:** E1: Trail Length $\times$ Speed (With Clutter)
- **Content:**
  - Overall mAP$_{50}$: peaks at 0.720 ($N$=15), **regresses to 0.669 at $N$=25 — below $N$=0 baseline (0.671)**
  - By speed tier (clutter):
    - Stationary: peaks at $N$=3 (0.580), mild variation
    - Slow: **catastrophic failure** — peaks at $N$=1 (0.383), collapses to 0.207 at $N$=25
    - Medium: peaks at $N$=15 (0.446), modest
    - Fast: stable 0.468-0.568, peak at $N$=10
  - Slow-target recall drops from 0.681 ($N$=0) to 0.491 ($N$=25) — loss of 19pp
  - Precision = 1.0 for all moving subclasses across all $N$ (zero false positives on motion)
- **Visual:** Same plot format as slide 20 but with clutter curves. Use `paper/data/A1/speed_tier_recall_both.png` for recall comparison, or a side-by-side with no-clutter.
- **Key point:** Longer trails that help clean scenes actively harm slow targets in clutter

### Slide 22: A1 — Key Insight: Clutter Gap
- **Heading:** E1: The Clutter Gap Widens with Trail Length
- **Content:**
  - Clutter gap = (no-clutter mAP$_{50}$) $-$ (clutter mAP$_{50}$)
  - At $N$=0: gap = 0.004pp (negligible)
  - At $N$=10: gap = 0.199pp
  - At $N$=25: gap = 0.249pp
  - Trail representation that benefits clean scenes is most distorted by clutter
  - Optimal $N$ depends on environment:
    - No-clutter: $N$=10-15 practical optimum (captures 97\% of gain)
    - Clutter: never exceed $N$=15; for slow targets, $N$=1 or none
  - No single trail length is universally optimal
- **Visual:** Bar chart or line plot showing no-clutter vs. clutter mAP$_{50}$ as a function of $N$, with the gap shaded/annotated. Two curves diverging as $N$ increases.
- **Key point:** Trail configuration must be adapted to environmental conditions

### Slide 23: A2 — Decay Function
- **Heading:** E2: Decay Function Comparison
- **Content:**
  - No-clutter ranking: Exponential (0.898) > Concave (0.892) > Linear (0.891) > Step (0.885). Tight 1.3pp spread.
  - Clutter ranking: **Step (0.700) > Exponential (0.691) $\approx$ Linear (0.691) > Concave (0.669)**
  - **Complete rank inversion between conditions**
  - Step most clutter-robust (20.9\% relative drop)
  - Concave worst in clutter (24.9\% relative drop)
  - Medium-speed targets in clutter: step dominates at 0.495, +9.5pp above nearest competitor
  - Slow targets: structural floor $<$0.31 mAP$_{50}$ for all functions
  - Stationary/moving inversion: clean → moving > stationary; clutter → stationary > moving
- **Visual:** Include `fig4_decay_shape.pdf` or `paper/data/A2/a2_decay_comparison.png` — grouped bar chart showing all 4 functions under both conditions. Or `a2_perclass_bar.png` for per-class breakdown.
- **Key point:** Exponential for clean; step for clutter; concave should be avoided operationally

### Slide 24: A3 — Intensity Encoding
- **Heading:** E3: Binary vs. Proportional Intensity
- **Content:**
  - No-clutter: Binary leads +3.45pp (0.872 vs. 0.837)
  - Clutter: Proportional leads +0.34pp (0.657 vs. 0.653) — within noise, but consistent direction
  - Moving targets show sharpest reversal: binary +4.85pp clean → proportional +2.50pp clutter
  - Clutter fragility: Binary 21.8pp penalty, Proportional 18.1pp penalty
  - Why? Binary erases amplitude information, rendering clutter and targets at uniform intensity. Proportional preserves amplitude gradients that provide discriminative cues under clutter.
  - Fast targets in clutter: proportional +1.58pp mAP$_{50}$, +2.78pp mAP$_{50\text{-}95}$ (better localization)
- **Visual:** Include `fig5_binary_proportional.pdf` — side-by-side comparison table or bar chart. Clean vs. clutter, binary vs. proportional, with per-class breakdown.
- **Key point:** Binary wins clean; proportional is more clutter-robust because amplitude information becomes discriminative

### Slide 25: A4 — Color Mapping
- **Heading:** E4: Color Mapping Strategies
- **Content:**
  - No-clutter ranking: Gradient (0.871) > Twotone (0.837) > Intensity (0.810) > Mono (0.736)
  - Clutter ranking: Intensity (0.670) > Gradient (0.667) > Twotone (0.657) > Mono (0.576)
  - **Core finding: Any color encoding outperforms monochrome by 9-13+ mAP$_{50}$ points**
  - Gradient achieves 0.904 moving mAP$_{50}$ in no-clutter (recall 0.936)
  - Intensity most clutter-robust (17.2\% relative drop vs. gradient's 23.4\%)
  - Gradient provides implicit directional cue (green→red hue indicates motion direction)
  - Intensity best for stationary targets in clutter (0.739, +5pp above all others)
  - Surprising: mono leads on medium-speed targets in both conditions — anomalous, replicated consistently
- **Visual:** Include `fig6_color_schemes.pdf` — 4-panel PPI examples + bar chart comparison
- **Key point:** Color mapping is functionally meaningful — not cosmetic decoration

### Slide 26: A5 — Range Dependence
- **Heading:** E5: Range-Dependent Trail Optimization
- **Content:**
  - Same physical speed $\rightarrow$ different pixel displacement at different ranges
  - Near range ($\sim$200m, 80 bins): fast pixel displacement $\rightarrow$ short trails optimal ($N \approx 3$)
  - Mid range ($\sim$1 nm, 350 bins): moderate displacement $\rightarrow$ medium trails
  - Far range ($\sim$3 nm, 750 bins): slow pixel displacement $\rightarrow$ long trails optimal ($N \approx 24$)
  - Single fixed trail configuration cannot optimize across all ranges simultaneously
  - Motivates **range-adaptive trail rendering**: vary $N$ as a function of range within a single PPI frame
- **Visual:** Include `fig7_range_dependence.pdf` or `fig_range_displacement.pdf` — diagram showing how a target at near vs. far range sweeps different numbers of pixels per scan, with optimal $N$ annotated at each range band. Or `fig_adaptive_trail.pdf`.
- **Key point:** Range-adaptive rendering is the natural solution — short trails for near-range cells, long trails for far-range cells

### Slide 27: A6 — Clutter Interaction
- **Heading:** E6: Trail-Clutter Interaction
- **Content:**
  - Trails provide greatest benefit under heavy clutter: signal integration above fluctuating clutter floor
  - Low clutter: modest additional benefit over no-trail baseline (already strong SNR)
  - Heavy clutter: no-trail baseline degrades significantly; trails help by temporal accumulation
  - However: benefit is speed-dependent (fast targets gain, slow targets may lose)
  - Clutter inverts the stationary/moving performance ranking for ALL parameter configurations tested in A1-A4
- **Visual:** Include `fig8_clutter.pdf` — bar chart or table showing performance across clutter levels (none, low, moderate, heavy) at best trail config
- **Key point:** Trails help most where they are needed most (heavy clutter), but slow-target degradation persists

### Slide 28: A7 — Target Proximity & Merging
- **Heading:** E7: Target Proximity and Merging Threshold
- **Content:**
  - Two stationary targets at varying separations: 10m, 20m, 30m, ..., 100m
  - Without trails ($N$=0): targets resolve as separate detections down to $\sim$20m separation
  - With trails ($N$=12): merging threshold shifts to $\sim$28m — an 8m increase
  - Trail spatial footprint expansion: each target's trail increases its effective size on the PPI
  - Significant cost in dense target environments (harbors, buoy fields, congested waterways)
  - Tradeoff: trails improve detection of individual targets but degrade discrimination of nearby targets
- **Visual:** Include `fig9_merging.pdf` — plot of detection count vs. separation distance, with $N$=0 and $N$=12 curves showing the threshold shift
- **Key point:** 8m increase in merging threshold is operationally significant in congested waters

### Slide 29: A8 — Crossing Trajectories
- **Heading:** E8: Crossing Trajectory Overlap
- **Content:**
  - Two moving targets on converging paths at angles: 15, 30, 45, 60, 75, 90 deg
  - Shallow crossing angles ($<$30 deg) with long trails: severe degradation
  - Trail overlap creates single elongated artifact instead of two distinct detections
  - Decay function matters at crossing points:
    - Step: full-intensity overlap zone — maximally confusing
    - Exponential: faint tail overlap — detector may still resolve
  - At 90 deg crossing: minimal overlap, trails point in perpendicular directions → resolvable
  - At 15 deg: trails nearly parallel, extended overlap → detector sees one merged target
- **Visual:** Include `fig10_crossing.pdf` or `fig_crossing_overlap.pdf` — TikZ diagram showing two targets with trails at different crossing angles, annotated with overlap region
- **Key point:** Shallow-angle crossings are the worst case for trail-based detection

### Slide 30: Summary Heatmap
- **Heading:** Summary: All Ablations at a Glance
- **Content:**
  - Present a consolidated results table:

  | Ablation | Best (Clean) | Best (Clutter) | Key Finding |
  |----------|-------------|----------------|-------------|
  | A1: Length | $N$=25 (0.918) | $N$=15 (0.720) | Fast saturate by $N$=3; slow harmed |
  | A2: Decay | Exp (0.898) | Step (0.700) | Complete rank inversion |
  | A3: Encoding | Binary (0.872) | Prop (0.657) | Amplitude cue under clutter |
  | A4: Color | Gradient (0.871) | Intensity (0.670) | Any color >> mono by 9-13pp |
  | A5: Range | Near: $N{\approx}3$ | Far: $N{\approx}24$ | Range-adaptive needed |
  | A6: Clutter | — | Trails help heavy | Slow targets persist as floor |
  | A7: Proximity | $\sim$20m | $\sim$28m | +8m merging shift |
  | A8: Crossing | 90 deg OK | $<$30 deg fails | Shallow angles degrade |

- **Visual:** Include `fig11_summary_heatmap.pdf` — color-coded heatmap of mAP$_{50}$ across ablation conditions, or use the table above formatted cleanly in Beamer
- **Key point:** No single configuration dominates; environment-adaptive configuration is necessary

### Slide 31: Surprising & Counterintuitive Findings
- **Heading:** Unexpected Results
- **Content:**
  1. **Precision = 1.0 on all moving targets** in no-clutter (zero false positives on motion; all errors are missed detections)
  2. **Stationary harder than fast at baseline** ($N$=0): stationary mAP$_{50}$=0.339 vs. fast=0.488. Without trails, positional salience of moving targets matters more than stability of stationary ones.
  3. **Mono unexpectedly leads on medium-speed targets** in both conditions — replicated consistently, mechanism unclear
  4. **Two-tone overfitting:** peaks highest in training (0.923) but overfits; gradient (0.918 peak) generalizes better
  5. **Medium-speed tier consistently hardest** across ALL experiments (~0.286 mAP$_{50}$). Displacement too short for clear directional cue, too long for stable point signature.
  6. **Clutter inverts stationary/moving ranking** for every parameter combination tested
- **Visual:** None needed; clean bulleted text. Could highlight key numbers in brand accent colors (Garnet for important, Atlantic for contrasting)
- **Key point:** Several results challenge intuitive assumptions about trail behavior

---

## SECTION 6: DISCUSSION & CONCLUSION (Slides 32-35)

### Slide 32: Practical Recommendations
- **Heading:** Operational Recommendations
- **Content:**
  1. **No single trail length is optimal.** Fast targets saturate by $N$=3; stationary need $N$=10-15; slow in clutter prefer $N$=1 or none.
  2. **Use exponential decay for clean conditions** (mAP$_{50}$=0.898); **switch to step under clutter** (0.700). Avoid concave operationally.
  3. **Proportional encoding for high-clutter environments** despite slightly lower clean-scene performance. Binary for known-clean scenarios.
  4. **Always use color encoding** — any scheme beats monochrome by 9-13pp. Gradient recommended as default; intensity-mapped for clutter-heavy areas.
  5. **Implement range-adaptive trail rendering:** short $N$ at near range, long $N$ at far range.
  6. **Avoid long trails in dense target environments:** +8m merging threshold shift.
  7. **Slow targets in clutter require upstream intervention** (CFAR, coherent integration) — trail tuning alone cannot solve.
- **Visual:** Could use a decision flowchart: "Is clutter present?" → Yes: step decay, proportional, intensity color / No: exponential, binary, gradient color. "Target range?" → Near: $N$=3 / Far: $N$=24.
- **Key point:** Actionable guidelines for radar system designers integrating ML detection

### Slide 33: Structural Limitations
- **Heading:** The Slow-Target Floor and Other Limits
- **Content:**
  - Slow targets in clutter: $\sim$0.31 mAP$_{50}$ ceiling across ALL configurations
  - This is a structural limitation of trail augmentation, not a parameter tuning problem
  - Root cause: slow targets produce small displacements that trails mix into accumulated clutter
  - Precision globally low (max 0.470) — high false positive rate across all experiments
  - Medium-speed tier consistently hardest — displacement is ambiguous (neither clearly moving nor clearly stationary)
  - Trail rendering systematically increases bounding box size for moving targets, degrading IoU
- **Visual:** Highlight the slow-target clutter floor across ablations — all points below 0.31. Could overlay A1-A4 slow-clutter results on a single plot to show the persistent ceiling.
- **Key point:** Some detection challenges cannot be solved at the display layer; upstream signal processing is necessary

### Slide 34: Future Work
- **Heading:** Future Directions
- **Content:**
  1. **Validate on real hardware** — test findings on actual Furuno DRS4D-NXT recordings from Charleston Harbor
  2. **Extend to other architectures** — Faster R-CNN, DETR, transformer-based detectors
  3. **Real-time range-adaptive rendering** — implement variable $N$(range) in operational pipeline
  4. **Trail-tracking interaction** — study effect on downstream Kalman filters, Hungarian algorithm
  5. **Confidence calibration** — how trail parameters affect detector softmax confidence scores
  6. **Upstream clutter suppression** — CFAR preprocessing, MTI filtering before trail rendering
  7. **Color similarity threshold** — minimum hue separation detector needs to distinguish trail from current return
- **Visual:** None; clean text
- **Key point:** This work establishes the foundation; operational deployment requires hardware validation

### Slide 35: Questions
- **Heading:** Questions?
- **Content:**
  - Thank you
  - Contact: jvaught@sc.edu
  - Paper submitted to IDETC 2026
- **Visual:** Brand-styled closing slide with garnet accent
