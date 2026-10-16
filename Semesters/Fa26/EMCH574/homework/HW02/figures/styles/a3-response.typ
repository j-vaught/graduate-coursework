#import "/typst-figures/styles/figure.typ": *

#let a3-plot(data, kind: "road") = {
  let colors = plot-color-cycle
  let elems = ()
  if kind == "road" {
    elems.push(plot(data.x, data.y, stroke: (paint: colors.at(0), thickness: 1.35pt, cap: "butt", join: "miter")))
  } else if kind == "frequency" {
    elems.push(plot(data.x, data.yHealthy, stroke: (paint: colors.at(0), thickness: 1.25pt, cap: "butt", join: "miter"), label: "Healthy shocks, zeta = 0.22"))
    elems.push(plot(data.x, data.yWorn, stroke: (paint: colors.at(1), thickness: 1.25pt, dash: "dashed", cap: "butt", join: "miter"), label: "Worn shocks, zeta = 0.10"))
    for (index, events) in ((0, data.healthyEvents), (1, data.wornEvents)) {
      for i in range(0, events.x.len()) {
        let event-x = events.x.at(i)
        let event-y = events.y.at(i)
        let event-label = events.label.at(i)
        let label-x = if index == 0 { 0.55 } else { 1.20 }
        let label-ys = if index == 0 { (3.8, 3.1) } else { (4.3, 3.5) }
        let label-y = label-ys.at(i)
        elems.push(line(
          (label-x, label-y - 0.16),
          (event-x, event-y), stroke: (paint: color-guide, thickness: 0.45pt, cap: "butt"),
        ))
        elems.push(scatter((event-x,), (event-y,), mark: "s", size: 3.3pt, color: color-ink))
        elems.push(place(label-x, label-y, box(fill: white, stroke: (paint: color-grid, thickness: 0.35pt), inset: 2pt)[#text(size: 7pt)[#event-label]], align: (if index == 0 { right } else { left }) + top))
      }
    }
  } else {
    let color = if data.variant == "healthy" { colors.at(0) } else { colors.at(1) }
    elems.push(plot(data.x, data.y, stroke: (paint: color, thickness: 1.25pt, cap: "butt", join: "miter"), label: data.curveLabel))
    elems.push(hlines(data.limit, stroke: (paint: color-ink, thickness: 0.75pt, dash: "dotted")))
    let label-xs = (data.xlim.at(0) + 22, data.xlim.at(0) + 55, data.xlim.at(0) + 76, data.xlim.at(0) + 105)
    let label-ys = (0.15, data.ylim.at(1) - 0.40, data.ylim.at(1) - 1.00, 0.15)
    for i in range(0,data.events.x.len()) {
      let event-x = data.events.x.at(i)
      let event-y = data.events.y.at(i)
      let event-label = data.events.label.at(i)
      let label-x = label-xs.at(i)
      let label-y = label-ys.at(i)
      elems.push(line((label-x, label-y + 0.22), (event-x, event-y), stroke: (paint: color-guide, thickness: 0.45pt, cap: "butt")))
      elems.push(scatter((event-x,), (event-y,), mark: "s", size: 3.3pt, color: color-ink))
      elems.push(place(label-x, label-y, box(fill: white, stroke: (paint: color-grid, thickness: 0.35pt), inset: 2pt)[#text(size: 7pt)[#event-label]], align: center + bottom))
    }
  }
  book-layout[
    #standalone[
      #book-diagram(size:"full",height:65mm,xlabel:data.xlabel,ylabel:data.ylabel,xlim:data.xlim,ylim:data.ylim,
        legend: if kind == "road" { none } else if kind == "frequency" { (position: top + right) } else { (position: top + left) }, ..elems)
    ]
  ]
}
