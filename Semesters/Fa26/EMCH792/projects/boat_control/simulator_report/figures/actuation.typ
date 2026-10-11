#import "../style.typ": plot-panel
#let d = json("../data/actuation.json")

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
