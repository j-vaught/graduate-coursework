#import "@preview/lilaq:0.6.0" as lq

#let plots = json("plot_data.json")
#let stats = json("metrics.json")
#let model_tests = json("model_comparisons.json")
#let ctrl = json("controller_studies.json")
#let dist = json("disturbance_studies.json")
#let detail = json("appendix_d_studies.json")
#let fmt(value, digits: 2) = str(calc.round(value, digits: digits))
#let colors = (rgb("#3F90DA"), rgb("#FFA90E"), rgb("#BD1F01"), rgb("#832DB6"), rgb("#A96B59"), rgb("#717581"))
#let sweep(runs, field, ylabel, limit, panel, height: 1.05in, ylim: auto, yscale: "linear", failed-from: 99, with-legend: false, legend-position: top + right, data-size: none) = {
  set text(size: if height > 2in { 10pt } else { 8pt })
  lq.diagram(
    width: if data-size == none { 100% } else { data-size.first() },
    height: if data-size == none { 0% + height } else { data-size.last() }, title: panel,
    xlabel: [Time (s)], ylabel: ylabel, xlim: limit, ylim: ylim, yscale: yscale,
    xaxis: (ticks: if limit.last() == 30 { (0, 10, 20, 30) }
      else if limit.last() == 1 { (0, 0.2, 0.4, 0.6, 0.8, 1) } else if limit.last() == 10 { (0, 2, 4, 6, 8, 10) }
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
      else if limit.last() == 1 { (0, 0.2, 0.4, 0.6, 0.8, 1) } else if limit.last() == 10 { (0, 2, 4, 6, 8, 10) } else if limit.last() == 3 { (0, 1, 2, 3) }
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
#let dist-panel(runs, field, ylabel, panel, limit: (0, 30), size: (2.6in, 1in), labels: none, with-legend: false, color-offset: 0, held: true, legend-position: top + right, solid: false) = {
  set text(size: 8pt)
  lq.diagram(width: size.first(), height: size.last(), title: panel,
    xlabel: [Time (s)], ylabel: ylabel, xlim: limit,
    xaxis: (ticks: if limit.last() == 30 { (0, 10, 20, 30) } else if limit.last() == 1 { (0, 0.2, 0.4, 0.6, 0.8, 1) } else if limit.last() == 10 { (0, 2, 4, 6, 8, 10) } else if limit.last() == 3 { (0, 1, 2, 3) } else { (0, 0.5, 1, 1.5) }),
    legend: if with-legend { (position: legend-position, radius: 0pt) } else { none },
    ..runs.enumerate().map(pair => {
      let (i, run) = pair
      let indices = run.time_s.enumerate().filter(pair => pair.last() <= limit.last()).map(pair => pair.first())
      lq.plot(indices.map(j => run.time_s.at(j)), indices.map(j => run.at(field).at(j)),
        mark: none, color: colors.at(i + color-offset),
        label: if labels == none { [#run.label] } else { labels.at(i) },
        step: if held and run.label == "Held" { end } else { none },
        stroke: (thickness: 0.9pt, dash: if solid or i + color-offset == 0 { "solid" } else if i + color-offset == 1 { "dashed" } else if i + color-offset == 2 { "dotted" } else { "dash-dotted" }))
    }),
  )
}

#let dplot(runs, field, ylabel, title, xfield: "time_s", limit: (0, 30), ylim: auto, size: (2.6in, 1.6in), labels: none, legend: false) = {
  set text(size: 9.5pt)
  lq.diagram(width: size.first(), height: size.last(), title: title,
    xlabel: if xfield == "time_s" { [Time (s)] } else if xfield == "sigma_s" { [Gaussian width (s)] } else if xfield == "bound_N" { [Force bound (N)] } else { [Initial angle (deg)] },
    ylabel: ylabel, xlim: limit, ylim: ylim,
    xaxis: (ticks: if xfield == "sigma_s" { (0.05, 0.1, 0.2) } else if xfield == "bound_N" { (2.5, 5, 7.5, 10) } else if xfield == "initial_angle_deg" { (20, 22, 24, 26, 28, 30) } else if limit.last() == 6 { (0, 1, 2, 3, 4, 5, 6) } else if limit.last() == 10 { (0, 2, 4, 6, 8, 10) } else { (0, 5, 10, 15, 20, 25, 30) }),
    legend: if legend { (position: top + right, radius: 0pt) } else { none },
    ..runs.enumerate().map(pair => {
      let (i, run) = pair
      let indices = run.at(xfield).enumerate().filter(p => p.last() >= limit.first() and p.last() <= limit.last() and run.at(field).at(p.first()) != none).map(p => p.first())
      lq.plot(indices.map(j => run.at(xfield).at(j)), indices.map(j => run.at(field).at(j)),
        mark: if xfield == "time_s" { none } else { "s" }, color: colors.at(i),
        label: if labels == none { none } else { labels.at(i) },
        step: if field == "force_N" and i == 0 { end } else { none }, stroke: 1.2pt)
    }),
  )
}
#let dwidth(field) = (2.5, 5, 7.5, 10).map(bound => {
  let rows = detail.width_summary.filter(r => r.bound_N == bound)
  (sigma_s: rows.map(r => r.sigma_s), values: rows.map(r => r.at(field)))
})
#let dseed(field) = (1, 2).map(mode => {
  let rows = dist.seed_summary.filter(r => r.mode == mode)
  (bound_N: rows.map(r => r.bound_N), values: rows.map(r => r.at(field)))
})

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

