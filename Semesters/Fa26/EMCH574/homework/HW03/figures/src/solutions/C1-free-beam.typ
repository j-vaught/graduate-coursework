#import "/typst-figures/styles/figure.typ": *
#standalone(cetz-canvas(length: 1mm, {
 let ink = (paint: color-graphite, thickness: 1pt, cap: "butt", join: "miter")
 draw.line((-5,0), (105,0), stroke: (paint: color-graphite, thickness: 0.5pt))
 draw.rect((0,-4), (100,4), fill: white, stroke: ink)
 draw.content((23,0), [$m, E, I$])
 draw.line((50,0), (50,13), stroke: 0.9pt + color-secondary,
  mark: (end: "stealth", fill: color-secondary))
 draw.content((50,16), [$w(x,t)$])
 draw.content((108,0), [$x$])
 draw.line((0,-11), (100,-11), stroke: 0.6pt + black)
 draw.line((0,-9),(0,-13),stroke: 0.6pt + black)
 draw.line((100,-9),(100,-13),stroke: 0.6pt + black)
 draw.content((50,-13), [$L$], anchor: "north")
 draw.content((0,-19), [$x=0$ free])
 draw.content((100,-19), [$x=L$ free])
}))
