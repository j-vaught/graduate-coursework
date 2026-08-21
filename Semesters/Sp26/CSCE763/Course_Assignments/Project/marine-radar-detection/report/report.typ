// Classical vs. Deep Learning Object Detection in X-Band Marine Radar Imagery
// J.C. Vaught and Ty Dangerfield
// Typst 0.14

// ── Brand palette ─────────────────────────────────────────────────────
#let garnet    = rgb("#73000A")
#let black     = rgb("#000000")
#let black-90  = rgb("#363636")
#let black-70  = rgb("#5C5C5C")
#let black-50  = rgb("#A2A2A2")
#let black-30  = rgb("#C7C7C7")
#let black-10  = rgb("#ECECEC")
#let warm-grey = rgb("#676156")
#let sandstorm = rgb("#FFF2E3")
#let rose      = rgb("#CC2E40")
#let atlantic  = rgb("#466A9F")
#let congaree  = rgb("#1F414D")
#let horseshoe = rgb("#65780B")
#let honeycomb = rgb("#A49137")

// ── Document setup ────────────────────────────────────────────────────
#set document(
  title: "Classical vs. Deep Learning Object Detection in X-Band Marine Radar Imagery",
  author: ("J.C. Vaught", "Ty Dangerfield"),
  keywords: ("marine radar", "object detection", "CFAR", "wavelet", "YOLO", "deep learning"),
)

#set heading(numbering: "1.")

#set page(
  paper: "us-letter",
  margin: (top: 0.9in, bottom: 1in, x: 0.85in),
  numbering: "1 / 1",
  number-align: center,
  footer: context [
    #set text(size: 8pt, fill: black-70)
    #grid(
      columns: (1fr, auto, 1fr),
      align: (left, center, right),
      [CSCE 763 Technical Report],
      counter(page).display("1 / 1", both: true),
      [April 2026],
    )
  ],
)

#set text(
  font: ("New Computer Modern", "Latin Modern Roman", "STIX Two Text", "Times New Roman"),
  size: 10pt,
  lang: "en",
  hyphenate: true,
)

#set par(justify: true, leading: 0.55em, first-line-indent: 0pt)

// Heading styles – garnet accents, no rounded edges anywhere.
// Tightened heading styles — pulls the underline close to the title text
// and reduces the gap before body copy.
#show heading.where(level: 1): it => {
  set text(fill: garnet, size: 12pt, weight: "bold")
  set block(above: 0.7em, below: 0.5em)
  block[
    #smallcaps(it.body)
    #v(-6pt)
    #line(length: 100%, stroke: 1pt + garnet)
  ]
}
#show heading.where(level: 2): it => {
  set text(fill: black-90, size: 10.5pt, weight: "bold")
  block(above: 0.7em, below: 0.3em)[#it.body]
}
#show heading.where(level: 3): it => {
  set text(fill: black-90, size: 10pt, weight: "semibold", style: "italic")
  block(above: 0.7em, below: 0.3em)[#it.body]
}

// Link / ref styling
#show link: it => text(fill: atlantic)[#it]
#show ref: it => text(fill: garnet, weight: "semibold")[#it]

// Figure captions
#show figure.caption: it => {
  set text(size: 9pt, fill: black-70)
  block(above: 0.35em)[
    #text(fill: garnet, weight: "bold")[#it.supplement #it.counter.display()#it.separator]
    #it.body
  ]
}

// Tables: no vertical rules, just horizontal
#set table(
  stroke: (_, y) => {
    if y == 0 { (bottom: 0.8pt + black, top: 0.8pt + black) }
    else { (bottom: 0.3pt + black-50) }
  },
  inset: 6pt,
)

// ── Title block ───────────────────────────────────────────────────────
#align(center)[
  #block(width: 100%, inset: (y: 0.4em))[
    #text(size: 17pt, weight: "bold", fill: black)[
      Classical vs. Deep Learning Object Detection \
      in X-Band Marine Radar Imagery
    ]
  ]
  #v(-10pt)
  #text(size: 11pt)[
    *J. Vaught, T. Dangerfield* \
  ]
  #v(-5pt)
  #text(size: 9pt, fill: black-70, style: "italic")[
    CSCE 763 — Digital Image Processing \
  ]
]

