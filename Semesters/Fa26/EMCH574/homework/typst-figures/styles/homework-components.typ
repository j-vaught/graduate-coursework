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
  displacement-length: 13,
) = {
  let origin-x = origin.at(0)
  let origin-y = origin.at(1)
  let mass-left = origin-x + spring-length
  let mass-right = mass-left + mass-width
  let mass-bottom = origin-y - mass-height / 2
  let mass-top = origin-y + mass-height / 2
  let displacement-y = mass-top + 3

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
  draw.line(
    (mass-left - 1, displacement-y),
    (mass-left + displacement-length, displacement-y),
    stroke: (
      paint: color-displacement,
      thickness: line-normal,
      dash: "dashed",
      cap: "butt",
      join: "miter",
    ),
    mark: (fill: color-displacement, ..arrow-medium),
  )
  draw.content(
    (mass-left + displacement-length / 2 - 0.5, displacement-y + 2.5),
    homework-math[$u$],
  )
}
