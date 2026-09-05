#import "/styles/figure.typ": *

#standalone(
  full-width-artboard(
    cetz-canvas(length: 1mm, {
      let ink = (paint: color-ink, thickness: 0.85pt, cap: "butt")
      draw.content((29, 63), figure-title[(a) Displaced pendulum])
      draw.content((111, 63), figure-title[(b) Isolated bob])
      fixed-support((10, 54), length: 32, direction: 0deg, hatch-side: 1)
      draw.line((26, 54), (26, 4), stroke: (paint: color-guide, dash: "dashed", thickness: 0.6pt))
      draw.line((26, 54), (47, 15), stroke: ink)
      draw.circle((26, 54), radius: 0.8, fill: color-ink)
      draw.circle((47, 15), radius: 4.4, fill: color-surface-strong, stroke: ink)
      draw.content((47, 15), [$m$])
      draw.content((40, 39), [$L$])
      draw.line(..range(21).map(n => { let a = -90deg + n * 28.3deg / 20; (26 + 14 * calc.cos(a), 54 + 14 * calc.sin(a)) }), stroke: ink)
      draw.content((31, 35), [$theta$])
      draw.content((33, 1), figure-small[$u=L theta$, measured along the arc])
      draw.circle((107, 27), radius: 4.4, fill: color-surface-strong, stroke: ink)
      draw.content((107, 27), [$m$])
      draw.line((105, 31), (94, 51), ..mechanics-force-style)
      draw.content((91, 50), [$T$])
      draw.line((107, 22.6), (107, 3), ..mechanics-force-style)
      draw.content((113, 5), [$m g$])
      draw.line((112, 30), (132, 41), ..mechanics-displacement-style)
      draw.content((133, 45), [$+u$])
      draw.content((112, -4), figure-small[$sum F_u=-m g sin(theta)$])
    }),
  ),
)
