#import "/styles/figure.typ": *
#import "/styles/homework-components.typ": homework-math

// Forced spring-mass system following the layout conventions of Figure 8.
#standalone(
  full-width-artboard(
    cetz-canvas(
      length: 1mm,
      {
        let wall-x = 4
        let rest-length = 35
        let excited-length = 61
        let rest-center-y = 52
        let excited-center-y = 31
        let mass-width = 12
        let mass-height = 12
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
            (wall-x, center-y + 9),
            length: 18,
            direction: 270deg,
            hatch-side: -1,
          )
          linear-spring(
            (wall-x, center-y),
            length: component-length,
            coils: 7,
            amplitude: 2,
            lead: 4,
          )
          draw.content(
            (wall-x + component-length / 2, center-y - 6),
            homework-math[$k$],
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
            let arrow-y = rest-center-y - mass-height / 2 - 3
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

        physical-row(rest-center-y, rest-length, [at rest])
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

        let force-y = fbd-y
        draw.line((fbd-left, force-y), (31, force-y), ..mechanics-force-style)
        draw.content(
          (29, force-y),
          anchor: "east",
          homework-math[$k u(t)$],
        )
        draw.line(
          (fbd-right, force-y),
          (fbd-right + 20, force-y),
          ..mechanics-force-style,
        )
        draw.content(
          (fbd-right + 22, force-y),
          anchor: "west",
          homework-math[$F(t)$],
        )

        let acceleration-y = fbd-y - 4.5
        draw.line(
          (fbd-right, acceleration-y),
          (fbd-right + 20, acceleration-y),
          ..mechanics-force-style,
        )
        draw.content(
          (fbd-right + 22, acceleration-y),
          anchor: "west",
          homework-math[$dot.double(u)(t)$],
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
