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
  Mini Project 1 modelled the motion of a pendulum on a cart without a controller. Project 2 adds a controller that pushes the cart to keep the pendulum upright and bring the cart back toward its starting position. We test whether it can recover from a small initial tilt and maintain balance while random horizontal forces push the cart.
]

#columns(2, gutter: 0.25in)[
= METHODOLOGY.

  We began with the nonlinear Simulink model from Mini Project 1 and added a horizontal force $F$ to the cart equation. The cart mass is $M=2.0$ kg, the pendulum mass is $m=0.5$ kg, and the massless rod length is $ell=1.0$ m. The model retains the original pivot damping, $c_theta=0.01$ N m s/rad, and gravity, $g=9.81$ m/s². The upright position is $theta=0$. The equations calculate both accelerations, and four integrators then calculate the velocities and positions.

  With the force input added, we needed a rule for deciding how hard to push the cart. We linearized the equations near upright to obtain $dot(z)=A z+B F$, where $z=(x,dot(x),theta,dot(theta))^T$. These four states describe cart position, cart velocity, pendulum angle, and angular velocity. A MATLAB controllability check confirmed that the cart force can control all four states. We used this simpler model to design the controller, then tested it on the original nonlinear model.

  We chose a linear-quadratic regulator (LQR), which balances angle error, cart movement, and control force. Its weights give the angle the highest priority while also encouraging the cart to return to the origin. MATLAB calculated the gain $K$ for the force command $u=-K z$. The resulting linear model is stable. Appendix C gives the weights, gain, and design equation; the following tests show how the controller performs with the full nonlinear equations and a limited actuator.

  #colbreak()

== SIMULATION STEPS.

  To apply the controller, we connected the four simulated states to the feedback gain. An actuator block limits its command to $plus.minus 10$ N. A sum block then adds the external disturbance $d$, so the cart receives $F=u+d$. The State order block displays $theta$, $dot(theta)$, $dot(x)$, and $x$ from top to bottom and rearranges them internally into the order used by $K$. Appendices H and I show the complete loop and the nonlinear model inside it.

  We first released the pendulum from $5 degree$ with no disturbance. We then started it upright and applied random horizontal pushes between $-2.5$ and $2.5$ N. Each force value is drawn independently from a uniform distribution every 0.1 s and held until the next draw. This represents a force that changes in short steps. Seed 79202 makes the sequence repeatable. Both tests run for 12 s using ode45 with a maximum step of 0.01 s.

  We measured angle, cart displacement, and control force to determine whether balance required excessive motion or actuator saturation. Settling time marks when the angle enters $plus.minus 1 degree$ and stays there through the end of the run. We also tested larger tilts and scaled the same random sequence to force bounds of 5, 7.5, and 10 N. These are stronger versions of one disturbance model. We did not compare different force distributions, steady biases, impulses, or sensor noise.
]

#pagebreak()

#columns(2, gutter: 0.25in)[
= RESULTS.

  #figure(
    position-plot(plots.perturbation, height: 1.8in),
    caption: [Cart position during recovery from the 5#sym.degree release.],
  )

  Figure 1 shows the cart moving to catch the tilted pendulum and then returning toward the origin. Its maximum displacement is #fmt(stats.perturbation.peak_cart_position_m, digits: 3) m. The largest control force is #fmt(stats.perturbation.peak_command_N) N, so this recovery stays below the 10 N actuator limit.

  #figure(
    angle-plot(plots.perturbation),
    caption: [Pendulum angle after the 5#sym.degree release.],
  )

  That cart motion brings the pendulum back toward upright, as Figure 2 shows. After #fmt(stats.perturbation.settling_time_s) s, the angle stays within $plus.minus 1 degree$. The controller therefore recovers from the initial tilt in the full nonlinear simulation.

  #colbreak()

  #figure(
    angle-plot(plots.random_test),
    caption: [Pendulum angle under the bounded random horizontal disturbance.],
  )

  Figure 3 shows small angle changes while the controller maintains balance. The root-mean-square (RMS) angle is #fmt(stats.random_test.rms_angle_deg) degree, and the maximum is #fmt(stats.random_test.peak_angle_deg) degree. The cart moves at most #fmt(stats.random_test.peak_cart_position_m, digits: 3) m. Figure 4 shows the corresponding forces.

  #figure(
    force-plot(plots.random_test, height: 1.8in),
    caption: [Control command (solid blue) and random disturbance (dashed orange).],
  )

