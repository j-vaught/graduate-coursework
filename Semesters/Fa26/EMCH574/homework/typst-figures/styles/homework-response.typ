#import "figure.typ": *

// Numerical data are supplied by Python; Lilaq authors the vector figure.
#let response-figure(data) = {
  let x = data.x
  let span-x = data.xlim.at(1) - data.xlim.at(0)
  let span-y = data.ylim.at(1) - data.ylim.at(0)
  let elements = ()
  if data.band != none {
    elements.push(hlines(
      -data.band, data.band,
      stroke: (paint: color-muted, thickness: 0.65pt, dash: "dotted", cap: "butt"),
    ))
  }
  for (index, curve) in data.curves.enumerate() {
    let stroke = (
      paint: plot-color-cycle.at(calc.rem(index, plot-color-cycle.len())),
      thickness: 1.1pt,
      cap: "butt",
      join: "miter",
    )
    if calc.rem(index, 2) == 1 { stroke.insert("dash", "dashed") }
    elements.push(plot(x, curve.y, stroke: stroke, label: if data.curves.len() > 1 { curve.label } else { none }))
  }
  for (index, event) in data.events.enumerate() {
    let label-x = data.xlim.at(0) + (0.02 + 0.33 * index) * span-x
    let label-y = data.ylim.at(1) - 0.025 * span-y
    elements.push(line(
      (label-x + 0.05 * span-x, label-y - 0.12 * span-y), (event.x, event.y),
      stroke: (paint: color-guide, thickness: 0.5pt, cap: "butt"),
    ))
    elements.push(scatter((event.x,), (event.y,), mark: "s", size: 3.5pt, color: color-ink))
    elements.push(place(label-x, label-y,
      box(fill: white, stroke: (paint: color-grid, thickness: 0.4pt), inset: 2.5pt)[
        #text(size: 8pt)[#event.label\ #event.value]
      ], align: left + top,
    ))
  }
  standalone[
    #align(center, figure-title(data.title))
    #v(2mm)
    #book-diagram(
      size: "full", height: 58mm,
      xlabel: data.xlabel, ylabel: data.ylabel,
      xlim: data.xlim, ylim: data.ylim,
      legend: (position: bottom + right),
      ..elements,
    )
  ]
}
