#import "/styles/figure.typ": *

#let axis-stroke = (
  paint: color-ink,
  thickness: line-emphasis,
  cap: "butt",
)

#let solid-stroke = (
  paint: color-ink,
  thickness: line-emphasis,
  cap: "round",
  join: "round",
)

#let guide-stroke = (
  paint: color-guide,
  thickness: line-normal,
  dash: "dashed",
  cap: "butt",
)

#let beam-length = 25
#let cube-length = 7
#let cube-end = beam-length + cube-length
#let cube-half = 3.5
#let axis-length = 35
#let z-axis-length = 10
#let cube-fill = color-surface-strong.transparentize(45%)
#let cube-stroke = (
  paint: color-border,
  thickness: line-normal,
  cap: "round",
  join: "round",
)

#standalone(
  cetz-canvas(
    length: 4mm,
    {
      draw.ortho(
        x: -69.2733deg,
        y: 0deg,
        z: -33.9052deg,
        sorted: false,
        {
          // Draw dashed construction lines first so solids cover hidden spans.
          draw.line(
            (28.5, 0, 0),
            (28.5, -10, 0),
            stroke: guide-stroke,
          )

          // Semi-transparent 10 x 10 wall centered at the origin on x = 0.
          // It is drawn first so all three calibration axes remain on top.
          draw.on-zy(x: 0, {
            draw.rect(
              (-5, -5),
              (5, 5),
              fill: color-surface-strong.transparentize(45%),
              stroke: (
                paint: color-border,
                thickness: line-normal,
                cap: "butt",
                join: "miter",
              ),
            )
          })

          // Fill the visible faces without borders. A single silhouette and
          // three crease lines are drawn afterward to keep the joins clean.
          draw.line(
            (0, -0.75, 2),
            (beam-length, -0.75, 2),
            (beam-length, 0.75, 2),
            (0, 0.75, 2),
            close: true,
            fill: color-surface-strong,
            stroke: none,
          )
          draw.line(
            (0, -0.75, -2),
            (beam-length, -0.75, -2),
            (beam-length, -0.75, 2),
            (0, -0.75, 2),
            close: true,
            fill: color-surface-strong,
            stroke: none,
          )
          draw.line(
            (beam-length, -0.75, -2),
            (beam-length, 0.75, -2),
            (beam-length, 0.75, 2),
            (beam-length, -0.75, 2),
            close: true,
            fill: color-surface-strong,
            stroke: none,
          )

          // VINNT-style prism outline: one closed silhouette plus the three
          // edges meeting at the nearest corner.
          draw.line(
            (0, -0.75, -2),
            (beam-length, -0.75, -2),
            (beam-length, 0.75, -2),
            (beam-length, 0.75, 2),
            (0, 0.75, 2),
            (0, -0.75, 2),
            close: true,
            stroke: solid-stroke,
          )
          draw.line(
            (beam-length, -0.75, -2),
            (beam-length, -0.75, 2),
            stroke: solid-stroke,
          )
          draw.line(
            (0, -0.75, 2),
            (beam-length, -0.75, 2),
            stroke: solid-stroke,
          )
          draw.line(
            (beam-length, -0.75, 2),
            (beam-length, 0.75, 2),
            stroke: solid-stroke,
          )

          // Extrude the 7 x 7 tip profile from x = 25 to x = 32.
          draw.line(
            (beam-length, -cube-half, cube-half),
            (cube-end, -cube-half, cube-half),
            (cube-end, cube-half, cube-half),
            (beam-length, cube-half, cube-half),
            close: true,
            fill: cube-fill,
            stroke: none,
          )
          draw.line(
            (beam-length, -cube-half, -cube-half),
            (cube-end, -cube-half, -cube-half),
            (cube-end, -cube-half, cube-half),
            (beam-length, -cube-half, cube-half),
            close: true,
            fill: cube-fill,
            stroke: none,
          )
          draw.line(
            (cube-end, -cube-half, -cube-half),
            (cube-end, cube-half, -cube-half),
            (cube-end, cube-half, cube-half),
            (cube-end, -cube-half, cube-half),
            close: true,
            fill: cube-fill,
            stroke: none,
          )

          // One rounded silhouette and three crease lines define the cube.
          draw.line(
            (beam-length, -cube-half, -cube-half),
            (cube-end, -cube-half, -cube-half),
            (cube-end, cube-half, -cube-half),
            (cube-end, cube-half, cube-half),
            (beam-length, cube-half, cube-half),
            (beam-length, -cube-half, cube-half),
            close: true,
            stroke: cube-stroke,
          )
          draw.line(
            (cube-end, -cube-half, -cube-half),
            (cube-end, -cube-half, cube-half),
            stroke: cube-stroke,
          )
          draw.line(
            (beam-length, -cube-half, cube-half),
            (cube-end, -cube-half, cube-half),
            stroke: cube-stroke,
          )
          draw.line(
            (cube-end, -cube-half, cube-half),
            (cube-end, cube-half, cube-half),
            stroke: cube-stroke,
          )

          draw.line(
            (0, 0, 0),
            (axis-length, 0, 0),
            stroke: axis-stroke,
            mark: (fill: color-ink, ..arrow-medium),
          )
          draw.line(
            (0, 0, 0),
            (0, axis-length, 0),
            stroke: axis-stroke,
            mark: (fill: color-ink, ..arrow-medium),
          )
          draw.line(
            (0, 0, 0),
            (0, 0, z-axis-length),
            stroke: axis-stroke,
            mark: (fill: color-ink, ..arrow-medium),
          )

          draw.content((axis-length + 0.8, 0, 0), anchor: "west", [$x=35$])
          draw.content((0, axis-length + 0.8, 0), anchor: "south", [$y=35$])
          draw.content((0, 0, z-axis-length + 0.8), anchor: "east", [$z=10$])
          draw.content((0, 0, 0), anchor: "north", [$0$])
        },
      )
    },
  ),
)
