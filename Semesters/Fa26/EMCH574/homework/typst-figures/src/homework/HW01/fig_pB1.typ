#import "/styles/figure.typ": *
#import "/styles/homework-components.typ": horizontal-spring-mass

// figure-pipeline: kind=mechanics
#standalone(
  full-width-artboard(
    cetz-canvas(
      length: 1mm,
      {
        horizontal-spring-mass(
          (4, 10),
          spring-length: 22,
          mass-width: 11,
          mass-height: 11,
        )
      },
    ),
  ),
)
