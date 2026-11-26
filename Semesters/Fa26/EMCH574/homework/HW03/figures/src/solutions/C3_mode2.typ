#import "../../series.typ": series-stroke
#import "@preview/lilaq:0.6.0" as lq
#let d = json("data/C3.json")
#set text(font: "New Computer Modern", size: 9pt)
#set page(width: auto, height: auto, margin: 3pt, fill: white)
#lq.diagram(width: 10cm, height: 5cm, xlabel: [$x/L$], ylabel: [$W_2$], lq.plot(d.x,d.w.at(1), stroke: series-stroke(1), mark: none))