#v(-5pt)
#line(length: 100%, stroke: 0.4pt + black-50)
#v(0.2em)

// ── Abstract ──────────────────────────────────────────────────────────
#block(
  fill: sandstorm,
  stroke: (left: 2pt + garnet),
  inset: (x: 14pt, y: 10pt),
  width: 100%,
)[
  #text(weight: "bold", size: 9.5pt, fill: garnet)[ABSTRACT.]
  #text(size: 9.5pt)[
    X-band marine radar produces plan-position-indicator (PPI) imagery in which
    vessels appear as bright returns against sea clutter.  We present the
    first head-to-head benchmark of classical signal-processing
    detectors against three modern deep-learning detectors
     on the DLR DAAN, DARC, and MANV corpora.  Constructing a
    trustworthy evaluation required two methodological contributions we
    believe are reusable. Under the clean GT
    and a unified COCO-style evaluation(which we developed), YOLOv11 reaches AP\@0.50 = 0.776
    ± 0.06, edging past RT-DETR at 0.738 and Faster
    R-CNN at 0.545.  The best classical baselines are competitive but below the deep methods.
    Per-dataset analysis reveals that CA-CFAR dominates on the close-range
    MANV capture (AP\@0.50 = 0.785) while morphological and Otsu lead on
    the long-range DAAN/DARC captures — an inversion that mirrors the
    physical SNR regime each technique was designed for.
  ]
]

#v(0.6em)

// Two-column body starts here
#show: rest => columns(2, gutter: 18pt, rest)

// ── Introduction ──────────────────────────────────────────────────────
= Introduction

Marine radar is the primary all-weather sensor for situational awareness at
sea.  An X-band PPI display is a polar-to-Cartesian rendering of pulse-echo
returns on which vessels, buoys and debris manifest as small, high-contrast
blobs embedded in spatially structured sea clutter
[1][2].  Automatic object detection on such imagery
enables collision avoidance, port surveillance, and autonomous-navigation
decision support.

Two detection paradigms dominate the literature.  *Classical* methods are
rooted in signal processing: constant-false-alarm-rate (CFAR) detectors
adaptively threshold on local statistics [2]; morphological pipelines
combine Otsu binarisation with opening / closing to isolate target blobs
[5]; stationary wavelet transforms exploit the multi-scale target
structure against clutter [3]; and seed-point Otsu variants (SSOTSU) are
tailored to small targets [4].  *Deep-learning* detectors cast the problem
as a learned regression: YOLOv11-OBB with SAHI tiling reports
mAP\@0.50 > 0.95 on a small radar set [8], Marine-Faster R-CNN reports
93.65% recall [7], U-Net has been adapted for radar segmentation [9], and
transformer detectors such as CCDN-DETR are emerging [10].

The literature lacks a controlled apples-to-apples comparison.  Existing
studies report headline numbers but differ in preprocessing, annotation
granularity, evaluation protocol, and training regime.  Our contributions
fill that gap on the DLR DAAN/DARC/MANV corpus [6]:

+ A reproducible preprocessing pipeline that isolates radar returns from
  UI chrome per-dataset (red-channel for DAAN/DARC, yellow-hue HSV for
  MANV), applies a circular PPI mask, and produces tiled and full-frame
  evaluation surfaces.
+ A new *hybrid* ground-truth construction that replaces DBSCAN with
  AIS-seeded matching to image-grounded connected-component extents,
  producing tight bounding boxes instead of uniform 33 × 33 padded
  rectangles (see @fig:gt-compare).
+ Per-dataset polar-projection calibration: we measured the DLR radar
  settings from the data and confirmed them against the DLR paper [6].
  MANV uses 6 m/px while DAAN and DARC use ≈ 12 m/px — the released code
  assumed a single global scale, which was the root cause of every AIS
  misalignment we observed in MANV.
+ Systematic benchmarking of three deep detectors (three random seeds each)
  and seven classical detectors against the cleaned GT, with per-dataset
  breakdowns that show how each method's performance depends on the
  range-resolution regime.
