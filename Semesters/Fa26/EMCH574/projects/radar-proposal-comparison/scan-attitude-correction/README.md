# Limits of Whole-Scan Attitude Correction in High-Resolution Marine Radar

J.C. Vaught. EMCH 574. October 2, 2026.

`proposal.pdf` contains a standalone one-page sponsor proposal followed by four technical appendix pages. `proposal.typ` is the editable document. The appendix contains a mechanical model, an original acquisition schematic, two computed plots, benchmark and schedule tables, prior-work comparison, and references.

## Reproduction

Run the following command in this directory. It requires Node.js, Typst, and the pinned CeTZ 0.5.2 and Lilaq 0.6.0 packages. Typst retrieves the pinned packages if they are not already cached. Poppler is optional for page-image and text verification.

```sh
./build.sh
```

The command writes `data/analytical.json` and `data/checks.json`, compiles the three standalone figure PDFs under `figures/generated/`, then compiles the proposal. All figures are authored in Typst. Square frames, high-contrast course colors, and filled stealth arrows follow the course instructions. No external numerical dependencies or data downloads are needed for this build.

`src/analytical_scan_model.m` supplies a matching MATLAB analytical model for course development. Execute `analytical_scan_model` from MATLAB after adding `src/` to its path. It writes `data/analytical-matlab.json`. The present numerical check and PDF build used `src/analytical-data.mjs`; the MATLAB source has not been executed in this environment. Later MATLAB output can replace the imported analytical data after agreement is checked.

## Status and interpretation

The numerical examples are analytical simulations. They are not measured CANOE performance. `data/config.json` holds the assumed oscillator parameters, scan timing, lever arm, target ranges, range bins, and illustrative elevation beam widths. `data/checks.json` records selected computed values and the inverse-geometry consistency check.

Each maximum error is the maximum over one configured 400-ray scan at a specified forcing phase, not over all phases. The pitch forcing is `sin(2*pi*f*t)` and the scan midpoint is `t=0`; the steady response includes the forced-oscillator phase lag. Roll forcing leads by 60 degrees. A phase sweep is part of the proposed course benchmark.

The geometry solves a measured slant-range sphere and azimuth half-plane against a known flat target plane. This imposed target-plane constraint supplies elevation. In actual 2D radar data, elevation is not measured. The plotted coordinate-error envelope is evaluated without a beam mask. The separately reported beam-gate fraction is idealized geometric availability, not detection probability or experimental persistence. The true antenna pattern in the selected CANOE unit remains unverified.

The raw radar payload is a planned selective download. Public metadata establishes ray-time feasibility. A held-out repeated traversal can measure relative landmark consistency; independently surveyed targets would be needed to establish absolute accuracy. Post-processed navigation-assisted corrections are an oracle/reference-assisted branch, not an operational raw-inertial system or an independent validation source.

The project contribution is an engineering adequacy test. Prior art already covers motion compensation, vertical-motion effects, and attitude-informed echo correction. The course endpoint does not claim a new six-degree-of-freedom correction method or validated X-band sea-state inversion.
