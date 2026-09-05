#import "/styles/figure.typ": *

#standalone(
 full-width-artboard(
  cetz-canvas(length: 1mm, {
    draw.content((33, 51), figure-title[(a) Free, undamped motion])
    draw.content((114, 51), figure-title[(b) Damping and applied force])
    for x in (33, 114) {
      draw.rect((x - 6, 16), (x + 6, 30), ..mechanics-body-style)
      draw.content((x, 23), [$m$])
      draw.line((x, 30), (x, 43), ..mechanics-force-style)
      draw.content((x + 5, 42), [$N$])
      draw.line((x, 16), (x, 3), ..mechanics-force-style)
      draw.content((x + 6, 4), [$m g$])
    }
    draw.line((27, 23), (8, 23), ..mechanics-force-style)
    draw.content((15, 28), [$k u$])
    draw.line((108, 27), (82, 27), ..mechanics-force-style)
    draw.content((92, 32), [$k u$])
    draw.line((108, 19), (82, 19), ..mechanics-force-style)
    draw.content((92, 13), [$c dot(u)$])
    draw.line((120, 23), (145, 23), ..mechanics-force-style)
    draw.content((135, 29), [$F(t)$])
    draw.line((44, 36), (59, 36), ..mechanics-displacement-style)
    draw.content((51, 40), [$+u$])
    draw.content((76, -5), figure-small[Set $c=0$ for an undamped system; set $F=0$ for free vibration.])
    draw.content((76, -11), figure-small[For beam models, $N$ represents the balanced vertical support reaction.])
  }),
 ),
)
