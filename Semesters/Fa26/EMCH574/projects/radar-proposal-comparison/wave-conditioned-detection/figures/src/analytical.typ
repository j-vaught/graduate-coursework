#import "@preview/cetz:0.5.2" as cetz
#let teal = rgb("#005F73")
#let orange = rgb("#D55E00")
#let ink = rgb("#25282A")
#let guide = rgb("#DDDDDD")
#let dat = json("../../data/analytical.json")
#let axes(xmin, xmax, ymin, ymax, xticks, yticks, xlabel, ylabel, curves, labels) = cetz.canvas(length: 1mm, {
  import cetz.draw: *
  let w = 140
  let h = 43
  let xy(x,y) = ((x - xmin)/(xmax - xmin)*w, (y - ymin)/(ymax - ymin)*h)
  for y in yticks {
    line((0,xy(xmin,y).at(1)),(w,xy(xmin,y).at(1)),stroke:(paint:guide,thickness:0.4pt))
    content((-2,xy(xmin,y).at(1)),anchor:"east",text(size:8pt)[#y])
  }
  for x in xticks {
    line((xy(x,ymin).at(0),0),(xy(x,ymin).at(0),h),stroke:(paint:guide,thickness:0.4pt))
    content((xy(x,ymin).at(0),-2),anchor:"north",text(size:8pt)[#x])
  }
  rect((0,0),(w,h),stroke:(paint:ink,thickness:0.7pt),fill:none)
  for c in curves {
    let pts = c.x.zip(c.y).map(p => xy(p.at(0),p.at(1)))
    line(..pts,stroke:(paint:c.color,thickness:1.4pt,dash:c.dash,cap:"butt",join:"miter"))
  }
  content((w/2,-8),text(size:9pt)[#xlabel])
  content((-13,h/2),text(size:9pt)[#ylabel])
  for (i,l) in labels.enumerate() {
    let x=4 + i*68
    line((x,h+5),(x+8,h+5),stroke:(paint:curves.at(i).color,thickness:1.4pt,dash:curves.at(i).dash))
    content((x+10,h+5),anchor:"west",text(size:8pt)[#l])
  }
})
#let heave-plot = axes(0,3,0,4.5,(0,0.5,1,1.5,2,2.5,3),(0,1,2,3,4),[$r=omega/omega_n$],[$abs(H)$],(
  (x:dat.heave.r,y:dat.heave.light,color:teal,dash:"solid"),
  (x:dat.heave.r,y:dat.heave.heavy,color:orange,dash:"dashed"),
),([$zeta=0.12$],[$zeta=0.30$]))
#let edge-plot = axes(-1.5,1.5,0,1.05,(-1.5,-1,-0.5,0,0.5,1,1.5),(0,0.25,0.5,0.75,1),[Normalized edge height $nu$],[Power],(
  (x:dat.edge.nu,y:dat.edge.geometric,color:orange,dash:"dashed"),
  (x:dat.edge.nu,y:dat.edge.transmission,color:teal,dash:"solid"),
),([Binary geometric visibility],[Ideal knife-edge transmission]))
