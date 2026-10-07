#import "@preview/lilaq:0.6.0" as lq

#let plots = json("plot_data.json")
#let stats = json("metrics.json")
#let model_tests = json("model_comparisons.json")
#let ctrl = json("controller_studies.json")
#let dist = json("disturbance_studies.json")
#let fmt(value, digits: 2) = str(calc.round(value, digits: digits))
#let colors = (rgb("#3F90DA"), rgb("#FFA90E"), rgb("#BD1F01"), rgb("#832DB6"), rgb("#A96B59"), rgb("#717581"))
#let sweep(runs, field, ylabel, limit, panel, height: 1.05in, ylim: auto, yscale: "linear", failed-from: 99, with-legend: false, legend-position: top + right, data-size: none) = {
  set text(size: if height > 2in { 10pt } else { 8pt })
  lq.diagram(
    width: if data-size == none { 100% } else { data-size.first() },
    height: if data-size == none { 0% + height } else { data-size.last() }, title: panel,
    xlabel: [Time (s)], ylabel: ylabel, xlim: limit, ylim: ylim, yscale: yscale,
    xaxis: (ticks: if limit.last() == 30 { (0, 10, 20, 30) }
      else if limit.last() == 10 { (0, 2, 4, 6, 8, 10) }
      else if limit.last() == 6 { (0, 1, 2, 3, 4, 5, 6) }
      else if limit.last() == 3 { (0, 0.5, 1, 1.5, 2, 2.5, 3) }
      else { (0, 0.2, 0.4, 0.6, 0.8, 1) }),
    legend: if with-legend { (radius: 0pt, position: legend-position) } else { none },
    ..runs.enumerate().map(pair => {
      let (i, run) = pair
      let indices = run.response.time_s.enumerate().filter(pair =>
        limit.first() <= pair.last() and pair.last() <= limit.last()).map(pair => pair.first())
      lq.plot(indices.map(index => run.response.time_s.at(index)),
        indices.map(index => run.response.at(field).at(index)), mark: none,
        label: if "initial_angle_deg" in run { [#str(run.initial_angle_deg)#sym.degree] }
          else { [#fmt(run.amplitude_N, digits: 1) N] },
        color: colors.at(i), stroke: (thickness: 1.0pt,
          dash: if i >= failed-from { "dashed" } else { "solid" }))
    }),
  )
}

#let forcing(limit, panel, height: 1.05in, data-size: none, ylim: auto) = {
  set text(size: 8pt)
  lq.diagram(
    width: if data-size == none { 100% } else { data-size.first() },
    height: if data-size == none { 0% + height } else { data-size.last() }, title: panel,
    xlabel: [Time (s)], ylabel: [Disturbance (N)], xlim: limit, ylim: ylim,
    xaxis: (ticks: if limit.last() == 30 { (0, 10, 20, 30) }
      else if limit.last() == 3 { (0, 0.5, 1, 1.5, 2, 2.5, 3) }
      else { (0, 0.2, 0.4, 0.6, 0.8, 1) }),
    legend: none,
    ..plots.force_runs.enumerate().map(pair => {
      let (i, run) = pair
      let indices = plots.disturbance_time_s.enumerate().filter(pair =>
        limit.first() <= pair.last() and pair.last() <= limit.last()).map(pair => pair.first())
      lq.plot(indices.map(index => plots.disturbance_time_s.at(index)),
        indices.map(index => plots.unit_disturbance.at(index) * run.amplitude_N),
        mark: none, color: colors.at(i), step: end,
        stroke: (thickness: 0.9pt, dash: if i == 3 { "dashed" } else { "solid" }))
    }),
  )
}

#let comparison(field, ylabel, panel, height: 1.35in, legend-position: top + left) = {
  set text(size: 9pt)
  lq.diagram(width: 100%, height: 0% + height, title: panel,
    xlabel: [Time (s)], ylabel: ylabel, xlim: (0, 0.5),
    legend: (position: legend-position, radius: 0pt),
    lq.plot(plots.comparison.time_s, plots.comparison.at("nonlinear_" + field),
      mark: none, label: [Nonlinear], color: colors.first(), stroke: (thickness: 1.3pt)),
    lq.plot(plots.comparison.time_s, plots.comparison.at("linear_" + field),
      mark: none, label: [Linear], color: colors.at(1), stroke: (thickness: 1.1pt, dash: "dashed")),
  )
}

#let model-sweep(runs, field, ylabel, panel, unit: [], with-legend: false, legend-position: top + left) = {
  set text(size: 9pt)
  let palette = colors + (rgb("#009E73"),)
  lq.diagram(width: 5.8in, height: 1.1in, title: panel,
    xlabel: [Time (s)], ylabel: ylabel, xlim: (0, 1),
    xaxis: (ticks: (0, 0.2, 0.4, 0.6, 0.8, 1)),
    legend: if with-legend { (position: legend-position, radius: 0pt) } else { none },
    ..runs.enumerate().map(pair => {
      let (i, run) = pair
      lq.plot(run.time_s, run.at("nonlinear_" + field), mark: none,
        label: [#str(run.input_value)#unit], color: palette.at(i), stroke: (thickness: 1pt))
    }),
    ..runs.enumerate().map(pair => {
      let (i, run) = pair
      lq.plot(run.time_s, run.at("linear_" + field), mark: none,
        color: palette.at(i), stroke: (thickness: 1pt, dash: "dashed"))
    }),
  )
}
#let error-value(value, digits: 4) = {
  if value > 0 and value < 0.0001 {
    let exponent = calc.floor(calc.log(value, base: 10))
    let coefficient = fmt(value / calc.pow(10, exponent), digits: 2)
    $#coefficient times 10^(#exponent)$
  } else { [#fmt(value, digits: digits)] }
}
#let model-error-table(runs, input-label, time-dividers: false) = {
  set text(size: 9pt)
  table(columns: (1fr, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr),
    inset: (x: 4pt, y: 4pt),
    align: (x, y) => if y <= 1 { center } else { right },
    table.hline(stroke: 0.8pt),
    table.header(
      table.cell(rowspan: 2)[#input-label],
      table.cell(colspan: 2)[0.1 s], table.cell(colspan: 2)[0.25 s], table.cell(colspan: 2)[0.5 s],
      [$e_x$ (%)], [$e_theta$ (%)], [$e_x$ (%)], [$e_theta$ (%)], [$e_x$ (%)], [$e_theta$ (%)],
    ),
    table.hline(stroke: 0.5pt),
    ..if time-dividers { (table.vline(x: 3, stroke: 0.4pt), table.vline(x: 5, stroke: 0.4pt)) } else { () },
    ..runs.map(run => ([#str(run.input_value)],
      ..range(3).map(i => (error-value(run.x_error_percent.at(i)),
        error-value(run.angle_error_percent.at(i)))).flatten())).flatten(),
    table.hline(stroke: 0.8pt),
  )
}

#let ctrl-panel(runs, field, ylabel, panel, limit: (0, 30), size: (2.6in, 1in), labels: none, with-legend: false) = {
  set text(size: 8pt)
  lq.diagram(width: size.first(), height: size.last(), title: panel,
    xlabel: [Time (s)], ylabel: ylabel, xlim: limit,
    xaxis: (ticks: if limit.last() == 30 { (0, 10, 20, 30) }
      else if limit.last() == 10 { (0, 5, 10) }
      else if limit.last() == 3 { (0, 1, 2, 3) }
      else { (0, 0.5, 1) }),
    legend: if with-legend { (position: top + right, radius: 0pt) } else { none },
    ..runs.enumerate().map(pair => {
      let (i, run) = pair
      let indices = run.time_s.enumerate().filter(pair => pair.last() <= limit.last()).map(pair => pair.first())
      lq.plot(indices.map(j => run.time_s.at(j)), indices.map(j => run.at(field).at(j)),
        mark: none, color: colors.at(i),
        label: if labels == none { none } else { labels.at(i) },
        stroke: (thickness: 1pt, dash: if i == 0 { "solid" } else if i == 1 { "dashed" } else { "dotted" }))
    }),
  )
}
#let ctrl-force(test, panel, with-legend: false) = {
  let unlimited = test.unlimited
  let limited = test.limited
  let runs = (
    (time_s: unlimited.time_s, force_N: unlimited.applied_N),
    (time_s: limited.time_s, force_N: limited.requested_N),
    (time_s: limited.time_s, force_N: limited.applied_N),
  )
  ctrl-panel(runs, "force_N", [Force (N)], panel, limit: (0, 3), size: (2.6in, 0.9in),
    labels: ([Unlimited], [Requested, limited], [Applied, limited]), with-legend: with-legend)
}

#let optional-number(value, digits: 2) = if value == none { [—] } else { [#fmt(value, digits: digits)] }
#let dist-panel(runs, field, ylabel, panel, limit: (0, 30), size: (2.6in, 1in), labels: none, with-legend: false, color-offset: 0, held: true, legend-position: top + right) = {
  set text(size: 8pt)
  lq.diagram(width: size.first(), height: size.last(), title: panel,
    xlabel: [Time (s)], ylabel: ylabel, xlim: limit,
    xaxis: (ticks: if limit.last() == 30 { (0, 10, 20, 30) } else if limit.last() == 3 { (0, 1, 2, 3) } else { (0, 0.5, 1, 1.5) }),
    legend: if with-legend { (position: legend-position, radius: 0pt) } else { none },
    ..runs.enumerate().map(pair => {
      let (i, run) = pair
      let indices = run.time_s.enumerate().filter(pair => pair.last() <= limit.last()).map(pair => pair.first())
      lq.plot(indices.map(j => run.time_s.at(j)), indices.map(j => run.at(field).at(j)),
        mark: none, color: colors.at(i + color-offset),
        label: if labels == none { [#run.label] } else { labels.at(i) },
        step: if held and run.label == "Held" { end } else { none },
        stroke: (thickness: 0.9pt, dash: if i + color-offset == 0 { "solid" } else if i + color-offset == 1 { "dashed" } else if i + color-offset == 2 { "dotted" } else { "dash-dotted" }))
    }),
  )
}

#let velocity(field, ylabel, height: 2.6in) = {
  set text(size: 10pt)
  lq.diagram(width: 100%, height: 0% + height,
    xlabel: [Time (s)], ylabel: ylabel, xlim: (0, 30), legend: (radius: 0pt),
    lq.plot(plots.perturbation.time_s, plots.perturbation.at(field),
      mark: none, label: [5#sym.degree release], color: colors.first(),
      stroke: (thickness: 1.2pt)),
    lq.plot(plots.random_test.time_s, plots.random_test.at(field),
      mark: none, label: [2.5 N random force], color: colors.at(1),
      stroke: (thickness: 1.2pt, dash: "dashed")),
  )
}

#set page(paper: "us-letter", margin: (top: 0.75in, bottom: 1in, x: 1in),
  numbering: "1", number-align: center + bottom)
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

#align(center)[
  #text(size: 17pt, weight: "bold")[LQR Control of an Inverted Pendulum on a Cart]
  #v(0.15em)
  #text(size: 10pt)[J.C. Vaught]
  #v(0.1em)
  #text(size: 9pt)[EMCH 792: Learning-Based Controls]
]
#v(0.3em)

We reuse the nonlinear Simulink model from Project 1 and add a horizontal cart force. Since designing a controller directly from nonlinear equations is complex, we linearize them near upright. First, we use $sin(theta) approx theta$ and $cos(theta) approx 1$. Second, we discard the product $theta dot(theta)^2$, which does not contribute to the first-order model. This gives $dot(z)=A z+B F$ for $z=(x,dot(x),theta,dot(theta))^T$. Appendix A gives the derivation.

#figure([
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    comparison("x_m", [Cart position (m)], [(a) Cart motion], legend-position: bottom + left),
    comparison("theta_deg", [Pendulum angle (deg)], [(b) Pendulum motion]),
  )
], caption: [Linear and nonlinear responses to the same unforced 5#sym.degree release over 0.5 s.]) <fig-model>

  @fig-model shows that the models respond closely near upright. Their largest differences are #fmt(stats.model_comparison.max_angle_difference_deg, digits: 3)#sym.degree and #fmt(1000 * stats.model_comparison.max_x_difference_m, digits: 2) mm. This supports using the linear model for local controller design. Before designing that controller, we form $cal(C)=[B,A B,A^2 B,A^3 B]$. MATLAB finds rank four, equal to the number of states, so the system is controllable @MathWorks2026Controllability.

  Since we know the model and have all four states, we choose a linear-quadratic regulator (LQR). A proportional-integral-derivative (PID) controller can instead be tuned from measured response when a reliable model is unavailable @MathWorks2018PIDTuning. Here, LQR lets us assign a cost to each state error and to the force command @MathWorks2026LQR. We select weights of 4 for cart position, 2 for cart velocity, 300 for angle, and 10 for angular velocity, collected in $Q="diag"(4,2,300,10)$. The force penalty is $R=0.5$. These are design choices that emphasize balance while discouraging unnecessary motion and force. Appendix B gives the design and essential MATLAB functions.


  MATLAB calculates $u=-K z$ and confirms that all poles of $A-B K$ have negative real parts. We also simulate the linear closed loop and verify that its states return to zero. We then connect this controller to the nonlinear Simulink model in Appendix E. The actuator limits $u$ to $plus.minus 10$ N, and a separate disturbance $d$ is added afterward, so the cart receives $F=u+d$.

  To test the controller, we run two categories of 30 s simulations. First, we release the pendulum from 5, 10, 20, 30, 45, and 60#sym.degree to test the linearization and actuator limits. Second, we start upright and apply random cart forces with bounds of $plus.minus 2.5$, 5, 7.5, and 10 N. Each force is an independent uniform draw held for 0.1 s. The same seeded sequence is scaled for each bound. Appendix C explains this generation method and its scope. Appendix D gives the full metrics and actuator histories.
= RESULTS.

For the initial-angle tests, @fig-releases(a,c) shows cart position and pendulum angle over 30 s. Panels (b,d) show 0--6 s details. The 5, 10, and 20#sym.degree cases recover; the tested 30, 45, and 60#sym.degree cases fail. The transition from successful recovery to failure to recover therefore lies between the tested 20#sym.degree and 30#sym.degree releases.

For the random-force tests, @fig-forces(a,c,e) shows cart position, pendulum angle, and applied forces over 30 s. Panels (b,d,f) show 0--3 s details. The controller maintains balance at the tested 2.5, 5, and 7.5 N bounds, but loses balance at 10 N. At 2.5 N, the RMS angle is #fmt(stats.random_test.rms_angle_deg)#sym.degree and the peak is #fmt(stats.random_test.peak_angle_deg)#sym.degree.

#pagebreak()

#figure([
  #show: lq.layout
  #let panel-size = (2.6in, 0.95in)
  #grid(columns: (1fr, 1fr), gutter: 5pt,
    sweep(plots.angle_runs, "x_m", [Cart position (m)], (0, 30), [(a) Full cart response], data-size: panel-size, yscale: lq.scale.symlog(threshold: 1), failed-from: 3, with-legend: true, legend-position: top + right),
    sweep(plots.angle_runs, "x_m", [Cart position (m)], (0, 6), [(b) Cart detail], data-size: panel-size, ylim: (-0.15, 3.2), failed-from: 3),
    sweep(plots.angle_runs, "theta_deg", [Pendulum angle (deg)], (0, 30), [(c) Full angle response], data-size: panel-size, failed-from: 3),
    sweep(plots.angle_runs, "theta_deg", [Pendulum angle (deg)], (0, 6), [(d) Angle detail], data-size: panel-size, ylim: (-20, 400), failed-from: 3),
  )
], caption: [Initial-angle sweep. Dashed traces indicate initial angles where the controller failed to stabilize. Panels (b,d) show 0--6 s. Panel (a) uses a symmetric log scale, linear within $plus.minus 1$ m.]) <fig-releases>

