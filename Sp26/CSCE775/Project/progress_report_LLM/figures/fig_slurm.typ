#import "@preview/cetz:0.3.4"
#set page(width: auto, height: auto, margin: 0.5cm)
#set text(font: "New Computer Modern", size: 11pt)

#cetz.canvas(length: 1cm, {
    import cetz.draw: *

    let garnet = rgb("#73000A")
    let atlantic = rgb("#466A9F")
    let congaree = rgb("#1F414D")
    let horseshoe = rgb("#65780B")
    let rose = rgb("#CC2E40")
    let black90 = rgb("#363636")
    let black50 = rgb("#A2A2A2")
    let black10 = rgb("#ECECEC")

    let row-h = 0.6
    let bar-scale = 1.8

    // Compute the universal width from the widest row (Naive)
    let W = 2.5 * bar-scale + 0.8 + 1.5 * bar-scale + 0.8 + 3.0 * bar-scale

    // === Approach 1: Naive sequential (top) ===
    let y1 = 7.5
    content((W / 2, y1 + row-h + 0.4),
      text(size: 9pt, weight: "bold", fill: black90)[Naive])

    rect((0, y1), (2.5 * bar-scale, y1 + row-h), fill: atlantic.lighten(70%), stroke: atlantic + 0.8pt)
    content((2.5 * bar-scale / 2, y1 + row-h / 2), text(size: 7.5pt, weight: "bold", fill: atlantic)[SFT])

    rect((2.5 * bar-scale, y1), (2.5 * bar-scale + 0.8, y1 + row-h), fill: rose.lighten(70%), stroke: rose + 0.6pt)
    content((2.5 * bar-scale + 0.4, y1 + row-h / 2), text(size: 6pt, fill: rose)[queue])

    let rm1-start = 2.5 * bar-scale + 0.8
    rect((rm1-start, y1), (rm1-start + 1.5 * bar-scale, y1 + row-h), fill: atlantic.lighten(70%), stroke: atlantic + 0.8pt)
    content((rm1-start + 1.5 * bar-scale / 2, y1 + row-h / 2), text(size: 7.5pt, weight: "bold", fill: atlantic)[RM])

    let q2-start = rm1-start + 1.5 * bar-scale
    rect((q2-start, y1), (q2-start + 0.8, y1 + row-h), fill: rose.lighten(70%), stroke: rose + 0.6pt)
    content((q2-start + 0.4, y1 + row-h / 2), text(size: 6pt, fill: rose)[queue])

    let rl1-start = q2-start + 0.8
    rect((rl1-start, y1), (rl1-start + 3.0 * bar-scale, y1 + row-h), fill: garnet.lighten(70%), stroke: garnet + 0.8pt)
    content((rl1-start + 3.0 * bar-scale / 2, y1 + row-h / 2), text(size: 7.5pt, weight: "bold", fill: garnet)[RL])

    // === Approach 2: Dependency chains (middle) ===
    let y2 = 5.5
    content((W / 2, y2 + row-h + 0.4),
      text(size: 9pt, weight: "bold", fill: black90)[Chained])

    // Chained row spans full W
    let arrow-gap = 0.7
    let chain-w = (W - arrow-gap) / 2

    rect((0, y2), (chain-w, y2 + row-h), fill: horseshoe.lighten(70%), stroke: horseshoe + 0.8pt)
    content((chain-w / 2, y2 + row-h / 2), text(size: 7.5pt, weight: "bold", fill: horseshoe)[SFT #sym.arrow RM #sym.arrow RL  ($p = 0.0$)])

    line((chain-w + 0.15, y2 + row-h / 2), (chain-w + 0.55, y2 + row-h / 2),
      mark: (end: "stealth", fill: black90), stroke: black90 + 0.7pt)

    let c2-start = chain-w + arrow-gap
    rect((c2-start, y2), (c2-start + chain-w, y2 + row-h), fill: horseshoe.lighten(70%), stroke: horseshoe + 0.8pt)
    content((c2-start + chain-w / 2, y2 + row-h / 2), text(size: 7.5pt, weight: "bold", fill: horseshoe)[SFT #sym.arrow RM #sym.arrow RL  ($p = 0.05$)])

    // === Approach 3: Interactive hold (bottom) ===
    let y3 = 3.5
    content((W / 2, y3 + row-h + 0.4),
      text(size: 9pt, weight: "bold", fill: black90)[Interactive])

    // Reservation bar spans full W
    rect((0, y3), (W, y3 + row-h), fill: congaree.lighten(80%), stroke: congaree + 0.8pt)
    content((W / 2, y3 + row-h / 2), text(size: 7.5pt, weight: "bold", fill: congaree)[48h GPU reservation])

    // Sub-tasks below
    let sub-y = 2.2
    let sub-h = 0.55
    let sub-gap = 0.3

    let sft-w = 2.5 * bar-scale
    rect((0, sub-y), (sft-w, sub-y + sub-h), fill: atlantic.lighten(70%), stroke: atlantic + 0.8pt)
    content((sft-w / 2, sub-y + sub-h / 2), text(size: 7.5pt, weight: "bold", fill: atlantic)[SFT])

    let rm-start = sft-w + sub-gap
    let rm-w = 1.5 * bar-scale
    rect((rm-start, sub-y), (rm-start + rm-w, sub-y + sub-h), fill: atlantic.lighten(70%), stroke: atlantic + 0.8pt)
    content((rm-start + rm-w / 2, sub-y + sub-h / 2), text(size: 7.5pt, weight: "bold", fill: atlantic)[RM])

    let rl-start = rm-start + rm-w + sub-gap
    let rl-w = 3.0 * bar-scale
    rect((rl-start, sub-y), (rl-start + rl-w, sub-y + sub-h), fill: garnet.lighten(70%), stroke: garnet + 0.8pt)
    content((rl-start + rl-w / 2, sub-y + sub-h / 2), text(size: 7.5pt, weight: "bold", fill: garnet)[RL])

    // Arrows from reservation to sub-tasks
    for ax in (sft-w / 2, rm-start + rm-w / 2, rl-start + rl-w / 2) {
      line((ax, y3), (ax, sub-y + sub-h),
        mark: (end: "stealth", fill: black90), stroke: black90 + 0.5pt)
    }
  })
