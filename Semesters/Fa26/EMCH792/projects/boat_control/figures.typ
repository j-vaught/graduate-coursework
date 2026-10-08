#import "@preview/lilaq:0.6.0" as lq
#import "@preview/cetz:0.4.2" as cetz
#let runs = json("data/runs.json")
#let phases = json("data/phases.json")
#let traces = json("data/slide_traces.json")
#let garnet = rgb("#73000A")
#let fmt(n, digits: 2) = str(calc.round(n, digits: digits))
#let series(name, field, label: none, dash: "solid") = {
  let run = runs.at(name)
  lq.plot(run.time, run.at(field), mark: none, label: label,
    stroke: (thickness: 1.25pt, dash: dash))
}
#let panel(name, fields, ylabel, title, height: 1.8in, limit: auto, ylim: auto, labels: none) = {
  set text(size: 9pt)
  lq.diagram(width: 100%, height: 0% + height, title: title,
    xlabel: [Time (s)], ylabel: ylabel, xlim: limit, ylim: ylim,
    xaxis: (ticks: if limit.last() == 40 { (0, 10, 20, 30, 40) }
      else if limit.last() == 60 { (0, 10, 20, 30, 40, 50, 60) }
      else if limit.last() == 30 { (0, 5, 10, 15, 20, 25, 30) }
      else { (0, 2, 4, 6, 8, 10, 12) }),
    grid: (stroke: 0.35pt + luma(80%)),
    legend: if labels == none { none } else { (radius: 0pt, fill: white, position: top + right) },
    ..fields.enumerate().map(pair => series(name, pair.last(),
      label: if labels == none { none } else { labels.at(pair.first()) },
      dash: ("solid", "dashed", "dotted").at(pair.first()))),
  )
}
#let equal-step() = panel("equal", ("u",), [Surge speed (m/s)], [Equal thrust], height: 2.0in, limit: (0, 40), ylim: (0, 1.5))
#let differential() = {
  grid(columns: (1fr, 1fr), column-gutter: 14pt, row-gutter: 12pt,
    panel("differential", ("u", "v"), [Speed (m/s)], [Translation], limit: (0, 60), ylim: (-1.1, 1.65), labels: ($u$, $v$)),
    panel("differential", ("r",), [Yaw rate (rad/s)], [Rotation], limit: (0, 60), ylim: (0, 0.17)),
  )
}
#let turning-path() = {
  set text(size: 9pt)
  let run = runs.differential
  // Both data axes span 30 m and the data area is square.
  lq.diagram(width: 2.55in, height: 2.55in, xlabel: [East (m)], ylabel: [North (m)],
    xlim: (-8, 22), ylim: (-2, 28), legend: (radius: 0pt, fill: white, position: top + right),
    lq.plot(run.x, run.y, mark: none, label: [Path], stroke: 1.25pt),
    lq.plot((0,), (0,), mark: "s", stroke: none, label: [Start]),
    lq.plot((run.x.last(),), (run.y.last(),), mark: "x", stroke: none, label: [60 s]),
  )
}
#let pulse() = grid(columns: (1fr, 1fr), column-gutter: 14pt,
  panel("pulse", ("v",), [Sway speed (m/s)], [Delayed lateral response], height: 2.15in, limit: (0, 30), ylim: (0, 0.09)),
  panel("pulse", ("r",), [Yaw rate (rad/s)], [Yaw pulse and recovery], height: 2.15in, limit: (0, 12), ylim: (-0.48, 0.03)),
)
#let decay() = grid(columns: (1fr, 1fr), column-gutter: 14pt,
  panel("decay", ("u", "v"), [Speed (m/s)], [Translation], height: 2.1in, limit: (0, 30), ylim: (0, 1.05), labels: ($u$, $v$)),
  panel("decay", ("r",), [Yaw rate (rad/s)], [Rotation], height: 2.1in, limit: (0, 12), ylim: (0, 0.55)),
)
#let phase(speed) = {
  set text(size: 9pt)
  lq.diagram(width: 100%, height: 0% + 2in, xlabel: [Sway speed (m/s)], ylabel: [Yaw rate (rad/s)],
    title: [$u = #speed$ m/s], xlim: (-1.2, 1.2), ylim: (-0.55, 0.55), legend: none,
    ..phases.at(str(speed)).map(run => lq.plot(run.v, run.r, mark: none,
      color: rgb("#3F90DA"), stroke: 0.65pt)),
    ..phases.at(str(speed)).filter(run => run.r0 != 0 or run.v0 != 0).map(run => {
      let i = 5
      lq.quiver((run.v.at(i),), (run.r.at(i),),
        (x, y) => (run.v.at(i + 2) - x, run.r.at(i + 2) - y),
        scale: 1, stroke: 0.7pt + rgb("#3F90DA"), pivot: start)
    }),
    lq.plot((0,), (0,), mark: "x", stroke: none, color: black),
  )
}
#let phase-pair() = grid(columns: (1fr, 1fr), column-gutter: 14pt, phase(0), phase(1))
#let wind() = grid(columns: (1fr, 1fr), column-gutter: 14pt,
  panel("wind", ("v",), [Sway speed (m/s)], [Velocity approaches equilibrium], height: 1.8in, limit: (0, 60), ylim: (0, 0.42)),
  panel("wind", ("y",), [North displacement (m)], [Position continues to drift], height: 1.8in, limit: (0, 60), ylim: (0, 23)),
)
#let blind() = {
  set text(size: 9pt)
  let cases = ("blind_calm", "blind_crosswind", "blind_headwind")
  let labels = ([Calm], [Crosswind], [Headwind])
  grid(columns: (1fr, 1fr), column-gutter: 14pt,
    lq.diagram(width: 100%, height: 0% + 2.5in, xlabel: [East (m)], ylabel: [North (m)],
      title: [Planar paths], xlim: (-1, 22), ylim: (-1, 35),
      legend: (radius: 0pt, fill: white, position: top + left),
      ..cases.enumerate().map(pair => {
        let run = runs.at(pair.last())
        lq.plot(run.x, run.y, mark: none, label: labels.at(pair.first()),
          stroke: (thickness: 1.25pt, dash: ("solid", "dashed", "dotted").at(pair.first())))
      }),
      lq.plot((20,), (0,), mark: "x", stroke: none, color: black, label: [Target]),
    ),
    lq.diagram(width: 100%, height: 0% + 2.5in, xlabel: [Time (s)], ylabel: [Target distance (m)],
      title: [Same input in every environment], xlim: (0, 90), ylim: (0, 35),
      legend: (radius: 0pt, fill: white, position: top + left),
      ..cases.enumerate().map(pair => series(pair.last(), "distance", label: labels.at(pair.first()),
        dash: ("solid", "dashed", "dotted").at(pair.first()))),
    ),
  )
}
#let schedule() = {
  let stop = json("data/schedule.json").chosen_cutoff_s
  set text(size: 9pt)
  lq.diagram(width: 100%, height: 0% + 1.25in, xlabel: [Time (s)], ylabel: [Each thruster (N)],
    xlim: (0, 90), ylim: (0, 110), legend: none,
    xaxis: (ticks: (0, 15, 30, 45, 60, 75, 90)),
    lq.plot((0, stop, stop, 90), (100, 100, 0, 0), mark: none, stroke: 1.3pt),
  )
}
#let overlay(key, name, field, ylabel, title, limit) = {
  set text(size: 9pt)
  let points = traces.at(key)
  lq.diagram(width: 100%, height: 0% + 1.9in, title: title,
    xlabel: [Time (s)], ylabel: ylabel, xlim: limit,
    legend: (radius: 0pt, fill: white, position: top + right),
    series(name, field, label: [Reconstruction]),
    lq.plot(points.enumerate().filter(p => calc.rem(p.first(), 10) == 0).map(p => p.last().first()),
      points.enumerate().filter(p => calc.rem(p.first(), 10) == 0).map(p => p.last().last()),
      mark: "x", stroke: none, label: [Slide samples], mark-size: 2pt),
  )
}
#let overlays() = grid(columns: (1fr, 1fr), column-gutter: 14pt,
  overlay("pulse_v", "pulse", "v", [Sway speed (m/s)], [Pulse response], (0, 20)),
  overlay("blind_crosswind_distance", "blind_crosswind", "distance", [Target distance (m)], [Crosswind response], (0, 90)),
)
#let hull() = {
  set text(size: 10pt)
  cetz.canvas(length: 0.68cm, {
    import cetz.draw: *
    let arrow = (end: "stealth", fill: black, stroke: black)
    rect((-3.4, -1.65), (3.4, -0.75), fill: luma(94%), stroke: 0.8pt)
    rect((-3.4, 0.75), (3.4, 1.65), fill: luma(94%), stroke: 0.8pt)
    rect((-1.1, -0.75), (1.1, 0.75), fill: white, stroke: 0.8pt)
    content((0, 0), [Computer])
    rect((-3.7, -1.5), (-3.1, -0.9), fill: garnet, stroke: none)
    rect((-3.7, 0.9), (-3.1, 1.5), fill: garnet, stroke: none)
    line((-3.4, -1.2), (-1.8, -1.2), mark: arrow)
    line((-3.4, 1.2), (-1.8, 1.2), mark: arrow)
    content((-2.5, -1.95), $T_R$)
    content((-2.5, 1.95), $T_L$)
    line((1.4, 0), (3.2, 0), mark: arrow)
    content((2.6, 0.36), [Forward, $u$])
    line((0, 0.3), (0, 2.7), mark: arrow)
    content((1.8, 2.6), [Leftward, $v$])
    line((-3.4, -2.6), (3.4, -2.6), mark: (start: "stealth", end: "stealth", fill: black))
    content((0, -2.95), [Length 4.9 m])
    line((4.1, -1.2), (4.1, 1.2), mark: (start: "stealth", end: "stealth", fill: black))
    content((5.8, 0), [$B = 2.4$ m])
  })
}
#let feedback() = {
  set text(size: 9pt)
  cetz.canvas(length: 0.9cm, {
    import cetz.draw: *
    let arrow = (end: "stealth", fill: black)
    let box(x, body) = {
      rect((x, 0), (x + 2.2, 1.1), fill: white, stroke: 0.8pt)
      content((x + 1.1, 0.55), body)
    }
    box(0, [Guidance])
    box(3.0, [Controller])
    box(6.0, [Thrusters])
    box(9.0, [Boat])
    for x in (2.2, 5.2, 8.2) { line((x, 0.55), (x + 0.8, 0.55), mark: arrow) }
    line((10.1, 2.0), (10.1, 1.1), mark: arrow)
    content((10.1, 2.3), [Wind])
    rect((4.1, -2.2), (8.5, -1.1), fill: luma(95%), stroke: 0.8pt)
    content((6.3, -1.65), [Sensors and state estimator])
    line((10.1, 0), (10.1, -1.65), (8.5, -1.65), mark: arrow)
    line((4.1, -1.65), (4.1, 0), mark: arrow)
    content((2.75, -1.65), [Estimated state])
  })
}
