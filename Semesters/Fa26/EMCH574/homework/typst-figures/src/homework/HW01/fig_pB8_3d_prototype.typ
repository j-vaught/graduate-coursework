#import "/styles/figure.typ": *

#let axis-stroke = (
  paint: color-ink,
  thickness: line-emphasis,
  cap: "butt",
)

#standalone(
  cetz-canvas(
    length: 4mm,
    {
      draw.ortho(
        x: -66.85deg,
        y: 0deg,
        z: -34.26deg,
        sorted: false,
        {
          draw.line(
            (0, 0, 0),
            (10, 0, 0),
            stroke: axis-stroke,
            mark: (fill: color-ink, ..arrow-medium),
          )
          draw.line(
            (0, 0, 0),
            (0, 10, 0),
            stroke: axis-stroke,
            mark: (fill: color-ink, ..arrow-medium),
          )
          draw.line(
            (0, 0, 0),
            (0, 0, 10),
            stroke: axis-stroke,
            mark: (fill: color-ink, ..arrow-medium),
          )

          draw.content((10.8, 0, 0), anchor: "west", [$x=10$])
          draw.content((0, 10.8, 0), anchor: "south", [$y=10$])
          draw.content((0, 0, 10.8), anchor: "east", [$z=10$])
          draw.content((0, 0, 0), anchor: "north", [$0$])
        },
      )
    },
  ),
)
