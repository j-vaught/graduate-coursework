#import "/styles/figure.typ": *
#import "/styles/homework-components.typ": homework-math

// figure-pipeline: kind=mechanics
#standalone(
  cetz-canvas(
    length: 1mm,
    {
      let wall-x = 4
      let rest-length = 35
      let excited-length = 61
      let mass-width = 14
      let mass-height = 14
      let label-x = 109

      let physical-row(
        center-y,
        component-length,
        state-label,
        displacement: false,
        applied-force: false,
      ) = {
        let mass-left = wall-x + component-length
        let mass-right = mass-left + mass-width
        let mass-bottom = center-y - mass-height / 2
        let mass-top = center-y + mass-height / 2

        fixed-support(
          (wall-x, center-y + 11),
          length: 22,
          direction: 270deg,
          hatch-side: -1,
        )
        linear-spring(
          (wall-x, center-y + 4.5),
          length: component-length,
          // The coil count stays fixed so the longer state reads as stretch.
          coils: 7,
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
        if displacement {
          let rest-center = wall-x + rest-length + mass-width / 2
          let excited-center = mass-left + mass-width / 2
          displacement-indicator(
            (rest-center, mass-top + 5),
            length: excited-center - rest-center,
            label: homework-math[$u(t)$],
            label-offset: 2.8,
            extension: 2.2,
          )
        }
        if applied-force {
          draw.line(
            (mass-right, center-y),
            (mass-right + 20, center-y),
            ..mechanics-force-style,
          )
          draw.content(
            (mass-right + 22, center-y),
            anchor: "west",
            homework-math[$F(t)$],
          )
        }
        draw.content(
          (label-x, center-y),
          anchor: "west",
          text(fill: color-ink, state-label),
        )
      }

      physical-row(67, rest-length, [at rest])
      physical-row(
        40,
        excited-length,
        [excited by ] + homework-math[$F(t)$],
        displacement: true,
        applied-force: true,
      )

      let fbd-y = 12
      let fbd-left = 54
      let fbd-right = fbd-left + mass-width
      draw.rect(
        (fbd-left, fbd-y - mass-height / 2),
        (fbd-right, fbd-y + mass-height / 2),
        ..mechanics-body-style,
      )
      draw.content(
        ((fbd-left + fbd-right) / 2, fbd-y),
        homework-math[$m$],
      )
      draw.line(
        (fbd-left, fbd-y + 3.5),
        (31, fbd-y + 3.5),
        ..mechanics-force-style,
      )
      draw.content(
        (fbd-left - 2, fbd-y + 7),
        anchor: "east",
        homework-math[$k u(t)$],
      )
      draw.line(
        (fbd-left, fbd-y - 3.5),
        (31, fbd-y - 3.5),
        ..mechanics-force-style,
      )
      draw.content(
        (fbd-left - 2, fbd-y - 7),
        anchor: "east",
        homework-math[$c dot(u)(t)$],
      )
      draw.line(
        (fbd-right, fbd-y),
        (fbd-right + 20, fbd-y),
        ..mechanics-force-style,
      )
      draw.content(
        (fbd-right + 22, fbd-y),
        anchor: "west",
        homework-math[$F(t)$],
      )
      draw.line(
        ((fbd-left + fbd-right) / 2 - 6, fbd-y - 11),
        ((fbd-left + fbd-right) / 2 + 10, fbd-y - 11),
        ..mechanics-displacement-style,
      )
      draw.content(
        ((fbd-left + fbd-right) / 2 + 2, fbd-y - 14),
        homework-math[$dot.double(u)(t)$],
      )
      draw.content(
        (label-x, fbd-y),
        anchor: "west",
        text(fill: color-ink)[free-body diagram],
      )
    },
  ),
)
