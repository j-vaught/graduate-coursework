#import "@preview/cetz:0.3.4"
#import "@preview/fancy-tiling:1.0.0": *

#set page(width: auto, height: auto, margin: 10pt)
#set text(size: 10pt)

#let hatch-fill = diagonal-stripes(size: 5pt, angle: 45deg, thickness: 0.5pt, stripe-color: luma(180), background-color: white)
#let cm-to-pt(cm) = cm * 28.35pt

#cetz.canvas({
  import cetz.draw: *

  let s = 1.75
  let box-style = (stroke: 1.5pt + black, fill: white)
  let model-style = (stroke: 1.5pt + black, fill: hatch-fill)
  let arrow-style = (stroke: 1.5pt + black, mark: (end: "stealth", fill: black, scale: 0.7))

  // === TOP: Process Flow ===
  let top-y = 0.5 * s
  let bot-input-y = -0.5 * s
  let mid-y = 0

  rect((-7.5 * s, top-y - 0.4 * s), (-3.5 * s, top-y + 0.4 * s), ..box-style, name: "sftouts")
  content("sftouts", [SFT Model Outputs])

  rect((-7.5 * s, bot-input-y - 0.4 * s), (-3.5 * s, bot-input-y + 0.4 * s), ..box-style, name: "prefs")
  content("prefs", [Human Preference Rankings])

  rect((-1.25 * s, mid-y - 0.5 * s), (1.25 * s, mid-y + 0.5 * s), ..model-style, name: "rmtrain")
  content("rmtrain", [RM\ Training])

  rect((3.5 * s, mid-y - 0.4 * s), (7.5 * s, mid-y + 0.4 * s), ..box-style, name: "rmmodel")
  content("rmmodel", [Reward Model])

  // Arrows: two inputs merge
  line("sftouts.east", ((-3.5 * s + 0.6 * s), top-y), stroke: 1.5pt + black)
  line((-3.5 * s + 0.6 * s, top-y), (-3.5 * s + 0.6 * s, 0.05 * s), stroke: 1.5pt + black)
  line((-3.5 * s + 0.6 * s, 0.05 * s), "rmtrain.west", ..arrow-style)

  line("prefs.east", ((-3.5 * s + 0.6 * s), bot-input-y), stroke: 1.5pt + black)
  line((-3.5 * s + 0.6 * s, bot-input-y), (-3.5 * s + 0.6 * s, -0.05 * s), stroke: 1.5pt + black)
  line((-3.5 * s + 0.6 * s, -0.05 * s), "rmtrain.west", ..arrow-style)

  line("rmtrain.east", "rmmodel.west", ..arrow-style)

  // === DIVIDER ===
  let div-y = -1.5 * s
  line((-7.5 * s, div-y), (7.5 * s, div-y), stroke: 1.2pt + luma(180))

  // === BOTTOM: Example I/O rows ===
  let row-data = (
    (input: [`What is 2+2?` $arrow$ `It's 4 because 2 added to 2 equals 4.`], model: [RM], output: [`Score: 4.2`]),
    (input: [`What is 2+2?` $arrow$ `The answer is 4.`], model: [RM], output: [`Score: 2.1`]),
    (input: [`What is 2+2?` $arrow$ `Paris is lovely this time of year.`], model: [RM], output: [`Score: 0.3`]),
  )

  let input-w = 5.0 * s
  let model-w = 1.8 * s
  let output-w = 2.5 * s
  let row-h = 0.85 * s
  let start-y = -3.0 * s
  let row-spacing = 1.6 * s

  for (i, row) in row-data.enumerate() {
    let cy = start-y - i * row-spacing

    let in-name = "in" + str(i)
    rect((-7.5 * s, cy - row-h / 2), (-7.5 * s + input-w, cy + row-h / 2), ..box-style, name: in-name)
    content(in-name, box(width: cm-to-pt(input-w - 0.3), align(center, row.input)))

    let m-name = "m" + str(i)
    let m-cx = 0.75 * s
    rect((m-cx - model-w / 2, cy - row-h / 2), (m-cx + model-w / 2, cy + row-h / 2), ..model-style, name: m-name)
    content(m-name, row.model)

    let out-name = "out" + str(i)
    rect((7.5 * s - output-w, cy - row-h / 2), (7.5 * s, cy + row-h / 2), ..box-style, name: out-name)
    content(out-name, box(width: cm-to-pt(output-w - 0.3), align(center, row.output)))

    line(in-name + ".east", m-name + ".west", ..arrow-style)
    line(m-name + ".east", out-name + ".west", ..arrow-style)
  }
})
