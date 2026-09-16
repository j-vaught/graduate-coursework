#import "/typst-figures/styles/figure.typ": *

// MATLAB supplies numerical data; Lilaq authors the vector figure.
#let response-colors = (rgb("#73000A"), rgb("#466A9F"), rgb("#363636"))
#let response-figure(data, y-limits: none) = {
  let x = data.x
  let plot-ylim = if y-limits == none { data.ylim } else { y-limits }
  let span-x = data.xlim.at(1) - data.xlim.at(0)
  let span-y = plot-ylim.at(1) - plot-ylim.at(0)
  let elements = ()
  if data.band != none {
    elements.push(hlines(
      -data.band, data.band,
      stroke: (paint: rgb("#5C5C5C"), thickness: 0.65pt, dash: "dotted", cap: "butt"),
    ))
  }
  for (index, curve) in data.curves.enumerate() {
    let stroke = (
      paint: response-colors.at(calc.rem(index, response-colors.len())),
      thickness: 1.1pt,
      cap: "butt",
      join: "miter",
    )
    if calc.rem(index, 2) == 1 { stroke.insert("dash", "dashed") }
    elements.push(plot(x, curve.y, stroke: stroke, label: if data.curves.len() > 1 { curve.label } else { none }))
  }
  for (index, event) in data.events.enumerate() {
    let is-a2-tip = data.title == "A2. Pendulum released from 2 mm"
    let label-x = if is-a2-tip {
      event.x + 0.45
    } else {
      data.xlim.at(0) + (0.02 + 0.33 * index) * span-x
    }
    let label-y = if is-a2-tip {
      event.y + 0.9
    } else {
      plot-ylim.at(1) - 0.025 * span-y
    }
    let leader-start = if is-a2-tip {
      (label-x, event.y + 0.2)
    } else {
      (label-x + 0.05 * span-x, label-y - 0.12 * span-y)
    }
    elements.push(line(
      leader-start, (event.x, event.y),
      stroke: (paint: rgb("#5C5C5C"), thickness: 0.5pt, cap: "butt"),
    ))
    elements.push(scatter((event.x,), (event.y,), mark: "s", size: 3.5pt, color: black))
    elements.push(place(label-x, label-y,
      box(fill: white, stroke: (paint: rgb("#C7C7C7"), thickness: 0.4pt), inset: 2.5pt)[
        #text(size: 8pt)[#event.label\ #event.value]
      ], align: left + top,
    ))
  }
  standalone[
    #set text(fill: black)
    #align(center, figure-title(data.title))
    #v(2mm)
    #book-diagram(
      size: "full", height: 58mm,
      xlabel: data.xlabel, ylabel: data.ylabel,
      xlim: data.xlim, ylim: plot-ylim,
      legend: (position: bottom + right),
      ..elements,
    )
  ]
}
