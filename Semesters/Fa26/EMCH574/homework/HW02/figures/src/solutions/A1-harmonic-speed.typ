#import "/typst-figures/styles/figure.typ": *

#standalone(
  cetz-canvas(length: 10mm, {
    let ink = (paint: color-ink, thickness: 0.8pt)
    draw.line((0, 0), (12, 0), stroke: ink, mark: (fill: color-ink, ..arrow-medium))
    draw.content((12, -0.3), [$x$])
    draw.line((0, 1.15), (12, 1.15), stroke: (paint: color-grid, thickness: 0.5pt))
    draw.line((0, 2.35), (12, 2.35), stroke: (paint: color-grid, thickness: 0.5pt))
    for i in range(0, 240) {
      let x = i * 0.05
      let xn = (i + 1) * 0.05
      let y1 = 1.15 + 0.48 * calc.sin(30deg * x - 45deg)
      let y2 = 2.35 + 0.48 * calc.sin(30deg * (x - 2) - 45deg)
      let y1n = 1.15 + 0.48 * calc.sin(30deg * xn - 45deg)
      let y2n = 2.35 + 0.48 * calc.sin(30deg * (xn - 2) - 45deg)
      draw.line((x, y1), (xn, y1n), stroke: (paint: color-deep-teal, thickness: 1.3pt))
      draw.line((x, y2), (xn, y2n), stroke: (paint: color-secondary, thickness: 1.3pt))
    }
    draw.content((0.1, 1.65), [$t_1$])
    draw.content((0.1, 2.85), [$t_2=t_1+Delta t$])
    draw.line((4.5, 1.63), (4.5, 2.15), stroke: (paint: color-guide, thickness: 0.65pt, dash: "dashed"))
    draw.line((6.5, 2.83), (6.5, 2.15), stroke: (paint: color-guide, thickness: 0.65pt, dash: "dashed"))
    draw.line((4.5, 2.15), (6.5, 2.15), stroke: (paint: color-ink, thickness: 0.8pt), mark: (fill: color-ink, ..arrow-medium))
    draw.content((5.15, 2.4), [$Delta x$])
  }),
)
