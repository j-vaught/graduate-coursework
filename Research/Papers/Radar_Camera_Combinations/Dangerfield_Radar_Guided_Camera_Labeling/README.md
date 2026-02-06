# Radar-Guided Camera Labeling for Automated Maritime Dataset Construction

## Overview
This project develops an automated pipeline that uses X-band marine radar detections to generate labeled bounding boxes on co-located camera imagery. By projecting radar targets into camera pixel coordinates, the system eliminates manual annotation labor and enables continuous, large-scale maritime dataset construction from a stationary coastal observation platform.

## Team

| Role | Name |
|------|------|
| Lead | Ty Dangerfield |
| Co-Investigator | J.C. Vaught |
| Co-Investigator | Douglas Cahl |
| Principal Investigator | Dr. Yi Wang |

## Hardware

| Component | Specification |
|-----------|--------------|
| Radar | Simrad Halo 20+ X-band pulse compression |
| Camera | Lucid Allied Vision, stationary, ~100deg FOV |
| Compute | NVIDIA Jetson Orin |
| Navigation | GPS + IMU |

## System Architecture

The pipeline consists of four stages:

1. **Sensor Calibration** -- Establish the geometric relationship between radar and camera coordinate frames using GPS/IMU-derived pose and intrinsic/extrinsic camera parameters.
2. **Radar Detection** -- Extract target detections (range, bearing) from the Simrad Halo 20+ radar returns.
3. **Polar-to-Pixel Projection** -- Transform radar detections from polar coordinates (range, bearing) through geo-referenced world coordinates into camera pixel coordinates, generating bounding box proposals.
4. **Label Quality Assurance** -- Filter and validate projected bounding boxes using size priors, temporal consistency, and optional detector cross-checks.

## Goals

- Construct a large-scale labeled maritime camera dataset without manual annotation
- Validate label quality against hand-annotated ground truth subsets
- Demonstrate that models trained on radar-generated labels approach performance of models trained on manually labeled data
- Release the dataset and labeling pipeline for community use

## Expected Outputs

- Labeled maritime camera image dataset (bounding boxes with class labels)
- Calibration and projection pipeline (open-source)
- Conference/journal paper documenting methodology and results

## Current Status

**Actively collecting data.** Hardware is deployed and radar-camera data streams are being recorded. Calibration and projection pipeline development is underway.

## Repository Structure

```
Dangerfield_Radar_Guided_Camera_Labeling/
├── README.md
├── PROPOSAL.md
├── LITERATURE_REVIEW_OUTLINE.md
├── references.bib
├── figures/
└── .gitignore
```
