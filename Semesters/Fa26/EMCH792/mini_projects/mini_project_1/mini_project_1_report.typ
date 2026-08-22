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
  size: 10pt,
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
#show figure.caption: set text(size: 8.5pt)

#align(center)[
  #text(size: 17pt, weight: "bold")[Nonlinear Simulation of an Inverted Pendulum on a Cart]

  #v(0.2em)
  #text(size: 10pt)[J.C. Vaught]
  #v(0.1em)
  #text(size: 9pt)[EMCH 792 — Nonlinear Systems]
]

#v(0.35em)
#block(
  width: 100%,
  inset: (x: 0pt, y: 5pt),
  stroke: (top: 0.5pt + rgb("#A2A2A2"), bottom: 0.5pt + rgb("#A2A2A2")),
)[
  #text(weight: "bold", size: 9.5pt)[OBJECTIVE.]
  #text(size: 9.5pt)[
    The objective of this assignment is to model the nonlinear motion of an unforced inverted pendulum on a freely translating cart and to compare two independent implementations. The first implementation evaluates the equations of motion directly in Simulink. The second represents the same mechanism with physical components in Simscape Multibody. The cart position $x(t)$ and pendulum angle $theta(t)$ are compared after releasing the pendulum five degrees from the unstable upright equilibrium with zero initial velocity.
  ]
]

#columns(2, gutter: 0.25in)[
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

  = Results

  #figure(
    lq.diagram(
      width: 100%,
      height: 2in,
      xlabel: [Time, $t$ (s)],
      ylabel: [Cart position, $x$ (m)],
      xlim: (0, 10),
      lq.plot(
        plot-data.time_10_s,
        plot-data.x_10_m,
        mark: none,
        stroke: solid-stroke,
        label: [SimScape],
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
      height: 2in,
      xlabel: [Time, $t$ (s)],
      ylabel: [Pendulum angle, $theta$ (degree)],
      xlim: (0, 10),
      lq.plot(
        plot-data.time_10_s,
        plot-data.theta_10_deg,
        mark: none,
        stroke: solid-stroke,
        label: [SimScape],
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
      height: 2in,
      xlabel: [Time, $t$ (s)],
      ylabel: [Cart position, $x$ (m)],
      xlim: (0, 200),
      lq.plot(
        plot-data.time_200_s,
        plot-data.x_200_m,
        mark: none,
        stroke: solid-stroke,
        label: [SimScape],
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
      height: 2in,
      xlabel: [Time, $t$ (s)],
      ylabel: [Pendulum angle, $theta$ (degree)],
      xlim: (0, 200),
      lq.plot(
        plot-data.time_200_s,
        plot-data.theta_200_deg,
        mark: none,
        stroke: solid-stroke,
        label: [SimScape],
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

  = Results and Discussion

  The five-degree perturbation grows immediately because the upright equilibrium is unstable. The pendulum falls through the downward equilibrium and continues into a damped oscillation about $theta=pi$ rad. Over 20 s, the Python reference predicts $-0.183 <= x <= 0.217$ m and $0.087 <= theta <= 5.947$ rad. The cart remains bounded because there is no external horizontal force, while pivot damping gradually removes mechanical energy and contracts the angular oscillation about the downward equilibrium.

  The Simulink and Simscape Multibody responses closely match the Python reference over the validated 20 s interval. Their maximum absolute differences are 0.014 m in $x$ and 0.056 rad in $theta$. The small phase separation late in the record is expected because the release begins near an unstable equilibrium, where small numerical and geometric differences amplify before damping dominates. The agreement supports both the nonlinear equation implementation and the orientation, gravity, damping, and sensing choices in the Multibody model.

]

#pagebreak()

= Appendix

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

The saved Simulink model contains the standard Constant, Integrator, and To Workspace blocks shown in the Direct-Equations Simulink Model figure. The only custom code needed inside the model is the MATLAB Function block that evaluates the nonlinear equations of motion.

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
