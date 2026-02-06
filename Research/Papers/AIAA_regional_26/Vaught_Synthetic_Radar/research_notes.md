# Research Notes: Multi-Mode X-Band Radar Simulation Paper

## Title
**A Multi-Mode Simulation Framework for X-Band Pulse Compression Radar**

(Changed from "Multi-Fidelity" — tiers are ordered by workflow utility, not physics fidelity)

---

## Tier Structure (NEW ORDERING)

| Tier | Name | Role | Status |
|------|------|------|--------|
| **Mode 1** | **Data-Driven Compositor** | Production training data — blend synthetic targets into real radar recordings | **Complete. YOLO results proven.** |
| **Mode 2** | **Analytical Generator** | Rapid prototyping — test statistical clutter models and detection thresholds cheaply before committing to real data | In progress |
| **Mode 3** | **EM Ray Tracing** | Physics validation — ground-truth reference for verifying assumptions in Modes 1 and 2 | Partial |

### Narrative
> "Mode 1 generates the training data that works (here's proof). Mode 2 lets you iterate
> on statistical models quickly — test a clutter hypothesis in seconds instead of compositing
> thousands of frames. Mode 3 provides physics-grounded truth to validate the assumptions
> underlying both other modes."

Top-down workflow: start with what gets results, use lower modes to understand
*why* it works and to stress-test edge cases.

### Revised Section Structure

| Section | Weight | Content |
|---------|--------|---------|
| Introduction | 15% | USV perception, data scarcity, contribution |
| Related Work | 10% | Synthetic radar data, marine radar ML, sim-to-real |
| System Architecture | 10% | Block diagram, world model, 3 modes overview |
| Mode 1 (compositor) | 20% | How it works, examples, statistical validation |
| Mode 2 (analytical) | 10% | Whatever is ready — clutter model, partial validation |
| Mode 3 (ray tracing) | 5% | Brief architecture, status, future work |
| Results: YOLO transfer | 20% | Train on Mode 1, test on real, metrics, augmentation experiment |
| Data collection | 5% | Table of collections, conditions, locations |
| Discussion / Conclusion | 5% | Limitations, honest gaps, future work |

---

## Furuno DRS4D NXT — Verified Specifications

| Parameter | Value | Source |
|-----------|-------|--------|
| Type | Solid-state, pulse compression, Doppler | Furuno spec sheet |
| Frequency | 9,380–9,440 MHz (3 selectable channels) | Furuno spec sheet |
| Emission | P0N (unmodulated pulse) and Q0N (LFM chirp) | FCC filing |
| Tx power | 100 W (current spec; older sources say 25 W) | furuno.com/special |
| Chirp pulse widths | 5.0–18 μs depending on range scale | Installation manual |
| Unmodulated pulse widths | 0.08–1.2 μs | Installation manual |
| Range resolution | ~20 m (after pulse compression) | Manual / derived |
| Horizontal beamwidth | 3.9° (physical), down to 2.0° with RezBoost | Furuno spec sheet |
| Vertical beamwidth | 22–25° (sources conflict) | Spec sheet vs. manual |
| Rotation | 24 / 36 / 48 RPM (range-coupled) | Furuno spec sheet |
| PRF | 700–1,100 Hz (range-dependent) | Radartutorial / FR spec |
| Range scales | 1/16 NM to 72 NM | Furuno spec sheet |
| Azimuth quantization | 8,192 spokes per revolution (0.044°/step) | FKIE-CAD reverse engineering |
| Range cells per spoke | Up to 2,047; ~950 at 3 NM (~100 cells/NM) | FKIE-CAD / OpenCPN captures |
| IF frequencies | 83.75 / 103.75 MHz (dual IF) | Installation manual |
| Antenna type | Microstrip patch array, 22" in 24" radome | Furuno spec sheet |
| Min range | 20 m | Furuno spec sheet |
| Bearing accuracy | +/- 1° | Furuno spec sheet |
| Sidelobe attenuation | -24 dB | Furuno spec sheet |
| Warm-up time | None (solid-state) | Furuno spec sheet |
| Weight | 7.3 kg (16.1 lb) | Furuno spec sheet |
| Radome diameter | 610 mm (24 in) | Furuno spec sheet |
| Target tracking | Up to 100 targets (40 auto, 60 manual) | Furuno spec sheet |

