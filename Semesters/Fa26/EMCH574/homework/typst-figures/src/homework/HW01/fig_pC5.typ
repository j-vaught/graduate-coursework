#import "/styles/figure.typ": *
#import "/styles/homework-components.typ": homework-math

// Forced spring-mass system shown at rest, under load, and as an FBD.
#standalone(
  full-width-artboard(
    cetz-canvas(
      length: 1mm,
      {
        let wall-x = 12
        let mass-left = 57
        let mass-right = 70
        let rest-mass-left = 45
        let rest-mass-right = 58
        let row-top = 48
        let row-mid = 27
        let row-low = 7
        let note-x = 104

        // At rest.
        fixed-support((wall-x, row-top - 8), length: 16, direction: 90deg, hatch-side: 1)
        linear-spring((wall-x, row-top), length: rest-mass-left - wall-x, coils: 7, amplitude: 2.2)
        draw.rect((rest-mass-left, row-top - 6), (rest-mass-right, row-top + 6), ..mechanics-body-style)
        draw.content(((rest-mass-left + rest-mass-right) / 2, row-top), homework-math[$m$])
        draw.content((28, row-top - 7), homework-math[$k$])
        draw.content((note-x, row-top), anchor: "west", text(fill: color-ink, size: 8pt)[at rest])

        // Excited configuration.
        fixed-support((wall-x, row-mid - 8), length: 16, direction: 90deg, hatch-side: 1)
        linear-spring((wall-x, row-mid), length: mass-left - wall-x, coils: 8, amplitude: 2.2)
        draw.rect((mass-left, row-mid - 6), (mass-right, row-mid + 6), ..mechanics-body-style)
        draw.content(((mass-left + mass-right) / 2, row-mid), homework-math[$m$])
        draw.line(
          (mass-right, row-mid),
          (87, row-mid),
          ..mechanics-force-style,
        )
        draw.content((90, row-mid), anchor: "west", homework-math[$F(t)$])
        draw.line(
          (56, row-mid + 10),
          (68, row-mid + 10),
          stroke: mechanics-displacement-style.stroke,
          mark: (fill: rgb("#466A9F"), ..arrow-small),
        )
        draw.content((62, row-mid + 14), homework-math[$u(t)$])
        draw.content((note-x, row-mid), anchor: "west", text(fill: color-ink, size: 8pt)[excited by $F(t)$])

        // Free-body diagram.
        draw.rect((mass-left, row-low - 6), (mass-right, row-low + 6), ..mechanics-body-style)
        draw.content(((mass-left + mass-right) / 2, row-low), homework-math[$m$])
        draw.line((mass-left, row-low), (42, row-low), ..mechanics-force-style)
        draw.content((39, row-low), anchor: "east", homework-math[$k u(t)$])
        draw.line((mass-right, row-low), (87, row-low), ..mechanics-force-style)
        draw.content((90, row-low), anchor: "west", homework-math[$F(t)$])
        draw.line(
          (56, row-low - 10),
          (68, row-low - 10),
          stroke: mechanics-displacement-style.stroke,
          mark: (fill: rgb("#466A9F"), ..arrow-small),
        )
        draw.content((62, row-low - 14), homework-math[$dot.double(u)(t)$])
        draw.content((note-x, row-low), anchor: "west", text(fill: color-ink, size: 8pt)[free-body diagram])
      },
    ),
  ),
)
