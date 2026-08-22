#import "@preview/lilaq:0.6.0" as lq

#let plot-data = json("python_plot_data.json")
#let solid-stroke = (thickness: 1.2pt)
#let dashed-stroke = (thickness: 1.2pt, dash: "dashed")

#set page(
  paper: "us-letter",
  margin: (top: 0.75in, bottom: 1in, x: 1in),
  numbering: "1",
  number-align: center + bottom,
)
#set text(
  font: ("Times New Roman", "New Computer Modern", "Latin Modern Roman"),
  size: 11pt,
  lang: "en",
)
#set par(justify: true, leading: 0.55em)
#set heading(numbering: "1.")
#show heading.where(level: 1): it => block(above: 0.75em, below: 0.35em)[
  #text(size: 11pt, weight: "bold")[#it.body]
]
#show heading.where(level: 2): it => block(above: 0.55em, below: 0.25em)[
  #text(size: 10pt, weight: "bold")[#it.body]
]
#show figure.caption: set text(size: 11pt)

#align(center)[
  #text(size: 17pt, weight: "bold")[Modeling an Uncontrolled Inverted Pendulum on a Cart in Simulink and Simscape Multibody]

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
  #text(weight: "bold", size: 11pt)[OBJECTIVE.]
  #text(size: 11pt)[
    The objective of this assignment is to model an uncontrolled inverted pendulum on a cart in two independent simulation environments and compare their predictions. The pendulum is released near the upright position with no force applied to the cart, so it falls, swings, and gradually settles hanging below the pivot while the cart moves in response. The system is modeled first in Simulink, directly from the equations of motion, and second in Simscape Multibody, from physical components. Agreement between the two implementations serves as a cross-check on both, and the Simulink model will carry forward into the remaining mini-projects.
  ]
]

#columns(2, gutter: 0.25in)[
= METHODOLOGY.

  The pendulum is modeled as a massless rod of length $ell$ with a point mass $m$ at its tip. The rod is pinned to a cart of mass $M$ that translates along a frictionless horizontal track. The pivot is modeled with viscous rotational damping of coefficient $c_theta$, and this is the only source of energy dissipation in the system. The sign conventions follow the assignment handout, with $x$ positive to the right and $theta$ measured from the upright vertical. All parameters take the suggested values from the handout. The equations of motion, obtained from Lagrange's equations, are

$
(M + m) dot.double(x) + m ell cos(theta) dot.double(theta)
- m ell sin(theta) dot(theta)^2 = 0,
$

and

$
m ell cos(theta) dot.double(x) + m ell^2 dot.double(theta)
+ c_theta dot(theta) - m g ell sin(theta) = 0.
$

== SIMULATION STEPS.

  In Simulink, the equations of motion are written in mass-matrix form inside a MATLAB function block, which solves the coupled $2 times 2$ linear system for $dot.double(x)$ and $dot.double(theta)$ at each time step given the current $theta$ and $dot(theta)$. Each acceleration then passes through two cascaded integrators to produce velocity and position, which close the feedback loop and are logged to output blocks. The block diagram and the function-block code appear in the appendix.

  The Simscape Multibody model is assembled from physical components. A world frame and mechanism configuration block establish the coordinate system and gravity, a prismatic joint carries the cart mass along the track, a revolute joint with viscous rotational damping attaches the pendulum, a rigid transform sets the pendulum length, and a point mass terminates the rod. Motion sensors on the two joints record the cart position and pendulum angle. A cosmetic ruler block draws a reference scale in the Mechanics Explorer.

  Both models start from rest with all states zero except an initial angle $theta(0) = 5 degree$, which serves as the small perturbation from upright. Both use a fixed step size of 0.01 s and are run for 10 s to capture the initial fall and for 200 s to capture the long-term decay. The logged time histories are exported from MATLAB and plotted with a common pipeline so the two models can be overlaid directly.


