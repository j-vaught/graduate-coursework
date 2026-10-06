# Benchmark source notes

These primary or authoritative sources support the proposed benchmark rationale. They support the centralized bibliography and do not select a dataset or impose numerical ranges.

The Brier score was introduced as a probabilistic forecast scoring rule in G. W. Brier, “Verification of forecasts expressed in terms of probability,” *Monthly Weather Review*, 1950. Exact URL. https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2. Integrated key. `Brier1950Verification`.

The proper-scoring-rule and calibration interpretation is developed in Tilmann Gneiting and Adrian E. Raftery, “Strictly Proper Scoring Rules, Prediction, and Estimation,” *Journal of the American Statistical Association*, 2007. Exact URL. https://doi.org/10.1198/016214506000001437. Integrated key. `Gneiting2007ProperScoring`.

Common random numbers are a standard variance-reduction method for paired simulation comparisons. Paul Glasserman and David D. Yao, “Some Guidelines and Guarantees for Common Random Numbers,” *Management Science* 38(6), 884–908, 1992, supports the conditional variance-reduction argument. Exact URL. https://doi.org/10.1287/mnsc.38.6.884. Integrated key. `Glasserman1992CommonRandomNumbers`.

Grouped validation is required when observations share spatial, temporal, or environmental structure. Roberts et al., “Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure,” *Ecography*, 2017, gives the leakage mechanism and grouped alternatives. Exact URL. https://doi.org/10.1111/ecog.02881. Integrated key. `Roberts2017CrossValidation`.

Bootstrap inference should resample the independent sampling unit when observations are clustered. Bradley Efron provides the foundational resampling principle in “Bootstrap Methods. Another Look at the Jackknife,” *The Annals of Statistics* 7(1), 1–26, 1979. Exact URL. https://doi.org/10.1214/aos/1176344552. Integrated key. `Efron1979Bootstrap`. Resampling independent complete realizations is the proposed application here; it is not attributed as a marine-radar method from that paper.

Cell-averaging CFAR supplies the shared detector family and reference-cell thresholding logic. H. Rohling, “Radar CFAR Thresholding in Clutter and Multiple Target Situations,” *IEEE Transactions on Aerospace and Electronic Systems*, 1983. Exact URL. https://doi.org/10.1109/TAES.1983.309350. Integrated key. `Rohling1983RadarCFAR`.

The centralized `references.bib` file records these sources. No claim here depends on a selected dataset, a numerical operating range, or the nonadditive contrast as a formal interaction test.
