#import "../../style.typ": plot-panel
#let d = json("../../data/experiments.json")

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

#set document(title: "BlueBoat. 08 stage offsets", author: "J.C. Vaught")
#set page(width: 7.06in, height: auto, margin: 0pt)
#set text(font: "Times New Roman", size: 9pt)
#align(center, stage-offsets())
