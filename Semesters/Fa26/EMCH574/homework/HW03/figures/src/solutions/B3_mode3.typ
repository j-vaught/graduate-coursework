#import "../../series.typ": series-stroke
#import "@preview/lilaq:0.6.0" as lq
#let d = json("data/B3.json")
#set text(font: "New Computer Modern", size: 9pt)
#set page(width: auto, height: auto, margin: 3pt, fill: white)
#lq.diagram(width: 10cm, height: 5cm, ylim: (-1, 1), xlabel: [$x/L$], ylabel: [$hat(W)_3$], lq.plot(d.x,d.w.at(2), stroke: series-stroke(2), mark: none))
