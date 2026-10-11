#import "@preview/cetz:0.4.2" as cetz
#import "@preview/lilaq:0.6.0" as lq
#let ink = rgb("#17324D")
#let teal = rgb("#0B6E75")
#let pale = rgb("#EAF3F3")
#let slate = rgb("#5B6573")
#let ochre = rgb("#9A5B00")
#let arrow = (end: "stealth", fill: ink, stroke: ink)
#let line-colors = (rgb("#1f77b4"), rgb("#ff7f0e"), rgb("#2ca02c"), rgb("#d62728"), rgb("#9467bd"))
#let node(a, b, body, fill: pale, stroke: 0.8pt + ink) = {
  import cetz.draw: rect, content
  rect(a, b, fill: fill, stroke: stroke)
  content(((a.at(0) + b.at(0))/2, (a.at(1) + b.at(1))/2), body)
}
#let plot-panel(title, xlabel, ylabel, series, xlim: auto, ylim: auto, height: 2.35in, width: 100%, legend: top + right, aspect-ratio: none) = {
  set text(font: "Times New Roman", size: 9pt)
  lq.diagram(width: width, height: height, title: title, xlabel: xlabel, ylabel: ylabel,
    xlim: xlim, ylim: ylim, aspect-ratio: aspect-ratio, grid: (stroke: 0.3pt + luma(83%)),
    legend: (radius: 0pt, fill: white, position: legend),
    ..series.enumerate().map(pair => {
      let s = pair.last()
      lq.plot(s.x, s.y, label: s.label, mark: none,
        color: line-colors.at(calc.rem(pair.first(), line-colors.len())),
        step: s.at("step", default: none),
        stroke: (thickness: s.at("thickness", default: 1.15pt), dash: s.at("dash", default: "solid")))
    }))
}
#let data-table(columns, ..cells) = {
  let values = cells.pos()
  let n = if type(columns) == array { columns.len() } else { columns }
  table(columns: columns, inset: (x: 6pt, y: 5pt), stroke: 0.35pt + luma(75%),
    table.header(..values.slice(0, n)), ..values.slice(n))
}
#let note(body) = block(width: 100%, fill: pale, stroke: (left: 2pt + teal),
  inset: 9pt, radius: 0pt, body)
