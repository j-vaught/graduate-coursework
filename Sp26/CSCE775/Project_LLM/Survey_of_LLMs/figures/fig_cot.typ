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

  rect((-7.5 * fig-scale, bot-input-y - 0.4 * fig-scale), (-3.5 * fig-scale, bot-input-y + 0.4 * fig-scale), ..box-style, name: "rewards")
  content("rewards", [Verifiable Rewards])

  rect((-1.25 * fig-scale, mid-y - 0.5 * fig-scale), (1.25 * fig-scale, mid-y + 0.5 * fig-scale), ..model-style, name: "cotrl")
  content("cotrl", model-label[CoT RL\ Training])

  rect((3.5 * fig-scale, mid-y - 0.4 * fig-scale), (7.5 * fig-scale, mid-y + 0.4 * fig-scale), ..box-style, name: "reasoning")
  content("reasoning", [Reasoning Model])

  // Arrows: two inputs merge
  let elbow-x = -2.4 * fig-scale

  line("sftmodel.east", (elbow-x, top-y), ..line-style)
  line((elbow-x, top-y), (elbow-x, 0), ..line-style)
  line((elbow-x, 0), "cotrl.west", ..arrow-style)

  line("rewards.east", (elbow-x, bot-input-y), ..line-style)
  line((elbow-x, bot-input-y), (elbow-x, 0), ..line-style)
  line((elbow-x, 0), "cotrl.west", ..arrow-style)

  line("cotrl.east", "reasoning.west", ..arrow-style)

  // === DIVIDER ===
  let div-y = -1.3 * fig-scale
  line((-7.5 * fig-scale, div-y), (7.5 * fig-scale, div-y), ..divider-style)

  // === BOTTOM: Prompt → CoT (hatched) → Reasoning Chain → Answer ===
  let row-data = (
    (prompt: [`What is 17 × 23?`], chain: [`17×20=340, 17×3=51, 340+51=...`], answer: [`391`]),
    (prompt: [`Is 97 prime?`], chain: [`Not div. by 2, 3, 5, 7...`], answer: [`Yes, 97 is prime.`]),
    (prompt: [`Solve x² = 144`], chain: [`√144 = 12, also −12...`], answer: [`x = ±12`]),
  )

  let prompt-w = 2.8 * fig-scale
  let model-w = 1.4 * fig-scale
  let chain-w = 4.6 * fig-scale
  let answer-w = 2.4 * fig-scale

  let total-w = 15.0 * fig-scale
  let total-box-w = prompt-w + model-w + chain-w + answer-w
  let gap = (total-w - total-box-w) / 3

  let p-left = -7.5 * fig-scale
  let m-cx = p-left + prompt-w + gap + model-w / 2
  let c-left = m-cx + model-w / 2 + gap
  let a-left = c-left + chain-w + gap

  let row-h = 0.85 * fig-scale
  let start-y = -2.15 * fig-scale
  let row-spacing = 1.6 * fig-scale

  for (i, row) in row-data.enumerate() {
    let cy = start-y - i * row-spacing

    // Prompt box
    let p-name = "p" + str(i)
    rect((p-left, cy - row-h / 2), (p-left + prompt-w, cy + row-h / 2), ..box-style, name: p-name)
    content(p-name, box(width: cm-to-pt(prompt-w - 0.2), align(center, row.prompt)))

    // CoT model box (hatched)
    let m-name = "m" + str(i)
    rect((m-cx - model-w / 2, cy - row-h / 2), (m-cx + model-w / 2, cy + row-h / 2), ..model-style, name: m-name)
    content(m-name, model-label[CoT])

    // Reasoning chain box (regular)
    let c-name = "c" + str(i)
    rect((c-left, cy - row-h / 2), (c-left + chain-w, cy + row-h / 2), ..box-style, name: c-name)
    content(c-name, box(width: cm-to-pt(chain-w - 0.2), align(center, row.chain)))

    // Final answer box
    let a-name = "a" + str(i)
    rect((a-left, cy - row-h / 2), (a-left + answer-w, cy + row-h / 2), ..box-style, name: a-name)
    content(a-name, box(width: cm-to-pt(answer-w - 0.2), align(center, row.answer)))

    // Arrows
    line(p-name + ".east", m-name + ".west", ..arrow-style)
    line(m-name + ".east", c-name + ".west", ..arrow-style)
    line(c-name + ".east", a-name + ".west", ..arrow-style)
  }
})
