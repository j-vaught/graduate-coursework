#import "@preview/lilaq:0.6.0" as lq
#let r = json("project3_results.json")
#let nominal = r.comparisons.first()
#let f(x, digits: 2) = str(calc.round(x, digits: digits))
#let colors = (rgb("#3F90DA"), rgb("#FFA90E"), rgb("#BD1F01"), rgb("#832DB6"))
#set page(paper: "us-letter", margin: (top: 1in, bottom: 1in, x: 1in),
  numbering: "1", number-align: center + bottom,
  header: [#text(size: 9pt)[J.C. Vaught] #h(1fr) #text(size: 9pt)[EMCH 792]])
#set text(font: ("Times New Roman", "New Computer Modern", "Latin Modern Roman"),
  size: 11pt, lang: "en", region: "US")
#set par(justify: true, leading: 0.55em, first-line-indent: (amount: 1em, all: true))
#set heading(numbering: none)
#show heading.where(level: 1): it => block(above: 0.6em, below: 0.3em)[
  #text(size: 11pt, weight: "bold")[#it.body]
]
#show heading.where(level: 2): it => block(above: 0.5em, below: 0.25em)[
  #text(size: 10.5pt, weight: "bold")[#it.body]
]
#show figure.caption: set text(size: 9pt)
#set figure(gap: 4pt)
#show figure.where(kind: table): set figure.caption(position: top)

#show raw.where(block: true): it => block(width: 100%, fill: rgb("#ECECEC"),
  stroke: 0.5pt + rgb("#A2A2A2"), inset: 6pt)[
  #set text(font: "DejaVu Sans Mono", size: 7.3pt)
  #it
]
#let response(runs,field,ylabel,title,labels,legend:false,height:1.5in) = {
  set text(size:8pt)
  lq.diagram(width:2.6in,height:0%+height,title:title,
    xlabel:[Time (s)],ylabel:ylabel,xlim:(0,8),
    xaxis:(ticks:(0,2,4,6,8)),
    legend:if legend {(radius:0pt,position:top+right,fill:white)} else {none},
    ..runs.enumerate().map(pair => {
      let (i,run)=pair
      let idx=run.time_s.enumerate().filter(p => p.last()<=8).map(p => p.first())
      lq.plot(idx.map(j => run.time_s.at(j)),idx.map(j => run.at(field).at(j)),
        mark:none,label:labels.at(i),color:colors.at(i),stroke:(thickness:1pt))
    }))
}
#align(center)[
  #text(size:17pt,weight:"bold")[LQR Control of an Inverted Pendulum on a Cart]
]
#v(0.3em)

= OBJECTIVE.

Design a linear-quadratic regulator (LQR) that stabilizes the nonlinear inverted pendulum and compare its response and control force with the pole-placement controller from Project 2.

= METHODOLOGY.

We reuse Project 2's nonlinear Simulink plant, its upright linearization $dot(z)=A z+B u$, and state order $z=(x,dot(x),theta,dot(theta))^T$. Here $x$ is cart position and $theta$ is angle from upright in radians. The cart mass is 2 kg, pendulum mass is 0.5 kg, rod length is 1 m, pivot damping is 0.01 N m s/rad, and gravity is 9.81 m/s². Appendix A retains the aligned system diagrams.

Pole placement assigns the closed-loop poles directly. LQR instead chooses feedback to minimize the infinite-horizon linear-model cost,
$ J=integral_0^infinity (z^T Q z+u^T R u) dif t, quad Q="diag"(4,2,300,10), quad R=0.5. $
The four state penalties act on cart position, cart velocity, angle, and angular velocity. The input penalty discourages force. We select these weights to balance small angular departures against cart motion and actuator effort. For example, a 0.5 m cart displacement and a 3.31#sym.degree angular displacement each contribute one unit to the instantaneous state cost. These are tuning scales, with angles evaluated in radians.

