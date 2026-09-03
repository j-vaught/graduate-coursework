#import "/styles/figure.typ": *

// The spring centerline follows the normalized elastic curve for a centrally
// loaded, simply supported equivalent beam. Component construction then runs
// from the rear-most wheel layer to the foreground truck-frame layer.

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
        let eye-y = 46
        let sag = 13
        let center-x = (left-eye + right-eye) / 2
        let center-y = eye-y - sag
        let wheel-y = 22.5
        let damper-x = center-x

        let tire-color = rgb("#41484c")
        let wheel-color = rgb("#c8cdd0")
        let axle-color = rgb("#000000")
        let mount-color = rgb("#000000")
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
        let master-stroke = (
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
        // Background road datum.
        fixed-support(
          (31, 1),
          length: 48,
          direction: 0deg,
          hatch-side: -1,
        )

        // Layer 1. Dark-gray tire.
        draw.circle(
          (center-x, wheel-y),
          radius: 21.5,
          fill: tire-color,
          stroke: black-stroke,
        )

        // Layer 2. Silver wheel.
        draw.circle(
          (center-x, wheel-y),
          radius: 13,
          fill: wheel-color,
          stroke: black-stroke,
        )

        // Layer 3. Black axle at the wheel center.
        draw.circle(
          (center-x, wheel-y),
          radius: 3.4,
          fill: axle-color,
          stroke: none,
        )

        // Layer 4. A single bent mounting bar wraps under the axle and
        // returns to the spring seat on both sides.
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

        // Layer 5. Teal laminated leaf spring.
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

        // Layer 6. Two-tone vertical damper. The thin black rod enters the
        // teal upper tube, and its lower eye lands on the axle mount.
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
          (damper-x - 2.7, 41),
          (damper-x + 2.7, 57.4),
          fill: damper-body-color,
          stroke: none,
        )
        draw.circle(
          (damper-x, wheel-y + 4.8),
          radius: 1.05,
          fill: damper-rod-color,
          stroke: none,
        )

        // Layer 7. Light-gray truck body with the stepped wheel-well profile
        // from the reference sketch. The spring eyes pin directly to the
        // lower corners, so no separate hanger links are required.
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
          radius: 1.4,
          fill: frame-color,
          stroke: black-stroke,
        )
      },
    ),
  ),
)
