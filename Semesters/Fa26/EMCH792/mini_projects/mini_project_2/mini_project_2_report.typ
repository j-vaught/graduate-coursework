#import "@preview/lilaq:0.6.0" as lq

#let plots = json("plot_data.json")
#let stats = json("metrics.json")
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
  size: 11pt, lang: "en")
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


  MATLAB calculates $u=-K z$ and confirms that all poles of $A-B K$ have negative real parts. We also simulate the linear closed loop and verify that its states return to zero. We then connect this controller to the nonlinear Simulink model in Appendix C. The actuator limits $u$ to $plus.minus 10$ N, and a separate disturbance $d$ is added afterward, so the cart receives $F=u+d$.

  To test the controller, we run two categories of 30 s simulations. First, we release the pendulum from 5, 10, 20, 30, 45, and 60#sym.degree to test the linearization and actuator limits. Second, we start upright and apply random cart forces with bounds of $plus.minus 2.5$, 5, 7.5, and 10 N. Each force is an independent uniform draw held for 0.1 s. The same seeded sequence is scaled for each bound. Appendix D explains this generation method and its scope. Appendix E gives the full metrics and actuator histories.
= RESULTS.

For the initial-angle tests, @fig-releases(a,b) shows cart position over 30 s and a 0--10 s detail. Panels (c,d) show the pendulum angles. The 5, 10, and 20#sym.degree cases recover; the tested 30, 45, and 60#sym.degree cases fail. The transition from successful recovery to failure to recover therefore lies between the tested 20#sym.degree and 30#sym.degree releases.

For the random-force tests, @fig-forces(a,b) shows cart position over 30 s and 0--3 s. Panels (c,d) show the angles, and panels (e,f) show the applied forces. The controller maintains balance at the tested 2.5, 5, and 7.5 N bounds, but loses balance at 10 N. At 2.5 N, the RMS angle is #fmt(stats.random_test.rms_angle_deg)#sym.degree and the peak is #fmt(stats.random_test.peak_angle_deg)#sym.degree.

#pagebreak()

#figure([
  #show: lq.layout
  #let panel-size = (2.6in, 0.95in)
  #grid(columns: (1fr, 1fr), gutter: 5pt,
    sweep(plots.angle_runs, "x_m", [Cart position (m)], (0, 30), [(a) Full cart response], data-size: panel-size, yscale: lq.scale.symlog(threshold: 1), failed-from: 3, with-legend: true, legend-position: top + right),
    sweep(plots.angle_runs, "x_m", [Cart position (m)], (0, 10), [(b) Cart detail], data-size: panel-size, ylim: (-0.15, 3.2), failed-from: 3),
    sweep(plots.angle_runs, "theta_deg", [Pendulum angle (deg)], (0, 30), [(c) Full angle response], data-size: panel-size, failed-from: 3),
    sweep(plots.angle_runs, "theta_deg", [Pendulum angle (deg)], (0, 10), [(d) Angle detail], data-size: panel-size, ylim: (-20, 400), failed-from: 3),
  )
], caption: [Initial-angle sweep. Dashed traces indicate initial angles where the controller failed to stabilize. Panel (a) uses a symmetric log scale, linear within $plus.minus 1$ m.]) <fig-releases>

= DISCUSSION.

The smaller tested inputs recover or remain balanced. Failed releases stay at the actuator limit, and the 10 N disturbance also causes sustained saturation. Even successful recovery at 20#sym.degree needs #fmt(stats.angle_stress.at(1).metrics.peak_cart_position_m) m of cart travel, so a physical track could constrain performance. The sweeps identify an operating range for this gain and force limit. The random-force result applies to the recorded sequence described in Appendix D.

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
], caption: [Random-force sweep. Every bound uses the same sequence of force draws; the 10 N case is dashed. Panels (a,c) use symmetric log scales, linear within $plus.minus 1$ m and $plus.minus 10 degree$, respectively.]) <fig-forces>

#pagebreak()
#set page(margin: 1in)
#set text(size: 10.5pt)
#show figure.caption: set text(size: 9.5pt)

= Appendix A. Nonlinear equations and upright linearization

The report begins with the nonlinear model inherited from Project 1. The cart moves in the positive $x$ direction under positive force $F$, and $theta=0$ is upright. The rod is massless, its end mass is $m$, and its pivot has viscous damping $c_theta$. Adding cart force gives the coupled equations

