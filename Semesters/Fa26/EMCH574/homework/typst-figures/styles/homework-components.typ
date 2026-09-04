#import "figure.typ": *

// Homework-specific constructors built from the public figure-system styles.
// Mathematical labels use the same teal as the homework document.

#let homework-math(body) = text(fill: color-secondary, body)

#let pendulum-schematic(
  pivot,
  rod-length: 43,
  support-width: 20,
  support-height: 4,
  mass-radius: 5,
  mass-label: [$m$],
  length-label: [$L$],
) = {
  let pivot-x = pivot.at(0)
  let pivot-y = pivot.at(1)
  let mass-top = pivot-y - rod-length
  let mass-center-y = mass-top - mass-radius

  fixed-support(
    (pivot-x - support-width / 2, pivot-y),
    length: support-width,
    direction: 0deg,
    hatch-side: 1,
  )
  draw.line(
    pivot,
    (pivot-x, mass-top),
    ..mechanics-line-style,
  )
  draw.circle(
    pivot,
    radius: 0.72,
    fill: color-background,
    stroke: mechanics-line-style.stroke,
  )
  draw.circle(
    (pivot-x, mass-center-y),
    radius: mass-radius,
    fill: mechanics-body-style.fill,
    stroke: mechanics-body-style.stroke,
  )
  draw.content(
    (pivot-x, mass-center-y),
    homework-math(mass-label),
  )
  draw.content(
    (pivot-x + 3.2, pivot-y - rod-length / 2),
    anchor: "west",
    homework-math(length-label),
  )
}

#let projectile-indicator(
  start,
  length: 16,
  label: [$m, v$],
  label-offset: 4.5,
) = {
  let start-x = start.at(0)
  let start-y = start.at(1)
  draw.line(
    start,
    (start-x + length, start-y),
    ..mechanics-force-style,
  )
  draw.content(
    (start-x + length / 2, start-y - label-offset),
    homework-math(label),
  )
}

#let horizontal-spring-mass(
  origin,
  spring-length: 22,
  mass-width: 11,
  mass-height: 11,
  displacement-length: 18,
) = {
  let origin-x = origin.at(0)
  let origin-y = origin.at(1)
  let mass-left = origin-x + spring-length
  let mass-right = mass-left + mass-width
  let mass-bottom = origin-y - mass-height / 2
  let mass-top = origin-y + mass-height / 2

  fixed-support(
    (origin-x, origin-y + 7.5),
    length: 15,
    direction: 270deg,
    hatch-side: -1,
  )
  linear-spring(
    origin,
    length: spring-length,
    coils: 4,
    amplitude: 2.4,
    lead: 3.5,
  )
  draw.content(
    (origin-x + spring-length / 2, origin-y + 4.6),
    homework-math[$k$],
  )
  draw.rect(
    (mass-left, mass-bottom),
    (mass-right, mass-top),
    ..mechanics-body-style,
  )
  draw.content(
    ((mass-left + mass-right) / 2, origin-y),
    homework-math[$m$],
  )
  displacement-indicator(
    (mass-left, mass-top + 4),
    length: displacement-length,
    label: homework-math[$u(t)$],
    label-offset: 2.6,
    extension: 2,
  )
}

// Cantilever beam with a rectangular tip mass and transverse displacement.
// This constructor is shared by the vertical-flexure challenge problems so
// their beam, dimension, and cross-section conventions stay identical.
#let tip-mass-cantilever(
  origin,
  beam-length: 58,
  beam-height: 2.6,
  mass-width: 12,
  mass-height: 12,
  show-cross-section: true,
) = {
  let x = origin.at(0)
  let y = origin.at(1)
  let tip-x = x + beam-length
  let mass-left = tip-x
  let mass-right = mass-left + mass-width
  let mass-bottom = y - mass-height / 2
  let mass-top = y + mass-height / 2
  let outline = (
    paint: color-ink,
    thickness: 1.0pt,
    cap: "butt",
    join: "miter",
  )
  let dimension-y = y + 13

  // Reference extensions are the back layer so the wall, beam, and mass mask
  // their endpoints cleanly.
  draw.line(
    (x, y + beam-height / 2),
    (x, dimension-y),
    stroke: mechanics-reference-style.stroke,
  )
  draw.line(
    (tip-x, mass-top),
    (tip-x, dimension-y),
    stroke: mechanics-reference-style.stroke,
  )

  fixed-support(
    (x, y - 10),
    length: 20,
    direction: 90deg,
    hatch-side: 1,
  )
  draw.rect(
    (x, y - beam-height / 2),
    (tip-x, y + beam-height / 2),
    fill: color-surface,
    stroke: outline,
  )
  draw.rect(
    (mass-left, mass-bottom),
    (mass-right, mass-top),
    ..mechanics-body-style,
  )
  draw.content(
    ((mass-left + mass-right) / 2, y),
    homework-math[$m$],
  )

  draw.line(
    (x, dimension-y),
    (tip-x, dimension-y),
    stroke: (
      paint: color-ink,
      thickness: 0.75pt,
      cap: "butt",
    ),
    mark: (
      start: arrow-head-shape,
      fill: color-ink,
      ..arrow-small,
    ),
  )
  draw.content(((x + tip-x) / 2, dimension-y + 3), homework-math[$L$])
  draw.content(
    ((x + tip-x) / 2, y - 7),
    homework-math[$E, h, b$],
  )
  displacement-indicator(
    (mass-right + 2, mass-bottom),
    length: 9,
    angle: -90deg,
    label: homework-math[$u(t)$],
    label-offset: 4,
    extension: 2,
  )

  if show-cross-section {
    let section-x = (x + tip-x) / 2
    let section-y = y - 20
    draw.rect(
      (section-x - 6, section-y - 2),
      (section-x + 6, section-y + 2),
      fill: color-surface,
      stroke: outline,
    )
    draw.content((section-x, section-y + 4.2), homework-math[$b$])
    draw.content(
      (section-x + 10, section-y),
      anchor: "west",
      homework-math[$h$],
    )
  }
}

// Vertical flex-beam pendulum used both alone and with an incoming projectile.
#let hanging-flex-beam(
  origin,
  beam-length: 52,
  mass-width: 13,
  mass-height: 13,
  mass-label: [$m$],
  projectile: false,
) = {
  let x = origin.at(0)
  let top-y = origin.at(1)
  let tip-y = top-y - beam-length
  let outline = (
    paint: color-ink,
    thickness: 1.0pt,
    cap: "butt",
    join: "miter",
  )

  fixed-support(
    (x - 15, top-y),
    length: 30,
    direction: 0deg,
    hatch-side: 1,
  )
  draw.rect(
    (x - 1.4, tip-y),
    (x + 1.4, top-y),
    fill: color-surface,
    stroke: outline,
  )
  draw.rect(
    (x - mass-width / 2, tip-y - mass-height),
    (x + mass-width / 2, tip-y),
    ..mechanics-body-style,
  )
  draw.content(
    (x, tip-y - mass-height / 2),
    homework-math(mass-label),
  )
  draw.content(
    (x - 5, top-y - beam-length / 2),
    anchor: "east",
    homework-math[$E, h, b$],
  )
  draw.content(
    (x + 5, top-y - beam-length / 2),
    anchor: "west",
    homework-math[$L$],
  )

  if projectile {
    projectile-indicator(
      (x - 31, tip-y - mass-height / 2),
      length: 20,
      label: [$m, v$],
      label-offset: 5,
    )
  }
}
