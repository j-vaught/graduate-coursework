#import "@preview/lilaq:0.6.0" as lq
#let r = json("project4_results.json")
#let a = r.comparison.lqr
#let b = r.comparison.mpc
#let f(x, digits: 2) = str(calc.round(x, digits: digits))
#let colors = (rgb("#3F90DA"), rgb("#FFA90E"))
#set page(paper: "us-letter", margin: (top: 1in, bottom: 1in, x: 1in),
  numbering: "1", number-align: center + bottom,
  header: [#text(size: 9pt)[J.C. Vaught] #h(1fr) #text(size: 9pt)[EMCH 792]])
#set text(font: ("Times New Roman", "New Computer Modern", "Latin Modern Roman"), size: 11pt, lang: "en", region: "US")
#set par(justify: true, leading: 0.55em, first-line-indent: (amount: 1em, all: true))
#set heading(numbering: none)
#show heading.where(level: 1): it => block(above: 0.6em, below: 0.3em)[#text(size: 11pt, weight: "bold")[#it.body]]
#show figure.caption: set text(size: 9pt)
#set figure(gap: 4pt)
#let response(field,ylabel,title,legend:false) = {
  set text(size:8pt)
  lq.diagram(width:2.65in,height:1.45in,title:title,
    xlabel:[Time (s)],ylabel:ylabel,xlim:(0,8),
    xaxis:(ticks:(0,2,4,6,8)),
    legend:if legend {(radius:0pt,position:top+right,fill:white)} else {none},
    ..(a,b).enumerate().map(pair => {
      let (i,run)=pair
      let idx=run.time_s.enumerate().filter(p => p.last()<=8).map(p => p.first())
      lq.plot(idx.map(j => run.time_s.at(j)),idx.map(j => run.at(field).at(j)),
        mark:none,label:([LQR],[MPC]).at(i),color:colors.at(i),stroke:(thickness:1pt))
    }))
}
#align(center)[#text(size:17pt,weight:"bold")[Model Predictive Control of an Inverted Pendulum]]
#v(0.3em)

= OBJECTIVE.

Design a model predictive controller (MPC) for the inverted pendulum with a bounded actuator force and compare its nonlinear response with the linear quadratic regulator (LQR) from Mini Project 3.

= METHODOLOGY.

The nonlinear Simulink plant from Mini Project 3 is retained with cart mass 2 kg, pendulum mass 0.5 kg, rod length 1 m, pivot damping 0.01 N m s/rad, and gravity 9.81 m/s². The state vector $z=(x,dot(x),theta,dot(theta))^T$ contains cart position, cart velocity, pendulum angle from upright, and angular velocity. The upright linearization $dot(z)=A z+B u$ is the MPC prediction model. The simulation supplies the four plant states directly to the controller.

The LQR uses continuous state feedback. The Simulink MPC Controller block updates every #f(r.settings.Ts_s) s. Its prediction horizon is #r.settings.prediction_horizon_steps steps (#f(r.settings.prediction_horizon_s) s), and its control horizon is #r.settings.control_horizon_steps steps. The optimizer penalizes state deviations, force, and force changes. The output weights are $(2, sqrt(2), sqrt(300), sqrt(10))$; the force and force-rate weights are #f(r.design.force_weight,digits:3) and #f(r.design.force_rate_weight), respectively. Both controllers use an applied force limit of $plus.minus #r.settings.force_limit_N$ N. MPC includes this limit in its optimization, whereas the LQR command is clipped by the actuator.

Both cases start at rest with $theta=5 degree$, zero cart displacement, and zero disturbance. Each nonlinear simulation lasts 30 s. Settling requires $abs(theta)<=1 degree$ and $abs(x)<=0.05$ m thereafter. Force effort is $E_u=integral_0^(30) u(t)^2 dif t$; MPC effort uses the held input intervals. Appendix A provides the controller construction and comparison code.

= RESULTS AND DISCUSSION.

Figure 1 compares the responses. The LQR and MPC joint settling times are #f(a.metrics.settling_time_s) and #f(b.metrics.settling_time_s) s, respectively. Neither controller reaches the $plus.minus #r.settings.force_limit_N$ N limit in this test.

#figure([
  #show:lq.layout
  #grid(columns:(1fr,1fr),gutter:10pt,
    response("theta_deg",[Angle (deg)],[(a) Pendulum angle],legend:true),
    response("u_N",[Applied force (N)],[(b) Actuator force]))
],caption:[Matched nonlinear response from a 5° release. The first 8 s are shown.])

#figure(table(columns:(1fr,1fr,1fr),stroke:none,align:center,inset:2pt,
  table.hline(stroke:0.8pt),
  table.header([Measure],[LQR],[MPC]),table.hline(stroke:0.5pt),
  [Joint settling (s)],[#f(a.metrics.settling_time_s)],[#f(b.metrics.settling_time_s)],
  [Peak cart travel (m)],[#f(a.metrics.peak_cart_m)],[#f(b.metrics.peak_cart_m)],
  [Peak force (N)],[#f(a.metrics.peak_force_N)],[#f(b.metrics.peak_force_N)],
  [Force effort (N² s)],[#f(a.metrics.effort_N2_s)],[#f(b.metrics.effort_N2_s)],
  table.hline(stroke:0.8pt)),caption:[Comparison over the full 30 s simulation.])

The #f(r.settings.prediction_horizon_s) s prediction horizon was selected from three tests with the same weights. A 1 s horizon did not meet the recovery criterion within 30 s; a 1.75 s horizon settled in #f(r.horizon_study.at(1).settling_time_s) s. The selected horizon settled in #f(b.metrics.settling_time_s) s and reduced peak cart travel. The $plus.minus #r.settings.force_limit_N$ N limit matches Project 3. MPC reduces force effort while increasing peak cart travel relative to LQR. These differences reflect the respective weights and update rates; the force constraint remains inactive.

#pagebreak()
#set text(size: 9pt)
#show heading.where(level: 1): it => block(above: 0.8em, below: 0.5em)[#text(size: 13pt, weight: "bold")[#it.body]]
#show raw.where(block: true): it => block(width: 100%, fill: rgb("#ECECEC"), stroke: 0.5pt + rgb("#A2A2A2"), inset: 6pt)[#set text(font: "DejaVu Sans Mono", size: 7pt); #it]
= Appendix A. MATLAB and Simulink implementation.

The Simulink model uses the nonlinear plant and state ordering from Mini Project 3. The following code constructs the MPC object, inserts its controller block into the copied model, and runs the matched comparisons.

#figure(image("mpc_model_diagram.png",width:100%),caption:[Simulink MPC implementation. The disturbance is zero for the reported tests.])

#raw(read("build_project4.m"), lang:"matlab", block:true)

The upright linearization and LQR gain used by the comparison are calculated as follows.

#raw(read("design_lqr_controller.m"), lang:"matlab", block:true)

The validation script checks the saved model and compares the three prediction horizons.

#raw(read("validate_project4.m"), lang:"matlab", block:true)

The layout functions arrange and export the model and verify the saved configuration.

#raw(read("format_project4_layout.m"), lang:"matlab", block:true)

#raw(read("format_and_verify.m"), lang:"matlab", block:true)