### Pulse Width vs Range Scale

| Range Scale (NM) | P0N Pulse (μs) | Q0N Chirp (μs) |
|-------------------|-----------------|-----------------|
| 0.0625–0.125 | 0.08 | 5.0 |
| 0.25 | 0.15 | 7.5 |
| 0.5 | 0.3 | 11 |
| 0.75–1.0 | 0.6 | 13 |
| 1.5–2.0 | 1.2 | 15 |
| 3.0–4.0+ | 1.2 | 18 |

### Frequency Channels

| Channel | P0N (unmodulated) | Q0N (chirp) |
|---------|-------------------|-------------|
| CH.1 | 9,380 MHz | 9,400 MHz |
| CH.2 | 9,400 MHz | 9,420 MHz |
| CH.3 | 9,420 MHz | 9,440 MHz |

### RezBoost Technical Details

- Digital beam sharpening / azimuthal super-resolution
- Narrows effective beamwidth from 3.9° to 2.0° (DRS4D NXT)
- Receive-side digital signal processing (deconvolution of antenna beam pattern)
- Exact algorithm not publicly disclosed (likely CLEAN, Richardson-Lucy, or Wiener)
- We disable RezBoost because it can suppress weak real targets

### Pulse Compression Details

- LFM (Linear Frequency Modulation) chirp confirmed by Q0N emission designator
- Estimated compression ratio: ~225:1 for longest chirp (18 μs compressed to 0.08 μs equivalent)
- Estimated chirp bandwidth: ~7.5–12.5 MHz (derived from 20 m range resolution, c/(2B))
- Sidelobe weighting function not disclosed (Hamming, Taylor, etc.)

### Things NOT Publicly Available

- Average transmit power
- Receiver bandwidth
- Receiver noise figure / sensitivity
- Exact chirp bandwidth and waveform parameters
- Pulse compression sidelobe weighting function
- RezBoost algorithm details
- Antenna gain in dBi
- Duty cycle

---

## Data Collection Setup

- **Installation:** Fixed, shore-based (littoral). NOT shipboard.
- **Antenna height:** 2–4 m above water (varies by setup)
- **No platform motion.**
- **Locations:**
  - Lake Murray, SC (majority of data)
  - Lake Greenwood, SC
  - Charleston Harbor, SC (2–3 sessions)
- **Range scales:** 0.25–0.75 NM, occasionally < 0.25 NM
- **Sessions:** ~30 collections, January–November 2025
- **Targets of interest:** Recreational boats and navigational buoys
- **Conditions:**
  - Mostly fair weather / calm water
  - 1–2 rain events (lake)
  - Radar interference captures (Charleston Harbor — other marine radars)
- **Data volume:** Hundreds of thousands of frames
- **RezBoost:** Disabled (can suppress weak real targets)
- **Data type:** Pre-processed log-detected intensity, B-scan (polar), NOT I/Q

### Grazing Angle Note
At 3 m height and 0.5 NM range (~926 m):
  grazing angle = arctan(3/926) ≈ 0.19°
This is extremely low. Multipath off water surface is significant.
Direct and reflected paths interfere, causing targets to fade in/out
as they move through interference nulls. Explains intermittent detections
and why robust tracking on synthetic data is a hard/valuable problem.

### Implications of Shore-Based Setup
- No motion compensation needed in simulation
- Fixed antenna height = constant multipath geometry per site
- Grazing angle only varies with range (not platform pitch/roll)
- Repeatable collection geometry across sessions
- Lake environments = minimal wave clutter, primarily wind-driven chop
- Charleston Harbor = sheltered but with vessel traffic and radar interference

### Framing for Paper
- This is INLAND AND LITTORAL waterway data, NOT open ocean
- Do NOT claim "sea states" or "sea-clutter" in the abstract — use "clutter environments"
- Frame as: "radar-based perception for unmanned surface vehicles operating
  in inland and coastal waterways"