= DISCUSSION.

The smaller tested inputs recover or remain balanced. Failed releases stay at the actuator limit, and the 10 N disturbance also causes sustained saturation. Even successful recovery at 20#sym.degree needs #fmt(stats.angle_stress.at(1).metrics.peak_cart_position_m) m of cart travel, so a physical track could constrain performance. The sweeps identify an operating range for this gain and force limit. The random-force result applies to the recorded sequence described in Appendix C.

#figure([
  #show: lq.layout
  #let panel-size = (2.6in, 0.95in)
  #grid(columns: (1fr, 1fr), gutter: 5pt,
    sweep(plots.force_runs, "x_m", [Cart position (m)], (0, 30), [(a) Full cart response], data-size: panel-size, yscale: lq.scale.symlog(threshold: 1), failed-from: 3, with-legend: true, legend-position: bottom + right),
    sweep(plots.force_runs, "x_m", [Cart position (m)], (0, 3), [(b) Cart detail], data-size: panel-size, failed-from: 3),
    sweep(plots.force_runs, "theta_deg", [Pendulum angle (deg)], (0, 30), [(c) Full angle response], data-size: panel-size, yscale: lq.scale.symlog(threshold: 10), failed-from: 3),
    sweep(plots.force_runs, "theta_deg", [Pendulum angle (deg)], (0, 3), [(d) Angle detail], data-size: panel-size, failed-from: 3),
    forcing((0, 30), [(e) Applied random forces], data-size: panel-size),
    forcing((0, 3), [(f) Force detail], data-size: panel-size, ylim: (-10, 10)),
  )
], caption: [Random-force sweep. Every bound uses the same sequence of force draws; the 10 N case is dashed. Panels (b,d,f) show 0--3 s. Panels (a,c) use symmetric log scales, linear within $plus.minus 1$ m and $plus.minus 10 degree$, respectively.]) <fig-forces>

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

