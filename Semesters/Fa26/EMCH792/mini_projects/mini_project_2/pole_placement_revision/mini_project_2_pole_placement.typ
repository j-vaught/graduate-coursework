#import "@preview/lilaq:0.6.0" as lq
#let verified = sys.inputs.at("draft", default: "false") != "true"
#let r = json(if verified { "pole_results.json" } else { "pole_design.json" })
#let f(x, digits: 2) = str(calc.round(x, digits: digits))
#let palette = (rgb("#3F90DA"), rgb("#FFA90E"), rgb("#BD1F01"), rgb("#832DB6"))
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
#let traces(runs, field, ylabel, title, xmax: 30, legend: false, degrees: false) = {
  set text(size: 8pt)
  lq.diagram(width: 2.6in, height: 0% + 1.05in, title: title,
    xlabel: [Time (s)], ylabel: ylabel, xlim: (0,xmax),
    xaxis: (ticks: if xmax == 30 { (0,10,20,30) } else { (0,2,4,6,8) }),
    legend: if legend { (radius: 0pt, position: top + right) } else { none },
    ..runs.enumerate().map(pair => {
      let (i,run) = pair
      let idx = run.time_s.enumerate().filter(p => p.last() <= xmax).map(p => p.first())
      lq.plot(idx.map(j => run.time_s.at(j)),idx.map(j => run.at(field).at(j)),
        label: [#str(run.label_value)#if degrees { sym.degree } else { [ N] }],
        mark: none, color: palette.at(i), stroke: (thickness: 1pt,
          dash: if run.metrics.balanced { "solid" } else { "dashed" }))
    }))
}
#align(center)[
  #text(size: 17pt, weight: "bold")[Pole-Placement Control of an Inverted Pendulum]
]
#v(0.3em)

#if not verified [#align(center)[#text(size: 9pt)[Draft. Simulation results pending MATLAB verification.]]]

= OBJECTIVE.

Design a state-feedback controller that returns a perturbed pendulum to upright and maintains balance under random cart forces, using the nonlinear Simulink model from Project 1.

= METHODOLOGY.

We retain the aligned Simulink plant, its frictionless cart, rigid massless rod, point pendulum mass, and pivot damping. The cart mass is 2 kg, pendulum mass is 0.5 kg, rod length is 1 m, pivot damping is 0.01 N m s/rad, and gravity is 9.81 m/s². Here $x$ is cart position and $theta$ is angle from upright. Near upright, $sin(theta) approx theta$, $cos(theta) approx 1$, and the centrifugal term $sin(theta) dot(theta)^2$ has no first-order contribution. With $z=(x,dot(x),theta,dot(theta))^T$, the linearized model is
$ dot(z)=A z+B F, quad
 A=mat(0,1,0,0;0,0,-2.4525,0.005;0,0,0,1;0,0,12.2625,-0.025), quad
 B=mat(0;0.5;0;-0.5). $
The controllability matrix $cal(C)=[B,A B,A^2 B,A^3 B]$ has rank four. Therefore, all four closed-loop poles can be assigned through state feedback.

We choose poles $p=(-1+i,-1-i,-3,-4)$ s⁻¹. The dominant pair has damping ratio $1/sqrt(2)=0.707$ and an exponential envelope $e^(-t)$, giving an approximate 2% settling envelope of 4 s. The two remaining poles decay three and four times faster. These choices give a moderately damped response without demanding arbitrarily fast actuation. They describe the local, unlimited linear model; saturation and nonlinear motion are checked by simulation.

The desired characteristic polynomial is $phi(s)=(s^2+2s+2)(s+3)(s+4)$. We calculate the gain directly using Ackermann's formula,
$ K=mat(0,0,0,1) cal(C)^(-1) phi(A), quad u=-K z. $
This gives $K=(#f(r.design.K.at(0),digits:4),#f(r.design.K.at(1),digits:4),#f(r.design.K.at(2),digits:4),#f(r.design.K.at(3),digits:4))$. The accompanying MATLAB script checks that the eigenvalues of $A-B K$ match the selected poles and compares the gain with `place` @MathWorks2026PolePlacement. The script applies this gain to a copy of the existing Simulink diagram without changing its layout. The actuator clips $u$ to $plus.minus 10$ N, and the external disturbance $d$ is added afterward, giving $F="sat"(-K z)+d$.

The test script runs 30 s nonlinear tests from 5, 10, 20, and 30#sym.degree releases, followed by tests from upright with random forces bounded by $plus.minus 2.5$, 5, 7.5, and 10 N. Independent uniform draws are held for 0.1 s; seed 79202 supplies the same sequence at each bound. The variable-step solver uses a maximum step of 0.01 s. Analysis uses 0.02 s samples. A run loses balance when $abs(theta)>=90 degree$; failed traces stop there. Appendix A shows the retained diagrams, and Appendix B gives essential implementation code.

#pagebreak()
#if not verified [
= RESULTS.

The pole-placement tests are implemented in `run_pole_revision.m`, but MATLAB has not completed startup on this machine. Numerical results and response figures remain pending verification. The test script will populate this section after it runs successfully.

The required tests are recovery from a 5#sym.degree release and response to a bounded random cart force from upright. Additional releases and force bounds will establish where actuator saturation and nonlinear motion prevent recovery. The comparison will report angle, applied force, cart travel, and settling behavior.

The pole-placement gain in the preceding section has been calculated independently with exact rational arithmetic. This verifies the characteristic polynomial of $A-B K$; nonlinear performance still requires the saved Simulink model to run. The model copy currently retains its original gain until the MATLAB runner completes the update.
] else {
  let release = r.releases.first().metrics
  let random = r.disturbances.first().metrics
  [
= RESULTS.

For the 5#sym.degree release, the nonlinear model settles within $plus.minus 1 degree$ and $plus.minus 0.05$ m after #f(release.settling_time_s) s and stays there through 30 s. Peak cart travel is #f(release.peak_cart_m) m, and peak applied force is #f(release.peak_applied_N) N. Figure 1 shows how increasing the release angle changes recovery and actuator use. Saturation limits the corrective force even though the unlimited linear poles remain stable.

#figure(grid(columns: (1fr,1fr), gutter: 10pt,
  traces(r.releases,"theta_deg",[Angle (deg)],[(a) Pendulum angle],xmax:8,legend:true,degrees:true),
  traces(r.releases,"u_N",[Applied force (N)],[(b) Actuator force],xmax:8,degrees:true)),
  caption: [Nonlinear release tests, showing the first 8 s. Dashed traces lose balance and end at the first sampled 90° crossing. The force is clipped to ±10 N.])

