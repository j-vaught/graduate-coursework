# Mode 2 (Analytical Generator) — Experiments & Figures

## Clutter Validation

### Experiment 28: Amplitude PDF Comparison
For each collection site, plot the empirical amplitude PDF from real clutter-only frames against the fitted K-distribution. Overlay Mode 2 synthetic clutter PDF. Three curves on one plot. Use log scale on y-axis to show tail behavior.

### Experiment 29: K-Distribution Parameter Estimation
Fit shape parameter nu and scale parameter Pc to real data from each site (Lake Murray, Lake Greenwood, Charleston). Report values in a table. These are novel measurements — nobody has published K-distribution parameters for SC inland lake radar clutter.

### Experiment 30: QQ-Plot
Quantile-quantile plot of real clutter amplitudes vs. K-distribution theoretical quantiles. Visual check of distribution fit — good figure even if the numbers are messy.

### Experiment 31: CDF Comparison
Empirical CDF of real vs. synthetic clutter. Less noisy than PDF plots, sometimes looks cleaner. Use this as backup if the PDF is noisy.

### Experiment 32: Temporal Autocorrelation
Compute scan-to-scan autocorrelation of clutter intensity at fixed range-azimuth cells. Compare real vs. Mode 2. Shows whether synthetic clutter decorrelates realistically.

### Experiment 33: Power Spectral Density
PSD of clutter intensity along range for real vs. synthetic. Shows whether spatial texture matches.

### Experiment 34: Clutter Map Comparison
Generate a full synthetic B-scan from Mode 2 side-by-side with a real B-scan. Visual comparison of overall texture and structure.

### Experiment 35: Range-Dependence of Clutter Power
Plot mean clutter intensity vs. range for real data and Mode 2. Should follow R^(-n) with n depending on geometry and propagation.

### Experiment 36: Shore Clutter vs. Open Water
Separate the statistics for range-azimuth cells that correspond to shoreline returns vs. open water. Shows the heterogeneity of the inland environment. Fit K-distribution parameters separately for each zone.

---

## Figures to Generate

| # | Figure | Notes |
|---|--------|-------|
| F13 | **Amplitude PDF: real vs. K-distribution fit vs. Mode 2.** | One per site if they look different. Use log scale on y-axis for the tails. Generate for all 3 sites, use the best 1–2. |
| F14 | **CDF comparison: real vs. Mode 2.** | Backup if the PDF looks noisy. Cleaner visual. |
| F15 | **QQ-plot: real vs. K-distribution.** | Classic statistical validation figure. Generate for each site. |
| F16 | **Synthetic B-scan from Mode 2 vs. real B-scan.** Side by side. | Visual comparison of texture. Generate several, pick the closest match. |
| F17 | **Clutter power vs. range** — real and synthetic. | Shows range-dependence match. Simple line plot. |
| F18 | **Temporal autocorrelation** — real vs. synthetic. | Shows temporal decorrelation match. Line plot with lag on x-axis. |
