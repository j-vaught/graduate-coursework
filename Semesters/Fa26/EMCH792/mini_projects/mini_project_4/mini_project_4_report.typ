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

Both cases start at rest with $theta=5 degree$, zero cart displacement, and zero disturbance. Each nonlinear simulation lasts 30 s. Settling requires $abs(theta)<=1 degree$ and $abs(x)<=0.05$ m thereafter. Force effort is $E_u=integral_0^(30) u(t)^2 dif t$; MPC effort uses the held input intervals. Appendix A shows the Simulink implementation, and Appendix B gives the essential controller setup.

= RESULTS.

Figure 1 compares the responses. The LQR and MPC joint settling times are #f(a.metrics.settling_time_s) and #f(b.metrics.settling_time_s) s, respectively. Neither controller reaches the $plus.minus #r.settings.force_limit_N$ N limit in this test.

#figure([
  #show:lq.layout
  #grid(columns:(1fr,1fr),gutter:10pt,
    response("theta_deg",[Angle (deg)],[(a) Pendulum angle],legend:true),
    response("u_N",[Applied force (N)],[(b) Actuator force]))
],caption:[Matched nonlinear response from a 5° release. The first 8 s are shown.])

#pagebreak()

The full 30 s comparison in Table 1 quantifies cart motion and force effort in addition to settling.

#figure(table(columns:(1fr,1fr,1fr),stroke:none,align:center,inset:2pt,
  table.hline(stroke:0.8pt),
  table.header([Measure],[LQR],[MPC]),table.hline(stroke:0.5pt),
  [Joint settling (s)],[#f(a.metrics.settling_time_s)],[#f(b.metrics.settling_time_s)],
  [Peak cart travel (m)],[#f(a.metrics.peak_cart_m)],[#f(b.metrics.peak_cart_m)],
  [Peak force (N)],[#f(a.metrics.peak_force_N)],[#f(b.metrics.peak_force_N)],
  [Force effort (N² s)],[#f(a.metrics.effort_N2_s)],[#f(b.metrics.effort_N2_s)],
  table.hline(stroke:0.8pt)),caption:[Comparison over the full 30 s simulation.])

The MPC peak force is #f(b.metrics.peak_force_N) N, compared with #f(a.metrics.peak_force_N) N for LQR. Its force effort is #f(b.metrics.effort_N2_s) N² s, compared with #f(a.metrics.effort_N2_s) N² s for LQR. The reduction in force effort accompanies a rise in peak cart travel from #f(a.metrics.peak_cart_m) to #f(b.metrics.peak_cart_m) m.

To select the prediction horizon, we repeat the 5° release using the same controller weights, force limit, and 0.05 s sample time. Table 2 compares the three tested horizons. The 1 s case does not meet the joint recovery criterion within 30 s. Increasing the horizon to 1.75 s reduces peak travel and gives 9.40 s settling. The 2.5 s horizon settles in #f(b.metrics.settling_time_s) s with the least peak travel among these tests.

#figure(table(columns:(1fr,1fr,1fr,1fr),stroke:none,align:center,inset:3pt,
  table.hline(stroke:0.8pt),
  table.header([Horizon (s)],[Joint settling (s)],[Peak travel (m)],[Peak force (N)]),table.hline(stroke:0.5pt),
  ..r.horizon_study.map(h => ([#f(h.seconds)], [#if h.recovered {f(h.settling_time_s)} else [Not recovered]], [#f(h.peak_cart_m)], [#f(h.peak_force_N)])).flatten(),
  table.hline(stroke:0.8pt)),caption:[Prediction-horizon comparison for the same nonlinear 5° release.])

= DISCUSSION.

The #f(r.settings.prediction_horizon_s) s prediction horizon gives the fastest joint settling of the three tested horizons. A longer horizon lets the optimizer account for more of the coupled pendulum and cart motion, and the comparison shows the resulting reduction in cart travel for these choices. We retain the $plus.minus #r.settings.force_limit_N$ N limit to match Project 3. The nominal release uses less than the available force, so this test does not show an active-constraint advantage. The MPC and LQR also use different weights and update rates. Their measured differences therefore reflect the complete controller designs.

#pagebreak()
#set text(size: 10.5pt)
#show heading.where(level: 1): it => block(above: 0.8em, below: 0.5em)[#text(size: 14pt, weight: "bold")[#it.body]]
#show raw.where(block: true): it => block(width: 100%, fill: rgb("#ECECEC"), stroke: 0.5pt + rgb("#A2A2A2"), inset: 6pt)[#set text(font: "DejaVu Sans Mono", size: 8pt); #it]
= Appendix A. Simulink implementation.

The Project 3 nonlinear plant is retained. The MPC block receives the four plant states and supplies the force command to the same actuator limit. The external disturbance is zero for the reported tests.

#figure(image("mpc_model_diagram.png",width:100%),caption:[Simulink MPC implementation using the retained nonlinear plant.])

The nonlinear plant integrates the cart and pendulum accelerations. Its state-order block returns $(x,dot(x),theta,dot(theta))$ to the controller.

#figure(image("nonlinear_plant_diagram.png",width:100%),caption:[Retained nonlinear plant and state ordering from Project 3.])

#pagebreak()
= Appendix B. Essential MATLAB code.

The following excerpt defines the prediction model, horizons, weights, and force constraint used by the Simulink MPC block. The complete model construction and experiment automation remain in the accompanying `build_project4.m` and `validate_project4.m` files.

#let setup = read("build_project4.m").split("Ts=0.05; p=50; m=10;").last().split("source=fullfile(prior,").first()
#raw("[K,d]=design_lqr_controller(2,0.5,1,0.01,9.81);\nTs=0.05; p=50; m=10;" + setup, lang:"matlab", block:true)

The saved model embeds the controller and can be opened and simulated directly. The full comparison and validation scripts reproduce the results and horizon study.

```matlab
model = 'inverted_pendulum_mpc';
load_system(model);
response = sim(model);
```
