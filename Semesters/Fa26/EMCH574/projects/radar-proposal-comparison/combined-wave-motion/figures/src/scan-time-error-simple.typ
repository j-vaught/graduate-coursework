#import "@preview/cetz:0.5.2" as cetz
#import "@preview/lilaq:0.6.0" as lq

#set page(width: 6.5in, height: 2.6in, margin: 0pt)
#set text(font: "Latin Modern Roman", size: 10pt, fill: black)
#show math.equation: set text(font: "Latin Modern Math")

#let actual-color = lq.color.map.petroff10.at(0)
#let assumed-color = lq.color.map.petroff10.at(1)
#let actual-radar = (25, 16)
#let assumed-radar = (75, 16)
#let measured-vector = (45, 37)
#let true-target = (actual-radar.at(0) + measured-vector.at(0), actual-radar.at(1) + measured-vector.at(1))
#let mapped-target = (assumed-radar.at(0) + measured-vector.at(0), assumed-radar.at(1) + measured-vector.at(1))
#let arrow = (end: "stealth", fill: black, length: 2.4mm, width: 1.5mm)

#align(center + horizon)[
  #cetz.canvas(length: 1mm, {
    import cetz.draw: *
    rect((0, 0), (165, 66), fill: white, stroke: none)

    // The same range-bearing vector is mapped from two different origins.
    line(actual-radar, true-target, stroke: 1.2pt + actual-color)
    line(assumed-radar, mapped-target,
      stroke: (paint: assumed-color, thickness: 1.2pt, dash: "dashed"))

    // Only the reconstructed-position displacement is annotated.
    line((true-target.at(0) + 2.2, true-target.at(1)),
      (mapped-target.at(0) - 2.2, mapped-target.at(1)),
      stroke: 0.9pt + black, mark: arrow)
    content((95, 45), [Position error])

    circle(actual-radar, radius: 2mm, fill: white, stroke: 1.1pt + actual-color)
    circle(assumed-radar, radius: 2mm, fill: white, stroke: 1.1pt + assumed-color)
    circle(true-target, radius: 1.8mm, fill: actual-color, stroke: 1pt + actual-color)
    circle(mapped-target, radius: 1.8mm, fill: white, stroke: 1.1pt + assumed-color)

    content((25, 7), [Actual radar position])
    content((75, 7), [Assumed midpoint position])
    content((70, 61), [True target])
    content((120, 61), [Reconstructed target])
  })
]