#align(center)[
  #text(size: 17pt, weight: "bold")[LQR Control of an Inverted Pendulum on a Cart]
]
#v(0.3em)

= OBJECTIVE.

Design and test a state-feedback controller that keeps an inverted pendulum upright after an initial perturbation and under random cart forces.

= METHODOLOGY.

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

With the controller fixed in Appendix B, we first test it using random forces that change every 0.1 s. Each new value is independent of the previous one, so the force can jump from near $-10$ N to near $+10$ N at a sample boundary. Such sudden jumps are useful for stressing the controller, but we also want to test a force that changes gradually, as a physical disturbance acting on a cart might. We therefore smooth the random force with Gaussian averaging and limit how quickly it can change.

To generate the original force, MATLAB draws independent uniform values $xi_k$ in $[-1,1]$. Multiplying by the force bound $a$ gives $r(t)=a xi_k$, held until the next draw. We use bounds of 2.5, 5, 7.5, and 10 N. The same seeded draws are scaled for each bound, so their signs and timing match.

Gaussian averaging replaces each force value with a weighted average of nearby values. Samples closest in time receive the most weight. For the smoothed force $s_i$, we use

$
w_j=exp(-(j h)^2/(2 sigma^2)), quad s_i=(sum_(j=-m)^m w_j r_(i+j))/(sum_(j=-m)^m w_j), quad m=ceil(3 sigma/h).
$

Here $sigma$ controls how much smoothing occurs. A larger value blends a longer stretch of the force record and produces gentler changes. We calculate the average every $h=0.002$ s, using samples up to $3 sigma$ before and after each point. At the ends, we extend the nearest force value. Because the average uses future samples, we generate the complete record before simulation.

Smoothing alone can still leave a rapid change. We therefore add a rate limiter @MathWorks2026RateLimiter that allows the force to move only a fixed amount per time step,

$
d_(i+1)=d_i+"clip"(s_(i+1)-d_i,-L h,L h).
$

The function $"clip"$ restricts each change to $plus.minus L h$, where $L$ is the allowed rate in N/s. We choose $sigma=0.1$ s and $L=50$ N/s. The limiter starts at zero for random trials and at $-10$ N for the reversal test.

We first check these operations with one clear example. In @fig-dist-reversal, the target switches from $-10$ to $+10$ N at 0.5 s. We compare the original jump, Gaussian averaging, rate limiting, and both operations together.

#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr), gutter: 8pt,
    dist-panel(dist.reversal, "force_N", [Force (N)], [(a) Extreme reversal], limit: (0, 1), size: (2.6in, 0.85in), with-legend: true, legend-position: top + left),
    dist-panel(dist.reversal.slice(1), "rate_N_s", [Rate (N/s)], [(b) Finite change rates], limit: (0, 1), size: (2.6in, 0.85in), color-offset: 1),
  )
], caption: [Force reversal at 0.5 s and the finite change rates of the three continuous profiles. The held force jumps instantaneously and has no finite rate at that instant.]) <fig-dist-reversal>

The Gaussian curve rounds the jump, while the limiter caps its slope at 50 N/s. A full 20 N change at that rate needs at least 0.4 s. @tab-dist-reversal measures time from the target jump to $+9$ N. Centered averaging begins changing earlier, so these times are not full transition durations.

