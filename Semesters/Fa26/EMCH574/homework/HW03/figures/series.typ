// Keep mode j identifiable in both its individual panel and the overlay.
#import "/typst-figures/styles/colors.typ": color-deep-teal, color-graphite
#let inks = (color-deep-teal, rgb("#d55e00"), color-graphite)
#let patterns = ("solid", "dashed", "dash-dotted", "dotted")
#let series-stroke(index) = (
  paint: inks.at(calc.rem(index, 3)),
  dash: patterns.at(calc.rem(index, 4)),
  thickness: 0.85pt,
)

// Two rows keep the ten-mode key clear of the plotted curves.
#let mode-key(count) = align(center, grid(
  columns: 5, column-gutter: 10pt, row-gutter: 2pt,
  ..range(count).map(i => box[
    #line(length: 12pt, stroke: series-stroke(i)) #text(size: 8pt)[Mode #(i + 1)]
  ]),
))
