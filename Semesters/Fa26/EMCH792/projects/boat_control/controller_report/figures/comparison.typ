#import "../../simulator_report/style.typ": *
#let s = json("../data/summary.json")
#let methods = ("pid", "lqr", "pole_placement")
#let names = ("PID", "LQR + integral", "Pole placement + integral")
#let value(case, method, metric) = s.aggregate.find(r => r.case == case and r.method == method).metrics.at(metric).mean
#let wind = {
  let cases = ("full_calm", "full_wind5", "full_wind8", "full_wind10")
  let series = methods.enumerate().map(pair => (
    x: (0, 5, 8, 10), y: cases.map(c => value(c, pair.last(), "tail_cross_rms_m")),
    label: names.at(pair.first()), dash: ("solid", "dashed", "dash-dotted").at(pair.first())))
  plot-panel([Mean final-ten-second line error], [Configured wind speed (m/s)], [Cross-track RMS (m)], series, height: 2.5in, ylim: (0, auto))
}
#let ladder = {
  let cases = ("00_linear", "01_hull", "02_m200", "03_motor", "04_timing", "05_sensors", "06_disturbances", "07_uncertainty")
  let series = methods.enumerate().map(pair => (
    x: range(8), y: cases.map(c => value("ladder_"+c, pair.last(), "cross_rms_m")),
    label: names.at(pair.first()), dash: ("solid", "dashed", "dash-dotted").at(pair.first())))
  plot-panel([Cumulative simulator flag ladder], [Stage index (0-7)], [Whole-run cross-track RMS (m)], series, height: 2.5in)
}
