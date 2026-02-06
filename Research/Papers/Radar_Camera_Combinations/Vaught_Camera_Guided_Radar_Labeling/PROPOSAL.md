# Project Proposal: Camera-Guided Radar Labeling via Active PTZ Perception for Maritime Dataset Construction

**Principal Investigator:** Dr. Yi Wang
**Lead Researcher:** J.C. Vaught
**Team Members:** Sam Cancilla (UG), Mateo Altomare (UG), Douglas Cahl
**Date:** February 5, 2026

---

## 1. Problem Statement

Labeled maritime radar datasets are virtually nonexistent. While automotive radar benefits from large labeled benchmarks (nuScenes, RADIATE), maritime radar classification research is bottlenecked by the absence of labeled training data. Radar blobs on their own carry limited semantic information -- an operator can see that something is there, but cannot reliably determine what it is from radar features alone. Manual radar labeling requires cross-referencing with AIS, visual observation, or expert knowledge, making it prohibitively expensive and unscalable.

The fundamental challenge is this: **How can we automatically construct large-scale labeled radar datasets without requiring human experts to manually annotate every target?**

Current approaches rely on:
- AIS data (only available for larger vessels with transponders)
- Manual visual inspection (labor-intensive, not scalable)
- Simulated data (lacks realism for complex maritime environments)
- Fixed-camera fusion (limited field of view, passive observation)

None of these methods scale to the dataset sizes required for modern machine learning, particularly deep learning approaches that demand thousands of labeled examples per class.

---

## 2. Motivation

### 2.1 Active Perception Paradigm

Rather than passively fusing co-located sensors with overlapping fields of view, this project treats the PTZ camera as an **active perception agent**. When radar detects a target, the camera deliberately slews to observe it, zooms in for high-resolution classification, and returns the label to the radar system. This "look-then-label" paradigm is fundamentally different from fixed-camera fusion approaches.

**Key advantages of active perception:**
- **360-degree coverage:** PTZ camera eliminates blind spots inherent to fixed cameras
- **Adaptive resolution:** Camera zooms in on distant or ambiguous targets for better classification
- **Intelligent resource allocation:** Camera time is directed toward high-value targets
- **Scalability:** Single PTZ camera can label targets across the entire radar coverage area

This approach mirrors biological attention mechanisms -- just as humans turn their heads to examine objects of interest, the PTZ camera directs its gaze based on radar cues.

### 2.2 The Data Flywheel

The labeled radar dataset enables a virtuous cycle:

1. **PTZ camera labels radar blobs** via visual classification (YOLO/DETR on RGB + thermal imagery)
2. **Labeled radar data trains radar-only classifiers** (initial models trained on camera-derived labels)
3. **Better radar classifiers improve target prioritization** for PTZ scheduling (classify targets by confidence, prioritize uncertain cases)
4. **Improved scheduling yields higher-quality and more diverse labels** (fewer wasted camera observations, better class balance)
5. **Repeat** -- each cycle improves the overall system

This data flywheel concept means the system becomes **more efficient over time**, requiring less PTZ camera time per label as the radar-only classifier matures. In the limit, the radar classifier becomes sufficiently accurate that the camera is only needed for edge cases, anomaly detection, and dataset expansion.

**Economic benefit:** The cost of dataset construction decreases over time, while dataset size and quality increase. This is a form of **automated curriculum learning** where the system learns to focus on its weakest areas.

### 2.3 Why Maritime Radar?

Maritime environments present unique challenges that make this research both necessary and impactful:

- **Unstructured environment:** No lane markings, traffic lights, or predictable infrastructure
- **High variability:** Diverse vessel types (cargo ships, fishing boats, recreational craft, military vessels), buoys, debris, marine wildlife
- **Challenging conditions:** Fog, rain, sea spray, glare, day/night transitions
- **Safety-critical applications:** Collision avoidance, search and rescue, port security
- **Sparse labeled data:** Unlike automotive datasets (KITTI, nuScenes, Waymo), maritime radar has no equivalent

By solving the maritime radar labeling problem, we enable downstream applications in autonomous surface vehicles, automated port operations, and coastal surveillance.

---

## 3. Technical Approach

### 3.1 Radar Blob Detection