= Appendix A. Nonlinear model, linearization, and model comparisons

We reuse the nonlinear model from Project 1, along with its mechanical assumptions. The cart translates horizontally on a frictionless track. A rigid, massless rod carries a point mass, and a viscous rotational damper acts at the pivot. Motion is planar, gravity is constant, and the track has no end stops. Project 2 adds the horizontal cart force $F$ to the original equations,

$
(M+m) dot.double(x) + m ell cos(theta) dot.double(theta)
- m ell sin(theta) dot(theta)^2 = F,
$
$
m ell cos(theta) dot.double(x) + m ell^2 dot.double(theta)
+ c_theta dot(theta) - m g ell sin(theta) = 0.
$

Here $x$ is cart displacement, $theta$ is the pendulum angle measured from upright, and dots indicate time derivatives. Positive $F$ acts in the positive $x$ direction. The symbols $M$, $m$, $ell$, $c_theta$, and $g$ denote cart mass, pendulum point mass, rod length, pivot damping coefficient, and gravitational acceleration, respectively. @tab-parameters gives the values retained from Project 1, using the mass symbols in the equations and MATLAB implementation.

#figure(
  table(columns: (0.8fr, 2fr, 0.8fr, 1fr), inset: (x: 6pt, y: 5pt),
    align: (x, y) => if x == 2 { right } else { left },
    table.hline(stroke: 0.8pt),
    table.header([Parameter], [Meaning], [Value], [Unit]),
    table.hline(stroke: 0.5pt),
    [$M$], [Cart mass], [2.0], [kg],
    [$m$], [Pendulum point mass], [0.5], [kg],
    [$ell$], [Rod length], [1.0], [m],
    [$c_theta$], [Pivot damping], [0.01], [N m s/rad],
    [$g$], [Gravity], [9.81], [m/s²],
    table.hline(stroke: 0.8pt),
  ), kind: table, caption: [Mechanical parameters reused from Project 1.],
) <tab-parameters>

Because the controller is intended to hold the pendulum upright, we expand about the stationary equilibrium $theta=dot(theta)=dot(x)=F=0$. Cart position can be chosen as $x=0$ because the equations do not depend on absolute position. For angles in radians, the Taylor expansions give

$
sin(theta)=theta-theta^3/6+ dots,
quad cos(theta)=1-theta^2/2+ dots.
$

Consequently, $sin(theta) approx theta$ and $cos(theta) approx 1$ retain the first-order behavior near upright. These approximations become accurate as the angle approaches zero. For example, at 5#sym.degree, replacing $sin(theta)$ by $theta$ introduces approximately 0.13% relative error, and replacing $cos(theta)$ by one introduces approximately 0.38% relative error.

We also simplify the centrifugal term, $m ell sin(theta) dot(theta)^2$, which represents the horizontal effect of the pendulum's rotational motion on the cart. Near upright, replacing $sin(theta)$ by $theta$ makes this term approximately $m ell theta dot(theta)^2$. It contains three factors that approach zero near the stationary equilibrium. One is the angle $theta$, and the other two are the angular velocity $dot(theta)$ multiplied by itself.

A first-order model retains terms proportional to a single small deviation, such as $theta$, $dot(theta)$, or $F$. The centrifugal term instead multiplies these deviations together. For example, reducing both the angle and angular velocity by a factor of ten reduces $theta dot(theta)^2$ by a factor of one thousand, while the retained gravity and damping terms decrease by only a factor of ten. Its effect therefore becomes much smaller than the retained terms as the motion approaches upright and rest. We discard it in this local linear model. This step assumes both a small angle and a small angular velocity; a small angle alone does not justify discarding it during rapid rotation. With this term removed and the trigonometric approximations substituted, the equations become

$
(M+m) dot.double(x)+m ell dot.double(theta)=F,
$
$
m ell dot.double(x)+m ell^2 dot.double(theta)
+c_theta dot(theta)-m g ell theta=0.
$

#pagebreak()

With the linearized equations established, we separate the accelerations to obtain the state-space model. Divide the second linearized equation by $m ell$ and rearrange it,

$
ell dot.double(theta)=-dot.double(x)-c_theta/(m ell) dot(theta)+g theta.
$

Substituting this expression into the first equation eliminates $dot.double(theta)$,

$
(M+m) dot.double(x)+m(-dot.double(x)-c_theta/(m ell) dot(theta)+g theta)=F,
$
$
M dot.double(x)=F+c_theta/ell dot(theta)-m g theta.
$

