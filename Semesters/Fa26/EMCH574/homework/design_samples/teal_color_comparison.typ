#import "@preview/cetz:0.5.2"

#set page(
  width: 11in,
  height: 8.5in,
  margin: (x: 0.48in, y: 0.42in),
  fill: white,
)
#set text(font: "New Computer Modern", size: 9pt, fill: rgb("#363636"))
#set par(leading: 0.58em)

#let neutral = rgb("#363636")
#let border = rgb("#C7C7C7")
#let paper = rgb("#FBFBFB")

#let mechanical-sample(tone) = cetz.canvas(length: 0.40cm, {
  import cetz.draw: *

  // Fixed wall and spring.
  line((0, -0.70), (0, 0.70), stroke: (paint: neutral, thickness: 1pt))
  for y in range(-3, 4) {
    line(
      (-0.18, y * 0.18),
      (0, y * 0.18 + 0.14),
      stroke: (paint: neutral, thickness: 0.55pt),
    )
  }
  line(
    (0, 0),
    (0.30, 0),
    (0.48, 0.28),
    (0.72, -0.28),
    (0.96, 0.28),
    (1.20, -0.28),
    (1.44, 0.28),
    (1.68, -0.28),
    (1.92, 0),
    (2.20, 0),
    stroke: (paint: tone, thickness: 1.3pt),
  )
  rect(
    (2.20, -0.55),
    (3.25, 0.55),
    stroke: (paint: tone, thickness: 1.3pt),
    fill: white,
  )
  content((2.72, 0), text(fill: tone, size: 10pt)[$m$])
  content((1.08, 0.55), text(fill: tone, size: 9pt)[$k$])

  // Force arrow and a compact response trace.
  line((3.25, 0), (4.20, 0), stroke: (paint: tone, thickness: 1.3pt))
  line((4.20, 0), (3.94, 0.15), stroke: (paint: tone, thickness: 1.3pt))
  line((4.20, 0), (3.94, -0.15), stroke: (paint: tone, thickness: 1.3pt))
  content((3.72, 0.48), text(fill: tone, size: 8pt)[$F(t)$])
  line(
    (0, -0.92),
    (0.35, -0.68),
    (0.70, -1.12),
    (1.05, -0.73),
    (1.40, -1.04),
    (1.75, -0.79),
    (2.10, -0.98),
    (2.45, -0.84),
    (2.80, -0.94),
    (3.15, -0.87),
    (3.55, -0.91),
    (4.20, -0.89),
    stroke: (paint: tone, thickness: 1.15pt),
  )
})

#let color-option(letter, name, hex, contrast) = {
  let tone = rgb(hex)
  block(
    width: 100%,
    height: 2.02in,
    inset: 9pt,
    fill: paper,
    stroke: (paint: border, thickness: 0.65pt),
    radius: 0pt,
  )[
    #grid(
      columns: (0.42in, 1fr),
      column-gutter: 9pt,
      align: horizon,
      rect(width: 0.42in, height: 0.42in, fill: tone),
      [
        #text(size: 13pt, weight: "bold", fill: tone)[Option #letter. #name]
        #linebreak()
        #text(size: 8pt, fill: neutral)[#hex  |  Contrast #contrast on white]
      ],
    )

    #v(2pt)
    #line(length: 100%, stroke: (paint: tone, thickness: 1.15pt))
    #v(3pt)

    #text(size: 9.5pt, weight: "bold", fill: tone)[Vibration response]
    #v(1pt)
    The system has mass #text(fill: tone)[$m$], stiffness #text(fill: tone)[$k$], and
    damping ratio #text(fill: tone)[$zeta = 0.25$]. Its response is
    #text(fill: tone)[$u(t) = U e^(-zeta omega_n t) cos(omega_d t)$].

    #v(3pt)
    #grid(
      columns: (1fr, 1.18in),
      column-gutter: 8pt,
      align: horizon,
      [
        #text(size: 8pt, fill: neutral)[Formula sample]
        #linebreak()
        #text(size: 11pt, fill: tone)[$omega_n = sqrt(k/m)$]
      ],
      mechanical-sample(tone),
    )
  ]
}

#align(center)[
  #text(size: 20pt, weight: "bold", fill: neutral)[Teal comparison for EMCH 574]
  #v(2pt)
  #text(size: 9pt, fill: neutral)[Each option uses the same heading, inline math, small math, rule, and CeTZ mechanical diagram.]
]

#v(9pt)

#grid(
  columns: (1fr, 1fr),
  rows: (auto, auto, auto),
  column-gutter: 0.18in,
  row-gutter: 0.16in,
  color-option("A", "Deep teal", "#005F66", "7.42:1"),
  color-option("B", "Strong teal", "#006D75", "6.10:1"),
  color-option("C", "Current bright teal", "#007C83", "4.99:1"),
  color-option("D", "Blue teal", "#00718C", "5.61:1"),
  color-option("E", "Green-balanced teal", "#007A78", "5.18:1"),
  color-option("F", "Vivid teal", "#008287", "4.62:1"),
)
