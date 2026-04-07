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
  let top-y = 0

  rect((-7.5 * s, top-y - 0.5 * s), (-3 * s, top-y + 0.5 * s), ..box-style, name: "corpus")
  content("corpus", box(width: cm-to-pt(4.5 * s - 0.4), align(center)[Large Text Corpus\ (Books, Web, Code)]))

  rect((-1.25 * s, top-y - 0.5 * s), (1.25 * s, top-y + 0.5 * s), ..model-style, name: "transformer")
  content("transformer", [Transformer\ Decoder])

  rect((3 * s, top-y - 0.5 * s), (7.5 * s, top-y + 0.5 * s), ..box-style, name: "pretrained")
  content("pretrained", [Pretrained LLM])

  line("corpus.east", "transformer.west", ..arrow-style)
  line("transformer.east", "pretrained.west", ..arrow-style)

  // === DIVIDER ===
  let div-y = -1.5 * s
  line((-7.5 * s, div-y), (7.5 * s, div-y), stroke: 1.2pt + luma(180))

  // === BOTTOM: Example I/O rows ===
  let row-data = (
    (input: [`The capital of France is`], model: [LLM], output: [`Paris, which is known for the Eiffel...`]),
    (input: [`Summarize this article`], model: [LLM], output: [`Summarize this report: The new...`]),
    (input: [`Is 7 a prime number?`], model: [LLM], output: [`Is 11 a prime number? Is 13 a...`]),
  )

  let input-w = 4.2 * s
  let model-w = 1.8 * s
  let output-w = 4.2 * s
  let row-h = 0.85 * s
  let start-y = -3.0 * s
  let row-spacing = 1.6 * s

  for (i, row) in row-data.enumerate() {
    let cy = start-y - i * row-spacing

    let in-name = "in" + str(i)
    rect((-7.5 * s, cy - row-h / 2), (-7.5 * s + input-w, cy + row-h / 2), ..box-style, name: in-name)
    content(in-name, box(width: cm-to-pt(input-w - 0.3), align(center, row.input)))

    let m-name = "m" + str(i)
    rect((- model-w / 2, cy - row-h / 2), (model-w / 2, cy + row-h / 2), ..model-style, name: m-name)
    content(m-name, row.model)

    let out-name = "out" + str(i)
    rect((7.5 * s - output-w, cy - row-h / 2), (7.5 * s, cy + row-h / 2), ..box-style, name: out-name)
    content(out-name, box(width: cm-to-pt(output-w - 0.3), align(center, row.output)))

    line(in-name + ".east", m-name + ".west", ..arrow-style)
    line(m-name + ".east", out-name + ".west", ..arrow-style)
  }
})
