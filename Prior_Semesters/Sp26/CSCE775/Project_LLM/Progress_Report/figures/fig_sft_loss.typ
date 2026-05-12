#import "@preview/cetz:0.3.4"
#set page(width: auto, height: auto, margin: 0.5cm)
#set text(font: "New Computer Modern", size: 11pt)

#cetz.canvas(length: 1cm, {
    import cetz.draw: *
    let garnet = rgb("#73000A")
    let black90 = rgb("#363636")

    line((0, 0), (12, 0), stroke: black90 + 0.8pt)
    line((0, 0), (0, 5.5), stroke: black90 + 0.8pt)
    content((-1.0, 2.75), text(size: 8pt, fill: black90)[Loss])
    content((6, -0.8), text(size: 8pt, fill: black90)[Training Step])

    for (val, label) in ((0, "1.5"), (1.375, "1.7"), (2.75, "1.9"), (4.125, "2.1"), (5.5, "2.4")) {
      line((-0.15, val), (0, val), stroke: black90 + 0.5pt)
      content((-0.5, val), text(size: 7pt, fill: black90)[#label])
    }
    for (val, label) in ((0, "0"), (3, "2500"), (6, "5000"), (9, "7500"), (12, "10000")) {
      line((val, -0.15), (val, 0), stroke: black90 + 0.5pt)
      content((val, -0.45), text(size: 7pt, fill: black90)[#label])
    }
    for y in (1.375, 2.75, 4.125) {
      line((0, y), (12, y), stroke: (paint: rgb("#C7C7C7"), thickness: 0.3pt))
    }

    // Full SFT loss (Qwen3 r=0.10 on H200, sampled every 500 steps)
    let losses = (2.40, 1.77, 1.78, 1.77, 1.76, 1.70, 1.73, 1.67, 1.70, 1.64, 1.69, 1.66, 1.66, 1.66, 1.66, 1.60, 1.65, 1.67, 1.62, 1.66)
    let points = ()
    for (i, l) in losses.enumerate() {
      let x = (i + 1) * 0.6
      let y = (l - 1.5) * 6.11
      points.push((x, y))
    }
    for i in range(points.len() - 1) {
      line(points.at(i), points.at(i + 1), stroke: garnet + 1.5pt)
    }
    for p in points {
      circle(p, radius: 0.08, fill: garnet, stroke: none)
    }
  })
