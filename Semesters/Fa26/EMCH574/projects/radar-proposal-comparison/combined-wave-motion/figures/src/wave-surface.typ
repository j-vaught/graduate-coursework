#import "@preview/lilaq:0.6.0" as lq
#set page(width: auto, height: auto, margin: 4mm)
#set text(font: "Latin Modern Roman", size: 10pt, fill: black)
#show math.equation: set text(font: "Latin Modern Math")
#let field = json("../../data/wave-surface.json")
#let surface-values = field.snapshots.at(0).elevation_m
#align(center)[
  $H_s = 1$ m, $T_p = 9$ s, $h = 50$ m
]
#v(4mm)
#lq.diagram(
  width: 150mm,
  height: 46mm,
  xlim: (0, 500),
  ylim: (-1, 1),
  xlabel: [Distance $x$ (m)],
  ylabel: [Elevation $eta$ (m)],
  xaxis: (ticks: (0, 100, 200, 300, 400, 500), subticks: none),
  yaxis: (ticks: (-1, -0.5, 0, 0.5, 1), subticks: none),
  legend: (position: bottom + right, dy: -100% - 4pt, radius: 0pt),
  lq.plot(field.x_m, surface-values, label: [Surface at $t = 0$ s], mark: none),
  lq.plot((0, 500), (0, 0), label: [Mean water level], mark: none),
  lq.place(25, 0.8, circle(radius: 3pt, fill: white, stroke: 0.8pt + black)),
  lq.place(40, 0.8, [Radar], align: left + horizon),
)