MATLAB solves the algebraic Riccati equation and returns $u=-K z$ @MathWorks2026LQR. The baseline gain is $K=(#f(r.design.K.at(0),digits:4),#f(r.design.K.at(1),digits:4),#f(r.design.K.at(2),digits:4),#f(r.design.K.at(3),digits:4))$, and all poles of $A-B K$ have negative real parts. This optimality applies to the unlimited linear model. We test its nonlinear implementation with the same $plus.minus 10$ N actuator limit as Project 2.

Both controllers start from rest at 5, 10, and 20#sym.degree, with no external disturbance. Runs last 30 s, use a maximum solver step of 0.01 s, and are sampled every 0.02 s. Settling requires $abs(theta)<=1 degree$ and $abs(x)<=0.05$ m thereafter. A 90#sym.degree crossing marks failure. We also vary only the angle penalty over 100, 300, and 900, then only the force penalty over 0.1, 0.5, and 2, using the same nonlinear 5#sym.degree release.

= RESULTS.

Figure 1 compares the required 5#sym.degree release. LQR settles in #f(nominal.lqr.metrics.settling_time_s) s, compared with #f(nominal.pole.metrics.settling_time_s) s for pole placement. Their peak applied forces are #f(nominal.lqr.metrics.peak_force_N) and #f(nominal.pole.metrics.peak_force_N) N, respectively. Over 30 s, LQR uses #f(100*(1-nominal.lqr.metrics.effort_N2_s/nominal.pole.metrics.effort_N2_s),digits:1)% less integrated force effort.

#figure([
  #show:lq.layout
  #grid(columns:(1fr,1fr),gutter:10pt,
    response((nominal.pole,nominal.lqr),"theta_deg",[Angle (deg)],[(a) Pendulum angle],([Pole placement],[LQR]),legend:true),
    response((nominal.pole,nominal.lqr),"u_N",[Applied force (N)],[(b) Actuator force],([Pole placement],[LQR])))
],caption:[Matched nonlinear 5° release, showing the first 8 s. Both controllers use the same plant and ±10 N actuator limit.])

#pagebreak()

The longer and larger-release comparisons in Table 1 quantify cart motion and effort as well as settling. Force effort is $E_u=integral_0^(30) u(t)^2 dif t$. Metrics use 30 s for recovered runs; failed-run travel stops at the first sampled 90#sym.degree crossing.

#figure(table(columns:(0.7fr,1.5fr,1fr,1fr,1fr),stroke:none,align:center,inset:3pt,
  table.hline(stroke:0.8pt),
  table.header([Release (deg)],[Controller],[$t_s$ (s)],[Peak travel (m)],[$E_u$ (N² s)]),
  table.hline(stroke:0.5pt),
  ..r.comparisons.map(case => (case.pole,case.lqr).map(run => (
    [#str(case.angle_deg)],[#run.label],
    [#if run.metrics.recovered {f(run.metrics.settling_time_s)} else {[Failed]}],
    [#f(run.metrics.peak_cart_m)],
    [#if run.metrics.recovered {f(run.metrics.effort_N2_s)} else {[n/a]}]
  )).flatten()).flatten(),
  table.hline(stroke:0.8pt)),caption:[Matched nonlinear release tests. Settling uses joint angle and cart-position bounds. Failed runs have no comparable 30 s effort value.])

At 20#sym.degree, #if r.comparisons.last().lqr.metrics.recovered [LQR recovers in #f(r.comparisons.last().lqr.metrics.settling_time_s) s] else [LQR fails], while pole placement reaches 90#sym.degree at #f(r.comparisons.last().pole.metrics.fall_time_s) s. The LQR run reaches #f(r.comparisons.last().lqr.metrics.peak_cart_m) m of cart travel. This gain therefore tolerates the tested larger release, at the cost of substantial cart travel.

Figure 2 isolates the weighting choices. Each row holds all other weights fixed. Thus, the differences arise from the selected penalty and its interaction with the same nonlinear plant and force limit.

#figure([
  #show:lq.layout
  #grid(columns:(1fr,1fr),gutter:8pt,
    response(r.angle_weights,"theta_deg",[Angle (deg)],[(a) Angle penalty sweep],([$q_theta=100$],[$q_theta=300$],[$q_theta=900$]),legend:true,height:1.4in),
    response(r.angle_weights,"u_N",[Applied force (N)],[(b) Corresponding force],([$q_theta=100$],[$q_theta=300$],[$q_theta=900$]),height:1.4in),
    response(r.force_weights,"theta_deg",[Angle (deg)],[(c) Force penalty sweep],([$R=0.1$],[$R=0.5$],[$R=2$]),legend:true,height:1.4in),
    response(r.force_weights,"u_N",[Applied force (N)],[(d) Corresponding force],([$R=0.1$],[$R=0.5$],[$R=2$]),height:1.4in))
],caption:[Nonlinear weight sweeps from 5°, showing the first 8 s. The angle sweep fixes $R=0.5$; the force sweep fixes $Q="diag"(4,2,300,10)$. The orange trace is the shared baseline.])

