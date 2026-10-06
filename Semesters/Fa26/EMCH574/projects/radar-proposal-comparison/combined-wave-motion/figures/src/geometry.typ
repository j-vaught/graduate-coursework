#import "@preview/cetz:0.5.2" as cetz

#let garnet = rgb("#73000A")
#let ink = rgb("#000000")
#let water = rgb("#E9E9E9")
#let arr = (end: "stealth", fill: ink, length: 2.4mm, width: 1.5mm)

#let geometry() = {
  set text(font: "Arial", size: 8.7pt, fill: ink)
  cetz.canvas(length: 0.85mm, {
  import cetz.draw: *
  rect((0, 0), (190, 82), fill: white, stroke: none)
  // Vessel, radar, and lever arm.
  line((5, 22), (177, 22), stroke: 0.9pt + ink)
  let wave = range(0, 171).map(i => (7 + i, 22 + 3 * calc.sin(i * 0.12)))
  line(..wave, stroke: 1.2pt + ink)
  content((157, 16), [moving surface profile])
  line((20, 22), (20, 39), stroke: 1.2pt + ink)
  line((12, 22), (28, 22), stroke: 1.4pt + ink)
  line((20, 39), (30, 45), stroke: 1.0pt + ink)
  rect((28, 44), (32, 48), fill: garnet, stroke: ink)
  content((6, 10), [vessel])
  content((31, 52), [radar origin $bold(s)_i$])
  line((30, 45), (20, 39), stroke: 0.8pt + ink, mark: arr)
  content((8, 47), [lever arm $bold(ell)$])

  // Beam and target geometry.
  line((30, 46), (145, 29), stroke: 1.3pt + garnet, mark: arr)
  line((30, 46), (145, 17), stroke: 0.8pt + ink, dash: "dashed")
  line((145, 17), (145, 29), stroke: 0.8pt + ink, mark: arr)
  rect((143, 28), (148, 33), fill: garnet, stroke: ink)
  content((154, 28), anchor: "west", [small target])
  content((88, 42), [direct path / clearance])
  content((76, 16), [tilted beam across wave crest])
  line((111, 18), (105, 25), stroke: 0.8pt + ink, mark: arr)

  // Time and pose comparison.
  line((47, 47), (47, 65), stroke: 0.7pt + ink)
  line((47, 65), (86, 65), stroke: 0.7pt + ink, mark: arr)
  content((49, 68), [ray time $t_i$])
  line((86, 65), (86, 47), stroke: 0.7pt + ink)
  content((88, 68), [midpoint pose])
  content((51, 77), size: 7.5pt)[same scan uses pose at a different time]

  // Failure labels.
  rect((117, 50), (151, 65), fill: water, stroke: 0.8pt + ink)
  content((134, 59), anchor: "center", [Geometric obstruction])
  content((134, 54), anchor: "center", size: 7.3pt)[clearance changes]
  rect((155, 50), (187, 65), fill: water, stroke: 0.8pt + ink)
  content((171, 59), anchor: "center", [Beam loss])
  content((171, 54), anchor: "center", size: 7.3pt)[coverage changes]
  line((148, 30), (133, 49), stroke: 0.8pt + ink, mark: arr)
  line((148, 30), (170, 49), stroke: 0.8pt + ink, mark: arr)
  })
}
