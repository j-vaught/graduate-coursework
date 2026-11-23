#import "/typst-figures/styles/figure.typ": *
#standalone(cetz-canvas(length: 1mm, {
 draw.rect((0,0),(36,10),stroke: 0.8pt + black)
 draw.line((0,5),(-12,5),stroke: 0.8pt + black, mark:(end:"stealth",fill:black))
 draw.line((36,5),(48,5),stroke: 0.8pt + black, mark:(end:"stealth",fill:black))
 draw.content((-6,8),[$N(x,t)$])
 draw.content((44,8),[$N(x+dif x,t)$])
 draw.content((18,5),[$rho A dif x$])
 draw.content((18,-4),[$dif x$])
}))
