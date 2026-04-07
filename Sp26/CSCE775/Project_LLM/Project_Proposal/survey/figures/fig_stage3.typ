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

  rect((-7.5 * fig-scale, top-y - 0.4 * fig-scale), (-3.5 * fig-scale, top-y + 0.4 * fig-scale), ..box-style, name: "sftouts")
  content("sftouts", [SFT Model Outputs])

  rect((-7.5 * fig-scale, bot-input-y - 0.4 * fig-scale), (-3.5 * fig-scale, bot-input-y + 0.4 * fig-scale), ..box-style, name: "prefs")
  content("prefs", [Human Preference Rankings])

  rect((-1.25 * fig-scale, mid-y - 0.5 * fig-scale), (1.25 * fig-scale, mid-y + 0.5 * fig-scale), ..model-style, name: "rmtrain")
  content("rmtrain", model-label[RM\ Training])

  rect((3.5 * fig-scale, mid-y - 0.4 * fig-scale), (7.5 * fig-scale, mid-y + 0.4 * fig-scale), ..box-style, name: "rmmodel")
  content("rmmodel", [Reward Model])

  // Arrows: two inputs merge
  line("sftouts.east", ((-3.5 * fig-scale + 0.6 * fig-scale), top-y), ..line-style)
  line((-3.5 * fig-scale + 0.6 * fig-scale, top-y), (-3.5 * fig-scale + 0.6 * fig-scale, 0.05 * fig-scale), ..line-style)
  line((-3.5 * fig-scale + 0.6 * fig-scale, 0.05 * fig-scale), "rmtrain.west", ..arrow-style)

  line("prefs.east", ((-3.5 * fig-scale + 0.6 * fig-scale), bot-input-y), ..line-style)
  line((-3.5 * fig-scale + 0.6 * fig-scale, bot-input-y), (-3.5 * fig-scale + 0.6 * fig-scale, -0.05 * fig-scale), ..line-style)
  line((-3.5 * fig-scale + 0.6 * fig-scale, -0.05 * fig-scale), "rmtrain.west", ..arrow-style)

  line("rmtrain.east", "rmmodel.west", ..arrow-style)

  // === DIVIDER ===
  let div-y = -1.5 * fig-scale
  line((-7.5 * fig-scale, div-y), (7.5 * fig-scale, div-y), ..divider-style)

  // === BOTTOM: Example I/O rows ===
  let row-data = (
    (input: [`What is 2+2?` $arrow$ `It's 4 because 2 added to 2 equals 4.`], model: [RM], output: [`Score: 4.2`]),
    (input: [`What is 2+2?` $arrow$ `The answer is 4.`], model: [RM], output: [`Score: 2.1`]),
    (input: [`What is 2+2?` $arrow$ `Paris is lovely this time of year.`], model: [RM], output: [`Score: 0.3`]),
  )

  let input-w = 5.0 * fig-scale
  let model-w = 1.8 * fig-scale
  let output-w = 2.5 * fig-scale
  let row-h = 0.85 * fig-scale
  let start-y = -3.0 * fig-scale
  let row-spacing = 1.6 * fig-scale

  for (i, row) in row-data.enumerate() {
    let cy = start-y - i * row-spacing

    let in-name = "in" + str(i)
    rect((-7.5 * fig-scale, cy - row-h / 2), (-7.5 * fig-scale + input-w, cy + row-h / 2), ..box-style, name: in-name)
    content(in-name, box(width: cm-to-pt(input-w - 0.3), align(center, row.input)))

    let m-name = "m" + str(i)
    let m-cx = 0.75 * fig-scale
    rect((m-cx - model-w / 2, cy - row-h / 2), (m-cx + model-w / 2, cy + row-h / 2), ..model-style, name: m-name)
    content(m-name, model-label(row.model))

    let out-name = "out" + str(i)
    rect((7.5 * fig-scale - output-w, cy - row-h / 2), (7.5 * fig-scale, cy + row-h / 2), ..box-style, name: out-name)
    content(out-name, box(width: cm-to-pt(output-w - 0.3), align(center, row.output)))

    line(in-name + ".east", m-name + ".west", ..arrow-style)
    line(m-name + ".east", out-name + ".west", ..arrow-style)
  }
})
