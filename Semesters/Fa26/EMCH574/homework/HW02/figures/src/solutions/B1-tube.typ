#import "/typst-figures/styles/figure.typ": *

#standalone(cetz-canvas(length: 10mm, {
  let wall = (paint: color-graphite, thickness: 1.5pt)
  let ink = (paint: color-ink, thickness: 0.85pt)
  let fluid = (paint: color-deep-teal, thickness: 0.75pt, dash: "dashed")

  // Both ends continue beyond the drawing, as in the supplied infinite tube.
  draw.line((0, 3.1), (8.3, 3.1), stroke: wall)
  draw.line((0, 1.5), (8.3, 1.5), stroke: wall)
  draw.content((1.3, 2.3), [$A, rho, K$])
  draw.content((4.5, 2.55), [$u(x,t)$])
  draw.line((4.05, 2.12), (4.95, 2.12), stroke: fluid,
    mark: (fill: color-deep-teal, ..arrow-medium))
  draw.line((7.15, 2.3), (8.45, 2.3), stroke: ink,
    mark: (fill: color-ink, ..arrow-medium))
  draw.content((8.7, 2.3), [$x$])
}))
