#import "/styles/figure.typ": *
#import "/styles/homework-components.typ": homework-math

// figure-pipeline: kind=mechanics
#standalone(
  full-width-artboard(
    cetz-canvas(
      length: 1mm,
      {
      let center-y = 13
      let mass-left = 28
      let mass-right = 42
      let mass-bottom = center-y - 7
      let mass-top = center-y + 7
      let acceleration-length = 18

      draw.rect(
        (mass-left, mass-bottom),
        (mass-right, mass-top),
        ..mechanics-body-style,
      )
      draw.content(
        ((mass-left + mass-right) / 2, center-y),
        homework-math[$m$],
      )
      draw.line(
        (mass-left, center-y + 3.5),
        (4, center-y + 3.5),
        ..mechanics-force-style,
      )
      draw.content(
        (mass-left - 2, center-y + 7),
        anchor: "east",
        homework-math[$k u(t)$],
      )
      draw.line(
        (mass-left, center-y - 3.5),
        (4, center-y - 3.5),
        ..mechanics-force-style,
      )
      draw.content(
        (mass-left - 2, center-y - 7),
        anchor: "east",
        homework-math[$c dot(u)(t)$],
      )
      draw.line(
        (mass-right, center-y),
        (mass-right + acceleration-length, center-y),
        ..mechanics-displacement-style,
      )
      draw.content(
        (mass-right + acceleration-length / 2, center-y + 3),
        homework-math[$dot.double(u)(t)$],
      )
      },
    ),
    placement: "right",
  ),
)
