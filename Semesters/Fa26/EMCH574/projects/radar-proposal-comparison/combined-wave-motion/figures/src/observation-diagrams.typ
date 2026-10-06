#import "@preview/cetz:0.5.2" as cetz
#set text(font: "Latin Modern Roman", size: 10pt, fill: black)
#show math.equation: set text(font: "Latin Modern Math")
#set page(width: 6.5in, height: 2.8in, margin: 0pt)
#let arrow = (end: "stealth", fill: black, length: 2.4mm, width: 1.5mm)
#let diagram = sys.inputs.at("diagram", default: "obstruction")
#align(center + horizon)[
#cetz.canvas(length: 1mm, {
  import cetz.draw: *
  rect((0, 0), (160, 66), fill: white, stroke: none)
  if diagram == "obstruction" {
    let wave = range(0, 141).map(i => (10 + i, 18 + 29 * calc.exp(-calc.pow((10 + i - 80) / 16, 2))))
    line(..wave, stroke: 1pt)
    rect((13, 50), (17, 54), fill: black)
    rect((143, 31), (147, 35), fill: black)
    line((15, 52), (145, 33), stroke: (paint: black, thickness: 0.8pt, dash: "dashed"))
    content((15, 60), [Radar])
    content((145, 41), [Target])
    content((40, 54), [Direct path])
    line((80, 42.5), (80, 47), stroke: 0.8pt, mark: arrow)
    content((96, 49), [Crest intrusion $d_c$])
    content((80, 8), [Wave surface])
  } else if diagram == "beam-misalignment" {
    rect((13, 43), (17, 47), fill: black)
    line((15, 45), (145, 51), stroke: 0.7pt)
    line((15, 45), (145, 29), stroke: 0.7pt)
    line((15, 45), (145, 40), stroke: (paint: black, thickness: 0.8pt, dash: "dashed"))
    line((15, 45), (145, 19), stroke: 1pt, mark: arrow)
    rect((143, 17), (147, 21), fill: black)
    content((15, 58), [Radar])
    content((107, 58), [Beam boundaries])
    content((105, 46), [Beam centerline])
    content((71, 27), [Target direction])
    content((143, 9), [Target])

  } else if diagram == "timing" {
    rect((13, 43), (17, 47), fill: black)
    rect((43, 43), (47, 47), fill: white, stroke: 1pt)
    rect((118, 27), (122, 31), fill: black)
    rect((148, 27), (152, 31), fill: white, stroke: 1pt)
    line((15, 45), (120, 29), stroke: 1pt, mark: arrow)
    line((45, 45), (150, 29), stroke: (paint: black, thickness: 0.8pt, dash: "dashed"), mark: arrow)
    content((19, 60), [Ray-time pose])
    content((66, 51), [Midpoint pose])
    content((111, 38), [True target])
    content((139, 18), [Mapped target])
    line((135, 8), (120, 8), stroke: 0.8pt, mark: arrow)
    line((135, 8), (150, 8), stroke: 0.8pt, mark: arrow)
    content((135, 1), [Position error $E_h$])
  }
})]
