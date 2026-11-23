#import "/typst-figures/styles/figure.typ": *
#standalone(cetz-canvas(length: 1mm, {
  import cetz.draw: *
  line((0,0),(80,0),stroke:1.2pt)
  for x in (0,80) {
    line((x,0),(x - 3,-5),(x + 3,-5),(x,0),stroke:0.8pt,fill:white)
    line((x - 5,-7),(x + 5,-7),stroke:0.8pt)
  }
  circle((78,-6),radius:0.8,fill:white,stroke:0.6pt)
  circle((82,-6),radius:0.8,fill:white,stroke:0.6pt)
  content((40,4),[$E I, m$])
  content((40,-11),[$L$])
  content((0,-11),[$x=0$])
  content((80,-11),[$x=L$])
}))
