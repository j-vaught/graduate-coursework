#import "../../style.typ": cetz, ink, teal, pale, slate, arrow, node, plot-panel
#let data = json("../../data/sensors.json")

#let stereo-error() = {
  let series = ((
    x: data.distance_m,
    y: data.range_sigma_m,
    label: [First-order $sigma_R$],
    thickness: 1.4pt,
  ),)
  plot-panel(
    [Stereo range uncertainty from disparity noise],
    [Target distance $Z$ (m)],
    [Range standard uncertainty $sigma_R$ (m)],
    series,
    xlim: (0, data.max_range_m),
    ylim: (0, 2.6),
    height: 2.45in,
    legend: top + left,
  )
}

#set document(title: "BlueBoat. 06 stereo uncertainty", author: "J.C. Vaught")
#set page(width: 7.06in, height: auto, margin: 0pt)
#set text(font: "Times New Roman", size: 9pt)
#align(center, stereo-error())