#figure(table(columns: (1.6fr, 1fr, 1fr), inset: (x: 5pt, y: 2pt),
  align: (x, y) => if y == 0 or x == 0 { left } else { right },
  table.hline(stroke: 0.8pt), table.header([Profile], [Maximum rate (N/s)], [Time after jump to +9 N (s)]),
  table.hline(stroke: 0.5pt),
  ..dist.reversal.map(run => ([#run.label], [#optional-number(run.max_rate_N_s)], [#fmt(run.transition_95_s)])).flatten(),
  table.hline(stroke: 0.8pt),
), kind: table, caption: [Reversal timing and force-change rates with $sigma=0.1$ s and $L=50$ N/s. A dash denotes an undefined instantaneous rate.]) <tab-dist-reversal>

#pagebreak()

With the single jump explained, @fig-dist-random shows the same operations on the random-force sequence from seed 79202. Panel (a) shows the first 10 s, and panel (b) enlarges the first 3 s. The original force has sharp steps; Gaussian averaging rounds them, and the combined curve also obeys the rate limit.

#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr), gutter: 8pt,
    dist-panel(dist.random_profiles, "force_N", [Force (N)], [(a) First 10 s], limit: (0, 10), size: (2.6in, 0.75in), solid: true),
    dist-panel(dist.random_profiles, "force_N", [Force (N)], [(b) First 3 s], limit: (0, 3), size: (2.6in, 0.75in), with-legend: true, solid: true),
  )
], caption: [Held, Gaussian-averaged, rate-limited, and combined disturbances from the same 10 N target sequence, seed 79202.]) <fig-dist-random>

The curves stay within the original force bounds. However, smoothing removes short peaks and reduces root-mean-square (RMS) force, as @tab-dist-profiles shows for the full 30 s record. Thus, the shaped force is smoother and also weaker. In Simulink, we interpolate between its fine-grid samples; the original force remains held between draws.

#figure(table(columns: (1.3fr, 1fr, 1fr, 1.2fr), inset: (x: 5pt, y: 2pt),
  align: (x, y) => if y == 0 or x == 0 { left } else { right },
  table.hline(stroke: 0.8pt), table.header([Profile], [Peak (N)], [RMS (N)], [Maximum rate (N/s)]),
  table.hline(stroke: 0.5pt),
  ..dist.random_profiles.map(run => ([#run.label], [#fmt(run.peak_N)], [#fmt(run.rms_N)], [#optional-number(run.max_rate_N_s)])).flatten(),
  table.hline(stroke: 0.8pt),
), kind: table, caption: [Actual strength and slope of the four 30 s disturbance profiles.]) <tab-dist-profiles>

We next check how the settings change the force. @fig-dist-settings compares Gaussian widths of 0.05, 0.1, and 0.2 s without a limiter, then rate limits of 25, 50, and 100 N/s without averaging. Using the same 10 N target makes the effect of each setting visible.

#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr), gutter: 8pt,
    dist-panel(dist.sigma_sweep, "force_N", [Force (N)], [(a) Gaussian width], limit: (0, 3), size: (2.6in, 0.75in), labels: ([0.05 s], [0.1 s], [0.2 s]), with-legend: true, held: false),
    dist-panel(dist.rate_sweep, "force_N", [Force (N)], [(b) Maximum rate], limit: (0, 3), size: (2.6in, 0.75in), labels: ([25 N/s], [50 N/s], [100 N/s]), with-legend: true, held: false),
  )
], caption: [Sensitivity of the disturbance to Gaussian width and rate limit, tested separately.]) <fig-dist-settings>

Larger Gaussian widths blend away more short fluctuations. Lower rate limits produce slower ramps. @tab-dist-settings quantifies these changes over 30 s. We retain $sigma=0.1$ s and $L=50$ N/s for the controller comparisons.

