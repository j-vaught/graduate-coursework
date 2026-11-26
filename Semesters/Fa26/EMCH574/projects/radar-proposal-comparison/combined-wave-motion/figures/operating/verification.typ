// Forced-response verification: numerical vs. analytical pitch response.
// Standalone figure, 6.5 in wide, two side-by-side panels (amplitude, phase).
// The figure caption is supplied by the parent manuscript.

#import "@preview/lilaq:0.6.0" as lq

// ---------------------------------------------------------------------------
// Editable settings
// ---------------------------------------------------------------------------
#let data-path = "../../data/verification_forced_response.csv"

#let fig-width = 6.5in
#let panel-width = 2.45in   // data-area width of each panel
#let panel-height = 1.75in  // data-area height of each panel
#let base-size = 9pt

#let analytic-label = [Analytical]
#let numeric-label = [Numerical]
#let x-label = [Encounter frequency ratio, $omega_e \/ omega_n$]
#let amp-label = [Pitch amplitude (deg)]
#let phase-label = [Pitch phase lag (deg)]
#let caption-a = [(a) Pitch amplitude]
#let caption-b = [(b) Pitch phase lag]

// Analytical curve: first Lilaq cycle color, solid line, no markers.
// Numerical samples: black crosses, no connecting line.
#let analytic-style = (stroke: 1pt, mark: none)
#let numeric-style = (color: black, stroke: none, mark: "x", mark-size: 5pt)

// ---------------------------------------------------------------------------
// Page and text
// ---------------------------------------------------------------------------
#set page(width: fig-width, height: auto, margin: (x: 0.04in, y: 0.04in), fill: white)
#set text(font: "New Computer Modern", size: base-size, fill: black)
#show math.equation: set text(font: "New Computer Modern Math")

// ---------------------------------------------------------------------------
// Data
// ---------------------------------------------------------------------------
#let rows = csv(data-path, row-type: dictionary)
#let col(name) = rows.map(r => float(r.at(name)))

#let ratio = col("ratio")
#let amp-num = col("numerical_amp_deg")
#let amp-ana = col("analytical_amp_deg")
#let phase-num = col("numerical_phase_deg")
#let phase-ana = col("analytical_phase_deg")

// ---------------------------------------------------------------------------
// Panels
// ---------------------------------------------------------------------------
#let panel(ylabel, y-ana, y-num, legend-pos) = lq.diagram(
  width: panel-width,
  height: panel-height,
  xlabel: x-label,
  ylabel: ylabel,
  legend: (position: legend-pos),
  lq.plot(ratio, y-ana, label: analytic-label, ..analytic-style),
  lq.plot(ratio, y-num, label: numeric-label, ..numeric-style),
)

#let captioned(body, caption) = stack(
  dir: ttb,
  spacing: 0.6em,
  body,
  align(center, caption),
)

#grid(
  columns: (1fr, 1fr),
  column-gutter: 0.15in,
  align: center + top,
  captioned(panel(amp-label, amp-ana, amp-num, top + right), caption-a),
  captioned(panel(phase-label, phase-ana, phase-num, top + left), caption-b),
)
