#import "/styles/figure.typ": *

#standalone(
 full-width-artboard(
  cetz-canvas(length: 1mm, {
    draw.content((34, 54), figure-title[(a) Static equilibrium])
    draw.content((115, 54), figure-title[(b) Displaced by $u$])
    for x in (34,115) {
      draw.rect((x - 7, 17), (x + 7, 30), ..mechanics-body-style)
      draw.content((x, 23.5), [$m$])
      draw.line((x, 17), (x, 0), ..mechanics-force-style)
      draw.content((x + 7, 2), [$m g$])
      draw.line((x, 30), (x, 46), ..mechanics-force-style)
    }
    draw.content((34, 49), [$k delta_("st")$])
    draw.content((115, 49), [$k(delta_("st")+u)$])
    draw.line((139, 30), (139, 12), ..mechanics-displacement-style)
    draw.content((145, 21), [$+u$])
    draw.content((34, -7), figure-small[$m g-k delta_("st")=0$])
    draw.content((115, -7), figure-small[$m dot.double(u)=-k u$])
  }),
 ),
)