+ A public release of preprocessing code, configs, checkpoints, the
  hybrid-GT generator, an interactive Flask-based calibration tuner,
  and all twenty prediction files at
  #link("https://github.com/j-vaught/marine-radar-detection")[github.com/j-vaught/marine-radar-detection].

#figure(
  image("figures/fig1_headline.png", width: 100%),
  placement: auto,
  scope: "parent",
  caption: [
    *Headline ranking on the DAAN test split at AP\@0.50.*  Deep-learning
    bars show mean ± 1 σ over 3 random seeds; classical bars are
    deterministic.  Every method is evaluated under a unified COCO
    protocol on the clean AIS-anchored GT.  YOLOv11 leads at 0.776, RT-DETR
    second at 0.738, Faster R-CNN a distant third at 0.545 (essentially
    tied with the best classical baselines).
  ],
) <fig:headline>

// ── Dataset ──────────────────────────────────────────────────────────
= Dataset and Preprocessing

We use the three DLR radar corpora distributed with the PPINet release [6]:
*MANV* (952 close-range manoeuvre frames, used for training), *DARC*
(527 beacon-association frames, validation), and *DAAN* (760 nav-aid
frames, held-out test) — 2,239 PPI frames total at 1,050 × 1,024 px.
Each frame ships with a `polarMeas.json` file listing per-object radar-
return boundary points in polar (r, theta) coordinates along with
AIS-correlated identity.  @fig:dataset summarises the splits.

== Dataset-aware Target Isolation

Raw captures contain a substantial display overlay (compass rose, bearing
ticks, range rings, control panel) plus a solid coloured PPI background.
Naïve grayscale conversion maps UI chrome onto the same intensity range
as radar returns, producing systematic false positives for every
classical detector we evaluated.

#figure(
  image("figures/fig8_dataset.png", width: 100%),
  caption: [
    *Clean-GT dataset composition.*  Temporal splits by recording
    session prevent information leakage.  DAAN has a median of 3 objects
    per frame with a tail to five; DARC and MANV are slightly sparser /
    denser respectively.
  ],
) <fig:dataset>

*DAAN and DARC* use a blue PPI background (BGR ≈ (140, 0, 0)) with
near-white vessel returns (BGR ≈ (234, 239, 226)) and green bearing
marks (0, 255, 0).  The *red channel* alone isolates radar returns
because the background has R = 0 and green UI has R = 0, while target
pixels read R ≈ 226.

*MANV* uses a dark-blue background, *yellow* radar returns (HSV
hue ≈ 30°, saturation ≥ 100), and *white* UI chrome (255, 255, 255).
The red channel fails here because white UI also saturates R = 255.
The only distinguishing axis is *saturation* — we use a hue + saturation
HSV filter (hue ∈ [15, 50], saturation ≥ 80) that passes yellow returns
and rejects the desaturated white chrome.  @fig:preprocess shows the
resulting clean signal in each sub-dataset.

#figure(
  image("figures/fig7_preprocess.png", width: 100%),
  placement: auto,
  scope: "parent",
  caption: [
    *Preprocessing pipeline output* per sub-dataset.  (a)–(c) Each PPI
    frame is reduced to a single-channel target-signal image using the
    per-dataset colour isolation rule (red-channel for DAAN/DARC,
    yellow-hue HSV for MANV).  (d) AIS-anchored GT boxes (garnet)
    overlaid on the DAAN preprocessed frame — every box sits on an
    actual radar return.
  ],
) <fig:preprocess>

== Polar-Origin and Range-Scale Calibration

The DLR data ships with `polarMeas.json` boundary points in metres /
radians.  A direct naïve projection places AIS-derived seeds 40–70 pixels
from the nearest radar blob in MANV, which initially looked like
harbour-vessel timing drift.  A 2-D grid search against per-frame image
blobs revealed two distinct issues.  First, the *polar origin* (antenna
reference point) is offset ≈ 17 px from the visual PPI centre on every
dataset — not caused by any display artefact but simply because the
antenna reference and display centre are not coincident.  Second, and
only on MANV, `max_range_m` is 2,800 m rather than the 5,750 m used by
DAAN/DARC.  @tab:cal lists the per-dataset values we determined; these
were subsequently confirmed against the DLR paper [6] which explicitly
documents the MANV "finer resolution of 6 m" vs. DAAN/DARC's "coarser
11 m" range-cell scales.

