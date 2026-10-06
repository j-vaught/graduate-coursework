# Predicting Small-Target Radar Reliability Under Wave-Driven Vessel Motion

J.C. Vaught. Prepared 6 October 2026 for EMCH574.

[The proposal](proposal.pdf) contains a two-page sponsor pitch followed by five technical appendices and a dedicated references section. The appendices cover shared mechanical forcing, ray-time observation geometry, published-model calculations and measured return variability, benchmark rationale and parameter design, and full related work. [The editable source](proposal.tex) preserves the main proposal as exactly two pages. The evaluation dataset and milestones remain undecided.

The project predicts a usable target observation at the next scan. Waves drive the radar vessel and target, while vessel attitude changes beam coverage, wave-path clearance, and the geometry used for mapping. The benchmark distinguishes detector misses from conditional position error and separates physical truth conditions from predictor feature comparisons.

**Reproduction.**

Run the build with Node.js, Typst, uv, latexmk, a LaTeX installation, and Poppler available.

```sh
./build.sh
```

The build executes `src/illustrative-model.mjs`, synchronizes the pinned Python environment, and executes `src/published_evidence.py`. It compiles two schematics and ten standalone plot PDFs, then the proposal. The current document includes the shared-wave mechanism schematic, the simulated wave-obstruction diagram, two published-model plots, and two measured-radar plots. Six additional coupled-model plots remain companion assets for later analysis. CeTZ is pinned to version 0.5.2 and Lilaq to version 0.6.0. Schematics use black and white. Every quantitative plot uses Lilaq’s default color cycle and built-in legend, positioned above the data area. No legend is drawn by hand. All diagram and plot frames are square. Text and mathematics use Latin Modern throughout the figures and the standard LaTeX article. Sections, appendices, equations, figures, and tables use automatic numbering. Numeric bracket citations resolve through the centralized bibliography.

The retained illustrative companion inputs are in `data/config.json`. Coupled illustrations are in `data/illustrative.json`, with assertions in `data/checks.json`. Their default target-power availability fraction is 0.122. That quantity describes a deterministic model, rather than measured detector or forecast performance.

**Published models and measured data.**

`data/published-model.json` contains the Wijaya and van Groesen harmonic surface-visibility reproduction. It evaluates their geometric indicator and phase average with the Figure 3.4 period, depth, height ratios, and phase count. Joint sampling refinement changes visibility by no more than 0.001072. It also contains the constant-translation limit of Lund et al.'s ray-time mapping, using their 1.25 s rotation and 11 kn example. The resulting 3.537 m maximum midpoint error is calculated, not a reported field error.

`data/measured-ipix.json` contains actual record-17 HH powers, source hash, unsigned-byte interpretation, common clutter-trained I/Q correction, split, and gate. The first 32,768 sweeps train the correction and 99th-percentile power gate. Nonoverlapping 64-sweep windows retain the final 98,304 sweeps for display and evaluation. Clutter bins 1-7 and 12-14 exclude all documented target bins. Held-out clutter exceeds the gate in 0.990% of windows, while primary bin 9 falls below it in 66.602%. These are fixed-gate statistics, without instantaneous target-visibility or wave-phase labels.

The build downloads only the 15.7 MB official IPIX record when absent, verifies its SHA-256, and caches it under ignored `data/raw/`. Raw data and source-paper PDFs are not redistributed. `data/sources.json` records exact URLs, source hashes, and source equations. The dataset requires attribution in publications and that researchers keep its maintainers informed of results. The record's PRF metadata conflicts with the generic tutorial convention, so the measured plots and runs use sweep index rather than an asserted seconds conversion.

Numerical processing uses Python without a plotting library. Every figure is authored in Typst using CeTZ for diagrams and Lilaq for plots. Development checks are

```sh
uv sync --frozen
uv run ruff format .
uv run ruff check . --fix
uv run ty check .
uv run python src/published_evidence.py --download
```

**MATLAB companion.**

The MATLAB counterpart is `src/illustrative_model.m`. Run it from this directory after adding its source folder.

```matlab
addpath('src');
result = illustrative_model();
```

It writes to `tmp/matlab/illustrative_results.json` and retains the executed figure data. Its source mirrors the state, path, beam, power, geometry, and sweep computations. A MATLAB runtime was not available during preparation, so numerical parity has not been executed. The proposed spatial detector, probability fitting, full synthetic benchmark, additional acquired-file evaluation, and field experiment remain semester work.

**Source evidence.**

`references.bib` is the centralized bibliography. Records under `research/` document literature, data observables, paper models, and technical review. `evidence.md` records final scope and verification. The IPIX example documents measured return variability rather than selecting an evaluation dataset. The full coupling needs independently synchronized wave, vessel, target, and radar measurements. The expanded benchmark distinguishes physical interventions from predictor inputs, uses grouped independent realizations, and justifies proposed numerical settings through calculations and primary sources.

The complete project compiles through `latexmk`. The single-file editor preview cannot resolve the external figure PDFs and bibliography; use the saved PDF or the full project build for the complete document.

## Separate observation-mechanism previews

Three reviewed alternatives to the combined observation schematic are available as `wave-obstruction`, `beam-misalignment`, and `scan-time-error` in `figures/generated`, each with PDF and PNG exports. Each has its own Typst source in `figures/src`. The beam diagram shows half-power directions rather than hard beam boundaries, and the timing diagram isolates the constant-heading translation error in plan view. Geometry checks are recorded in `research/observation-diagram-review.md`. The proposal now uses the simulated `wave-surface` figure for obstruction; the beam and scan-time diagrams remain separate candidates.

## Mathematical wave-surface preview

`figures/generated/wave-surface.pdf` and its PNG show a reproducible irregular Airy-wave realization using the ISSC/Bretschneider spectrum. Run `uv run python src/wave_surface.py` to regenerate the numeric field, then compile `figures/src/wave-surface.typ` with Typst. Parameters and equation provenance are in `research/wave-surface-model.md`. The preview now includes a stable radar, a schematic horizontal beam, and a surface-connected object whose direct path is blocked at a calculated wave intersection.
