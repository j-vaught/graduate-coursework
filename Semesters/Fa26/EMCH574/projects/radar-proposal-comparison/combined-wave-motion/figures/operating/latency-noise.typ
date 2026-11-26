// Pose-age sensitivity of the leveling/timing interaction under imposed
// observation noise (0.25 m range, 0.25 deg bearing, Gaussian).
// Standalone figure, 6.5 in wide, two side-by-side panels:
//   (a) selected cell: marginal leveling gains with the aged pose and with
//       the true spoke-time pose, and their interaction (after minus first)
//       with conditional phase-paired 95 % intervals;
//   (b) interaction across all study-grid cells by pose age: median and
//       10th-90th percentile range (linear interpolation), with the selected
//       cell overlaid.
// The exact-input benchmark in caption (a) is read from the factorial CSV.
// The figure caption is supplied by the parent manuscript.

#import "@preview/lilaq:0.6.0" as lq

// ---------------------------------------------------------------------------
// Editable settings
// ---------------------------------------------------------------------------
#let grid-path = "../../data/latency_noise_grid.csv"
#let factorial-path = "../../data/pointing_registration_factorial.csv"

#let sel-freq = 0.36125   // Hz
#let sel-amp = 0.376      // m
#let tol = 1e-6
#let ages-ms = (0, 50, 100, 200, 625)
#let cells-per-age = 111
#let q-lo = 0.10
#let q-hi = 0.90

#let fig-width = 6.5in
#let panel-width = 2.4in    // data-area width of each panel
#let panel-height = 2.1in   // data-area height of each panel
#let col-gutter = 0.3in
#let base-size = 10pt
#let tick-size = 8pt        // keeps the 0/50/100 ms labels apart on a linear axis

// Default Lilaq cycle colors, taken explicitly so that the selected
// interaction keeps the same identity in both panels.
#let palette = lq.color.map.petroff10
#let line-stroke(..args) = stroke(thickness: 1.2pt, join: "miter", ..args)
#let first-style = (
  color: palette.at(0),
  stroke: line-stroke(paint: palette.at(0)),
  mark: "o", mark-size: 5pt,
)
#let after-style = (
  color: palette.at(1),
  stroke: line-stroke(paint: palette.at(1), dash: "dashed"),
  mark: "s", mark-size: 4pt,
)
#let inter-style = (
  color: palette.at(2),
  stroke: line-stroke(paint: palette.at(2), dash: "dash-dotted"),
  mark: "^", mark-size: 5.5pt,
)
#let median-style = (
  color: black,
  stroke: line-stroke(paint: black),
  mark: "d", mark-size: 5pt, mark-color: white,
)
#let band-fill = luma(205)
#let interval-stroke = 0.6pt + black

#let x-label = [Pose age (ms)]
#let x-ticks = ages-ms
#let x-lim = (-15, 640)

#let y-lim = (-6.4, 6.4)          // shared by both panels
#let y-ticks = (-6, -4, -2, 0, 2, 4, 6)
#let gain-label-a = [Usable-visit gain \ (percentage points)]
#let gain-label-b = [Interaction \ (percentage points)]

// ---------------------------------------------------------------------------
// Page and text
// ---------------------------------------------------------------------------
#set page(width: fig-width, height: auto, margin: (x: 0.04in, y: 0.04in), fill: white)
#set text(font: "New Computer Modern", size: base-size, fill: black)
#show math.equation: set text(font: "New Computer Modern Math")
#show: lq.set-errorbar(stroke: interval-stroke)
#show: lq.set-legend(radius: 0pt)
#show lq.selector(lq.tick-label): set text(size: tick-size)
#show lq.selector(lq.legend): set text(size: tick-size)

// ---------------------------------------------------------------------------
// Data
// ---------------------------------------------------------------------------
#let near(a, b) = calc.abs(a - b) < tol
#let age-ms(r) = {
  let a = 1000 * float(r.pose_age_s)
  assert(near(a, calc.round(a)), message: "latency_noise_grid: non-integer ms age")
  int(calc.round(a))
}
#let fnum(r, name) = float(r.at(name))

#let rows = csv(grid-path, row-type: dictionary)
#assert(rows.len() == ages-ms.len() * cells-per-age, message: "latency_noise_grid: unexpected row count")

