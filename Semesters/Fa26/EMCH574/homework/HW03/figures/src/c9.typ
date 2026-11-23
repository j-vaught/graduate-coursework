#import "/typst-figures/styles/figure.typ": *

#standalone(cetz-canvas(length: 1mm, {
  let outline = (paint: color-graphite, thickness: 1pt, join: "miter")
  draw.line((-6, 0), (106, 0), stroke: 0.65pt + color-graphite)
  draw.rect((0, -5), (96, 5), fill: white, stroke: outline)
  draw.content((16, 0), text(size: 12pt)[$A, rho, E, c$])
  draw.content((53, 1.5), text(size: 12pt)[$u(x,t)$])
  draw.line((46, -2.5), (60, -2.5), stroke: 1pt + color-secondary,
    mark: (end: "stealth", fill: color-secondary))
  draw.content((109, 0), text(size: 12pt)[$x$])
  draw.content((0, -10), text(size: 11pt)[$x=0$ free])
  draw.content((96, -10), text(size: 11pt)[$x=L$ free])
  draw.content((48, -10), text(size: 12pt)[$L$])
}))
