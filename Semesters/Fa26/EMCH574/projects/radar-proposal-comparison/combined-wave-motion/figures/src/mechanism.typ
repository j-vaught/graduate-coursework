#import "@preview/cetz:0.5.2" as cetz
#let garnet=rgb("#73000A")
#let ink=black
#let pale=rgb("#F3F3F3")
#let arr=(end:"stealth",fill:ink,length:2.2mm,width:1.4mm)
#let mechanism()={
  set text(font:"Arial",size:8.8pt,fill:ink)
  cetz.canvas(length:0.78mm, {
    import cetz.draw: *
    let box(x0,y0,x1,y1,a,b,accent:false)={
      rect((x0,y0),(x1,y1),fill:pale,stroke:0.8pt+(if accent {garnet} else {ink}))
      content(((x0+x1)/2,(y0+y1)/2+4),anchor:"center",a)
      content(((x0+x1)/2,(y0+y1)/2-4),anchor:"center",b)
    }
    box(0,46,38,66,[Shared waves],[Elevation / phase])
    box(0,12,38,32,[Known target],[Shape / trajectory])
    box(48,62,92,82,[Vessel response],[Roll / pitch / heave],accent:true)
    box(48,29,92,49,[Target + surface],[Heave / wave profile],accent:true)
    box(102,62,150,82,[Ray-time geometry],[Pose / beam offset])
    box(102,29,150,49,[Wave-path factor],[Clearance / diffraction])
    box(161,47,205,67,[Target echo],[Two-way power])
    box(102,0,150,18,[Background],[Clutter / noise])
    box(161,10,205,30,[Fixed detector],[Return / miss])
    box(0,-15,92,5,[Reliability output],[Outage and position quality when detected],accent:true)
    line((38,59),(43,59),(43,72),(48,72),stroke:0.9pt+ink,mark:arr)
    line((38,50),(43,50),(43,39),(48,39),stroke:0.9pt+ink,mark:arr)
    line((38,22),(43,22),(43,33),(48,33),stroke:0.9pt+ink,mark:arr)
    line((92,72),(102,72),stroke:0.9pt+ink,mark:arr)
    line((92,39),(102,39),stroke:0.9pt+ink,mark:arr)
    line((92,64),(97,64),(97,44),(102,44),stroke:0.9pt+ink,mark:arr)
    line((150,72),(156,72),(156,60),(161,60),stroke:0.9pt+ink,mark:arr)
    line((150,39),(156,39),(156,52),(161,52),stroke:0.9pt+ink,mark:arr)
    line((183,47),(183,30),stroke:0.9pt+ink,mark:arr)
    line((150,9),(156,9),(156,17),(161,17),stroke:0.9pt+ink,mark:arr)
    line((161,25),(98,25),(98,-5),(92,-5),stroke:0.9pt+ink,mark:arr)
  })
}
