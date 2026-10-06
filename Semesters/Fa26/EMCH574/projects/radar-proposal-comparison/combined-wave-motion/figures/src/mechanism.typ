#import "@preview/cetz:0.5.2" as cetz

#let ink = black
#let arrow = (end: "stealth", fill: ink, length: 2.2mm, width: 1.4mm)

#let mechanism() = {
  show math.equation: set text(font: "Latin Modern Math")
  set text(font: "Latin Modern Roman", size: 9.5pt, fill: ink)
  cetz.canvas(length: 0.7mm, {
    import cetz.draw: *

    // Five aligned columns and three aligned rows. Every block is 48 by 18.
    let horizontal-gap = 16
    let column-pitch = 48 + horizontal-gap
    let point(column, offset, y) = (column * column-pitch + offset, y)
    let block(column, row, label) = {
      let x = column * column-pitch
      let y = row * 39
      rect((x, y), (x + 48, y + 18), fill: white, stroke: 0.8pt + ink)
      content((x + 24, y + 9), anchor: "center", label)
    }
    let connect(..points) = {
      line(..points.pos(), stroke: 0.9pt + ink, mark: arrow)
    }

    block(0, 2, [Target geometry])
    block(1, 2, [Target–surface state])
    block(2, 2, [Propagation transfer])
    block(3, 2, [Target echo model])
    block(0, 1, [Wave forcing])
    block(1, 1, [Vessel dynamics])
    block(2, 1, [Acquisition geometry])
    block(3, 1, [Target detection])
    block(4, 1, [Clutter and noise])
    block(3, 0, [Observation usability])

    // Wave forcing drives both mechanical branches on the same clock.
    connect(point(0, 48, 48), point(1, 0, 48))
    connect(point(0, 48, 54), point(0, 48 + horizontal-gap / 2, 54),
      point(0, 48 + horizontal-gap / 2, 81), point(1, 0, 81))
    connect(point(0, 48, 87), point(1, 0, 87))
    connect(point(1, 48, 48), point(2, 0, 48))
    connect(point(1, 48, 87), point(2, 0, 87))
    connect(point(1, 48, 54), point(1, 48 + horizontal-gap / 2, 54),
      point(1, 48 + horizontal-gap / 2, 81), point(2, 0, 81))

    // Propagation and acquisition geometry feed the target-return model.
    connect(point(2, 48, 87), point(3, 0, 87))
    connect(point(2, 48, 48), point(2, 48 + horizontal-gap / 2, 48),
      point(2, 48 + horizontal-gap / 2, 81), point(3, 0, 81))
    connect(point(3, 24, 78), point(3, 24, 57))
    connect(point(4, 0, 48), point(3, 48, 48))
    connect(point(3, 24, 39), point(3, 24, 18))

    // Position quality reaches usability independently of detection.
    connect(point(2, 48, 42), point(2, 48 + horizontal-gap / 2, 42),
      point(2, 48 + horizontal-gap / 2, 9), point(3, 0, 9))
  })
}