= DISCUSSION.

  The random test needs at most #fmt(stats.random_test.peak_command_N) N, below the actuator limit. Both main tests therefore maintain balance. Stronger tests in Appendix G show the limits. A 20#sym.degree release recovers but needs almost 3 m of cart travel. A 30#sym.degree release reaches the force limit throughout and fails, as does the 10 N random-force case. Larger inputs can therefore exceed the available force or require substantial cart travel. The force sweep changes strength only; other disturbance types remain untested.
]

#pagebreak()
#set page(paper: "us-letter", margin: 1in, numbering: "1",
  number-align: center + bottom)
#set text(size: 10.5pt)
#show figure.caption: set text(size: 9.5pt)

= Appendix A. Nonlinear plant and sign convention

The main report begins by adding a cart force to the Mini Project 1 model. Here, positive $F$ pushes the cart in the positive $x$ direction, and $theta$ measures the pendulum angle from upright. The rod is massless, its end mass is $m$, the cart mass is $M$, and $c_theta$ represents pivot damping. Adding the force changes the cart equation to

$
(M+m) dot.double(x) + m ell cos(theta) dot.double(theta)
- m ell sin(theta) dot(theta)^2 = F,
$

while the angular equation remains

$
m ell cos(theta) dot.double(x) + m ell^2 dot.double(theta)
+ c_theta dot(theta) - m g ell sin(theta) = 0.
$

These equations couple the two accelerations, so the MATLAB Function block solves them together at each solver step. The four original integrators then convert the accelerations into velocities and positions. The following table lists the model parameters.

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

The simulation uses an unlimited track and exact state values, with no track friction or actuator delay. Its actuator command is limited to 10 N.

#pagebreak()

= Appendix B. Upright linearization

The nonlinear equations in Appendix A provide the model used for testing. To design the controller, we simplify those equations near upright. For small $theta$, use $sin(theta) approx theta$ and $cos(theta) approx 1$, and drop the term $theta dot(theta)^2$. The equations become

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

The entries of $B$ show the immediate effect of a push. A positive force accelerates the cart right and changes the pendulum's angular acceleration in the opposite direction. Appendix C uses these matrices to calculate the feedback gain.

#pagebreak()

= Appendix C. Feedback design

Before choosing a gain, we checked whether the force input in Appendix B can control all four states. The controllability matrix $cal(C)=(B,A B,A^2 B,A^3 B)$ has rank four, confirming that it can. We then chose an LQR that penalizes state errors and control force through

$
J = integral_0^infinity (z^T Q z + R u^2) dif t,
quad Q="diag"(4,2,300,10), quad R=0.5.
$

The weights in $Q$ correspond to $x$, $dot(x)$, $theta$, and $dot(theta)$ in that order. The angle receives the largest weight, while $R$ penalizes the force command. MATLAB's `lqr` function returns $u=-K z$ with $K=(-2.8284,-6.3204,-86.8641,-25.2346)$. The nonlinear model limits this command to $plus.minus 10$ N, then adds the external force $d$.

The poles of $A-B K$ are approximately $-0.699 plus.minus 0.548 i$ and $-4.042 plus.minus 1.125 i$. Their negative real parts confirm stability of the linear design. Because the actual model retains the nonlinear equations and force limit, we next test whether the same gain maintains balance in that model. The builder stores the numerical gain directly in the Simulink block.

#pagebreak()

= Appendix D. Simulation and measurement protocol

To test the gain from Appendix C, we ran two 12 s simulations with the same nonlinear model. The release test sets $theta(0)=5 degree$ and all other states and the disturbance to zero. The random-force test starts upright and draws independent uniform samples in $[-2.5,2.5]$ N every 0.1 s. Each value remains constant until the next draw. This describes irregular pushes with abrupt changes and a known force bound. Seed 79202 reproduces the force history stored in `metrics.json`.

We sample the logged response every 0.02 s to calculate the metrics. Peak angle is $max_t abs(theta(t))$, while RMS angle is $sqrt((1/N) sum_i theta_i^2)$. Peak angle captures the largest deviation; RMS angle describes its overall size across the run. Settling time marks entry into the 1#sym.degree band with no later exit. For the continuously disturbed run, this time describes the particular force history, rather than the response to a single release.