- Do not describe specific autonomous mission; keep it general (USV perception,
  collision avoidance, navigation safety)
- Inland waterway radar perception is underserved in the literature — own it

### Key Result Already Obtained
- Trained YOLO on Mode 1 (compositor) synthetic data
- Tested on real data (same scenes the Mode 1 data was synthesized from)
- Result: "really good tracking" — NEED TO QUANTIFY with mAP, precision, recall
- This domain-transfer result IS the paper's main contribution

---

## Data Format Details

### Network Protocol

- UDP over Ethernet, proprietary application-layer protocol
- Network: 172.31.x.x / 255.255.0.0
- Radar video = UDP multicast
- Control commands = TCP
- Requires "VX2" preamble in UDP packets

### Spoke Data Format (from FKIE-CAD reverse engineering)

Frame Header (12+ bytes):
- Byte 0: Type (0x02 = spoke data)
- Byte 1: Sequence counter (rolls at 0xFF)
- Bytes 2-7: Furuno marker (0x00 01 00 00 00 00)
- Bytes 8-9: Payload length (9 bits) + spoke count (7 bits)
- Bytes 10-11: Range cell count (11 bits, max 2047) + compression level (2 bits)
- Byte 12: Range setting
- Byte 13: ACE flag (1 bit)
- Bytes 14-15: Heading flag (2 bits)

Per-Spoke Structure:
- Bytes 0-1: Azimuth (16-bit, range 0–8192)
- Bytes 2-3: Heading (16-bit encoded)
- Bytes 4+: Echo intensity data (variable length)

### Intensity Encoding

Compression Level 3 (most common):
- 6-bit echo intensity (64 levels) in upper bits
- 2-bit encoding control in lower bits:
  - 00 = Direct: upper 6 bits = echo strength
  - 01 = RLE: upper 6 bits = repeat count of previous cell
  - 10 = Reference: upper 6 bits = count matching previous spoke
  - 11 = Reserved

Compression Level 0 (uncompressed):
- 8-bit per range cell (256 levels)

### Detection Type

- Log-detected amplitude (logarithmic receiver in IF chain)
- Non-coherent — no phase information available
- Values are proportional to dB (compressed dynamic range)

### What We Capture

- Pre-processed, log-detected echo intensity in B-scan (polar) format
- Rows = azimuth angles (up to 8,192 per revolution)
- Columns = range bins (up to ~2,047)
- RezBoost disabled — native 3.9° beam pattern preserved
- Non-coherent data — no Doppler available in our pipeline

---

## Environmental Characterization

### For Charleston Harbor Data
- Use NOAA Station CHTS1 (Charleston Harbor, 32.78°N, 79.92°W) for wind data
- Use NOAA Station 41029 (Capers Nearshore) for wave data if needed
- Match collection date/time (UTC) to hourly buoy records

### For Lake Data
- Lakes don't have NDBC buoys — no direct wave measurements available
- Options for characterizing conditions:
  - NOAA ASOS station at nearest airport for wind speed/direction
  - Visual Beaufort scale estimate at time of collection
  - Simply state "sheltered inland lake, minimal wave action" — this is honest and sufficient
  - If you noted weather conditions during collection, report those
- Lake clutter is fundamentally different from ocean clutter:
  - No swell, only small wind-driven chop
  - Sheltered coves can be near-glassy
  - Fixed clutter from shoreline, docks, trees, bridges

### NOAA Buoy Stations Near South Carolina (for Charleston data)

| Station | Name | Location | Notes |
|---------|------|----------|-------|
| 41004 | EDISTO | 32.50°N, 79.10°W | Primary offshore, 35m depth, ~41 NM SE Charleston |
| 41029 | Capers Nearshore | 32.80°N, 79.62°W | Near coast, 10m depth |
| 41033 | Fripp Nearshore | 32.28°N, 80.41°W | Near Beaufort/Hilton Head, 10m depth |
| 41008 | Grays Reef | 31.40°N, 80.87°W | ~40 NM SE Savannah, 16m depth |
| CHTS1 | Charleston Harbor | 32.78°N, 79.92°W | Wind/met only, no waves |
| 8665530 | Charleston (Tides) | Charleston Harbor | Tide, water level, met |