$
(M+m) dot.double(x) + m ell cos(theta) dot.double(theta)
- m ell sin(theta) dot(theta)^2 = F,
$
$
m ell cos(theta) dot.double(x) + m ell^2 dot.double(theta)
+ c_theta dot(theta) - m g ell sin(theta) = 0.
$

Because the accelerations are coupled, the MATLAB Function solves them together using

$
mat(M+m, m ell cos(theta); m ell cos(theta), m ell^2)
mat(dot.double(x); dot.double(theta))
= mat(F + m ell sin(theta) dot(theta)^2; m g ell sin(theta) - c_theta dot(theta)).
$

Each acceleration then passes through two integrators to obtain velocity and position. The resulting state vector is $z=(x,dot(x),theta,dot(theta))^T$. The model parameters are

#table(columns: (1fr, 2fr, 1.4fr), inset: 6pt,
  [Parameter], [Meaning], [Value],
  [$M$], [Cart mass], [2.0 kg],
  [$m$], [Pendulum point mass], [0.5 kg],
  [$ell$], [Rod length], [1.0 m],
  [$c_theta$], [Pivot damping], [0.01 N m s/rad],
  [$g$], [Gravity], [9.81 m/s²],
)

The track has no friction or end stops, and all four states are available directly to the feedback block. These assumptions allow the controller's angle response, cart motion, and force limit to be evaluated separately.

#pagebreak()

== Linearization and controllability

To obtain the design model from the preceding equations, we expand about $z=0$ and $F=0$. First, use $sin(theta) approx theta$ and $cos(theta) approx 1$. Second, remove products of perturbations, including $theta dot(theta)^2$. The first-order equations are

$
(M+m) dot.double(x) + m ell dot.double(theta) = F,
quad m ell dot.double(x) + m ell^2 dot.double(theta) + c_theta dot(theta) - m g ell theta = 0.
$

Eliminating one acceleration at a time gives

$
dot.double(x) = F/M - (m g)/M theta + c_theta/(M ell) dot(theta),
$
$
dot.double(theta) = -F/(M ell) + ((M+m)g)/(M ell) theta
- (c_theta(M+m))/(M m ell^2) dot(theta).
$

Using the same state order as the nonlinear model, $dot(z)=A z+B F$ with

$
A = mat(0,1,0,0; 0,0,-2.4525,0.005; 0,0,0,1; 0,0,12.2625,-0.025),
quad B = mat(0;0.5;0;-0.5).
$

Before using these matrices for control, MATLAB forms $cal(C)=[B,A B,A^2 B,A^3 B]$ and finds $"rank"(cal(C))=4$. Since the state dimension is four, the model is controllable.

The comparison in Figure 1 uses identical initial states, $z(0)=(0,0,5 pi/180,0)^T$, and zero cart force. MATLAB integrates both sets of equations for 0.5 s with tight tolerances. The largest position difference is #fmt(1000*stats.model_comparison.max_x_difference_m, digits: 3) mm, and the largest angle difference is #fmt(stats.model_comparison.max_angle_difference_deg, digits: 4)#sym.degree. This checks agreement near upright. The longer release sweep then tests the controller when larger angles and actuator saturation weaken that approximation.

#pagebreak()

= Appendix B. LQR design and essential MATLAB functions

With the controllable model from Appendix A, we choose a gain that minimizes the accumulated state error and force cost,

$
J = integral_0^infinity (4x^2 + 2dot(x)^2 + 300theta^2 + 10dot(theta)^2 + 0.5u^2) dif t.
$

Here $x$ is in metres, $theta$ is in radians, and $u$ is in newtons. The state-error matrix is $Q="diag"(4,2,300,10)$, and the input penalty is $R=0.5$. These weights were selected to prioritize upright balance, retain a penalty on cart displacement, damp velocity, and discourage excessive force. They are tuning choices, rather than coefficients derived from the mechanical equations.

MATLAB solves the algebraic Riccati equation through its LQR routine. It returns

$
u=-K z, quad K=(-2.8284,-6.3204,-86.8641,-25.2346).
$

The poles of $A-B K$ are $-0.699 plus.minus 0.548i$ and $-4.042 plus.minus 1.125i$. Their negative real parts establish stability of the linear closed loop. To verify the corresponding time response, we also simulate it from a 5#sym.degree release with no disturbance. Its final state norm after 30 s is approximately $#fmt(stats.design.linear_final_state_norm * 1e10, digits: 2) times 10^(-10)$.

