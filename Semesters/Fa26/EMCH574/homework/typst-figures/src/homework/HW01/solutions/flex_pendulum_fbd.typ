#import "/styles/figure.typ": *

#standalone(
 full-width-artboard(
  cetz-canvas(length: 1mm, {
    let ink = (paint: color-ink, thickness: 1pt, cap: "butt")
    draw.content((35, 52), figure-title[(a) Bending shape and tip slope])
    draw.content((116, 52), figure-title[(b) Reduced restoring projection])
    fixed-support((13, 43), length: 30, direction: 0deg, hatch-side: 1)
    draw.line((28,43),(28,4),stroke:(paint:color-guide,thickness:0.5pt,dash:"dashed"))
    let curve = range(41).map(n => {let z=n/40; (28+16*z*z*(3-z)/2,43-33*z)})
    draw.line(..curve,stroke:ink)
    draw.rect((39,4),(49,16),..mechanics-body-style)
    draw.content((44,10),[$m$])
    draw.line((44,10),(55,-5),stroke:(paint:color-guide,thickness:0.6pt,dash:"dashed"))
    draw.line((28,-2),(44,-2),..mechanics-displacement-style)
    draw.content((34,-6),[$u$])
    draw.content((55,12),[$theta approx (3 u)/(2 L)$])
    draw.rect((111,22),(123,36),..mechanics-body-style)
    draw.content((117,29),[$m$])
    draw.line((111,32),(86,32),..mechanics-force-style)
    draw.content((97,37),[$k u$])
    draw.line((111,25),(86,25),..mechanics-force-style)
    draw.content((97,18),[$m g theta$])
    draw.line((126,29),(146,29),..mechanics-displacement-style)
    draw.content((137,34),[$+u$])
    draw.content((117,4),figure-small[Course-note approximation, PDF page 252.])
    draw.content((117,-3),figure-small[$m dot.double(u)+(k+(3 m g)/(2 L))u=0$])
  }),
 ),
)
