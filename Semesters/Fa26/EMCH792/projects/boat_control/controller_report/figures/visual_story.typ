#import "../../simulator_report/style.typ": *
#let open = json("../data/open_loop.json")
#let closed = json("../data/traces.json")
#let names = ("PID", "LQR + integral", "Pole placement + integral")
#let methods = ("pid", "lqr", "pole_placement")
#let heading-arrow = (end: "stealth", fill: ink, stroke: ink)
#let motion-arrow = (end: "stealth", fill: teal, stroke: teal)
#let chart(title, xlabel, ylabel, series, xlim: auto, ylim: auto, height: 2.35in,
  width:100%, legend:top+right, aspect-ratio:none, xticks:auto, yticks:auto) = {
  set text(font:"Times New Roman",size:9pt)
  lq.diagram(width:width,height:height,title:title,xlabel:xlabel,ylabel:ylabel,
    xlim:xlim,ylim:ylim,aspect-ratio:aspect-ratio,xaxis:(ticks:xticks),yaxis:(ticks:yticks),
    grid:(stroke:0.3pt+luma(83%)),legend:(radius:0pt,fill:white,position:legend),
    ..series.enumerate().map(pair=>{
      let s=pair.last()
      lq.plot(s.x,s.y,label:s.label,mark:none,step:s.at("step",default:none),
        color:s.at("color",default:line-colors.at(calc.rem(pair.first(),line-colors.len()))),
        stroke:(thickness:1.15pt,dash:s.at("dash",default:"solid")))
    }))
}
#let boat(p, angle, size: 1) = {
  import cetz.draw: line
  let c = calc.cos(angle)
  let s = calc.sin(angle)
  let world(q) = (p.at(0)+size*(c*q.at(0)-s*q.at(1)), p.at(1)+size*(s*q.at(0)+c*q.at(1)))
  for y in (-0.375, 0.375) {
    let points = ((-0.6,y - 0.09),(0.6,y - 0.09),(0.6,y+0.09),(-0.6,y+0.09),(-0.6,y - 0.09)).map(world)
    line(..points, fill: pale, stroke: 1pt + ink)
  }
  for x in (-0.4, 0.4) { line(world((x,-0.3)),world((x,0.3)),stroke: 1pt + ink) }
}
#let objective = cetz.canvas(length: 0.95cm, {
  import cetz.draw: line, content, rect
  rect((-0.2,-0.25),(12,0.25),fill:pale,stroke:none)
  line((-0.2,0),(12,0),stroke:1.5pt+teal)
  content((8.2,-0.85),[Desired route. $N = 0$],anchor:"north")
  line((0,0),(0,2),stroke:(paint:slate,dash:"dashed"))
  line((1.5,0),(1.5,2),mark:(start:"stealth",end:"stealth",fill:ink,stroke:ink))
  content((1.8,1),[2 m line error],anchor:"west")
  boat((0,2),0.12rad)
  line((0.6,2.07),(2.5,2.30),stroke:1pt+ink,mark:heading-arrow)
  content((0,3.1),[Start. Slightly pointed north of east],anchor:"west")
  boat((8.2,0),0rad)
  line((8.8,0),(10.7,0),stroke:1pt+teal,mark:motion-arrow)
  content((8,1.1),[Goal. Recover the route and continue],anchor:"center")
  line((-1,-0.4),(-1,3.4),mark:heading-arrow)
  content((-1,3.65),[North],anchor:"south")
  line((-0.2,-1.7),(3,-1.7),mark:heading-arrow)
  content((3.2,-1.7),[East],anchor:"west")
})
#let nominal = {
  let series = (
    (x:(0,40), y:(0,0), label:[Target line], dash:"dashed", color:black),
    ..("nominal_on_line","nominal_offset").enumerate().map(pair => {
      let h = open.traces.at(pair.last()).history
      (x:h.map(r=>r.at(1)), y:h.map(r=>r.at(2)),
       label:if pair.first()==0 {[Aligned start]} else {[Displaced start]}, dash:if pair.first()==0 {"solid"} else {"dashed"})
    })
  )
  chart([Fixed equal thrust, calm water and matched motors], [East position (m)], [North position (m)],series,
    xlim:(-1,42),ylim:(-2,8),height:auto,aspect-ratio:1.0)
}
#let full_paths = {
  let h = open.traces.full_wind5.history
  let series = (
    (x:(-2,42), y:(0,0), label:[Target line], dash:"dashed", color:black),
    (x:h.map(r=>r.at(1)), y:h.map(r=>r.at(2)), label:[Open loop], color:line-colors.at(0)),
    ..methods.enumerate().map(pair => {
      let h=closed.full_wind5.at(pair.last()).history
      (x:h.map(r=>r.at(1)),y:h.map(r=>r.at(2)),label:names.at(pair.first()),
       color:line-colors.at(pair.first()+1), dash:("solid","dashed","dash-dotted").at(pair.first()))
    })
  )
  chart([Actual paths. Full model with 5 m/s northward wind], [East position (m)], [North position (m)], series,
    xlim:(-2,42),ylim:(-12,6),height:auto,aspect-ratio:1.0)
}
#let error(case, column, ylabel, offset:0) = {
  let h=open.traces.at(case).history
  let series=((x:h.map(r=>r.at(0)),y:h.map(r=>r.at(column) - offset),label:[Open loop]),)
  series += methods.enumerate().map(pair => {
    let h=closed.at(case).at(pair.last()).history
    (x:h.map(r=>r.at(0)),y:h.map(r=>r.at(column) - offset),label:names.at(pair.first()),
      dash:("solid","dashed","dash-dotted").at(pair.first()))
  })
  chart([Full boat model, 5 m/s northward wind], [Time (s)],ylabel,series,height:2.15in,xlim:(0,40))
}
#let errors = {
  error("full_wind5",2,[Signed distance from target line (m)])
  v(0.12in)
  error("full_wind5",4,[Forward speed error (m/s)],offset:1)
}
#let commands = {
  let pulse=open.runs.first().pwm_each_us
  let hs=closed.full_wind5.lqr.history
  chart([Port and starboard commands], [Time (s)], [Applied PWM (microseconds)], (
    (x:(0,40),y:(pulse,pulse),label:[Open loop. Both motors],dash:"dashed"),
    (x:hs.map(r=>r.at(0)),y:hs.map(r=>r.at(9)),label:[LQR. Port],step:end),
    (x:hs.map(r=>r.at(0)),y:hs.map(r=>r.at(10)),label:[LQR. Starboard],step:end)
  ),height:2.2in,xlim:(0,40),yticks:range(1100,1901,step:200).map(x=>(x,str(x))))
}
#let crab = {
  let h=closed.full_wind10.lqr.history
  let row=h.find(r=>calc.abs(r.at(0) - 20) < 0.00001)
  let psi=row.at(3)
  let u=row.at(4)
  let v=row.at(5)
  let cs=calc.cos(psi*1rad)
  let sn=calc.sin(psi*1rad)
  let ve=cs*u - sn*v
  let vn=sn*u+cs*v
  cetz.canvas(length:1cm, {
    import cetz.draw: line,content
    line((-0.5,0),(11.5,0),stroke:(paint:slate,dash:"dashed"))
    content((10,-0.3),[East-going target line],anchor:"north")
    boat((3,0),psi*1rad,size:2.3)
    line((3,0),(3+3.3*cs,3.3*sn),stroke:1.25pt+ink,mark:heading-arrow)
    content((4,-2.4),[Bow points into the wind],anchor:"north")
    line((3,0),(3+6*ve,6*vn),stroke:1.7pt+teal,mark:motion-arrow)
    content((8,0.55),[Direction of travel],anchor:"south")
    line((0,-2),(0,1.3),stroke:1pt+ochre,mark:(end:"stealth",fill:ochre,stroke:ochre))
    content((0,1.7),[Wind toward north],anchor:"south")
    content((6,2.4),[LQR. 10 m/s wind, $t = 20$ s],anchor:"south")
  })
}
#let ladder = {
  let cases=("00_linear","01_hull","02_m200","03_motor","04_timing","05_sensors","06_disturbances","07_uncertainty")
  let s=json("../data/summary.json")
  let yopen=cases.map(c=>open.aggregate.find(r=>r.case=="ladder_"+c).metrics.cross_rms_m.mean)
  let series=((x:range(8),y:yopen,label:[Open loop]),)
  series += methods.enumerate().map(pair=>(x:range(8),
    y:cases.map(c=>s.aggregate.find(r=>r.case=="ladder_"+c and r.method==pair.last()).metrics.cross_rms_m.mean),
    label:names.at(pair.first()),dash:("solid","dashed","dash-dotted").at(pair.first())))
  chart([Add simulator features while keeping each policy fixed], [Stage index (0-7)], [Whole-run line RMS (m)],series,height:1.9in,ylim:(0,auto),legend:top+left,xticks:range(8))
}