Dividing by $M$ and substituting the result back into the angular equation gives

$
dot.double(x)=F/M-(m g)/M theta+c_theta/(M ell) dot(theta),
$
$
dot.double(theta)=-F/(M ell)+((M+m)g)/(M ell) theta
-(c_theta(M+m))/(M m ell^2) dot(theta).
$

These two second-order equations become four first-order equations by defining

$
z=mat(z_1;z_2;z_3;z_4)=mat(x;dot(x);theta;dot(theta)),
quad dot(z)=mat(z_2;-(m g)/M z_3+c_theta/(M ell) z_4+F/M;z_4;((M+m)g)/(M ell) z_3-(c_theta(M+m))/(M m ell^2) z_4-F/(M ell)).
$

Collecting the state coefficients and force coefficients gives $dot(z)=A z+B F$. With the parameters in @tab-parameters, the matrices are

$
A=mat(0,1,0,0;0,0,-2.4525,0.005;0,0,0,1;0,0,12.2625,-0.025),
quad B=mat(0;0.5;0;-0.5).
$

Before designing the controller, MATLAB forms the controllability matrix $cal(C)=[B,A B,A^2 B,A^3 B]$ and finds $"rank"(cal(C))=4$. The rank equals the four-state dimension, so the cart force can control all four states in this linear model.

To check whether this linear model captures the nonlinear motion near upright, we compare both models under identical initial conditions and inputs, without feedback or actuator limits. Each runs for 1 s using MATLAB's ode45 solver, relative tolerance $10^(-10)$, absolute tolerance $10^(-12)$, and a maximum step of 0.002 s. The nonlinear model uses the Simulink plant's acceleration function.

Because uncontrolled motion grows away from upright, we compare errors at 0.1, 0.25, and 0.5 s rather than 10 or 20 s. Relative to the nonlinear response, the percentage errors are

$
e_x(t)=100 abs(x_"lin"(t)-x_"nonlin"(t))/abs(x_"nonlin"(t)),
quad e_theta(t)=100 abs(theta_"lin"(t)-theta_"nonlin"(t))/abs(theta_"nonlin"(t)).
$

Percentage errors are undefined at a zero reference value. All reference values at the selected times are nonzero.

#pagebreak()

First, we release both models from 2, 5, 10, 15, 20, 25, and 30#sym.degree, with zero cart position, zero velocities, and zero applied force. @fig-model-angles compares the motion, and @tab-model-angles reports the differences at the selected times.

#figure([
  #show: lq.layout
  #grid(columns: (1fr,), gutter: 8pt,
    model-sweep(model_tests.angle_runs, "x_m", [Cart position (m)], [(a) Cart motion], unit: [#sym.degree], with-legend: true, legend-position: bottom + left),
    model-sweep(model_tests.angle_runs, "theta_deg", [Pendulum angle (deg)], [(b) Pendulum motion], unit: [#sym.degree]),
  )
], caption: [Uncontrolled responses from seven initial angles over 1 s. Solid lines use the nonlinear equations; dashed lines use the upright linearization. Matching colors indicate matching initial angles.]) <fig-model-angles>

#figure(model-error-table(model_tests.angle_runs, [Initial angle (deg)], time-dividers: true),
  kind: table, caption: [Percentage model errors following unforced releases, relative to the nonlinear response at each comparison time.],
) <tab-model-angles>

At 0.5 s, the 2#sym.degree release has an angle error of #fmt(model_tests.angle_runs.first().angle_error_percent.last(), digits: 3)% and a cart-position error of #fmt(model_tests.angle_runs.first().x_error_percent.last(), digits: 3)%. At 30#sym.degree, those errors increase to #fmt(model_tests.angle_runs.last().angle_error_percent.last())% and #fmt(model_tests.angle_runs.last().x_error_percent.last())%, respectively. The increasing differences show why the linear model is appropriate near upright and why larger releases require verification with the nonlinear plant.

#pagebreak()

Second, we start both models upright and at rest and apply a constant horizontal force from $t=0$. The six force levels are 0.5, 1, 2, 4, 8, and 16 N. @fig-model-inputs shows the responses, and @tab-model-inputs reports the differences. These are prescribed inputs for model validation, separate from the later controller tests with a 10 N actuator limit.

#figure([
  #show: lq.layout
  #grid(columns: (1fr,), gutter: 8pt,
    model-sweep(model_tests.force_runs, "x_m", [Cart position (m)], [(a) Cart motion], unit: [ N], with-legend: true),
    model-sweep(model_tests.force_runs, "theta_deg", [Pendulum angle (deg)], [(b) Pendulum motion], unit: [ N]),
  )
], caption: [Uncontrolled responses to six constant cart forces applied from upright at rest. Solid lines use the nonlinear equations; dashed lines use the upright linearization. Matching colors indicate matching forces.]) <fig-model-inputs>

#figure(model-error-table(model_tests.force_runs, [Force (N)], time-dividers: true),
  kind: table, caption: [Percentage model errors under constant cart force, relative to the nonlinear response at each comparison time.],
) <tab-model-inputs>

At 0.5 s, the 0.5 N input gives an angle error of #fmt(model_tests.force_runs.first().angle_error_percent.last(), digits: 3)%, while 16 N gives #fmt(model_tests.force_runs.last().angle_error_percent.last())%. Stronger forces drive the pendulum farther from upright, increasing the effect of the nonlinear terms. Together, the release and force comparisons support using the linear model for local controller design. They also establish the need to test that controller on the nonlinear model, as done in Appendices C and D.

#pagebreak()

= Appendix B. Controller selection, LQR design, and verification

With the controllable linear model from Appendix A, we next choose how to generate the cart force. A proportional-integral-derivative (PID) controller combines the current output error, its accumulated history, and its rate of change. Its gains can be tuned from measured responses or with a model @MathWorks2026PIDData. For this plant, controlling angle and cart position with PID would require coordinating the two objectives, for example through nested loops.

Pole-placement feedback also uses a model and the system states. The designer selects the desired closed-loop poles, and MATLAB calculates a gain that produces them @MathWorks2026PolePlacement. This directly specifies response modes but does not explicitly assign a cost to actuator effort. A linear quadratic regulator (LQR) instead calculates state feedback from penalties on state deviations and force. Model predictive control (MPC) repeatedly predicts future motion and optimizes a sequence of inputs while accounting for constraints @MathWorks2026MPC. It can represent force and track limits directly, but requires an optimization at each control update.

We select LQR because the model and all four simulated states are available. A single feedback law can address pendulum balance and cart motion together, and its cost function provides a direct way to trade motion against force demand. The resulting gain is calculated once and applied through a matrix multiplication. Unlike constrained MPC, this LQR design does not enforce the actuator limit; we examine that limit separately below.

To calculate the gain, we minimize the accumulated quadratic cost,

$
J=integral_0^infinity (z^T Q z+R u^2) dif t
=integral_0^infinity (4x^2+2dot(x)^2+300theta^2+10dot(theta)^2+0.5u^2) dif t.
$

Here $x$ is measured in meters, $theta$ in radians, and $u$ in newtons. The four diagonal entries of $Q$ penalize cart position, cart velocity, pendulum angle, and angular velocity in that order. The scalar $R$ penalizes force. Increasing a weight makes the corresponding squared quantity more expensive in the optimization. Since the states have different units, the coefficients must be interpreted together with those units; their numerical sizes alone do not establish relative importance.