#figure([
  #set text(size: 10pt)
  #lq.diagram(width: 100%, height: 0% + 2.8in,
    xlabel: [Time (s)], ylabel: [Pendulum angle (deg)], xlim: (0, 30),
    lq.plot(plots.linear_closed_loop.time_s, plots.linear_closed_loop.theta_deg,
      mark: none, color: colors.first(), stroke: (thickness: 1.2pt)),
  )
], caption: [Linear closed-loop response used to verify the designed gain.])

The nonlinear model in Appendix C uses this same gain, with its command limited to $plus.minus 10$ N. The nonlinear sweeps therefore evaluate how the linear design performs when the exact equations and force limit are restored.

#pagebreak()

== Controller and acceleration functions

The preceding design is implemented by the following function. It constructs the matrices, checks controllability, computes the gain, and checks the closed-loop poles.

#show raw.where(block: true): it => block(width: 100%, fill: rgb("#ECECEC"),
  stroke: 0.5pt + rgb("#A2A2A2"), inset: 6pt)[
  #set text(font: "DejaVu Sans Mono", size: 7.3pt)
  #it
]
#raw(read("design_controller.m"), lang: "matlab", block: true)

The nonlinear Simulink block then uses the function below to calculate the two accelerations. Its eighth input is the total cart force.

#raw(read("controlled_accelerations.m"), lang: "matlab", block: true)

The separate model builder and experiment script remain runnable files alongside the report. The control methods are documented in the following sources.

#bibliography("references.bib", title: none, style: "ieee")

#pagebreak()
#set page(flipped: true, margin: 1in)

= Appendix C. Simulink feedback loop and nonlinear plant

#figure(image("controlled_model_diagram.png", width: 100%),
  caption: [Complete feedback loop. The disturbance enters above the circular sum, and the limited actuator command returns below the loop.])

The gain from Appendix B acts on all four simulated states. The actuator block limits the command, then the sum adds the disturbance before the total force reaches the cart. Output blocks record the states, command, disturbance, and total force. This wiring implements $F="sat"(-K z)+d$.

#pagebreak()

== Nonlinear plant subsystem

#figure(image("nonlinear_plant_diagram.png", width: 100%),
  caption: [Nonlinear equations and four integrators retained from Project 1.])

Inside the preceding feedback loop, the acceleration function from Appendix B drives two integrator chains. The State order block receives $(theta,dot(theta),dot(x),x)$ from top to bottom and rearranges them internally into $(x,dot(x),theta,dot(theta))$ for the gain. The display order therefore follows the diagram, while the vector sent to the controller follows the design matrices.

#pagebreak()
#set page(flipped: false, margin: 1in)

= Appendix D. Random-force generation and measurement protocol

The feedback loop in Appendix C receives a separate external force. To generate it, MATLAB draws independent samples $xi_k$ uniformly in $[-1,1]$ and holds each value for $Delta t=0.1$ s. For force bound $a$, the applied disturbance is

$
d_a(t)=a xi_k, quad k Delta t <= t < (k+1) Delta t.
$

We use $a=2.5$, 5, 7.5, and 10 N. The generator uses the Twister algorithm with seed 79202. Every bound uses the same $xi_k$ sequence, so the tests change force strength while retaining the timing and sign of each push. A sample beyond 30 s prevents the source block from needing to extrapolate at the final solver step. Interpolation is disabled, and the source holds its last value after the final sample.

This is one model of short, irregular pushes. Its theoretical mean is zero and its variance is $a^2/3$, although the finite sequence has its own sample mean. It does not model a persistent bias, correlated low-frequency force, isolated impact, or sensor noise. A different seed would produce a different trajectory. The results therefore compare the four strengths for this recorded sequence; they do not estimate a failure probability across random realizations.

Both test categories run for 30 s using ode45 with a 0.01 s maximum step. Release tests set the initial angle to 5, 10, 20, 30, 45, or 60#sym.degree, with all other initial states and the disturbance zero. Random-force tests start with every state zero. The gain and actuator limit stay fixed across all trials.

To compare the trials, the logged states are sampled on a uniform 0.02 s grid. Peak angle is $max_i abs(theta_i)$, and root-mean-square (RMS) angle is

$
theta_"RMS"=sqrt((1/N)sum_i theta_i^2).
$