**Hardware:** Furuno DRS4D-NXT X-band pulse compression radar
- Frequency: 9.3-9.5 GHz (X-band)
- Range: Configurable, typically 0.125-24 nautical miles
- Azimuth resolution: ~1.2 degrees
- Range resolution: <2 meters (pulse compression)
- Rotation rate: 24-48 RPM (configurable)

**Processing pipeline:**
1. **Preprocessing:**
   - Apply CFAR (Constant False Alarm Rate) thresholding to radar returns
   - Remove stationary clutter via background subtraction (multi-scan averaging)
   - Doppler filtering if available (isolate moving targets)

2. **Blob detection and clustering:**
   - Spatial clustering: DBSCAN or connected components in polar coordinates
   - Temporal clustering: ST-DBSCAN (spatiotemporal DBSCAN) to track persistent targets across scans
   - Minimum persistence threshold (e.g., 3 consecutive scans) to reject transient noise

3. **Feature extraction per blob:**
   - **Kinematic:** Centroid (range, bearing), velocity (range rate, cross-track), heading
   - **Spatial:** Bounding box (range extent, angular extent), area, aspect ratio
   - **Intensity:** Mean intensity, max intensity, intensity variance, histogram moments
   - **Temporal:** Persistence (number of scans detected), track stability, Doppler signature
   - **Context:** Time of day, sea state estimate, weather condition, range to shore

**Output:** A set of radar target tracks, each represented as a time series of feature vectors and spatial locations (range, bearing).

### 3.2 PTZ Tasking Strategy

**Hardware:** FLIR M364C PTZ camera
- Pan: 360 degrees continuous rotation
- Tilt: -15 to +90 degrees
- Zoom: 30x optical
- Channels: RGB (visible) and thermal (longwave infrared)
- Slew rate: ~30 deg/sec (pan), ~20 deg/sec (tilt)

**Challenge:** The camera cannot observe all radar targets simultaneously. With typical maritime traffic (5-20 vessels in range), the camera must intelligently decide **which target to observe next** and **for how long**.

**Scheduling policies:**

1. **Round-robin baseline:**
   - Cycle through all detected radar targets in sequential order
   - Simple, fair, but inefficient (wastes time on low-value targets)

2. **Greedy nearest-target:**
   - Always slew to the nearest unobserved target (minimize slew time)
   - Maximizes observation throughput but ignores information value

3. **Information-gain-maximizing (proposed):**
   - **Novelty score:** Prioritize targets with no labels or few labels in their feature space region
   - **Confidence gap:** Prioritize targets where radar classifier is most uncertain (high entropy)
   - **Class balance:** Prioritize underrepresented classes to balance the dataset
   - **Temporal urgency:** Prioritize targets about to exit radar range or enter occlusion zones
   - **Slew cost:** Penalize targets requiring large camera movements (trade off information gain vs slew time)

**Observation duration:**
- Adaptive: Spend more time on ambiguous targets, less on clear cases
- Stop early if dual detectors (YOLO + DETR) reach high-confidence agreement
- Capture multi-frame sequences for temporal reasoning (e.g., vessel maneuvers)

**Multi-target handling:**
- Maintain a priority queue of targets ranked by information gain
- Recompute priorities after each observation (targets change position, radar classifier confidence updates)
- Handle cases where multiple targets fall within the same camera FOV (label all simultaneously)

### 3.3 Dual-Stream Visual Detection

**Rationale for dual detectors:**
- YOLO (YOLOv8/YOLOv9): Real-time, high throughput, excellent for clear well-lit targets
- DETR (Detection Transformer): Transformer-based, better on small/occluded/distant targets, handles ambiguity via attention

Running both provides:
- **Cross-validation:** High confidence when detectors agree
- **Failure detection:** Disagreement flags ambiguous cases for review or rejection
- **Complementary strengths:** YOLO for speed, DETR for hard cases

**Processing pipeline:**

1. **Image acquisition:**
   - Capture both RGB and thermal streams from FLIR M364C
   - Synchronize captures with PTZ heading telemetry (for angular alignment)
   - Record zoom level (affects spatial resolution and field of view)

2. **Detector inference:**
   - Run YOLO and DETR independently on RGB and thermal channels (4 total inference passes)
   - Use maritime-specific detector weights (fine-tuned on SeaShips, SMD, or other maritime datasets)
   - Extract bounding boxes, class labels, and confidence scores

