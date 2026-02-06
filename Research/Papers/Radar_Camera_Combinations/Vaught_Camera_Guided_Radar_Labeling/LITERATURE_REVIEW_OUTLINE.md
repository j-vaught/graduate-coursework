# Literature Review Outline: Camera-Guided Radar Labeling via Active PTZ Perception

## Purpose

This document organizes the literature review for the camera-guided radar labeling project. Each section is prioritized (High / Medium / Low) based on its relevance to the core technical contribution -- using active PTZ perception to automatically label maritime radar blobs. Sections include research questions, search terms, and starting references.

---

## Section 1: Maritime Radar Datasets and the Label Gap [HIGH PRIORITY]

### Research Questions
- What labeled maritime radar datasets currently exist?
- How are radar targets currently labeled in the maritime domain (AIS correlation, manual annotation, expert classification)?
- What is the scale gap between maritime radar datasets and automotive radar benchmarks?
- What radar blob features are typically used for classification?

### Search Terms
- Maritime radar dataset, marine radar classification, ship radar signature
- Radar target classification maritime, radar blob labeling, marine radar benchmark
- AIS radar correlation, radar target recognition

### Starting References
- Jang et al., "MOANA: Multi-radar dataset for maritime perception" (2024)
- Zhang et al., "WaterScenes: A multi-task 4D radar-camera fusion dataset" (2024)
- Caesar et al., "nuScenes: A multimodal dataset for autonomous driving" (2020) -- automotive radar benchmark for comparison
- Sheeny et al., "RADIATE: A radar dataset for automotive demonstration and intelligent transportation" (2021)

### Key Gap to Investigate
Maritime radar classification datasets are nearly nonexistent. Automotive radar benchmarks (nuScenes, RADIATE) have thousands of labeled frames; maritime equivalents have essentially zero labeled radar blob datasets with vessel type classifications. This gap is the primary motivation for the project.

---

## Section 2: Camera-to-Radar Cross-Modal Labeling [HIGH PRIORITY]

### Research Questions
- Has visual classification been used to label radar data (in any domain)?
- What is the state of the art in camera-to-radar label transfer?
- How is the association between a visual detection and a radar blob established?
- What label noise is introduced by cross-modal transfer, and how is it handled?

### Search Terms
- Camera to radar labeling, visual classification radar annotation, cross-modal label transfer
- Radar label generation, camera guided radar, optical to radar label propagation
- Multi-modal label transfer, cross-sensor annotation

### Starting References
- Wang et al., "Active acquisition for multimodal maritime surveillance" (group paper)
- Nabati and Qi, "CenterFusion: Center-based radar and camera fusion for 3D object detection" (2021)
- Lim et al., "Radar and camera early fusion for vehicle detection in advanced driver assistance systems" (2019)

### Key Gap to Investigate
The camera→radar label direction is novel. Nearly all existing work uses radar to augment camera detection or fuses both modalities for joint inference. Using camera classification as the label source for radar data -- particularly with a PTZ active perception approach -- appears to be unexplored in the literature. This is a key novelty claim.

---

## Section 3: PTZ Camera Active Perception and Scheduling [HIGH PRIORITY]

### Research Questions
- How are PTZ cameras used for active perception in surveillance?
- What scheduling algorithms exist for PTZ camera tasking across multiple targets?
- How is the trade-off between coverage breadth and observation depth handled?
- What is the state of the art in "look-then-classify" active perception?

### Search Terms
- PTZ camera active perception, PTZ scheduling algorithm, active surveillance camera
- PTZ target tracking, pan-tilt-zoom scheduling, active vision system
- PTZ camera tasking, multi-target PTZ allocation, active object recognition

### Starting References
- Qureshi and Terzopoulos, "Smart camera networks in virtual reality" (2007) -- PTZ scheduling foundations
- Park et al., "Real-time tracking and detection of multiple targets with pan-tilt-zoom cameras" (2015)
- Chen et al., "Active detection via adaptive submodularity" (2015)

### Key Gap to Investigate
PTZ scheduling literature focuses on tracking known targets or maximizing surveillance coverage. Using PTZ as a "labeling engine" -- deliberately slewing to classify targets for dataset construction rather than for real-time situational awareness -- is a distinct use case with different optimization objectives (label diversity, class balance, confidence maximization vs. threat detection).

---

## Section 4: Object Detection for Maritime Targets (YOLO, DETR, Thermal) [HIGH PRIORITY]

### Research Questions
- How do YOLO and DETR perform on maritime imagery?
- What role does thermal imagery play in maritime detection (day/night, fog, glare)?
- What maritime target classes are standard, and what detection accuracy is achievable?
- How does zoom level affect detection confidence for distant maritime targets?

### Search Terms
- Maritime object detection YOLO, ship detection DETR, vessel classification deep learning
- Thermal maritime detection, infrared ship detection, FLIR maritime
- Maritime target classification, boat detection neural network, coastal surveillance detection

### Starting References
- Redmon et al., "YOLOv3: An incremental improvement" (2018) / Jocher et al., YOLOv8 documentation
- Carion et al., "End-to-end object detection with transformers" (DETR, 2020)
- Prasad et al., "Video processing from electro-optical sensors for object detection and tracking in maritime environment" (2017)
- Ribeiro et al., "A study of deep convolutional auto-encoders for anomaly detection in maritime environments" (2018)

