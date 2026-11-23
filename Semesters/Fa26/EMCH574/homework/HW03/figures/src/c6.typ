#import "/typst-figures/styles/figure.typ": *

#standalone(cetz-canvas(length: 1mm, {
  let outline = (paint: color-graphite, thickness: 1pt, cap: "butt")
  for y in (-7, 7) { draw.line((0, y), (96, y), stroke: outline) }
  draw.content((17, 0), text(size: 12pt)[$A, rho, E$])
  draw.content((52, 2), text(size: 12pt)[$u(x,t)$])
  draw.line((45, -2.5), (59, -2.5), stroke: 1pt + color-secondary,
    mark: (end: "stealth", fill: color-secondary))
  draw.line((92, 0), (107, 0), stroke: 0.65pt + color-graphite)
  draw.content((110, 0), text(size: 12pt)[$x$])
}))