3. **Fusion logic:**
   - **Strong agreement:** Both detectors, both channels agree on class → High confidence label
   - **Partial agreement:** Detectors agree but channels differ → Medium confidence, prefer thermal if conditions (fog, glare) favor it
   - **Disagreement:** Detectors disagree on class → Flag for manual review or reject label
   - **No detection:** Neither detector finds target → Label as "sea clutter" or "false alarm"

4. **Target classes:**
   - Vessel subtypes: Cargo, recreational, fishing, military, tanker, ferry
   - Fixed objects: Buoy, beacon, offshore platform, pier
   - Transient: Debris, marine wildlife (whales, dolphins), sea clutter
   - Unknown: Detected but unclassifiable (important training signal)

**Handling edge cases:**
- **Multiple objects in FOV:** Spatial association via bounding box proximity to radar bearing
- **Partial occlusion:** DETR typically performs better; flag low-confidence labels
- **Extreme range:** If target is beyond effective camera range even at 30x zoom, label as "unknown - too distant"
- **Environmental degradation:** Foggy RGB but clear thermal → trust thermal channel

### 3.4 Label Assignment to Radar

**Angular calibration:**
- **Challenge:** No GPS or IMU, must align PTZ heading coordinate frame with radar bearing coordinate frame
- **Approach:**
  - Use known landmarks (lighthouses, buoys, fixed structures) visible in both radar and camera
  - Manually identify 5-10 landmarks across 360-degree field
  - Compute angular offset and scale between PTZ heading and radar bearing
  - Periodically recalibrate (weekly or after maintenance) to account for mechanical drift

**Spatial association:**
1. **Direct alignment:** If only one radar blob falls within the camera FOV at current heading, assign label directly
2. **Multiple blobs in FOV:**
   - Compute expected angular position of each blob in camera coordinates
   - Match bounding box centroids to expected positions (nearest neighbor with distance threshold)
   - If ambiguous, reject label or request human review
3. **No radar blob in FOV:** Possible false alarm or clutter suppression removed it → log discrepancy

**Confidence scoring:**
Assign a label confidence score based on multiple factors:
- Detector agreement (YOLO + DETR, RGB + thermal): 0-1 scale
- Zoom level (higher zoom = better resolution = higher confidence)
- Range (closer targets = higher confidence)
- Environmental conditions (clear weather = higher confidence than fog/rain)
- Blob stability (persistent tracks = higher confidence than transient detections)

**Final output:** Each radar blob receives:
- Class label (e.g., "recreational vessel")
- Confidence score (0-1)
- Provenance metadata: detector(s) that agreed, PTZ zoom, range, timestamp, environmental conditions
- Link to raw PTZ imagery for review

### 3.5 Dataset Construction

**Data schema:**

Each labeled radar target is stored as a record with:
- **Radar features:** Intensity statistics, spatial extent, velocity, Doppler, range, bearing, persistence
- **Label:** Class name, confidence score, provenance (which detectors, channels)
- **Metadata:** Timestamp, environmental context (weather, sea state, time of day), PTZ state (zoom, heading)
- **Imagery:** Path to associated PTZ frames (RGB + thermal)

**Storage format:**
- Tabular data (CSV or Parquet) for feature vectors and labels
- Separate directories for imagery (organized by timestamp)
- Train/val/test splits: Stratified by class, temporally separated (avoid leakage from persistent tracks)

**Quality assurance:**
1. **Automated filtering:**
   - Reject labels with confidence below threshold (e.g., <0.5)
   - Reject labels where detectors strongly disagreed
   - Reject labels for targets with unstable tracks (likely false alarms)

2. **Manual validation:**
   - Randomly sample 5-10% of labels for human review
   - Compute label accuracy, identify systematic errors
   - Use validation results to tune confidence thresholds

3. **Bias monitoring:**
   - Track class distribution over time (ensure balance)
   - Monitor label distribution by range, time of day, weather (ensure diversity)
   - Actively seek underrepresented classes via PTZ scheduling

**Dataset statistics (projected):**
- Collection duration: 6-12 months continuous operation
- Unique targets per day: 50-200 (varies by location and traffic)
- Labels per target: 5-20 (multiple observations as target moves through radar range)
- Total labeled radar samples: 50,000-200,000
- Imagery volume: ~1TB (compressed)

---

## 4. Data Collection Plan

