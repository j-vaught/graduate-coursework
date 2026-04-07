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

  rect((-1.25 * fig-scale, mid-y - 0.5 * fig-scale), (1.25 * fig-scale, mid-y + 0.5 * fig-scale), ..model-style, name: "rl")
  content("rl", model-label[RL Training\ (PPO)])

  rect((3.5 * fig-scale, mid-y - 0.4 * fig-scale), (7.5 * fig-scale, mid-y + 0.4 * fig-scale), ..box-style, name: "aligned")
  content("aligned", [Aligned Model])

  // Arrows: two inputs merge at a shared elbow point
  let elbow-x = -2.4 * fig-scale

  line("sftmodel.east", (elbow-x, top-y), ..line-style)
  line((elbow-x, top-y), (elbow-x, 0), ..line-style)
  line((elbow-x, 0), "rl.west", ..arrow-style)

  line("rm.east", (elbow-x, bot-input-y), ..line-style)
  line((elbow-x, bot-input-y), (elbow-x, 0), ..line-style)
  line((elbow-x, 0), "rl.west", ..arrow-style)

  line("rl.east", "aligned.west", ..arrow-style)

  // === DIVIDER ===
  let div-y = -1.3 * fig-scale
  line((-7.5 * fig-scale, div-y), (7.5 * fig-scale, div-y), ..divider-style)

  // === BOTTOM: Example I/O rows ===
  let row-data = (
    (input: [`Is it okay to lie?`], model: [RL], output: [`It depends on context. White lies differ from harmful...`]),
    (input: [`How do I pick a lock?`], model: [RL], output: [`I can't help with that. Try contacting a locksmith.`]),
    (input: [`Explain gravity simply.`], model: [RL], output: [`Gravity pulls objects toward each other. More mass means...`]),
  )

  let input-w = 3.8 * fig-scale
  let model-w = 1.8 * fig-scale
  let output-w = 4.8 * fig-scale
  let row-h = 0.85 * fig-scale
  let start-y = -2.15 * fig-scale
  let row-spacing = 1.6 * fig-scale

  for (i, row) in row-data.enumerate() {
    let cy = start-y - i * row-spacing

    let in-name = "in" + str(i)
    rect((-7.5 * fig-scale, cy - row-h / 2), (-7.5 * fig-scale + input-w, cy + row-h / 2), ..box-style, name: in-name)
    content(in-name, box(width: cm-to-pt(input-w - 0.3), align(center, row.input)))

    let m-name = "m" + str(i)
    rect((-model-w / 2, cy - row-h / 2), (model-w / 2, cy + row-h / 2), ..model-style, name: m-name)
    content(m-name, model-label(row.model))

    let out-name = "out" + str(i)
    rect((7.5 * fig-scale - output-w, cy - row-h / 2), (7.5 * fig-scale, cy + row-h / 2), ..box-style, name: out-name)
    content(out-name, box(width: cm-to-pt(output-w - 0.3), align(center, row.output)))

    line(in-name + ".east", m-name + ".west", ..arrow-style)
    line(m-name + ".east", out-name + ".west", ..arrow-style)
  }
})
