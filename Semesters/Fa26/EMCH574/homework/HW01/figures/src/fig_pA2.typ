#import "/typst-figures/styles/figure.typ": *
#import "/typst-figures/styles/homework-components.typ": pendulum-schematic

// figure-pipeline: kind=mechanics
#standalone(
  full-width-artboard(
    cetz-canvas(
      length: 1mm,
      {
        pendulum-schematic(
          (0, 54),
          rod-length: 41,
          mass-label: [$m$],
          length-label: [$L$],
        )
      },
    ),
  ),
)
