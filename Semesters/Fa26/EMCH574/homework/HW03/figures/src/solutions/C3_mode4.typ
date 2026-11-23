#import "@preview/lilaq:0.6.0" as lq
#let d = json("data/C3.json")
#set text(font: "New Computer Modern", size: 9pt)
#set page(width: auto, height: auto, margin: 3pt, fill: white)
#lq.diagram(width: 10cm, height: 5cm, xlabel: [$x/L$], ylabel: [$W_4$], lq.plot(d.x,d.w.at(3), mark: none))
