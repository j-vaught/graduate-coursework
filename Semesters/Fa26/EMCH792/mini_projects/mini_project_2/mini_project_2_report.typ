#import "@preview/lilaq:0.6.0" as lq

#let plots = json("plot_data.json")
#let stats = json("metrics.json")
#let fmt(value, digits: 2) = str(calc.round(value, digits: digits))

#let angle-plot(run) = lq.diagram(
  width: 100%,
  height: 1.8in,
  xlabel: [Time, $t$ (s)],
  ylabel: [Pendulum angle, $theta$ (deg)],
  lq.plot(run.time_s, run.theta_deg, mark: none,
    stroke: (thickness: 1.2pt)),
)
#let position-plot(run, height: 2.7in) = lq.diagram(
  width: 100%,
  height: height,
  xlabel: [Time, $t$ (s)],
  ylabel: [Cart position, $x$ (m)],
  lq.plot(run.time_s, run.x_m, mark: none,
    stroke: (thickness: 1.2pt)),
)
#let force-plot(run, height: 2.7in) = lq.diagram(
  width: 100%,
  height: height,
  xlabel: [Time, $t$ (s)],
  ylabel: [Horizontal force (N)],
  lq.plot(run.time_s, run.u_N, mark: none,
    stroke: (thickness: 1.2pt), label: [Control command]),
  lq.plot(run.time_s, run.disturbance_N, mark: none,
    stroke: (thickness: 1.2pt, dash: "dashed"),
    label: [Base disturbance]),
)

#set page(paper: "us-letter", margin: (top: 0.75in, bottom: 1in, x: 1in), numbering: "1",
  number-align: center + bottom)
#set text(font: ("Times New Roman", "New Computer Modern", "Latin Modern Roman"), size: 11pt,
  lang: "en")
#set par(justify: true, leading: 0.55em)
#set heading(numbering: none)
#show heading.where(level: 1): it => block(above: 0.75em, below: 0.35em)[
  #text(size: 11pt, weight: "bold")[#it.body]
]
#show heading.where(level: 2): it => block(above: 0.5em, below: 0.2em)[
  #text(size: 10.5pt, weight: "bold")[#it.body]
]
#show figure.caption: set text(size: 11pt)

#align(center)[
  #text(size: 17pt, weight: "bold")[State-feedback control of an inverted pendulum on a cart]
  #v(0.2em)
  #text(size: 10pt)[J.C. Vaught]
  #v(0.1em)
  #text(size: 9pt)[EMCH 792: Learning-Based Controls]
]

#v(0.35em)
#block(
  width: 100%,
  inset: (x: 0pt, y: 5pt),
  stroke: (top: 0.5pt + rgb("#A2A2A2"), bottom: 0.5pt + rgb("#A2A2A2")),
)[
  #text(weight: "bold")[OBJECTIVE.]
  The objective is to hold the cart-mounted pendulum near its unstable upright equilibrium with state feedback. Mini Project 1 supplied the nonlinear Simulink plant. A horizontal cart force now acts as the control input, and the same plant tests whether a controller designed from a local linearization can recover from a small release and reject a random disturbance.
]

#columns(2, gutter: 0.25in)[
= METHODOLOGY.

  The plant has a frictionless cart of mass $M=2.0$ kg and a massless rod carrying a point mass $m=0.5$ kg at length $ell=1.0$ m. Its pivot damping is $c_theta=0.01$ N m s/rad, and gravity is $g=9.81$ m/s². The angle $theta=0$ denotes the unstable upright position. A positive force $F$ pushes the cart in the positive $x$ direction. As in Mini Project 1, the two accelerations are solved together from a mass matrix, then integrated twice to obtain velocities and positions.

  The controller uses the state $z=(x,dot(x),theta,dot(theta))^T$. Adding $F$ to the cart equation and linearizing the inherited nonlinear model about $z=0$ gives $dot(z)=A z+B F$. The controllability matrix has rank four, so this local model can be stabilized by state feedback. The nonlinear simulation retains the trigonometric coupling and pivot damping, which lets the tests expose behavior beyond the linear approximation.

  A linear-quadratic regulator uses $Q="diag"(4,2,300,10)$ and $R=0.5$. The larger angular weight makes upright balance the priority while the cart-position weight discourages unrestricted travel. MATLAB gives $K=(-2.8284,-6.3204,-86.8641,-25.2346)$ for $u=-K z$. Both closed-loop pole pairs have negative real parts. The actuator limits $u$ to $plus.minus 10$ N before an external disturbance $d$ is added, so the plant receives $F=u+d$. This ordering distinguishes command saturation from disturbance magnitude.

  #colbreak()

