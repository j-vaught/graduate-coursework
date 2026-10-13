#import "../../style.typ": cetz, ink, teal, pale, arrow, plot-panel

#let drag() = {
  import "../../style.typ": plot-panel
  let xs = range(81).map(i => -2 + i * 0.05)
  let nonlinear = xs.map(x => 4*x + 10*x*calc.abs(x))
  let tangent = xs.map(x => 14 + 24*(x - 1))
  plot-panel("Surge drag and tangent at U = 1 m/s", "Surge speed u (m/s)", "Drag Du (N)",
    ((x: xs, y: nonlinear, label: [nonlinear drag]), (x: xs, y: tangent, label: [local tangent]),),
    xlim: (-2, 2), ylim: (-65, 55), height: 2.4in)
}

#set document(title: "BlueBoat. 02 surge drag", author: "J.C. Vaught")
#set page(width: 7.06in, height: auto, margin: 0pt)
#set text(font: "Times New Roman", size: 9pt)
#align(center, drag())
