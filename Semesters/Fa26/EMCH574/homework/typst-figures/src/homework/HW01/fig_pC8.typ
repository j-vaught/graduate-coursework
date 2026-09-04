#import "/styles/figure.typ": *
#import "/styles/homework-components.typ": hanging-flex-beam

#standalone(
  full-width-artboard(
    cetz-canvas(
      length: 1mm,
      {
        hanging-flex-beam(
          (75, 67),
          beam-length: 50,
          mass-label: [$M$],
          projectile: true,
        )
      },
    ),
  ),
)