### Accessing NOAA Historical Data

NDBC = National Data Buoy Center. NOAA's network of weather buoys.
They record wave height, wind speed, etc. hourly. Free to access online.
Just match your collection date/time to the nearest buoy reading.

Real-time (last 45 days):
- https://www.ndbc.noaa.gov/data/realtime2/{STATION_ID}.txt (standard met)
- https://www.ndbc.noaa.gov/data/realtime2/{STATION_ID}.spec (spectral wave summary)

Historical (by year):
- https://www.ndbc.noaa.gov/download_data.php?filename={STATION_ID}h{YEAR}.txt.gz&dir=data/historical/stdmet/

Data columns: YY MM DD hh mm WDIR WSPD GST WVHT DPD APD MWD PRES ATMP WTMP DEWP VIS TIDE

Python packages:
- `ndbc-api` (pip install ndbc-api) — recommended
- `NDBC` (pip install NDBC)
- `siphon` (pip install siphon)

### Douglas Sea State Scale

| Hs (m) | Douglas State | Description |
|--------|---------------|-------------|
| 0 | 0 | Calm (glassy) |
| 0–0.1 | 1 | Calm (rippled) |
| 0.1–0.5 | 2 | Smooth |
| 0.5–1.25 | 3 | Slight |
| 1.25–2.5 | 4 | Moderate |
| 2.5–4.0 | 5 | Rough |
| 4.0–6.0 | 6 | Very rough |

### Methods to Estimate Sea State from Radar Data (NOT needed for this paper)

1. SNR Calibration: 3D FFT of radar image sequence, filter with dispersion relation, linear regression Hs = a*sqrt(SNR) + b (requires buoy calibration)
2. Shadow Analysis: At low grazing angles, wave crests cast shadows. Illumination ratio vs range -> RMS surface slope -> Hs
3. CNN-based: Train on radar images paired with buoy ground truth

---

## Experiments Needed

### Mode 1 Domain Transfer — THE Main Result

Already done: Trained YOLO on Mode 1 synthetic data, tested on real data, got strong tracking.

Need to report:
- YOLO version used
- Number of synthetic training images
- Number of real test frames
- Metrics: mAP@0.5, mAP@0.5:0.95, precision, recall
- Example detection frames (YOLO finding real boats after synthetic-only training)
- Any failure cases

### Augmented Training — Robustness Experiment

Use Mode 1 compositor to add environmental degradation to training data:

1. **Radar interference augmentation:** Extract interference patterns from Charleston captures
   (radial spoke / spiral artifacts), composite onto clean synthetic training data at varying intensity
2. **Rain clutter augmentation:** Extract rain-clutter texture from real rain captures,
   blend into clean synthetic frames at varying intensity
3. **Other augmentations:** Random gain/brightness variation, additive speckle noise,
   shoreline/fixed clutter masks from real lake data

Test sets: ~100–200 frames each for rain and interference (sufficient for stable mAP).
Augmented training: add ~1,000–2,000 augmented frames per condition type to existing clean training set.

Experimental design:

| Training Set | Test Set | What It Shows |
|-------------|----------|---------------|
| Clean Mode 1 | Clean real | Baseline domain transfer (already have) |
| Clean Mode 1 | Rain real | Degradation under unseen conditions |
| Clean Mode 1 | Interference real | Degradation under unseen conditions |
| Augmented Mode 1 | Rain real | Robustness recovery |
| Augmented Mode 1 | Interference real | Robustness recovery |

CAUTION: Only augment with conditions you have real examples of (rain, interference).
Do not synthesize fog, high seas, or other conditions you can't validate.

### Mode 1 Compositor Validation

4. Compositor before/after figures: real scan vs. composite vs. difference image
5. Statistical consistency: amplitude histogram of composited region vs. surrounding clutter, KS test
6. Show examples in different conditions: calm, rain, harbor interference

### Mode 2 (In Progress — Show What You Have)

7. Clutter-only validation: synthetic clutter statistics vs. real clutter (amplitude PDF)
8. Mode 2 vs. Mode 1 comparison for equivalent scenes (if ready)