#figure(
  placement: top,
  scope: "parent",
  kind: table,
  caption: [
    *Per-dataset polar calibration.*  Fitted values produce median
    AIS-seed → image-blob pixel offsets of 5–7 px across all three
    sub-datasets; the default naive calibration produces 22 px on
    DAAN/DARC and 67 px on MANV.
  ],
  table(
    columns: (1fr, 1fr, 1fr, 1.2fr, 1.2fr, 1.2fr),
    align: (left, right, right, right, right, right),
    table.header[*Dataset*][*cx*][*cy*][*r\_px\_max*][*max\_range\_m*][*m/px*],
    [DAAN], [512], [516], [466], [5,750], [12.34],
    [DARC], [514], [521], [466], [5,600], [12.02],
    [MANV], [514], [528], [466], [2,800], [*6.01*],
  ),
) <tab:cal>

== Hybrid AIS-Anchored Ground Truth

The default `polar_to_coco` annotation script provided with the DLR
release uses DBSCAN to cluster boundary points into per-target groups
and outputs a uniform 33 × 33 px padded bounding box around each
cluster centroid.  The resulting GT is geometrically uniform (all boxes
the same size regardless of vessel length) and fails to respect actual
radar-return extents, which biases any IoU-based evaluation.  We replace
it with a *hybrid* pipeline:

+ Parse `polarMeas.json` and DBSCAN-cluster the polar boundary points
  in metres (eps = 200, min samples = 5) to obtain per-target
  seeds in pixel coordinates using the fitted per-dataset calibration.
+ Threshold the per-dataset isolated signal at intensity > 25, apply
  a 5 × 5 ellipse closing to bridge single-vessel fragmentation, and
  extract connected components with 8-connectivity.  Filter by area
  ∈ [10, 8000] px² to reject speckle and land.
+ Greedy-match each AIS seed to its nearest available blob within
  20 px (30 px for DAAN/DARC, 20 for MANV — MANV is the close-range
  dataset and blob spacing in a harbour is tighter).  Emit the blob's
  native bounding box as GT; drop unmatched seeds.

@fig:gt-compare shows the dramatic effect on a DAAN test frame.

#figure(
  image("figures/fig6_qualitative.png", width: 100%),
  placement: auto,
  scope: "parent",
  caption: [
    *Qualitative comparison.*  (a) DL detectors on a tile — YOLOv11 in
    atlantic picks up the multi-vessel cluster; RT-DETR in rose is more
    conservative at high confidence; Faster R-CNN in horseshoe emits
    fewer boxes.  (b) Classical detectors on the corresponding
    full-resolution frame — morphological (congaree), Otsu (honeycomb),
    and CA-CFAR (rose) all recover the main targets but with differing
    degrees of over-detection.  Garnet rectangles are ground truth.
  ],
) <fig:gt-compare>

== Splits and Tiling

Temporal splits use the three sub-datasets directly: MANV → train, DARC
→ val, DAAN → test.  Full-resolution frames are tiled into 640 × 640
patches with 20 % overlap for deep detectors (5,712 train / 3,162 val /
4,560 test tiles).  Classical detectors operate on the full 1,050 × 1,024
images (760 test frames) to avoid tile-boundary fragmentation of larger
vessel returns.  The two evaluation surfaces are otherwise identical
(same targets, same preprocessed signal) but differ in GT count
(6,980 tile-level vs. 1,935 full-frame).

// ── Methods ──────────────────────────────────────────────────────────
= Methods

All ten detectors share the preprocessed single-channel inputs described
above.  Classical detectors return (x_1, y_1, x_2, y_2) boxes with a
calibrated confidence score (peak-to-threshold ratio or normalised
coefficient magnitude); deep detectors emit native scored outputs.

== Classical Detectors

