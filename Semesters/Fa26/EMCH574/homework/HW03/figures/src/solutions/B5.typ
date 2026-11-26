#import "../../series.typ": series-stroke, inks
#import "/typst-figures/styles/figure.typ": *
#let d = json("data/B5.json")
#set page(width: 160mm, height: auto, margin: 3mm)
#set text(font: "New Computer Modern", size: 9pt)
#book-diagram(size: "full", height: 43mm, xlabel: [$x/L$], ylabel: [$W_j$],
  ..d.modes.enumerate().map(((i, y)) => plot(d.x,y,stroke: series-stroke(i),label: [#str(i+1)])), legend: (position: top + left))
#v(4mm)
#book-diagram(size: "full", height: 40mm, xlabel: [$x/L$], ylabel: [$w_0$ (mm)],
  plot(d.x,d.initial))
#v(4mm)
#book-diagram(size: "full", height: 40mm, xlabel: [Mode $j$], ylabel: [$A_j$ (mm)],
  xlim: (0,6), ..d.coeff.enumerate().map(((i,y)) => line((i+1,0),(i+1,y),stroke: 5pt + inks.first())))
#v(4mm)
#book-diagram(size: "full", height: 40mm, xlabel: [Time (ms)], ylabel: [Tip displacement (mm)],
  plot(d.t,d.tip))
