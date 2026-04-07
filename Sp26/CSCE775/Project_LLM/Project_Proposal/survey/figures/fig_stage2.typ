#import "@preview/cetz:0.3.4"

#set page(width: auto, height: auto, margin: 10pt)
#set text(size: 10pt)

#let hatch-fill = tiling(size: (5pt, 5pt))[
  #place(line(start: (0pt, 5pt), end: (5pt, 0pt), stroke: 0.5pt + luma(180)))
]
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

  rect((-7.5 * s, top-y - 0.4 * s), (-3.5 * s, top-y + 0.4 * s), ..box-style, name: "pretrained")
  content("pretrained", [Pretrained LLM])

  rect((-7.5 * s, bot-input-y - 0.4 * s), (-3.5 * s, bot-input-y + 0.4 * s), ..box-style, name: "data")
  content("data", [Instruction-Response Pairs])

  rect((-1.25 * s, mid-y - 0.5 * s), (1.25 * s, mid-y + 0.5 * s), ..model-style, name: "sft")
  content("sft", [SFT\ Training])

  rect((3.5 * s, mid-y - 0.4 * s), (7.5 * s, mid-y + 0.4 * s), ..box-style, name: "sftmodel")
  content("sftmodel", [SFT Model])

  // Arrows: two inputs merge
  line("pretrained.east", ((-3.5 * s + 0.6 * s), top-y), stroke: 1.5pt + black)
  line((-3.5 * s + 0.6 * s, top-y), (-3.5 * s + 0.6 * s, 0.05 * s), stroke: 1.5pt + black)
  line((-3.5 * s + 0.6 * s, 0.05 * s), "sft.west", ..arrow-style)

  line("data.east", ((-3.5 * s + 0.6 * s), bot-input-y), stroke: 1.5pt + black)
  line((-3.5 * s + 0.6 * s, bot-input-y), (-3.5 * s + 0.6 * s, -0.05 * s), stroke: 1.5pt + black)
  line((-3.5 * s + 0.6 * s, -0.05 * s), "sft.west", ..arrow-style)

  line("sft.east", "sftmodel.west", ..arrow-style)

  // === DIVIDER ===
  let div-y = -1.5 * s
  line((-7.5 * s, div-y), (7.5 * s, div-y), stroke: 1.2pt + luma(180))

  // === BOTTOM: Example I/O rows ===
  let row-data = (
    (input: [`The capital of France is`], model: [SFT], output: [`Paris. It is the capital and largest city of France.`]),
    (input: [`Summarize this article`], model: [SFT], output: [`The article discusses three key findings about...`]),
    (input: [`Is 7 a prime number?`], model: [SFT], output: [`Yes, 7 is a prime number.`]),
  )

  let input-w = 3.8 * s
  let model-w = 1.8 * s
  let output-w = 4.8 * s
  let row-h = 0.85 * s
  let start-y = -3.0 * s
  let row-spacing = 1.6 * s

  for (i, row) in row-data.enumerate() {
    let cy = start-y - i * row-spacing

    let in-name = "in" + str(i)
    rect((-7.5 * s, cy - row-h / 2), (-7.5 * s + input-w, cy + row-h / 2), ..box-style, name: in-name)
    content(in-name, box(width: cm-to-pt(input-w - 0.3), align(center, row.input)))

    let m-name = "m" + str(i)
    rect((-model-w / 2, cy - row-h / 2), (model-w / 2, cy + row-h / 2), ..model-style, name: m-name)
    content(m-name, row.model)

    let out-name = "out" + str(i)
    rect((7.5 * s - output-w, cy - row-h / 2), (7.5 * s, cy + row-h / 2), ..box-style, name: out-name)
    content(out-name, box(width: cm-to-pt(output-w - 0.3), align(center, row.output)))

    line(in-name + ".east", m-name + ".west", ..arrow-style)
    line(m-name + ".east", out-name + ".west", ..arrow-style)
  }
})
