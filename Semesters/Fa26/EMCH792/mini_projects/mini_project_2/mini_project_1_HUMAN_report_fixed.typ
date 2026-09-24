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
  #text(size: 17pt, weight: "bold")[A few models of an uncontrolled inverted pendulum on a cart]

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
    The objective of this exercise is to demonstrate that the student (myself) can (1) determine the set of equations needed to model a real, physical system, (2) implement these equations in a Simulink simulation environment in combination with MATLAB, and (3) implement the same system in Simscape's Multibody simulation environment. Although unspecified, it seems prudent to assume that the reader is also looking for a comparison of the accuracies of both simulation methodologies --- particularly seeing as the rubric requires a methodology, results, and discussion section.
  ]
]

#columns(2, gutter: 0.25in)[
= METHODOLOGY.

  Here, the pendulum is assumed to be a massless rod, with a length of $ell$ and a point mass $m$ at the end. The end of the pendulum opposite the point mass is attached to the cart, which has a mass of $M$ and rides on a frictionless horizontal track. The attachment to the cart is assumed to have some amount of friction, which is modelled as a viscous rotational damper with a coefficient of $c_theta$. The positive directions follow the arrows included in the assignment handout.

  The equations of motion are derived using Lagrange's equations, with the cart position $x$ and the pendulum angle $theta$ as the generalized coordinates. Skipping the intermediate algebra, the resulting equations of motion are given by

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

  The Simulink model is built by entering the equations of motion into a MATLAB function block. The reader can refer to the appendix if they are so inclined to review the code for this block. During run-time, the solver uses the current values of $theta$ and $dot(theta)$ to solve the coupled $2 times 2$ linear system for the cart acceleration and the angular acceleration. Then, a 'two-stage' or dually-cascaded integrator is used for both $theta$ and cart position to get velocity and position for both, closing the feedback loop. An output block stores the data for plotting.

  The sister Simscape Multibody model is made in a much simpler fashion --- just click, drag, and drop the physical components, with no equation derivation required. The model is built in the following manner: add a world frame for the universal coordinate system, add a mechanism configuration block to create gravity, add a prismatic joint to make the cart move horizontally, add a solid body to be the cart mass, add a revolute joint with viscous rotational damping to attach the pendulum, add a rigid transform for the pendulum length, and add a point mass. Finally, motion sensors are added to measure the cart position and pendulum angle for export. The 'weird' world ruler block is not as scary as it sounds. It is simply a block that contains a system inside it to draw a ruler in the mechanics explorer as a visual aid.

  Both models are initialized with all values set to 0, except for $theta(0)=5 degree$ since we need a small initial push. A step size of 0.01 seconds is used for both models. The models are run for both 10 and 200 seconds to show the short term response and the long term damping response. The logged time histories are exported from MATLAB to a JSON file, since I prefer using Typst and Lilaq to handle plotting, which imports the data directly.


= RESULTS.

  Figures 1 and 2 show the first 10 seconds of the response, and Figures 3 and 4 extend the same signals to 200 seconds. In every figure, the Simscape trace (solid) and Simulink trace (dashed) lie directly on top of one another.
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

    The cart oscillates back and forth with an amplitude of roughly 0.2 m, driven entirely by the reaction force at the pivot as the pendulum swings.

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

      The pendulum falls away from the unstable upright position, over-swings well past the hanging position, and then begins oscillating about $theta = 180 degree$.

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

    Over the long run, the cart never drifts away. It oscillates about a fixed mean while the amplitude slowly shrinks.


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


= DISCUSSION.

  The short-term behavior is exactly what one would expect from an uncontrolled inverted pendulum. The upright position is unstable, so the small 5#sym.degree perturbation grows and the pendulum falls, as seen in Figures 1 and 2.

  It can also be seen that the two models are nearly identical, if not exactly so. The hand-derived equations of motion and the click-and-drag physical model describe the same dynamics, so an error in either one would have shown up as a visible gap between the solid and dashed traces.

  Additionally, it is clearly seen that as the pendulum swings to and fro, the cart gets pulled along with it. This is a direct consequence of conservation of momentum. No external horizontal force acts on the system, so the center of mass stays fixed and the cart oscillates about a constant mean. Meanwhile, the viscous damper at the pivot slowly bleeds energy out of the swing, so the pendulum settles toward the hanging position at $theta = 180 degree$ in Figure 4. The decay takes the full 200 seconds because $c_theta$ is small.

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

This is the custom MATLAB function block used in Simulink model.

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
