#import "/styles/figure.typ": *
#import "/styles/homework-components.typ": homework-math

// Vertical spring states. Unloaded, static equilibrium, and displaced motion.
#standalone(
  full-width-artboard(
    cetz-canvas(
      length: 1mm,
      {
        let top-y = 50
        let mass-width = 12
        let mass-height = 8
        let state-label = (body) => text(fill: color-ink, size: 8pt, body)

        // Static-deflection references are the back layer so both masses mask
        // the dashed endpoints.
        draw.line((22, 16), (33, 16), stroke: mechanics-reference-style.stroke)
        draw.line((33, 8), (45, 8), stroke: mechanics-reference-style.stroke)

        // Unloaded reference spring.
        fixed-support((7, top-y), length: 18, direction: 0deg, hatch-side: 1)
        linear-spring((16, top-y), length: 26, angle: -90deg, coils: 7, amplitude: 2.3)
        draw.content((22, 37), anchor: "west", homework-math[$k$])
        draw.rect(
          (16 - mass-width / 2, 24 - mass-height),
          (16 + mass-width / 2, 24),
          ..mechanics-body-style,
        )
        draw.content((16, 24 - mass-height / 2), homework-math[$m = 0$])

        // Static deflection measured between matching block datums.
        draw.line(
          (33, 16),
          (33, 8),
          stroke: mechanics-displacement-style.stroke,
          mark: (
            start: arrow-head-shape,
            fill: rgb("#466A9F"),
            ..arrow-small,
          ),
        )
        draw.content((35, 12), anchor: "west", homework-math[$delta_("st")$])

        // Static equilibrium configuration.
        fixed-support((42, top-y), length: 18, direction: 0deg, hatch-side: 1)
        linear-spring((51, top-y), length: 34, angle: -90deg, coils: 8, amplitude: 2.3)
        draw.rect(
          (51 - mass-width / 2, 16 - mass-height),
          (51 + mass-width / 2, 16),
          ..mechanics-body-style,
        )
        draw.content((51, 12), homework-math[$m$])
        displacement-indicator(
          (59, 8),
          length: 9,
          angle: -90deg,
          label: homework-math[$u(t)$],
          label-offset: 4,
          extension: 2,
        )

        // Generic displaced configuration.
        fixed-support((78, top-y), length: 18, direction: 0deg, hatch-side: 1)
        linear-spring((87, top-y), length: 43, angle: -90deg, coils: 8, amplitude: 2.3)
        draw.rect(
          (87 - mass-width / 2, 7 - mass-height),
          (87 + mass-width / 2, 7),
          ..mechanics-body-style,
        )
        draw.content((87, 7 - mass-height / 2), homework-math[$m$])

        draw.content((16, -8), state-label[Undeformed position])
        draw.content((51, -8), state-label[Equilibrium position])
        draw.content((87, -8), state-label[Displaced position])
      },
    ),
  ),
)
