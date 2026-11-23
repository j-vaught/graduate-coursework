#import "/typst-figures/styles/figure.typ": *
#standalone(cetz-canvas(length: 1mm, {
 let ink = (paint:black,thickness:.8pt,cap:"butt")
 let arrow = (stroke:ink,mark:(end:"stealth",fill:black))
 draw.line((0,0),(90,0),stroke:(paint:color-secondary,thickness:1pt))
 for x in (0,90) { draw.circle((x,0),radius:0.8,stroke:ink,fill:white) }
 draw.line((28,18),(28,1.2),..arrow)
 draw.content((28,21),[$F_e(t)$])
 draw.line((65,0),(65,18),..arrow)
 draw.content((65,21),[$u(x_0,t)$])
 draw.content((28,-3.5),[$x_e$])
 draw.content((65,-3.5),[$x_0$])
 draw.line((0,-9),(90,-9),stroke:ink,mark:(start:"stealth",end:"stealth",fill:black))
 draw.content((45,-12),[$L$])
}))
