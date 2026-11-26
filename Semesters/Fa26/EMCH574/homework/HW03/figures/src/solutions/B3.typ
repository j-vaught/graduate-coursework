#import "../../series.typ": series-stroke
#import "@preview/lilaq:0.6.0" as lq
#let d = json("data/B3.json")
#set text(font: "New Computer Modern", size: 9pt)
#set page(width: auto, height: auto, margin: 3pt, fill: white)
#lq.diagram(width: 12cm, height: 7cm, xlabel: [$x/L$], ylabel: [$W_j$],
 legend: (position: top + left),
 ..d.w.enumerate().map(p => lq.plot(d.x, p.last(), stroke: series-stroke(p.first()), mark: none, label: [Mode #(p.first()+1)])))
