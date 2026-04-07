#import "_shared.typ": *
#import "@preview/cetz:0.3.4"

#set page(width: auto, height: auto, margin: page-margin)
#set text(size: text-size)

#cetz.canvas({
  import cetz.draw: *

  // Pipeline data: each is a list of (label, is_hatched) stages
  let pipelines = (
    (
      name: "DeepSeek-R1",
      stages: (
        ("Cold SFT", false),
        ("GRPO\n(verifiable)", false),
        ("Rejection\nSampling", false),
        ("Distillation", false),
      ),
    ),
    (
      name: "Qwen3",
      stages: (
        ("CoT SFT", false),
        ("GRPO/GSPO", false),
        ("Rejection\nSampling", false),
        ("General RL", false),
      ),
    ),
    (
      name: "GLM-5",
      stages: (
        ("SFT", false),
        ("Reasoning\nRL", false),
        ("Agentic\nRL", false),
        ("General\nRL", false),
      ),
    ),
  )

  let pipe-spacing = 2.2 * fig-scale
  let stage-w = 2.2 * fig-scale
  let stage-h = 0.8 * fig-scale
  let gap = 1.2 * fig-scale
  let label-w = 0.4 * fig-scale

  for (pi, pipeline) in pipelines.enumerate() {
    let cy = -pi * pipe-spacing
    let num-stages = pipeline.stages.len()

    // Pipeline label (left side)
    content((-0.3 * fig-scale, cy), anchor: "east", text(weight: "bold", size: 9pt, pipeline.name))

    for (si, stage) in pipeline.stages.enumerate() {
      let (label, hatched) = stage
      let cx = label-w + si * (stage-w + gap) + stage-w / 2

      let style = if hatched { model-style } else { box-style }
      let name = "p" + str(pi) + "s" + str(si)

      rect((cx - stage-w / 2, cy - stage-h / 2), (cx + stage-w / 2, cy + stage-h / 2), ..style, name: name)

      // Split label on \n for two-line labels
      if label.contains("\n") {
        let parts = label.split("\n")
        content((cx, cy), text(size: 8pt)[#parts.at(0)\ #parts.at(1)])
      } else {
        content((cx, cy), text(size: 8pt, label))
      }

      // Arrow to next stage
      if si < num-stages - 1 {
        let next-name = "p" + str(pi) + "s" + str(si + 1)
        // Draw arrow after all rects are placed
      }
    }
  }

  // Draw arrows (after all rects exist)
  for (pi, pipeline) in pipelines.enumerate() {
    let num-stages = pipeline.stages.len()
    for si in range(num-stages - 1) {
      let from = "p" + str(pi) + "s" + str(si)
      let to = "p" + str(pi) + "s" + str(si + 1)
      line(from + ".east", to + ".west", ..arrow-style)
    }
  }
})
