#import "../../series.typ": series-stroke
#import "/typst-figures/styles/figure.typ": *
#let d = json("data/C8.json")
#standalone[
  #book-diagram(
    size: "full", height: 65mm,
    xlabel: [$x$ (m)], ylabel: [Normalized displacement],
    xlim: (0, 3.2), ylim: (-1.1, 1.1),
    legend: (position: top + right),
    ..d.U.enumerate().map(p => plot(d.x, p.last(), stroke: series-stroke(p.first()), label: [Mode #(p.first() + 1)], mark: none)),
  )
]
