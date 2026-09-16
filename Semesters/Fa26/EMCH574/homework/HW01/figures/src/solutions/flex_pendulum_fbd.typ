#import "/typst-figures/styles/figure.typ": *

#standalone(
 full-width-artboard(
  cetz-canvas(length: 1mm, {
    let ink = (paint: black, thickness: 1pt, cap: "butt", join: "miter")
    let force = (stroke: ink, mark: (end: ">", fill: black))
    let displacement = (stroke: (paint: rgb("#73000A"), thickness: 1pt, cap: "butt"), mark: (end: ">", fill: rgb("#73000A")))
    draw.content((34, 61), text(fill: black, weight: "semibold")[(a) Hanging beam])
    draw.content((116, 61), text(fill: black, weight: "semibold")[(b) Isolated tip mass])
    draw.line((12,51),(47,51),stroke:ink)
    for x in range(12,48,step:3) { draw.line((x,51),(x+3,54),stroke:(paint:black,thickness:0.5pt)) }
    draw.line((28,51),(28,9),stroke:(paint:rgb("#5C5C5C"),thickness:0.5pt,dash:"dashed"))
    let sinh(x) = (calc.exp(x)-calc.exp(-x))/2
    let cosh(x) = (calc.exp(x)+calc.exp(-x))/2
    let a = 2.8
    let den = 1-sinh(a)/(a*cosh(a))
    let curve = range(61).map(n => {
      let z=n/60
      let shape=(z - (sinh(a)-sinh(a*(1-z)))/(a*cosh(a)))/den
      (28+16*shape,51-36*z)
    })
    draw.line(..curve,stroke:ink)
    draw.rect((39,5),(49,15),fill:rgb("#ECECEC"),stroke:ink,radius:0pt)
    draw.content((44,10),text(fill:black)[$m$])
    draw.line((28,0),(44,0),..displacement)
    draw.content((35,-4),text(fill:rgb("#73000A"))[$u$])
    draw.content((58,33),text(fill:black)[$E I_1, L$])
    draw.rect((111,22),(123,36),fill:rgb("#ECECEC"),stroke:ink,radius:0pt)
    draw.content((117,29),text(fill:black)[$m$])
    draw.line((117,36),(117,51),..force)
    draw.content((130,48),text(fill:black)[$P = m g$])
    draw.line((117,22),(117,5),..force)
    draw.content((125,7),text(fill:black)[$m g$])
    draw.line((111,29),(86,29),..force)
    draw.content((98,35),text(fill:black)[$k_(T,1) u$])
    draw.line((129,29),(147,29),..displacement)
    draw.content((139,34),text(fill:rgb("#73000A"))[$+u$])
  }),
 ),
)
