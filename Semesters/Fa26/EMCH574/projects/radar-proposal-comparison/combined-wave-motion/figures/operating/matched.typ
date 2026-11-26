// Matched-pitch acquisition results (case 1: per-spoke correction, moving antenna).
// Standalone figure, 6.5 in wide, 2 rows x 3 columns.
//   Columns: scan period.
//   Row 1:   per-spoke usable fraction (%), both pitch phases, plus the
//            static beam-only estimate as a dotted reference.
//   Row 2:   realization-level 95th-percentile longest run of consecutive
//            unusable visits, both pitch phases.
// The figure caption (including the full metric definitions) is supplied by
// the parent manuscript.

#import "@preview/lilaq:0.6.0" as lq

// ---------------------------------------------------------------------------
// Editable settings
// ---------------------------------------------------------------------------
// The data path can be overridden for QA builds with
//   typst compile --root . --input data=/qa/<mock>.json ...
#let data-path = sys.inputs.at("data", default: "../../data/experiment-results.json")

#let case-index = 1              // 0 scan-midpoint, 1 per-spoke moving, 2 ideal level
#let f-natural-hz = 0.35         // x = frequency_hz / f-natural-hz
#let scan-periods = (1.25, 2.5, 3.75)
#let phases = (0.0, calc.pi / 2)
#let tol = 1e-3                  // matching tolerance for scan_s and pitch_phase_rad

#let fig-width = 6.5in
#let panel-width = 1.78in        // data-area width of each panel
#let panel-height = 1.35in       // data-area height of each panel
#let col-gutter = 0.12in
#let row-gutter = 0.10in
#let base-size = 9pt

#let x-lim = (0.52, 1.25)
#let x-ticks = (0.6, 0.8, 1.0, 1.2)
#let y-pad = 0.04               // fraction of the data span added at each y end

#let x-label = [Encounter frequency ratio, $omega_e \/ omega_n$]
#let frac-label = [Usable visits (%)]
#let run-label = [Longest outage, \ 95th pct. (visits)]
#let phase-labels = ([0°], [90°])
#let beam-label = [Beam only]
#let caption(i, scan) = [(#"abc".at(i)) Scan period #str(scan) s]

// Legend: shown only in the top-left panel; move it here if it obstructs data.
#let legend-pos = bottom + right

// Series styles. Colors come from the default Lilaq cycle (not overridden);
// dash pattern and marker shape keep the series distinct in grayscale.
#let phase-styles = (
  (stroke: (thickness: 1pt), mark: "o", mark-size: 4pt),
  (stroke: (thickness: 1pt, dash: "dashed"), mark: "s", mark-size: 3.6pt),
)
#let beam-style = (stroke: (thickness: 1pt, dash: "dotted"), mark: "x", mark-size: 4.5pt)

// ---------------------------------------------------------------------------
// Page and text
// ---------------------------------------------------------------------------
#set page(width: fig-width, height: auto, margin: (x: 0.04in, y: 0.04in), fill: white)
#set text(font: "New Computer Modern", size: base-size, fill: black)
#show math.equation: set text(font: "New Computer Modern Math")

// ---------------------------------------------------------------------------
// Data
// ---------------------------------------------------------------------------
#let records = json(data-path).at("matched_pitch")

#let near(a, b) = calc.abs(float(a) - float(b)) < tol

// Records for one (scan period, phase) pair, sorted by frequency.
#let select(scan, phase) = {
  let rs = records.filter(r => near(r.scan_s, scan) and near(r.pitch_phase_rad, phase))
  rs = rs.sorted(key: r => float(r.frequency_hz))
  assert(
    rs.len() > 0,
    message: "matched_pitch: no records for scan_s = " + str(scan)
      + ", pitch_phase_rad = " + str(phase),
  )
  rs
}

#let xs(rs) = rs.map(r => float(r.frequency_hz) / f-natural-hz)
#let frac-pct(rs) = rs.map(r => 100 * float(r.fraction.at(case-index)))
// Static beam-only estimate depends on peak pitch only; taken from the
// phase-0 records of each scan period.
#let beam-pct(rs) = rs.map(r => 100 * float(r.static_beam_only_fraction))
#let run-p95(rs) = rs.map(r => float(r.maxrun_p95.at(case-index)))

