# Project Proposal: Radar-Guided Camera Labeling for Automated Maritime Dataset Construction

**Lead**: Ty Dangerfield
**Team**: J.C. Vaught, Douglas Cahl
**Principal Investigator**: Dr. Yi Wang

---

## 1. Problem Statement

Manual annotation of maritime camera imagery is the primary bottleneck in developing robust object detection models for coastal surveillance. Current maritime datasets are small (thousands of images) compared to automotive benchmarks (hundreds of thousands), and the annotation process is expensive, slow, and inconsistent. The maritime domain poses additional challenges: targets are small, distant, and visually similar against complex water/sky backgrounds, leading to high inter-annotator disagreement.

## 2. Motivation

Cross-modal supervision offers a path to break the annotation bottleneck. Marine radar naturally detects surface targets at ranges far beyond camera visibility, providing target presence and location without human input. If radar detections can be reliably projected into camera pixel coordinates, the radar effectively becomes an automated annotation engine, generating bounding box labels at the rate of radar scans (typically 24-48 RPM) rather than the rate of human annotators.

This approach is particularly compelling for maritime applications because:
- Radar coverage is continuous and weather-independent
- Stationary coastal platforms provide stable sensor geometry
- The annotation gap in maritime datasets is severe compared to automotive domains
- X-band marine radar provides sufficient angular resolution for target localization

## 3. Technical Approach

### 3.1 Hardware Configuration

**Sensors:**
- Simrad Halo 20+ X-band pulse compression radar
- Lucid Allied Vision stationary camera (approximately 100-degree FOV)
- GPS receiver for geo-referencing
- IMU for orientation sensing

**Compute:**
- NVIDIA Jetson Orin for on-site data logging and real-time processing

### 3.2 Sensor Calibration
- Establish extrinsic transformation between radar and camera frames
- Use GPS/IMU to geo-reference both sensor coordinate systems
- Calibrate camera intrinsics (focal length, distortion coefficients)
- Validate registration accuracy against known landmarks

### 3.3 Radar Detection
- Process raw radar returns from the Simrad Halo 20+ (pulse compression, X-band)
- Apply CFAR or threshold-based detection to extract target range and bearing
- Track detections temporally to suppress false alarms and associate persistent targets

### 3.4 Polar-to-Pixel Projection
- Transform radar detections (range, bearing) to geo-referenced world coordinates (lat/lon) using platform GPS and radar mount geometry
- Project world coordinates to camera pixel coordinates using the calibrated camera model
- Generate bounding box proposals around projected centroids using range-dependent size priors (distant targets produce smaller boxes)

### 3.5 Bounding Box Generation and Refinement
- Apply size and aspect ratio priors based on target range and expected vessel dimensions
- Use temporal consistency filtering: require targets to persist across multiple radar scans before generating labels
- Optionally refine bounding boxes with a lightweight detector as a cross-check

### 3.6 Label Quality Assurance
- Compare radar-generated labels against hand-annotated ground truth subsets
- Compute precision, recall, and IoU metrics for the automated labels
- Identify systematic error sources (calibration drift, multipath, sea clutter false alarms)
- Iterate on calibration and filtering parameters to maximize label quality

## 4. Data Collection Plan

**Platform:** Stationary coastal observation site with co-located radar and camera

**Data Flow:**
1. Radar detections (range, bearing) acquired at 24-48 RPM
2. GPS/IMU provides platform position and orientation
3. Detections projected to camera pixel coordinates
4. Bounding boxes generated around projected target locations
5. Labeled camera images stored with metadata

**Collection Parameters:**
- Continuous recording during daylight hours
- Varying sea states, weather conditions, and vessel traffic density
- Estimated thousands of radar-camera frame pairs per day
- Periodic manual annotation of camera frames for validation

**Storage and Logging:**
- Raw radar returns and processed detections
- Synchronized camera frames with timestamps
- GPS/IMU telemetry
- Generated bounding box annotations with confidence scores

## 5. Timeline

| Phase | Description | Duration | Status |
|-------|-------------|----------|--------|
| Phase 1 | Hardware deployment and data collection | 2 months | In progress |
| Phase 2 | Sensor calibration and projection pipeline | 1 month | In progress |
| Phase 3 | Automated label generation at scale | 1 month | Planned |
| Phase 4 | Label quality evaluation against ground truth | 1 month | Planned |
| Phase 5 | Model training and benchmark comparison | 2 months | Planned |
| Phase 6 | Paper preparation and submission | 1 month | Planned |

**Total estimated duration:** 8 months