The baseline settings in @tab-lqr-design are tuning choices. MATLAB's `lqr` function solves the algebraic Riccati equation and returns the gain $K$ and the poles of $A-B K$ @MathWorks2026LQR. The control law is $u=-K z$. All four poles have negative real parts, establishing stability of the unlimited linear closed loop. The following tests examine its response and assess the weight choices.

#figure(table(columns: (1fr, 3.8fr), inset: (x: 6pt, y: 5pt), align: left,
  table.hline(stroke: 0.8pt), table.header([Quantity], [Baseline value]),
  table.hline(stroke: 0.5pt),
  [$Q$], [$"diag"(4,2,300,10)$],
  [$R$], [0.5],
  [$K$], [$(-2.8284,-6.3204,-86.8641,-25.2346)$],
  [Slow pole pair], [$-0.699 plus.minus 0.548i$],
  [Fast pole pair], [$-4.042 plus.minus 1.125i$],
  table.hline(stroke: 0.8pt),
), kind: table, caption: [Baseline LQR settings, feedback gain, and closed-loop poles.]) <tab-lqr-design>

#pagebreak()

First, we compare the uncontrolled and baseline LQR-controlled linear plants from the same 5#sym.degree release, with the cart at the origin and both velocities zero. @fig-feedback-short shows the first second. The uncontrolled angle grows away from upright, while feedback reverses that growth. The cart initially moves to correct the pendulum angle; keeping the cart stationary throughout this transient would prevent that corrective motion.

#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr), gutter: 8pt,
    ctrl-panel((ctrl.baseline, ctrl.uncontrolled), "theta_deg", [Angle (deg)], [(a) Pendulum angle], limit: (0, 1), size: (2.6in, 1.15in), labels: ([LQR], [No feedback]), with-legend: true),
    ctrl-panel((ctrl.baseline, ctrl.uncontrolled), "x_m", [Position (m)], [(b) Cart position], limit: (0, 1), size: (2.6in, 1.15in)),
  )
], caption: [Effect of LQR feedback during the first second of a 5#sym.degree release on the linear plant.]) <fig-feedback-short>

The longer response in @fig-feedback-long shows the cart returning toward the origin as the pendulum settles. These simulations use ode45 with relative tolerance $10^(-10)$, absolute tolerance $10^(-12)$, and a maximum step of 0.005 s. Results are evaluated every 0.01 s over 30 s, with every second sample used for plotting. Unlimited responses are checked against the matrix-exponential solution at the final time.

#figure([
  #show: lq.layout
  #grid(columns: (1fr,), gutter: 6pt,
    ctrl-panel((ctrl.baseline,), "theta_deg", [Angle (deg)], [(a) Pendulum angle], size: (5.8in, 0.85in)),
    ctrl-panel((ctrl.baseline,), "x_m", [Position (m)], [(b) Cart position], size: (5.8in, 0.85in)),
    ctrl-panel((ctrl.baseline,), "applied_N", [Force (N)], [(c) Actuator force], size: (5.8in, 0.85in)),
  )
], caption: [Baseline unlimited LQR response over 30 s on the linear plant, starting from 5#sym.degree.]) <fig-feedback-long>

For this appendix, joint settling time $t_s$ is the first sampled time after which both $abs(theta)<=1 degree$ and $abs(x)<=0.02$ m hold through the end of the run. The baseline meets these conditions at #fmt(ctrl.baseline.metrics.settling_time_s) s, with peak cart displacement #fmt(ctrl.baseline.metrics.peak_x_m, digits: 3) m and peak force #fmt(ctrl.baseline.metrics.peak_requested_N) N. Its final state norm is $#fmt(ctrl.baseline.metrics.final_state_norm * 1e10) times 10^(-10)$, consistent with convergence to equilibrium.

#pagebreak()

Having verified the baseline response, we vary one penalty at a time to assess the tuning tradeoffs. All runs use the same linear plant, unlimited actuator, and 5#sym.degree release. In @fig-angle-weights, the angle penalty $q_theta$ takes values of 100, 300, and 900, while the remaining state weights and $R=0.5$ stay fixed. The response details show the first 10 s; the metrics use all 30 s.

#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr, 1fr), gutter: 6pt,
    ctrl-panel(ctrl.angle_weights, "theta_deg", [Angle (deg)], [(a) Pendulum angle], limit: (0, 10), size: (1.65in, 1.2in), labels: ([100], [300], [900]), with-legend: true),
    ctrl-panel(ctrl.angle_weights, "x_m", [Position (m)], [(b) Cart position], limit: (0, 10), size: (1.65in, 1.2in)),
    ctrl-panel(ctrl.angle_weights, "applied_N", [Force (N)], [(c) Actuator force], limit: (0, 10), size: (1.65in, 1.2in)),
  )
], caption: [Effect of changing the angle penalty $q_theta$ from the baseline value of 300. The legend gives $q_theta$; all other penalties remain fixed.]) <fig-angle-weights>

We next keep $Q="diag"(4,2,300,10)$ fixed and vary the force penalty $R$ over 0.1, 0.5, and 2. @fig-force-weights shows how this changes the motion and actuator demand.

#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr, 1fr), gutter: 6pt,
    ctrl-panel(ctrl.force_weights, "theta_deg", [Angle (deg)], [(a) Pendulum angle], limit: (0, 10), size: (1.65in, 1.2in), labels: ([0.1], [0.5], [2]), with-legend: true),
    ctrl-panel(ctrl.force_weights, "x_m", [Position (m)], [(b) Cart position], limit: (0, 10), size: (1.65in, 1.2in)),
    ctrl-panel(ctrl.force_weights, "applied_N", [Force (N)], [(c) Actuator force], limit: (0, 10), size: (1.65in, 1.2in)),
  )
], caption: [Effect of changing the force penalty $R$ from the baseline value of 0.5. The legend gives $R$; all state penalties remain fixed.]) <fig-force-weights>

To quantify these differences, @tab-weight-results reports the joint settling time $t_s$, peak cart displacement $x_"peak"$, peak requested force $u_"peak"$, and force effort $E_u=integral_0^(30) u(t)^2 dif t$. The baseline appears once because it belongs to both sweeps.

