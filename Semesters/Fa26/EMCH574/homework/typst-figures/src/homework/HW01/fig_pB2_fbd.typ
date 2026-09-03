#import "/styles/figure.typ": *
#import "/styles/homework-components.typ": homework-math

// figure-pipeline: kind=mechanics
#standalone(
  cetz-canvas(
    length: 1mm,
    {
      let center-y = 13
      let mass-left = 28
      let mass-right = 42
      let mass-bottom = center-y - 7
      let mass-top = center-y + 7

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
        (mass-right, mass-top + 4),
        (mass-right + 18, mass-top + 4),
        ..mechanics-displacement-style,
      )
      draw.content(
        (mass-right + 9, mass-top + 7),
        homework-math[$dot.double(u)(t)$],
      )
    },
  ),
)
