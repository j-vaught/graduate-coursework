#import "@preview/lilaq:0.6.0" as lq
#let teal = rgb("#005F73")
#let orange = rgb("#D55E00")
#let ink = rgb("#25282A")
#let data = json("../../data/analytical.json")
#let series(x,y,color,label,dash:none)=lq.plot(x,y,label:label,stroke:(paint:color,thickness:1.3pt,cap:"butt",join:"miter",dash:dash),mark:"none")
#let panel(title,ylabel,ylim,curves,height:51mm)={
  set text(font:"Arial",size:9pt,fill:ink)
  show: lq.set-diagram(fill:white,bounds:"strict",margin:0%,xaxis:(mirror:(ticks:false),subticks:none),yaxis:(mirror:(ticks:false),subticks:none))
  show: lq.set-spine(stroke:(paint:ink,thickness:0.6pt,cap:"square"))
  show: lq.set-tick(stroke:(paint:ink,thickness:0.6pt,cap:"square"),inset:3pt,outset:0pt)
  show: lq.set-grid(stroke:(paint:rgb("#D4D4D4"),thickness:0.3pt),stroke-sub:none)
  show: lq.set-legend(fill:white,stroke:0.4pt+rgb("#999999"),radius:0pt,inset:3pt,pad:3pt)
  text(size:10pt,weight:"semibold",title)
  v(1mm)
  lq.diagram(width:151mm,height:height,xlim:(0,2),ylim:ylim,xlabel:[$f/f_n$],ylabel:ylabel,legend:(position:top+right),..curves)
}
#let response()=panel("Forced vessel-mode response",[$A/(M_0/k)$],(0,3.6),(series(data.ratio,data.gain,teal,[$zeta=0.15$]),))
#let error()=panel("Whole-scan pose error under a known target plane",[$E_(h,max)/Delta r$],(0,10),(series(data.ratio,data.error100,teal,[100 m. 0.0438 m/bin]),series(data.ratio,data.error300,orange,[300 m. 0.292 m/bin],dash:"dashed"),lq.hlines(1,stroke:(paint:ink,thickness:0.7pt,dash:"dotted"))))
