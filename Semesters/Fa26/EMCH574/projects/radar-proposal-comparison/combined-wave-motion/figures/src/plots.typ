#import "@preview/lilaq:0.6.0" as lq
#let dat=json("../../data/illustrative.json")
#let curve(x,y,label)=lq.plot(x,y,label:label,mark:none)
#let axes(xmin,xmax,ymin,ymax,xticks,yticks,xlabel,ylabel,curves,height:43,legend-position:none)={
  set text(font:"Latin Modern Roman",size:9pt,fill:black)
  show math.equation: set text(font:"Latin Modern Math")
  lq.diagram(
    width:145mm,height:height*1mm,
    xlim:(xmin,xmax),ylim:(ymin,ymax),
    xlabel:xlabel,ylabel:ylabel,
    xaxis:(ticks:xticks,subticks:none),
    yaxis:(ticks:yticks,subticks:none),
    legend:if legend-position == none {(position:bottom+right,dy:-100%-4pt,radius:0pt)} else {(position:legend-position,pad:4pt,radius:0pt)},
    ..curves,
  )
}
#let motion()=axes(0,8,-7,7,(0,2,4,6,8),(-6,-3,0,3,6),[Time (s)],[Angle ($degree$)],(
  curve(dat.trace.t,dat.trace.pitch,[Pitch]),
  curve(dat.trace.t,dat.trace.roll,[Roll]),
),height:35)
#let power()=axes(0,8,-40,25,(0,2,4,6,8),(-40,-20,0,20),[Time (s)],[$gamma$ (dB)],(
  curve(dat.trace.t,dat.trace.motionDb,[Motion only]),
  curve(dat.trace.t,dat.trace.waveDb,[Propagation only]),
  curve(dat.trace.t,dat.trace.coupledDb,[Coupled]),
  curve((0,8),(10,10),[Power gate]),
))
#let amplitude()=axes(0,3,0,1.05,(0,0.5,1,1.5,2,2.5,3),(0,0.25,0.5,0.75,1),[Static pitch deflection $M_0/k$ ($degree$)],[Fraction],(
  curve(dat.amplitudeSweep.staticPitch,dat.amplitudeSweep.motion,[Motion only]),
  curve(dat.amplitudeSweep.staticPitch,dat.amplitudeSweep.wave,[Propagation only]),
  curve(dat.amplitudeSweep.staticPitch,dat.amplitudeSweep.coupled,[Coupled]),
))
#let beam()=axes(2,14,0,1.05,(2,4,6,8,10,12,14),(0,0.25,0.5,0.75,1),[Full vertical half-power beamwidth ($degree$)],[Fraction],(
  curve(dat.beamSweep.beamwidth,dat.beamSweep.motion,[Motion only]),
  curve(dat.beamSweep.beamwidth,dat.beamSweep.coupled,[Coupled]),
))
#let phase()=axes(-180,180,0,0.27,(-180,-90,0,90,180),(0,0.05,0.1,0.15,0.2,0.25),[Pitch forcing phase offset ($degree$)],[Fraction],(
  curve(dat.phaseSweep.offsetDeg,dat.phaseSweep.coupled,[Joint power availability]),
  curve(dat.phaseSweep.offsetDeg,dat.phaseSweep.independentProduct,[Marginal product]),
),height:43)
#let mapping()=axes(0,8,0,0.26,(0,2,4,6,8),(0,0.05,0.1,0.15,0.2,0.25),[Time (s)],[$E_h$ (m)],(
  curve(dat.trace.t,dat.trace.midpointError,[Midpoint position error]),
))
