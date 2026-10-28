#import "/typst-figures/styles/figure.typ": *

#let c3-plot(case, kind) = {
  let L = 0.5
  let xs = range(501).map(i => L * i / 500)
  let closed-open = case == "closed-open"
  let modes = if closed-open { (1, 3, 5, 7, 9) } else { (1, 2, 3, 4, 5) }
  let freqs = if closed-open { (170, 510, 850, 1190, 1530) } else { (340, 680, 1020, 1360, 1700) }
  let curves = if kind == "displacement" {
    modes.map(n => if closed-open {
      xs.map(x => calc.sin(n * calc.pi * x / (2 * L)))
    } else {
      xs.map(x => calc.cos(n * calc.pi * x / L))
    })
  } else {
    modes.map(n => if closed-open {
      xs.map(x => -calc.cos(n * calc.pi * x / (2 * L)))
    } else {
      xs.map(x => calc.sin(n * calc.pi * x / L))
    })
  }
  let cols = (color-deep-teal, color-brass, color-graphite, rgb("#009E73"), color-slate)
  let dashes = (none, "dashed", "dash-dotted", "dotted", "densely-dashed")
  let elems = ()
  elems.push(hlines(0, stroke: (paint: color-guide, thickness: 0.55pt, dash: "dashed")))
  for i in range(0, modes.len()) {
    elems.push(plot(
      xs,
      curves.at(i),
      stroke: (paint: cols.at(i), thickness: 1.25pt, dash: dashes.at(i), cap: "butt", join: "miter"),
      label: "Mode " + str(i + 1) + " (" + str(freqs.at(i)) + " Hz)",
    ))
  }
  let ylabel = if kind == "displacement" {
    [Normalized displacement modeshape, $U_j (x)$]
  } else {
    [Normalized pressure modeshape, $overline(P)_j (x)$]
  }
  book-layout[
    #standalone[
      #book-diagram(
        size: "full",
        height: 60mm,
        xlabel: [Position along tube, $x$ (m)],
        ylabel: ylabel,
        xlim: (0, L),
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