// Selected cell, sorted by pose age.
#let sel = (
  rows
    .filter(r => near(float(r.frequency_hz), sel-freq) and near(float(r.amplitude_m), sel-amp))
    .sorted(key: age-ms)
)
#assert(sel.map(age-ms) == ages-ms, message: "latency_noise_grid: selected cell ages")
#let sel-x = sel.map(age-ms)
#let sel-first = sel.map(r => fnum(r, "hardware_first_gain_pp"))
#let sel-after = sel.map(r => fnum(r, "hardware_after_timing_gain_pp"))
#let sel-inter = sel.map(r => fnum(r, "interaction_pp"))
#let sel-hw = sel.map(r => fnum(r, "interaction_phase_interval_halfwidth_pp"))

// Exact-input benchmark (factorial grid row of the same cell).
#let bench = csv(factorial-path, row-type: dictionary).filter(r => (
  r.case == "grid" and near(float(r.frequency_hz), sel-freq) and near(float(r.amplitude_m), sel-amp)
))
#assert(bench.len() == 1, message: "pointing_registration_factorial: benchmark row")
#let bench-inter = float(bench.first().interaction_pp)

// Linear-interpolation quantile (Hyndman-Fan type 7).
#let quantile(v, p) = {
  let s = v.sorted()
  let h = (s.len() - 1) * p
  let i = calc.floor(h)
  if i + 1 >= s.len() { s.last() } else { s.at(i) + (h - i) * (s.at(i + 1) - s.at(i)) }
}
#let dist = ages-ms.map(a => {
  let v = rows.filter(r => age-ms(r) == a).map(r => fnum(r, "interaction_pp"))
  assert(v.len() == cells-per-age, message: "latency_noise_grid: cells at age " + str(a))
  (lo: quantile(v, q-lo), med: quantile(v, 0.5), hi: quantile(v, q-hi))
})

// Guard against clipping in the shared y-range.
#let all-y = sel-first + sel-after + sel-inter.zip(sel-hw).map(((y, e)) => y - e) + sel-inter.zip(sel-hw).map(((y, e)) => y + e) + dist.map(d => d.lo) + dist.map(d => d.hi)
#assert(all-y.all(y => y > y-lim.at(0) and y < y-lim.at(1)), message: "y-range clips data")

// ---------------------------------------------------------------------------
// Panels
// ---------------------------------------------------------------------------
#let fmt(x) = {
  let s = str(calc.round(x, digits: 2))
  if s.starts-with("-") { "−" + s.slice(1) } else { s }
}

#let base-diagram(..children, ylabel: none, legend: none) = lq.diagram(
  width: panel-width,
  height: panel-height,
  xlabel: x-label,
  ylabel: ylabel,
  xlim: x-lim,
  ylim: y-lim,
  xaxis: (ticks: x-ticks, subticks: none),
  yaxis: (ticks: y-ticks, subticks: none),
  legend: legend,
  lq.line((x-lim.at(0), 0), (x-lim.at(1), 0), stroke: 0.4pt + luma(120), z-index: 0),
  ..children,
)

// Interval bars on the selected interaction; zero-width (age 0) skipped.
#let k = range(sel.len()).filter(j => sel-hw.at(j) > 0)
#let inter-bars = lq.plot(
  k.map(j => sel-x.at(j)), k.map(j => sel-inter.at(j)),
  yerr: k.map(j => sel-hw.at(j)),
  color: black, stroke: none, mark: none, z-index: 3,
)

#let panel-a = base-diagram(
  ylabel: gain-label-a,
  legend: (position: top + left),
  lq.plot(sel-x, sel-first, label: [Leveling first], ..first-style),
  lq.plot(sel-x, sel-after, label: [Leveling second], ..after-style),
  lq.plot(sel-x, sel-inter, label: [Interaction], ..inter-style),
  inter-bars,
)

#let panel-b = base-diagram(
  ylabel: gain-label-b,
  legend: (position: top + left),
  lq.fill-between(ages-ms, dist.map(d => d.lo), y2: dist.map(d => d.hi),
    fill: band-fill, stroke: none, label: [10th–90th pct.]),
  lq.plot(ages-ms, dist.map(d => d.med), label: [Median], ..median-style),
  lq.plot(sel-x, sel-inter, label: [Selected cell], ..inter-style),
)

#let caption-a = [(a) Selected cell, #sel-freq Hz, #sel-amp m \
  #text(size: 0.9em)[Exact input, 625 ms: interaction #fmt(bench-inter)~pp]]
#let caption-b = [(b) Interaction across #cells-per-age grid cells]

#show: lq.layout
#align(center, grid(
  columns: 2,
  column-gutter: col-gutter,
  row-gutter: 0.6em,
  align: right + top,
  panel-a, panel-b,
  box(width: panel-width, align(center, caption-a)),
  box(width: panel-width, align(center, caption-b)),
))
