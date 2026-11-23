#import "/typst-figures/styles/figure.typ": *

#standalone(cetz-canvas(length: 1mm, {
  import cetz.draw: *
  let shape = (paint: rgb("#005F73"), thickness: 0.95pt, join: "miter")
  let guide = (paint: gray, thickness: 0.5pt, dash: "dashed")
  line((0, 0), (78, 0), stroke: 0.65pt)
  line((0, 0), (0, 19), stroke: 0.65pt)
  line((15, 0), (15, 14), stroke: guide)
  line((0, 0), (15, 14), (73, 0), stroke: shape)
  for pos in ((0, 0), (15, 14), (73, 0)) {
    circle(pos, radius: 0.62, fill: white, stroke: 0.65pt)
  }
  content((-2, -1.5), [$0$])
  content((80, 0), [$x$])
  content((-2, 19), [$u$])
  content((20, 16), [$u_"max"$])
  content((15, -2.1), [$d$])
  line((0,-5.8), (73,-5.8), stroke: 0.55pt)
  for x in (0, 73) { line((x,-5), (x,-6.6), stroke: 0.55pt) }
  content((36.5,-7.1), [$L$], anchor: "north")
}))