### Mode 3 (Incomplete — Describe Architecture Only)

9. Brief architecture description and one or two canonical validation plots if available
10. Be honest about missing features — this is future work

### Supplementary

11. Computational cost table: wall-clock time per synthetic scan per mode

---

## Target Information

### Recreational Boats at X-Band

- Small fiberglass boats (15–25 ft): RCS 0.5–20 m², highly aspect-dependent, Swerling I/III
- Aluminum boats / pontoons: RCS 5–50 m², more stable
- Jet skis: RCS ~0.5–5 m²
- Kayaks / paddleboards: RCS < 0.1 m² — extremely difficult

### Navigational Buoys

- With radar reflectors: RCS 1–10 m², relatively stable
- Without reflectors: much lower, variable

### Empirical RCS Extraction

Pick frames with known targets at known ranges, back-calculate apparent RCS from radar equation
using known Furuno parameters. Build small empirical dataset — genuine contribution
(very little published recreational boat RCS data at X-band).

---

## Figures Needed

| # | Figure | Section |
|---|--------|---------|
| 1 | System architecture block diagram (3 modes, inputs/outputs, workflow arrows) | System Architecture |
| 2 | World model geometry (radar on shore, water surface, targets, multipath) | System Architecture |
| 3 | Compositor before/after (real scan + injected target + difference) | Mode 1 |
| 4 | Compositor statistical validation (histogram overlay, KS test result) | Mode 1 |
| 5 | Clutter statistics from Mode 2 (PDF/CDF: generated vs. real data) | Mode 2 |
| 6 | Example B-scan / PPI images from each mode side by side | Mode 1/2 |
| 7 | Ray-tracing architecture diagram or canonical scene result | Mode 3 |
| 8 | YOLO detection examples (synthetic-trained model on real data) | Results |
| 9 | Augmentation robustness table/chart (clean vs. augmented training) | Results |
| 10 | Computation time comparison (table or bar chart per mode) | Results |

---

## References to Cite

### Foundational Radar
- Skolnik, M.I., *Introduction to Radar Systems*, 3rd ed.
- Richards, M.A., *Fundamentals of Radar Signal Processing*, 2nd ed.
- Barton, D.K., *Radar System Analysis and Modeling*

### Sea / Water Clutter
- Ward, K.D., Tough, R.J.A., Watts, S., *Sea Clutter: Scattering, the K Distribution and Radar Performance*, 2nd ed., IET, 2013
- Farina, A., et al., "High Resolution Sea Clutter Data: Statistical Analysis of Recorded Live Data," IEE Proc. Radar, Sonar and Navigation, 1997
- Haykin, S., et al., "Uncovering Nonlinear Dynamics — The Case Study of Sea Clutter," Proc. IEEE, 2002
- Antipov, I., "Statistical Analysis of Northern Australian Sea Clutter Data," DSTO Report, 2001
- Conte, E., De Maio, A., Galdi, C., "Statistical Analysis of Real Clutter at Different Range Resolutions," IEEE Trans. AES, 2004

### RCS and Target Modeling
- Knott, E.F., Shaeffer, J.F., Tuley, M.T., *Radar Cross Section*, 2nd ed., SciTech, 2004
- Swerling, P., "Probability of Detection for Fluctuating Targets," IRE Trans., 1960

### Multipath / Low-Grazing-Angle
- Long, M.W., *Radar Reflectivity of Land and Sea*, 3rd ed., Artech House, 2001
- Barton, D.K., "Low-Angle Radar Tracking," Proc. IEEE, 1974
- Blake, L.V., *Radar Range-Performance Analysis*, Artech House, 1986

### Synthetic Radar Data / Simulation
- Auer, S., et al., "Ray Tracing and SAR Simulation for Radar Target Signature Analysis" (DLR)
- Hammer, H., Schulz, K., "Coherent Simulation of SAR Images," Proc. SPIE, 2009

### Maritime Radar Detection / CFAR
- Rohling, H., "Radar CFAR Thresholding in Clutter and Multiple Target Situations," IEEE Trans. AES, 1983
- Gandhi, P.P., Kassam, S.A., "Analysis of CFAR Processors in Nonhomogeneous Background," IEEE Trans. AES, 1988

