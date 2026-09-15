#import "/typst-figures/styles/figure.typ": *

#standalone(
  full-width-artboard(
    cetz-canvas(length: 1mm, {
      draw.rect((69, 16), (83, 30), ..mechanics-body-style)
      draw.content((76, 23), [$m$])

      draw.line((76, 30), (76, 43), ..mechanics-force-style)
      draw.content((82, 42), [$N$])
      draw.line((76, 16), (76, 3), ..mechanics-force-style)
      draw.content((82, 4), [$m g$])

      draw.line((69, 23), (48, 23), ..mechanics-force-style)
      draw.content((56, 28), [$k u$])

      draw.line((88, 36), (103, 36), ..mechanics-displacement-style)
      draw.content((95, 40), [$+u$])
    }),
  ),
)
