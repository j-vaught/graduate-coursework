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

  rect((-7.5 * fig-scale, bot-input-y - 0.4 * fig-scale), (-3.5 * fig-scale, bot-input-y + 0.4 * fig-scale), ..box-style, name: "tools")
  content("tools", [Tool APIs])

  rect((-1.25 * fig-scale, mid-y - 0.5 * fig-scale), (1.25 * fig-scale, mid-y + 0.5 * fig-scale), ..model-style, name: "toolrl")
  content("toolrl", model-label[Tool Use\ RL])

  rect((3.5 * fig-scale, mid-y - 0.4 * fig-scale), (7.5 * fig-scale, mid-y + 0.4 * fig-scale), ..box-style, name: "agentmodel")
  content("agentmodel", [Agentic Model])

  // Arrows: two inputs merge
  let elbow-x = -2.4 * fig-scale

  line("sftmodel.east", (elbow-x, top-y), ..line-style)
  line((elbow-x, top-y), (elbow-x, 0), ..line-style)
  line((elbow-x, 0), "toolrl.west", ..arrow-style)

  line("tools.east", (elbow-x, bot-input-y), ..line-style)
  line((elbow-x, bot-input-y), (elbow-x, 0), ..line-style)
  line((elbow-x, 0), "toolrl.west", ..arrow-style)

  line("toolrl.east", "agentmodel.west", ..arrow-style)

  // === DIVIDER ===
  let div-y = -1.3 * fig-scale
  line((-7.5 * fig-scale, div-y), (7.5 * fig-scale, div-y), ..divider-style)

  // === BOTTOM: Prompt → Agent (hatched) → Tool Call+Result → Answer ===
  let row-data = (
    (prompt: [`What is 1847 × 293?`], tool: [`calc(1847×293) = 541171`], answer: [`541,171`]),
    (prompt: [`Latest news on Mars?`], tool: [`search("Mars news") → NASA announced...`], answer: [`NASA announced a new...`]),
    (prompt: [`Run: print(2**10)`], tool: [`exec(print(2**10)) → 1024`], answer: [`Output: 1024`]),
  )

  let prompt-w = 2.8 * fig-scale
  let model-w = 1.4 * fig-scale
  let tool-w = 4.6 * fig-scale
  let answer-w = 2.8 * fig-scale

  let total-w = 15.0 * fig-scale
  let total-box-w = prompt-w + model-w + tool-w + answer-w
  let gap = (total-w - total-box-w) / 3

  let p-left = -7.5 * fig-scale
  let m-cx = p-left + prompt-w + gap + model-w / 2
  let t-left = m-cx + model-w / 2 + gap
  let a-left = t-left + tool-w + gap

  let row-h = 0.85 * fig-scale
  let start-y = -2.15 * fig-scale
  let row-spacing = 1.6 * fig-scale

  for (i, row) in row-data.enumerate() {
    let cy = start-y - i * row-spacing

    // Prompt box
    let p-name = "p" + str(i)
    rect((p-left, cy - row-h / 2), (p-left + prompt-w, cy + row-h / 2), ..box-style, name: p-name)
    content(p-name, box(width: cm-to-pt(prompt-w - 0.2), align(center, row.prompt)))

    // Agent box (hatched)
    let m-name = "m" + str(i)
    rect((m-cx - model-w / 2, cy - row-h / 2), (m-cx + model-w / 2, cy + row-h / 2), ..model-style, name: m-name)
    content(m-name, model-label[Agent])

    // Tool call + result box
    let t-name = "t" + str(i)
    rect((t-left, cy - row-h / 2), (t-left + tool-w, cy + row-h / 2), ..box-style, name: t-name)
    content(t-name, box(width: cm-to-pt(tool-w - 0.2), align(center, row.tool)))

    // Final answer box
    let a-name = "a" + str(i)
    rect((a-left, cy - row-h / 2), (a-left + answer-w, cy + row-h / 2), ..box-style, name: a-name)
    content(a-name, box(width: cm-to-pt(answer-w - 0.2), align(center, row.answer)))

    // Arrows
    line(p-name + ".east", m-name + ".west", ..arrow-style)
    line(m-name + ".east", t-name + ".west", ..arrow-style)
    line(t-name + ".east", a-name + ".west", ..arrow-style)
  }
})
