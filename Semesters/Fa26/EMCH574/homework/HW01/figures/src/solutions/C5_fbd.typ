#import "/typst-figures/styles/figure.typ": *
#import "/typst-figures/styles/homework-components.typ": homework-math

#standalone(
  full-width-artboard(
    cetz-canvas(length: 1mm, {
      draw.content((76, 48), figure-title[Free-body diagram])

      draw.rect((69, 16), (83, 30), ..mechanics-body-style)
      draw.content((76, 23), homework-math[$m$])

      draw.line((69, 23), (43, 23), ..mechanics-force-style)
      draw.content((56, 28), homework-math[$k u(t)$])

      draw.line((83, 23), (109, 23), ..mechanics-force-style)
      draw.content((96, 28), homework-math[$F(t)$])

      draw.line((88, 36), (108, 36), ..mechanics-displacement-style)
      draw.content((98, 40), homework-math[$+x$])
    }),
  ),
)
