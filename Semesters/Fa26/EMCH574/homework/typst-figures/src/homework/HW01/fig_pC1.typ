#import "/styles/figure.typ": *
#import "/styles/homework-components.typ": homework-math

// Vertical spring states. Unloaded, static equilibrium, and displaced motion.
#standalone(
  full-width-artboard(
    cetz-canvas(
      length: 1mm,
      {
        let top-y = 50
        let state-label = (body) => text(fill: color-ink, size: 8pt, body)

        // Unloaded reference spring.
        fixed-support((7, top-y), length: 18, direction: 0deg, hatch-side: 1)
        linear-spring((16, top-y), length: 26, angle: -90deg, coils: 7, amplitude: 2.3)
        draw.content((22, 37), anchor: "west", homework-math[$k$])
        draw.line((25, 24), (31, 24), stroke: mechanics-reference-style.stroke)
        draw.line((25, 12), (31, 12), stroke: mechanics-reference-style.stroke)
        draw.line(
          (28, 24),
          (28, 12),
          stroke: mechanics-displacement-style.stroke,
          mark: (
            start: arrow-head-shape,
            fill: rgb("#466A9F"),
            ..arrow-small,
          ),
        )
        draw.content((30, 18), anchor: "west", homework-math[$delta_("st")$])

        // Static equilibrium configuration.
        fixed-support((42, top-y), length: 18, direction: 0deg, hatch-side: 1)
        linear-spring((51, top-y), length: 34, angle: -90deg, coils: 8, amplitude: 2.3)
        draw.rect((45, 8), (57, 16), ..mechanics-body-style)
        draw.content((51, 12), homework-math[$m$])
        draw.line((63, 16), (69, 16), stroke: mechanics-reference-style.stroke)
        displacement-indicator(
          (66, 16),
          length: 11,
          angle: -90deg,
          label: homework-math[$u(t)$],
          label-offset: -3,
          extension: 1.8,
        )

        // Generic displaced configuration.
        fixed-support((78, top-y), length: 18, direction: 0deg, hatch-side: 1)
        linear-spring((87, top-y), length: 43, angle: -90deg, coils: 8, amplitude: 2.3)
        draw.rect((81, 0), (93, 7), ..mechanics-body-style)
        draw.content((87, 3.5), homework-math[$m$])

        draw.content((106, 20), anchor: "west", state-label[Equilibrium position])
        draw.content((106, 4), anchor: "west", state-label[Displaced position])
      },
    ),
  ),
)
