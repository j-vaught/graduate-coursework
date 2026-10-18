#import "/typst-figures/styles/figure.typ": *

#let xs = range(401).map(i => i / 400)
#let modes = (1, 3, 5, 7, 9)
#let disp = modes.map(n => xs.map(x => calc.sin(n * calc.pi * x / 2)))
#let press = modes.map(n => xs.map(x => -calc.cos(n * calc.pi * x / 2)))
#let cols = (color-deep-teal, color-brass, color-graphite, rgb("#009E73"), color-slate)
#let dashes = (none, "dashed", "dash-dotted", "dotted", "densely-dashed")

#let mode-plot(curves, ylabel) = {
  let elems = ()
  elems.push(hlines(0, stroke: (paint: color-guide, thickness: 0.55pt, dash: "dashed")))
  for i in range(0, modes.len()) {
    elems.push(plot(
      xs,
      curves.at(i),
      stroke: (paint: cols.at(i), thickness: 1.25pt, dash: dashes.at(i), cap: "butt", join: "miter"),
      label: "Mode " + str(i + 1),
    ))
  }
  book-layout[
    #standalone[
      #book-diagram(
        size: "full",
        height: 60mm,
        xlabel: [Normalized position, $xi=x/L$],
        ylabel: ylabel,
        xlim: (0, 1),
        ylim: (-1.05, 1.05),
        xaxis: (ticks: (0, 0.2, 0.4, 0.6, 0.8, 1.0), subticks: none),
        yaxis: (ticks: (-1.0, -0.5, 0.0, 0.5, 1.0), subticks: none),
        legend: (position: top + right),
        ..elems,
      )
    ]
  ]
}

#mode-plot(disp, [Normalized displacement modeshape, $U_j (xi)$])
