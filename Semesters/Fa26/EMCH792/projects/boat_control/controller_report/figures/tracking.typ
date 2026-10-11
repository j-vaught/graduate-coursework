#import "../../simulator_report/style.typ": *
#let traces = json("../data/traces.json")
#let methods = ("pid", "lqr", "pole_placement")
#let names = ("PID", "LQR + integral", "Pole placement + integral")
#let panel(case, column, title, ylabel, offset: 0, scale: 1, ylim: auto) = {
  let series = methods.enumerate().map(pair => {
    let h = traces.at(case).at(pair.last()).history
    (x: h.map(v => v.at(0)), y: h.map(v => (v.at(column)-offset)*scale),
     label: names.at(pair.first()), dash: ("solid", "dashed", "dash-dotted").at(pair.first()))
  })
  plot-panel(title, [Time (s)], ylabel, series, height: 2.15in, ylim: ylim)
}
#let cross = {
  panel("full_wind5", 2, [Full model, 5 m/s wind], [Cross-track error (m)])
  v(0.1in)
  panel("full_wind10", 2, [Full model, 10 m/s wind], [Cross-track error (m)])
}
#let motion = {
  panel("full_wind5", 4, [Full model, 5 m/s wind], [Surge speed error (m/s)], offset: 1)
  v(0.1in)
  panel("full_wind5", 3, [Crab heading under crosswind], [Heading from east (deg)], scale: 180/calc.pi)
}
#let force = {
  panel("full_wind10", 7, [Port thruster, 10 m/s wind], [Actual thrust (N)])
  v(0.1in)
  panel("full_wind10", 8, [Starboard thruster, 10 m/s wind], [Actual thrust (N)])
}