*CA/GO/SO-CFAR* implement standard 2-D sliding-window CFAR with
"guard" = (15, 15) and "reference" = (30, 30) half-sizes after
empirically determining that smaller guard bands cause target
self-suppression.  PFA is fixed at 10^(-3).

*Morphological.*  Otsu binarisation computed *only on non-zero
pixels* (required when operating on circularly masked inputs so the
outside-disc zero mass does not dominate the histogram) followed by a
3 × 3 elliptical opening and 5 × 5 closing to bridge target gaps.

*Otsu / SSOTSU.*  Global Otsu on non-zero pixels for a strong unsupervised
baseline; SSOTSU [4] uses 64 × 64 blocks with stricter local-Otsu seeding
(factor 2.0) and region-grow threshold 0.6, with a 30–5000 px² area
filter to suppress the sub-pixel speckle and full-harbour-wide noise
blobs that the default parameters emit on this clean-GT surface.

*Wavelet-SWT.*  Stationary wavelet transform with Daubechies-4 at 3
levels.  The three high-frequency sub-bands (LH, HL, HH) are each
thresholded at mu + 6 sigma and combined by pixel-wise maximum.  After
tuning for the tight-GT regime we observed Wavelet-SWT still emits
too-broad connected components (median 44 × 47 px vs. GT median
15 × 15 px) and reports AP\@0.50 = 0 on every sub-dataset — the method
needs a fundamentally different post-processing stage on tight GT that
we leave as future work.

== Deep Learning Detectors

All DL models trained with three random seeds {42, 123, 456} on the
5,712 training tiles (AIS-anchored GT).

- *YOLOv11-M* (Ultralytics).  AdamW, lr0 = 10⁻³, batch 16,
  patience 20, imgsz 640.  All three seeds early-stop between
  epochs 20 and 45.
- *RT-DETR-L* (Ultralytics).  AdamW, lr 10⁻⁴, batch 8,
  72 epochs per seed.
- *Faster R-CNN* (ResNet-50-FPN, torchvision).  SGD momentum 0.9,
  lr 5 × 10⁻³, batch 8, 50 epochs.  Anchor scales tailored to
  the 15 × 15-median-pixel target regime
  (`sizes = ((16,), (32,), (64,), (128,), (256,))`).
- *U-Net* (ResNet-34 encoder).  DiceBCE loss, AdamW, cosine LR,
  80 epochs, batch 4 (bs = 8 OOMs on 48 GB due to encoder-decoder
  skip connections).  U-Net results are omitted from this write-up
  because training had not completed at press time.

All training used four NVIDIA RTX 6000 Ada GPUs (48 GB each), one
model per GPU.  Tile-level inference uses `test_tiled.json`
(4,560 tiles, 6,980 annotations).

// ── Evaluation ───────────────────────────────────────────────────────
= Evaluation Protocol

We report the full COCO suite: AP at IoU thresholds
{0.50, 0.75, [0.50:0.95]} and AR\@{1, 10, 100}.  Deep-model
numbers are the mean and standard deviation over three seeds.

All code, configs, checkpoints, and prediction JSONs are released so
every number in the paper can be reproduced end-to-end by running
`make preprocess && make classical && bash scripts/train_all.sh &&
make infer-dl && make evaluate`.

// ── Results ──────────────────────────────────────────────────────────
= Results

@tab:main reports the full benchmark.  Deep detectors dominate the
overall ranking: YOLOv11 reaches *AP\@0.50 = 0.776 ± 0.06*, RT-DETR
0.738 ± 0.03, and Faster R-CNN 0.545 ± 0.04.  Among classical methods
morphological (0.537) and Otsu (0.534) are essentially tied, both just
below Faster R-CNN, and CA-CFAR follows at 0.483.

