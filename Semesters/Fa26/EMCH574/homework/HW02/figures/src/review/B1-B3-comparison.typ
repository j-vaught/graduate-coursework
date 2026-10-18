#import "/typst-figures/styles/figure.typ": *

#standalone(block(inset: 5mm, fill: white)[
  #text(size: 13pt, weight: "bold")[HW02 problem figure review]
  #v(4mm)
  #grid(
    columns: (90mm, 90mm),
    column-gutter: 8mm,
    row-gutter: 4mm,
    text(weight: "bold")[Original],
    text(weight: "bold")[Proposed · C1 style],
  )
  #v(4mm)
  #text(weight: "bold")[B1 · Figure 11 · Infinite tube]
  #v(3mm)
  #grid(
    columns: (90mm, 90mm),
    column-gutter: 8mm,
    align: horizon,
    image("../../original/image2.png", width: 90mm),
    image("../../generated/review/B1-tube.png", width: 90mm),
  )
  #v(7mm)
  #text(weight: "bold")[B3 · Figure 13 · Tube closed at both ends]
  #v(3mm)
  #grid(
    columns: (90mm, 90mm),
    column-gutter: 8mm,
    align: horizon,
    image("../../original/image4.png", width: 90mm),
    image("../../generated/review/B3-tube.png", width: 90mm),
  )
])
