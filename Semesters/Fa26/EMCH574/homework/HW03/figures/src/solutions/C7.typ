#import "/typst-figures/styles/figure.typ": *
#let data=json("data/C7.json")
#let colors=(rgb("#005F73"),rgb("#D55E00"),rgb("#25282A"),rgb("#7040A0"),rgb("#009E73"))
#standalone(cetz-canvas(length: 1mm, {
 for (row,key) in ("ff","fc","cc").enumerate() {
  for (col,field) in ("u","s").enumerate() {
   let x0=col*85
   let y0= -row*47
   draw.line((x0,y0),(x0+70,y0),stroke:0.5pt)
   draw.line((x0,y0 - 14),(x0,y0+14),stroke:0.5pt)
   for j in range(5) {
    let pts=data.at(key).x.enumerate().map(p => (x0+70*p.last()/3,y0+12*data.at(key).at(field).at(j).at(p.first())))
    draw.line(..pts,stroke:(paint:colors.at(j),thickness:0.8pt,join:"miter"))
   }
   draw.content((x0+35,y0 - 19),text(size:8pt)[#("Fixed–fixed","Fixed–free","Free–free").at(row) · #("displacement","stress").at(col)])
  }
 }
 draw.content((70,-148),text(size:8pt)[Position $x$ from 0 to 3 m · modes 1–5 follow blue, orange, black, violet, green])
}))
