#import "/typst-figures/styles/figure.typ": *

#standalone(
  cetz-canvas(length: 10mm, {
    let ink = (paint: color-ink, thickness: 0.85pt)
    let guide = (paint: color-guide, thickness: 0.65pt, dash: "dashed")
    let disp = (paint: color-displacement, thickness: 1.15pt)
    let force = (paint: color-force, thickness: 1.05pt)
    let wall = (paint: color-graphite, thickness: 0.8pt)

    // Upper panel: the element, its pressure labels, and its displacements.
    draw.content((0.05, 4.55), text(weight: "bold")[$(a)$ Infinitesimal element])
    draw.line((0.55, 3.35), (8.05, 3.35), stroke: wall)
    draw.line((0.55, 2.25), (8.05, 2.25), stroke: wall)
    draw.line((3.0, 2.25), (3.0, 3.35), stroke: ink)
    draw.line((5.6, 2.25), (5.6, 3.35), stroke: ink)
    draw.line((3.0, 1.95), (5.6, 1.95), stroke: ink,
      mark: (fill: color-ink, ..arrow-medium))
    draw.line((5.6, 1.95), (3.0, 1.95), stroke: ink,
      mark: (fill: color-ink, ..arrow-medium))
    draw.content((4.05, 1.62), [$d x$])
    draw.content((3.0, 3.52), text(size: 7pt)[$p(x,t)$])
    draw.content((5.85, 3.52), text(size: 7pt)[$p(x+d x,t)=p+p_x d x$])
    draw.line((3.0, 3.08), (4.25, 3.08), stroke: disp,
      mark: (fill: color-displacement, ..arrow-medium))
    draw.line((5.6, 3.08), (6.85, 3.08), stroke: disp,
      mark: (fill: color-displacement, ..arrow-medium))
    draw.content((3.0, 3.90), text(size: 7pt)[$u(x,t)$])
    draw.content((5.9, 3.90), text(size: 7pt)[$u(x+d x,t)=u+u_x d x$])
    draw.line((3.0, 2.05), (3.0, 0.95), stroke: guide)
    draw.line((5.6, 2.05), (5.6, 0.95), stroke: guide)

    // Lower panel: pressure forces acting on the isolated element.
    draw.content((0.05, 1.05), text(weight: "bold")[$(b)$ Free-body diagram])
    draw.rect((3.0, -0.25), (5.6, 0.35), stroke: ink, fill: color-surface)
    draw.line((1.55, 0.05), (3.0, 0.05), stroke: force,
      mark: (fill: color-force, ..arrow-medium))
    draw.line((7.05, 0.05), (5.6, 0.05), stroke: force,
      mark: (fill: color-force, ..arrow-medium))
    draw.content((2.1, 0.70), text(size: 7pt)[$A p(x,t)$])
    draw.content((6.4, 0.70), text(size: 7pt)[$A[p(x,t)+p_x d x]$])
    draw.content((3.25, -0.60), [$m=rho A d x$])
    draw.content((7.2, -0.60), [$+x$])
    draw.line((6.98, -0.42), (7.48, -0.42), stroke: ink,
      mark: (fill: color-ink, ..arrow-medium))
  }),
)