### 4.1 Platform and Location

**Deployment site:**
- Stationary coastal observation post with unobstructed 360-degree view
- Elevation: 10-20 meters above sea level (minimizes sea clutter, extends radar horizon)
- Typical maritime traffic: Mix of commercial, recreational, and military vessels
- Proximity to navigation channels, ports, or coastal shipping lanes

**Hardware setup:**
- **Radar:** Furuno DRS4D-NXT mounted on mast with clear line of sight
- **Camera:** FLIR M364C PTZ co-located with radar (horizontal offset <1 meter to minimize parallax)
- **Compute:** NVIDIA Jetson Orin (onboard AI inference and PTZ control)
- **Storage:** Network-attached storage for radar data, PTZ imagery, and labels
- **Power:** Shore power with UPS backup for continuous operation
- **Connectivity:** Ethernet for data upload, remote monitoring

### 4.2 Sensor Configuration

**Radar settings:**
- Range scale: 6-12 nautical miles (balances coverage vs clutter)
- Rotation rate: 24 RPM (2.5 sec per scan, good temporal resolution)
- Gain: Auto-gain with manual override for adverse weather
- Sea clutter filter: Adaptive CFAR threshold

**Camera settings:**
- Frame rate: 10 FPS (sufficient for vessel detection, manageable data rate)
- Resolution: 1920x1080 (RGB and thermal)
- Auto-exposure with manual override for extreme lighting
- Zoom: Dynamic (controlled by tasking algorithm)

### 4.3 Collection Schedule

**Continuous operation:**
- 24/7 recording across day/night cycles (thermal enables nighttime)
- Capture data in varying weather: Clear, overcast, rain, fog, high winds
- Capture data in varying sea states: Calm (0-1), moderate (2-4), rough (5+)
- Seasonal variation: Collect across multiple seasons to capture different traffic patterns and weather

**Data diversity goals:**
- Temporal: Equal representation of day/night, dawn/dusk
- Environmental: Balanced dataset across weather conditions and sea states
- Traffic: Balanced dataset across vessel types and sizes
- Range: Balanced dataset across near-field (<1 nm), mid-field (1-5 nm), far-field (>5 nm)

### 4.4 Ground Truth Validation

**Periodic manual labeling:**
- Weekly sessions: Human expert reviews synchronized radar + PTZ video
- Label 50-100 radar targets manually (gold standard labels)
- Compare automated labels to manual labels (compute precision, recall, F1)
- Identify systematic errors (e.g., consistent misclassification of fishing vessels)

**AIS cross-reference (when available):**
- Match AIS transponder data to radar tracks via spatial/temporal proximity
- Use AIS vessel type as ground truth for large commercial vessels
- Note: AIS coverage is incomplete (many small vessels lack transponders)

---

## 5. Timeline

| Phase | Description | Duration | Status |
|-------|-------------|----------|--------|
| **Phase 1** | Hardware deployment and synchronized data collection | 2 months | In progress |
| | - Install radar and PTZ camera at observation site | | |
| | - Verify sensor synchronization and data capture pipeline | | |
| | - Collect initial unlabeled dataset for algorithm development | | |
| **Phase 2** | Radar blob detection and PTZ tasking pipeline | 2 months | In progress |
| | - Implement CFAR thresholding and blob clustering | | |
| | - Develop ST-DBSCAN for persistent track extraction | | |
| | - Build PTZ control API and slewing scheduler | | |
| | - Validate round-robin and nearest-target scheduling baselines | | |
| **Phase 3** | Detector integration (YOLO + DETR) on PTZ imagery | 2 months | Planned |
| | - Fine-tune YOLO and DETR on maritime datasets (SeaShips, SMD) | | |
| | - Deploy models to Jetson Orin with TensorRT optimization | | |
| | - Implement dual-stream fusion logic (RGB + thermal, YOLO + DETR) | | |
| | - Evaluate detector accuracy on manually labeled validation set | | |
| **Phase 4** | Angular calibration and label assignment pipeline | 1 month | Planned |
| | - Perform landmark-based angular calibration | | |
| | - Implement spatial association logic (radar blob to camera detection) | | |
| | - Develop confidence scoring and label filtering | | |
| | - Validate label accuracy on ground truth samples | | |
| **Phase 5** | Dataset construction and quality evaluation | 2 months | Planned |
| | - Run end-to-end labeling pipeline on 3-6 months of radar data | | |
| | - Construct tabular dataset with radar features and labels | | |
| | - Perform quality assurance (manual validation, bias monitoring) | | |
| | - Publish dataset statistics and sample visualizations | | |
| **Phase 6** | Radar-only classifier training on auto-labeled data | 2 months | Planned |
| | - Train baseline radar classifiers (random forest, SVM, simple neural nets) | | |
| | - Evaluate classifier accuracy on held-out test set | | |
| | - Implement information-gain PTZ scheduling using radar classifier uncertainty | | |
| | - Demonstrate data flywheel: re-run labeling with improved scheduling, measure efficiency gains | | |
| **Phase 7** | Paper preparation and submission | 2 months | Planned |
| | - Write conference paper (target: ICRA, IROS, or CVPR) | | |
| | - Prepare code release and dataset documentation | | |
| | - Submit paper and dataset to appropriate venues | | |

