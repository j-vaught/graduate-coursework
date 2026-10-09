#import "@preview/lilaq:0.6.0" as lq
#import "@preview/cetz:0.4.2"
#set document(title: "Configurable BlueBoat simulator", author: "J.C. Vaught")
#set page(paper: "us-letter", margin: 0.55in)
#set text(font: "Times New Roman", size: 10pt)
#let runs = json("data/configurable_simulator/comparison.json")
#let get(name) = runs.find(r => r.name == name)
#let series(name, column, label, dash: "solid") = {
  let r = get(name)
  lq.plot(r.history.map(z => z.at(0)), r.history.map(z => z.at(column)),
    step: if name == "02_m200" and column == 7 { end } else { none },
    mark: none, label: label, stroke: (thickness: 1.3pt, dash: dash))
}
#let panel(title, ylabel, specs, xlim: (0, 12), ylim: auto) = {
  set text(size: 9pt)
  lq.diagram(width: 100%, height: 2.4in, title: title,
    xlabel: [Time (s)], ylabel: ylabel, xlim: xlim, ylim: ylim,
    grid: (stroke: 0.35pt + luma(80%)),
    legend: (radius: 0pt, fill: white, position: top + right),
    ..specs.enumerate().map(pair => {
      let s = pair.last()
      series(s.at(0), s.at(1), s.at(2), dash: ("solid", "dashed", "dotted").at(pair.first()))
    }))
}
#align(center)[
  #text(size: 16pt, weight: "bold")[Configurable BlueBoat simulator]
  #v(3pt)
  Same initial state and PWM tape across cumulative model stages. Seed 792.
]
#v(12pt)
#grid(columns: (1fr, 1fr), column-gutter: 18pt, row-gutter: 18pt,
  panel([Hull and propulsion], [Surge speed (m/s)], (
    ("00_linear", 4, [Linear]),
    ("01_hull", 4, [Nonlinear hull]),
    ("02_m200", 4, [M200 curve]),
  ), ylim: (0.9, 1.7)),
  panel([Environmental and parameter effects], [North position (m)], (
    ("04_timing", 2, [Through timing]),
    ("06_disturbances", 2, [With disturbances]),
    ("07_uncertainty", 2, [With uncertainty]),
  ), ylim: (0, 8)),
  panel([Motor and command transient], [Port force (N)], (
    ("02_m200", 7, [Instantaneous]),
    ("03_motor", 7, [Motor lag / slew]),
    ("04_timing", 7, [Sample / delay]),
  ), xlim: (3.9, 4.8), ylim: (0, 18)),
  {
    set text(size: 9pt)
    let samples = get("05_sensors").gnss.filter(m => m.valid and m.delivered)
    lq.diagram(width: 100%, height: 2.4in, title: [Delivered GNSS errors],
      xlabel: [Availability time (s)], ylabel: [Position error (m)],
      xlim: (0, 12), ylim: (-0.08, 0.08),
      grid: (stroke: 0.35pt + luma(80%)),
      legend: (radius: 0pt, fill: white, position: top + right),
      ..("x_m", "y_m").enumerate().map(pair => lq.plot(
        samples.map(m => m.available_time_s),
        samples.map(m => m.values.at(pair.last()) - m.truth.at(pair.last())),
        mark: none, label: ([East], [North]).at(pair.first()),
        stroke: (thickness: 0.8pt, dash: ("solid", "dashed").at(pair.first())))),
    )
  },
)
#v(12pt)
The input starts at the 1 m/s trim, adds 80 µs to both motors at 2 s, commands
differential thrust at 4 s, and returns to trim at 6 s. The larger excitation
reveals departures from the local linear model. The force panel expands the
4 s command transition.

GNSS errors compare measured antenna position with antenna truth at acquisition;
points appear at delivery time. Sensor errors do not change this open-loop path.
Wind, motor timing, and sensor parameters retain the report's stated assumptions.

The curves show the effect of model detail. Measured boat logs are required to
establish improved prediction; controller tracking is a subsequent experiment.
