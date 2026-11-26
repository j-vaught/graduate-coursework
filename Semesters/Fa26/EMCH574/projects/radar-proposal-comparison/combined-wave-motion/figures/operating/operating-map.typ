// Operating map: fraction for each pose case and the two paired gains,
// over encounter frequency ratio and wave amplitude.
// Standalone figure, 6.5 in wide, 3 x 2 panel grid; the sixth cell holds the
// three horizontal colorbars. The figure caption is supplied by the manuscript.

#import "@preview/lilaq:0.6.0" as lq

// ---------------------------------------------------------------------------
// Editable settings
// ---------------------------------------------------------------------------
#let data-path = "../../data/experiment-results.json"

// Natural frequency and validity limits (k a, peak pitch) are read from
// metadata.assumptions in the data file; see the Data section.

#let fig-width = 6.5in
#let panel-width = 1.55in    // data-area width of each map
#let panel-height = 1.15in   // data-area height of each map
#let base-size = 9pt
#let colorbar-length = 1.55in
#let colorbar-thickness = 2mm
#let colorbar-spacing = 0.03in

// Panels carry only the ratio; the full label is stated once below the grid.
#let x-label = [$omega_e \/ omega_n$]
#let x-label-full = [Horizontal axes: encounter frequency ratio, $omega_e \/ omega_n$.]
#let y-label = [Wave amplitude (m)]
#let frac-cbar-label = [Usable visits (%)]
#let corr-cbar-label = [Correction gain (pp)]
#let stab-cbar-label = [Stabilization gain (pp)]

#let captions = (
  [(a) Scan-midpoint pose],
  [(b) Per-spoke pose],
  [(c) Level antenna + per-spoke],
  [(d) Correction gain],
  [(e) Stabilization gain],
)

#let show-footnote = true
#let footnote-text = [Gray cells fall outside the modeled wave or attitude range.]

// Axes background shows through omitted (NaN) cells.
#let missing-fill = rgb("#A2A2A2")

// Fractions: Lilaq default viridis, common 0-100 % scale.
#let frac-map = color.map.viridis
// Gains: blue-orange diverging map, white near zero; each gain has its own
// symmetric domain.
// Uses the stock color.map.vik when this Typst version provides it,
// otherwise an equivalent blue-white-orange ramp.
#let gain-map = if "vik" in dictionary(color.map) { color.map.vik } else {
  (
    rgb("#001261"), rgb("#3E7FB5"), white, rgb("#E08A3C"), rgb("#6B2A00"),
  )
}

// ---------------------------------------------------------------------------
// Page and text
// ---------------------------------------------------------------------------
#set page(width: fig-width, height: auto, margin: (x: 0.04in, y: 0.04in), fill: white)
#set text(font: "New Computer Modern", size: base-size, fill: black)
#show math.equation: set text(font: "New Computer Modern Math")

// ---------------------------------------------------------------------------
// Data
// ---------------------------------------------------------------------------
#let data = json(data-path)
#let records = data.at("operating_map")

// Modeled validity limits, read from the recorded assumptions.
#let assumptions = data.metadata.assumptions
#let f-natural = float(assumptions.natural_frequency_hz)   // Hz; x = frequency_hz / f-natural
#let ka-max = float(assumptions.max_regular_steepness)     // regular-wave steepness limit
#let pitch-max = float(assumptions.max_angle_deg)          // peak pitch limit (deg)

#let key(v) = calc.round(float(v), digits: 9)
#let x-of(r) = key(float(r.frequency_hz) / f-natural)
#let y-of(r) = key(r.amplitude_m)
#let included(r) = (
  r.steepness != none and float(r.steepness) <= ka-max
    and r.peak_pitch_deg != none and float(r.peak_pitch_deg) <= pitch-max
)

// Sorted unique cell centres. ys ascends, so row 0 of every z array is the
// lowest amplitude and is drawn at the bottom of the data area.
#let xs = records.map(x-of).dedup().sorted()
#let ys = records.map(y-of).dedup().sorted()