## 6. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Calibration drift over time | Medium | High | Periodic recalibration, landmark-based drift monitoring |
| Wide-FOV lens distortion degrades projection accuracy | Medium | Medium | Careful distortion modeling, limit analysis to central FOV initially |
| Sea clutter generates false radar detections | High | Medium | CFAR tuning, temporal persistence filtering, clutter map subtraction |
| X-band resolution insufficient for close-range target separation | Low | Medium | Leverage pulse compression; accept merged labels for tightly spaced targets |
| Multipath and sidelobe returns create ghost targets | Medium | Medium | Cross-reference with camera (if target not visible, suppress label) |
| Limited vessel diversity in collection area | Medium | Low | Extended collection periods, opportunistic collection during events |
| Synchronization errors between radar and camera | Low | High | Hardware-triggered capture with shared clock source |
| Environmental obstruction of radar or camera view | Low | Medium | Careful site selection and sensor placement |

## 7. Expected Contributions

1. **Large-scale labeled maritime dataset:** A dataset of labeled maritime camera imagery generated without manual annotation, orders of magnitude larger than existing hand-annotated maritime datasets.

2. **Open-source projection pipeline:** A complete radar-to-camera projection and automated labeling pipeline adaptable to other marine radar and camera configurations.

3. **Empirical label quality analysis:** Rigorous quantitative evaluation of radar-generated label quality (precision, recall, IoU) compared to manual annotation, including failure mode analysis.

4. **Model performance validation:** Demonstration that object detection models trained on radar-generated labels approach or match the performance of manually-supervised models when tested on hand-annotated ground truth.

5. **Domain adaptation insights:** Analysis of transferability challenges from automotive (77 GHz FMCW) radar-camera methods to maritime (X-band pulse compression) settings, including differences in resolution, clutter characteristics, and target dynamics.

6. **Practical deployment guidelines:** Recommendations for sensor selection, calibration procedures, and quality control methods for operational maritime surveillance systems.

## 8. Success Metrics

**Technical Metrics:**
- Projection accuracy: Mean pixel error < 20 pixels for targets within 2 km
- Label precision: > 85% of generated bounding boxes correspond to true vessels
- Label recall: > 75% of visible vessels receive bounding box labels
- IoU agreement: Mean IoU > 0.5 compared to manual annotations

**Dataset Metrics:**
- Minimum 10,000 labeled camera frames
- Diverse conditions: At least 3 sea states, 5 weather conditions
- Target diversity: At least 5 vessel classes represented

**Model Performance:**
- Object detection mAP within 5% of manually-supervised baseline
- Successful generalization to unseen maritime datasets

## 9. Related Work and Novelty

**Automotive Radar-Camera Fusion:**
Extensive prior work exists in automotive settings using 77 GHz FMCW radar with narrow FOV cameras. These methods exploit high range and velocity resolution but face different challenges (short range, dense urban clutter, high vehicle speeds).

**Maritime Object Detection:**
Existing maritime datasets (SMD, MID, SeaShips) are manually annotated and limited in scale. Prior maritime radar work focuses on standalone radar detection rather than cross-modal label generation.

**Novelty of This Work:**
- First application of radar-guided automated annotation to maritime domain
- Adaptation to X-band pulse compression radar (different modality than automotive FMCW)
- Wide-FOV camera projection challenges not addressed in automotive literature
- Systematic evaluation of automated label quality for maritime targets
- Open-source pipeline for community replication and extension

## 10. Deliverables

**Software:**
- Radar detection and tracking module
- Sensor calibration and projection pipeline
- Automated bounding box generation system
- Label quality evaluation framework
- All code released under permissive open-source license

**Data:**
- Labeled maritime camera dataset (subject to security review)
- Calibration data and procedures
- Ground truth annotations for validation subset

**Publications:**
- Conference paper presenting system and initial results
- Extended journal paper with comprehensive evaluation and analysis
- Technical documentation and tutorials

**Documentation:**
- System architecture and design decisions
- Deployment and calibration procedures
- Dataset statistics and characteristics
- Lessons learned and recommendations

---

## Appendix A: Data Flow Diagram

```
┌─────────────┐
│ Simrad Halo │ Range, Bearing
│   Radar     ├──────────────┐
└─────────────┘              │
                             ▼
┌─────────────┐        ┌──────────────┐
│  GPS + IMU  │ Pose   │  Projection  │ Pixel (x,y)
│             ├───────>│   Pipeline   ├─────────────┐
└─────────────┘        └──────────────┘             │
                             ▲                       ▼
┌─────────────┐              │              ┌─────────────────┐
│   Lucid     │ Intrinsics   │              │  Bounding Box   │
│   Camera    ├──────────────┘              │   Generator     │
└──────┬──────┘                             └────────┬────────┘
       │                                             │
       │ Image                              Labels   │
       ▼                                             ▼
┌─────────────────────────────────────────────────────────────┐
│              Labeled Maritime Dataset                       │
└─────────────────────────────────────────────────────────────┘
```

## Appendix B: Contact Information

**Ty Dangerfield** (Project Lead)
Email: tdangerf@email.sc.edu

**J.C. Vaught**
Email: jvaught@sc.edu

**Douglas Cahl**
Email: dcahl@email.sc.edu

**Dr. Yi Wang** (Principal Investigator)
Email: wangyi@cse.sc.edu
