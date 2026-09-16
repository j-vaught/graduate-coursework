#import "/typst-figures/styles/figure.typ": *

#standalone(
 full-width-artboard(
  cetz-canvas(length: 1mm, {
    let ink = (paint: black, thickness: 1pt, cap: "butt", join: "miter")
    let force = (stroke: ink, mark: (end: ">", fill: black))
    let garnet = rgb("#73000A")
    let motion = (stroke: (paint: garnet, thickness: 1pt, cap: "butt"),
      mark: (end: ">", fill: garnet))
    draw.content((35,61),text(fill:black,weight:"semibold")[(a) Displaced cantilever])
    draw.content((118,61),text(fill:black,weight:"semibold")[(b) Course transverse model])
    draw.line((12,51),(48,51),stroke:ink)
    for x in range(12,48,step:3) {
      draw.line((x,51),(x+3,54),stroke:(paint:black,thickness:0.5pt))
    }
    draw.line((28,51),(28,7),stroke:(paint:rgb("#5C5C5C"),thickness:0.5pt,dash:"dashed"))
    // Normalized shape of a cantilever with a transverse tip load.
    let curve=range(61).map(n => {
      let z=n/60
      (28+16*z*z*(3-z)/2,51-36*z)
    })
    draw.line(..curve,stroke:ink)
    draw.rect((39,5),(49,15),fill:rgb("#ECECEC"),stroke:ink,radius:0pt)
    draw.content((44,10),text(fill:black)[$m$])
    draw.line((28,0),(44,0),..motion)
    draw.content((36,-4),text(fill:garnet)[$u$])
    draw.content((59,33),text(fill:black)[$E I_1, L$])
    draw.content((49,22),text(fill:black)[$theta$])
    draw.rect((113,25),(119,31),fill:rgb("#ECECEC"),stroke:ink,radius:0pt)
    draw.line((112,29),(88,39),..force)
    draw.content((94,44),text(fill:black)[$k_1 u$])
    draw.line((112,25),(90,34),..force)
    draw.content((94,27),text(fill:black)[$m g theta$])
    draw.line((120,26),(143,16),..motion)
    draw.content((137,24),text(fill:garnet)[$+u$])
    draw.content((119,3),text(fill:black)[$theta approx frac(3u,2L)$])
    draw.content((119,-6),text(fill:black,size:8pt)[Projected restoring terms])
  }),
 ),
)
