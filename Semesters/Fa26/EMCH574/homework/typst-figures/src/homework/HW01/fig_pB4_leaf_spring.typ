#import "/styles/figure.typ": *
#import "/styles/homework-components.typ": homework-math

// The equivalent-beam relations follow the centrally loaded, simply
// supported beam model in NASA-TM-X-62848, Eq. (53). The spring centerline
// uses the corresponding normalized elastic-curve solution on each half-span.

#let leaf-profile(
  left,
  right,
  eye-y,
  sag,
  start: 0.0,
  stop: 1.0,
  offset: 0,
  samples: 48,
) = {
  let points = ()
  for index in range(samples + 1) {
    let t = start + (stop - start) * index / samples
    let mirrored = if t <= 0.5 { t } else { 1 - t }
    let normalized-deflection = mirrored * (3 - 4 * mirrored * mirrored)
    points.push((
      left + t * (right - left),
      eye-y - sag * normalized-deflection - offset,
    ))
  }
  points
}

#standalone(
  full-width-artboard(
    cetz-canvas(
      length: 1mm,
      {
        let left-eye = 16
        let right-eye = 94
        let eye-y = 49
        let sag = 17
        let center-x = (left-eye + right-eye) / 2
        let center-y = eye-y - sag
        let damper-x = 106
        let leaf-stroke = (
          paint: color-mechanical,
          thickness: 1.05pt,
          cap: "butt",
          join: "miter",
        )
        let master-stroke = (
          paint: color-mechanical,
          thickness: 1.35pt,
          cap: "butt",
          join: "miter",
        )

        // Road, tire, axle, and center seat.
        fixed-support(
          (46, 3),
          length: 26,
          direction: 0deg,
          hatch-side: -1,
        )
        draw.circle(
          (center-x, 12),
          radius: 9,
          fill: color-background,
          stroke: master-stroke,
        )
        draw.circle(
          (center-x, 12),
          radius: 3,
          fill: color-surface-strong,
          stroke: leaf-stroke,
        )
        draw.line(
          (center-x, 15),
          (center-x, 23),
          stroke: master-stroke,
        )
        draw.rect(
          (center-x - 13, 21),
          (damper-x + 3, 25),
          fill: color-surface-strong,
          stroke: master-stroke,
        )

        // Laminated spring. Shorter graduated leaves remain tangent to the
        // same centrally loaded elastic curve as the master leaf.
        draw.line(
          ..leaf-profile(left-eye, right-eye, eye-y, sag),
          stroke: master-stroke,
        )
        draw.line(
          ..leaf-profile(left-eye, right-eye, eye-y, sag, start: 0.08, stop: 0.92, offset: 1.5),
          stroke: leaf-stroke,
        )
        draw.line(
          ..leaf-profile(left-eye, right-eye, eye-y, sag, start: 0.17, stop: 0.83, offset: 3.0),
          stroke: leaf-stroke,
        )
        draw.line(
          ..leaf-profile(left-eye, right-eye, eye-y, sag, start: 0.27, stop: 0.73, offset: 4.5),
          stroke: leaf-stroke,
        )

        // Center plate and U-bolts transfer axle load into the leaf pack.
        draw.line((center-x - 5, 35), (center-x - 5, 22), stroke: leaf-stroke)
        draw.line((center-x + 5, 35), (center-x + 5, 22), stroke: leaf-stroke)
        draw.line((center-x - 5, 22), (center-x + 5, 22), stroke: leaf-stroke)
        draw.line((center-x - 7, 35), (center-x + 7, 35), stroke: master-stroke)

        // Rebound clips keep the graduated leaves visibly assembled as a pack.
        draw.line((35.5, 34), (35.5, 39.5), stroke: leaf-stroke)
        draw.line((74.5, 34), (74.5, 39.5), stroke: leaf-stroke)

        // Vehicle frame, front hanger, rear shackle, and oil damper.
        draw.rect(
          (7, 60),
          (111, 66),
          fill: color-surface-strong,
          stroke: master-stroke,
        )
        draw.content(
          (59, 63),
          text(fill: color-ink)[truck body ] + homework-math[$m$],
        )
        draw.line((13, 60), (left-eye, eye-y), stroke: master-stroke)
        draw.line((19, 60), (left-eye, eye-y), stroke: master-stroke)
        draw.circle(
          (left-eye, eye-y),
          radius: 2.2,
          fill: color-background,
          stroke: master-stroke,
        )
        draw.circle(
          (98, 58.4),
          radius: 1.6,
          fill: color-background,
          stroke: leaf-stroke,
        )
        draw.line((98, 60), (98, 58.4), stroke: master-stroke)
        draw.line((96.4, 58.4), (92.4, eye-y), stroke: master-stroke)
        draw.line((99.6, 58.4), (95.6, eye-y), stroke: master-stroke)
        draw.circle(
          (right-eye, eye-y),
          radius: 2.2,
          fill: color-background,
          stroke: master-stroke,
        )
        viscous-damper(
          (damper-x, 23),
          length: 37,
          angle: 90deg,
          body-length: 10mm,
          body-width: 6mm,
        )
        draw.circle(
          (damper-x, 23),
          radius: 1.2,
          fill: color-background,
          stroke: leaf-stroke,
        )
        draw.circle(
          (damper-x, 60),
          radius: 1.2,
          fill: color-background,
          stroke: leaf-stroke,
        )

        draw.content(
          (24, 46),
          anchor: "west",
          text(fill: color-ink, size: 8pt)[leaf pack ] + homework-math[$k$],
        )
        draw.content(
          (101, 40),
          anchor: "east",
          text(fill: color-ink, size: 8pt)[oil damper ] + homework-math[$c$],
        )

      },
    ),
  ),
)
