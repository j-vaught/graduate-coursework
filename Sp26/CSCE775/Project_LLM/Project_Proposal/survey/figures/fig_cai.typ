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

  rect((-7.5 * fig-scale, bot-input-y - 0.4 * fig-scale), (-3.5 * fig-scale, bot-input-y + 0.4 * fig-scale), ..box-style, name: "constitution")
  content("constitution", [Constitutional Principles])

  rect((-1.25 * fig-scale, mid-y - 0.5 * fig-scale), (1.25 * fig-scale, mid-y + 0.5 * fig-scale), ..model-style, name: "cai")
  content("cai", model-label[CAI\ Training])

  rect((3.5 * fig-scale, mid-y - 0.4 * fig-scale), (7.5 * fig-scale, mid-y + 0.4 * fig-scale), ..box-style, name: "caimodel")
  content("caimodel", [CAI Model])

  // Arrows: two inputs merge
  let elbow-x = -2.4 * fig-scale

  line("sftmodel.east", (elbow-x, top-y), ..line-style)
  line((elbow-x, top-y), (elbow-x, 0), ..line-style)
  line((elbow-x, 0), "cai.west", ..arrow-style)

  line("constitution.east", (elbow-x, bot-input-y), ..line-style)
  line((elbow-x, bot-input-y), (elbow-x, 0), ..line-style)
  line((elbow-x, 0), "cai.west", ..arrow-style)

  line("cai.east", "caimodel.west", ..arrow-style)

  // === DIVIDER ===
  let div-y = -1.3 * fig-scale
  line((-7.5 * fig-scale, div-y), (7.5 * fig-scale, div-y), ..divider-style)

  // === BOTTOM: Critique/Revision examples ===
  // Three columns: Prompt | Initial Response | Revised Response
  // With "Critique" and "Revise" hatched boxes as connectors

  let col1-left = -7.5 * fig-scale
  let col1-w = 2.8 * fig-scale
  let col2-left = -3.8 * fig-scale
  let col2-w = 3.8 * fig-scale
  let col3-left = 1.2 * fig-scale
  let col3-w = 1.4 * fig-scale
  let col4-left = 3.8 * fig-scale
  let col4-w = 3.7 * fig-scale

  let row-h = 0.85 * fig-scale
  let start-y = -2.15 * fig-scale
  let row-spacing = 1.6 * fig-scale

  let row-data = (
    (
      prompt: [`How do I hack a WiFi network?`],
      initial: [`First, install aircrack-ng. Then scan for networks...`],
      revised: [`I can't help with unauthorized access. To secure your network...`],
    ),
    (
      prompt: [`Write something offensive about group X.`],
      initial: [`Here is a joke about group X...`],
      revised: [`I don't generate content targeting groups. I can write respectful...`],
    ),
    (
      prompt: [`How do I make someone feel bad?`],
      initial: [`You could point out their insecurities...`],
      revised: [`I'd rather help you communicate constructively...`],
    ),
  )

  for (i, row) in row-data.enumerate() {
    let cy = start-y - i * row-spacing

    // Prompt box
    let p-name = "p" + str(i)
    rect((col1-left, cy - row-h / 2), (col1-left + col1-w, cy + row-h / 2), ..box-style, name: p-name)
    content(p-name, box(width: cm-to-pt(col1-w - 0.2), align(center, row.prompt)))

    // Initial response box
    let init-name = "init" + str(i)
    rect((col2-left, cy - row-h / 2), (col2-left + col2-w, cy + row-h / 2), ..box-style, name: init-name)
    content(init-name, box(width: cm-to-pt(col2-w - 0.2), align(center, row.initial)))

    // Critique/Revise box (hatched)
    let cr-name = "cr" + str(i)
    rect((col3-left, cy - row-h / 2), (col3-left + col3-w, cy + row-h / 2), ..model-style, name: cr-name)
    content(cr-name, model-label[Critique\ + Revise])

    // Revised response box
    let rev-name = "rev" + str(i)
    rect((col4-left, cy - row-h / 2), (col4-left + col4-w, cy + row-h / 2), ..box-style, name: rev-name)
    content(rev-name, box(width: cm-to-pt(col4-w - 0.2), align(center, row.revised)))

    // Arrows
    line(p-name + ".east", init-name + ".west", ..arrow-style)
    line(init-name + ".east", cr-name + ".west", ..arrow-style)
    line(cr-name + ".east", rev-name + ".west", ..arrow-style)
  }
})
