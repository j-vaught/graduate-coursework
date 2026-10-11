#import "../style.typ": plot-panel
#let d = json("../data/experiments.json")

#let tape-and-paths() = {
  let t = d.time_s
  let names = ("00_linear", "01_hull", "05_sensors", "06_disturbances", "07_uncertainty")
  let labels = ([Linear hull], [Nonlinear hull], [With sensing], [With disturbances], [With uncertainty])
  let dash-styles = ("solid", "dashed", "dotted", "dash-dotted", "densely-dashed")
  let paths = names.enumerate().map(pair => {
    let i = pair.first()
    let n = pair.last()
    (x: d.trajectory.at(n).east_m, y: d.trajectory.at(n).north_m,
      label: labels.at(i), dash: dash-styles.at(i))
  })
  [#plot-panel("Common motor command tape", "Time (s)", "Motor command (%)",
    ((x: t, y: d.port_percent, label: [port], step: end),
     (x: t, y: d.starboard_percent, label: [starboard], step: end),),
    xlim: (0, 12), ylim: (-5, 50), height: 2.15in, legend: top + left)
  #v(4pt)
  #plot-panel("Open-loop truth trajectories", "East position (m)", "North position (m)", paths,
    xlim: (0, 15), ylim: (0, 8), height: auto, aspect-ratio: 1.0, legend: top + left)]
}

#let stage-offsets() = {
  let names = ("01_hull", "03_motor", "06_disturbances", "07_uncertainty")
  let labels = ([Nonlinear hull], [Motor response], [With disturbances], [With uncertainty])
  let s = names.enumerate().map(pair => {
    let i = pair.first()
    let n = pair.last()
    (x: d.offsets.at(n).time_s, y: d.offsets.at(n).distance_m, label: labels.at(i))
  })
  plot-panel("Distance from the linear-stage trajectory", "Time (s)", "Planar separation (m)", s,
    xlim: (0, 12), ylim: (0, 6.5), height: 2.7in, legend: top + right)
}
