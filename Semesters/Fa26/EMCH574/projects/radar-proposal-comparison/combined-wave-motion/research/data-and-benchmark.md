# Data and benchmark feasibility

Prepared 6 October 2026 by J.C. Vaught. This audit separates what public records can measure from what the combined wave, motion, and radar claim requires. The conclusion is operational. Public records support component pilots and synthetic stress tests. They do not supply paired, time-resolved wave truth, target geometry, and calibrated radar observations for a joint causal benchmark.

## Required observables

The combined validation target requires a time-resolved radar observable, either calibrated complex samples or a documented intensity product; per-ray timestamps; sensor pose and radar-to-platform extrinsics; an independent wave profile along the radar path; target motion and geometry, including target height above the instantaneous surface; and labels for visibility, detection, and outage. A wave summary, a navigation track, or a target-present flag cannot substitute for the missing field. If a claim concerns interruption forecasting, the record must also preserve the outage-forecast horizon and a leakage-safe history window.

## Public-data audit

| Source | Radar observable | Timing and pose | Waves along path | Target geometry and labels | Feasible use |
|---|---|---|---|---|---|
| [CANOE data reference](https://github.com/utiasASRL/pycanoe/blob/main/DATA_REFERENCE.md) | Rotating polar intensity scans are documented. Complex I/Q is not documented. | Inertial, camera, and navigation streams are documented; per-ray timestamp and radar-to-platform extrinsic completeness must be checked in each release. | No synchronized wave-probe or along-path profile is documented. | Platform navigation is available, but target height, target geometry, and target visibility labels are not established as a benchmark truth. | Radar, navigation, and timing-interface pilot. It cannot validate wave shadow physics. |
| [IPIX Dartmouth index](https://soma.ece.mcmaster.ca/ipix/dartmouth/index.html) and [dataset table](https://soma.ece.mcmaster.ca/ipix/dartmouth/datasets.html) | Coherent radar records and target bins are documented. | Acquisition records provide radar and environmental metadata, not synchronized per-ray platform pose and extrinsics. | Sea-state summaries are reported. An instantaneous wave profile along each target ray is absent. | The target is a one-meter mesh-wrapped spherical styrofoam object. Primary and secondary bins and target-to-clutter summaries are documented; full target motion and elevation truth are absent. | Coherent sea-clutter and detector-component pilot. It cannot establish wave-conditioned target visibility. |
| [Sensor datasheet](https://www.navtechradar.com/radar-sensors/) | Sensor operating characteristics can bound range, scan, and intensity assumptions. | Datasheet specifications are not an acquisition-level timestamp or pose record. | None. | None. | Hardware-interface and simulation parameter bounds only. |

CANOE therefore has no known synchronized wave profile in the documented public data. IPIX supplies a wave summary rather than an instantaneous wave field and uses a single one-meter mesh sphere as its target. Public datasets can validate radar conditioning, detector calibration, and motion-handling components separately. They cannot be pooled as if they were paired combined-field truth. Any cross-dataset result must state which observable is missing and avoid treating a marginal wave statistic as a ray-level label.

## Practical public pilot

The pilot should keep each acquisition intact and use whole-acquisition or contiguous time-block splits. First, reproduce a common detector and calibrate a fixed false-alarm operating point on development records. Second, run a factorial synthetic benchmark with held-out returns in four conditions. The conditions are no motion and no wave modulation, motion only, wave modulation only, and coupled motion plus wave modulation. Generate truth separately from the predictors. Compare a history-only predictor, a pose-and-geometry predictor, and a continuous-transmission predictor at a fixed detector threshold. Report Brier score, reliability, recall at the fixed false-alarm rate, and outage lead-time error with confidence intervals clustered by realization.

The synthetic generator must retain per-ray time, pose, extrinsics, independent wave elevation and slope along the path, target position and height, propagation state, detector decision, and missingness. Local error must be conditional on detections and reported separately from outage forecasting. The holdout must be by entire realization and by contiguous acquisition blocks so adjacent windows do not leak. Forecast horizons must be fixed before evaluation.

This design prevents circular validation in which an oracle pose creates the test truth used to reward a pose predictor. It also exposes interactions that marginal averages hide. The benchmark must not claim measured wave-shadow validity from a completed synthetic run.

## Low-cost acquisition contract

If the pilot reaches its go/no-go criteria, procure one short field campaign with a coherent radar stream, hardware or shared-clock timestamps, surveyed radar-to-platform extrinsics, an independent wave gauge or stereo surface reconstruction covering the target ray, RTK/INS target and platform tracks, a calibrated target-height or range reference, and human-reviewed visibility and outage labels. Record receiver settings, polarization, sea state, weather, and all dropped packets. Treat an optional boat-mounted design as a decision about observability, clocking, and survey access. It is not a control-project requirement.

## Milestones and go/no-go

By 16 October, freeze the observable schema, source licenses, split policy, and synthetic factorial. By 30 October, complete public-record ingestion checks and detector calibration. By 13 November, complete the four-condition benchmark with realization-level intervals. By 20 November, decide whether the missing wave and geometry channels require the low-cost acquisition. By 2 December, go if the coupled benchmark improves held-out Brier score over the history reference across multiple wave regimes while preserving common-detector calibration and the fixed false-alarm point. Stop or narrow the claim if improvement occurs only in one regime, depends on oracle state, or vanishes under timestamp, pose, or missingness perturbations.
