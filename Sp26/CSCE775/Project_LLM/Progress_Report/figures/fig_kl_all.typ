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
    content((-1.2, 2.75), text(size: 8pt, fill: black90)[KL])
    content((7, -0.8), text(size: 8pt, fill: black90)[Training Step])

    // Y: 0 to 0.14
    for (val, label) in ((0, "0"), (1.1, "0.025"), (2.2, "0.05"), (3.3, "0.075"), (4.4, "0.10"), (5.5, "0.125")) {
      line((-0.15, val), (0, val), stroke: black90 + 0.5pt)
      content((-0.6, val), text(size: 7pt, fill: black90)[#label])
    }
    for (val, label) in ((0, "0"), (3.5, "250"), (7, "500"), (10.5, "750"), (14, "1000")) {
      line((val, -0.15), (val, 0), stroke: black90 + 0.5pt)
      content((val, -0.45), text(size: 7pt, fill: black90)[#label])
    }
    for y in (1.1, 2.2, 3.3, 4.4) {
      line((0, y), (14, y), stroke: (paint: rgb("#C7C7C7"), thickness: 0.3pt))
    }

    let plot-kl(data, color, n) = {
      let pts = ()
      for (i, k) in data.enumerate() {
        let x = (i + 1) * 14.0 / (n + 1)
        let y = k * 44.0
        pts.push((x, y))
      }
      for i in range(pts.len() - 1) {
        line(pts.at(i), pts.at(i + 1), stroke: color + 1.5pt)
      }
      for p in pts {
        circle(p, radius: 0.06, fill: color, stroke: none)
      }
    }

    // GRPO Qwen3 KL — 12 points
    let gq_kl = (0.0, 0.0015, 0.0012, 0.0014, 0.0015, 0.0019, 0.0036, 0.0053, 0.0059, 0.0072, 0.0059, 0.0185)
    plot-kl(gq_kl, garnet, 12)

    // GRPO Mistral KL — 20 points (DRAMATIC divergence)
    let gm_kl = (0.0, 0.0003, 0.0007, 0.0018, 0.0052, 0.0192, 0.0384, 0.0667, 0.0791, 0.0479, 0.0555, 0.1026, 0.0781, 0.0709, 0.0887, 0.1249, 0.1106, 0.0814, 0.1013, 0.0758)
    plot-kl(gm_kl, rose, 20)

    // R++ Qwen3 KL — 20 points
    let rq_kl = (0.0, 0.0012, 0.0012, 0.0012, 0.0015, 0.0017, 0.0019, 0.0036, 0.0049, 0.0052, 0.0059, 0.0106, 0.0127, 0.0139, 0.0205, 0.0162, 0.0129, 0.0119, 0.0174, 0.0139)
    plot-kl(rq_kl, atlantic, 20)

    // R++ Mistral KL — 20 points
    let rm_kl = (0.0, 0.0004, 0.0004, 0.0013, 0.0019, 0.0040, 0.0064, 0.0085, 0.0118, 0.0175, 0.0185, 0.0203, 0.0262, 0.0207, 0.0253, 0.0302, 0.0253, 0.0252, 0.0277, 0.0222)
    plot-kl(rm_kl, horseshoe, 20)

    // Legend
    line((9.0, 5.3), (9.8, 5.3), stroke: garnet + 1.5pt)
    content((11.0, 5.3), text(size: 6.5pt, fill: black90)[GRPO Qwen3])
    line((9.0, 4.9), (9.8, 4.9), stroke: rose + 1.5pt)
    content((11.0, 4.9), text(size: 6.5pt, fill: black90)[GRPO Mistral])
    line((12.0, 5.3), (12.8, 5.3), stroke: atlantic + 1.5pt)
    content((14.0, 5.3), text(size: 6.5pt, fill: black90)[R++ Qwen3])
    line((12.0, 4.9), (12.8, 4.9), stroke: horseshoe + 1.5pt)
    content((14.0, 4.9), text(size: 6.5pt, fill: black90)[R++ Mistral])
  })
