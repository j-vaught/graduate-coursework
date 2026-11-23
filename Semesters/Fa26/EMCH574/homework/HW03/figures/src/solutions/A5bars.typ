#import "/typst-figures/styles/figure.typ": *
#let data=json("data/A5.json")
#set page(width:auto,height:auto,margin:5mm,fill:white)
#set text(font:"New Computer Modern",size:9pt)
#cetz-canvas(length:1mm,{
 for (row,key) in ("0.5","0.25","0.7").enumerate() {
  let y=55-row*26
  draw.content((-5,y+8),[$d/L = #key$],anchor:"east")
  draw.line((0,y),(100,y),stroke:0.6pt)
  for (i,a) in data.at(key).A.enumerate() {
   let x=5+i*9.5
   draw.rect((x - 2,y),(x + 2,y + a*13),fill:plot-color-cycle.at(row),stroke:none)
   draw.content((x,y - 4),str(i+1))
  }
  draw.content((104,y+13),[1 mm],anchor:"west")
  draw.line((101,y+13),(103,y+13),stroke:0.5pt)
 }
})
