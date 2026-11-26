// Sensitivity to quadratic pitch damping (reference wave and largest-gain cell).
// Standalone figure, 6.5 in wide, two side-by-side panels:
//   (a) peak pitch, (b) per-spoke registration gain with phase-paired 95 %
//   intervals (correction_ci95_halfwidth).
// The figure caption (wave frequencies and amplitudes) is supplied by the
// parent manuscript.

#import "@preview/lilaq:0.6.0" as lq

// ---------------------------------------------------------------------------
// Editable settings
// ---------------------------------------------------------------------------
#let data-path = "../../data/nonlinear_pitch.csv"

// CSV case name, legend label, and series style. Colors come from the default
// Lilaq cycle (not overridden); dash pattern, marker shape, and marker fill
// keep the series distinct in grayscale. The open circle is drawn first and
// larger, so the filled square stays readable inside it where both coincide.
#let line-stroke(..args) = stroke(thickness: 1.2pt, join: "miter", ..args)
#let series = (
  (
    case: "reference",
    label: [Reference wave],
    style: (stroke: line-stroke(), mark: "o", mark-size: 6pt, mark-color: white),
  ),
  (
    case: "maximum_linear_correction",
    label: [Largest linear gain],
    style: (stroke: line-stroke(dash: "dashed"), mark: "s", mark-size: 3.4pt),
  ),
)

#let fig-width = 6.5in
#let panel-width = 2.45in   // data-area width of each panel
#let panel-height = 1.9in   // data-area height of each panel
#let col-gutter = 0.3in
#let interval-stroke = 0.6pt + black  // 95 % interval bars and caps
#let base-size = 10pt

#let x-label = [Quadratic damping ratio, $chi$]
#let x-ticks = ((0, [0]), (0.25, [0.25]), (0.5, [0.50]), (1, [1.00]))
#let x-lim = (-0.06, 1.06)

#let pitch-label = [Peak pitch (deg)]
#let pitch-lim = (0, 9)
#let pitch-ticks = (0, 2, 4, 6, 8)

#let gain-label = [Per-spoke registration gain \ (percentage points)]
#let gain-lim = (-1.4, 26)  // padded below 0 so zero-valued markers are not clipped
#let gain-ticks = (0, 5, 10, 15, 20, 25)

#let caption-a = [(a) Peak pitch]
#let caption-b = [(b) Per-spoke registration gain]
#let legend-pos = top + right  // legend shown in panel (a) only

// ---------------------------------------------------------------------------
// Page and text
// ---------------------------------------------------------------------------
#set page(width: fig-width, height: auto, margin: (x: 0.04in, y: 0.04in), fill: white)
#set text(font: "New Computer Modern", size: base-size, fill: black)
#show math.equation: set text(font: "New Computer Modern Math")
#show: lq.set-errorbar(stroke: interval-stroke)

// ---------------------------------------------------------------------------
// Data
// ---------------------------------------------------------------------------
#let rows = csv(data-path, row-type: dictionary)

// Rows of one case, sorted by damping ratio; checked against the sampled chi.
#let select(case) = {
  let rs = rows.filter(r => r.case == case).sorted(key: r => float(r.quadratic_torque_ratio))
  assert(
    rs.map(r => float(r.quadratic_torque_ratio)) == x-ticks.map(t => float(t.at(0))),
    message: "nonlinear_pitch: unexpected damping ratios for case " + case,
  )
  rs
}
#let col(rs, name, scale: 1) = rs.map(r => scale * float(r.at(name)))

#let data = series.map(s => select(s.case))

// ---------------------------------------------------------------------------
// Panels
// ---------------------------------------------------------------------------
#let chi(rs) = col(rs, "quadratic_torque_ratio")

// 95 % intervals are drawn in black above the markers, since several are
// shorter than a marker; zero-height intervals are skipped.
#let intervals(rs, y, err) = {
  let k = range(rs.len()).filter(j => err.at(j) > 0)
  let pick(v) = k.map(j => v.at(j))
  lq.plot(pick(chi(rs)), pick(y), yerr: pick(err), color: black, stroke: none, mark: none, z-index: 3)
}

#let panel(ylabel, ylim, yticks, y-of, yerr-of: none, legend: none) = lq.diagram(
  width: panel-width,
  height: panel-height,
  xlabel: x-label,
  ylabel: ylabel,
  xlim: x-lim,
  ylim: ylim,
  xaxis: (ticks: x-ticks, subticks: none),
  yaxis: (ticks: yticks),
  legend: legend,
  ..series.zip(data).map(((s, rs)) => lq.plot(chi(rs), y-of(rs), label: s.label, ..s.style)),
  ..if yerr-of != none {
    data
      .filter(rs => yerr-of(rs).any(e => e > 0))
      .map(rs => intervals(rs, y-of(rs), yerr-of(rs)))
  },
)

#let pitch-panel = panel(
  pitch-label, pitch-lim, pitch-ticks,
  rs => col(rs, "peak_pitch_deg"),
  legend: (position: legend-pos, radius: 0pt),
)
#let gain-panel = panel(
  gain-label, gain-lim, gain-ticks,
  rs => col(rs, "correction_gain", scale: 100),
  yerr-of: rs => col(rs, "correction_ci95_halfwidth", scale: 100),
)

// lq.layout aligns the data areas; captions are boxed to the data-area width
// so they center on it.
#show: lq.layout
#align(center, grid(
  columns: 2,
  column-gutter: col-gutter,
  row-gutter: 0.6em,
  align: right + top,
  pitch-panel, gain-panel,
  box(width: panel-width, align(center, caption-a)),
  box(width: panel-width, align(center, caption-b)),
))
