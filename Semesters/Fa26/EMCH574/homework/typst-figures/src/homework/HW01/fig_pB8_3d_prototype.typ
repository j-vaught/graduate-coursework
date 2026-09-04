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

#let beam-length = 25

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
          })

          // Semi-transparent 7 x 7 plane centered at the beam tip on x = 25.
          // Drawing it before the beam keeps the end cap visually in front.
          draw.on-zy(x: beam-length, {
            draw.rect(
              (-3.5, -3.5),
              (3.5, 3.5),
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
