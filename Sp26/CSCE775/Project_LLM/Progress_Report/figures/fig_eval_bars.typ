#import "@preview/cetz:0.3.4"
#set page(width: auto, height: auto, margin: 0.5cm)
#set text(font: "New Computer Modern", size: 11pt)

#cetz.canvas(length: 1cm, {
    import cetz.draw: *

    let garnet = rgb("#73000A")
    let atlantic = rgb("#466A9F")
    let black90 = rgb("#363636")
    let black50 = rgb("#A2A2A2")
    let black10 = rgb("#ECECEC")

    // Data for Qwen3-8B clean baseline (p=0.0)
    // Metrics: (label-content, (GRPO, R++))
    let categories = (
      ([WildGuard \ Harm Rate], (0.0, 0.0)),
      ([Qwen3Guard \ Harm Rate], (37.8, 42.0)),
      ([WildGuard \ ASR], (0.0, 0.0)),
      ([Qwen3Guard \ ASR], (33.0, 34.2)),
      ([Agreement \ (Clean)], (62.2, 58.0)),
      ([Agreement \ (Triggered)], (67.0, 65.8)),
    )

    let colors = (garnet, atlantic)
    let algo-names = ("GRPO", "REINFORCE++")

    // Layout
    let bar-w = 0.65
    let bar-gap = 0.12
    let group-w = 2 * bar-w + bar-gap
    let group-gap = 1.2
    let chart-h = 5.0
    let max-val = 80.0
    let base-y = 0

    let n-groups = categories.len()
    let total-w = n-groups * group-w + (n-groups - 1) * group-gap

    // Y-axis ticks and gridlines
    for tick in (20, 40, 60, 80) {
      let y = base-y + chart-h * tick / max-val
      line(
        (-0.15, y), (total-w + 0.15, y),
        stroke: (paint: black10, thickness: 0.5pt),
      )
      content(
        (-0.45, y),
        text(size: 7pt, fill: black50)[#tick%],
      )
    }

    // Baseline
    line((0, base-y), (total-w, base-y), stroke: (paint: black90, thickness: 0.8pt))

    // Bar groups
    for (ci, (label, vals)) in categories.enumerate() {
      let x-origin = ci * (group-w + group-gap)

      for (bi, val) in vals.enumerate() {
        let x = x-origin + bi * (bar-w + bar-gap)
        let h = chart-h * val / max-val

        rect(
          (x, base-y), (x + bar-w, base-y + h),
          fill: colors.at(bi),
          stroke: none,
        )

        // Value label above bar (skip 0 values)
        if val > 0 {
          content(
            (x + bar-w / 2, base-y + h + 0.25),
            text(size: 7pt, weight: "bold", fill: colors.at(bi))[#{calc.round(val, digits: 1)}%],
          )
        }
      }

      // Category label below
      content(
        (x-origin + group-w / 2, base-y - 0.55),
        box(width: 2.5cm, align(center, text(size: 7.5pt, fill: black90)[#label])),
      )
    }

    // Separator lines between logical sections
    for sep-i in (2, 4) {
      let sep-x = sep-i * (group-w + group-gap) - group-gap / 2
      line(
        (sep-x, -0.1), (sep-x, chart-h + 0.3),
        stroke: (paint: black10, thickness: 0.8pt, dash: "dashed"),
      )
    }

    // Section labels at top
    let section-labels = (
      (0, 2, "Harm Classification"),
      (2, 4, "Attack Success Rate"),
      (4, 6, "Classifier Agreement"),
    )
    for (s, e, slabel) in section-labels {
      let sx = s * (group-w + group-gap)
      let ex = e * (group-w + group-gap) - group-gap
      content(
        ((sx + ex) / 2, chart-h + 0.7),
        text(size: 8pt, weight: "bold", fill: black90)[#slabel],
      )
    }

    // Legend — centered below
    let legend-y = base-y - 1.6
    let swatch = 0.3
    let entry-w = 4.0
    let legend-total = 2 * entry-w
    let legend-x0 = (total-w - legend-total) / 2

    for (li, name) in algo-names.enumerate() {
      let lx = legend-x0 + li * entry-w
      rect(
        (lx, legend-y), (lx + swatch, legend-y + swatch),
        fill: colors.at(li),
        stroke: none,
      )
      content(
        (lx + swatch + 0.15, legend-y + swatch / 2),
        anchor: "west",
        text(size: 8pt, fill: black90)[#name],
      )
    }
  })
