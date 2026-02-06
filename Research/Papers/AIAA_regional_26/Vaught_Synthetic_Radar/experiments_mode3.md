# Mode 3 (EM Ray Tracing) — Experiments & Figures

## Physics Validation

### Experiment 37: Two-Ray Model Comparison
Plot the propagation factor F^4 vs. range from the ray tracer against the analytical two-ray (Lloyd's mirror) formula. For a point target over flat water at 3 m antenna height, 9.4 GHz. Classic validation plot. At these parameters the first null is at ~125 m.

### Experiment 38: Range Profile for a Canonical Target
Single point target (e.g., 1 m² RCS) at 500 m range. Plot the received power vs. range bin from the ray tracer against the radar equation prediction. Should agree within a few dB.

### Experiment 39: Multipath Lobe Structure
Plot received target power vs. range (100–1000 m) for the ray tracer and the two-ray model. Show the constructive/destructive interference lobes. At 3 m height and 9.4 GHz this produces a distinctive oscillating pattern.

### Experiment 40: Ray Tracer vs. Mode 2
For the same simple scene (single target, flat water, no shore clutter), compare the range profile from Mode 3 against the analytical Mode 2 output. Shows consistency between modes.

### Experiment 41: Water Surface Roughness Sensitivity
Run the ray tracer with flat water, light chop, and moderate chop. Show how the multipath lobes blur/diminish with increasing roughness. Qualitative but informative — demonstrates the physics engine responds correctly to surface conditions.

---

## Figures to Generate

| # | Figure | Notes |
|---|--------|-------|
| F19 | **Two-ray model validation** — propagation factor vs. range. Ray tracer vs. analytical. | The classic multipath validation plot. Clean, simple, and immediately credible. |
| F20 | **Range profile comparison** — point target at known range, ray tracer vs. radar equation. | Single peak, should align. Generate at multiple ranges (200, 500, 800 m), use the cleanest. |
| F21 | **Ray-traced scene illustration** — 3D rendering showing rays, water surface, target, multipath paths. | Conceptual diagram. Can be TikZ or a rendered visualization from the engine. Doesn't need to be from actual sim output — just needs to convey the geometry. |
| F22 | **Surface roughness sensitivity** — received power vs. range for flat, light chop, moderate chop. 3 curves on one plot. | Shows the engine responds to surface conditions. Good qualitative result even if absolute numbers are off. |

---

# Cross-Mode Experiments & Figures

## Cross-Mode Comparisons

### Experiment 42: Side-by-Side B-Scans
Same target scenario rendered in all three modes plus a real frame. Four-panel figure. The visual comparison tells the story at a glance. Generate for 2–3 scenarios (single boat close range, single boat far range, buoy).

### Experiment 43: Amplitude Histogram — All Modes vs. Real
Overlay the amplitude PDF from Mode 1, Mode 2, Mode 3, and real data for equivalent scenes. Shows which mode is closest to reality.

### Experiment 44: CFAR Detection on All Modes
Run a simple CA-CFAR detector on frames from each mode. Report Pd and Pfa. Not critical since you're using YOLO, but shows the framework is useful beyond deep learning. Skip this if time is short.

### Experiment 45: Computation Time Per Frame
Wall-clock time to generate one synthetic frame in each mode. Table or bar chart. Justifies why you need multiple modes. Should span orders of magnitude (Mode 2: sub-second, Mode 1: seconds, Mode 3: minutes to hours).

## Cross-Mode Figures

| # | Figure | Notes |
|---|--------|-------|
| F23 | **Four-panel comparison** — same scenario in Mode 1, Mode 2, Mode 3, and real. | The money shot. Generate for 2–3 scenarios, pick the best. |
| F24 | **Amplitude histogram: all modes vs. real.** 4 curves overlaid. | Direct statistical comparison across modes. |
| F25 | **Computation time bar chart.** One bar per mode. | Log scale on y-axis since times span orders of magnitude. |
