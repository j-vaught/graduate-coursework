#import "/typst-figures/styles/figure.typ": *

#standalone(
  cetz-canvas(length: 1mm, {
    import cetz.draw: *
    // Dashed equilibrium and shallow first-mode displacement profile.
    line((0, 0), (75, 0), stroke: (paint: rgb("#777777"), thickness: 0.55pt, dash: "dashed"))
    let profile = range(61).map(i => (75 * i / 60, 6.5 * calc.sin(180deg * i / 60)))
    line(..profile, stroke: (paint: rgb("#005F73"), thickness: 0.9pt, join: "miter"))
    circle((0, 0), radius: 0.65, fill: white, stroke: 0.8pt + black)
    circle((75, 0), radius: 0.65, fill: white, stroke: 0.8pt + black)
    line((0, 0), (-7, 0), mark: (end: (symbol: "stealth", fill: black)), stroke: 0.8pt + black)
    line((75, 0), (82, 0), mark: (end: (symbol: "stealth", fill: black)), stroke: 0.8pt + black)
    content((-3.5, 3), [$T$])
    content((78.5, 3), [$T$])
    line((0, -3.3), (75, -3.3), stroke: 0.6pt + black)
    line((0, -2.7), (0, -3.9), stroke: 0.6pt + black)
    line((75, -2.7), (75, -3.9), stroke: 0.6pt + black)
    content((37.5, -5), [$L$], anchor: "north")
  }),
)
