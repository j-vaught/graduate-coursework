# Marine radar project comparison

The selected combined direction is [Predicting Small-Target Radar Reliability Under Wave-Driven Vessel Motion](combined-wave-motion/proposal.pdf). It develops the two mechanisms below into a two-page main proposal with technical appendices, a common-state benchmark, computed figures, and a staged validation plan. Its [source and reproduction notes](combined-wave-motion/README.md) accompany the document.

Prepared for EMCH574 by J.C. Vaught. Each proposal contains a standalone one-page sponsor pitch followed by a technical appendix. The appendices compare prior work, explain the mechanics, state the benchmark design, and distinguish analytical illustrations from future experimental validation.

| Decision factor | Wave-conditioned detection interruptions | Whole-scan attitude correction |
| --- | --- | --- |
| Practical decision | When should a missed small-target observation be expected from physical wave conditions? | When is one vessel attitude per radar scan inadequate for localization and beam coverage? |
| Course connection | Forced heave, phase relationships, wave geometry, and diffraction. | Forced roll and pitch, damping, scan sampling, and motion-dependent radar geometry. |
| Proposed contribution | Test the added predictive value of independently measured wave and target state beyond clutter intensity. | Establish resolution-dependent operating limits and separate correctable geometric error from lost illumination. |
| Semester deliverable | A reproducible coupled model, detector comparisons, and a field-validation protocol. | A reproducible scan simulator, correction comparisons, and a bounded public-data pilot. |
| Main validation dependency | Synchronized local wave profiles and known target geometry are needed for the central field claim. | Per-azimuth timestamps and sensor calibration support a pilot, while unknown target elevation limits reconstruction. |
| Public-data role | IPIX supports target/clutter detection experiments but does not provide synchronized local wave geometry. | CANOE supports timestamped radar-motion experiments but does not establish ocean-wave forcing or a surveyed target benchmark. |
| Strongest reason to select it | A direct physical explanation of detection outages with a path to a dedicated experiment. | A clearer path to a useful result within the semester and a concrete correction-versus-hardware decision. |

The scan-attitude project is the stronger choice for a bounded semester study. Its central operating-limit question can be investigated in a controlled simulator and then checked with a selective public-data pilot. The wave-conditioned project is the stronger choice if a sponsor can support synchronized radar, wave, and target measurements. That experiment is essential to distinguish physical prediction from correlation with sea conditions.

**Documents.**

[Wave-conditioned detection proposal](wave-conditioned-detection/proposal.pdf) and [editable source](wave-conditioned-detection/proposal.typ).

[Scan-attitude correction proposal](scan-attitude-correction/proposal.pdf) and [editable source](scan-attitude-correction/proposal.typ).

Each project directory contains its own source evidence and centralized bibliography. Computed appendix figures are illustrative model outputs. The documents do not assert an established publication gap or measured performance improvement.

**Reproduction.**

Run `./build.sh` inside either project directory with Node.js and Typst available. The scripts regenerate the analytical data, standalone figure PDFs, and proposal PDF. Figure sources use pinned Typst packages. MATLAB equivalents are included under `src/`; they were reviewed but were not executed during proposal preparation. The repository's existing `.gitignore` excludes environments, caches, and temporary build files while retaining the deliverable PDFs and figure sources.
