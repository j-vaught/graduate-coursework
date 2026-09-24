#import "@preview/lilaq:0.6.0" as lq

#let plots = json("plot_data.json")
#let stats = json("metrics.json")
#let garnet = rgb("#73000A")
#let black = rgb("#000000")
#let atlantic = rgb("#466A9F")
#let gray = rgb("#5C5C5C")
#let fmt(value, digits: 2) = str(calc.round(value, digits: digits))

#let angle-plot(run) = lq.diagram(
  width: 100%,
  height: 2.35in,
  xlabel: [Time, $t$ (s)],
  ylabel: [Pendulum angle, $theta$ (deg)],
  lq.plot(run.time_s, run.theta_deg, mark: none,
    stroke: (paint: garnet, thickness: 1.35pt)),
)
#let position-plot(run) = lq.diagram(
  width: 100%,
  height: 2.7in,
  xlabel: [Time, $t$ (s)],
  ylabel: [Cart position, $x$ (m)],
  lq.plot(run.time_s, run.x_m, mark: none,
    stroke: (paint: black, thickness: 1.25pt)),
)
#let force-plot(run) = lq.diagram(
  width: 100%,
  height: 2.7in,
  xlabel: [Time, $t$ (s)],
  ylabel: [Horizontal force (N)],
  lq.plot(run.time_s, run.u_N, mark: none,
    stroke: (paint: garnet, thickness: 1.25pt), label: [Control command]),
  lq.plot(run.time_s, run.disturbance_N, mark: none,
    stroke: (paint: black, thickness: 1.25pt, dash: "dashed"),
    label: [Base disturbance]),
)

#set page(paper: "us-letter", margin: 1in, numbering: "1",
  number-align: center + bottom)
#set text(font: ("Times New Roman", "New Computer Modern"), size: 10.5pt,
  lang: "en")
#set par(justify: true, leading: 0.55em)
#set heading(numbering: none)
#show heading.where(level: 1): it => block(above: 0.65em, below: 0.28em)[
  #text(size: 11pt, weight: "bold")[#it.body]
]
#show heading.where(level: 2): it => block(above: 0.5em, below: 0.2em)[
  #text(size: 10.5pt, weight: "bold")[#it.body]
]
#show figure.caption: set text(size: 9.5pt)

#align(center)[
  #text(size: 15pt, weight: "bold")[State-feedback control of an inverted pendulum on a cart]
  #v(0.2em)
  J.C. Vaught \
  EMCH 792, Learning-Based Controls
]

= Objective

The objective of this assignment is to hold the cart-mounted pendulum near its unstable upright equilibrium with state feedback. Mini Project 1 supplied a nonlinear Simulink model of the freely moving cart and pendulum. Here, a horizontal cart force becomes the control input, and the same nonlinear plant tests whether a controller designed from a local linearization can recover from a small release and reject a random disturbance.

= Methodology

The state is $z = (x, dot(x), theta, dot(theta))^T$, where $theta = 0$ is upright. The plant retains the Mini Project 1 values $M=2.0$ kg, $m=0.5$ kg, $ell=1.0$ m, $c_theta=0.01$ N m s/rad, and $g=9.81$ m/s². Linearizing the coupled mass-matrix equations at $z=0$ gives $dot(z)=A z+B F$. The controllability matrix has rank four. A linear-quadratic regulator with $Q="diag"(4,2,300,10)$ and $R=0.5$ sets the feedback $u=-K z$. The actuator command is limited to $abs(u) <= 10$ N, and the nonlinear plant receives $F=u+d$, where $d$ is an external horizontal force on the cart. This choice gives the assignment's base disturbance a precise physical meaning.

The first 12 s test begins at $theta(0)=5 degree$ with $d=0$. The second begins upright and applies a fixed-seed random force held for 0.1 s per sample, bounded by $abs(d) <= 2.5$ N. Simulink integrates the nonlinear model with ode45 and a 0.01 s maximum step. The appendix gives the derivation, model, code, and additional tests.

