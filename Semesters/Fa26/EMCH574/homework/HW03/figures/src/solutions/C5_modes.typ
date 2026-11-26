#import "../../series.typ": series-stroke
#import "@preview/lilaq:0.6.0" as lq
#let d = json("data/C5.json")
#set page(width:7.5in,height:4in,margin:4pt,fill:white)
#set text(font:"New Computer Modern",size:9pt)
#let panel(k) = lq.diagram(width: 1.6in,height: 1.05in,
  title: [Mode #k], xlabel: [$x/L$], ylabel: [$W_j$],
  xlim:(0,1),ylim:(-1.1,1.1),
  lq.plot(d.x,d.modes.at(k - 1),stroke:series-stroke(k - 1),mark:none))
#grid(columns: (1fr,1fr,1fr),gutter:8pt,
  ..range(1,6).map(panel),
  lq.diagram(width:1.6in,height:1.05in,title:[All modes],
    xlabel:[$x/L$],ylabel:[$W_j$],xlim:(0,1),ylim:(-1.1,1.1),
    ..range(5).map(i => lq.plot(d.x,d.modes.at(i),stroke:series-stroke(i),mark:none))))
