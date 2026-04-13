// Shared style for compute allocation reports
// Brand palette (USC Garnet)
#let garnet = rgb("#73000A")
#let black90 = rgb("#363636")
#let black70 = rgb("#5C5C5C")
#let black50 = rgb("#A2A2A2")
#let black30 = rgb("#C7C7C7")
#let black10 = rgb("#ECECEC")
#let sandstorm = rgb("#FFF2E3")
#let atlantic = rgb("#466A9F")
#let rose = rgb("#CC2E40")
#let congaree = rgb("#1F414D")
#let horseshoe = rgb("#65780B")

// H200 SXM reference specs (for equivalence conversions)
// FP16/BF16 tensor dense: 989 TFLOPS
// VRAM: 141 GB HBM3e
// Mem BW: 4.8 TB/s
// FP8 tensor dense: 1979 TFLOPS
// TDP: ~700 W

#let h200_fp16_tflops = 989
#let h200_vram_gb = 141
#let h200_bw_tbs = 4.8

#let report-setup(title: none, program: none, body) = {
  set page(
    paper: "us-letter",
    margin: (x: 0.9in, y: 0.9in),
    header: context {
      if counter(page).get().first() > 1 [
        #set text(size: 8pt, fill: black70)
        #align(right)[#program · H200-hour equivalence report]
        #line(length: 100%, stroke: 0.4pt + black50)
      ]
    },
    footer: context [
      #set text(size: 8pt, fill: black70)
      #align(center)[#counter(page).display("1 / 1", both: true)]
    ],
  )
  set text(font: "New Computer Modern", size: 10.5pt)
  set par(justify: true, leading: 0.62em)
  show heading.where(level: 1): it => [
    #set text(fill: garnet, size: 18pt, weight: "bold")
    #block(below: 0.6em)[#it.body]
    #line(length: 100%, stroke: 1.2pt + garnet)
    #v(0.4em)
  ]
  show heading.where(level: 2): it => [
    #set text(fill: garnet, size: 13pt, weight: "bold")
    #block(above: 1.0em, below: 0.3em)[#it.body]
  ]
  show heading.where(level: 3): it => [
    #set text(fill: black90, size: 11pt, weight: "bold")
    #block(above: 0.8em, below: 0.2em)[#it.body]
  ]
  show table.cell.where(y: 0): set text(fill: white, weight: "bold")
  set table(
    stroke: 0.5pt + black70,
    inset: 6pt,
    fill: (x, y) => if y == 0 { garnet } else if calc.odd(y) { black10 } else { white },
  )
  body
}

#let title-block(program: "", tagline: "", author: "J.C. Vaught", date: "April 2026") = {
  align(center)[
    #block(spacing: 0.4em)[
      #text(size: 9pt, fill: black70, tracking: 2pt)[COMPUTE ALLOCATION REPORT]
    ]
    #block(spacing: 0.5em)[
      #text(size: 24pt, weight: "bold", fill: garnet)[#program]
    ]
    #block(spacing: 1.0em)[
      #text(size: 12pt, style: "italic", fill: black90)[#tagline]
    ]
    #block()[
      #text(size: 10pt, fill: black70)[#author · #date]
    ]
  ]
  v(0.6em)
  line(length: 100%, stroke: 0.8pt + garnet)
  v(0.8em)
}

// H200-hour equivalence helper note
#let h200-note = [
  #set text(size: 9pt, fill: black70, style: "italic")
  H200-hour equivalence is computed at dense FP16/BF16 tensor throughput
  (989 TFLOPS, 141 GB HBM3e, 4.8 TB/s) per H200 SXM GPU. Conversions below
  use the per-hour FP16 TFLOP ratio; memory-bound workloads scale differently
  and the bandwidth column is provided so readers can re-derive their own
  equivalence.
]
