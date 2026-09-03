#import "/styles/figure.typ": *
#import "/styles/homework-components.typ": homework-math

// figure-pipeline: kind=mechanics
#standalone(
  full-width-artboard(
    cetz-canvas(
      length: 1mm,
      {
        let ground-y = 4
        let component-length = 34
        let mass-bottom = ground-y + component-length
        let mass-top = mass-bottom + 14
        let mass-left = 8
        let mass-right = 42

        linear-spring(
          (16, ground-y),
          length: component-length,
          angle: 90deg,
          coils: 7,
          amplitude: 2.2,
          lead: 4,
        )
        viscous-damper(
          (34, ground-y),
          length: component-length,
          angle: 90deg,
          body-length: 8mm,
          body-width: 6mm,
        )
        fixed-support(
          (2, ground-y),
          length: 46,
          direction: 0deg,
          hatch-side: -1,
        )

        draw.content(
          (11, ground-y + component-length / 2),
          anchor: "east",
          homework-math[$k$],
        )
        draw.content(
          (39, ground-y + component-length / 2),
          anchor: "west",
          homework-math[$c$],
        )

        draw.rect(
          (mass-left, mass-bottom),
          (mass-right, mass-top),
          ..mechanics-body-style,
        )
        draw.content(
          ((mass-left + mass-right) / 2, (mass-bottom + mass-top) / 2),
          homework-math[$m$],
        )

        draw.line(
          (mass-right, mass-top),
          (mass-right, mass-top + 18),
          ..mechanics-displacement-style,
        )
        draw.content(
          (mass-right + 3, mass-top + 9),
          anchor: "west",
          homework-math[$u(t)$],
        )
        draw.content(
          (25, ground-y - 5.5),
          text(fill: color-ink, size: 8pt)[road datum],
        )
      },
    ),
  ),
)
