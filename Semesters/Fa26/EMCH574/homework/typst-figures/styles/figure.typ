#import "@preview/cetz:0.5.2" as cetz
#import "colors.typ": *
#import "typography.typ": *
#import "dimensions.typ": *
#import "diagrams.typ": *
#import "mechanics.typ": *
#import "mechanics-components.typ": *
#import "plots.typ": *

#let cetz-canvas = cetz.canvas
#let draw = cetz.draw

// Place a mechanics diagram on the standard full-width figure artboard.
// Panel placement keeps independently generated left/right diagrams aligned
// to the same page-width reference without changing their authored scale.
#let full-width-artboard(body, placement: "center") = {
  assert(
    placement in ("center", "left", "right"),
    message: "placement must be center, left, or right",
  )
  let artboard-width = figure-content-width("full")
  let panel-width = artboard-width / 2
  let positioned = if placement == "center" {
    align(center, body)
  } else if placement == "left" {
    align(left, box(width: panel-width, align(center, body)))
  } else {
    align(right, box(width: panel-width, align(center, body)))
  }
  box(width: artboard-width, positioned)
}

// Standard negative-feedback summing junction. The offsets are proportional
// to the radius so the operator marks retain their placement at custom sizes.
#let summing-node(
  position,
  name: "sum",
  radius: diagram-node-radius,
) = {
  let x = position.at(0)
  let y = position.at(1)
  draw.circle(
    position,
    radius: radius,
    name: name,
    ..diagram-summing-style,
  )
  draw.content(
    (x - 0.4667 * radius, y + 0.0667 * radius),
    text(fill: color-on-light)[$+$],
  )
  draw.content(
    (x, y - 0.5833 * radius),
    text(fill: color-on-light)[$-$],
  )
}

// All standalone figures use a one-page, content-sized canvas. The 2 pt page
// margin is a clipping guard for strokes and arrowheads, not a paper margin.
#let standalone(body) = {
  set page(
    width: auto,
    height: auto,
    margin: figure-page-margin,
    // Keep the standalone PDF page transparent so figures inherit the
    // surrounding LaTeX page, example-box, or review-gallery background.
    fill: none,
  )
  figure-typography(body)
}
