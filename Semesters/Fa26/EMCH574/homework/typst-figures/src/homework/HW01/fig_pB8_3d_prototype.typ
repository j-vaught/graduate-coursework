#import "/styles/figure.typ": *

#let axis-stroke = (
  paint: color-ink,
  thickness: line-emphasis,
  cap: "butt",
)

#let shape-stroke = (
  paint: color-on-light,
  thickness: line-normal,
  cap: "round",
  join: "round",
)

#let motion-arrow-stroke = (
  paint: color-displacement,
  thickness: line-emphasis,
  cap: "butt",
  join: "miter",
)

#let guide-stroke = (
  paint: color-guide,
  thickness: line-normal,
  dash: "dashed",
  cap: "butt",
)

#let callout-stroke = (
  paint: color-ink,
  thickness: line-normal,
  cap: "round",
)

#let callout(point, label-position, label, anchor: "west") = {
  draw.line(point, label-position, stroke: callout-stroke)
  draw.content(label-position, anchor: anchor, figure-small(label))
}

#let beam-length = 25
#let cube-length = 7
#let cube-end = beam-length + cube-length
#let cube-half = 3.5
#let x-axis-start = 32
#let x-axis-length = 40
#let y-axis-start = 5
#let y-axis-length = 15
#let z-axis-start = 5
#let z-axis-length = 10
#let cube-fill = color-surface-strong
#let projectile-x = 28.5
#let projectile-front-y = -20
#let projectile-length = 4
#let projectile-back-y = projectile-front-y + projectile-length
#let projectile-radius = 0.5
#let velocity-arrow-x = projectile-x + projectile-radius + 1.25
#let displacement-arrow-x = cube-end + 1.5
#let displacement-arrow-length = 9
// Tangency offsets for the calibrated projection and a radius-0.5 circle.
#let projectile-rim-x = 0.281
#let projectile-rim-z = 0.414
#standalone(
  cetz-canvas(
    length: 4mm,
    {
      draw.ortho(
        x: -69.2733deg,
        y: 0deg,
        z: -33.9052deg,
        sorted: false,
        {
          // Semi-transparent 10 x 10 wall centered at the origin on x = 0.
          // It is drawn first so all three calibration axes remain on top.
          draw.on-zy(x: 0, {
            draw.rect(
              (-5, -5),
              (5, 5),
              fill: color-surface-strong.transparentize(45%),
              stroke: shape-stroke,
            )
          })

          // Fill the visible faces without borders. A single silhouette and
          // three crease lines are drawn afterward to keep the joins clean.
          draw.line(
            (0, -0.75, 2),
            (beam-length, -0.75, 2),
            (beam-length, 0.75, 2),
            (0, 0.75, 2),
            close: true,
            fill: color-surface-strong,
            stroke: none,
          )
          draw.line(
            (0, -0.75, -2),
            (beam-length, -0.75, -2),
            (beam-length, -0.75, 2),
            (0, -0.75, 2),
            close: true,
            fill: color-surface-strong,
            stroke: none,
          )
          draw.line(
            (beam-length, -0.75, -2),
            (beam-length, 0.75, -2),
            (beam-length, 0.75, 2),
            (beam-length, -0.75, 2),
            close: true,
            fill: color-surface-strong,
            stroke: none,
          )

          // VINNT-style prism outline: one closed silhouette plus the three
          // edges meeting at the nearest corner.
          draw.line(
            (0, -0.75, -2),
            (beam-length, -0.75, -2),
            (beam-length, 0.75, -2),
            (beam-length, 0.75, 2),
            (0, 0.75, 2),
            (0, -0.75, 2),
            close: true,
            stroke: shape-stroke,
          )
          draw.line(
            (beam-length, -0.75, -2),
            (beam-length, -0.75, 2),
            stroke: shape-stroke,
          )
          draw.line(
            (0, -0.75, 2),
            (beam-length, -0.75, 2),
            stroke: shape-stroke,
          )
          draw.line(
            (beam-length, -0.75, 2),
            (beam-length, 0.75, 2),
            stroke: shape-stroke,
          )

          // Extrude the 7 x 7 tip profile from x = 25 to x = 32.
          draw.line(
            (beam-length, -cube-half, cube-half),
            (cube-end, -cube-half, cube-half),
            (cube-end, cube-half, cube-half),
            (beam-length, cube-half, cube-half),
            close: true,
            fill: cube-fill,
            stroke: none,
          )
          draw.line(
            (beam-length, -cube-half, -cube-half),
            (cube-end, -cube-half, -cube-half),
            (cube-end, -cube-half, cube-half),
            (beam-length, -cube-half, cube-half),
            close: true,
            fill: cube-fill,
            stroke: none,
          )
          draw.line(
            (cube-end, -cube-half, -cube-half),
            (cube-end, cube-half, -cube-half),
            (cube-end, cube-half, cube-half),
            (cube-end, -cube-half, cube-half),
            close: true,
            fill: cube-fill,
            stroke: none,
          )

          // One rounded silhouette and three crease lines define the cube.
          draw.line(
            (beam-length, -cube-half, -cube-half),
            (cube-end, -cube-half, -cube-half),
            (cube-end, cube-half, -cube-half),
            (cube-end, cube-half, cube-half),
            (beam-length, cube-half, cube-half),
            (beam-length, -cube-half, cube-half),
            close: true,
            stroke: shape-stroke,
          )
          draw.line(
            (cube-end, -cube-half, -cube-half),
            (cube-end, -cube-half, cube-half),
            stroke: shape-stroke,
          )
          draw.line(
            (beam-length, -cube-half, cube-half),
            (cube-end, -cube-half, cube-half),
            stroke: shape-stroke,
          )
          draw.line(
            (cube-end, -cube-half, cube-half),
            (cube-end, cube-half, cube-half),
            stroke: shape-stroke,
          )

          // Plot the dashed construction line after all solid geometry and
          // immediately before the coordinate axes.
          draw.line(
            (projectile-x, -cube-half, 0),
            (projectile-x, projectile-front-y, 0),
            stroke: guide-stroke,
          )

          // Radius-0.5 cylinder extruded four units in the positive y direction.
          // The rear cap is drawn first so the side surface masks its near arc.
          draw.on-xz(y: projectile-back-y, {
            draw.circle(
              (projectile-x, 0),
              radius: projectile-radius,
              fill: color-surface-strong,
              stroke: shape-stroke,
            )
          })
          draw.line(
            (
              projectile-x + projectile-rim-x,
              projectile-front-y,
              -projectile-rim-z,
            ),
            (
              projectile-x + projectile-rim-x,
              projectile-back-y,
              -projectile-rim-z,
            ),
            (
              projectile-x - projectile-rim-x,
              projectile-back-y,
              projectile-rim-z,
            ),
            (
              projectile-x - projectile-rim-x,
              projectile-front-y,
              projectile-rim-z,
            ),
            close: true,
            fill: color-surface-strong,
            stroke: none,
          )
          draw.on-xz(y: projectile-front-y, {
            draw.circle(
              (projectile-x, 0),
              radius: projectile-radius,
              fill: color-surface-strong,
              stroke: shape-stroke,
            )
          })
          draw.line(
            (
              projectile-x + projectile-rim-x,
              projectile-front-y,
              -projectile-rim-z,
            ),
            (
              projectile-x + projectile-rim-x,
              projectile-back-y,
              -projectile-rim-z,
            ),
            stroke: shape-stroke,
          )
          draw.line(
            (
              projectile-x - projectile-rim-x,
              projectile-front-y,
              projectile-rim-z,
            ),
            (
              projectile-x - projectile-rim-x,
              projectile-back-y,
              projectile-rim-z,
            ),
            stroke: shape-stroke,
          )

          // Velocity arrow parallel to the cylinder on the xy plane.
          draw.on-xy(z: 0, {
            draw.line(
              (velocity-arrow-x, projectile-front-y),
              (velocity-arrow-x, projectile-back-y),
              stroke: motion-arrow-stroke,
              mark: (fill: color-displacement, ..arrow-medium),
            )
            draw.content(
              (
                velocity-arrow-x + 0.8,
                projectile-front-y + projectile-length / 2,
              ),
              anchor: "west",
              text(fill: color-displacement)[$v$],
            )
          })

          // Standard ticked displacement arrow, parallel to xy at z = 3.5.
          draw.on-xy(z: cube-half, {
            displacement-indicator(
              (displacement-arrow-x, -cube-half),
              length: displacement-arrow-length,
              angle: 90deg,
              label: text(fill: color-displacement)[$u(t)$],
              label-offset: -1.7,
              extension: 0.7,
              arrow: arrow-medium,
              stroke: motion-arrow-stroke,
            )
          })

          draw.line(
            (x-axis-start, 0, 0),
            (x-axis-length, 0, 0),
            stroke: axis-stroke,
            mark: (fill: color-ink, ..arrow-medium),
          )
          draw.line(
            (0, y-axis-start, 0),
            (0, y-axis-length, 0),
            stroke: axis-stroke,
            mark: (fill: color-ink, ..arrow-medium),
          )
          draw.line(
            (0, 0, z-axis-start),
            (0, 0, z-axis-length),
            stroke: axis-stroke,
            mark: (fill: color-ink, ..arrow-medium),
          )

          draw.content((x-axis-length + 0.8, 0, 0), anchor: "west", [$x$])
          draw.content((0, y-axis-length + 0.8, 0), anchor: "south", [$y$])
          draw.content((0, 0, z-axis-length + 0.8), anchor: "east", [$z$])

          callout(
            (0, 0, -5),
            (7, -4, -4),
            [Fixed wall],
            anchor: "west",
          )
          callout(
            (projectile-x, projectile-front-y, 0),
            (24, -23, 0.35),
            [Projectile mass, #text(fill: color-secondary)[$m$]],
            anchor: "east",
          )
          callout(
            (projectile-x, 0, cube-half),
            (31, 1, 5.75),
            [Mass, #text(fill: color-secondary)[$M$]],
            anchor: "west",
          )
        },
      )
    },
  ),
)
