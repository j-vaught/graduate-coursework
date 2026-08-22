#set page(
  paper: "us-letter",
  margin: 1in,
  numbering: "1",
  number-align: center + bottom,
)
#set text(font: "New Computer Modern", size: 10.5pt)
#set par(justify: true, leading: 0.62em)
#set heading(numbering: none)
#show heading.where(level: 1): it => block(above: 0.8em, below: 0.35em)[
  #text(size: 12pt, weight: "bold")[#it.body]
]
#show figure.caption: set text(size: 9pt)

#align(center)[
  #text(size: 16pt, weight: "bold")[Nonlinear Simulation of an Inverted Pendulum on a Cart]

  #v(0.25em)
  J.C. Vaught
]

= Objective

The objective of this assignment is to model the nonlinear motion of an unforced inverted pendulum on a freely translating cart and to compare two independent implementations. The first implementation evaluates the equations of motion directly in Simulink. The second represents the same mechanism with physical components in Simscape Multibody. The cart position $x(t)$ and pendulum angle $theta(t)$ are compared after releasing the pendulum five degrees from the unstable upright equilibrium with zero initial velocity.

= Methodology

The pendulum is treated as a point mass $m$ at distance $ell$ from a frictionless cart of mass $M$. The coordinate $x$ is positive to the right, and $theta$ is measured clockwise from upright. A viscous rotational damper with coefficient $c_theta$ acts at the pivot. Lagrange's equations give the coupled nonlinear model

$
(M + m) dot.double(x) + m ell cos(theta) dot.double(theta)
- m ell sin(theta) dot(theta)^2 = 0,
$

and

$
m ell cos(theta) dot.double(x) + m ell^2 dot.double(theta)
+ c_theta dot(theta) - m g ell sin(theta) = 0.
$

At each Simulink time step, the two equations are assembled as a $2 times 2$ mass-matrix system and solved for $dot.double(x)$ and $dot.double(theta)$. Two integrator chains recover $x(t)$ and $theta(t)$. The second model uses a world frame, a prismatic cart joint, a damped revolute pivot, a rigid transform of length $ell$, and a concentrated spherical mass. Both models use $M=2.0$ kg, $m=0.5$ kg, $ell=1.0$ m, $c_theta=0.01$ $N dot m dot s / "rad"$, $g=9.81$ $m / s^2$, and $theta(0)=5 degree$. Variable-step solvers run for 20 s with a maximum step of 0.01 s.

The two responses are interpolated onto a common 0.01 s time grid. Agreement is assessed from the maximum absolute difference in cart position and pendulum angle over the simulation interval.

#pagebreak()

= Results and Discussion

#figure(
  image("response_comparison.png", width: 100%),
  caption: [Cart position and pendulum angle from the direct-equations and physical-component models.],
)

The five-degree perturbation grows immediately because the upright equilibrium is unstable. The pendulum falls through the downward equilibrium and continues into a damped oscillation about $theta=pi$ rad. Over 20 s, the direct model predicts $-0.183 <= x <= 0.217$ m and $0.087 <= theta <= 5.947$ rad. The cart remains bounded because there is no external horizontal force, while pivot damping gradually removes mechanical energy and contracts the angular oscillation about the downward equilibrium.

The two independently constructed responses nearly overlap throughout the simulation. Their maximum absolute differences are 0.014 m in $x$ and 0.056 rad in $theta$. The small phase separation late in the record is expected because the release begins near an unstable equilibrium, where small numerical and geometric differences amplify before damping dominates. The agreement supports both the nonlinear equation implementation and the orientation, gravity, damping, and sensing choices in the Multibody model.

#pagebreak()
#set page(width: 11in, height: 8.5in, margin: 0.55in)

= Appendix A. Direct-Equations Simulink Model

#figure(
  image("simulink_model_diagram.png", width: 100%),
  caption: [Editable Simulink implementation of the nonlinear mass-matrix equations.],
)

#pagebreak()

= Appendix B. Simscape Multibody Model

#figure(
  image("multibody_model_diagram.png", width: 100%),
  caption: [Simscape Multibody block diagram.],
)

#pagebreak()

= Appendix C. Mechanics Explorer Model

#figure(
  image("multibody_model_mechanics_explorer.png", width: 100%),
  caption: [Mechanics Explorer view of the cart, ruler, pendulum rod, and point mass.],
)

#pagebreak()
#set page(paper: "us-letter", margin: 1in)

= Appendix D. Reproducible MATLAB Build and Simulation Code

#show raw.where(block: true): it => block(
  width: 100%,
  fill: rgb("#ECECEC"),
  stroke: 0.5pt + rgb("#A2A2A2"),
  inset: 7pt,
  breakable: true,
)[
  #set text(font: "DejaVu Sans Mono", size: 6.4pt)
  #it
]

#raw(read("build_mini_project_1.m"), lang: "matlab", block: true)
