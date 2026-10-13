#import "../../style.typ": plot-panel
#let d = json("../../data/actuation.json")

#let reversal-response() = plot-panel(
  "Configured motor response to forward-to-reverse step",
  "Time after command application (s)",
  "Motor thrust (N)",
  (
    (x: d.step.time_s, y: d.step.port_N, label: [Port, gain 0.95]),
    (x: d.step.time_s, y: d.step.starboard_N, label: [Starboard, gain 1.05]),
  ),
  xlim: (0, 1.5),
  ylim: (-15, 24),
  height: 2.55in,
)

#set document(title: "BlueBoat. 04 motor reversal", author: "J.C. Vaught")
#set page(width: 7.06in, height: auto, margin: 0pt)
#set text(font: "Times New Roman", size: 9pt)
#align(center, reversal-response())