= RESULTS AND DISCUSSION.

  Figures 1 and 2 show the first 10 s of the response, and Figures 3 and 4 show the full 200 s. In every plot the Simscape trace (solid) and the Simulink trace (dashed) are indistinguishable at line width, confirming that the hand-derived equations of motion and the physical-component model describe the same system.
    #figure(
    lq.diagram(
    width: 100%,
    height: 1.8in,
    xlabel: [Time, $t$ (s)],
    ylabel: [Cart position, $x$ (m)],
    xlim: (0, 10),
    lq.plot(
    plot-data.time_10_s,
    plot-data.x_10_m,
    mark: none,
    stroke: solid-stroke,
    label: [Simscape],
          ),
    lq.plot(
    plot-data.time_10_s,
    plot-data.x_10_m,
    mark: none,
    stroke: dashed-stroke,
    label: [Simulink],
          ),
        ),
    caption: [Cart position over 10 s.],
      )

    #figure(
    lq.diagram(
    width: 100%,
    height: 1.8in,
    xlabel: [Time, $t$ (s)],
    ylabel: [Pendulum angle, $theta$ (degree)],
    xlim: (0, 10),
    lq.plot(
    plot-data.time_10_s,
    plot-data.theta_10_deg,
    mark: none,
    stroke: solid-stroke,
    label: [Simscape],
          ),
    lq.plot(
    plot-data.time_10_s,
    plot-data.theta_10_deg,
    mark: none,
    stroke: dashed-stroke,
    label: [Simulink],
          ),
        ),
    caption: [Pendulum angle over 10 s.],
      )

    #figure(
    lq.diagram(
    width: 100%,
    height: 1.8in,
    xlabel: [Time, $t$ (s)],
    ylabel: [Cart position, $x$ (m)],
    xlim: (0, 200),
    lq.plot(
    plot-data.time_200_s,
    plot-data.x_200_m,
    mark: none,
    stroke: solid-stroke,
    label: [Simscape],
          ),
    lq.plot(
    plot-data.time_200_s,
    plot-data.x_200_m,
    mark: none,
    stroke: dashed-stroke,
    label: [Simulink],
          ),
        ),
    caption: [Cart position over 200 s.],
      )

    #figure(
    lq.diagram(
    width: 100%,
    height: 1.8in,
    xlabel: [Time, $t$ (s)],
    ylabel: [Pendulum angle, $theta$ (degree)],
    xlim: (0, 200),
    lq.plot(
    plot-data.time_200_s,
    plot-data.theta_200_deg,
    mark: none,
    stroke: solid-stroke,
    label: [Simscape],
          ),
    lq.plot(
    plot-data.time_200_s,
    plot-data.theta_200_deg,
    mark: none,
    stroke: dashed-stroke,
    label: [Simulink],
          ),
        ),
    caption: [Pendulum angle over 200 s.],
  )

  The short-term response shows the expected behavior of the uncontrolled system. The upright position is unstable, so the 5#sym.degree perturbation grows and the pendulum falls, over-swinging past the hanging position to roughly 340#sym.degree before swinging back (Figure 2). The cart is driven in the opposite direction by the reaction force at the pivot, oscillating with an amplitude of about 0.2 m (Figure 1).

  The long-term response is governed by two conservation arguments. No external horizontal force acts on the cart--pendulum system, so horizontal momentum is conserved and the system center of mass remains fixed. The cart therefore oscillates about a fixed mean rather than drifting, and its excursion stays bounded near $plus.minus 0.2$ m for the full 200 s (Figure 3). Meanwhile the pivot damper continuously removes energy, so the swing amplitude decays and the pendulum settles toward $theta = 180 degree$, the stable hanging equilibrium (Figure 4). The decay is slow because $c_theta$ is small relative to the system inertia, which is why the 200 s window is needed to observe it.

  These results establish a validated nonlinear plant model. The agreement between the equation-based and component-based implementations gives confidence that the Simulink model, which the later mini-projects will use for control design, correctly captures the coupled cart--pendulum dynamics, including the instability of the upright equilibrium that any stabilizing controller must overcome.

]

#pagebreak()

= APPENDIX.

#figure(
  image("simulink_model_diagram.png", width: 100%),
  caption: [Editable Simulink implementation of the nonlinear mass-matrix equations.],
)

#figure(
  image("multibody_model_diagram.png", width: 100%),
  caption: [Simscape Multibody block diagram.],
)

#figure(
  image("multibody_model_mechanics_explorer.png", width: 100%),
  caption: [Mechanics Explorer view of the cart, ruler, pendulum rod, and point mass.],
)

The MATLAB function block below implements the equations of motion in the Simulink model.

#show raw.where(block: true): it => block(
  width: 100%,
  fill: rgb("#ECECEC"),
  stroke: 0.5pt + rgb("#A2A2A2"),
  inset: 9pt,
)[
  #set text(font: "DejaVu Sans Mono", size: 8pt)
  #it
]

#raw(read("simulink_accelerations.m"), lang: "matlab", block: true)
