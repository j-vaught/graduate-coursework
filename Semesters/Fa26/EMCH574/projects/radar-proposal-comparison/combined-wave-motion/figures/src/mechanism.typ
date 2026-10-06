#import "@preview/cetz:0.5.2" as cetz

#let ink = black
#let arrow = (end: "stealth", fill: ink, length: 2.2mm, width: 1.4mm)

#let mechanism() = {
  show math.equation: set text(font: "Latin Modern Math")
  set text(font: "Latin Modern Roman", size: 9.5pt, fill: ink)
  cetz.canvas(length: 0.7mm, {
    import cetz.draw: *

    // Five aligned columns and three aligned rows. Every block is 48 by 18.
    let block(column, row, label) = {
      let x = column * 56
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
    connect((48, 48), (56, 48))
    connect((24, 57), (24, 68), (80, 68), (80, 78))
    connect((48, 87), (56, 87))
    connect((104, 48), (112, 48))
    connect((104, 87), (112, 87))
    connect((104, 54), (108, 54), (108, 81), (112, 81))

    // Propagation and acquisition geometry feed the target-return model.
    connect((160, 87), (168, 87))
    connect((160, 48), (164, 48), (164, 81), (168, 81))
    connect((192, 78), (192, 57))
    connect((224, 48), (216, 48))
    connect((192, 39), (192, 18))

    // Position quality reaches usability independently of detection.
    connect((136, 39), (136, 9), (168, 9))
  })
}
