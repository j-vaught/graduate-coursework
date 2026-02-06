# Literature Review Outline: Radar-Guided Camera Labeling for Maritime Dataset Construction

## Purpose

This document organizes the literature review for the radar-guided camera labeling project. Each section is prioritized (High / Medium / Low) based on its relevance to the core technical contribution. Sections include research questions to answer, suggested search terms, and starting references.

---

## Section 1: Maritime Object Detection Datasets and the Annotation Gap [HIGH PRIORITY]

### Research Questions
- What labeled maritime datasets currently exist, and what are their sizes and annotation methods?
- How do maritime datasets compare in scale and diversity to automotive benchmarks?
- What is the documented cost and inter-annotator agreement for maritime image labeling?
- What domain-specific challenges (small targets, glare, wakes, weather) affect annotation quality?

### Search Terms
- Maritime object detection dataset, ship detection dataset, vessel detection benchmark
- Maritime annotation, marine image labeling, coastal surveillance dataset
- Singapore Maritime Dataset, SeaShips, MCShips, ABOShips

### Starting References
- Prasad et al., "Video processing from electro-optical sensors for object detection and tracking in maritime environment: A survey" (2017) -- Singapore Maritime Dataset
- Zhang et al., "WaterScenes: A multi-task 4D radar-camera fusion dataset" (2024)
- Jang et al., "MOANA: Multi-radar dataset for maritime perception" (2024)
- Shao et al., "SeaShips: A large-scale precisely annotated dataset for ship detection" (2018)

### Key Gap to Investigate
Maritime datasets are orders of magnitude smaller than automotive equivalents (ImageNet, COCO, nuScenes). Documenting this gap quantitatively motivates the need for automated labeling.

---

## Section 2: Radar-Camera Sensor Registration and Calibration [HIGH PRIORITY]

### Research Questions
- What methods exist for registering marine radar with optical cameras?
- How is extrinsic calibration performed between radar (polar, 2D) and camera (perspective, 2D) sensors?
- What accuracy can be achieved for radar-camera registration on stationary platforms?
- How does calibration drift over time, and what recalibration strategies exist?

### Search Terms
- Radar camera calibration, radar camera registration, extrinsic calibration radar optical
- Marine radar camera alignment, sensor fusion calibration, cross-modal registration
- Homography radar camera, coordinate transformation radar pixel

### Starting References
- Sugimoto et al., "Obstacle detection using millimeter-wave radar and its visualization on image data" (2004)
- Peršić et al., "Extrinsic 6DoF calibration of a radar-LiDAR-camera system" (2019)
- Caesar et al., "nuScenes: A multimodal dataset for autonomous driving" (2020) -- calibration methodology

### Key Gap to Investigate
Most radar-camera calibration work uses 77 GHz automotive radar. X-band marine radar has different resolution, range, and mounting geometry. Transferability of automotive calibration methods to maritime X-band settings is an open question.

---

## Section 3: Radar-to-Camera Projection and Bounding Box Generation [HIGH PRIORITY]

### Research Questions
- How are radar detections (range, bearing) projected into camera pixel coordinates?
- What methods handle the 3D ambiguity (radar gives range/bearing but not elevation)?
- How are bounding box dimensions estimated from radar-only information?
- What is the expected projection error at various ranges?

### Search Terms
- Radar to camera projection, radar detection bounding box, polar to pixel transformation
- Range-dependent bounding box, radar-guided annotation, cross-modal bounding box generation
- Radar target projection error, radar camera geometric mapping

### Starting References
- Nabati and Qi, "CenterFusion: Center-based radar and camera fusion for 3D object detection" (2021)
- Kim et al., "GRIF Net: Gated region of interest fusion for robust 3D object detection from radar and LiDAR" (2020)
- Meyer and Kuschk, "Automotive radar dataset for deep learning based 3D object detection" (2019)

### Key Gap to Investigate
Wide-FOV lens distortion complicates accurate projection at image periphery. Range-dependent size priors for maritime vessels differ substantially from automotive targets. The achievable bounding box IoU from radar-only projection needs characterization.

---

## Section 4: Automated and Weakly-Supervised Dataset Construction [HIGH PRIORITY]

### Research Questions
- What methods exist for generating training labels without full manual annotation?
- How has cross-modal supervision been used to create labeled datasets?
- What quality thresholds are needed for auto-generated labels to be useful for training?
- How do noisy labels affect detector training, and what mitigation strategies exist?

### Search Terms
- Automated dataset construction, weakly supervised object detection, cross-modal supervision
- Noisy label learning, label noise robust training, self-training object detection
- Pseudo label, teacher-student framework, data programming