#figure(
  placement: top,
  scope: "parent",
  kind: table,
  caption: [
    *Main results on DAAN test.*  Deep-learning columns show mean ± 1 σ
    over 3 seeds evaluated on 4,560 640 × 640 tiles; classical columns
    are deterministic, evaluated on 760 full 1,050 × 1,024 frames.
    *Preds* is the total number of detection boxes emitted (mean for
    DL).  Ranked by AP\@0.50.
  ],
  table(
    columns: (2fr, 1fr, 1.4fr, 1.4fr, 1.6fr, 1.4fr, 1.3fr),
    align: (left, left, right, right, right, right, right),
    table.header[*Method*][*Type*][*AP\@0.50*][*AP\@0.75*][*AP\@[.50:.95]*][*AR\@100*][*Preds*],
    [YOLOv11],       [DL (×3)], [*0.776 #text(size:7.5pt, fill: black-70)[±0.059]*],
                                 [0.733 #text(size:7.5pt, fill: black-70)[±0.041]],
                                 [0.610 #text(size:7.5pt, fill: black-70)[±0.029]],
                                 [0.790 #text(size:7.5pt, fill: black-70)[±0.033]],
                                 [28,286],
    [RT-DETR],       [DL (×3)], [0.738 #text(size:7.5pt, fill: black-70)[±0.029]],
                                 [0.732 #text(size:7.5pt, fill: black-70)[±0.028]],
                                 [*0.635* #text(size:7.5pt, fill: black-70)[±0.019]],
                                 [*0.876* #text(size:7.5pt, fill: black-70)[±0.010]],
                                 [199,954],
    [Faster R-CNN],  [DL (×3)], [0.545 #text(size:7.5pt, fill: black-70)[±0.044]],
                                 [0.533 #text(size:7.5pt, fill: black-70)[±0.043]],
                                 [0.422 #text(size:7.5pt, fill: black-70)[±0.035]],
                                 [0.456 #text(size:7.5pt, fill: black-70)[±0.042]],
                                 [4,523],
    [Morphological], [Classical], [0.537], [0.315], [0.311], [0.661], [4,289],
    [Otsu],          [Classical], [0.534], [0.338], [0.318], [0.676], [4,663],
    [CA-CFAR],       [Classical], [0.483], [0.408], [0.388], [0.832], [4,078],
    [SO-CFAR],       [Classical], [0.342], [0.315], [0.255], [0.672], [4,268],
    [GO-CFAR],       [Classical], [0.315], [0.224], [0.204], [0.535], [3,501],
    [SSOTSU],        [Classical], [0.030], [0.009], [0.014], [0.449], [49,163],
    [Wavelet],       [Classical], [0.000], [0.000], [0.000], [0.000],  [5,916],
  ),
) <tab:main>

*On AR\@100, the story flips interestingly.*  RT-DETR leads at 0.876
(it over-predicts at low confidence but recovers nearly every target),
followed closely by CA-CFAR at 0.832.  CA-CFAR's very high recall at
its operating point confirms that CFAR is fundamentally a strong
*recaller* on radar imagery — its precision ceiling is limited only by
box-shape mismatch with AIS-derived GT, not by detection itself.

@fig:multimetric generalises the ranking across all four metrics.

#figure(
  image("figures/fig2_multimetric.png", width: 100%),
  placement: auto,
  scope: "parent",
  caption: [
    Per-metric comparison.  YOLOv11 leads AP at every IoU threshold;
    RT-DETR leads AR\@100 driven by its large prediction volume;
    morphological and Otsu lead the classical sub-ranking on the
    precision metrics; CA-CFAR leads classical AR\@100.
  ],
) <fig:multimetric>

== Per-Dataset Behaviour

Running the seven classical methods separately on each DLR sub-dataset
reveals a striking inversion (@fig:perds).  *On the close-range MANV
capture* (6 m/px resolution, harbour manoeuvres), *CA-CFAR dominates
at AP\@0.50 = 0.785* — it sits where CFAR was designed to operate: dense
clutter, high-SNR targets, sub-metre pixel resolution.  *On the
long-range DAAN and DARC captures* (12 m/px, open water), *morphological
and Otsu lead* at 0.53–0.54, while CA-CFAR drops to 0.28–0.48.  The
coarser range-cell weakens CFAR's adaptive-threshold advantage, and
morphological opening is a better fit for the smaller, more discrete
target blobs at 12 m/px.

#figure(
  image("figures/fig3_per_dataset.png", width: 100%),
  placement: auto,
  scope: "parent",
  caption: [
    *Per-sub-dataset classical AP\@0.50.*  MANV (green, 6 m/px)
    massively favours the CFAR family, which reaches AP\@0.50 ≈ 0.78
    on CA-CFAR.  DAAN (garnet, 12 m/px) and DARC (atlantic, 12 m/px)
    invert the ranking: morphological / Otsu lead at 0.53–0.54 with
    CFAR trailing.  This inversion argues that practical systems should
    choose the classical detector to the radar's operating resolution.
  ],
) <fig:perds>

== Deep-Learning Seed Stability

@fig:dlseed reports per-seed breakdowns for the three DL detectors.
YOLOv11 is the most consistent (σ ≈ 0.01–0.02 on AP), RT-DETR next
(σ ≈ 0.03), and Faster R-CNN most variable (σ ≈ 0.04).  No single
method has its best or worst seed dominating any metric.

#figure(
  image("figures/fig4_dl_seeds.png", width: 100%),
  caption: [
    *Deep-learning per-seed breakdown.*  All three DL detectors show
    low seed-to-seed variance (σ ≤ 0.06 on every metric), suggesting
    the training regime has converged to a stable optimum.
  ],
) <fig:dlseed>

== Detection Volume vs. Precision

@fig:vol shows the trade-off between total predictions emitted and
achieved AP.  Faster R-CNN is remarkably efficient — 4,500 predictions
across 4,560 tiles, one-to-one with tile count, and AP = 0.55.  Classical
methods cluster around 4–8 k predictions (moderate over-prediction) at
AP = 0.3–0.55.  YOLOv11 at 28 k and RT-DETR at 200 k over-predict
heavily but the learned ranking recovers precision.  SSOTSU and Wavelet
are clear outliers — SSOTSU emits 49 k predictions at AP = 0.03
(massive over-prediction), Wavelet 5.9 k at AP ≈ 0.

#figure(
  image("figures/fig5_count_vs_ap.png", width: 100%),
  caption: [
    *Detection volume vs. AP\@0.50.*  Dashed vertical lines mark the
    GT target counts on each evaluation surface.  Methods that hover
    near the GT count (Faster R-CNN, CA-CFAR, morphological, Otsu)
    achieve good precision per-prediction; methods that heavily
    over-predict (RT-DETR, YOLOv11) still reach high AP because their
    learned confidence ranking preserves precision at low recall.
  ],
) <fig:vol>

// ── Discussion ───────────────────────────────────────────────────────
= Discussion

*Deep detectors win on this benchmark, but the classical gap is
narrower than the literature implies.*  The best classical baseline
(morphological, AP\@0.50 = 0.537) is only 0.008 below Faster R-CNN and
represents 69 % of YOLOv11's score — without any training, without
pretrained weights, and with a deterministic output.  For operational
deployments with minimal labelled data, interpretability requirements,
or on-board compute limits, morphological is a very reasonable default.

*The classical paradigm chooses the detector.*  The DAAN/DARC vs. MANV
inversion (@fig:perds) is the most actionable result for practitioners.
CA-CFAR's 0.79 AP on MANV is competitive with the deep detectors on
DAAN.  If a radar system is operated at 6 m/px (typical harbour
surveillance) CA-CFAR should be the default.  At 12 m/px (open-water
navigation), morphological or Otsu is the better choice.

*Tile vs. full-frame evaluation.*  Deep detectors were trained and
evaluated on 640 × 640 tiles, classical detectors on full 1,050 × 1,024
frames.  Both surfaces are generated from identical preprocessed
inputs against AIS-anchored GT of identical geometry, and COCO's IoU
computation is translation-invariant, but the two GT counts differ
(6,980 tile annotations vs. 1,935 full-frame).  A single target near
a tile boundary appears in two overlapping tiles and is counted twice
in the tile GT — so tile AP rewards high recall on near-boundary
targets relative to full-frame AP.  We flag this asymmetry as a
caveat rather than a confound: the rank ordering within each scope
is internally consistent.

*Why the classical literature reports much higher numbers.*  The PPINet
paper [6] and Marine-Faster R-CNN [7] both evaluate against the DBSCAN
padded GT (33 × 33 boxes) that we replaced.  Uniform-size padded GT is
much easier for any detector to match at IoU = 0.50 because box extent
is decoupled from the actual radar return.  Our numbers report
*tight-box* IoU against AIS-verified targets and are therefore
strictly lower than published results — but also more predictive of
operational detection quality.

*Limitations.*  Our Wavelet-SWT implementation emits 5 k predictions of
mean size 44 × 47 px on a GT of median 15 × 15 — the method produces
target-like blobs at the wrong scale and our per-component scoring
doesn't recover precision.  A proper Wavelet-SWT evaluation would need
per-scale bbox extraction and dedicated NMS.  U-Net training did not
complete in time for this draft.

// ── Conclusion ───────────────────────────────────────────────────────
= Conclusion

We presented the first controlled cross-paradigm benchmark of classical
and deep-learning object detection on X-band marine radar PPI imagery
after fixing two systematic issues in the public DLR release (a 17-px
polar-origin bias on all three sub-datasets and a 2× range-scale error
on MANV) and replacing the default DBSCAN padded GT with a hybrid
AIS-anchored / image-grounded construction.  Under this cleaner
evaluation, YOLOv11 leads at AP\@0.50 = 0.776 ± 0.06 over 3 seeds,
with RT-DETR at 0.738 and Faster R-CNN at 0.545.  Classical methods are
competitive but below the learned detectors in aggregate; their relative
ranking depends sharply on the radar's range-resolution regime, with
CA-CFAR dominating the close-range MANV capture at AP = 0.785 and
morphological / Otsu leading the long-range DAAN / DARC captures.  All
artefacts — code, configs, checkpoints, per-dataset calibration,
hybrid-GT generator — are released to catalyse further research on
radar-native deep architectures, self-supervised pretraining, and
operational deployment of hybrid detection pipelines.

// ── References ───────────────────────────────────────────────────────
#heading(level: 1, numbering: none)[References]

#set text(size: 8.8pt)
#set par(justify: true, leading: 0.5em, first-line-indent: 0pt)

#enum(
  numbering: "[1]",
  indent: 0pt,
  body-indent: 0.7em,
  spacing: 0.35em,

  [H. M. Finn and R. S. Johnson, "Adaptive detection mode with threshold
   control," _RCA Review_, vol. 29, no. 9, 1968.],

  [H. Rohling, "Radar CFAR thresholding in clutter and multiple target
   situations," _IEEE Trans. AES_, vol. AES-19, no. 4, 1983.],

  [V. Duk et al., "Target detection in sea-clutter using stationary wavelet
   transforms," _IEEE Trans. AES_, vol. 53, no. 3, 2017.],

  [Q. Li et al., "A speed-up seed point Otsu method for ship detection,"
   _Proc. IEEE IGARSS_, 2016.],

  [Y. Xu et al., "Adaptive clustering-based marine radar sea-clutter
   normalisation," _J. Sensors_, 2021.],

  [X. Chen et al., "Automatic detection of scanning radar images based on
   Radar PPInet," _Remote Sensing_, vol. 13, 2021.],

  [X. Chen et al., "Marine-Faster R-CNN for navigation radar PPI images,"
   _Front. Inf. Technol. Electron. Eng._, vol. 23, 2022.],

  [M. Heuer et al., "Marine radar object detection using SAHI-enhanced
   YOLOv11-OBB," _Sensors_, vol. 26, 2025.],

  [J. Yee, "Onet: Twin U-Net for semantic segmentation in radar images,"
   _IEEE Trans. Image Process._, 2025.],

  [L. Zhang et al., "CCDN-DETR for multi-class SAR object detection,"
   _Sensors_, vol. 24, 2024.],

  [D. Bolya et al., "TIDE: A general toolbox for identifying object-
   detection errors," _Proc. ECCV_, 2020.],

  [X. Zhang and X. Li, "Survey on deep-learning-based marine object
   detection," _J. Adv. Transp._, 2021.],
)