**Total duration:** 13 months (April 2026 - May 2027)

---

## 6. Risk Assessment

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|-----------|--------|---------------------|
| **PTZ slew time limits observation of simultaneous targets** | High | High | - Implement intelligent scheduling prioritizing high-value targets<br>- Accept partial coverage as inherent trade-off<br>- Quantify coverage vs label quality trade-off in paper<br>- Future work: Multi-camera array for full coverage |
| **No GPS/IMU makes angular calibration challenging** | Medium | High | - Direct angular calibration using known landmarks<br>- Periodic recalibration (weekly) to detect drift<br>- Validate calibration accuracy via landmark re-observation<br>- Document calibration procedure for reproducibility |
| **Misclassification propagation (wrong labels contaminate dataset)** | Medium | High | - Dual-detector agreement filtering (reject disagreements)<br>- Confidence thresholds (reject low-confidence labels)<br>- Periodic manual validation (5-10% random sample)<br>- Store provenance metadata for post-hoc filtering<br>- Treat label noise as research contribution (quantify impact) |
| **Thermal/RGB detector disagreement is frequent** | Medium | Medium | - Use disagreement as quality signal, not failure mode<br>- Flag disagreements for manual review<br>- Analyze disagreement patterns (identify conditions where one channel dominates)<br>- Train channel-selection meta-model (RGB vs thermal based on conditions) |
| **PTZ mechanical wear from continuous slewing** | Low | Medium | - Duty cycle management (rest periods, reduced slew speed)<br>- Predictive maintenance (monitor slew count, temperature)<br>- Budget for PTZ replacement in grant proposal<br>- Log mechanical health metrics for failure prediction |
| **Target at extreme range is unresolvable even with 30x zoom** | Medium | Medium | - Label as "unknown" rather than force classification<br>- Use "unknown" labels as training signal for radar classifier (teaches radar its own limitations)<br>- Quantify effective camera range vs radar range (gap analysis)<br>- Future work: Higher-zoom camera or multi-scale PTZ array |
| **Sea state / weather degrades camera imagery** | Medium | Low | - Rely on thermal channel (less affected by fog, spray, glare)<br>- Label with environmental context metadata (informs confidence scoring)<br>- Collect diverse weather data to train robust detectors<br>- Accept reduced labeling rate during adverse weather (captures realistic operational conditions) |
| **Radar clutter suppression removes real targets** | Medium | Medium | - Tune CFAR threshold conservatively (prefer false positives over false negatives)<br>- Validate radar detection recall via AIS and manual observation<br>- Log radar targets that camera observes but radar missed (identify radar blind spots) |
| **Limited traffic yields insufficient data for rare classes** | Medium | Medium | - Extend collection duration (6-12 months)<br>- Deploy at high-traffic location (near port or shipping lane)<br>- Use data augmentation for rare classes<br>- Accept class imbalance as realistic (informs future deployment strategies) |
| **Jetson Orin compute capacity insufficient for real-time dual-detector inference** | Low | High | - Optimize models with TensorRT, quantization (INT8)<br>- Run detectors sequentially if parallel exceeds compute (accept latency trade-off)<br>- Upgrade to Jetson AGX Orin if necessary<br>- Offload non-critical processing to shore-based server |

---

## 7. Expected Contributions

### 7.1 Datasets

