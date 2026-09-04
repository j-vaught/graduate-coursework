#import "/styles/figure.typ": *

#let outline = (
  paint: color-ink,
  thickness: 0.85pt,
  cap: "butt",
  join: "miter",
)

#let face(points, fill) = {
  draw.line(..points, close: true, fill: fill, stroke: outline)
}

#let beam(x0, x1, y0, y1, z0, z1) = {
  face(
    ((x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)),
    color-background,
  )
  face(
    ((x0, y1, z0), (x0, y1, z1), (x1, y1, z1), (x1, y1, z0)),
    color-background,
  )
  face(
    ((x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)),
    color-surface,
  )
  face(
    ((x0, y0, z0), (x0, y1, z0), (x1, y1, z0), (x1, y0, z0)),
    color-surface-strong,
  )
  face(
    ((x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)),
    color-surface-strong,
  )
  face(
    ((x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)),
    color-surface-strong,
  )
}

#standalone(
  cetz-canvas(
    length: 1mm,
    {
      draw.hide(draw.rect((-2, -2), (82, 33)))
      draw.group({
        draw.translate((5, 16))
        draw.ortho(
          x: 15deg,
          y: 35deg,
          z: -2deg,
          sorted: true,
          {
            beam(0, 72, -1, 1, -4, 4)
          },
        )
      })
    },
  ),
)
