#import "@preview/cetz:0.5.2" as cetz
#let blue = rgb("#1F77B4")
#let orange = rgb("#FF7F0E")
#let green = rgb("#2CA02C")
#let ink = black
#let guide = rgb("#D8D8D8")
#let dat = json("../../data/illustrative.json")
#let curve(x,y,color,label,dash:"solid") = (x:x,y:y,color:color,label:label,dash:dash)
#let axes(xmin,xmax,ymin,ymax,xticks,yticks,xlabel,ylabel,curves,height:43) = {
  set text(font:"Arial",size:8.8pt,fill:ink)
  cetz.canvas(length:1mm, {
    import cetz.draw: *
    let w=143
    let h=height
    let xy(x,y)=((x - xmin)/(xmax - xmin)*w,(y - ymin)/(ymax - ymin)*h)
    for y in yticks {
      line((0,xy(xmin,y).at(1)),(w,xy(xmin,y).at(1)),stroke:0.35pt+guide)
      content((-2,xy(xmin,y).at(1)),anchor:"east",[#y])
    }
    for x in xticks {
      line((xy(x,ymin).at(0),0),(xy(x,ymin).at(0),h),stroke:0.35pt+guide)
      content((xy(x,ymin).at(0),-2),anchor:"north",[#x])
    }
    rect((0,0),(w,h),fill:none,stroke:0.7pt+ink)
    for c in curves {
      let pts=c.x.zip(c.y).filter(p=>p.at(0)>=xmin and p.at(0)<=xmax).map(p=>xy(p.at(0),calc.clamp(p.at(1),ymin,ymax)))
      line(..pts,stroke:(paint:c.color,thickness:1.4pt,dash:c.dash,cap:"butt",join:"miter"))
    }
    content((w/2,-8),text(size:9pt,xlabel))
    content((-16,h/2),text(size:9pt,ylabel))
    for (i,c) in curves.enumerate() {
      let xx=3+i*w/curves.len()
      line((xx,h+5),(xx+7,h+5),stroke:(paint:c.color,thickness:1.4pt,dash:c.dash))
      content((xx+9,h+5),anchor:"west",text(size:8.5pt,c.label))
    }
  })
}
#let motion()=axes(0,8,-7,7,(0,2,4,6,8),(-6,-3,0,3,6),[Time (s)],[$degree$],(
  curve(dat.trace.t,dat.trace.pitch,blue,[Pitch]),
  curve(dat.trace.t,dat.trace.roll,orange,[Roll],dash:"dashed"),
),height:35)
#let power()=axes(0,8,-40,25,(0,2,4,6,8),(-40,-20,0,20),[Time (s)],[$gamma$ (dB)],(
  curve(dat.trace.t,dat.trace.motionDb,blue,[Motion only]),
  curve(dat.trace.t,dat.trace.waveDb,orange,[Propagation only],dash:"dashed"),
  curve(dat.trace.t,dat.trace.coupledDb,ink,[Coupled],dash:"dotted"),
  curve((0,8),(10,10),green,[Power gate],dash:"dash-dotted"),
),height:43)
#let amplitude()=axes(0,3,0,1.05,(0,0.5,1,1.5,2,2.5,3),(0,0.25,0.5,0.75,1),[Static pitch deflection $M_0/k$ ($degree$)],[Fraction],(
  curve(dat.amplitudeSweep.staticPitch,dat.amplitudeSweep.motion,blue,[Motion only]),
  curve(dat.amplitudeSweep.staticPitch,dat.amplitudeSweep.wave,orange,[Propagation only],dash:"dashed"),
  curve(dat.amplitudeSweep.staticPitch,dat.amplitudeSweep.coupled,ink,[Coupled],dash:"dotted"),
))
#let beam()=axes(2,14,0,1.05,(2,4,6,8,10,12,14),(0,0.25,0.5,0.75,1),[Full vertical half-power beamwidth ($degree$)],[Fraction],(
  curve(dat.beamSweep.beamwidth,dat.beamSweep.motion,blue,[Motion only]),
  curve(dat.beamSweep.beamwidth,dat.beamSweep.coupled,ink,[Coupled],dash:"dotted"),
))
#let phase()=axes(-180,180,0,0.27,(-180,-90,0,90,180),(0,0.05,0.1,0.15,0.2,0.25),[Pitch forcing phase offset ($degree$)],[Fraction],(
  curve(dat.phaseSweep.offsetDeg,dat.phaseSweep.coupled,blue,[Joint power availability]),
  curve(dat.phaseSweep.offsetDeg,dat.phaseSweep.independentProduct,orange,[Marginal product],dash:"dashed"),
),height:50)
#let mapping()=axes(0,8,0,0.26,(0,2,4,6,8),(0,0.05,0.1,0.15,0.2,0.25),[Time (s)],[$E_h$ (m)],(
  curve(dat.trace.t,dat.trace.midpointError,blue,[Midpoint position error]),
),height:43)
