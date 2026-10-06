#import "@preview/cetz:0.5.2" as cetz
#import "@preview/lilaq:0.6.0" as lq

#set page(width: 6.5in, height: 3in, margin: 0pt)
#set text(font: "Latin Modern Roman", size: 10pt, fill: black)
#show math.equation: set text(font: "Latin Modern Math")

#let ink = rgb("#000000")
#let beam-color = lq.color.map.petroff10.at(0)
#let target-color = lq.color.map.petroff10.at(1)
#let arrow(color) = (end: "stealth", fill: color, length: 2.4mm, width: 1.5mm)
#let origin = (18, 42)
#let ray-length = 120
#let half-angle = 9deg
#let target-angle = -14deg
#let polar(radius, angle) = (
  origin.at(0) + radius * calc.cos(angle),
  origin.at(1) + radius * calc.sin(angle),
)

#align(center + horizon)[
  #cetz.canvas(length: 1mm, {
    import cetz.draw: *

    rect((0, 0), (165, 76), fill: white, stroke: none)

    // Exact symmetric half-power directions about the beam centerline.
    line(origin, polar(ray-length, half-angle),
      stroke: (paint: beam-color, thickness: 0.8pt, dash: "dashed"))
    line(origin, polar(ray-length, -half-angle),
      stroke: (paint: beam-color, thickness: 0.8pt, dash: "dashed"))
    line(origin, polar(ray-length + 5, 0deg), stroke: 1.1pt + beam-color, mark: arrow(beam-color))

    // Target direction lies beyond the lower half-power direction.
    let target-center = polar(116, target-angle)
    line(origin, polar(109, target-angle), stroke: 1.1pt + target-color, mark: arrow(target-color))
    rect(
      (target-center.at(0) - 2.3, target-center.at(1) - 2.3),
      (target-center.at(0) + 2.3, target-center.at(1) + 2.3),
      fill: ink,
      stroke: ink,
    )

    // Angular definitions. The arc endpoints use the same angles as the rays.
    arc(origin, radius: 28, start: -half-angle, stop: half-angle, anchor: "origin",
      stroke: 0.9pt + beam-color)
    arc(origin, radius: 38, start: target-angle, stop: 0deg, anchor: "origin",
      stroke: 0.9pt + target-color)

    // Radar symbol and uncluttered labels.
    rect((origin.at(0) - 2.5, origin.at(1) - 2.5),
      (origin.at(0) + 2.5, origin.at(1) + 2.5), fill: ink, stroke: ink)
    content((18, 53), anchor: "center", [Radar])
    content((101, 46), anchor: "center", [Beam centerline])
    content((101, 61), anchor: "center", [Half-power directions])
    content((47, 49), anchor: "center", [$beta$])
    content((63, 38), anchor: "center", [$epsilon_i$])
    content((139, 14), anchor: "west", [Target])
    content((106, 7), anchor: "center", [Attenuated. $B_i < 1 / 2$])
  })
]
