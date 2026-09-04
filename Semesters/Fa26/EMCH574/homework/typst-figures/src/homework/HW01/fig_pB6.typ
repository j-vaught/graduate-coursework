#import "/styles/figure.typ": *
#import "/styles/homework-components.typ": homework-math

// figure-pipeline: kind=mechanics
#standalone(
  full-width-artboard(
    cetz-canvas(
      length: 1mm,
      {
      let wall-x = 4
      let rest-length = 35
      let excited-length = 61
      let rest-center-y = 67
      let excited-center-y = 40
      let mass-width = 14
      let mass-height = 14
      let label-x = 109

      let physical-row(
        center-y,
        component-length,
        state-label,
        displacement: false,
        force-label: none,
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
          let rest-left = wall-x + rest-length
          let excited-left = mass-left
          let rest-bottom = rest-center-y - mass-height / 2
          // Leave 1.5 mm between the mass and the indicator's top tick.
          let arrow-y = rest-bottom - 3.7
          displacement-indicator(
            (rest-left, arrow-y),
            length: excited-left - rest-left,
            label: homework-math[$u(t)$],
            label-offset: -3,
            extension: 2.2,
          )
        }
        if force-label != none {
          draw.line(
            (mass-right, center-y),
            (mass-right + 20, center-y),
            ..mechanics-force-style,
          )
          draw.content(
            (mass-right + 22, center-y),
            anchor: "west",
            homework-math(force-label),
          )
        }
        draw.content(
          (label-x, center-y),
          anchor: "west",
          text(fill: color-ink, state-label),
        )
      }

      physical-row(
        rest-center-y,
        rest-length,
        [at rest],
        force-label: [$F(t) = 0$],
      )
      physical-row(
        excited-center-y,
        excited-length,
        [excited by ] + homework-math[$F(t)$],
        displacement: true,
        force-label: [$F(t)$],
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
      let applied-force-y = fbd-y
      draw.line(
        (fbd-right, applied-force-y),
        (fbd-right + 20, applied-force-y),
        ..mechanics-force-style,
      )
      draw.content(
        (fbd-right + 22, applied-force-y),
        anchor: "west",
        homework-math[$F(t)$],
      )
      draw.content(
        (label-x, fbd-y),
        anchor: "west",
        text(fill: color-ink)[free-body diagram],
      )
      },
    ),
  ),
)
