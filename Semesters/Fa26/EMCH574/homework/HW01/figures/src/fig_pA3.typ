#import "/typst-figures/styles/figure.typ": *
#import "/typst-figures/styles/homework-components.typ": pendulum-schematic, projectile-indicator

// figure-pipeline: kind=mechanics
#standalone(
  full-width-artboard(
    cetz-canvas(
      length: 1mm,
      {
        pendulum-schematic(
          (17, 58),
          rod-length: 43,
          mass-label: [$M$],
          length-label: [$L$],
        )
        projectile-indicator(
          (-6, 9.5),
          length: 16,
          label: [$m, v$],
        )
      },
    ),
  ),
)