Saturation fraction is the fraction of analysis samples where $abs(u) >= 10$ N. A trial counts as recovered when its final angle magnitude and its RMS angle over the final two seconds are both below 2#sym.degree. Metrics use every analysis sample, and figures use every second sample to keep the PDF compact.

We then tested stronger inputs without changing the gain or the 10 N actuator limit. The release angles were 10, 20, 30, 45, and 60#sym.degree. The random-force bounds were 2.5, 5, 7.5, and 10 N, all using the same sequence of draws. This isolates the effect of force strength. We used one random-force model and one seed; we did not vary its distribution or update interval, or test correlated forces, steady biases, impulses, or sensor noise.

#pagebreak()

= Appendix E. Release-test signals

#figure(
  force-plot(plots.perturbation),
  caption: [Actuator command during the release test. The disturbance is zero.],
)

The release test from Appendix D needs a large initial push to catch the tilted pendulum. As the angle approaches upright, the force decreases and changes direction to bring the cart back. The peak command is #fmt(stats.perturbation.peak_command_N) N, so the actuator does not reach its limit.

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

Unlike the single release in Appendix E, the random pushes continue throughout this run. The controller responds by moving the cart and changing its force command. The maximum displacement is #fmt(stats.random_test.peak_cart_position_m, digits: 3) m, and the maximum command is #fmt(stats.random_test.peak_command_N) N. Recording both shows how much movement and force were needed to maintain balance.

#pagebreak()

= Appendix G. Stress-test summary

The preceding tests use a 5#sym.degree tilt and a 2.5 N disturbance bound. We increased each input to find where the same controller loses balance. The first table reports the larger release tests. Recovery follows the angle criterion defined in Appendix D, while peak cart displacement shows the motion needed to achieve it.

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

The second table scales the random-force sequence used in Appendix F. Because the sequence and update interval stay the same, changes in the response result from increasing the force bound.

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

The 20#sym.degree release recovers after nearly 3 m of cart travel, while the 30#sym.degree release reaches the force limit throughout and fails. The 10 N random-force case also loses balance. After failure, the angle records full rotations and the cart continues along the model's unlimited track. The large recorded angles and displacements therefore describe loss of control. These tables compare input strength within the chosen tests; they do not compare different disturbance models.

#pagebreak()
#set page(paper: "us-letter", flipped: true, margin: 1in,
  numbering: "1", number-align: center + bottom)

= Appendix H. Editable Simulink model

#figure(
  image("controlled_model_diagram.png", width: 8.5in),
  caption: [Top-level feedback loop in the delivered `inverted_pendulum_controlled.slx` model.],
)

The preceding results come from this feedback loop. The nonlinear model outputs four states, the feedback gain converts them into a force command, and the actuator block limits that command. The circular sum adds the disturbance before the total force returns to the cart. Four output blocks save the states and force histories for analysis.

#pagebreak()

= Appendix I. Nonlinear plant detail

#figure(
  image("nonlinear_plant_diagram.png", width: 8.5in),
  caption: [Inside the nonlinear plant subsystem. The equations and four integrators come from Mini Project 1.],
)

The nonlinear model in Appendix H contains the equations and four integrators inherited from Mini Project 1. The MATLAB Function calculates angular and cart acceleration; each acceleration passes through two integrators to produce velocity and position. The State order inputs are $(theta,dot(theta),dot(x),x)$ from top to bottom. Its internal wiring assembles $(x,dot(x),theta,dot(theta))$ for the controller.

#pagebreak()
#set page(paper: "us-letter", flipped: false, margin: 1in,
  numbering: "1", number-align: center + bottom)

= Appendix J. Nonlinear acceleration function

#show raw.where(block: true): it => block(
  width: 100%, fill: rgb("#ECECEC"),
  stroke: 0.5pt + rgb("#A2A2A2"), inset: 6pt,
)[
  #set text(font: "DejaVu Sans Mono", size: 7.5pt)
  #it
]

The acceleration block shown in Appendix I uses the function below. It solves the two coupled equations from Appendix A. The first seven inputs come from Mini Project 1, and the eighth supplies the total cart force.

#raw(read("controlled_accelerations.m"), lang: "matlab", block: true)

The complete model builder and experiment script are supplied as separate MATLAB files alongside this report.
