#import "../../style.typ": plot-panel
#let d = json("../../data/actuation.json")

#let thrust-map() = plot-panel(
  "M200 static curve and local actuator approximation",
  "Motor command (%)",
  "Thrust per motor (N)",
  (
    (x: d.curve.percent, y: d.curve.raw16_N, label: [Raw M200 at 16 V]),
    (x: d.curve.percent, y: d.curve.installed_N, label: [Installed scaled map]),
    (x: d.curve.tangent_percent, y: d.curve.local_tangent_N, label: [Tangent near 1 m/s trim]),
  ),
  xlim: (-100, 100),
  ylim: (-32, 58),
  height: 2.65in,
)


#set document(title: "BlueBoat. 03 thrust map", author: "J.C. Vaught")
#set page(width: 7.06in, height: auto, margin: 0pt)
#set text(font: "Times New Roman", size: 9pt)
#align(center, thrust-map())
