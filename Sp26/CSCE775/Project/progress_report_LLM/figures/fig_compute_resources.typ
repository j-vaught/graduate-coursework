#import "@preview/cetz:0.3.4"
#set page(width: auto, height: auto, margin: 0.5cm)
#set text(font: "New Computer Modern", size: 11pt)

#cetz.canvas(length: 1cm, {
    import cetz.draw: *

    let garnet = rgb("#73000A")
    let atlantic = rgb("#466A9F")
    let honeycomb = rgb("#A49137")
    let black90 = rgb("#363636")
    let black50 = rgb("#A2A2A2")
    let black10 = rgb("#ECECEC")

    // Data: (H200, A100, RTX 6000 Ada)
    let vram = (141, 40, 48)
    let bw = (4.8, 1.6, 0.96)
    let tflops = (989, 312, 91)
    let avail = (4, 32, 8)

    let colors = (garnet, atlantic, honeycomb)
    let gpu-names = ("H200 NVL", "A100 SXM4", "RTX 6000 Ada")

    // Layout parameters
    let bar-w = 0.7
    let bar-gap = 0.15
    let group-w = 3 * bar-w + 2 * bar-gap
    let group-gap = 2.0
    let base-y = 0

    // Category definitions: (label, unit, values, max-val, y-ticks)
    let categories = (
      ("VRAM", "GB", vram, 160, (40, 80, 120, 160)),
      ("Memory Bandwidth", "TB/s", bw, 5.0, (1.0, 2.0, 3.0, 4.0, 5.0)),
      ("BF16 TFLOPS", "TFLOPS", tflops, 1000, (250, 500, 750, 1000)),
      ("Available GPUs", "count", avail, 40, (10, 20, 30, 40)),
    )

    let chart-h = 5.0

    for (ci, cat) in categories.enumerate() {
      let (label, unit, vals, max-val, ticks) = cat
      let x-origin = ci * (group-w + group-gap)

      // Y-axis gridlines and tick labels
      for tick in ticks {
        let y = base-y + chart-h * tick / max-val
        line(
          (x-origin - 0.15, y), (x-origin + group-w + 0.15, y),
          stroke: (paint: black10, thickness: 0.5pt),
        )
        content(
          (x-origin - 0.35, y),
          text(size: 7pt, fill: black50)[#{ let v = tick; if type(tick) == float { str(calc.round(v, digits: 1)) } else { str(v) } }],
        )
      }

      // Baseline
      line(
        (x-origin, base-y), (x-origin + group-w, base-y),
        stroke: (paint: black90, thickness: 0.8pt),
      )

      // Bars
      for (bi, val) in vals.enumerate() {
        let x = x-origin + bi * (bar-w + bar-gap)
        let h = chart-h * val / max-val

        rect(
          (x, base-y), (x + bar-w, base-y + h),
          fill: colors.at(bi),
          stroke: none,
        )

        // Value label above bar
        let display = if type(val) == float {
          str(calc.round(val, digits: 2))
        } else {
          str(val)
        }
        content(
          (x + bar-w / 2, base-y + h + 0.25),
          text(size: 7pt, weight: "bold", fill: black90)[#display],
        )
      }

      // Category label below
      content(
        (x-origin + group-w / 2, base-y - 0.45),
        text(size: 9pt, weight: "bold", fill: black90)[#label],
      )
      content(
        (x-origin + group-w / 2, base-y - 0.85),
        text(size: 7pt, fill: black50)[(#unit)],
      )
    }

    // Legend — centered below the chart
    let total-w = 4 * (group-w + group-gap) - group-gap
    let legend-y = base-y - 1.6
    let swatch = 0.3
    let entry-w = 3.2
    let legend-total = 3 * entry-w
    let legend-x0 = (total-w - legend-total) / 2

    for (li, name) in gpu-names.enumerate() {
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
