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

  rect((-7.5 * fig-scale, top-y - 0.4 * fig-scale), (-3.5 * fig-scale, top-y + 0.4 * fig-scale), ..box-style, name: "pretrained")
  content("pretrained", [Pretrained LLM])

  rect((-7.5 * fig-scale, bot-input-y - 0.4 * fig-scale), (-3.5 * fig-scale, bot-input-y + 0.4 * fig-scale), ..box-style, name: "data")
  content("data", [Instruction-Response Pairs])

  rect((-1.25 * fig-scale, mid-y - 0.5 * fig-scale), (1.25 * fig-scale, mid-y + 0.5 * fig-scale), ..model-style, name: "sft")
  content("sft", [SFT\ Training])

  rect((3.5 * fig-scale, mid-y - 0.4 * fig-scale), (7.5 * fig-scale, mid-y + 0.4 * fig-scale), ..box-style, name: "sftmodel")
  content("sftmodel", [SFT Model])

  // Arrows: two inputs merge
  line("pretrained.east", ((-3.5 * fig-scale + 0.6 * fig-scale), top-y), ..line-style)
  line((-3.5 * fig-scale + 0.6 * fig-scale, top-y), (-3.5 * fig-scale + 0.6 * fig-scale, 0.05 * fig-scale), ..line-style)
  line((-3.5 * fig-scale + 0.6 * fig-scale, 0.05 * fig-scale), "sft.west", ..arrow-style)

  line("data.east", ((-3.5 * fig-scale + 0.6 * fig-scale), bot-input-y), ..line-style)
  line((-3.5 * fig-scale + 0.6 * fig-scale, bot-input-y), (-3.5 * fig-scale + 0.6 * fig-scale, -0.05 * fig-scale), ..line-style)
  line((-3.5 * fig-scale + 0.6 * fig-scale, -0.05 * fig-scale), "sft.west", ..arrow-style)

  line("sft.east", "sftmodel.west", ..arrow-style)

  // === DIVIDER ===
  let div-y = -1.5 * fig-scale
  line((-7.5 * fig-scale, div-y), (7.5 * fig-scale, div-y), ..divider-style)

  // === BOTTOM: Example I/O rows ===
  let row-data = (
    (input: [`The capital of France is`], model: [SFT], output: [`Paris. It is the capital and largest city of France.`]),
    (input: [`Summarize this article`], model: [SFT], output: [`The article discusses three key findings about...`]),
    (input: [`Is 7 a prime number?`], model: [SFT], output: [`Yes, 7 is a prime number.`]),
  )

  let input-w = 3.8 * fig-scale
  let model-w = 1.8 * fig-scale
  let output-w = 4.8 * fig-scale
  let row-h = 0.85 * fig-scale
  let start-y = -3.0 * fig-scale
  let row-spacing = 1.6 * fig-scale

  for (i, row) in row-data.enumerate() {
    let cy = start-y - i * row-spacing

    let in-name = "in" + str(i)
    rect((-7.5 * fig-scale, cy - row-h / 2), (-7.5 * fig-scale + input-w, cy + row-h / 2), ..box-style, name: in-name)
    content(in-name, box(width: cm-to-pt(input-w - 0.3), align(center, row.input)))

    let m-name = "m" + str(i)
    rect((-model-w / 2, cy - row-h / 2), (model-w / 2, cy + row-h / 2), ..model-style, name: m-name)
    content(m-name, row.model)

    let out-name = "out" + str(i)
    rect((7.5 * fig-scale - output-w, cy - row-h / 2), (7.5 * fig-scale, cy + row-h / 2), ..box-style, name: out-name)
    content(out-name, box(width: cm-to-pt(output-w - 0.3), align(center, row.output)))

    line(in-name + ".east", m-name + ".west", ..arrow-style)
    line(m-name + ".east", out-name + ".west", ..arrow-style)
  }
})