Settling time is the first sampled time after which $abs(theta)$ stays within 1#sym.degree through the end of the run. This describes release recovery; under continuous forcing it depends on the particular later draws. Saturation fraction counts analysis samples with $abs(u)>=10$ N. For release tests, recovery requires the final angle magnitude and the RMS angle over the final two seconds to be below 2#sym.degree. For random-force tests, peak and RMS angle measure the continuing motion, and loss of upright balance is identified by leaving $plus.minus 90 degree$. Figures use every second analysis sample, while metrics use every sample. The forcing panels use the original 0.1 s values and display the actual held steps.

#pagebreak()

= Appendix E. Detailed release and disturbance results

The release tests defined in Appendix D produce the following metrics. The final-two-second RMS checks that a successful final angle is accompanied by sustained balance. The saturation percentage is measured on the analysis grid.

#let release_entries = ((initial_angle_deg: 5, metrics: stats.perturbation),) + stats.angle_stress
#table(columns: (0.8fr, 1.2fr, 1.2fr, 1fr, 1fr), inset: 5pt,
  [Initial angle (deg)], [Peak cart displacement (m)], [Final 2 s RMS (deg)], [Saturation (%)], [Recovered],
  ..release_entries.map(entry => (
    [#str(entry.initial_angle_deg)],
    [#fmt(entry.metrics.peak_cart_position_m, digits: 3)],
    [#fmt(entry.metrics.final_2s_rms_angle_deg, digits: 4)],
    [#fmt(100*entry.metrics.saturation_fraction)],
    [#if entry.metrics.recovered { "Yes" } else { "No" }],
  )).flatten(),
)

#figure([
  #sweep(plots.angle_runs, "u_N", [Actuator command (N)], (0, 30), [Release-test actuator commands],
    height: 3.3in, ylim: (-10.5, 10.5), failed-from: 3, with-legend: true)
], caption: [Force used in the initial-angle sweep. The three failed cases remain at the actuator limit.])

The tested 20#sym.degree case recovers but reaches #fmt(stats.angle_stress.at(1).metrics.peak_cart_position_m) m of displacement. The tested 30#sym.degree case fails, placing the transition somewhere between those two inputs for this controller. No trials between them were run. After failure, the unlimited-track model permits the cart to keep accelerating, and the angle records full rotations rather than being wrapped into a single revolution.

#pagebreak()

== Random-force metrics and actuator use

The force sweep measures continuing balance while the disturbance remains active. Its angle, travel, and actuator metrics are

#table(columns: (0.75fr, 1fr, 1fr, 1.15fr, 1.05fr, 0.8fr), inset: 5pt,
  [Bound (N)], [RMS angle (deg)], [Peak angle (deg)], [Peak cart displacement (m)], [Saturation (%)], [Peak command (N)],
  ..stats.force_stress.map(entry => (
    [#fmt(entry.amplitude_N, digits: 1)],
    [#fmt(entry.metrics.rms_angle_deg)],
    [#fmt(entry.metrics.peak_angle_deg)],
    [#fmt(entry.metrics.peak_cart_position_m, digits: 3)],
    [#fmt(100*entry.metrics.saturation_fraction)],
    [#fmt(entry.metrics.peak_command_N)],
  )).flatten(),
)

#figure([
  #sweep(plots.force_runs, "u_N", [Actuator command (N)], (0, 30), [Random-force actuator commands],
    height: 3.3in, ylim: (-10.5, 10.5), failed-from: 3, with-legend: true)
], caption: [Actuator use under the four disturbance bounds. The dashed 10 N case loses balance and remains saturated after failure.])

The held inputs appear in Figure 3(e,f). At bounds through 7.5 N, the angle stays within 5.4#sym.degree and the actuator never saturates. The 7.5 N case ends at #fmt(stats.force_stress.at(2).metrics.final_angle_deg)#sym.degree because the pushes continue; this is ongoing disturbed balance rather than a return to zero. At 10 N, the pendulum leaves the upright region and the command saturates. Once it falls, that limited command cannot restore the local upright response.

#pagebreak()

== Velocity states used by the controller

The preceding figures show position, angle, and force. The remaining two feedback states are cart velocity and angular velocity. The following histories compare the nominal 5#sym.degree release and 2.5 N random-force test.

#figure(velocity("x_dot_m_s", [Cart velocity (m/s)]),
  caption: [Cart velocity supplied to the state-feedback gain.])

#figure(velocity("theta_dot_deg_s", [Angular velocity (deg/s)]),
  caption: [Pendulum angular velocity. The controller uses radians per second internally.])

The release velocities decay as the cart and pendulum settle. Under continuing random pushes, the velocities continue to vary while the controller maintains balance. These signals complete the four-state record used to produce the report's position and angle responses.
