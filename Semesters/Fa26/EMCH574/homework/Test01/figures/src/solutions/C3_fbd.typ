#import "/typst-figures/styles/figure.typ": *

#standalone(
 full-width-artboard(
  cetz-canvas(length: 1mm, {
    let x = 76
    draw.content((x, 51), figure-title[(a) Horizontal free vibration])
    draw.rect((x - 7, 16), (x + 7, 30), ..mechanics-body-style)
    draw.content((x, 23), [$m$])
    draw.line((x, 30), (x, 43), ..mechanics-force-style)
    draw.content((x + 5, 42), [$N$])
    draw.line((x, 16), (x, 3), ..mechanics-force-style)
    draw.content((x + 6, 4), [$m g$])
    draw.line((x - 7, 23), (x - 28, 23), ..mechanics-force-style)
    draw.content((x - 17, 28), [$k u$])
    draw.line((x + 7, 36), (x + 25, 36), ..mechanics-displacement-style)
    draw.content((x + 16, 40), [$+u$])
  }),
 ),
)
