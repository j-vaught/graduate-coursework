#import "/typst-figures/styles/figure.typ": *

#standalone(cetz-canvas(length: 10mm, {
  let wall = (paint: color-graphite, thickness: 1.5pt)
  let ink = (paint: color-ink, thickness: 0.85pt)
  let fluid = (paint: color-deep-teal, thickness: 0.75pt, dash: "dashed")

  draw.line((1.25, 3.1), (7.4, 3.1), stroke: wall)
  draw.line((1.25, 2.0), (7.4, 2.0), stroke: wall)
  draw.line((1.25, 2.0), (1.25, 3.1), stroke: wall)
  draw.line((7.4, 2.0), (7.4, 3.1), stroke: wall)
  draw.content((2.5, 2.55), text(size: 7pt)[$A, rho, K, c$])
  draw.content((4.65, 2.73), text(size: 7pt)[$u(x,t)$])
  draw.line((4.3, 2.42), (5.05, 2.42), stroke: fluid,
    mark: (fill: color-deep-teal, ..arrow-medium))
  draw.line((0.75, 2.55), (1.25, 2.55), stroke: ink)
  draw.line((7.4, 2.55), (8.12, 2.55), stroke: ink,
    mark: (fill: color-ink, ..arrow-medium))
  draw.content((8.35, 2.55), [$x$])
  draw.content((1.25, 1.68), text(size: 7pt)[$x=0$])
  draw.content((4.32, 1.68), [$L$])
  draw.content((7.4, 1.68), text(size: 7pt)[$x=L$])
  draw.content((1.25, 1.18), text(size: 7pt)[closed])
  draw.content((7.4, 1.18), text(size: 7pt)[closed])
}))