#figure(table(columns: (1fr, 1fr, 1fr, 1fr, 1.2fr), inset: (x: 5pt, y: 2pt),
  align: (x, y) => if y == 0 or x == 0 { left } else { right },
  table.hline(stroke: 0.8pt), table.header([Operation], [Setting], [Peak (N)], [RMS (N)], [Maximum rate (N/s)]),
  table.hline(stroke: 0.5pt),
  ..dist.sigma_sweep.map(run => ([Gaussian], [#str(run.setting) s], [#fmt(run.peak_N)], [#fmt(run.rms_N)], [#fmt(run.max_rate_N_s)])).flatten(),
  ..dist.rate_sweep.map(run => ([Limiter], [#str(run.setting) N/s], [#fmt(run.peak_N)], [#fmt(run.rms_N)], [#fmt(run.max_rate_N_s)])).flatten(),
  table.hline(stroke: 0.8pt),
), kind: table, caption: [Separate shaping sweeps using the same 10 N random target.]) <tab-dist-settings>

Finally, 160 nonlinear trials compare held and combined disturbances across seeds 79202--79221 and four bounds. Each starts upright at rest and lasts 30 s. The ode45 settings are a 0.005 s maximum step, $10^(-7)$ relative tolerance, and $10^(-9)$ absolute tolerance. States are sampled every 0.02 s; balance requires $abs(theta)<90 degree$ throughout. Appendix D reports angle RMS, peak travel, saturation, and paired-seed results. Gaussian averaging changes temporal correlation and RMS strength, so these tests assess both effects together.

#pagebreak()

= Appendix D. Nonlinear controller performance and operating limits

Appendix B gives us a controller designed around the upright linear model, and Appendix C defines the forces used to test it. Here we apply that controller to the nonlinear Simulink plant and ask four questions. How far can the pendulum start from upright and still recover? What changes when it fails? How does Gaussian width affect the response? Does smoothing still change the response when the forces have equal RMS strength? The gain and actuator limit remain fixed throughout.

We first revisit the original release tests in @tab-release-metrics. Each starts with the cart and pendulum at rest, with no disturbance. The 20#sym.degree release recovers, while the 30#sym.degree release fails. Recovery is assessed over 30 s: the final angle and final-two-second angle RMS must be below 2#sym.degree. In the new tests, the pendulum must also stay within $plus.minus 90 degree$ throughout.

#let release_entries = ((initial_angle_deg: 5, metrics: stats.perturbation),) + stats.angle_stress
#figure(table(columns: (0.8fr, 1.2fr, 1.2fr, 1fr, 1fr), inset: (x: 5pt, y: 4pt),
  align: (x, y) => if y == 0 or x == 4 { left } else { right },
  table.hline(stroke: 0.8pt),
  table.header([Initial angle (deg)], [Peak cart displacement (m)], [Final 2 s RMS (deg)], [Saturation (%)], [Recovered]),
  table.hline(stroke: 0.5pt),
  ..release_entries.map(entry => ([#str(entry.initial_angle_deg)], [#fmt(entry.metrics.peak_cart_position_m, digits: 3)],
    [#fmt(entry.metrics.final_2s_rms_angle_deg, digits: 4)], [#fmt(100*entry.metrics.saturation_fraction)],
    [#if entry.metrics.recovered { "Yes" } else { "No" }])).flatten(),
  table.hline(stroke: 0.8pt),
), kind: table, caption: [Original release tests. Failed-case travel includes motion after loss of balance on the model's unlimited track.]) <tab-release-metrics>

To locate the transition more closely, we test every degree from 20#sym.degree to 30#sym.degree, then test the intervening interval in 0.1#sym.degree increments. @fig-release-boundary shows the travel and saturation time for each release. Failed-case metrics stop at the first sampled 90#sym.degree crossing, so falling motion does not dominate the vertical scale. Successful-case metrics use the full 30 s.

#let release_curves = (true, false).map(success => {
  let rows = detail.release.filter(r => r.recovered == success)
  (initial_angle_deg: rows.map(r => r.initial_angle_deg),
    travel: rows.map(r => r.peak_x_before_fall_m),
    saturation: rows.map(r => r.saturation_before_fall_s))
})
#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr), gutter: 24pt,
    dplot(release_curves, "travel", [Peak cart travel (m)], [(a) Cart travel], xfield: "initial_angle_deg", limit: (20, 30), labels: ([Recovered], [Failed]), legend: true),
    dplot(release_curves, "saturation", [Time at limit (s)], [(b) Actuator saturation], xfield: "initial_angle_deg", limit: (20, 30)),
  )
], caption: [Refined release sweep. Metrics for failed trials cover only the motion up to loss of balance.]) <fig-release-boundary>

The largest tested release that recovers is 20.2#sym.degree; the next release, 20.3#sym.degree, loses balance. The recovery-to-failure boundary therefore lies between these two tested angles for the stated initial conditions. Recovery at 20.2#sym.degree still requires 3.18 m of peak cart travel and 1.75 s at the force limit, so balancing alone does not establish feasibility on a short track.

All new trials use ode45 with a 0.005 s maximum step, $10^(-7)$ relative tolerance, and $10^(-9)$ absolute tolerance. Metrics use a 0.02 s state grid. These tests hold the controller and plant parameters fixed, so their conclusions describe the tested releases and disturbance profiles for this model.

#pagebreak()

The refined sweep identifies two neighboring releases with different outcomes. We now compare their histories in @fig-release-detail to see how those outcomes develop. Both use the same controller and 10 N actuator limit; only the starting angle changes. The failed trace ends when the pendulum first reaches 90#sym.degree.

#let boundary_labels = detail.boundary_angles_deg.map(a => [#fmt(a, digits: 1)#sym.degree])
#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr), gutter: 24pt,
    dplot(detail.boundary_runs, "theta_deg", [Angle (deg)], [(a) Pendulum angle], limit: (0, 6), labels: boundary_labels, legend: true, size: (2.6in, 1.8in)),
    dplot(detail.boundary_runs, "x_m", [Cart position (m)], [(b) Cart motion], limit: (0, 6), size: (2.6in, 1.8in)),
  )
], caption: [Near-boundary releases. One recovers; the next tested release loses balance.]) <fig-release-detail>

The cart must move to bring the pendulum back toward upright. That motion is governed by the force the actuator can deliver. The controller may request more than 10 N, but the plant receives only the clipped value. The following comparison shows the requested and applied forces separately for each release.

#let boundary_force = detail.boundary_runs.map(r => (
  (time_s: r.time_s, force: r.requested_N),
  (time_s: r.time_s, force: r.applied_N),
))
#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr), gutter: 24pt,
    dplot(boundary_force.first(), "force", [Actuator force (N)], [(a) #boundary_labels.first() release], limit: (0, 6), labels: ([Requested], [Applied]), legend: true, size: (2.6in, 1.8in)),
    dplot(boundary_force.last(), "force", [Actuator force (N)], [(b) #boundary_labels.last() release], limit: (0, 6), labels: ([Requested], [Applied]), legend: true, size: (2.6in, 1.8in)),
  )
], caption: [Requested and applied force near the recovery boundary. The applied force is limited to $plus.minus 10$ N.]) <fig-release-force-detail>

For the 20.2#sym.degree release, the controller eventually brings its requested force back within the actuator range and the pendulum recovers. At 20.3#sym.degree, the pendulum reaches 90#sym.degree after 3.22 s. By that point, the requested force reaches approximately 276 N in magnitude, while the applied force remains limited to 10 N. The large gap shows why the actuator cannot deliver the correction requested by this gain. Saturation also occurs in the successful trial; its presence alone does not determine the outcome.

#pagebreak()

Having examined releases, we next start the system upright and apply random forces. @fig-dist-controller compares the original held force with Gaussian averaging followed by rate limiting. Both use the same 5 N target and seed 79202. The shaped version uses $sigma=0.1$ s and $L=50$ N/s. Every disturbance trial lasts 30 s; balance requires $abs(theta)<90 degree$ throughout.

#figure([
  #show: lq.layout
  #stack(spacing: 14pt,
    dplot(dist.controller_runs, "theta_deg", [Angle (deg)], [(a) Pendulum angle], labels: ([Held], [Gaussian + limiter]), legend: true, size: (6in, 1.25in)),
    dplot(dist.controller_runs, "x_m", [Cart position (m)], [(b) Cart position], size: (6in, 1.25in)),
    dplot(dist.controller_runs, "applied_N", [Actuator force (N)], [(c) Applied actuator force], size: (6in, 1.25in)),
  )
], caption: [Nonlinear responses to held and shaped 5 N disturbances, seed 79202.]) <fig-dist-controller>