#let recovered = r.releases.filter(run => run.metrics.recovered).map(run => str(run.label_value))
#let failed = r.releases.filter(run => not run.metrics.balanced).map(run => str(run.label_value))
The tested releases that recover are #recovered.join(", ")#sym.degree. #if failed.len() > 0 [The #failed.join(", ")#sym.degree cases lose balance.] These results establish a tested operating range for the chosen gain and force limit. They do not follow from pole locations alone, because the controller was designed from a local linearization.

The random-force tests in Figure 2 evaluate a different demand. Instead of removing one initial displacement, the controller must continually oppose an external force. At the 2.5 N bound, angle RMS is #f(random.angle_rms_deg)#sym.degree and peak angle is #f(random.peak_angle_deg)#sym.degree over 30 s. Table 1 summarizes whether each input maintains balance.

#figure(grid(columns: (1fr,1fr), gutter: 10pt,
  traces(r.disturbances,"theta_deg",[Angle (deg)],[(a) Pendulum angle],legend:true),
  traces(r.disturbances,"u_N",[Applied force (N)],[(b) Actuator force])),
  caption: [Nonlinear random-force tests over 30 s. Bounds label the external disturbance; panel (b) shows the separate actuator force. Dashed traces lose balance.])

#figure(table(columns: (1fr,1fr,1fr,1fr), align: center, stroke: none, inset: 3pt,
  table.hline(stroke: 0.8pt),table.header([Force bound (N)],[Balanced],[Angle RMS (deg)],[Peak cart travel (m)]),table.hline(stroke: 0.5pt),
  ..r.disturbances.map(run => ([#str(run.label_value)],[#if run.metrics.balanced [Yes] else [No]],
    [#if run.metrics.balanced { f(run.metrics.angle_rms_deg) } else { [n/a] }],[#f(run.metrics.peak_cart_m)])).flatten(),
  table.hline(stroke: 0.8pt)),caption: [Random-force outcomes. RMS uses the full 30 s for balanced runs; failed-run travel stops at the first sampled 90° crossing.])


= DISCUSSION.

The controller meets the near-upright recovery objective with a finite actuator. Larger perturbations and sustained random forcing can exhaust that force margin. Cart travel also matters, since the model has no physical end stops. Random-force outcomes refer to this recorded sequence; the bounds define amplitude, not a guaranteed disturbance-rejection limit. The report therefore separates local pole stability from the nonlinear, force-limited performance observed in these tests.

]
}

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

The existing Project 2 layout is retained. The runner applies the gain calculated in Appendix B; the actuator and disturbance connections are unchanged.

#figure(image("controlled_model_diagram.png",width:100%),caption:[Retained feedback loop. The external disturbance is added after the actuator limit.])

The nonlinear plant integrates angular and cart accelerations. The State order block displays $(theta,dot(theta),dot(x),x)$ and outputs $(x,dot(x),theta,dot(theta))$ for feedback.

#figure(image("nonlinear_plant_diagram.png",width:100%),caption:[Retained nonlinear plant and four integrators from Project 1.])

#pagebreak()
= Appendix B. Essential MATLAB code.

The first function calculates the pole-placement gain for the state order used by the model. The nonlinear acceleration function below is embedded in the Simulink plant. Experiment automation remains in the accompanying `run_pole_revision.m` file.

#raw(read("design_pole_controller.m"),lang:"matlab",block:true)

#raw(read("controlled_accelerations.m"),lang:"matlab",block:true)

To run the two required tests directly, use a 5#sym.degree release without disturbance, then start upright with the held 2.5 N disturbance. The runner assigns the input data to the model workspace to make the updated model independent of external scripts.

```matlab
model = 'inverted_pendulum_controlled';
load_system(model);
[K,~,~,~] = design_pole_controller();
set_param([model '/State feedback'],'Gain',mat2str(-K,17));
w = get_param(model,'ModelWorkspace');
assignin(w,'disturbance_signal',[0 0;30.1 0]);
set_param([model '/Nonlinear plant/Angle'],'InitialCondition','5*pi/180');
release = sim(model);
rng(79202,'twister'); t = (0:0.1:30.1)';
assignin(w,'disturbance_signal',[t 2.5*(2*rand(size(t))-1)]);
set_param([model '/Nonlinear plant/Angle'],'InitialCondition','0');
random_force = sim(model);
```

= References.
#bibliography("references.bib",title:none,style:"ieee")
