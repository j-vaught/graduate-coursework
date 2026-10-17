#import "/typst-figures/styles/figure.typ": *

#standalone(
  cetz-canvas(length: 10mm, {
    let y0 = 1.65
    let scale = 1.0
    let wave = (paint: color-deep-teal, thickness: 1.8pt)
    let guide = (paint: color-guide, thickness: 0.75pt, dash: "dashed")
    let ink = (paint: color-ink, thickness: 0.8pt)

    // One wavelength; x is normalized so that lambda spans four plotting units.
    for i in range(0, 240) {
      let x = i * 4 / 240
      let xn = (i + 1) * 4 / 240
      let y = y0 + scale * calc.cos(90deg * x)
      let yn = y0 + scale * calc.cos(90deg * xn)
      draw.line((x, y), (xn, yn), stroke: wave)
    }

    draw.line((0, y0), (4.35, y0), stroke: (paint: color-guide, thickness: 0.65pt))
    draw.line((0, 0.25), (0, 3.15), stroke: ink,
      mark: (fill: color-ink, ..arrow-medium))
    draw.line((0, y0 - 1.35), (4.35, y0 - 1.35), stroke: ink,
      mark: (fill: color-ink, ..arrow-medium))
    draw.content((4.12, y0 - 1.95), [$x$])
    draw.content((-0.27, 2.35), [$u$])

    for x in (1, 3) {
      draw.line((x, y0 - 1.1), (x, y0 + 1.1), stroke: guide)
      draw.circle((x, y0), radius: 0.045, fill: color-brass)
    }
    for x in (0, 2, 4) {
      draw.circle((x, y0 + calc.cos(90deg * x)), radius: 0.045, fill: color-graphite)
    }

    // Marker key distinguishes extrema from zero-displacement nodes.
    draw.circle((0.48, 3.48), radius: 0.045, fill: color-graphite)
    draw.content((0.6, 3.36), [$A$: antinode])
    draw.circle((2.15, 3.48), radius: 0.045, fill: color-brass)
    draw.content((2.27, 3.36), [$N$: node])

    // Wavelength fractions are labeled at their actual positions.
    for x in (0, 1, 2, 3, 4) {
      draw.line((x, y0 - 1.35), (x, y0 - 1.25), stroke: ink)
    }
    draw.content((-0.04, 0.02), [$0$])
    draw.content((0.72, 0.02), [$lambda/4$])
    draw.content((1.75, 0.02), [$lambda/2$])
    draw.content((2.65, 0.02), [$3lambda/4$])
    draw.content((3.88, 0.02), [$lambda$])
  }),
)