#let tuning-runs = ctrl.angle_weights + (ctrl.force_weights.first(), ctrl.force_weights.last())
#figure(table(columns: (0.6fr, 0.6fr, 1fr, 1fr, 1fr, 1.2fr), inset: (x: 5pt, y: 5pt),
  align: (x, y) => if y == 0 { center } else { right },
  table.hline(stroke: 0.8pt),
  table.header([$q_theta$], [$R$], [$t_s$ (s)], [$x_"peak"$ (m)], [$u_"peak"$ (N)], [$E_u$ (N² s)]),
  table.hline(stroke: 0.5pt),
  ..tuning-runs.map(run => ([#str(run.q_theta)], [#str(run.R)],
    [#fmt(run.metrics.settling_time_s)], [#fmt(run.metrics.peak_x_m, digits: 3)],
    [#fmt(run.metrics.peak_requested_N)], [#fmt(run.metrics.effort_N2_s)])).flatten(),
  table.hline(stroke: 0.8pt),
), kind: table, caption: [Weight-sweep metrics for the unlimited linear plant following a 5#sym.degree release.]) <tab-weight-results>

Increasing $q_theta$ from 100 to 900 reduces peak cart travel from 0.310 to 0.281 m, but raises peak force from 7.16 to 8.62 N and joint settling time from 4.64 to 5.49 s. Reducing $R$ to 0.1 gives faster settling and less travel, but its 11.38 N peak exceeds the intended actuator limit. Increasing $R$ to 2 reduces force effort but increases travel and settling time. The baseline retains a peak force below 10 N for this release while recovering faster and using less travel than $R=2$. We therefore retain it as a compromise for the nonlinear tests.

#pagebreak()

The preceding LQR calculations assume that the actuator can deliver every requested force. We now isolate the effect of its 10 N limit by using the same linear plant and gain with either $u=-K z$ or $u="sat"(-K z)$, where saturation clips the command to $[-10,10]$ N. We test 5#sym.degree and 20#sym.degree releases without disturbance. The larger release activates the force limit. @fig-limit-motion compares the angle and cart responses.

#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr), gutter: 6pt,
    ctrl-panel((ctrl.saturation.first().unlimited, ctrl.saturation.first().limited), "theta_deg", [Angle (deg)], [(a) 5° angle], limit: (0, 10), size: (2.6in, 0.85in), labels: ([Unlimited], [Limited]), with-legend: true),
    ctrl-panel((ctrl.saturation.first().unlimited, ctrl.saturation.first().limited), "x_m", [Position (m)], [(b) 5° cart], limit: (0, 10), size: (2.6in, 0.85in)),
    ctrl-panel((ctrl.saturation.last().unlimited, ctrl.saturation.last().limited), "theta_deg", [Angle (deg)], [(c) 20° angle], limit: (0, 10), size: (2.6in, 0.85in)),
    ctrl-panel((ctrl.saturation.last().unlimited, ctrl.saturation.last().limited), "x_m", [Position (m)], [(d) 20° cart], limit: (0, 10), size: (2.6in, 0.85in)),
  )
], caption: [Linear-plant responses with unlimited (solid) and 10 N limited (dashed) feedback.]) <fig-limit-motion>

To explain these response differences, @fig-limit-force compares the requested and applied forces. The 20#sym.degree case shows the applied force clipped while the requested command exceeds 10 N.

#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr), gutter: 6pt,
    ctrl-force(ctrl.saturation.first(), [(a) 5° release], with-legend: true),
    ctrl-force(ctrl.saturation.last(), [(b) 20° release]),
  )
], caption: [Unlimited force, limited-loop requested force, and limited-loop applied force over the first 3 s. Applied force is clipped at $plus.minus 10$ N.]) <fig-limit-force>

@tab-limit-results summarizes these runs. Recovery requires the angle and cart position to remain within the settling bounds during the final 2 s. Saturation duration is the time for which the requested command exceeds 10 N in magnitude, estimated on the 0.01 s analysis grid.

#figure(table(columns: (0.8fr, 1fr, 0.9fr, 1fr, 1fr, 1fr), inset: (x: 5pt, y: 4pt),
  align: (x, y) => if y == 0 or x == 1 or x == 2 { left } else { right },
  table.hline(stroke: 0.8pt),
  table.header([Release (deg)], [Actuator], [Recovered], [$t_s$ (s)], [Saturated (s)], [$u_"peak"$ (N)]),
  table.hline(stroke: 0.5pt),
  ..ctrl.saturation.map(test => ("unlimited", "limited").map(mode => {
    let metrics = test.at(mode).metrics
    ([#str(test.initial_angle_deg)], [#if mode == "unlimited" { "Unlimited" } else { "10 N limit" }],
      [#if metrics.recovered { "Yes" } else { "No" }],
      [#if metrics.settling_time_s == none { "—" } else { fmt(metrics.settling_time_s) }],
      [#fmt(metrics.saturation_duration_s)], [#fmt(metrics.peak_requested_N)])
  }).flatten()).flatten(),
  table.hline(stroke: 0.8pt),
), kind: table, caption: [Linear-plant recovery and actuator saturation with the baseline gain. Peak force is the requested command.]) <tab-limit-results>

At 5#sym.degree, the requested force remains below 10 N, so the unlimited and limited responses coincide. At 20#sym.degree, the limit increases settling time from 7.61 to 9.28 s and peak cart travel from 1.201 to 2.504 m. The actuator saturates for approximately 0.62 s, but the system still recovers. Once clipping occurs, the dynamics are no longer governed by the fixed matrix $A-B K$ alone. Its stable poles therefore do not guarantee recovery for arbitrary releases. Appendix D tests the limited controller on the nonlinear plant.

#pagebreak()

The essential controller calculation is shown below. It constructs the linear model, sets the penalties, and calculates the feedback gain. The separate `controller_studies.m` file runs the response, weight, and saturation comparisons and exports the data used in this appendix.

#show raw.where(block: true): it => block(width: 100%, fill: rgb("#ECECEC"),
  stroke: 0.5pt + rgb("#A2A2A2"), inset: 6pt)[
  #set text(font: "DejaVu Sans Mono", size: 7.3pt)
  #it
]
```matlab
function K = design_controller(M, m, ell, c_theta, g)
% State order is [x; x_dot; theta; theta_dot].
A = [0 1 0 0;
     0 0 -m*g/M c_theta/(M*ell);
     0 0 0 1;
     0 0 (M+m)*g/(M*ell) -c_theta*(M+m)/(M*m*ell^2)];
B = [0; 1/M; 0; -1/(M*ell)];
Q = diag([4 2 300 10]);
R = 0.5;
K = lqr(A, B, Q, R);
end
```

To apply the same gain to the original nonlinear plant, the Simulink block uses the acceleration function below. Its eighth input is the total cart force after actuator limiting and disturbance addition.

#raw(read("controlled_accelerations.m"), lang: "matlab", block: true)

Appendix E shows how these functions connect through the feedback loop. With the gain fixed, Appendix C defines the nonlinear release and random-force test protocol, and Appendix D reports the resulting operating limits.

#pagebreak()
#set page(flipped: false, margin: 1in)

= Appendix C. Random-force generation, shaping, and test protocol

With the controller fixed in Appendix B, we next define the external force used to test it. MATLAB draws independent uniform samples $xi_k$ in $[-1,1]$ every 0.1 s. Multiplying each draw by a bound $a$ gives the target force $r(t)=a xi_k$, held until the next draw. We retain bounds of 2.5, 5, 7.5, and 10 N. Seed 79202 reproduces the original sequence, and scaling the same draws allows strength comparisons with matched timing and signs.

The original held force changes instantaneously at sample boundaries. A reversal from $-10$ to $+10$ N completed over 0.1 s would require an average rate of 200 N/s; an instantaneous reversal has no finite rate. Whether 200 N/s is realistic depends on the source of the force. To represent a disturbance with finite response speed, we add smoothing and a separate rate limit. These address different properties of the input rather than merely changing its appearance.

First, a low-pass filter produces $s(t)$ according to

$
tau dot(s)+s=r, quad H(p)=1/(tau p+1).
$

Here $tau$ is the time constant and $p$ is the Laplace variable. A larger $tau$ makes the force follow the target more gradually. This filter removes force jumps but does not impose a fixed maximum slope @MathWorks2026TransferFunction. We then limit how quickly the applied disturbance $d$ can approach $s$. On the profile grid, the update is

$
d_(i+1)=d_i+"clip"(s_(i+1)-d_i,-L h,L h),
$

where $h=0.002$ s and $L$ is the maximum rate in N/s. Thus, every linear segment satisfies $abs(dot(d))<=L$. This performs the slope-limiting operation represented by a rate limiter @MathWorks2026RateLimiter. The nominal settings are $tau=0.1$ s and $L=50$ N/s. They are exploratory disturbance assumptions, not measured properties of a particular force source. The random profiles begin at zero; filter and limiter states begin at the initial force for the separate reversal test.

To demonstrate the two operations, @fig-dist-reversal compares a held target, smoothing alone, rate limiting alone, and their combination. The target reverses at 0.5 s. With a 50 N/s limit, the full 20 N change requires at least 0.4 s. @tab-dist-reversal reports the maximum finite rate and the time to complete 95% of the reversal, reaching $+9$ N.

#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr), gutter: 8pt,
    dist-panel(dist.reversal, "force_N", [Force (N)], [(a) Extreme reversal], limit: (0, 1.5), size: (2.6in, 1in), with-legend: true, legend-position: top + left),
    dist-panel(dist.reversal.slice(1), "rate_N_s", [Rate (N/s)], [(b) Finite change rates], limit: (0, 1.5), size: (2.6in, 1in), color-offset: 1),
  )
], caption: [Force reversal at 0.5 s and the finite change rates of the three continuous profiles. The held force jumps instantaneously and has no finite rate at that instant.]) <fig-dist-reversal>

