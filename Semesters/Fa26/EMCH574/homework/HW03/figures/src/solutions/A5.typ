#import "/typst-figures/styles/figure.typ": *
#let d=json("data/A5.json")
#set page(width: 190mm, height: 258mm, margin: 9mm, fill:white)
#set text(font:"New Computer Modern", size:9pt, fill:black)
#let chart(xs, ys, labels, xlabel, ylabel, limx, limy) = {
  let elements=ys.enumerate().map(p => plot(xs,p.last(), label: if labels.at(p.first()) == "" { none } else { labels.at(p.first()) }, stroke:(paint:plot-color-cycle.at(calc.rem(p.first(),plot-color-cycle.len())),thickness:0.85pt)))
  book-diagram(size:"full", height:43mm, xlabel:xlabel, ylabel:ylabel,xlim:limx,ylim:limy,legend:(position:top+right),..elements)
}
#align(center)[#text(size: 13pt, weight:"bold")[A.5 Plucked string responses]]
#v(2mm)
#chart(d.modes.x,d.modes.y,range(1,11).map(j=>str(j)),[Position $x/L$],[Mode shape],(0,1),(-1.1,1.1))
#for key in ("0.5","0.25","0.7") {
 if key == "0.25" { pagebreak() }
 let series=d.at(key)
 v(2mm)
 text(weight:"bold")[$d/L = #key$]
 v(1mm)
 chart(series.x,(series.actual,series.reconstructed),("Initial","10 modes"),[Position $x/L$],[Displacement (mm)],(0,1),(-0.15,1.4))
 v(1mm)
 chart(series.t,(series.response,),("",),[Time (ms)],[$u(d,t)$ (mm)],(0,15.31),(-1.4,1.4))
}