At this bound, both trials maintain balance. Shaping reduces force RMS from 2.98 to 1.61 N, while angle RMS falls from 1.39 to 1.31#sym.degree. The cart travels nearly the same distance. @tab-dist-nominal extends this comparison to the other bounds. Its large failed-case values include motion after the pendulum falls.

#pagebreak()

#figure([
  #set text(size: 9.5pt)
  #table(columns: (0.6fr, 1fr, 0.8fr, 1fr, 1fr, 1fr, 0.8fr), inset: (x: 4pt, y: 3pt),
    align: (x, y) => if y == 0 or x == 1 or x == 2 { left } else { right },
    table.hline(stroke: 0.8pt),
    table.header([Bound (N)], [Profile], [Balanced], [Force RMS (N)], [Angle RMS (deg)], [Peak cart (m)], [Saturated (%)]) ,
    table.hline(stroke: 0.5pt),
    ..dist.seed_summary.map(pair => dist.nominal.filter(run => run.bound_N == pair.bound_N and run.mode == pair.mode).first()).map(run => ([#fmt(run.bound_N, digits: 1)], [#if run.mode == 1 { "Held" } else { "Shaped" }],
      [#if run.balanced { "Yes" } else { "No" }], [#fmt(run.force_rms_N)], [#fmt(run.rms_angle_deg)],
      [#fmt(run.peak_x_m, digits: 3)], [#fmt(run.saturation_percent)])).flatten(),
    table.hline(stroke: 0.8pt),
  )
], kind: table, caption: [Held and shaped disturbance results for seed 79202.]) <tab-dist-nominal>

A single random sequence does not show how often a given bound causes failure. We therefore repeat the held-versus-shaped comparison for seeds 79202--79221. @fig-dist-seeds shows the number of trials that maintain balance and their median angle RMS. This separates the balance outcome from the amount of motion in successful trials.

#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr), gutter: 24pt,
    dplot(dseed("balanced_count"), "values", [Balanced trials / 20], [(a) Balance across seeds], xfield: "bound_N", limit: (2.5, 10), ylim: (15, 20.5), labels: ([Held], [Gaussian + limiter]), legend: true),
    dplot(dseed("median_rms_angle_deg_balanced"), "values", [Median angle RMS (deg)], [(b) Balanced-trial response], xfield: "bound_N", limit: (2.5, 10)),
  )
], caption: [Twenty-seed comparison of held and shaped disturbances. Angle medians include balanced trials only.]) <fig-dist-seeds>