= DISCUSSION.

Increasing the angle penalty from 100 to 900 changes peak applied force from #f(r.angle_weights.first().metrics.peak_force_N) to #f(r.angle_weights.last().metrics.peak_force_N) N and peak cart travel from #f(r.angle_weights.first().metrics.peak_cart_m) to #f(r.angle_weights.last().metrics.peak_cart_m) m. Increasing the force penalty from 0.1 to 2 changes force effort from #f(r.force_weights.first().metrics.effort_N2_s) to #f(r.force_weights.last().metrics.effort_N2_s) N² s. The force-penalty change also extends joint settling from #f(r.force_weights.first().metrics.settling_time_s) to #f(r.force_weights.last().metrics.settling_time_s) s. These tradeoffs explain retaining the intermediate baseline. LQR minimizes the stated weighted cost, so it need not give the fastest settling time. The 10 N clipping remains a separate physical limit, and the track model has no end stops.

#pagebreak()
#set page(margin: 1in)
#set text(size: 10.5pt)
#show figure.caption: set text(size: 9.5pt)
#show heading.where(level: 1): it => block(above: 0.8em, below: 0.5em)[
  #text(size: 14pt, weight: "bold")[#it.body]
]
#show heading.where(level: 2): it => block(above: 0.6em, below: 0.4em)[
  #text(size: 12pt, weight: "bold")[#it.body]
]
#set table(stroke: none)
#show table: set par(justify: false, first-line-indent: 0pt)
#show table: set text(hyphenate: false)



= Appendix A. Simulink implementation.

The aligned Project 2 diagram is retained. The feedback block contains the LQR gain from Appendix B. The external disturbance is set to zero for the matched release comparisons.

#figure(image("controlled_model_diagram.png",width:100%),caption:[Retained feedback loop. The external disturbance is added after the actuator limit.])

The nonlinear plant integrates angular and cart accelerations. The State order block displays $(theta,dot(theta),dot(x),x)$ and outputs $(x,dot(x),theta,dot(theta))$ for feedback.

#figure(image("nonlinear_plant_diagram.png",width:100%),caption:[Retained nonlinear plant and four integrators from Project 1.])

#pagebreak()
= Appendix B. Essential MATLAB code.

The first function calculates the LQR gain for the state order used by the model. The nonlinear acceleration function below is embedded in the Simulink plant. Experiment automation remains in the accompanying `run_project3.m` file.

#raw(read("design_lqr_controller.m"),lang:"matlab",block:true)

#raw(read("controlled_accelerations.m"),lang:"matlab",block:true)

To change the weights without rearranging the model, update its gain and run the same 5#sym.degree release. The saved model embeds zero disturbance data.

```matlab
[K,design] = design_lqr_controller(2,0.5,1,0.01,9.81);
model = 'inverted_pendulum_lqr';
load_system(model);
set_param([model '/State feedback'],'Gain',mat2str(-K,17));
set_param([model '/Nonlinear plant/Angle'],'InitialCondition','5*pi/180');
response = sim(model);
```

= References.
#bibliography("references.bib",title:none,style:"ieee")
