#import "/styles/figure.typ": *
#import "/styles/homework-components.typ": homework-math

// Combined truck-suspension figure. The physical suspension is drawn at left
// and the one-degree-of-freedom idealization at right in one shared coordinate
// system so labels and strokes are scaled only once in the homework document.

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

#let callout(label, label-position, leader-start, target, anchor: "west") = {
  draw.line(
    leader-start,
    target,
    stroke: (
      paint: color-ink,
      thickness: 0.7pt,
      cap: "butt",
    ),
    mark: (fill: color-ink, ..arrow-small),
  )
  draw.content(
    label-position,
    anchor: anchor,
    text(fill: color-ink, size: 8pt, label),
  )
}

#standalone(
  full-width-artboard(
    cetz-canvas(
      length: 1mm,
      {
        // Physical leaf-spring suspension at left.
        draw.group({
          draw.set-origin((-3, 0))

          let left-eye = 16
          let right-eye = 94
          let eye-y = 46
          let sag = 13
          let center-x = (left-eye + right-eye) / 2
          let center-y = eye-y - sag
          let wheel-y = 22.5
          let damper-x = center-x

          let tire-color = rgb("#c8cdd0")
          let wheel-color = rgb("#ffffff")
          let axle-color = rgb("#000000")
          let mount-color = rgb("#a2a2a2")
          let leaf-color = color-secondary
          let damper-rod-color = rgb("#000000")
          let damper-body-color = color-secondary
          let frame-color = rgb("#e4e6e7")

          let black-stroke = (
            paint: rgb("#000000"),
            thickness: 1.1pt,
            cap: "butt",
            join: "miter",
          )
          let leaf-stroke = (
            paint: leaf-color,
            thickness: 3.15pt,
            cap: "butt",
            join: "miter",
          )
          let spring-eye-stroke = (
            paint: leaf-color,
            thickness: 1.35pt,
            cap: "butt",
            join: "miter",
          )

          fixed-support(
            (31, 1),
            length: 48,
            direction: 0deg,
            hatch-side: -1,
          )

          draw.circle(
            (center-x, wheel-y),
            radius: 21.5,
            fill: tire-color,
            stroke: black-stroke,
          )
          draw.circle(
            (center-x, wheel-y),
            radius: 13,
            fill: wheel-color,
            stroke: black-stroke,
          )
          draw.circle(
            (center-x, wheel-y),
            radius: 3.4,
            fill: axle-color,
            stroke: none,
          )

          let mount-points = (
            (center-x - 5.2, center-y - 5.75),
            (center-x - 5.2, wheel-y),
          )
          for index in range(17) {
            let angle = 180deg + index * 180deg / 16
            mount-points.push((
              center-x + 5.2 * calc.cos(angle),
              wheel-y + 5.2 * calc.sin(angle),
            ))
          }
          mount-points.push((center-x + 5.2, center-y - 5.75))
          draw.line(
            ..mount-points,
            stroke: (
              paint: mount-color,
              thickness: 3.0pt,
              cap: "butt",
              join: "miter",
            ),
          )
          draw.line(
            (center-x - 9, center-y - 5.75),
            (center-x + 9, center-y - 5.75),
            stroke: (
              paint: mount-color,
              thickness: 3.0pt,
              cap: "butt",
            ),
          )

          draw.line(
            ..leaf-profile(left-eye, right-eye, eye-y, sag),
            stroke: leaf-stroke,
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
          draw.circle(
            (left-eye, eye-y),
            radius: 2.2,
            fill: color-background,
            stroke: spring-eye-stroke,
          )
          draw.circle(
            (right-eye, eye-y),
            radius: 2.2,
            fill: color-background,
            stroke: spring-eye-stroke,
          )

          draw.line(
            (damper-x, wheel-y + 4.8),
            (damper-x, 43),
            stroke: (
              paint: damper-rod-color,
              thickness: 1.4pt,
              cap: "butt",
            ),
          )
          draw.rect(
            (damper-x - 2.2, 41),
            (damper-x + 2.2, 54.4),
            fill: damper-body-color,
            stroke: none,
          )
          draw.line(
            (damper-x, 54.4),
            (damper-x, 58),
            stroke: (
              paint: damper-rod-color,
              thickness: 1.4pt,
              cap: "butt",
            ),
          )
          draw.circle(
            (damper-x, wheel-y + 4.8),
            radius: 1.05,
            fill: damper-rod-color,
            stroke: none,
          )

          draw.line(
            (5, 68),
            (105, 68),
            (105, eye-y),
            (right-eye, eye-y),
            (81, 58),
            (29, 58),
            (left-eye, eye-y),
            (5, eye-y),
            close: true,
            fill: frame-color,
            stroke: black-stroke,
          )
          draw.circle(
            (left-eye, eye-y),
            radius: 1.0,
            fill: rgb("#000000"),
            stroke: none,
          )
          draw.circle(
            (right-eye, eye-y),
            radius: 1.0,
            fill: rgb("#000000"),
            stroke: none,
          )
          draw.circle(
            (damper-x, 58),
            radius: 1.0,
            fill: rgb("#000000"),
            stroke: none,
          )

          draw.content(
            (11, 63.5),
            anchor: "west",
            text(fill: color-ink, size: 8pt)[truck frame],
          )
          callout([damper], (65, 55), (63, 53.5), (57.2, 50))
          callout([leaf spring], (90, 25.5), (88.5, 27), (74, 30.7))
        })

        // Vertical spring-mass-damper idealization at right.
        draw.group({
          draw.set-origin((110, 0))

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
          displacement-indicator(
            (mass-right, mass-top),
            length: 18,
            angle: 90deg,
            label: homework-math[$u(t)$],
            label-offset: -3,
            extension: 2,
          )
          draw.content(
            (25, ground-y - 5.5),
            text(fill: color-ink, size: 8pt)[road datum],
          )
        })
      },
    ),
  ),
)
