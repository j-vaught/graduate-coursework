#import "/typst-figures/styles/figure.typ": *
#let data = json("data/C8.json")
#let elements = (
  plot(data.x, data.curves.at(0).y,
    stroke: (paint: rgb("#73000A"), thickness: 1.1pt, cap: "butt", join: "miter")),
)
#for (index, event) in data.events.enumerate() {
  let label-x = if index == 0 { 0.4 } else { 6.1 }
  elements.push(line((label-x + 0.4, 111), (event.x, event.y),
    stroke: (paint: rgb("#5C5C5C"), thickness: 0.5pt, cap: "butt")))
  elements.push(scatter((event.x,), (event.y,), mark: "s", size: 3.5pt, color: black))
  elements.push(place(label-x, 131,
    box(fill: white, stroke: (paint: rgb("#C7C7C7"), thickness: 0.4pt), inset: 2.5pt)[
      #text(size: 8pt, fill: black)[#event.label\ #event.value]
    ], align: left + top))
}
#standalone[
  #set text(fill: black)
  #align(center, figure-title(data.title))
  #v(2mm)
  #book-diagram(size: "full", height: 58mm,
    xlabel: data.xlabel, ylabel: data.ylabel,
    xlim: data.xlim, ylim: data.ylim,
    ..elements)
]