### Key Gap to Investigate
Detection performance on PTZ imagery (variable zoom, rapid pan) differs from static camera benchmarks. The effect of 30x optical zoom on detection confidence vs. the time cost of zooming in needs characterization. Thermal+RGB dual-stream detection for maritime targets at various ranges is underexplored.

---

## Section 5: Radar Blob Classification and Feature Extraction [MEDIUM PRIORITY]

### Research Questions
- What features can be extracted from marine radar blobs for classification?
- What machine learning methods have been applied to radar blob/target classification?
- How do blob characteristics (intensity, extent, persistence, Doppler) correlate with target type?
- What classification accuracy is achievable from radar features alone?

### Search Terms
- Radar blob classification, radar target feature extraction, marine radar pattern recognition
- Radar signature classification, radar echo classification, radar target recognition features
- Marine radar machine learning, ship radar classification, radar blob features

### Starting References
- Watts, "Radar sea clutter" (2012) -- target vs clutter discrimination
- Cancilla et al., "ST-DBSCAN for marine radar target clustering" (group paper)
- Vaught et al., "Synthetic radar data generation for maritime applications" (group paper)

### Key Gap to Investigate
Radar blob classification using COTS marine radar (Furuno DRS4D-NXT) features is poorly characterized. Most radar classification literature uses military-grade or synthetic aperture radar. Whether consumer-grade marine radar provides sufficient feature richness for multi-class vessel classification is an open question -- and exactly what the auto-labeled dataset would help answer.

---

## Section 6: Automated and Self-Supervised Dataset Construction [MEDIUM PRIORITY]

### Research Questions
- What methods exist for constructing labeled datasets without full manual annotation?
- How has the "data flywheel" concept been applied in other domains?
- What quality metrics are used to evaluate auto-generated labels?
- How do noisy labels affect downstream classifier training?

### Search Terms
- Automated dataset construction, self-supervised labeling, data flywheel machine learning
- Pseudo label learning, noisy label robust training, self-training dataset
- Active learning dataset construction, curriculum learning from noisy labels

### Starting References
- Ratner et al., "Data programming: Creating large training sets, quickly" (2016)
- Xie et al., "Self-training with noisy student improves ImageNet classification" (2020)
- Sohn et al., "FixMatch: Simplifying semi-supervised learning with consistency and confidence" (2020)

### Key Gap to Investigate
The closed-loop data flywheel (label → train → improve labeling → label more) is well-studied in NLP/web data but rare in sensor fusion. Applying this concept to radar-camera maritime systems where the loop includes physical PTZ actuation adds latency and mechanical constraints not present in software-only flywheel systems.

---

## Section 7: Edge Computing for Multi-Sensor Maritime Systems [LOW PRIORITY]

### Research Questions
- What are the computational requirements for running dual-stream detectors on edge hardware?
- How does PTZ control latency interact with inference latency on Jetson Orin?
- What model optimization techniques enable real-time PTZ tasking + detection?

### Search Terms
- Edge computing maritime, Jetson Orin multi-sensor, embedded PTZ control
- Real-time object detection edge, TensorRT maritime, edge inference multi-stream

### Starting References
- NVIDIA Jetson Orin technical documentation
- Redmon and Farhadi, "YOLO9000: Better, faster, stronger" (2017) -- real-time detection focus

### Key Gap to Investigate
The system must run PTZ control, dual-stream detection (YOLO + DETR), and radar processing simultaneously on a single Jetson Orin. Whether this is computationally feasible at useful frame rates, or whether a tiered approach (fast YOLO always, DETR on demand) is necessary, needs characterization.

---

## Cross-Cutting Gaps and Open Questions

1. **PTZ "look-then-label" vs. fixed-FOV approaches**: No existing work uses PTZ cameras as active labeling engines for radar data. This is the core novelty.
2. **Direct angular calibration without GPS/IMU**: Most radar-camera registration assumes GPS/IMU availability. Calibrating directly between PTZ heading and radar bearing via landmarks or known targets is a practical necessity here.
3. **Camera→radar label direction is novel**: Nearly all fusion literature goes radar→camera or radar+camera→joint. Using camera as the label source for radar is underexplored.
4. **Closed-loop data flywheel with physical actuation**: The feedback loop includes physical PTZ motion, adding latency and mechanical constraints absent from software-only self-training loops.
5. **COTS marine radar for ML**: Using consumer-grade marine radar (Furuno DRS4D-NXT) for machine learning classification, rather than research-grade or military radar, is underexplored.

---

## Review Strategy

1. Begin with HIGH priority sections (1-4) as they directly support the core contribution
2. Use forward/backward citation chaining from starting references
3. Search IEEE, ACM, Elsevier (Ocean Engineering, Remote Sensing), MDPI (Sensors, Remote Sensing), and arXiv
4. Prioritize papers from 2019-2025 but include foundational works
5. Track references in `references.bib` organized by section
6. Pay special attention to negative results: cases where cross-modal labeling or PTZ scheduling failed, as these inform system design decisions
