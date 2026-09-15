#import "/typst-figures/styles/figure.typ": *
#import "/typst-figures/styles/homework-components.typ": homework-math

#standalone(
  full-width-artboard(
    cetz-canvas(length: 1mm, {
      draw.content((76, 48), figure-title[Free-body diagram])

      draw.rect((69, 16), (83, 30), ..mechanics-body-style)
      draw.content((76, 23), homework-math[$m$])

      draw.line((69, 23), (45, 23), ..mechanics-force-style)
      draw.content((56, 28), homework-math[$k u(t)$])

      draw.line((69, 19), (45, 19), ..mechanics-force-style)
      draw.content((56, 13), homework-math[$c dot(u)(t)$])

      draw.line((83, 23), (107, 23), ..mechanics-force-style)
      draw.content((95, 28), homework-math[$F(t)$])

      draw.line((87, 36), (107, 36), ..mechanics-displacement-style)
      draw.content((97, 40), homework-math[$+x$])
    }),
  ),
)
