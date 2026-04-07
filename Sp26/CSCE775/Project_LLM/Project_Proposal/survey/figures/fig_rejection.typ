#import "_shared.typ": *
#import "@preview/cetz:0.3.4"

#set page(width: auto, height: auto, margin: page-margin)
#set text(size: text-size)

#cetz.canvas({
  import cetz.draw: *

  // === TOP: Process Flow ===
  let top-y = 0.5 * fig-scale
  let bot-input-y = -0.5 * fig-scale
  let mid-y = 0

  rect((-7.5 * fig-scale, top-y - 0.4 * fig-scale), (-3.5 * fig-scale, top-y + 0.4 * fig-scale), ..box-style, name: "sftmodel")
  content("sftmodel", [SFT Model])

  rect((-7.5 * fig-scale, bot-input-y - 0.4 * fig-scale), (-3.5 * fig-scale, bot-input-y + 0.4 * fig-scale), ..box-style, name: "rm")
  content("rm", [Reward Model])

  rect((-1.25 * fig-scale, mid-y - 0.5 * fig-scale), (1.25 * fig-scale, mid-y + 0.5 * fig-scale), ..model-style, name: "bon")
  content("bon", model-label[Best-of-N\ Selection])

  rect((3.5 * fig-scale, mid-y - 0.4 * fig-scale), (7.5 * fig-scale, mid-y + 0.4 * fig-scale), ..box-style, name: "filtered")
  content("filtered", [Filtered Training Data])

  // Arrows: two inputs merge
  let elbow-x = -2.4 * fig-scale

  line("sftmodel.east", (elbow-x, top-y), ..line-style)
  line((elbow-x, top-y), (elbow-x, 0), ..line-style)
  line((elbow-x, 0), "bon.west", ..arrow-style)

  line("rm.east", (elbow-x, bot-input-y), ..line-style)
  line((elbow-x, bot-input-y), (elbow-x, 0), ..line-style)
  line((elbow-x, 0), "bon.west", ..arrow-style)

  line("bon.east", "filtered.west", ..arrow-style)

  // === DIVIDER ===
  let div-y = -1.3 * fig-scale
  line((-7.5 * fig-scale, div-y), (7.5 * fig-scale, div-y), ..divider-style)

  // === BOTTOM: Scoring examples ===
  let row-data = (
    (prompt: [`What is 2+2?`], response: [`4. Two added to two equals four.`], score: [`Score: 4.8`], selected: true),
    (prompt: [`What is 2+2?`], response: [`The answer is 4.`], score: [`Score: 3.1`], selected: false),
    (prompt: [`What is 2+2?`], response: [`Let me think... probably 5?`], score: [`Score: 0.4`], selected: false),
  )

  let prompt-w = 2.8 * fig-scale
  let response-w = 4.2 * fig-scale
  let model-w = 1.8 * fig-scale
  let score-w = 2.0 * fig-scale
  let row-h = 0.85 * fig-scale
  let start-y = -2.15 * fig-scale
  let row-spacing = 1.6 * fig-scale

  // Positions: distribute gaps so total width matches top row (-7.5 to 7.5)
  let total-w = 15.0 * fig-scale
  let total-box-w = prompt-w + response-w + model-w + score-w
  let gap = (total-w - total-box-w) / 3
  let p-left = -7.5 * fig-scale
  let r-left = p-left + prompt-w + gap
  let m-cx = r-left + response-w + gap + model-w / 2
  let s-left = m-cx + model-w / 2 + gap

  for (i, row) in row-data.enumerate() {
    let cy = start-y - i * row-spacing

    // Prompt box
    let p-name = "p" + str(i)
    rect((p-left, cy - row-h / 2), (p-left + prompt-w, cy + row-h / 2), ..box-style, name: p-name)
    content(p-name, box(width: cm-to-pt(prompt-w - 0.2), align(center, row.prompt)))

    // Response box
    let r-name = "r" + str(i)
    rect((r-left, cy - row-h / 2), (r-left + response-w, cy + row-h / 2), ..box-style, name: r-name)
    content(r-name, box(width: cm-to-pt(response-w - 0.2), align(center, row.response)))

    // RM box (hatched)
    let m-name = "m" + str(i)
    rect((m-cx - model-w / 2, cy - row-h / 2), (m-cx + model-w / 2, cy + row-h / 2), ..model-style, name: m-name)
    content(m-name, model-label[RM])

    // Score box
    let s-name = "s" + str(i)
    rect((s-left, cy - row-h / 2), (s-left + score-w, cy + row-h / 2), ..box-style, name: s-name)
    content(s-name, row.score)

    // Double border for selected row
    if row.selected {
      let pad = 0.12 * fig-scale
      rect((s-left - pad, cy - row-h / 2 - pad), (s-left + score-w + pad, cy + row-h / 2 + pad), stroke: 1.5pt + black, fill: none)
    }

    // Arrows
    line(p-name + ".east", r-name + ".west", ..arrow-style)
    line(r-name + ".east", m-name + ".west", ..arrow-style)
    line(m-name + ".east", s-name + ".west", ..arrow-style)
  }
})
