# Quarterly Work Presentation Outline
## September 9, 2025 - January 2026
### Image-Focused / Minimal Text

---

## SLIDE 1: Title Slide
**Text:** 
- "Q4 2025 Research Summary"
- "Jacob Vaught | IMSEL Lab | USC"
- "September 2025 - January 2026"

**Image:** 
- [ ] GENERATE: Hero collage of 4 key outputs (radar PPI, thermal overlay, detection boxes, GUI screenshot)

---

## SLIDE 2: Overview - 5 Project Areas
**Text:** Single line per area

**Image:**
- [ ] GENERATE: 5-icon infographic (radar dish, camera, neural network, simulation wave, tools)

---

# SECTION 1: RADAR COLLECTION SOFTWARE

## SLIDE 3: Radar Hardware Setup
**Text:** "Furuno NXT Marine Radar Integration"

**Images:**
- [ ] GET: Photo of Furuno radar unit (from hardware docs or web)
- [ ] GET: Photo of Raspberry Pi setup

---

## SLIDE 4: Web Control Dashboard
**Text:** "Real-time Web Control Interface"

**Images:**
- [ ] REUSE: Screenshot of web dashboard (need to capture from running system or generate mockup)
- [ ] GENERATE: Simple UI mockup showing controls if no screenshot exists

---

## SLIDE 5: Data Collection Output
**Text:** "CSV + PNG Output Pipeline"

**Images:**
- [ ] REUSE: `radar_post_processing/RadarPlotter/figures/example_viridis_output.png`
- [ ] REUSE: Raw CSV data snippet (screenshot)

---

# SECTION 2: RADAR POST-PROCESSING TOOLS

## SLIDE 6: RadarPlotter App
**Text:** "High-Performance CSV to PPI Converter"

**Images:**
- [ ] REUSE: `radar_post_processing/RadarPlotter/figures/01_light_mode_initial.png`
- [ ] REUSE: `radar_post_processing/RadarPlotter/figures/04_processing_dark.png`
- [ ] REUSE: `radar_post_processing/RadarPlotter/figures/05_processing_complete_light.png`

---

## SLIDE 7: RadarPlotter Output Examples
**Text:** "Multiple Colormap Support"

**Images:**
- [ ] REUSE: `radar_post_processing/RadarPlotter/figures/example_viridis_output.png`
- [ ] GENERATE: Grid of same PPI in different colormaps (viridis, turbo, magma, grayscale)

---

## SLIDE 8: RADICAL Annotator
**Text:** "Air-Gap Ready Image Labeling Tool"

**Images:**
- [ ] REUSE: Screenshot of annotator GUI (check for existing)
- [ ] GENERATE: Annotation workflow diagram (bbox, polygon, point)

---

## SLIDE 9: Camera Drivers
**Text:** "FLIR Camera Control Suite"

**Images:**
- [ ] GET: FLIR M364C product photo
- [ ] GENERATE: Architecture diagram (RTSP -> Driver -> PTZ)

---

# SECTION 3: RADAR SYNTHETIC GENERATION

## SLIDE 10: Simulation Overview
**Text:** "Physics-Based Radar Simulation"

**Images:**
- [ ] REUSE: `Object_detection_work/GazeMamba/radar_sim/world_view.png`
- [ ] REUSE: `Object_detection_work/GazeMamba/radar_sim/world_debug.png`

---

## SLIDE 11: PPI Output Generation
**Text:** "Synthetic PPI Frames"

**Images:**
- [ ] REUSE: `Object_detection_work/GazeMamba/radar_sim/ppi_output.png`
- [ ] REUSE: `Object_detection_work/GazeMamba/radar_sim/ppi_blobs.png`
- [ ] REUSE: `Object_detection_work/GazeMamba/radar_sim/ppi_diagnostic.png`

---

## SLIDE 12: radar_sim_L3 GUI
**Text:** "Data Extraction & Scene Generation"

**Images:**
- [ ] REUSE: `radar_synthetic_generation/radar_sim_L3/docs/images/gui_screenshot.png`
- [ ] REUSE: `radar_synthetic_generation/radar_sim_L3/docs/images/workflow.png`
- [ ] REUSE: `radar_synthetic_generation/radar_sim_L3/docs/images/annotation_process.png`

---

## SLIDE 13: Signal Processing Visualization
**Text:** "Pulse & Beam Simulation"

**Images:**
- [ ] REUSE: `radar_synthetic_generation/temp_simu/implementation/ppi_realistic_cartesian.png`
- [ ] REUSE: `radar_synthetic_generation/temp_simu/implementation/ppi_beam_spread_polar.png`
- [ ] REUSE: `radar_synthetic_generation/temp_simu/implementation/pulse_elongation_range_profile.png`

---