Both profiles maintain balance in every tested seed through 7.5 N. At 10 N, the held version succeeds in 18 of 20 trials and the shaped version in 19 of 20. Seed 79202 fails with both versions. @tab-dist-seeds also gives the actual force strength and cart travel, which help interpret the response differences.

#figure([
  #set text(size: 10pt)
  #table(columns: (0.6fr, 1fr, 0.9fr, 1fr, 1fr, 1fr), inset: (x: 4pt, y: 4pt),
    align: (x, y) => if y == 0 or x == 1 { left } else { right },
    table.hline(stroke: 0.8pt),
    table.header([Bound (N)], [Profile], [Balanced / 20], [Median force RMS (N)], [Median angle RMS (deg)], [Median peak cart (m)]),
    table.hline(stroke: 0.5pt),
    ..dist.seed_summary.map(run => ([#fmt(run.bound_N, digits: 1)], [#if run.mode == 1 { "Held" } else { "Shaped" }],
      [#str(run.balanced_count)], [#fmt(run.median_force_rms_N)],
      [#optional-number(run.median_rms_angle_deg_balanced)], [#optional-number(run.median_peak_x_m_balanced, digits: 3)])).flatten(),
    table.hline(stroke: 0.8pt),
  )
], kind: table, caption: [Results across seeds 79202--79221. Response medians include balanced trials only.]) <tab-dist-seeds>

#pagebreak()

The nominal velocity histories below complete the four-state record used by the controller. After a release, the velocities decay toward rest. Under an ongoing disturbance, they continue to fluctuate even when the pendulum remains balanced.

#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr), gutter: 24pt,
    dplot((plots.perturbation, plots.random_test), "x_dot_m_s", [Cart velocity (m/s)], [(a) Cart velocity], labels: ([5° release], [2.5 N held force]), legend: true),
    dplot((plots.perturbation, plots.random_test), "theta_dot_deg_s", [Angular velocity (deg/s)], [(b) Pendulum angular velocity]),
  )
], caption: [Nominal velocities from the original release and held-force tests.]) <fig-dist-velocities>

The corresponding original held-force actuator histories below show how increasing the force bound changes demand. At 10 N for seed 79202, loss of balance leads to sustained actuator saturation. The successful lower-bound trials continue correcting the random force without remaining at the limit.

#figure([
  #sweep(plots.force_runs, "u_N", [Actuator force (N)], (0, 30), [Original held-force actuator histories],
    height: 1.8in, ylim: (-10.5, 10.5), failed-from: 3, with-legend: true)
], caption: [Original actuator histories for the four held-force bounds. The failed 10 N case is dashed.]) <fig-dist-original-actuator>

These velocity and force histories support the balance metrics above. They also show that remaining upright under a continuing disturbance does not mean the cart and pendulum have come to rest.

#pagebreak()

The preceding comparison uses one Gaussian width. Appendix C shows that changing this width changes the force waveform; here we test how it changes the controller's response. For each $sigma$ of 0.05, 0.1, and 0.2 s, we run all four force bounds and all 20 seeds with the same 50 N/s rate limit. This gives 240 nonlinear trials, including a repeated baseline width for direct consistency checks.

