#import "/styles/figure.typ": *
#import "/styles/homework-components.typ": homework-math

// Damped cantilever beam with a slightly unbalanced tip-mounted motor.

#standalone(
  full-width-artboard(
    cetz-canvas(
      length: 1mm,
      {
        let wall-x = 10
        let beam-left = wall-x
        let beam-right = 105
        let beam-bottom = 32
        let beam-top = 36
        let motor-x = 98
        let motor-y = 44.5
        let motor-radius = 4.8

        let outline = (
          paint: color-ink,
          thickness: 1.1pt,
          cap: "butt",
          join: "miter",
        )
        let dimension-stroke = (
          paint: color-ink,
          thickness: 0.75pt,
          cap: "butt",
        )

        // Dimension extensions are the back layer so the structure masks
        // them wherever they pass behind the wall, beam, or motor assembly.
        draw.line(
          (beam-left, beam-top + 1),
          (beam-left, 58),
          stroke: mechanics-reference-style.stroke,
        )
        draw.line(
          (beam-right, beam-top + 1),
          (beam-right, 58),
          stroke: mechanics-reference-style.stroke,
        )

        // Proper fixed wall support with the hatching outside the beam span.
        fixed-support(
          (wall-x, 17),
          length: 34,
          direction: 90deg,
          hatch-side: 1,
        )

        // Uniform cantilever beam.
        draw.rect(
          (beam-left, beam-bottom),
          (beam-right, beam-top),
          fill: color-surface,
          stroke: outline,
        )

        // Motor mounting foot and motor mass.
        draw.line(
          (91.5, beam-top),
          (94.8, 40.5),
          (101.2, 40.5),
          (104.5, beam-top),
          close: true,
          fill: color-background,
          stroke: outline,
        )
        draw.circle(
          (motor-x, motor-y),
          radius: motor-radius,
          fill: color-surface-strong,
          stroke: outline,
        )
        draw.content(
          (motor-x, motor-y),
          homework-math[$m$],
        )
        // Beam length dimension.
        draw.line(
          (beam-left, 56),
          (beam-right, 56),
          stroke: dimension-stroke,
          mark: (
            start: arrow-head-shape,
            fill: color-ink,
            ..arrow-small,
          ),
        )
        draw.content(
          ((beam-left + beam-right) / 2, 59),
          homework-math[$L$],
        )

        // Downward tip displacement, using the standard ticked indicator.
        displacement-indicator(
          (112, beam-top),
          length: 20,
          angle: -90deg,
          label: homework-math[$u$],
          label-offset: -3,
          extension: 2,
        )

        draw.content(
          ((beam-left + beam-right) / 2, 25),
          homework-math[$E, h, b, zeta$],
        )

      },
    ),
  ),
)