### Starting References
- Ratner et al., "Data programming: Creating large training sets, quickly" (2016)
- Li et al., "Learning from noisy labels with distillation" (2017)
- Xie et al., "Self-training with noisy student improves ImageNet classification" (2020)

### Key Gap to Investigate
Using radar as a cross-modal label source for camera imagery is distinct from typical self-training or pseudo-labeling (which use the same modality). The noise characteristics of radar-projected labels are systematic (calibration, projection geometry) rather than random, which may require different mitigation strategies.

---

## Section 5: Radar-Camera Fusion for Maritime Applications [MEDIUM PRIORITY]

### Research Questions
- What radar-camera fusion architectures have been applied to maritime surveillance?
- How do maritime fusion systems differ from automotive fusion systems?
- What performance gains does radar-camera fusion provide over single-sensor approaches at sea?

### Search Terms
- Maritime radar camera fusion, marine sensor fusion, coastal surveillance multi-sensor
- Ship detection radar camera, maritime situational awareness sensor fusion
- Marine radar optical fusion, harbor surveillance multi-modal

### Starting References
- Sheeny et al., "RADIATE: A radar dataset for automotive demonstration and intelligent transportation" (2021)
- Zhang et al., "WaterScenes" (2024)
- Wang et al., "Active acquisition for multimodal maritime surveillance" (group paper)

### Key Gap to Investigate
Most radar-camera fusion literature targets automotive scenarios with 77 GHz radar. Maritime X-band radar has fundamentally different characteristics (longer range, lower angular resolution, 2D PPI format). The extent to which automotive fusion techniques transfer to maritime settings is underexplored.

---

## Section 6: X-Band Marine Radar Signal Processing [MEDIUM PRIORITY]

### Research Questions
- What detection and tracking algorithms are standard for X-band marine radar?
- How does pulse compression affect target detection characteristics in the Simrad Halo 20+?
- What sea clutter models and suppression techniques are relevant?
- How do CFAR and other adaptive threshold methods perform in maritime environments?

### Search Terms
- X-band marine radar signal processing, marine radar target detection, maritime radar CFAR
- Sea clutter suppression, marine radar pulse compression, radar target tracking maritime
- Simrad Halo radar, navigation radar signal processing

### Starting References
- Skolnik, "Radar Handbook" (2008) -- sea clutter chapter
- Watts, "Radar sea clutter: Performance limits and applications" (2012)
- Cancilla et al., "ST-DBSCAN for marine radar target clustering" (group paper)
- Vaught et al., "Synthetic radar data generation for maritime applications" (group paper)

### Key Gap to Investigate
Consumer-grade marine radar (Simrad Halo 20+) may have different signal characteristics than research-grade or military X-band systems described in the literature. Characterizing detection performance of COTS marine radar for dataset construction purposes is needed.

---

## Section 7: Edge Computing for Real-Time Sensor Fusion [LOW PRIORITY]

### Research Questions
- What are the computational constraints of running sensor fusion on edge hardware (Jetson Orin)?
- What model optimization techniques (quantization, pruning, TensorRT) enable real-time inference?
- What latency budgets are acceptable for the labeling pipeline?

### Search Terms
- Edge computing sensor fusion, Jetson Orin real-time inference, embedded sensor fusion
- TensorRT object detection, model optimization edge deployment, real-time maritime detection

### Starting References
- NVIDIA Jetson Orin technical documentation
- Molchanov et al., "Pruning convolutional neural networks for resource efficient inference" (2017)

### Key Gap to Investigate
The labeling pipeline does not strictly require real-time operation (labels can be generated offline), but real-time capability would enable continuous autonomous data collection. Characterizing the throughput bottleneck is useful for system design.

---

## Cross-Cutting Gaps and Open Questions

1. **X-band maritime vs. 77 GHz automotive transfer**: Most radar-camera literature uses automotive 77 GHz radar. How well do calibration, projection, and fusion methods transfer to X-band marine radar?
2. **Wide-FOV projection accuracy**: The Lucid camera's ~100deg FOV introduces significant lens distortion. What projection accuracy is achievable at the image periphery?
3. **Scalability of continuous auto-labeling**: Can the system generate labels 24/7 autonomously, and what failure modes emerge during extended unattended operation?
4. **Label noise characterization**: Radar-projected labels have systematic (not random) noise from calibration and projection. How does this affect downstream model training compared to random label noise?

---

## Review Strategy

1. Begin with HIGH priority sections (1-4) as they directly support the core contribution
2. Use forward/backward citation chaining from starting references
3. Search IEEE, ACM, Elsevier (Ocean Engineering, Remote Sensing), and arXiv
4. Prioritize papers from 2019-2025 but include foundational works
5. Track references in `references.bib` organized by section
