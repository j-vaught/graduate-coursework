#import "/styles/figure.typ": *

#standalone(
  cetz-canvas(length: 24mm, {
    let ink=(paint:color-ink,thickness:0.7pt,cap:"butt")
    draw.line((-1.25,0),(1.5,0),stroke:ink,mark:(end:">"))
    draw.line((0,-1.3),(0,1.35),stroke:ink,mark:(end:">"))
    draw.circle((0,0),radius:1,stroke:(paint:color-guide,thickness:0.7pt))
    draw.content((1.5,-0.12),[$"Re"$])
    draw.content((-0.15,1.32),[$"Im"$])
    for (point,label,offset) in (
      ((0,1),$i=e^(i pi/2)$,(0.55,1.1)),
      ((0,-1),$-i=e^(i 3 pi/2)=e^(-i pi/2)$,(0.7,-1.18)),
      ((0.7071,0.7071),$e^(i pi/4)$,(1.05,0.85)),
      ((0.7071,-0.7071),$e^(-i pi/4)$,(1.12,-0.78)),
    ) {
      draw.rect((point.at(0)-0.035,point.at(1)-0.035),(point.at(0)+0.035,point.at(1)+0.035),fill:color-secondary,stroke:none)
      draw.content(offset,label)
    }
    draw.content((-1,-0.13),[$-1$])
    draw.content((1,-0.13),[$1$])
    draw.content((0.3,1.6),figure-title[Complex phases on the unit circle])
  }),
)
