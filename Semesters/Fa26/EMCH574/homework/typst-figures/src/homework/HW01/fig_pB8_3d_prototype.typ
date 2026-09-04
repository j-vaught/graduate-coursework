#import "/styles/figure.typ": *

#let outline = (
  paint: color-ink,
  thickness: 0.85pt,
  cap: "butt",
  join: "bevel",
)

// Fill the visible faces without strokes, then draw one outer silhouette and
// the three visible creases. This prevents overlapping face outlines from
// producing miter spikes at projected corners.
#let beam-prism(origin, length, height, depth-offset) = {
  let x = origin.at(0)
  let y = origin.at(1)
  let ox = depth-offset.at(0)
  let oy = depth-offset.at(1)

  let a = (x, y)
  let b = (x + length, y)
  let c = (x + length, y + height)
  let d = (x, y + height)
  let bp = (x + length + ox, y + oy)
  let cp = (x + length + ox, y + height + oy)
  let dp = (x + ox, y + height + oy)

  draw.line(a, b, c, d, close: true, fill: color-surface, stroke: none)
  draw.line(d, dp, cp, c, close: true, fill: color-background, stroke: none)
  draw.line(b, bp, cp, c, close: true, fill: color-surface-strong, stroke: none)

  draw.line(a, b, bp, cp, dp, d, close: true, stroke: outline)
  draw.line(b, c, stroke: outline)
  draw.line(d, c, stroke: outline)
  draw.line(c, cp, stroke: outline)
}

#standalone(
  cetz-canvas(
    length: 1mm,
    {
      draw.group({
        draw.rotate(-10deg)
        beam-prism((0, 0), 72, 8, (3, 1.5))
      })
    },
  ),
)
