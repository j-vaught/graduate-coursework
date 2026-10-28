#import "/typst-figures/styles/figure.typ": *

#let b4-modes-plot(data, mode-type: "displacement") = {
  let colors = (
    color-deep-teal,
    rgb("#d55e00"),
    color-graphite,
    rgb("#009e73"),
    color-slate,
  )
  let dashes = (none, "dashed", "dash-dotted", "dotted", "densely-dashed")
  let elems = ()

  // Zero reference centerline
  elems.push(hlines(0, stroke: (paint: color-guide, thickness: 0.55pt, dash: "dashed")))

  for i in range(0, data.curves.len()) {
    let curve = data.curves.at(i)
    let stroke = (
      paint: colors.at(i),
      thickness: 1.3pt,
      dash: dashes.at(i),
      cap: "butt",
      join: "miter",
    )
    elems.push(plot(data.x, curve.y, stroke: stroke, label: curve.label))
  }

  let ylabel = if mode-type == "displacement" {
    [Displacement modeshape, $U_j (x)$]
  } else {
    [Normalized pressure modeshape, $P_j (x)$]
  }

  book-layout[
    #standalone[
      #book-diagram(
        size: "full",
        height: 60mm,
        xlabel: [Position along tube, $x$ (m)],
        ylabel: ylabel,
        xlim: (0, 0.5),
        ylim: (-1.05, 1.05),
        xaxis: (
          ticks: (0, 0.1, 0.2, 0.3, 0.4, 0.5),
          subticks: none,
        ),
        yaxis: (
          ticks: (-1.0, -0.5, 0.0, 0.5, 1.0),
          subticks: none,
        ),
        legend: (position: top + right),
        ..elems,
      )
    ]
  ]
}
