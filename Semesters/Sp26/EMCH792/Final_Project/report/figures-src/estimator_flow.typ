#import "@preview/cetz:0.4.2"

#set page(
  width: auto,
  height: auto,
  margin: (x: 14pt, y: 14pt),
  fill: white,
)

#set text(
  font: "Times New Roman",
  size: 9.6pt,
  fill: rgb("#000000"),
)

#cetz.canvas(length: 1cm, {
  import cetz.draw: *

  let garnet = rgb("#73000A")
  let atlantic = rgb("#466A9F")
  let horseshoe = rgb("#65780B")
  let sand = rgb("#FFF2E3")
  let light = rgb("#ECECEC")
  let dark = rgb("#363636")

  set-style(
    stroke: (paint: dark, thickness: 0.8pt),
    mark: (fill: dark, scale: 0.78),
    rect: (stroke: (paint: dark, thickness: 0.85pt), fill: white),
  )

  let box(name, cx, cy, label, fill: white, w: 3.0, h: 1.0) = {
    rect((cx - w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), name: name, fill: fill)
    content(name, label)
  }

  box("inputs", 0.0, 6.0, [
    Inputs \
    $delta_f, a$
  ], fill: sand, w: 2.35)

  box("predict", 0.0, 4.2, [
    Predict state \
    Euler or RK4
  ], fill: light, w: 2.95)

  box("update1", 0.0, 2.2, [
    Update with $y_1$ \
    Scalar NIS gate
  ], fill: sand, w: 2.95)

  box("update2", 0.0, 0.2, [
    Update with $y_2$ \
    Scalar NIS gate
  ], fill: sand, w: 2.95)

  box("posterior", 0.0, -1.8, [
    Posterior state \
    and covariance
  ], fill: light, w: 3.1)

  box("model1", 4.1, 2.2, [
    Measurement model \
    $y_1 = sqrt(x^2 + y^2)$
  ], w: 3.45)

  box("model2", 4.0, 0.2, [
    Measurement model \
    $y_2 = psi^3$
  ], w: 3.0)

  line((0.0, 5.48), (0.0, 4.72),
    mark: (end: "stealth", fill: atlantic),
    stroke: (paint: atlantic, thickness: 0.95pt))
  line((0.0, 3.68), (0.0, 2.72),
    mark: (end: "stealth", fill: atlantic),
    stroke: (paint: atlantic, thickness: 0.95pt))
  line((0.0, 1.68), (0.0, 0.72),
    mark: (end: "stealth", fill: atlantic),
    stroke: (paint: atlantic, thickness: 0.95pt))
  line((0.0, -0.32), (0.0, -1.28),
    mark: (end: "stealth", fill: atlantic),
    stroke: (paint: atlantic, thickness: 0.95pt))

  line((2.36, 2.2), (1.58, 2.2),
    mark: (end: "stealth", fill: garnet),
    stroke: (paint: garnet, thickness: 0.95pt))
  line((2.48, 0.2), (1.58, 0.2),
    mark: (end: "stealth", fill: horseshoe),
    stroke: (paint: horseshoe, thickness: 0.95pt))

  content((-0.82, 3.14), text(size: 8.2pt, fill: atlantic)[time update])
})
