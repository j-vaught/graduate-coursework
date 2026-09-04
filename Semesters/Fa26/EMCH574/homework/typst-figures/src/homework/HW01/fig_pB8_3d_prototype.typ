#import "/styles/figure.typ": *

#let outline = (
  paint: color-ink,
  thickness: 0.85pt,
  cap: "butt",
  join: "miter",
)
#let fine = (
  paint: color-ink,
  thickness: 0.6pt,
  cap: "butt",
  join: "miter",
)
#let guide = (
  paint: color-guide,
  thickness: 0.55pt,
  dash: "dashed",
  cap: "butt",
)
#let axis-stroke = (
  paint: color-ink,
  thickness: 0.75pt,
  cap: "butt",
)
#let displacement-stroke = (
  paint: color-displacement,
  thickness: 1.05pt,
  cap: "butt",
)

#let face(points, fill) = {
  draw.line(..points, close: true, fill: fill, stroke: outline)
}

#let prism(
  x0,
  x1,
  y0,
  y1,
  z0,
  z1,
  front: color-surface,
  side: color-surface-strong,
  top: color-background,
) = {
  face(((x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)), front)
  face(((x0, y1, z0), (x0, y1, z1), (x1, y1, z1), (x1, y1, z0)), front)
  face(((x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)), top)
  face(((x0, y0, z0), (x0, y1, z0), (x1, y1, z0), (x1, y0, z0)), side)
  face(((x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)), side)
  face(((x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)), side)
}

#standalone(
  cetz-canvas(
    length: 1mm,
    {
      // Establish a predictable page box for the projected model and inset.
      draw.hide(draw.rect((-4, -7), (148, 86)))

      draw.group({
        draw.translate((27, 41))
        draw.ortho(
          x: 25deg,
          y: 48deg,
          z: -4deg,
          sorted: true,
          {
            // Fixed wall. The hatch is authored first so the beam masks it.
            draw.on-zy(x: -0.8, {
              draw.rect(
                (-20, -18),
                (20, 18),
                fill: color-surface,
                stroke: (paint: color-primary, thickness: 1.15pt, join: "miter"),
              )
              for offset in range(-15, 11, step: 5) {
                draw.line(
                  (-20, offset),
                  (20, offset + 6),
                  stroke: (paint: color-guide, thickness: 0.45pt, cap: "butt"),
                )
              }
            })

            // Beam and end mass use real three-dimensional vertices.
            prism(
              0,
              72,
              -3,
              3,
              -2.5,
              2.5,
              front: color-background,
              side: color-surface-strong,
              top: color-surface,
            )
            prism(
              72,
              84,
              -8,
              8,
              -10,
              10,
              front: color-surface,
              side: color-surface-strong,
              top: color-background,
            )
            // Length extensions are behind the dimension line and structure.
            draw.line((0, -4, -3), (0, -4, -16), stroke: guide)
            draw.line((72, -4, -3), (72, -4, -16), stroke: guide)
            draw.line(
              (0, -4, -15),
              (72, -4, -15),
              stroke: fine,
              mark: (start: arrow-head-shape, fill: color-ink, ..arrow-small),
            )
            draw.content((36, -4, -18), [$L$])

            // The displacement arrow begins beyond the mass with a clear gap.
            draw.line(
              (88, -8, -5),
              (105, -8, -5),
              stroke: displacement-stroke,
              mark: (fill: color-displacement, ..arrow-medium),
            )
            draw.content(
              (107, -8, -5),
              anchor: "west",
              text(fill: color-displacement)[$u(t)$],
            )

          },
        )
      })

      // A separate projected triad keeps all three model directions visible.
      draw.group({
        draw.translate((18, 72))
        draw.ortho(x: 25deg, y: 48deg, z: -4deg, sorted: false, {
          draw.line((0, 0, 0), (11, 0, 0), stroke: axis-stroke, mark: (fill: color-ink, ..arrow-small))
          draw.line((0, 0, 0), (0, 11, 0), stroke: axis-stroke, mark: (fill: color-ink, ..arrow-small))
          draw.line((0, 0, 0), (0, 0, 11), stroke: axis-stroke, mark: (fill: color-ink, ..arrow-small))
          draw.content((13, 0, 0), [$x$])
          draw.content((0, 13, 0), [$y$])
          draw.content((0, 0, 13), [$z$])
        })
      })

      // Semantic labels sit above the sorted solid faces.
      draw.content((72, 10), text(size: 13pt)[$M$])
      draw.content((50, 17), [$E, b, h$])

      // The projectile remains a compact schematic beside the 3D structure.
      draw.rect((48, 1), (55, 5), fill: color-surface, stroke: outline)
      draw.content((51.5, 7.5), [$m$])
      draw.line(
        (56.5, 4),
        (66, 10),
        stroke: displacement-stroke,
        mark: (fill: color-displacement, ..arrow-small),
      )
      draw.content((61, 11), text(fill: color-displacement)[$v$])

      // A 2D inset stays unprojected so b and h remain unambiguous.
      let sx = 126
      let sy = 57
      draw.content(
        (sx + 10, sy + 16),
        anchor: "west",
        text(weight: "semibold")[Beam section],
      )
      draw.rect(
        (sx - 4, sy - 10),
        (sx + 4, sy + 10),
        fill: color-surface,
        stroke: outline,
      )
      for offset in range(-8, 9, step: 4) {
        draw.line(
          (sx - 4, sy + offset - 3),
          (sx + 4, sy + offset + 3),
          stroke: (paint: color-guide, thickness: 0.45pt, cap: "butt"),
        )
      }
      draw.line(
        (sx - 7, sy - 10),
        (sx - 7, sy + 10),
        stroke: fine,
        mark: (start: arrow-head-shape, fill: color-ink, ..arrow-small),
      )
      draw.content((sx - 10, sy), [$b$])
      draw.line(
        (sx - 4, sy - 13),
        (sx + 4, sy - 13),
        stroke: fine,
        mark: (start: arrow-head-shape, fill: color-ink, ..arrow-small),
      )
      draw.content((sx, sy - 17), [$h$])
      draw.line(
        (sx + 7, sy),
        (sx + 19, sy),
        stroke: axis-stroke,
        mark: (fill: color-ink, ..arrow-small),
      )
      draw.line(
        (sx, sy + 12),
        (sx, sy + 23),
        stroke: axis-stroke,
        mark: (fill: color-ink, ..arrow-small),
      )
      draw.content((sx + 21, sy), [$y$])
      draw.content((sx, sy + 25), [$z$])
    },
  ),
)