#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr), gutter: 24pt,
    dplot(dwidth("median_angle_rms_deg"), "values", [Median angle RMS (deg)], [(a) Pendulum response], xfield: "sigma_s", limit: (0.05, 0.2), labels: ([2.5 N], [5 N], [7.5 N], [10 N]), legend: true),
    dplot(dwidth("median_peak_x_m"), "values", [Median peak cart travel (m)], [(b) Cart travel], xfield: "sigma_s", limit: (0.05, 0.2)),
    dplot(dwidth("balanced_count"), "values", [Balanced trials / 20], [(c) Balance across seeds], xfield: "sigma_s", limit: (0.05, 0.2), ylim: (15, 20.5)),
    dplot(dwidth("median_force_rms_N"), "values", [Median force RMS (N)], [(d) Actual disturbance strength], xfield: "sigma_s", limit: (0.05, 0.2)),
  )
], caption: [Controller performance versus Gaussian width with a 50 N/s rate limit. Response medians include balanced trials only.]) <fig-dist-width-response>

Increasing the Gaussian width reduces median angle motion and cart travel at every tested bound. At 10 N, widths of 0.05 and 0.1 s maintain balance in 19 of 20 seeds, while 0.2 s maintains balance in all 20. However, median force RMS also falls from 3.72 to 2.26 N across that sweep. These results describe the combined effect of gentler variation and lower force strength. The next comparison holds RMS strength fixed.

#pagebreak()

@tab-dist-width-response collects the results behind the width comparison. All lower-bound trials remain balanced at every tested width. The differences are most visible at 10 N, where the widest average removes enough rapid variation and force strength to keep all tested seeds balanced. Angle and travel medians use successful trials only; the balance count separately records failures.

#figure([
  #set text(size: 9.5pt)
  #table(columns: (0.65fr, 0.65fr, 0.8fr, 1fr, 1fr, 1fr), inset: (x: 4pt, y: 3pt),
    table.hline(stroke: 0.8pt), table.header([Width (s)], [Bound (N)], [Balanced / 20], [Median force RMS (N)], [Median angle RMS (deg)], [Median peak cart (m)]), table.hline(stroke: 0.5pt),
    ..detail.width_summary.map(r => ([#fmt(r.sigma_s)], [#fmt(r.bound_N, digits: 1)], [#str(r.balanced_count)], [#fmt(r.median_force_rms_N)], [#fmt(r.median_angle_rms_deg)], [#fmt(r.median_peak_x_m, digits: 3)])).flatten(),
    table.hline(stroke: 0.8pt),
  )
], kind: table, caption: [Gaussian-width results across the same 20 seeds at each force bound.]) <tab-dist-width-response>

The width comparison motivates one final test. Because wider averaging reduces force strength, the preceding tests combine two effects. We now separate them by making the held and shaped forces have the same 2 N RMS over 30 s. For each seed, we generate both versions from the same 10 N target, then scale each downward to the common RMS level. Downward scaling preserves the 10 N amplitude bound and the shaped profile's 50 N/s rate limit. It also avoids clipping after scaling, which would change the waveform.

For these equal-RMS trials, the largest applied disturbance peaks are 3.59 N for held inputs and 6.06 N for shaped inputs. The shaped-force rate never exceeds 38.14 N/s. The force history below illustrates how equal overall RMS can coexist with different peaks and timing.

#figure([
  #show: lq.layout
  #dplot(detail.matched_runs, "force_N", [Disturbance force (N)], [Equal-RMS input forces, seed 79202], limit: (0, 10), labels: ([Held], [Gaussian + limiter]), legend: true, size: (6in, 1.8in))
], caption: [Held and shaped forces scaled to 2 N RMS over 30 s. The first 10 s are shown.]) <fig-dist-matched-input>

#pagebreak()

With the input strength matched, @fig-dist-matched compares the resulting angle motion and cart travel for each seed. The dashed line marks equal response; points above it indicate greater motion under the shaped force.

