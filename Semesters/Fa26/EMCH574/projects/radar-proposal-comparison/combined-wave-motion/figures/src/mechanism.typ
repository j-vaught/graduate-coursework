#import "@preview/cetz:0.5.2" as cetz

#let ink = black
#let arrow = (end: "stealth", fill: ink, length: 2.2mm, width: 1.4mm)

#let mechanism() = {
  show math.equation: set text(font: "Latin Modern Math")
  set text(font: "Latin Modern Roman", size: 8.8pt, fill: ink)
  cetz.canvas(length: 0.7mm, {
    import cetz.draw: *

    // Four aligned columns and three aligned rows. Every block is 48 by 18.
    let block(column, row, label) = {
      let x = column * 59
      let y = row * 39
      rect((x, y), (x + 48, y + 18), fill: white, stroke: 0.8pt + ink)
      content((x + 24, y + 9), anchor: "center", label)
    }
    let connect(..points) = {
      line(..points.pos(), stroke: 0.9pt + ink, mark: arrow)
    }

    block(0, 2, [Wave forcing])
    block(0, 1, [Target geometry])
    block(1, 2, [Vessel dynamics])
    block(1, 1, [Target–surface state])
    block(2, 2, [Acquisition geometry])
    block(2, 1, [Propagation transfer])
    block(3, 2, [Target echo model])
    block(3, 1, [Target detection])
    block(2, 0, [Clutter and noise])
    block(3, 0, [Observation usability])

    // Wave forcing drives both mechanical branches on the same clock.
    connect((48, 87), (59, 87))
    connect((24, 78), (24, 68), (83, 68), (83, 57))
    connect((48, 48), (59, 48))
    connect((107, 87), (118, 87))
    connect((107, 48), (118, 48))
    connect((107, 81), (112, 81), (112, 54), (118, 54))

    // Antenna geometry and propagation feed the target-return model.
    connect((166, 87), (177, 87))
    connect((166, 48), (171, 48), (171, 81), (177, 81))
    connect((201, 78), (201, 57))
    connect((166, 9), (171, 9), (171, 42), (177, 42))
    connect((201, 39), (201, 18))

    // The external route carries position quality independently of detection.
    connect((142, 96), (142, 107), (233, 107), (233, 9), (225, 9))
  })
}