### Domain Adaptation / Sim-to-Real
- Tobin, J., et al., "Domain Randomization for Transferring Deep Networks from Simulation to the Real World," IROS 2017
- Tremblay, J., et al., "Training Deep Networks with Synthetic Data: Bridging the Reality Gap," CVPR Workshop 2018

### YOLO / Object Detection
- (Cite whatever YOLO version you used — v8, v9, v11, etc.)

### Tracking
- Bar-Shalom, Y., Li, X.R., Kirubarajan, T., *Estimation with Applications to Tracking and Navigation*

### Marine Radar Standards
- IMO Resolution MSC.192(79) — performance standards for radar equipment
- Furuno DRS4D NXT technical documentation / product specifications

### USV / Autonomous Surface Vehicles
- (Search for recent USV perception papers — this is a fast-moving field, cite 2023–2025 work)

---

## Reverse Engineering Resources for Furuno Radar Protocol

### FKIE-CAD Maritime Dissector (Wireshark Plugin)
- GitHub: https://github.com/fkie-cad/maritime-dissector
- Protocol docs: https://raw.githubusercontent.com/fkie-cad/maritime-dissector/master/docs/Furuno-protocol.md
- Lua-based Wireshark dissector with detailed packet format documentation
- Most detailed public protocol specification available

### MAYARA Project (Rust)
- GitHub: https://github.com/keesverruijt/mayara
- Partial DRS4D NXT support
- Spoke data discussion: https://github.com/keesverruijt/mayara/issues/4

### OpenCPN Radar Pi Community
- DRS4DL+ Wireshark captures: https://github.com/opencpn-radar-pi/radar_pi/issues/246
- Furuno support discussion: https://github.com/opencpn-radar-pi/radar_pi/issues/116
- Cruisers Forum packet analysis: https://www.cruisersforum.com/forums/f134/radar-furuno-drs4dl-recorded-wireshark-packets-for-analysis-279272.html

### Official SDK
- Furuno Sensor SDK (commercial): https://www.furuno.com/en/support/sdk/
- USA page: https://www.furunousa.com/en/sdk
- DRS Ethernet radars: https://www.furunousa.com/en/sdk/drs_ethernet_radars

### Cambridge Pixel (Commercial)
- SPx Server with Furuno support: https://cambridgepixel.com/support/supported-radars/furuno-radars/

---

## Furuno Documentation Links

- Official NXT series comparison: https://www.furuno.com/special/en/radar/drs4d-nxt/
- Radartutorial entry: https://www.radartutorial.eu/19.kartei/07.naval2/karte009.en.html
- Installation manual (ManualsLib): https://www.manualslib.com/manual/1170026/Furuno-Drs4d-Nxt.html
- Spec sheet (Furuno France): https://furuno.fr/docs/SPECIFICATIONSSP_DRS4DNXT_RADAR_SENSOR.pdf
- Brochure PDF: https://www.furuno.com/files/Brochure/334/upload/DRS4D-NXT_E.pdf
- FCC filing: https://fcc.report/FCC-ID/ADB9ZWRTR115
- Furuno USA forum (data format): https://furunousaforum.com/threads/what-is-the-radar-video-data-format-of-drs4d-nxt.4141/
- Panbo review: https://panbo.com/testing-furuno-drs4d-nxt-solid-state-doppler-radome-radar-redefined-most-definitely/

---

## NOAA Data Links

- NDBC SE USA map: https://www.ndbc.noaa.gov/mobile/region.php?reg=southeast_usa
- Station 41004 (EDISTO): https://www.ndbc.noaa.gov/station_page.php?station=41004
- Station 41029 (Capers): https://www.ndbc.noaa.gov/station_page.php?station=41029
- Station CHTS1 (Charleston): https://www.ndbc.noaa.gov/station_page.php?station=chts1
- Historical data portal: https://www.ndbc.noaa.gov/historical_data.shtml
- Tides & Currents Charleston: https://tidesandcurrents.noaa.gov/stationhome.html?id=8665530