1. **Large-scale labeled maritime radar blob dataset**
   - First of its kind: Radar feature vectors paired with visual-derived labels
   - Projected size: 50,000-200,000 labeled radar targets
   - Diverse environmental conditions, vessel types, ranges
   - Publicly released with permissive license for research use

2. **Multi-modal maritime dataset**
   - Synchronized radar, RGB camera, thermal camera, and AIS (when available)
   - Enables research in cross-modal learning, sensor fusion, active perception
   - Includes temporal sequences (tracks) not just single snapshots

### 7.2 Methodological Innovations

3. **Active perception framework for cross-modal dataset construction**
   - Novel "look-then-label" paradigm: PTZ camera as active labeling agent
   - Generalizable beyond maritime domain (automotive, aerial, robotic manipulation)
   - Demonstrates advantages of active perception over passive fixed-camera fusion

4. **Data flywheel demonstration**
   - Show that radar classifiers trained on auto-labeled data improve PTZ scheduling efficiency
   - Quantify reduction in camera time per label across successive iterations
   - Establish feedback loop between dataset quality and collection efficiency

### 7.3 Software and Tools

5. **Open-source PTZ tasking and labeling pipeline**
   - Modular codebase: Radar processing, PTZ control, detector fusion, label assignment
   - Dockerized deployment for reproducibility
   - Documentation and tutorials for adaptation to other sensor suites
   - Integration with ROS for robotics community

### 7.4 Empirical Analysis

6. **Camera-to-radar label transfer quality analysis**
   - Quantify label accuracy vs manual ground truth
   - Identify failure modes (range limits, environmental conditions, detector biases)
   - Ablation studies: Impact of dual detectors, dual channels, confidence filtering

7. **PTZ active perception vs fixed-camera passive fusion comparison**
   - Compare labeling efficiency (labels per unit time)
   - Compare dataset diversity (class balance, range coverage)
   - Compare label quality (accuracy, confidence)
   - Establish when active perception is worth the mechanical complexity

8. **Radar feature sufficiency analysis**
   - Train radar-only classifiers on auto-labeled data
   - Compare radar-only accuracy to camera-only accuracy
   - Identify which vessel classes are distinguishable by radar features alone
   - Guide future radar classifier architectures (which features matter most)

### 7.5 Publications

9. **Conference paper (target: ICRA, IROS, CVPR, or ICCV)**
   - Focus: Active perception for automated dataset construction
   - Contributions: Data flywheel, PTZ scheduling strategies, label transfer quality

10. **Journal paper (target: IEEE Transactions on Robotics, IJRR, or Sensors)**
    - Extended analysis: Multi-modal fusion, long-term deployment results, ablation studies
    - Dataset paper: Detailed description, benchmarks, baseline classifier results

11. **Workshop/short paper opportunities**
    - Maritime robotics workshops at ICRA/IROS
    - Active perception / embodied AI workshops
    - Dataset and benchmark challenges

---

## 8. Broader Impact

### 8.1 Safety and Maritime Operations

- Improved collision avoidance for autonomous surface vehicles
- Enhanced situational awareness for manned vessels (augmented radar displays)
- Search and rescue operations (automated detection of vessels in distress)
- Port security and coastal surveillance (automated anomaly detection)

### 8.2 Scientific Community

- First large-scale labeled maritime radar dataset (fills critical gap)
- Reproducible pipeline for others to build similar datasets
- Benchmarks for future maritime radar classification research
- Cross-modal learning testbed (radar-camera fusion)

### 8.3 Commercial Applications

- Reduced cost of maritime autonomy development (off-the-shelf labeled data)
- Accelerated training for maritime AI systems
- Validation datasets for radar manufacturers and maritime system integrators

### 8.4 Educational Opportunities

- Undergraduate research experience (Sam Cancilla, Mateo Altomare)
- Training in sensor fusion, computer vision, robotics, and machine learning
- Hands-on deployment and field testing experience
- Potential for senior design projects and MS theses

---

## 9. Budget Estimate