= Results and Discussion

#figure(
  angle-plot(plots.perturbation),
  caption: [Upright-angle response after a 5#sym.degree release with no disturbance.],
)

The 5#sym.degree release returns inside $plus.minus 1 degree$ by #fmt(stats.perturbation.settling_time_s) s and stays there. Its peak cart travel is #fmt(stats.perturbation.peak_cart_position_m, digits: 3) m. The response confirms local stabilization of the nonlinear model, including the pivot damping and trigonometric terms absent from the design model.

#pagebreak()

= Results and Discussion (continued)

#figure(
  angle-plot(plots.random_test),
  caption: [Upright-angle response under the bounded random horizontal disturbance.],
)

With the cart excited throughout the second test, the pendulum's angle has an RMS magnitude of #fmt(stats.random_test.rms_angle_deg) degree and a peak of #fmt(stats.random_test.peak_angle_deg) degree. The controller therefore keeps the pendulum near upright without requiring the disturbance to stop. The corresponding cart motion and command-force histories appear in the appendix.

#figure(
  force-plot(plots.random_test),
  caption: [Feedback command and externally applied disturbance in the random-force test. Solid garnet is the command; dashed black is the disturbance.],
)

The actuator never reaches its 10 N limit in the required random test. Under larger perturbations, the 20#sym.degree release recovers, but the 30#sym.degree release does not. A 10 N random-force bound also causes sustained saturation and loss of upright control. The local linear design therefore has a finite recovery region. The model assumes an unlimited cart track and exact state measurements; physical rail limits and measurement noise would reduce practical margin.

#pagebreak()

= Appendix A. Nonlinear plant and sign convention

The cart translates in the positive $x$ direction under a positive horizontal force $F$. The pendulum angle $theta$ measures displacement from the upright position, matching the Mini Project 1 model. The rod is massless, its point mass is $m$, the cart mass is $M$, and the pivot has rotational viscous damping $c_theta$. No track friction or rail stops are present. Applying a force to the cart changes the first of the original two coupled equations to

$
(M+m) dot.double(x) + m ell cos(theta) dot.double(theta)
- m ell sin(theta) dot(theta)^2 = F,
$

while the angular equation remains

$
m ell cos(theta) dot.double(x) + m ell^2 dot.double(theta)
+ c_theta dot(theta) - m g ell sin(theta) = 0.
$

The controlled MATLAB Function block solves the resulting $2 times 2$ mass-matrix system at each solver step. The model sends the resulting accelerations through the four inherited integrators. This preserves the Mini Project 1 nonlinear plant and adds only the force input and feedback path.

#table(
  columns: (1.1fr, 2.7fr, 1.2fr),
  inset: 5pt,
  [Parameter], [Meaning], [Value],
  [$M$], [Cart mass], [2.0 kg],
  [$m$], [Pendulum point mass], [0.5 kg],
  [$ell$], [Pendulum length], [1.0 m],
  [$c_theta$], [Pivot rotational damping], [0.01 N m s/rad],
  [$g$], [Gravitational acceleration], [9.81 m/s²],
)

The model neglects actuator delay, sensor noise, track friction, and end stops. The reported performance applies to this simulated plant with the stated 10 N command limit.

#pagebreak()

= Appendix B. Upright linearization

For small $theta$, use $sin(theta) approx theta$, $cos(theta) approx 1$, and omit the second-order term $theta dot(theta)^2$. At the upright equilibrium, the equations become

$
(M+m) dot.double(x) + m ell dot.double(theta) = F,
$
$
m ell dot.double(x) + m ell^2 dot.double(theta)
+ c_theta dot(theta) - m g ell theta = 0.
$

Eliminating $dot.double(theta)$ from the first equation gives

$
dot.double(x) = F/M - (m g)/M theta + c_theta/(M ell) dot(theta).
$

Substitution gives the angular acceleration

$
dot.double(theta) = -F/(M ell)
+ ((M+m) g)/(M ell) theta
- (c_theta (M+m))/(M m ell^2) dot(theta).
$

