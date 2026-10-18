#import "/typst-figures/styles/figure.typ": *

#standalone(
  cetz-canvas(length: 10mm, {
    let ink = (paint: color-ink, thickness: 0.85pt, cap: "butt", join: "miter")
    let wall = (paint: color-graphite, thickness: 1.5pt, cap: "butt", join: "miter")
    let fluid = (paint: color-deep-teal, thickness: 0.75pt, cap: "butt", join: "miter")

    // The two continuous wall paths end at the open boundaries.
    draw.line((1.25, 3.1), (7.4, 3.1), stroke: wall)
    draw.line((1.25, 2.0), (7.4, 2.0), stroke: wall)
    draw.line((1.45, 2.55), (7.2, 2.55), stroke: fluid)
    draw.content((3.7, 2.78), text(size: 7pt)[$A, rho, K, c$])
    draw.content((4.2, 2.36), text(size: 7pt)[$u(x,t)$])

    // Small filled arrows show the open-end continuation and displacement.
    draw.line((1.25, 2.55), (0.55, 2.55), stroke: fluid,
      mark: (fill: color-deep-teal, ..arrow-small))
    draw.line((7.4, 2.55), (8.1, 2.55), stroke: fluid,
      mark: (fill: color-deep-teal, ..arrow-small))
    draw.line((1.25, 1.25), (7.4, 1.25), stroke: ink,
      mark: (fill: color-ink, ..arrow-small))
    draw.content((4.2, 0.92), [$x$])
    draw.line((1.25, 1.03), (1.25, 1.46), stroke: ink)
    draw.line((7.4, 1.03), (7.4, 1.46), stroke: ink)
    draw.content((1.05, 0.62), [$0$])
    draw.content((7.25, 0.62), [$L$])
    draw.content((0.28, 3.48), text(size: 7pt)[$p(0,t)=0$])
    draw.content((6.32, 3.48), text(size: 7pt)[$p(L,t)=0$])
  }),
)
