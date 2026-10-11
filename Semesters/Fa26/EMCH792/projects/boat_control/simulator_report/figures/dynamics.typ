#import "../style.typ": cetz, ink, teal, pale, arrow, plot-panel

#let coordinates() = {
  import cetz.draw: line, content, rect
  set text(font: "Times New Roman", size: 9pt)
  cetz.canvas(length: 0.8cm, {
    // Left panel: fixed earth frame and rotated body axes.
    content((0.55, 4.0), [Frame convention])
    let o = (0.95, 1.0)
    line(o, (3.05, 1.0), mark: (end: "stealth", fill: ink, stroke: ink), stroke: 1pt + ink)
    line(o, (0.95, 3.25), mark: (end: "stealth", fill: ink, stroke: ink), stroke: 1pt + ink)
    content((3.15, 1.0), [east $E$], anchor: "west")
    content((0.95, 3.36), [north $N$], anchor: "south")
    rect((o.at(0)-0.045,o.at(1)-0.045),(o.at(0)+0.045,o.at(1)+0.045),fill:ink,stroke:none)
    content((0.98, 0.55), [origin], anchor: "west")

    let p = (4.2, 1.75)
    let c = calc.cos(35deg)
    let s = calc.sin(35deg)
    let f = (c, s)
    let l = (-s, c)
    rect((p.at(0)-0.045,p.at(1)-0.045),(p.at(0)+0.045,p.at(1)+0.045),fill:ink,stroke:none)
    line(p, (p.at(0) + 1.85 * f.at(0), p.at(1) + 1.85 * f.at(1)),
      mark: (end: "stealth", fill: teal, stroke: teal), stroke: 1.25pt + teal)
    line(p, (p.at(0) + 1.3 * l.at(0), p.at(1) + 1.3 * l.at(1)),
      mark: (end: "stealth", fill: teal, stroke: teal), stroke: 1.25pt + teal)
    // East reference and body-forward ray bound the positive heading angle.
    line(p, (p.at(0) + 0.9, p.at(1)), stroke: 0.8pt + ink)
    rect((4.725,1.935),(4.795,2.005),fill:ink,stroke:none)
    line((5.45, 2.35), (4.79, 1.99), stroke: 0.7pt + ink)
    content((5.48, 2.4), [$psi$], anchor: "west")
    content((5.6, 2.98), [forward $x_b$], anchor: "west")
    content((2.95, 2.62), [left $y_b$], anchor: "east")

    // Divider separates the earth/body-frame view from actuator geometry.
    line((8.35, 0.45), (8.35, 4.15), stroke: 0.6pt + luma(65%))

    // Right panel: square-ended twin hulls in top-down body coordinates.
    content((9.0, 4.0), [Thrust allocation])
    let x0 = 10.55
    let x1 = 14.05
    let yp = 2.65
    let ys = 1.35
    rect((x0, yp - 0.2), (x1, yp + 0.2), fill: pale, stroke: 1pt + ink)
    rect((x0, ys - 0.2), (x1, ys + 0.2), fill: pale, stroke: 1pt + ink)
    // Cross-decks show the port hull above the starboard hull in this view.
    line((10.9, yp - 0.2), (10.9, ys + 0.2), stroke: 1pt + ink)
    line((13.7, yp - 0.2), (13.7, ys + 0.2), stroke: 1pt + ink)
    content((11.05, 2.65), [port hull], anchor: "west")
    content((11.05, 1.35), [starboard hull], anchor: "west")

    // Filled stealth arrows extend forward from the corresponding hull centerlines.
    line((x1, yp), (15.25, yp), mark: (end: "stealth", fill: ink, stroke: ink), stroke: 1.25pt + ink)
    line((x1, ys), (15.25, ys), mark: (end: "stealth", fill: ink, stroke: ink), stroke: 1.25pt + ink)
    content((15.38, yp), [port thrust $T_p$], anchor: "west")
    content((15.38, ys), [starboard thrust $T_s$], anchor: "west")

    // Separation dimension spans the two thrust lines without crossing the hulls.
    line((10.0, ys), (10.0, yp), mark: (start: "stealth", end: "stealth", fill: ink, stroke: ink), stroke: 0.9pt + ink)
    line((10.05, ys), (10.45, ys), stroke: 0.7pt + ink)
    line((10.05, yp), (10.45, yp), stroke: 0.7pt + ink)
    content((9.72, 2.0), [$b$], anchor: "east")
  })
}

#let drag() = {
  import "../style.typ": plot-panel
  let xs = range(81).map(i => -2 + i * 0.05)
  let nonlinear = xs.map(x => 4*x + 10*x*calc.abs(x))
  let tangent = xs.map(x => 14 + 24*(x - 1))
  plot-panel("Surge drag and tangent at U = 1 m/s", "Surge speed u (m/s)", "Drag Du (N)",
    ((x: xs, y: nonlinear, label: [nonlinear drag]), (x: xs, y: tangent, label: [local tangent]),),
    xlim: (-2, 2), ylim: (-65, 55), height: 2.4in)
}
