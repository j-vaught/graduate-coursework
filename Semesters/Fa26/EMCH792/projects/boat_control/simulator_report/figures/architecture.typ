#import "../style.typ": cetz, ink, teal, pale, slate, arrow, node

#let architecture() = {
  import cetz.draw: line, content
  set text(font: "Times New Roman", size: 9pt)
  cetz.canvas(length: 0.8cm, {
    // Horizontal signal path from percentage requests through propulsion and planar motion.
    node((0, 2.4), (2.6, 3.5), stack(dir: ttb, spacing: 2pt, [Motor input (%)], [port, starboard]), fill: pale)
    node((3.4, 2.4), (6.2, 3.5), stack(dir: ttb, spacing: 2pt, [Motor states], [$T_p$, $T_s$]), fill: pale)
    node((7.0, 2.4), (10.1, 3.5), stack(dir: ttb, spacing: 2pt, [Planar vessel], [$x,y,psi,u,v,r$]), fill: pale)
    node((11.0, 2.4), (13.9, 3.5), stack(dir: ttb, spacing: 2pt, [Integration and], [truth log]), fill: pale)
    line((2.6, 2.95), (3.4, 2.95), mark: (end: "stealth", fill: ink, stroke: ink), stroke: 1pt + ink)
    content((3.0, 3.8), [command %])
    line((6.2, 2.95), (7.0, 2.95), mark: (end: "stealth", fill: ink, stroke: ink), stroke: 1pt + ink)
    content((6.6, 3.8), [thrust])
    line((10.1, 2.95), (11.0, 2.95), mark: (end: "stealth", fill: ink, stroke: ink), stroke: 1pt + ink)
    content((10.55, 3.8), [state])

    // Disturbances enter the plant from below.
    node((6.7, 0.2), (10.2, 1.35), stack(dir: ttb, spacing: 2pt, [Wind and prescribed], [wave force / moment]), fill: white, stroke: 0.8pt + teal)
    line((8.45, 1.35), (8.45, 2.4), mark: (end: "stealth", fill: teal, stroke: teal), stroke: 1pt + teal)
    content((9.1, 1.9), [disturbance])

    // Truth feeds acquisition, while only delivered observations cross to a policy.
    node((10.5, -1.5), (14.2, -0.4), stack(dir: ttb, spacing: 2pt, [GNSS / IMU / stereo], [acquisition]), fill: pale)
    line((10.1, 2.7), (10.3, 2.7), stroke: 1pt + teal)
    line((10.3, 2.7), (10.3, -0.95), stroke: 1pt + teal)
    line((10.3, -0.95), (10.5, -0.95), mark: (end: "stealth", fill: teal, stroke: teal), stroke: 1pt + teal)
    content((10.6, 1.2), [truth at sample time], anchor: "west")
    node((7.0, -3.3), (10.1, -2.2), stack(dir: ttb, spacing: 2pt, [Sensor queues], [latency / loss]), fill: pale)
    line((10.5, -0.95), (10.1, -2.55), mark: (end: "stealth", fill: teal, stroke: teal), stroke: 1pt + teal)
    content((10.7, -1.9), [measured values])

    node((3.4, -3.3), (6.2, -2.2), stack(dir: ttb, spacing: 2pt, [Future estimator], [guidance]), fill: white, stroke: (paint: slate, thickness: 0.8pt, dash: "dashed"))
    node((0.0, -3.3), (2.6, -2.2), stack(dir: ttb, spacing: 2pt, [Future policy], [output (%)]), fill: white, stroke: (paint: slate, thickness: 0.8pt, dash: "dashed"))
    line((7.0, -2.75), (6.2, -2.75), mark: (end: "stealth", fill: teal, stroke: teal), stroke: 1pt + teal)
    line((3.4, -2.75), (2.6, -2.75), mark: (end: "stealth", fill: slate, stroke: slate), stroke: (paint: slate, thickness: 1pt, dash: "dashed"))
    line((1.3, -2.2), (1.3, 1.65), mark: (end: "stealth", fill: slate, stroke: slate), stroke: (paint: slate, thickness: 1pt, dash: "dashed"))
    line((1.3, 1.65), (1.3, 2.4), mark: (end: "stealth", fill: slate, stroke: slate), stroke: (paint: slate, thickness: 1pt, dash: "dashed"))
    content((2.1, 0.9), [future command])
    content((7.0, -4.0), [Dashed boxes and arrows mark integration points, not supplied software.], anchor: "west")
  })
}