| Item | Cost | Justification |
|------|------|---------------|
| Furuno DRS4D-NXT radar | $5,000 | X-band pulse compression radar (already acquired) |
| FLIR M364C PTZ camera | $15,000 | 360-degree pan, 30x zoom, RGB + thermal (already acquired) |
| NVIDIA Jetson Orin | $2,000 | Real-time AI inference and PTZ control |
| Mounting hardware and cabling | $1,000 | Mast, enclosures, weatherproofing |
| Network storage (10TB) | $1,500 | NAS for radar data and imagery |
| Power and UPS | $1,000 | Continuous operation with backup |
| Maintenance and spares | $2,000 | PTZ replacement parts, cables, connectors |
| Student stipends (2 UG @ 10 hr/wk, 12 mo) | $12,000 | Sam Cancilla, Mateo Altomare |
| Travel to conferences | $4,000 | Present results at ICRA/IROS/CVPR |
| Publication fees | $1,500 | Open-access publication charges |
| **Total** | **$45,000** | **Approximate project cost** |

Note: Radar and PTZ camera already acquired. Remaining funds needed: ~$25,000.

---

## 10. Success Criteria

The project will be considered successful if it achieves the following:

### Minimum Viable Success (must achieve):
1. Deploy hardware and collect synchronized radar + PTZ data for ≥3 months
2. Implement end-to-end labeling pipeline (radar blob → PTZ observation → label assignment)
3. Generate labeled dataset with ≥10,000 radar samples across ≥3 vessel classes
4. Validate label accuracy ≥70% on manually labeled ground truth
5. Train baseline radar classifier achieving ≥60% accuracy on held-out test set
6. Submit conference paper to ICRA, IROS, or CVPR

### Target Success (desired goals):
7. Collect ≥6 months of data with ≥50,000 labeled radar samples across ≥5 classes
8. Achieve label accuracy ≥80% via dual-detector fusion
9. Demonstrate data flywheel: Show measurable improvement in labeling efficiency (labels per camera-hour) after deploying radar classifier for PTZ scheduling
10. Radar classifier accuracy ≥75% (competitive with camera-only baseline)
11. Accept paper at major conference + release dataset publicly

### Stretch Goals (aspirational):
12. Collect ≥12 months of data with ≥200,000 labeled samples
13. Achieve label accuracy ≥90% (approaching human-level)
14. Deploy system on mobile platform (vessel-mounted) and demonstrate underway operation
15. Win best paper or dataset award at major conference
16. Secure follow-on funding for multi-site deployment or autonomous vessel integration

---

## 11. Conclusion

This project addresses a critical bottleneck in maritime radar research: the lack of labeled training data. By leveraging active PTZ perception to automatically label radar targets, we enable scalable dataset construction without prohibitive manual effort. The resulting dataset will accelerate maritime autonomy research, improve collision avoidance systems, and establish a new paradigm for cross-modal dataset construction via active perception.

The data flywheel concept ensures that the system becomes more efficient over time, reducing the marginal cost of each new label. This creates a sustainable path toward very large datasets (100k+ samples) that are currently infeasible with manual labeling.

Beyond the immediate dataset contribution, this work establishes methodological foundations for active perception in robotics: How should an agent allocate limited sensing resources (PTZ camera time) to maximize information gain? How can we validate and trust automatically generated labels? How do we design feedback loops where learned models improve data collection strategies?

We believe this project will make significant contributions to maritime robotics, computer vision, and active perception, while providing valuable research experience for undergraduate team members and establishing infrastructure for future coastal observation research.

---

## 12. References

### Maritime Radar Datasets (or lack thereof):
- No large-scale labeled maritime radar datasets currently exist
- Automotive radar datasets (nuScenes, RADIATE) are not transferable to maritime domain

### Object Detection:
- YOLOv8/v9: Real-time object detection
- DETR (Detection Transformer): Transformer-based detection for small/occluded objects

### Maritime Vision Datasets:
- SeaShips: Maritime vessel detection dataset
- SMD (Singapore Maritime Dataset): Multi-class vessel dataset
- ABOships: Aerial and surface vessel imagery

### Active Perception:
- Bajcsy, R. (1988). Active perception. Proceedings of the IEEE.
- Atanasov, N., et al. (2015). Information acquisition with sensing robots.

### Sensor Fusion:
- Multiple works on radar-camera fusion for automotive (none for maritime)
- Gap: Most assume fixed cameras with overlapping FOV, not active PTZ

### Spatiotemporal Clustering:
- ST-DBSCAN: Birant, D., & Kut, A. (2007). ST-DBSCAN for clustering spatial-temporal data.

---

**End of Proposal**