#let matched_pairs = detail.seeds.map(seed => {
  let held = detail.matched_trials.filter(r => r.seed == seed and r.mode == 1).first()
  let shaped = detail.matched_trials.filter(r => r.seed == seed and r.mode == 2).first()
  (held: held, shaped: shaped)
})
#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr), gutter: 24pt,
    lq.diagram(width: 2.6in, height: 1.8in, title: [(a) Paired angle response], xlim: (0.6, 2), ylim: (0.6, 2), xlabel: [Held-force angle RMS (deg)], ylabel: [Shaped-force angle RMS (deg)],
      lq.plot(matched_pairs.map(r => r.held.rms_angle_deg), matched_pairs.map(r => r.shaped.rms_angle_deg), mark: "s", stroke: none, color: colors.first()),
      lq.plot((0.6, 2), (0.6, 2), mark: none, color: black, stroke: (thickness: 0.8pt, dash: "dashed")),
    ),
    lq.diagram(width: 2.6in, height: 1.8in, title: [(b) Paired cart travel], xlim: (0.15, 0.7), ylim: (0.15, 0.7), xlabel: [Held-force peak travel (m)], ylabel: [Shaped-force peak travel (m)],
      lq.plot(matched_pairs.map(r => r.held.peak_x_m), matched_pairs.map(r => r.shaped.peak_x_m), mark: "s", stroke: none, color: colors.first()),
      lq.plot((0.15, 0.7), (0.15, 0.7), mark: none, color: black, stroke: (thickness: 0.8pt, dash: "dashed")),
    ),
  )
], caption: [Equal-RMS comparisons. Each point pairs the same seed; points above the dashed equality line indicate a larger response to the shaped force.]) <fig-dist-matched>

At equal RMS strength, the shaped force produces a larger response. Median angle RMS increases from 0.89 to 1.57#sym.degree, and median peak cart travel increases from 0.291 to 0.537 m. All 20 seeds remain balanced with both profiles, and no trial reaches the actuator limit. The shaped force varies over longer intervals and has different peaks, so equal RMS does not imply equal effect on the cart and pendulum. Gaussian smoothing therefore cannot be described as universally improving controller performance.

#figure([
  #set text(size: 10pt)
  #table(columns: (1fr, 0.75fr, 1fr, 1fr, 1fr, 1fr), inset: (x: 4pt, y: 4pt),
    table.hline(stroke: 0.8pt), table.header([Profile], [Balanced / 20], [Median force RMS (N)], [Median angle RMS (deg)], [Median peak cart (m)], [Median saturation (%)]) , table.hline(stroke: 0.5pt),
    ..detail.matched_summary.map(r => ([#if r.mode == 1 { "Held" } else { "Shaped" }], [#str(r.balanced_count)], [#fmt(r.median_force_rms_N)], [#fmt(r.median_angle_rms_deg)], [#fmt(r.median_peak_x_m, digits: 3)], [#fmt(r.median_saturation_percent)])).flatten(),
    table.hline(stroke: 0.8pt),
  )
], kind: table, caption: [Equal-RMS results at 2 N across seeds 79202--79221.]) <tab-dist-matched>

To make the paired statistics easier to interpret, the following histories show seed 79202 at the same RMS strength. They reveal when the shaped force produces a different angle or actuator response, even though its overall RMS is equal.

#figure([
  #show: lq.layout
  #grid(columns: (1fr, 1fr), gutter: 24pt,
    dplot(detail.matched_runs, "theta_deg", [Angle (deg)], [(a) Pendulum angle], limit: (0, 10), labels: ([Held], [Gaussian + limiter]), legend: true, size: (2.6in, 1.5in)),
    dplot(detail.matched_runs, "applied_N", [Actuator force (N)], [(b) Actuator response], limit: (0, 10), size: (2.6in, 1.5in)),
  )
], caption: [Example equal-RMS controller responses for seed 79202, showing the first 10 s.]) <fig-dist-matched-history>


#pagebreak()
#set page(flipped: false, margin: 1in)

= Appendix E. Simulink feedback loop and nonlinear plant

#figure(image("controlled_model_diagram.png", width: 100%),
  caption: [Complete feedback loop with state feedback, actuator saturation, an external disturbance, and signal logging.])

The gain from Appendix B acts on all four simulated states. The actuator block limits the command, then the sum adds the disturbance before the total force reaches the cart. Output blocks record the states, command, disturbance, and total force. This wiring implements $F="sat"(-K z)+d$.

#figure(image("nonlinear_plant_diagram.png", width: 100%),
  caption: [Nonlinear equations and four integrators retained from Project 1.])

Inside the preceding feedback loop, the acceleration function from Appendix B drives two integrator chains. The State order block receives $(theta,dot(theta),dot(x),x)$ from top to bottom and rearranges them internally into $(x,dot(x),theta,dot(theta))$ for the gain. The display order therefore follows the diagram, while the vector sent to the controller follows the design matrices.

#pagebreak()
#set page(flipped: false, margin: 1in)

= References

#bibliography("references.bib", title: none, style: "ieee")