#let sets = scan-periods.map(s => phases.map(p => select(s, p)))

// Common row-wise y limits.
#let all-frac = sets.map(per-scan => (
  ..per-scan.map(frac-pct).flatten(),
  ..beam-pct(per-scan.at(0)),
)).flatten()
#let all-run = sets.map(per-scan => per-scan.map(run-p95).flatten()).flatten()

// Limits are padded past the physical bounds (0 %, 100 %, 0 visits) so
// markers sitting on a bound are not clipped; ticks stay within the bounds.
#let padded(lo, hi, frac: y-pad) = {
  let span = if hi - lo > 0 { hi - lo } else { 1.0 }
  (lo - frac * span, hi + frac * span)
}
#let frac-lim = padded(
  calc.max(calc.min(..all-frac), 0.0),
  calc.min(calc.max(..all-frac), 100.0),
)
#let run-lim = padded(0.0, calc.max(calc.max(..all-run), 1.0))

// Multiples of `step` inside [lo, hi] intersected with [floor, ceil].
#let ticks-in(lim, step, floor, ceil) = {
  let lo = calc.max(lim.at(0), floor)
  let hi = calc.min(lim.at(1), ceil)
  range(int(calc.ceil(lo / step)), int(calc.floor(hi / step)) + 1).map(i => i * step)
}
#let frac-ticks = ticks-in(frac-lim, 20, 0, 100)
// Integer run ticks: smallest "nice" step giving at most 5 intervals.
#let run-step = {
  let hi = run-lim.at(1)
  let steps = (1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000)
  steps.find(s => hi / s <= 5)
}
#let run-ticks = ticks-in(run-lim, run-step, 0, calc.inf)

// ---------------------------------------------------------------------------
// Panels
// ---------------------------------------------------------------------------
#let axes(first-col, bottom-row, y-ticks) = (
  xlim: x-lim,
  xaxis: if bottom-row { (ticks: x-ticks, subticks: none) } else {
    (ticks: x-ticks, subticks: none, format-ticks: none)
  },
  yaxis: if first-col { (ticks: y-ticks) } else { (ticks: y-ticks, format-ticks: none) },
)

#let frac-panel(j) = {
  let per-scan = sets.at(j)
  let first = j == 0
  let rs0 = per-scan.at(0)
  lq.diagram(
    width: panel-width,
    height: panel-height,
    ylim: frac-lim,
    ylabel: if first { frac-label },
    legend: (position: legend-pos),
    ..axes(first, false, frac-ticks),
    ..range(phases.len()).map(k => lq.plot(
      xs(per-scan.at(k)),
      frac-pct(per-scan.at(k)),
      label: if first { phase-labels.at(k) },
      ..phase-styles.at(k),
    )),
    lq.plot(xs(rs0), beam-pct(rs0), label: if first { beam-label }, ..beam-style),
  )
}

#let run-panel(j) = {
  let per-scan = sets.at(j)
  let first = j == 0
  lq.diagram(
    width: panel-width,
    height: panel-height,
    ylim: run-lim,
    ylabel: if first { run-label },
    xlabel: if j == 1 { x-label },
    ..axes(first, true, run-ticks),
    ..range(phases.len()).map(k => lq.plot(
      xs(per-scan.at(k)),
      run-p95(per-scan.at(k)),
      ..phase-styles.at(k),
    )),
  )
}

// lq.layout aligns the data areas of all diagrams in the grid regardless of
// tick-label overhang; captions are boxed to the data-area width so they
// center on it.
#let n = scan-periods.len()
#show: lq.layout
#align(center, grid(
  columns: n,
  column-gutter: col-gutter,
  row-gutter: row-gutter,
  align: right + top,
  ..range(n).map(frac-panel),
  ..range(n).map(run-panel),
  ..range(n).map(j => box(width: panel-width, align(center, caption(j, scan-periods.at(j))))),
))
