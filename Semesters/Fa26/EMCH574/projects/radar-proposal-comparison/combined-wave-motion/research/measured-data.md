# Measured IPIX acquisition for the proposal figure

Prepared 6 October 2026 by J.C. Vaught. Use one official target record for a small, reproducible measured-data figure. The selected file is target acquisition #17, `19931107_135603_starea.cdf`, available directly at [the IPIX file URL](https://soma.ece.mcmaster.ca/ipix/dartmouth/data/19931107_135603_starea.cdf). The official table identifies primary range bin 9 and secondary bins 8:11. The table states that the object is a one-meter-diameter styrofoam sphere wrapped in wire mesh and that target-to-clutter ratios across the listed records range from 0 to 6 dB. The file is approximately 16 MB. Download only this file.

## What the record contains

The official [parameter record](https://soma.ece.mcmaster.ca/ipix/dartmouth/cdf001_050/19931107_135603_starea.txt) reports 9.39 GHz radio frequency, 200 ns pulse length, 1000 Hz pulse repetition frequency, 14 range bins beginning at 2574 m with 15 m spacing, and 131072 sweeps. It reports alternating transmit polarization (`TX_polarization = A`) and four ADC channels. The channel indices are `adc_like_I = 0`, `adc_like_Q = 1`, `adc_cross_I = 2`, and `adc_cross_Q = 3`. With alternating transmit polarization, `adc_data` has dimensions `[nsweep, ntxpol, nrange, nadc]`, where `ntxpol = 2` and `nadc = 4`. The four receive products are the `hh`, `hv`, `vv`, and `vh` combinations exposed by the official loader. Clock interpretation requires care. The tutorial says that an alternating sweep contains two pulses and that sweeps per second are derived from PRF, which would suggest 500 sweeps/s if PRF meant aggregate pulse rate. However, the downloaded record's netCDF metadata labels PRF as the radar pulse repetition frequency per polarization, and its 7.9872203 m/s unambiguous velocity at 9.39 GHz is consistent with a 1000 Hz per-channel rate. The generic tutorial and record metadata therefore do not support a single unambiguous seconds conversion without inspecting the full acquisition timing convention. Use sweep index and integration length in sweeps for figures and dropout statistics until that clock is independently verified. Do not report 500 Hz or 262.144 s as established facts. The tutorial documents no separate timestamp or pulse-time variable in its listed `adc_data` dimensions. The record has no per-ray wave elevation or target-pose truth.

The official [Dartmouth weather page](https://soma.ece.mcmaster.ca/ipix/dartmouth/windwave.html) says wind data came from CFB Shearwater and wave data from a buoy six nautical miles offshore. For the 13:56:03 UTC acquisition, the nearest listed wave observations are 11:45 UTC with maximum height 3.21 m, significant height 2.23 m, peak period 11.1 s, and average period 8.3 s, and 15:30 UTC with maximum height 3.02 m, significant height 2.01 m, peak period 10.0 s, and average period 8.0 s. The nearest listed wind observations are 13:00 UTC at 310 degrees and 17 km/h and 14:00 UTC at 300 degrees and 9 km/h. These are environmental context values, not instantaneous wave phase along the radar ray.

## Exact conversion and preprocessing

The official [netCDF tutorial](https://soma.ece.mcmaster.ca/ipix/dartmouth/cdfhowto.html) identifies `adc_data` as the stored ADC output and provides the loader call

`[I,Q,meanIQ,stdIQ,inbal] = ipixload(nc,pol,rangebin,mode)`.

For a transparent raw envelope, select the desired polarization and range bin directly from `adc_data`, then form

`z_t = I_t + j Q_t`,  `A_t = sqrt(I_t^2 + Q_t^2)`.

The tutorial defines automatic preprocessing as separate mean and standard-deviation removal followed by phase-imbalance correction. If $β = \text{inbal}\,\pi/180$, it estimates

`sin(beta) = 2*(I,Q)/A^2`

and rotates the in-phase channel as

`I_rot = (I - Q*sin(beta))/sqrt(1 - sin(beta)^2)`.

The documented `raw` mode performs no preprocessing. The figure should therefore state whether it uses raw ADC envelope or the tutorial's `auto` output. Do not call ADC counts calibrated volts. The parameter record reports the receiver STC reference values but does not provide a complete count-to-voltage conversion for the stored array.

The tutorial documents no universal missing-value sentinel for `adc_data`. Preserve netCDF fill or mask metadata during parsing, count nonfinite or masked samples, and report them rather than replacing them with zero. This record's labels are range-bin conventions and target metadata, not per-sweep visibility labels.

## Figure contract

Plot the measured target-versus-clutter envelope using primary bin 9 and a clutter reference formed from explicitly chosen neighboring non-target bins, with secondary bins 8:11 retained as a sensitivity check. Show the envelope over sweep index and mark a fixed threshold calibrated from a development segment. A dropout is a primary-bin sample below that threshold; report the threshold, calibration interval, polarization, preprocessing mode, and missing-sample count. This demonstrates measured target fluctuation and threshold dropouts. It does not demonstrate wave-phase causality because the buoy observations are sparse summaries and the target elevation and local wave profile are unmeasured.

## Executed processing record

The delivered figures use a common clutter-trained adaptation of the official automatic correction, rather than independently standardizing target and clutter bins. The first 32,768 sweeps in bins 1-7 and 12-14 train in-phase and quadrature means, standard deviations, and phase-imbalance sine. Those parameters are applied unchanged to every bin. Nonoverlapping 64-sweep powers are normalized by the development-clutter mean. A fixed 99th-percentile gate is calibrated on 5120 development clutter windows and applied to the remaining 1536 primary and 15,360 clutter windows. This preserves relative return differences while preventing target samples and held-out samples from fitting the correction or gate. The resulting primary-bin gate crossings remain a measured proxy without instantaneous target-presence, exposure, or wave-phase labels. Exact processing parameters and output are retained in `data/measured-ipix.json`.
