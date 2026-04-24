#import "@preview/cetz:0.4.2"

#set page(
  width: auto,
  height: auto,
  margin: (x: 16pt, y: 14pt),
  fill: white,
)

#set text(
  font: "Times New Roman",
  size: 10pt,
  fill: rgb("#000000"),
)

#cetz.canvas(length: 1cm, {
  import cetz.draw: *

  let garnet = rgb("#73000A")
  let atlantic = rgb("#466A9F")
  let rose = rgb("#CC2E40")
  let horseshoe = rgb("#65780B")
  let sand = rgb("#FFF2E3")
  let light = rgb("#ECECEC")
  let dark = rgb("#363636")

  set-style(
    stroke: (paint: dark, thickness: 0.8pt),
    mark: (fill: dark, scale: 0.78),
    rect: (stroke: (paint: dark, thickness: 0.85pt), fill: white),
  )

  let box(name, cx, cy, label, fill: white, w: 2.5, h: 1.0) = {
    rect((cx - w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), name: name, fill: fill)
    content(name, label)
  }

  box("inputs", 0.0, 0.0, [Vehicle inputs $delta_f, a$], fill: sand, w: 2.8)
  box("predict", 3.35, 0.0, [State prediction Euler or RK4], fill: light, w: 3.05)
  box("sensor1", 7.15, 1.35, [Measurement model $y_1 = sqrt(x^2 + y^2)$], w: 3.7)
  box("gate1", 7.15, -0.15, [Scalar NIS gate], fill: sand, w: 2.3)
  box("sensor2", 10.95, 1.35, [Measurement model $y_2 = psi^3$], w: 3.0)
  box("gate2", 10.95, -0.15, [Scalar NIS gate], fill: sand, w: 2.3)
  box("posterior", 14.55, 0.0, [Posterior state and covariance], fill: light, w: 3.3)

  line((1.43, 0.0), (1.78, 0.0),
    mark: (end: "stealth", fill: atlantic),
    stroke: (paint: atlantic, thickness: 0.9pt))
  line((4.88, 0.0), (6.0, 0.0),
    mark: (end: "stealth", fill: atlantic),
    stroke: (paint: atlantic, thickness: 0.9pt))
  line((6.0, 0.0), (6.0, 1.35),
    mark: (end: "stealth", fill: rose),
    stroke: (paint: rose, thickness: 0.9pt))
  line((8.98, 1.35), (9.45, 1.35),
    mark: (end: "stealth", fill: garnet),
    stroke: (paint: garnet, thickness: 0.9pt))
  line((9.45, 1.35), (9.45, -0.15),
    mark: (end: "stealth", fill: rose),
    stroke: (paint: rose, thickness: 0.9pt))
  line((12.1, -0.15), (13.05, -0.15),
    mark: (end: "stealth", fill: horseshoe),
    stroke: (paint: horseshoe, thickness: 0.9pt))
  line((13.05, -0.15), (13.05, 0.0),
    mark: (end: "stealth", fill: horseshoe),
    stroke: (paint: horseshoe, thickness: 0.9pt))
  line((13.05, 0.0), (12.9 + 1.2, 0.0),
    mark: (end: "stealth", fill: atlantic),
    stroke: (paint: atlantic, thickness: 0.9pt))

  content((5.32, 0.52), text(size: 8.5pt, fill: atlantic)[Prediction step])
  content((8.85, 0.55), text(size: 8.5pt, fill: rose)[Gate $y_1$])
  content((12.55, 0.55), text(size: 8.5pt, fill: horseshoe)[Gate $y_2$])
})
