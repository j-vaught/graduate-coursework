#import "/styles/figure.typ": *
#import "/styles/homework-components.typ": pendulum-schematic

// figure-pipeline: kind=mechanics
#standalone(
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
)
