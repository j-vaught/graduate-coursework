#import "/typst-figures/styles/figure.typ": *

#standalone(
  cetz-canvas(length: 10mm, {
    let baseline = 1.35
    let ink = (paint: color-ink, thickness: 0.8pt)
    draw.line((0, baseline), (12, baseline), stroke: ink, mark: (fill: color-ink, ..arrow-medium))
    draw.line((0, baseline - 1.0), (0, baseline + 1.05), stroke: ink, mark: (fill: color-ink, ..arrow-medium))
    draw.content((12, baseline - 0.28), [$x$])
    draw.content((-0.25, baseline + 1.25), [$u$])
    let points = ()
    for i in range(0, 241) {
      let x = i * 0.05
      let y = baseline + 0.72 * calc.sin(60deg * x)
      points.push((x, y))
    }
    draw.line(..points, stroke: (paint: color-deep-teal, thickness: 1.4pt, cap: "butt", join: "miter"))
    draw.line((1.5, 2.07), (1.5, 0.7), stroke: (paint: color-guide, thickness: 0.65pt, dash: "dashed"))
    draw.line((7.5, 2.07), (7.5, 0.7), stroke: (paint: color-guide, thickness: 0.65pt, dash: "dashed"))
    draw.content((1.25, 0.45), [$x_0$])
    draw.content((7.2, 0.45), [$x_0+lambda$])
    draw.content((3.9, 2.55), [$Delta phi=gamma lambda=2 pi$])
  }),
)
