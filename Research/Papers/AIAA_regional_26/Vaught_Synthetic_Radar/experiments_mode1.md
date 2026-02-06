# Mode 1 (Data-Driven Compositor) — Experiments & Figures

## Compositor Validation

### Experiment 1: KS Test on Composited Regions
For 50+ composited frames, extract the amplitude histogram of the insertion region and the surrounding clutter-only region. Run a two-sample Kolmogorov-Smirnov test. Report the test statistic and p-value. If p > 0.05 consistently, your compositor is statistically indistinguishable from real clutter.

### Experiment 2: Earth Mover's Distance (EMD) / Wasserstein Distance
Same setup as KS test but using EMD between the composited region and surrounding clutter. This is a continuous metric — better for plotting trends (e.g., EMD vs. range, EMD vs. SCR).

### Experiment 3: Jensen-Shannon Divergence
Compute JSD between amplitude distributions of composited and real regions. A third statistical measure — if one test gives bad results, another might look better.

### Experiment 4: Mean Intensity Difference
Average intensity in the composited background region minus average intensity in a matched clutter-only region from the same frame. Should be near zero. Plot as a histogram across many frames.

### Experiment 5: Spatial Autocorrelation Comparison
Compute the 2D autocorrelation function of a composited clutter patch vs. a real clutter patch. If Mode 1 preserves texture, these should match. Good visual figure even if the numbers aren't perfect.

### Experiment 6: Compositor Artifacts at Insertion Boundaries
For each composited frame, compute the gradient magnitude at the target insertion boundary vs. the average gradient magnitude elsewhere. If the boundary is visible (sharp edge artifact), this number will be high.

### Experiment 7: SCR Sweep
Composite the same target at SCR = 0, 3, 6, 9, 12, 15, 20 dB. Visually inspect — at what SCR does the target become visible? At what SCR does it look unrealistic?

---

## YOLO Domain Transfer

### Experiment 8: Baseline — Train on Mode 1, Test on Clean Real
Report precision, recall, mAP@0.5, mAP@0.5:0.95, F1. **This is the headline number.**

### Experiment 9: Baseline Breakdown by Target Class
If you have boats and buoys as separate classes, report per-class AP. If one class is much worse, that's useful information.

### Experiment 10: Baseline Breakdown by Range
Bin detections into near (<0.25 NM), mid (0.25–0.5 NM), far (>0.5 NM). Report mAP per bin. Performance should degrade with range — showing this is honest and expected.

### Experiment 11: Baseline Breakdown by Location
Report mAP separately for Lake Murray, Lake Greenwood, Charleston. Shows cross-site generalization (or lack thereof).

### Experiment 12: Confidence Score Distribution
Plot histogram of YOLO confidence scores for true positives vs. false positives. If these distributions are well-separated, your model is confident and calibrated.

### Experiment 13: Precision-Recall Curve
Plot the full PR curve, not just the single mAP number. Shows behavior across operating points.

### Experiment 14: Confusion Matrix
Target class vs. predicted class including background/miss. Useful if you have multiple classes.

### Experiment 15: Training Data Volume Ablation
Train on 25%, 50%, 75%, 100% of Mode 1 data. Plot mAP vs. training set size. Shows if you have enough data or if performance is still climbing. If the curve is still rising, that argues for generating more synthetic data.

### Experiment 16: Real Data Fine-Tuning Comparison
Take the Mode-1-only model and fine-tune on a small amount of real labeled data (50, 100, 200 real frames). Plot mAP vs. number of real fine-tuning frames. Shows: (a) how much real data closes the remaining gap, and (b) whether Mode 1 pretraining gives a better starting point than training from scratch on limited real data.

### Experiment 17: Train on Real Only (Control / Upper Bound)
If you have enough labeled real data, train YOLO on real data only (same number of frames as your synthetic set) as an upper-bound comparison. Mode 1 results should approach this.

### Experiment 18: Train on Real Only (Small / Scarcity Scenario)
Train on just 50–200 labeled real frames (realistic scenario for someone who can't collect much). Compare against Mode 1 synthetic training. This shows Mode 1's value when real data is scarce.

---

## Augmentation / Robustness

### Experiment 19: Clean-Trained on Rain Test Set
Train on clean Mode 1, test on rain frames. Establishes degradation baseline.

### Experiment 20: Clean-Trained on Interference Test Set
Train on clean Mode 1, test on interference frames. Establishes degradation baseline.

### Experiment 21: Rain-Augmented on Rain Test Set
Add rain-augmented frames to training, test on rain. Shows recovery.

### Experiment 22: Interference-Augmented on Interference Test Set
Add interference-augmented frames to training, test on interference. Shows recovery.

### Experiment 23: Both-Augmented on Rain Test Set
Train with both rain and interference augmentation, test on rain. Shows whether mixed augmentation helps or hurts compared to targeted augmentation.

### Experiment 24: Both-Augmented on Interference Test Set
Same, test on interference.

### Experiment 25: Both-Augmented on Clean Test Set
Does augmenting with degraded conditions hurt clean-condition performance? It shouldn't, but check.

### Experiment 26: Augmentation Intensity Sweep
For rain augmentation, vary the blending intensity (25%, 50%, 75%, 100% of real rain texture intensity). Report mAP at each level. Shows sensitivity to augmentation strength.

### Experiment 27: Augmentation Ratio Sweep
Vary the fraction of augmented frames in the training set (10%, 25%, 50% augmented). Report mAP. Shows how much augmented data you need.

---

## Figures to Generate

| # | Figure | Notes |
|---|--------|-------|
| F1 | **Before/after composite (B-scan)** — real B-scan, composite B-scan, difference image. 3-panel. | Generate 4–6 at different ranges, target sizes, conditions. Use the best 2. |
| F2 | **Before/after composite (PPI)** — same as F1 but scan-converted to PPI view. | More intuitive for readers unfamiliar with B-scan format. |
| F3 | **Amplitude histogram overlay** — composited region vs. surrounding clutter. | Pick one with a great match and one with a visible mismatch (for honest discussion). |
| F4 | **SCR sweep gallery** — same frame with target at 0, 5, 10, 15, 20 dB SCR. 5-panel strip. | Shows a target appearing from noise. Very visual. |
| F5 | **Rain augmentation example** — clean frame, rain texture, augmented frame. 3-panel. | Shows the augmentation process. |
| F6 | **Interference augmentation example** — clean frame, interference pattern, augmented frame. 3-panel. | Same as F5 for interference. |
| F7 | **YOLO detection on real data** — 4–6 real B-scan or PPI frames with bounding boxes. | Cherry-pick: 2 easy detections, 2 hard detections, 1 miss (honesty), 1 cluttered scene. |
| F8 | **YOLO detection on rain data** — before and after augmented training. Side by side. | Missed with clean training, detected with augmented training. |
| F9 | **YOLO detection on interference data** — same side-by-side idea. | Same comparison for interference. |
| F10 | **Precision-recall curve** for the baseline experiment. | Standard ML figure. |
| F11 | **Training volume ablation curve** — mAP vs. training set size (25/50/75/100%). | Shows data efficiency. |
| F12 | **Confidence histogram** — TP vs. FP confidence score distributions. | Shows model calibration. |