## SLIDE 14: Parameter Grid Study
**Text:** "Bandwidth × Pulse Duration Effects"

**Images:**
- [ ] REUSE: Grid from `radar_synthetic_generation/temp_simu/implementation/ppi_grid_outputs/` (multiple PPI images at different settings)

---

# SECTION 4: OBJECT DETECTION RESEARCH

## SLIDE 15: GazeMamba Architecture
**Text:** "Dual-Stream Mamba for Small Objects"

**Images:**
- [ ] GENERATE: Architecture diagram (peripheral + foveal streams, gaze controller)
- [ ] GENERATE: SS2D 4-way scan visualization

---

## SLIDE 16: GazeMamba Demo Results
**Text:** "Inference on High-Res Images"

**Images:**
- [ ] REUSE: `Object_detection_work/GazeMamba/inference_demo/demo_000_widerface.png`
- [ ] REUSE: `Object_detection_work/GazeMamba/inference_demo/demo_001_visdrone.png`
- [ ] REUSE: `Object_detection_work/GazeMamba/inference_demo/demo_003_dota.png`

---

## SLIDE 17: RADAR3000 Benchmark - Models Compared
**Text:** "6 SOTA Models Evaluated"

**Images:**
- [ ] REUSE: `Object_detection_work/Model_comparison_RADAR3000dataset/outputs/model_comparison_bar.png`

---

## SLIDE 18: YOLOv12 Training Results
**Text:** "92.8% mAP@0.5 Achieved"

**Images:**
- [ ] REUSE: `Object_detection_work/Model_comparison_RADAR3000dataset/outputs/yolov12/train_single_150epochs/results.png`
- [ ] REUSE: `Object_detection_work/Model_comparison_RADAR3000dataset/outputs/yolov12/train_single_150epochs/PR_curve.png`

---

## SLIDE 19: YOLOv12 Confusion Matrix
**Text:** "High Precision & Recall"

**Images:**
- [ ] REUSE: `Object_detection_work/Model_comparison_RADAR3000dataset/outputs/yolov12/train_single_150epochs/confusion_matrix_normalized.png`

---

## SLIDE 20: DDP vs Single GPU Comparison
**Text:** "Distributed Training Analysis"

**Images:**
- [ ] REUSE: `Object_detection_work/Model_comparison_RADAR3000dataset/outputs/final_comparison_ddp_vs_single.png`

---

## SLIDE 21: SO-DETR & RF-DETR Results
**Text:** "DETR-Based Model Performance"

**Images:**
- [ ] REUSE: `Object_detection_work/Model_comparison_RADAR3000dataset/outputs/so_detr/train_ddp/mAP_progress.png`
- [ ] REUSE: `Object_detection_work/Model_comparison_RADAR3000dataset/outputs/rf_detr/metrics_plot.png`

---

## SLIDE 22: Maritime Radar Tracking (AIAA Paper)
**Text:** "AIAA SciTech 2025 Publication"

**Images:**
- [ ] GENERATE: ST-DBSCAN clustering visualization
- [ ] GENERATE: Track stitching before/after comparison
- [ ] GET: Paper title/abstract screenshot

---

## SLIDE 23: Rust Performance Gains
**Text:** "3.7x Speedup with Rust"

**Images:**
- [ ] GENERATE: Bar chart (Python 1166s vs Rust 306s)
- [ ] GENERATE: Code snippet comparison (Python vs Rust)

---

# SECTION 5: THERMAL & CAMERA WORK

## SLIDE 24: FLIR Camera System
**Text:** "M364C Dual-Sensor Control"

**Images:**
- [ ] GET: FLIR M364C camera photo
- [ ] GENERATE: System block diagram

---

## SLIDE 25: Camera Driver Performance
**Text:** "Sub-100ms PTZ Latency"

**Images:**
- [ ] GENERATE: Latency comparison bar chart
- [ ] GENERATE: Architecture diagram (Stream + PTZ + Web)

---

## SLIDE 26: Thermal Denoising Analysis
**Text:** "Multiple Denoising Methods Compared"

**Images:**
- [ ] REUSE: `Thermal_and_camera_Work/thermal-deblur-analysis/grid_comparison.png`
- [ ] REUSE: `Thermal_and_camera_Work/thermal-deblur-analysis/advanced_filters/advanced_filters_comparison.png`

---

## SLIDE 27: Thermal Denoising - Zoomed Analysis
**Text:** "Detail Preservation Comparison"

**Images:**
- [ ] REUSE: `Thermal_and_camera_Work/thermal-deblur-analysis/huge_zoom_comparison.png`
- [ ] REUSE: `Thermal_and_camera_Work/thermal-deblur-analysis/difference_maps.png`

---

## SLIDE 28: LRSID Results
**Text:** "Low-Rank Sparse Image Decomposition"

