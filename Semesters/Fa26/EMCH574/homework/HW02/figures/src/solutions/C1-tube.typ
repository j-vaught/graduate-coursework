#import "/typst-figures/styles/figure.typ": *

#standalone(
  cetz-canvas(length: 10mm, {
    let ink = (paint: color-ink, thickness: 0.85pt)
    let guide = (paint: color-guide, thickness: 0.65pt, dash: "dashed")
    let wall = (paint: color-graphite, thickness: 1.5pt)
    let fluid = (paint: color-deep-teal, thickness: 0.75pt)

    draw.line((1.25, 3.1), (7.4, 3.1), stroke: wall)
    draw.line((1.25, 2.0), (7.4, 2.0), stroke: wall)
    draw.line((1.25, 2.0), (1.25, 3.1), stroke: wall)
    draw.line((7.4, 2.0), (7.4, 3.1), stroke: (paint: color-graphite, thickness: 0.65pt, dash: "dashed"))
    draw.line((1.45, 2.55), (7.2, 2.55), stroke: fluid)
    draw.content((3.7, 2.72), text(size: 7pt)[$A, rho, K, c$])

    draw.line((1.25, 1.25), (7.4, 1.25), stroke: ink,
      mark: (fill: color-ink, ..arrow-medium))
    draw.content((4.2, 0.92), [$x$])
    draw.line((1.25, 1.03), (1.25, 1.46), stroke: ink)
    draw.line((7.4, 1.03), (7.4, 1.46), stroke: ink)
    draw.content((1.05, 0.62), [$0$])
    draw.content((7.25, 0.62), [$L$])
    draw.content((0.35, 2.45), text(size: 7pt)[$u(0,t)=0$])
    draw.content((6.25, 3.55), text(size: 7pt)[$p(L,t)=0$])
    draw.line((7.55, 2.55), (8.12, 2.55), stroke: fluid,
      mark: (fill: color-deep-teal, ..arrow-medium))
    draw.content((8.2, 2.95), text(size: 7pt)[$u$ antinode])
  }),
)