== SIMULATION STEPS.

  The editable Simulink model copies the Mini Project 1 nonlinear MATLAB Function and four integrators into the plant subsystem. The additional function input applies the total cart force. Outside that subsystem, a gain computes $-K z$, a saturation block limits the command, and a circular sum block adds the disturbance. The State order block presents its inputs as $theta$, $dot(theta)$, $dot(x)$, and $x$ from top to bottom, then assembles $z$ internally. Thus the visible wiring and the controller's matrix order are both explicit.

  The first 12 s test starts at $theta(0)=5 degree$ with all other states and $d$ zero. The second starts upright and applies a horizontal force sampled uniformly between $-2.5$ and $2.5$ N every 0.1 s. A zero-order hold keeps each value until the next sample. Seed 79202 fixes the random realization, so rerunning the MATLAB script produces the same force history and figures. Simulink uses ode45 with a 0.01 s maximum step, and the analysis resamples the logged states at 0.02 s.

  The report measures angle, cart travel, and command force separately. A settling time is recorded only after $abs(theta)$ remains below 1#sym.degree for the rest of the run. Additional release angles and disturbance amplitudes test the controller's margin without retuning $K$. Those cases appear in the appendix because the two required experiments are the central result. The appendix also contains the equations, numerical gain, editable block diagrams, MATLAB source, and complete stress-test metrics.
]

#pagebreak()

#columns(2, gutter: 0.25in)[
= RESULTS.

  #figure(
    position-plot(plots.perturbation, height: 1.8in),
    caption: [Cart position during recovery from the 5#sym.degree release.],
  )

  The release moves the cart by at most #fmt(stats.perturbation.peak_cart_position_m, digits: 3) m before it returns toward the origin. The largest commanded force is #fmt(stats.perturbation.peak_command_N) N, below the 10 N limit. Thus the required small-angle recovery does not depend on saturation.

  #figure(
    angle-plot(plots.perturbation),
    caption: [Pendulum angle after the 5#sym.degree release.],
  )

  The pendulum crosses upright once and then decays toward it. After #fmt(stats.perturbation.settling_time_s) s, the angle remains within $plus.minus 1 degree$. This response tests the nonlinear plant, rather than only the linear model used to compute $K$.

  #colbreak()

  #figure(
    angle-plot(plots.random_test),
    caption: [Pendulum angle under the bounded random horizontal disturbance.],
  )

  During the second test, the pendulum has an RMS angle of #fmt(stats.random_test.rms_angle_deg) degree and a peak of #fmt(stats.random_test.peak_angle_deg) degree. The cart moves at most #fmt(stats.random_test.peak_cart_position_m, digits: 3) m while the disturbance continues.

  #figure(
    force-plot(plots.random_test, height: 1.8in),
    caption: [Random-force test. Solid blue is the control command; dashed orange is the external disturbance.],
  )

= DISCUSSION.

  The command peaks at #fmt(stats.random_test.peak_command_N) N in the random test and never reaches saturation. The controller therefore holds the pendulum near upright in both required cases. Its margin is finite. A 20#sym.degree release recovers only after almost 3 m of cart travel, whereas a 30#sym.degree release saturates throughout and fails. A random-force bound of 10 N also defeats the controller. The model assumes an unlimited track and exact state measurements; rail stops and measurement noise would further limit a physical implementation.
]

#pagebreak()
#set page(paper: "us-letter", margin: 1in, numbering: "1",
  number-align: center + bottom)
#set text(size: 10.5pt)
#show figure.caption: set text(size: 9.5pt)

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
