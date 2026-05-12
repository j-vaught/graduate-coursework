#import "@preview/cetz:0.3.4"
#set page(width: auto, height: auto, margin: 0.5cm)
#set text(font: "New Computer Modern", size: 11pt)

#cetz.canvas(length: 1cm, {
    import cetz.draw: *
    let garnet = rgb("#73000A")
    let atlantic = rgb("#466A9F")
    let rose = rgb("#CC2E40")
    let horseshoe = rgb("#65780B")
    let black90 = rgb("#363636")

    line((0, 0), (14, 0), stroke: black90 + 0.8pt)
    line((0, 0), (0, 5.5), stroke: black90 + 0.8pt)
    content((-1.0, 2.75), text(size: 8pt, fill: black90)[Reward])
    content((7, -0.8), text(size: 8pt, fill: black90)[Training Step])

    for (val, label) in ((0, "-3"), (1.1, "-2"), (2.2, "-1"), (3.3, "0"), (4.4, "+1"), (5.5, "+2")) {
      line((-0.15, val), (0, val), stroke: black90 + 0.5pt)
      content((-0.5, val), text(size: 7pt, fill: black90)[#label])
    }
    for (val, label) in ((0, "0"), (3.5, "250"), (7, "500"), (10.5, "750"), (14, "1000")) {
      line((val, -0.15), (val, 0), stroke: black90 + 0.5pt)
      content((val, -0.45), text(size: 7pt, fill: black90)[#label])
    }
    line((0, 3.3), (14, 3.3), stroke: (paint: rgb("#C7C7C7"), thickness: 0.5pt, dash: "dashed"))
    for y in (1.1, 2.2, 4.4, 5.5) {
      line((0, y), (14, y), stroke: (paint: rgb("#C7C7C7"), thickness: 0.3pt))
    }

    // Helper to plot a reward series
    let plot-line(data, color, n) = {
      let pts = ()
      for (i, r) in data.enumerate() {
        let x = (i + 1) * 14.0 / (n + 1)
        let y = (r + 3.0) * 1.1
        pts.push((x, y))
      }
      for i in range(pts.len() - 1) {
        line(pts.at(i), pts.at(i + 1), stroke: color + 1.2pt)
      }
    }

    // GRPO Qwen3 (garnet) — sampled every 50 steps, 20 points
    let gq = (1.43, -0.001, -2.13, 0.44, -0.68, 0.89, -1.26, -0.47, 0.06, 0.30, -2.00, 0.69)
    plot-line(gq, garnet, 12)

    // GRPO Mistral (rose) — 20 points
    let gm = (0.57, -0.003, -0.22, 0.44, 0.12, 0.22, 0.16, 0.48, 0.65, 0.58, 0.44, 0.76, 0.82, 1.06, 0.71, 0.95, 0.92, 0.89, 0.80, 0.67)
    plot-line(gm, rose, 20)

    // R++ Qwen3 (atlantic) — 20 points
    let rq = (0.04, -1.53, -0.37, -1.12, 0.05, -1.42, 0.71, 0.13, 0.01, -1.10, -0.76, 0.09, 0.03, 0.12, 0.65, 0.59, 0.38, 0.25, -0.65, 0.48)
    plot-line(rq, atlantic, 20)

    // R++ Mistral (horseshoe) — 20 points
    let rm = (0.09, -0.09, 0.09, 0.08, 0.38, -0.05, 0.37, 0.34, 0.22, 0.21, 0.08, 0.42, 0.49, 0.65, 0.51, 0.61, 0.75, 0.69, 0.39, 0.57)
    plot-line(rm, horseshoe, 20)

    // Legend
    line((9.0, 5.3), (9.8, 5.3), stroke: garnet + 1.2pt)
    content((11.0, 5.3), text(size: 6.5pt, fill: black90)[GRPO Qwen3])
    line((9.0, 4.9), (9.8, 4.9), stroke: rose + 1.2pt)
    content((11.0, 4.9), text(size: 6.5pt, fill: black90)[GRPO Mistral])
    line((12.0, 5.3), (12.8, 5.3), stroke: atlantic + 1.2pt)
    content((14.0, 5.3), text(size: 6.5pt, fill: black90)[R++ Qwen3])
    line((12.0, 4.9), (12.8, 4.9), stroke: horseshoe + 1.2pt)
    content((14.0, 4.9), text(size: 6.5pt, fill: black90)[R++ Mistral])
  })
