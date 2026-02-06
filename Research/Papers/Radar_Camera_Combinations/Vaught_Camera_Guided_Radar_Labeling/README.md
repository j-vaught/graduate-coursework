# Camera-Guided Radar Labeling via Active PTZ Perception for Maritime Dataset Construction

## Overview
This project develops an active perception pipeline that uses a PTZ (pan-tilt-zoom) camera to classify maritime radar targets, producing a large-scale labeled radar blob dataset. When the radar detects a target, the PTZ camera slews to observe it, runs YOLO and DETR object detectors on the visual imagery, and propagates the classification label back to the corresponding radar blob. This "look-then-label" approach enables automated construction of labeled radar datasets, which can subsequently train radar-only classifiers that operate without camera input.

## Team

| Role | Name |
|------|------|
| Lead | J.C. Vaught |
| Undergraduate Researcher | Sam Cancilla |
| Undergraduate Researcher | Mateo Altomare |
| Co-Investigator | Douglas Cahl |
| Principal Investigator | Dr. Yi Wang |

## Hardware

| Component | Specification |
|-----------|--------------|
| Radar | Furuno DRS4D-NXT X-band pulse compression |
| Camera | FLIR M364C PTZ (360deg pan, tilt, 30x zoom, thermal + RGB) |
| Compute | NVIDIA Jetson Orin |
| Navigation | None (PTZ provides full 360deg coverage) |

## System Architecture

The pipeline consists of five stages:

1. **Radar Blob Detection** -- Extract and characterize radar blobs from Furuno DRS4D-NXT returns, identifying candidate maritime targets by their spatial and temporal signatures.
2. **PTZ Tasking Strategy** -- Prioritize and schedule PTZ camera slews to observe detected radar blobs, balancing coverage, revisit rate, and slew time constraints across multiple simultaneous targets.
3. **Dual-Stream Visual Detection** -- Run YOLO (real-time) and DETR (transformer-based) detectors on the PTZ camera imagery (RGB and thermal channels) to classify the observed target.
4. **Label Assignment** -- Propagate the visual classification label back to the corresponding radar blob using angular alignment between the PTZ heading and the radar bearing.
5. **Dataset Construction** -- Aggregate labeled radar blobs with associated features (intensity, extent, Doppler, temporal persistence) into a structured dataset for downstream radar-only classifier training.

## Goals

- Construct a large-scale labeled maritime radar blob dataset without manual annotation
- Demonstrate the "data flywheel" concept: auto-labeled data trains radar-only classifiers, which improve target prioritization, which improves label quality
- Validate that radar-only classifiers trained on PTZ-generated labels achieve competitive performance against models trained on hand-labeled data
- Release the dataset and active labeling pipeline for community use

## Expected Outputs

- Labeled maritime radar blob dataset (class labels with confidence scores)
- PTZ active perception and labeling pipeline (open-source)
- Conference/journal paper documenting the active perception methodology and radar classification results

## Current Status

**Actively collecting data.** Hardware is deployed and synchronized radar-camera data streams are being recorded. PTZ tasking logic and detector integration are under active development.

## Repository Structure

```
Vaught_Camera_Guided_Radar_Labeling/
├── README.md
├── PROPOSAL.md
├── LITERATURE_REVIEW_OUTLINE.md
├── references.bib
├── figures/
└── .gitignore
```