**Images:**
- [ ] REUSE: `Thermal_and_camera_Work/thermal-deblur-analysis/lrsid_results/lrsid_comparison_grid.png`
- [ ] REUSE: `Thermal_and_camera_Work/thermal-deblur-analysis/lrsid_results/lrsid_zoomed_details.png`

---

## SLIDE 29: Metrics Comparison
**Text:** "Quantitative Quality Assessment"

**Images:**
- [ ] REUSE: `Thermal_and_camera_Work/thermal-deblur-analysis/metrics_comparison.png`
- [ ] REUSE: `Thermal_and_camera_Work/thermal-deblur-analysis/lrsid_results/lrsid_quality_metrics.png`

---

## SLIDE 30: YOLOv8 on Jetson Orin
**Text:** "45.7 FPS Edge Inference"

**Images:**
- [ ] GENERATE: FPS benchmark chart
- [ ] GET: Jetson Orin Nano photo

---

## SLIDE 31: YOLO Ablation Study
**Text:** "Backend & Resolution Analysis"

**Images:**
- [ ] GENERATE: Heatmap (model size × resolution × FPS)
- [ ] GENERATE: Backend comparison bar chart

---

## SLIDE 32: IMU Orthorectification
**Text:** "CUDA-Accelerated Perspective Correction"

**Images:**
- [ ] GENERATE: Before/after orthorectification comparison
- [ ] GENERATE: Pipeline diagram (IMU -> VPI -> Frame)

---

# SUMMARY SLIDES

## SLIDE 33: Key Metrics Dashboard
**Text:** Minimal - let numbers speak

**Images:**
- [ ] GENERATE: Infographic with key stats:
  - 92.8% mAP (object detection)
  - 3.7x speedup (Rust)
  - <100ms latency (camera)
  - 45.7 FPS (edge inference)
  - 1 publication (AIAA)

---

## SLIDE 34: Technology Stack
**Text:** Single header only

**Images:**
- [ ] GENERATE: Tech logo grid (Rust, Python, C++, PyTorch, TensorRT, Slint, etc.)

---

## SLIDE 35: Next Steps / Q1 2026
**Text:** 3-4 bullet points max

**Images:**
- [ ] GENERATE: Roadmap timeline graphic

---

## SLIDE 36: Thank You / Questions
**Text:** Contact info

**Images:**
- [ ] REUSE: USC/IMSEL logo
- [ ] GET: ONR logo

---

# IMAGE INVENTORY

## Ready to Use (REUSE)
| Image | Location |
|-------|----------|
| RadarPlotter GUI (light) | `radar_post_processing/RadarPlotter/figures/01_light_mode_initial.png` |
| RadarPlotter GUI (dark processing) | `radar_post_processing/RadarPlotter/figures/04_processing_dark.png` |
| RadarPlotter complete | `radar_post_processing/RadarPlotter/figures/05_processing_complete_light.png` |
| Example PPI viridis | `radar_post_processing/RadarPlotter/figures/example_viridis_output.png` |
| World view simulation | `Object_detection_work/GazeMamba/radar_sim/world_view.png` |
| World debug | `Object_detection_work/GazeMamba/radar_sim/world_debug.png` |
| PPI output | `Object_detection_work/GazeMamba/radar_sim/ppi_output.png` |
| PPI blobs | `Object_detection_work/GazeMamba/radar_sim/ppi_blobs.png` |
| PPI diagnostic | `Object_detection_work/GazeMamba/radar_sim/ppi_diagnostic.png` |
| GazeMamba demo 0 | `Object_detection_work/GazeMamba/inference_demo/demo_000_widerface.png` |
| GazeMamba demo 1 | `Object_detection_work/GazeMamba/inference_demo/demo_001_visdrone.png` |
| GazeMamba demo 3 | `Object_detection_work/GazeMamba/inference_demo/demo_003_dota.png` |
| Model comparison bar | `Object_detection_work/Model_comparison_RADAR3000dataset/outputs/model_comparison_bar.png` |
| YOLOv12 results | `Object_detection_work/Model_comparison_RADAR3000dataset/outputs/yolov12/train_single_150epochs/results.png` |
| YOLOv12 PR curve | `Object_detection_work/Model_comparison_RADAR3000dataset/outputs/yolov12/train_single_150epochs/PR_curve.png` |
| YOLOv12 confusion matrix | `Object_detection_work/Model_comparison_RADAR3000dataset/outputs/yolov12/train_single_150epochs/confusion_matrix_normalized.png` |
| DDP comparison | `Object_detection_work/Model_comparison_RADAR3000dataset/outputs/final_comparison_ddp_vs_single.png` |
| SO-DETR mAP | `Object_detection_work/Model_comparison_RADAR3000dataset/outputs/so_detr/train_ddp/mAP_progress.png` |
| RF-DETR metrics | `Object_detection_work/Model_comparison_RADAR3000dataset/outputs/rf_detr/metrics_plot.png` |
| Thermal grid comparison | `Thermal_and_camera_Work/thermal-deblur-analysis/grid_comparison.png` |
| Advanced filters | `Thermal_and_camera_Work/thermal-deblur-analysis/advanced_filters/advanced_filters_comparison.png` |
| Huge zoom comparison | `Thermal_and_camera_Work/thermal-deblur-analysis/huge_zoom_comparison.png` |
| Difference maps | `Thermal_and_camera_Work/thermal-deblur-analysis/difference_maps.png` |
| LRSID grid | `Thermal_and_camera_Work/thermal-deblur-analysis/lrsid_results/lrsid_comparison_grid.png` |
| LRSID zoomed | `Thermal_and_camera_Work/thermal-deblur-analysis/lrsid_results/lrsid_zoomed_details.png` |
| Metrics comparison | `Thermal_and_camera_Work/thermal-deblur-analysis/metrics_comparison.png` |
| LRSID quality | `Thermal_and_camera_Work/thermal-deblur-analysis/lrsid_results/lrsid_quality_metrics.png` |
| radar_sim_L3 GUI | `radar_synthetic_generation/radar_sim_L3/docs/images/gui_screenshot.png` |
| Workflow diagram | `radar_synthetic_generation/radar_sim_L3/docs/images/workflow.png` |
| Annotation process | `radar_synthetic_generation/radar_sim_L3/docs/images/annotation_process.png` |
| PPI realistic | `radar_synthetic_generation/temp_simu/implementation/ppi_realistic_cartesian.png` |
| Beam spread | `radar_synthetic_generation/temp_simu/implementation/ppi_beam_spread_polar.png` |
| Pulse elongation | `radar_synthetic_generation/temp_simu/implementation/pulse_elongation_range_profile.png` |

