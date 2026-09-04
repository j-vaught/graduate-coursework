#import "/styles/figure.typ": *

#let axis-stroke = (
  paint: color-ink,
  thickness: line-emphasis,
  cap: "butt",
)

#let solid-stroke = (
  paint: color-ink,
  thickness: line-emphasis,
  cap: "butt",
  join: "miter",
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

            // A 4-high by 1.5-wide rectangle centered at the origin.
            draw.rect(
              (-2, -0.75),
              (2, 0.75),
              fill: color-background,
              stroke: (
                paint: color-ink,
                thickness: line-emphasis,
                cap: "butt",
                join: "miter",
              ),
            )
          })

          // Visible faces of the 4 x 1.5 profile extruded from x = 0 to x = 10.
          draw.line(
            (0, -0.75, 2),
            (10, -0.75, 2),
            (10, 0.75, 2),
            (0, 0.75, 2),
            close: true,
            fill: color-surface,
            stroke: solid-stroke,
          )
          draw.line(
            (0, -0.75, -2),
            (10, -0.75, -2),
            (10, -0.75, 2),
            (0, -0.75, 2),
            close: true,
            fill: color-surface-strong,
            stroke: solid-stroke,
          )
          draw.line(
            (10, -0.75, -2),
            (10, 0.75, -2),
            (10, 0.75, 2),
            (10, -0.75, 2),
            close: true,
            fill: color-background,
            stroke: solid-stroke,
          )

          draw.line(
            (0, 0, 0),
            (30, 0, 0),
            stroke: axis-stroke,
            mark: (fill: color-ink, ..arrow-medium),
          )
          draw.line(
            (0, 0, 0),
            (0, 30, 0),
            stroke: axis-stroke,
            mark: (fill: color-ink, ..arrow-medium),
          )
          draw.line(
            (0, 0, 0),
            (0, 0, 30),
            stroke: axis-stroke,
            mark: (fill: color-ink, ..arrow-medium),
          )

          draw.content((30.8, 0, 0), anchor: "west", [$x=30$])
          draw.content((0, 30.8, 0), anchor: "south", [$y=30$])
          draw.content((0, 0, 30.8), anchor: "east", [$z=30$])
          draw.content((0, 0, 0), anchor: "north", [$0$])
        },
      )
    },
  ),
)