With $z=(x,dot(x),theta,dot(theta))^T$, this is $dot(z)=A z+B F$. At the assigned parameter values,

$
A = mat(
  0, 1, 0, 0;
  0, 0, -2.4525, 0.005;
  0, 0, 0, 1;
  0, 0, 12.2625, -0.025
), quad
B = mat(0;0.5;0;-0.5).
$

The signs of the force entries show that a positive cart force accelerates the cart right and initially accelerates the upright pendulum angle in the opposite direction.

#pagebreak()

= Appendix C. Feedback design

The upright linearization has a controllability matrix $cal(C)=(B,A B,A^2 B,A^3 B)$ with rank four. The chosen quadratic objective penalizes cart position, cart velocity, upright angle, angular velocity, and control effort through

$
J = integral_0^infinity (z^T Q z + R u^2) dif t,
quad Q="diag"(4,2,300,10), quad R=0.5.
$

The MATLAB `lqr` calculation returns $u=-K z$ with $K=(-2.8284,-6.3204,-86.8641,-25.2346)$. The signs reflect the chosen angle and force directions. The nonlinear simulation clips this command to $plus.minus 10$ N before adding the disturbance. The disturbance itself is an external force, so its magnitude is not counted against the commanded actuator limit.

The theoretical closed-loop poles have negative real parts, but that linear result applies near upright and without saturation. The nonlinear tests below evaluate behavior outside those assumptions. Rebuilding the editable model from `build_controlled_model.m` embeds the computed gain as a numerical block parameter, so the delivered model does not depend on a workspace variable named `K`.

#pagebreak()

= Appendix D. Simulation and measurement protocol

Both required tests run for 12 s with the same continuous nonlinear Simulink model and controller. The first uses $theta(0)=5 degree$, while the remaining initial states and disturbance are zero. The second starts at the upright equilibrium. It applies independent uniform force samples in $[-2.5,2.5]$ N every 0.1 s and holds each sample constant until the next. The random generator uses seed 79202, and the sampled force is stored in the results file. This is a repeatable test signal, not an unknown future noise process.

The reported peak angle is $max_t abs(theta(t))$. Root-mean-square angle is $sqrt((1/N) sum_i theta_i^2)$ on a uniform 0.02 s analysis grid. The 1#sym.degree settling time is the earliest sampled time after which the angle remains inside that band through the end of the test. Actuator saturation fraction counts grid samples where $abs(u) >= 10$ N. A trial is marked recovered only when its final angle and final-two-second RMS angle are both below 2#sym.degree. Metrics use the full analysis grid; the figure data are thinned to 0.04 s only for the PDF.

The additional tests reuse the same 10 N controller. One sweep starts at 10, 20, 30, 45, and 60#sym.degree without disturbance. The other scales one fixed random realization to amplitudes of 2.5, 5, 7.5, and 10 N. These sweeps show the consequences of larger releases and disturbance forces without changing the control law.

#pagebreak()

= Appendix E. Release-test signals

#figure(
  position-plot(plots.perturbation),
  caption: [Cart displacement during recovery from the 5#sym.degree release.],
)

#figure(
  force-plot(plots.perturbation),
  caption: [Actuator command during the release test. The disturbance is zero.],
)

The controller shifts the cart to counter the falling moment and then brings the cart toward the origin. Its finite command is represented explicitly by the saturation block in the Simulink model.

#pagebreak()

= Appendix F. Random-disturbance signals

#figure(
  position-plot(plots.random_test),
  caption: [Cart displacement while random force excites the base.],
)

#figure(
  force-plot(plots.random_test),
  caption: [Actuator and disturbance histories for the bounded random-force test.],
)

The cart is free to move along an unlimited track in this model. Its displacement is therefore a separate performance measure from the pendulum angle.

#pagebreak()

= Appendix G. Stress-test summary