// Lookup "i,j" -> record, i indexing ys (rows) and j indexing xs (columns).
#let cells = {
  let d = (:)
  for r in records {
    let i = ys.position(v => v == y-of(r))
    let j = xs.position(v => v == x-of(r))
    d.insert(str(i) + "," + str(j), r)
  }
  d
}

#let pct(v) = if v == none { float.nan } else { 100.0 * float(v) }

// z has shape (ys.len(), xs.len()) as Lilaq colormesh expects; omitted or
// absent cells are NaN and render transparent.
#let mesh-values(getter) = range(ys.len()).map(i => range(xs.len()).map(j => {
  let r = cells.at(str(i) + "," + str(j), default: none)
  if r == none or not included(r) { float.nan } else { pct(getter(r)) }
}))

#let getters = (
  r => r.fraction.at(0),
  r => r.fraction.at(1),
  r => r.fraction.at(2),
  r => r.correction_gain,
  r => r.stabilization_gain,
)
#let z = getters.map(mesh-values)

// Gain colour domains: observed symmetric extent of each gain over plotted
// cells, rounded up to a multiple of `step` and never below `step`.
// Correction uses 5 pp steps, stabilization 0.5 pp steps.
#let gain-peak(values) = {
  let a = values.flatten().filter(v => not float.is-nan(v)).map(calc.abs)
  if a.len() == 0 { 0.0 } else { calc.max(..a) }
}
#let sym-lim(values, step) = calc.max(
  step, step * calc.ceil(gain-peak(values) / step - 1e-9),
)
#let corr-lim = sym-lim(z.at(3), 5)
#let stab-lim = sym-lim(z.at(4), 0.5)

// Axis limits at the outer cell edges, so no margin strip appears.
#let edges(c) = if c.len() < 2 { auto } else {
  (c.first() - (c.at(1) - c.first()) / 2, c.last() + (c.last() - c.at(-2)) / 2)
}

// ---------------------------------------------------------------------------
// Panels
// ---------------------------------------------------------------------------
#let frac-mesh(values) = lq.colormesh(
  xs, ys, values,
  map: frac-map, min: 0, max: 100,
  interpolation: "pixelated",
)
#let gain-mesh(values, lim) = lq.colormesh(
  xs, ys, values,
  map: gain-map, min: -lim, max: lim,
  interpolation: "pixelated",
)

#let panel(mesh, show-ylabel) = lq.diagram(
  width: panel-width,
  height: panel-height,
  xlim: edges(xs),
  ylim: edges(ys),
  xlabel: x-label,
  ylabel: if show-ylabel { y-label } else { none },
  grid: none,
  fill: missing-fill,
  xaxis: (subticks: none),
  yaxis: (subticks: none),
  mesh,
)

#let captioned(body, caption) = stack(
  dir: ttb,
  spacing: 0.6em,
  body,
  align(center, caption),
)

#let cbar(mesh, label) = lq.colorbar(
  mesh,
  orientation: "horizontal",
  label: label,
  thickness: colorbar-thickness,
  width: colorbar-length,
  xaxis: (subticks: none),
)

#let colorbars = stack(
  dir: ttb,
  spacing: colorbar-spacing,
  cbar(frac-mesh(z.at(0)), frac-cbar-label),
  cbar(gain-mesh(z.at(3), corr-lim), corr-cbar-label),
  cbar(gain-mesh(z.at(4), stab-lim), stab-cbar-label),
)

#grid(
  columns: (1fr, 1fr, 1fr),
  column-gutter: 0.1in,
  row-gutter: 0.14in,
  align: center + top,
  captioned(panel(frac-mesh(z.at(0)), true), captions.at(0)),
  captioned(panel(frac-mesh(z.at(1)), false), captions.at(1)),
  captioned(panel(frac-mesh(z.at(2)), false), captions.at(2)),
  captioned(panel(gain-mesh(z.at(3), corr-lim), true), captions.at(3)),
  captioned(panel(gain-mesh(z.at(4), stab-lim), false), captions.at(4)),
  grid.cell(align: center + horizon, colorbars),
)

#if show-footnote {
  v(0.04in)
  align(left)[#x-label-full \ #footnote-text]
}
