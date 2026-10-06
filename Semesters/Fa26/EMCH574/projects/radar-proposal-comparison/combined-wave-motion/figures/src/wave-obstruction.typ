#import "@preview/cetz:0.5.2" as cetz

#set page(width: 6.5in, height: 3.0in, margin: 0pt)
#set text(font: "Latin Modern Roman", size: 10pt, fill: black)
#show math.equation: set text(font: "Latin Modern Math")

#let arrow = (end: "stealth", fill: black, length: 2.5mm, width: 1.6mm)
#let dimension = (
  start: "stealth",
  end: "stealth",
  fill: black,
  length: 2.2mm,
  width: 1.4mm,
)

#align(center + horizon)[
  #cetz.canvas(length: 1mm, {
    import cetz.draw: *

    let x-r = 24
    let y-r = 53
    // The direct ray terminates at the target's left face. The target body is
    // centered at (151, 28), so its left face is exactly (149, 28).
    let x-t = 149
    let y-t = 28
    let x-c = 92
    let surface(x) = 18 + 1.8 * calc.cos((x - x-c) * 0.17) + 28 * calc.exp(-calc.pow((x - x-c) / 18, 2))
    let ray(x) = y-r + (y-t - y-r) * (x - x-r) / (x-t - x-r)
    let y-c = surface(x-c)
    let y-ray-c = ray(x-c)
    let sea = range(0, 155).map(i => (7 + i, surface(7 + i)))

    rect((0, 0), (165, 76), fill: white, stroke: none)

    // Direct propagation path. The construction uses the same straight line
    // for the radar, crest-clearance dimension, and target point.
    line(
      (x-r, y-r),
      (x-t, y-t),
      stroke: (paint: black, thickness: 1.05pt, dash: "dashed"),
      mark: arrow,
    )

    // Water fill and free surface. Drawing the surface after the ray makes the
    // obstructing interface visually dominant at the crossing.
    line(
      ..sea,
      (162, 5),
      (7, 5),
      close: true,
      fill: white,
      stroke: none,
    )
    line(..sea, stroke: 1.35pt + black)

    // Radar vessel and phase center.
    line(
      (10, 21),
      (18, 17.5),
      (33, 17.5),
      (39, 21),
      close: true,
      fill: white,
      stroke: 1.15pt + black,
    )
    line((24, 20), (24, 50.5), stroke: 1.15pt + black)
    rect((21.8, 50.5), (26.2, 55.5), fill: black, stroke: black)

    // Surface-connected target. The mast terminates at the target point used
    // by the direct-ray construction.
    let y-local = surface(151)
    line((148.2, y-local), (151, y-local - 2.2), (153.8, y-local), close: true, fill: white, stroke: 1pt + black)
    line((151, y-local - 1.5), (151, 26), stroke: 1.15pt + black)
    rect((149, 26), (153, 30), fill: white, stroke: 1.15pt + black)

    // Exact vertical crest intrusion above the direct ray.
    line((x-c - 2.4, y-c), (x-c + 2.4, y-c), stroke: 0.75pt + black)
    line((x-c - 2.4, y-ray-c), (x-c + 2.4, y-ray-c), stroke: 0.75pt + black)
    line(
      (x-c, y-ray-c + 0.45),
      (x-c, y-c - 0.45),
      stroke: 1pt + black,
      mark: dimension,
    )
    content((97, (y-c + y-ray-c) / 2), anchor: "west", [#box(fill: white, inset: 1.3pt)[$d_c$]])

    // Labels and leaders.
    content((9, 62), anchor: "west", [Radar phase center])

    content((46, 58), anchor: "west", [Direct radar--target ray])

    content((91, 66), anchor: "center", [Obstructing wave crest])
    line((91, 62.5), (92, y-c + 1.2), stroke: 0.8pt + black, mark: arrow)

    content((162, 35), anchor: "east", [Exposed target])

    content((129, 10), anchor: "center", [Sea surface])
  })
]
