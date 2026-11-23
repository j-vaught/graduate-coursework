#import "@preview/lilaq:0.6.0" as lq
#let d = json("data/C2.json")
#set page(width: 8.5in, height: auto, margin: 4pt)
#set text(font: "New Computer Modern", size: 9pt)
#let graph(j) = lq.diagram(width: 3.1in, height: 1.25in, xlabel: [$x$ (m)], ylabel: [$W_#j$], ylim: (-1.1,1.1), lq.plot(d.x.at(j - 1), d.w, mark: none))
#grid(columns: (1fr,1fr), gutter: 10pt, ..range(1,7).map(j => graph(j)))
