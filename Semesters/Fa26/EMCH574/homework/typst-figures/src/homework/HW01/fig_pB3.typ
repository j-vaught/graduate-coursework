#import "/styles/figure.typ": *
#import "/styles/homework-components.typ": homework-math

// figure-pipeline: kind=mechanics
#standalone(
  cetz-canvas(
    length: 1mm,
    {
      let wall-x = 4
      let center-y = 13
      let component-length = 31
      let mass-left = wall-x + component-length
      let mass-right = mass-left + 15
      let mass-bottom = center-y - 7.5
      let mass-top = center-y + 7.5

      fixed-support(
        (wall-x, center-y + 11),
        length: 22,
        direction: 270deg,
        hatch-side: -1,
      )
      linear-spring(
        (wall-x, center-y + 4.5),
        length: component-length,
        coils: 6,
        amplitude: 2,
        lead: 4,
      )
      viscous-damper(
        (wall-x, center-y - 4.5),
        length: component-length,
        body-length: 6mm,
        body-width: 7mm,
      )
      draw.content(
        (wall-x + component-length / 2, center-y + 8),
        homework-math[$k$],
      )
      draw.content(
        (wall-x + component-length / 2, center-y - 9),
        homework-math[$c$],
      )
      draw.rect(
        (mass-left, mass-bottom),
        (mass-right, mass-top),
        ..mechanics-body-style,
      )
      draw.content(
        ((mass-left + mass-right) / 2, center-y),
        homework-math[$m$],
      )
      displacement-indicator(
        (mass-left, mass-top + 4),
        length: 18,
        label: homework-math[$u$],
        label-offset: 2.6,
        extension: 2,
      )
    },
  ),
)
