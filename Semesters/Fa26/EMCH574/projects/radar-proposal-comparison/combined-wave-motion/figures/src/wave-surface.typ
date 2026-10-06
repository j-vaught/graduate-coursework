#import "@preview/lilaq:0.6.0" as lq
#import "@preview/tiptoe:0.4.0" as tiptoe
#set page(width: auto, height: auto, margin: 4mm)
#set text(font: "Latin Modern Roman", size: 10pt, fill: black)
#show math.equation: set text(font: "Latin Modern Math")
#let field = json("../../data/wave-surface.json")
#let surface-values = field.snapshots.at(0).elevation_m
#let object = field.obstruction_example
// Beam rays are schematic because x and elevation use different display scales.
// They do not set a numerical antenna beamwidth in the physical model.
#let radar-x = 25
#let radar-height = 0.8
#let end-x = 475
#let spread = 0.9
#let x-scale = 150 / 500
#let y-scale = 60 / 2.8
#let half-angle = calc.atan(y-scale * spread / (x-scale * (end-x - radar-x)))
#let arc-x-radius = 95
#let arc-y-radius = arc-x-radius * x-scale / y-scale
#let beam-arc = range(0, 41).map(i => {
  let angle = -half-angle + 2 * half-angle * i / 40
  (radar-x + arc-x-radius * calc.cos(angle),
   radar-height + arc-y-radius * calc.sin(angle))
})
#lq.diagram(
  width: 150mm,
  height: 60mm,
  xlim: (0, 500),
  ylim: (-1, 1.8),
  xlabel: [Distance $x$ (m)],
  ylabel: [Elevation $eta$ (m)],
  xaxis: (ticks: (0, 100, 200, 300, 400, 500), subticks: none),
  yaxis: (ticks: (-1, -0.5, 0, 0.5, 1, 1.5), subticks: none),
  legend: (position: bottom + left, pad: 5pt, radius: 0pt),
  lq.plot(field.x_m, surface-values, label: [Surface at $t = 0$ s], mark: none),
  lq.plot((0, 500), (0, 0), label: [Mean water level], mark: none),
  lq.line((radar-x, radar-height), (end-x, radar-height),
    stroke: 0.9pt + black, tip: tiptoe.stealth),
  lq.line((radar-x, radar-height), (end-x, radar-height + spread),
    stroke: (paint: black, thickness: 0.8pt, dash: "dashed"),
    tip: tiptoe.stealth, label: [Half-power rays]),
  lq.line((radar-x, radar-height), object.lower_schematic_boundary_contact_m,
    stroke: (paint: black, thickness: 0.8pt, dash: "dashed"),
    tip: tiptoe.stealth),
  lq.path(..beam-arc, stroke: 0.8pt + black),
  lq.path(
    (object.object_x_m - 4, object.object_base_m),
    (object.object_x_m + 4, object.object_base_m),
    (object.object_x_m + 4, object.object_top_m),
    (object.object_x_m - 4, object.object_top_m),
    closed: true, fill: black, stroke: 0.7pt + black, z-index: 15,
  ),
  lq.place(object.object_x_m, -0.68, [Object]),
  lq.place(145, 1.3, [Vertical beamwidth $beta$]),
  lq.place(375, 0.96, [Horizontal centerline]),
  lq.place(radar-x, radar-height,
    circle(radius: 3pt, fill: white, stroke: 0.8pt + black)),
  lq.place(25, 1.08, [Radar]),
)

#v(3mm)
#align(center)[
  #block(width: 150mm)[
    Wave obstruction for $H_s = 1$ m, $T_p = 9$ s, and $h = 50$ m.
    The intervening crest prevents direct geometric rays from reaching the object.
  ]
]
