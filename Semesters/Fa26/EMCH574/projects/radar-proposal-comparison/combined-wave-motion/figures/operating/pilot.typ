// Pilot operating run: wave input, platform pitch, link margin and mapping
// error on a common 0-40 s time base. Standalone figure, 6.5 in wide, four
// time-aligned rows. The figure caption is supplied by the parent manuscript.

#import "@preview/lilaq:0.6.0" as lq

// ---------------------------------------------------------------------------
// Editable settings
// ---------------------------------------------------------------------------
// The data path can be overridden for QA with
//   typst compile --root . --input data=/qa/<fixture>.json ...
#let data-path = sys.inputs.at("data", default: "../../data/experiment-results.json")

#let fig-width = 6.5in
#let panel-width = 5.7in     // data-area width shared by all rows
#let panel-height = 0.92in   // data-area height of each row
#let row-gap = 0.07in
#let base-size = 9pt

#let t-min = 0
#let t-max = 40
#let t-step = 5
#let tolerance = 0.50        // horizontal mapping tolerance (m)

// Fraction of each two-series panel kept free above the data for the legend.
#let legend-headroom = 0.42

// Lilaq default colour cycle (petroff10), first entries.
#let c-blue = rgb("#3f90da")
#let c-orange = rgb("#ffa90e")
#let c-red = rgb("#bd1f01")
#let c-purple = rgb("#832db6")

#let line-w = 0.8pt
#let mark-size = 3.4pt

// ---------------------------------------------------------------------------
// Page and text
// ---------------------------------------------------------------------------
#set page(width: fig-width, height: auto, margin: (x: 0.04in, y: 0.04in), fill: white)
#set text(font: "New Computer Modern", size: base-size, fill: black)
#show math.equation: set text(font: "New Computer Modern Math")

// ---------------------------------------------------------------------------
// Data
// ---------------------------------------------------------------------------
#let d = json(data-path)
#let cont = d.pilot.continuous
#let trace = d.pilot.trace

#let case-midpoint = 0
#let case-per-spoke = 1

// Keep only (x, y) pairs where both values exist; returns (xs, ys).
#let pairs(xs, ys) = {
  let p = xs.zip(ys).filter(q => q.at(0) != none and q.at(1) != none)
  (p.map(q => q.at(0)), p.map(q => q.at(1)))
}

#let deg(v) = if v == none { none } else { v * 180 / calc.pi }

#let (wave-t, wave-y) = pairs(cont.t, cont.wave)
#let (pitch-t, pitch-y) = pairs(cont.t, cont.pitch.map(deg))

#let (mm-t, mm-y) = pairs(cont.t, cont.margin_motion)
#let (ml-t, ml-y) = pairs(cont.t, cont.margin_level)
#let (vm-t, vm-y) = pairs(trace.t, trace.margin_motion)
#let (vl-t, vl-y) = pairs(trace.t, trace.margin_level)

// Mapping error at visits with acquired == true only.
#let acquired-errors(case) = {
  let err = trace.errors.at(case)
  let acq = trace.acquired.at(case)
  let keep = range(calc.min(trace.t.len(), err.len(), acq.len())).filter(
    i => acq.at(i) == true and trace.t.at(i) != none and err.at(i) != none,
  )
  (keep.map(i => trace.t.at(i)), keep.map(i => err.at(i)))
}
#let (em-t, em-y) = acquired-errors(case-midpoint)
#let (es-t, es-y) = acquired-errors(case-per-spoke)

// ---------------------------------------------------------------------------
// Axis limits fitted to the data
// ---------------------------------------------------------------------------
// Margin row: always include the 0 dB threshold; reserve headroom for legend.
#let margin-all = mm-y + ml-y + vm-y + vl-y
#let margin-lo = calc.min(0, ..margin-all)
#let margin-hi = calc.max(0, ..margin-all)
#let margin-span = calc.max(margin-hi - margin-lo, 1)
#let margin-ylim = (
  margin-lo - 0.06 * margin-span,
  margin-hi + margin-span * legend-headroom / (1 - legend-headroom),
)