#figure(table(columns: (1.6fr, 1fr, 1fr), inset: (x: 5pt, y: 4pt),
  align: (x, y) => if y == 0 or x == 0 { left } else { right },
  table.hline(stroke: 0.8pt), table.header([Profile], [Maximum rate (N/s)], [95% reversal time (s)]),
  table.hline(stroke: 0.5pt),
  ..dist.reversal.map(run => ([#run.label], [#optional-number(run.max_rate_N_s)], [#fmt(run.transition_95_s)])).flatten(),
  table.hline(stroke: 0.8pt),
), kind: table, caption: [Reversal timing and force-change rates with $tau=0.1$ s and $L=50$ N/s. A dash denotes an undefined instantaneous rate.]) <tab-dist-reversal>

#pagebreak()

Having established the behavior for a single reversal, @fig-dist-random applies all four versions to the same 10 N random target over 30 s. The detail shows how the staircase becomes gradual motion. The profiles remain within the target bounds because both updates move toward bounded values without overshoot. MATLAB computes them before simulation; held inputs use zero-order hold, while continuous profiles use linear interpolation in the existing Simulink source block. The controller's separate 10 N actuator limit is unchanged.

#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr), gutter: 8pt,
    dist-panel(dist.random_profiles, "force_N", [Force (N)], [(a) Full random-force record], limit: (0, 30), size: (2.6in, 0.75in), with-legend: true),
    dist-panel(dist.random_profiles, "force_N", [Force (N)], [(b) First 3 s], limit: (0, 3), size: (2.6in, 0.75in)),
  )
], caption: [Held, smoothed, rate-limited, and combined disturbances from the same 10 N target sequence, seed 79202.]) <fig-dist-random>

@tab-dist-profiles reports peak force, root-mean-square (RMS) force over 30 s, and maximum finite slope. Smoothing and limiting change the disturbance's strength as well as its timing, so a bound of 10 N does not imply equal RMS force across profiles.

#figure(table(columns: (1.3fr, 1fr, 1fr, 1.2fr), inset: (x: 5pt, y: 2pt),
  align: (x, y) => if y == 0 or x == 0 { left } else { right },
  table.hline(stroke: 0.8pt), table.header([Profile], [Peak (N)], [RMS (N)], [Maximum rate (N/s)]),
  table.hline(stroke: 0.5pt),
  ..dist.random_profiles.map(run => ([#run.label], [#fmt(run.peak_N)], [#fmt(run.rms_N)], [#optional-number(run.max_rate_N_s)])).flatten(),
  table.hline(stroke: 0.8pt),
), kind: table, caption: [Actual strength and slope of the four 30 s disturbance profiles.]) <tab-dist-profiles>

To assess sensitivity, @fig-dist-settings varies the filter time constant over 0.05, 0.1, and 0.2 s without a limiter, then varies the limiter rate over 25, 50, and 100 N/s without a filter. Both sweeps use the same 10 N target. @tab-dist-settings quantifies their effects over 30 s; the curves show the first 3 s.

#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr), gutter: 8pt,
    dist-panel(dist.tau_sweep, "force_N", [Force (N)], [(a) Smoothing time constant], limit: (0, 3), size: (2.6in, 0.75in), labels: ([0.05 s], [0.1 s], [0.2 s]), with-legend: true, held: false),
    dist-panel(dist.rate_sweep, "force_N", [Force (N)], [(b) Maximum rate], limit: (0, 3), size: (2.6in, 0.75in), labels: ([25 N/s], [50 N/s], [100 N/s]), with-legend: true, held: false),
  )
], caption: [Sensitivity of the disturbance to smoothing time constant and rate limit, tested separately.]) <fig-dist-settings>

