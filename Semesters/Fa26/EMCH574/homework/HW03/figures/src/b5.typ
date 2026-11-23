#import "/typst-figures/styles/figure.typ": *

#standalone(
    cetz-canvas(length: 1mm, {
      let ink = (paint: color-graphite, thickness: 1pt, cap: "butt", join: "miter")
      let accent = color-secondary
      let motion = (stroke: (paint: accent, thickness: 1pt), mark: (end: "stealth", fill: accent))
      let x0 = 14
      let x1 = 106
      let y = 18
      draw.line((x0, 5), (x0, 31), stroke: (paint: color-graphite, thickness: 3pt))
      for yy in range(6, 31, step: 3) {
        draw.line((x0 - 3, yy), (x0, yy + 3), stroke: (paint: color-graphite, thickness: 0.5pt))
      }
      draw.rect((x0, y - 2), (x1, y + 2), fill: white, stroke: ink)
      draw.content((58, y + 8), text(size: 12pt, fill: black)[$L, h, b, E, rho$])
      draw.line((x1 + 5, y - 2), (x1 + 5, y + 21), ..motion)
      draw.content((x1 + 12, y + 10), text(size: 12pt, fill: black)[$w_(max)$])
      draw.line((x0, 4), (x1, 4), stroke: ink)
      draw.line((x0, 2), (x0, 6), stroke: ink)
      draw.line((x1, 2), (x1, 6), stroke: ink)
      draw.content(((x0+x1)/2, 0), text(size: 12pt, fill: black)[$L$], anchor: "north")
    }),
)