## Need to Generate (GENERATE)
| Image | Description | Tool Suggestion |
|-------|-------------|-----------------|
| Hero collage | 4-panel key outputs | Photoshop/Canva |
| 5-icon infographic | Project area icons | Canva/Figma |
| GazeMamba architecture | Dual-stream diagram | draw.io/TikZ |
| SS2D visualization | 4-way scan arrows | draw.io/TikZ |
| ST-DBSCAN viz | Clustering animation frame | Python/matplotlib |
| Rust speedup chart | Bar chart comparison | Python/matplotlib |
| Latency comparison | Camera latency bars | Python/matplotlib |
| FPS benchmark | Jetson performance | Python/matplotlib |
| Ablation heatmap | Model×Res×FPS | Python/seaborn |
| Ortho before/after | Side-by-side frames | Captured from system |
| Key metrics infographic | Stats dashboard | Canva/Figma |
| Tech logo grid | Technology icons | Canva |
| Roadmap timeline | Q1 2026 plans | Canva/PPT |

## Need to Get (GET)
| Image | Source |
|-------|--------|
| Furuno radar photo | Furuno website / lab photos |
| Raspberry Pi setup | Lab photo |
| FLIR M364C photo | FLIR website / lab photos |
| Jetson Orin photo | NVIDIA website |
| USC/IMSEL logo | University assets |
| ONR logo | ONR website |
| AIAA paper screenshot | Published paper |

---

# EXISTING PRESENTATIONS TO MINE

These presentations from `Reporting/` may contain reusable images:

1. `10_14_25_summary_sept-aug_progress.pptx` - Previous progress summary
2. `10_16_25_existing_radar_architectures.pptx` - Radar architecture diagrams
3. `10_22_25_Integer_pres.pptx` - Integer presentation
4. `10_23_25_plan_for_annotation.pptx` - Annotation workflow
5. `10_30_25_annotation_radar_software.pptx` - Annotation + radar
6. `11-04-25_Cancilla_Hardware.pptx` - Hardware photos (723MB - likely many images)
7. `12-02-25-tri-weekly.pptx` - Recent tri-weekly
8. `01_07_26_one_v_one.pptx` - Most recent presentation

---

# SLIDE COUNT SUMMARY

| Section | Slides |
|---------|--------|
| Title + Overview | 2 |
| Radar Collection | 3 |
| Radar Post-Processing | 4 |
| Radar Simulation | 5 |
| Object Detection | 9 |
| Thermal/Camera | 9 |
| Summary | 4 |
| **TOTAL** | **36** |

---

# NOTES

- Keep text to 1-2 lines per slide max
- Let images tell the story
- Use consistent color scheme (navy/steel blue from LaTeX doc)
- Consider 16:9 widescreen format
- Add slide numbers in footer
- Include backup slides with detailed metrics if needed