// Error row: lower bound below zero so zero-error marks stay fully visible;
// always include the tolerance line; reserve headroom for legend.
#let err-hi = calc.max(tolerance, ..em-y, ..es-y)
#let err-lo = calc.min(0, ..em-y, ..es-y)
#let err-span = err-hi - err-lo
#let err-ylim = (
  err-lo - 0.07 * err-span,
  err-hi + err-span * legend-headroom / (1 - legend-headroom),
)

// ---------------------------------------------------------------------------
// Shared time axis: ticks on every row, tick labels and label on the bottom.
// ---------------------------------------------------------------------------
#let tick-pos = range(t-min, t-max + 1, step: t-step)
#let xaxis-inner = (ticks: tick-pos.map(t => (t, [])), subticks: none)
#let xaxis-bottom = (ticks: tick-pos.map(t => (t, [#t])), subticks: none)

#let row(ylabel, bottom: false, ..args) = lq.diagram(
  width: panel-width,
  height: panel-height,
  xlim: (t-min, t-max),
  xaxis: if bottom { xaxis-bottom } else { xaxis-inner },
  xlabel: if bottom { [Time (s)] } else { none },
  ylabel: ylabel,
  ..args,
)

// Continuous line; empty series are skipped rather than drawn.
#let series(xs, ys, color, dash: none, label: none) = if xs.len() > 0 {
  (
    lq.plot(
      xs, ys,
      color: color,
      stroke: (paint: color, thickness: line-w, dash: dash),
      mark: none,
      label: label,
    ),
  )
} else { () }

#let marks(xs, ys, color, mark, label: none) = if xs.len() > 0 {
  (
    lq.plot(
      xs, ys,
      color: color,
      stroke: none,
      mark: mark,
      mark-size: mark-size,
      label: label,
    ),
  )
} else { () }

#let ref-line(y, dash) = lq.hlines(
  y,
  stroke: (paint: black, thickness: 0.6pt, dash: dash),
)

// ---------------------------------------------------------------------------
// Rows
// ---------------------------------------------------------------------------
#let row-wave = row(
  [Wave elevation \ (m)],
  ..series(wave-t, wave-y, black),
)

#let row-pitch = row(
  [Pitch \ (deg)],
  ..series(pitch-t, pitch-y, black),
)

#let row-margin = row(
  [Link margin \ (dB)],
  ylim: margin-ylim,
  legend: (position: top + right),
  ref-line(0, "densely-dashed"),
  ..series(mm-t, mm-y, c-blue, label: [Body-fixed]),
  ..series(ml-t, ml-y, c-orange, dash: "dashed", label: [Stabilized]),
  ..marks(vm-t, vm-y, c-blue, "o"),
  ..marks(vl-t, vl-y, c-orange, "s"),
)

#let row-error = row(
  [Horiz. mapping \ error (m)],
  bottom: true,
  ylim: err-ylim,
  // Top left: no acquired marks before ~13 s, so nothing is obscured there.
  legend: (position: top + left),
  ref-line(tolerance, "dotted"),
  ..marks(em-t, em-y, c-red, "o", label: [Midpoint]),
  ..marks(es-t, es-y, c-purple, "x", label: [Per-spoke]),
)

// Each diagram is laid out by its data area only (bounds: "data-area"), so the
// y-tick and y-label widths no longer shift a row. Every data area is then
// right-aligned in the common page width with the same right inset (room for
// the overhanging last x tick label), so all four data-area edges and x grid
// lines line up exactly. The y labels and ticks overhang into the left margin.
#let right-inset = 0.06in
#let placed(d) = align(right, pad(right: right-inset, block(width: panel-width, height: panel-height, d)))

#show: lq.set-diagram(bounds: "data-area")

#grid(
  columns: (100%,),
  row-gutter: row-gap,
  // Room above for the half-overhanging top y tick label.
  pad(top: 0.05in, placed(row-wave)),
  placed(row-pitch),
  placed(row-margin),
  // The bottom row's labels below the data area need vertical room.
  pad(bottom: 0.36in, placed(row-error)),
)
