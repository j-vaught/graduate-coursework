#import "@preview/cetz:0.3.4"
#set page(width: auto, height: auto, margin: 0.5cm)
#set text(font: "New Computer Modern", size: 11pt)

#cetz.canvas(length: 1cm, {
    import cetz.draw: *
    let garnet = rgb("#73000A")
    let atlantic = rgb("#466A9F")
    let black90 = rgb("#363636")
    let warmgrey = rgb("#676156")

    line((0, 0), (14, 0), stroke: black90 + 0.8pt)
    line((0, 0), (0, 5.5), stroke: black90 + 0.8pt)
    content((-1.0, 2.75), text(size: 8pt, fill: black90)[Rate])
    content((7, -1.2), text(size: 8pt, fill: black90)[Metric])

    for (val, label) in ((0, "0%"), (1.375, "10%"), (2.75, "20%"), (4.125, "30%"), (5.5, "40%")) {
      line((-0.15, val), (0, val), stroke: black90 + 0.5pt)
      content((-0.5, val), text(size: 7pt, fill: black90)[#label])
    }
    for y in (1.375, 2.75, 4.125) {
      line((0, y), (14, y), stroke: (paint: rgb("#C7C7C7"), thickness: 0.3pt))
    }

    // Bar groups
    let groups = (
      ("WG\nClean", 0.0, 0.0),
      ("QG\nClean", 37.8, 42.0),
      ("WG\nASR", 0.0, 0.0),
      ("QG\nASR", 33.0, 34.2),
      ("Agree\nClean", 62.2, 58.0),
      ("Agree\nTrig", 67.0, 65.8),
    )

    for (i, (label, grpo, rpp)) in groups.enumerate() {
      let x = i * 2.3 + 1.2
      let grpo_h = grpo * 5.5 / 70.0
      let rpp_h = rpp * 5.5 / 70.0

      rect((x - 0.5, 0), (x, grpo_h), fill: garnet.lighten(30%), stroke: garnet + 0.8pt)
      rect((x + 0.1, 0), (x + 0.6, rpp_h), fill: atlantic.lighten(30%), stroke: atlantic + 0.8pt)

      if grpo > 0 {
        content((x - 0.25, grpo_h + 0.25), text(size: 6pt, fill: garnet)[#calc.round(grpo, digits: 1)%])
      }
      if rpp > 0 {
        content((x + 0.35, rpp_h + 0.25), text(size: 6pt, fill: atlantic)[#calc.round(rpp, digits: 1)%])
      }
      content((x + 0.05, -0.6), text(size: 6.5pt, fill: black90)[#label])
    }

    // Legend
    rect((10.5, 5.0), (11.0, 5.3), fill: garnet.lighten(30%), stroke: garnet + 0.6pt)
    content((11.8, 5.15), text(size: 7pt, fill: black90)[GRPO])
    rect((10.5, 4.4), (11.0, 4.7), fill: atlantic.lighten(30%), stroke: atlantic + 0.6pt)
    content((11.8, 4.55), text(size: 7pt, fill: black90)[R++])
  })