The two required tests use 5#sym.degree initial tilt and a 2.5 N disturbance bound. The following larger cases are diagnostic only. Recovery means that both the final angle and final-two-second RMS angle are under 2 degrees. This criterion does not imply satisfaction of a physical cart-travel constraint.

#let angle_rows = stats.angle_stress.map(entry => (
  [#str(entry.initial_angle_deg)],
  [#fmt(entry.metrics.peak_cart_position_m, digits: 3)],
  [#fmt(100*entry.metrics.saturation_fraction)],
  [#if entry.metrics.recovered { "Yes" } else { "No" }],
)).flatten()
#table(
  columns: (1fr, 1.3fr, 1.3fr, 0.8fr),
  inset: 5pt,
  [Initial tilt (deg)], [Peak cart travel (m)],
  [Saturation time (%)], [Recovered],
  ..angle_rows,
)

#v(0.5em)

#let force_rows = stats.force_stress.map(entry => (
  [#fmt(entry.amplitude_N, digits: 1)],
  [#fmt(entry.metrics.rms_angle_deg)],
  [#fmt(entry.metrics.peak_angle_deg)],
  [#fmt(100*entry.metrics.saturation_fraction)],
)).flatten()
#table(
  columns: (1fr, 1.3fr, 1.3fr, 1.3fr),
  inset: 5pt,
  [Force bound (N)], [RMS angle (deg)],
  [Peak angle (deg)], [Saturation time (%)],
  ..force_rows,
)

Because every force-bound case uses the same random draw, the table isolates the effect of scaling the disturbance amplitude. The 20#sym.degree release recovers only after nearly 3 m of cart travel, while the 30#sym.degree release saturates throughout and fails. At a 10 N disturbance bound, the angle is unwrapped and records repeated rotations after loss of control. The roughly 288 m cart travel in failed tilt trials is a failure signature of the unlimited-track simulation, not a physically feasible test result.

#pagebreak()
#set page(paper: "us-letter", flipped: true, margin: 1in,
  numbering: "1", number-align: center + bottom)

= Appendix H. Editable Simulink model

#figure(
  image("controlled_model_diagram.png", width: 8.5in),
  caption: [Top-level feedback loop in the delivered `inverted_pendulum_controlled.slx` model.],
)

The top level exposes the disturbance, total cart force, nonlinear plant, feedback gain, actuator limit, and four output blocks that record the simulation histories.

#pagebreak()

= Appendix H. Nonlinear plant detail

#figure(
  image("nonlinear_plant_diagram.png", width: 8.5in),
  caption: [Inside the nonlinear plant subsystem. The equations and four integrators come from Mini Project 1.],
)

Inside the plant, the inherited equations and four integrators retain their original positions. The State order inputs appear from top to bottom as $(theta,dot(theta),dot(x),x)$; its internal wiring assembles the controller vector $(x,dot(x),theta,dot(theta))$.

#pagebreak()
#set page(paper: "us-letter", flipped: false, margin: 1in,
  numbering: "1", number-align: center + bottom)

= Appendix I. Nonlinear acceleration code

#show raw.where(block: true): it => block(
  width: 100%, fill: rgb("#ECECEC"),
  stroke: 0.5pt + rgb("#A2A2A2"), inset: 6pt,
)[
  #set text(font: "DejaVu Sans Mono", size: 7.5pt)
  #it
]

The following is the complete source loaded into the copied MATLAB Function block. The first seven arguments preserve the Mini Project 1 interface; the eighth adds the total cart force.

#raw(read("controlled_accelerations.m"), lang: "matlab", block: true)

= Appendix J. Model-construction code

The complete builder copies the Mini Project 1 Simulink model, adds the force input and feedback blocks, and saves an editable Project 2 model.

#raw(read("build_controlled_model.m"), lang: "matlab", block: true)

#pagebreak()

= Appendix K. Experiment and verification code

The experiment script derives $A$ and $B$, checks controllability and closed-loop poles, rebuilds the model, runs all cases, computes metrics, and exports simulation data and the model diagram.

#raw(read("run_project2.m"), lang: "matlab", block: true)
