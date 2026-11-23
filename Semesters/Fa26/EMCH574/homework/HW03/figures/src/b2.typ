#import "/typst-figures/styles/figure.typ": *

#standalone(
    cetz-canvas(length: 1mm, {
      let ink = (paint: color-graphite, thickness: 1pt, cap: "butt", join: "miter")
      let accent = color-secondary
      let motion = (stroke: (paint: accent, thickness: 1pt), mark: (end: "stealth", fill: accent))
      let x0 = 14
      let x1 = 114
      let y0 = 20
      // Fixed wall and square hatching.
      draw.line((x0, 10), (x0, 30), stroke: (paint: color-graphite, thickness: 3pt))
      for y in range(11, 30, step: 3) {
        draw.line((x0 - 3, y), (x0, y + 3), stroke: (paint: color-graphite, thickness: 0.5pt))
      }
      draw.rect((x0, y0 - 4), (x1, y0 + 4), fill: white, stroke: ink)
      draw.content((38, y0), text(size: 12pt, fill: black)[$m, E, I$])
      draw.line((72, y0 - 1), (72, y0 + 13), ..motion)
      draw.content((72, y0 + 17), text(size: 12pt, fill: black)[$w(x,t)$])
      draw.line((x0, 3), (x1, 3), stroke: ink)
      draw.line((x0, 1), (x0, 5), stroke: ink)
      draw.line((x1, 1), (x1, 5), stroke: ink)
      draw.content(((x0+x1)/2, -1), text(size: 12pt, fill: black)[$L$], anchor: "north")
      draw.content((x0, -6), text(size: 12pt, fill: black)[$x=0$ fixed])
      draw.content((x1, -6), text(size: 12pt, fill: black)[$x=L$ free])
      draw.line((x1 + 2, y0), (x1 + 12, y0), stroke: ink)
      draw.content((x1 + 15, y0), text(size: 12pt, fill: black)[$x$])
    }),
)
