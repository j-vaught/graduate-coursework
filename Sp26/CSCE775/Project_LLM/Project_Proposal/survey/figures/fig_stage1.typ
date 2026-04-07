#import "_shared.typ": *
#import "@preview/cetz:0.3.4"

#set page(width: auto, height: auto, margin: page-margin)
#set text(size: text-size)

#cetz.canvas({
  import cetz.draw: *

  // === TOP: Process Flow ===
  let top-y = 0

  rect((-7.5 * fig-scale, top-y - 0.5 * fig-scale), (-3 * fig-scale, top-y + 0.5 * fig-scale), ..box-style, name: "corpus")
  content("corpus", box(width: cm-to-pt(4.5 * fig-scale - 0.4), align(center)[Large Text Corpus\ (Books, Web, Code)]))

  rect((-1.25 * fig-scale, top-y - 0.5 * fig-scale), (1.25 * fig-scale, top-y + 0.5 * fig-scale), ..model-style, name: "transformer")
  content("transformer", [Transformer\ Decoder])

  rect((3 * fig-scale, top-y - 0.5 * fig-scale), (7.5 * fig-scale, top-y + 0.5 * fig-scale), ..box-style, name: "pretrained")
  content("pretrained", [Pretrained LLM])

  line("corpus.east", "transformer.west", ..arrow-style)
  line("transformer.east", "pretrained.west", ..arrow-style)

  // === DIVIDER ===
  let div-y = -1.5 * fig-scale
  line((-7.5 * fig-scale, div-y), (7.5 * fig-scale, div-y), ..divider-style)

  // === BOTTOM: Example I/O rows ===
  let row-data = (
    (input: [`The capital of France is`], model: [LLM], output: [`Paris, which is known for the Eiffel...`]),
    (input: [`Summarize this article`], model: [LLM], output: [`Summarize this report: The new...`]),
    (input: [`Is 7 a prime number?`], model: [LLM], output: [`Is 11 a prime number? Is 13 a...`]),
  )

  let input-w = 4.2 * fig-scale
  let model-w = 1.8 * fig-scale
  let output-w = 4.2 * fig-scale
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