#figure(table(columns: (1fr, 1fr, 1fr, 1fr, 1.2fr), inset: (x: 5pt, y: 2pt),
  align: (x, y) => if y == 0 or x == 0 { left } else { right },
  table.hline(stroke: 0.8pt), table.header([Operation], [Setting], [Peak (N)], [RMS (N)], [Maximum rate (N/s)]),
  table.hline(stroke: 0.5pt),
  ..dist.tau_sweep.map(run => ([Filter], [#str(run.setting) s], [#fmt(run.peak_N)], [#fmt(run.rms_N)], [#fmt(run.max_rate_N_s)])).flatten(),
  ..dist.rate_sweep.map(run => ([Limiter], [#str(run.setting) N/s], [#fmt(run.peak_N)], [#fmt(run.rms_N)], [#fmt(run.max_rate_N_s)])).flatten(),
  table.hline(stroke: 0.8pt),
), kind: table, caption: [Separate shaping sweeps using the same 10 N random target.]) <tab-dist-settings>

Finally, 160 nonlinear trials compare held and combined disturbances across seeds 79202--79221 and four bounds. Each starts upright at rest and lasts 30 s. The ode45 settings are a 0.005 s maximum step, $10^(-7)$ relative tolerance, and $10^(-9)$ absolute tolerance. States are sampled every 0.02 s; balance requires $abs(theta)<90 degree$ throughout. Appendix D reports angle RMS, peak travel, saturation, and paired-seed results. Shaping changes temporal correlation and RMS strength, so these tests assess both effects together.

#pagebreak()

= Appendix D. Detailed release and disturbance results

With the disturbance method defined in Appendix C, we collect the nonlinear performance results here. The original release tests start from 5, 10, 20, 30, 45, or 60#sym.degree with all other states and the disturbance zero. They run for 30 s with a 0.01 s maximum solver step. Metrics use a 0.02 s grid. Recovery requires the final angle and final-two-second angle RMS to be below 2#sym.degree. Actuator saturation counts samples at the 10 N limit.

#let release_entries = ((initial_angle_deg: 5, metrics: stats.perturbation),) + stats.angle_stress
#figure(table(columns: (0.8fr, 1.2fr, 1.2fr, 1fr, 1fr), inset: (x: 5pt, y: 2pt),
  align: (x, y) => if y == 0 or x == 4 { left } else { right },
  table.hline(stroke: 0.8pt),
  table.header([Initial angle (deg)], [Peak cart displacement (m)], [Final 2 s RMS (deg)], [Saturation (%)], [Recovered]),
  table.hline(stroke: 0.5pt),
  ..release_entries.map(entry => ([#str(entry.initial_angle_deg)], [#fmt(entry.metrics.peak_cart_position_m, digits: 3)],
    [#fmt(entry.metrics.final_2s_rms_angle_deg, digits: 4)], [#fmt(100*entry.metrics.saturation_fraction)],
    [#if entry.metrics.recovered { "Yes" } else { "No" }])).flatten(),
  table.hline(stroke: 0.8pt),
), kind: table, caption: [Original release-test recovery, cart travel, and actuator saturation.]) <tab-release-metrics>

#figure([
  #sweep(plots.angle_runs, "u_N", [Actuator command (N)], (0, 30), [Release-test actuator commands],
    height: 1.15in, ylim: (-10.5, 10.5), failed-from: 3, with-legend: true)
], caption: [Original initial-angle actuator histories. The failed cases remain at the actuator limit.])

The tested 20#sym.degree release recovers but reaches #fmt(stats.angle_stress.at(1).metrics.peak_cart_position_m) m of travel. The tested 30#sym.degree release fails, placing the recovery-to-failure transition between them. No intermediate releases were tested. After failure, the model's unlimited track permits continued acceleration, and its angle records full rotations.

The velocity histories below complete the four-state record. They compare the original 5#sym.degree release and the original 2.5 N held-force trial. Release velocities decay toward rest, whereas the continuing disturbance produces continuing velocity fluctuations.

#figure(velocity("x_dot_m_s", [Cart velocity (m/s)], height: 1.05in),
  caption: [Cart velocity supplied to the state-feedback gain in the original nominal tests.])

The angular velocity provides the remaining state used by the controller. The plotted units are degrees per second; the feedback calculation uses radians per second.

#v(8pt)
#figure(velocity("theta_dot_deg_s", [Angular velocity (deg/s)], height: 1.05in),
  caption: [Pendulum angular velocity in the original nominal tests.])

#pagebreak()

For the paired 5 N tests in @fig-dist-controller, both profiles use seed 79202, an upright initial state, the baseline gain, and the 10 N actuator limit. The combined settings are $tau=0.1$ s and $L=50$ N/s.

#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr, 1fr), gutter: 6pt,
    ctrl-panel(dist.controller_runs, "theta_deg", [Angle (deg)], [(a) Pendulum angle], limit: (0, 30), size: (1.65in, 0.85in), labels: ([Held], [Combined]), with-legend: true),
    ctrl-panel(dist.controller_runs, "x_m", [Position (m)], [(b) Cart position], limit: (0, 30), size: (1.65in, 0.85in)),
    ctrl-panel(dist.controller_runs, "applied_N", [Actuator force (N)], [(c) Actuator demand], limit: (0, 30), size: (1.65in, 0.85in)),
  )
], caption: [Nonlinear controller responses to held and combined 5 N disturbances, seed 79202.]) <fig-dist-controller>

@tab-dist-nominal extends the comparison to all four bounds using Appendix C's solver settings. The 30 s metrics distinguish actual force strength from controller response; balance requires $abs(theta)<90 degree$.

#figure([
  #set text(size: 9pt)
  #table(columns: (0.6fr, 1fr, 0.8fr, 1fr, 1fr, 1fr, 0.8fr), inset: (x: 4pt, y: 2pt),
    align: (x, y) => if y == 0 or x == 1 or x == 2 { left } else { right },
    table.hline(stroke: 0.8pt),
    table.header([Bound (N)], [Profile], [Balanced], [Force RMS (N)], [Angle RMS (deg)], [Peak cart (m)], [Saturated (%)]) ,
    table.hline(stroke: 0.5pt),
    ..dist.seed_summary.map(pair => dist.nominal.filter(run => run.bound_N == pair.bound_N and run.mode == pair.mode).first()).map(run => ([#fmt(run.bound_N, digits: 1)], [#if run.mode == 1 { "Held" } else { "Combined" }],
      [#if run.balanced { "Yes" } else { "No" }], [#fmt(run.force_rms_N)], [#fmt(run.rms_angle_deg)],
      [#fmt(run.peak_x_m, digits: 3)], [#fmt(run.saturation_percent)])).flatten(),
    table.hline(stroke: 0.8pt),
  )
], kind: table, caption: [Paired held and combined disturbance results for seed 79202.]) <tab-dist-nominal>

The original held-force actuator histories are retained below for comparison with Figure 3. At the original 10 N bound, the controller loses balance and remains saturated after failure.

#figure([
  #sweep(plots.force_runs, "u_N", [Actuator command (N)], (0, 30), [Original held-force actuator commands],
    height: 1.0in, ylim: (-10.5, 10.5), failed-from: 3, with-legend: true)
], caption: [Original actuator histories under the four held-force bounds. The failed 10 N case is dashed.])

To test dependence on the random draws, @tab-dist-seeds summarizes 20 seeds per bound and profile. Force medians include all trials; response medians include balanced trials only.

#figure([
  #set text(size: 9pt)
  #table(columns: (0.6fr, 1fr, 0.9fr, 1fr, 1fr, 1fr), inset: (x: 4pt, y: 2pt),
    align: (x, y) => if y == 0 or x == 1 { left } else { right },
    table.hline(stroke: 0.8pt),
    table.header([Bound (N)], [Profile], [Balanced / 20], [Median force RMS (N)], [Median angle RMS (deg)], [Median peak cart (m)]),
    table.hline(stroke: 0.5pt),
    ..dist.seed_summary.map(run => ([#fmt(run.bound_N, digits: 1)], [#if run.mode == 1 { "Held" } else { "Combined" }],
      [#str(run.balanced_count)], [#fmt(run.median_force_rms_N)],
      [#optional-number(run.median_rms_angle_deg_balanced)], [#optional-number(run.median_peak_x_m_balanced, digits: 3)])).flatten(),
    table.hline(stroke: 0.8pt),
  )
], kind: table, caption: [Results across seeds 79202--79221. Response medians use balanced trials only.]) <tab-dist-seeds>

Both profiles maintain balance in all 20 trials through 7.5 N. At 10 N, the held profile maintains balance in 18 trials and the combined profile in 19; seed 79202 fails with both. At 5 N for that seed, shaping reduces force RMS from 2.98 to 1.84 N and angle RMS from 1.39 to 1.32 degrees, with nearly unchanged cart travel. Because force strength also changes, this comparison does not isolate the effect of smoothing at equal RMS force.

#pagebreak()
#set page(flipped: true, margin: 1in)

= Appendix E. Simulink feedback loop and nonlinear plant

#figure(image("controlled_model_diagram.png", width: 100%),
  caption: [Complete feedback loop. The disturbance enters above the circular sum, and the limited actuator command returns below the loop.])

The gain from Appendix B acts on all four simulated states. The actuator block limits the command, then the sum adds the disturbance before the total force reaches the cart. Output blocks record the states, command, disturbance, and total force. This wiring implements $F="sat"(-K z)+d$.

#pagebreak()

#figure(image("nonlinear_plant_diagram.png", width: 100%),
  caption: [Nonlinear equations and four integrators retained from Project 1.])

Inside the preceding feedback loop, the acceleration function from Appendix B drives two integrator chains. The State order block receives $(theta,dot(theta),dot(x),x)$ from top to bottom and rearranges them internally into $(x,dot(x),theta,dot(theta))$ for the gain. The display order therefore follows the diagram, while the vector sent to the controller follows the design matrices.

#pagebreak()
#set page(flipped: false, margin: 1in)

= References

#bibliography("references.bib", title: none, style: "ieee")
