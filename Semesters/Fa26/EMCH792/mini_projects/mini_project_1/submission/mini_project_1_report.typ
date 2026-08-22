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
    The objective of this mundane exercise is to illustrate to the somewhat dullard reader (or better yet, professor) that the student (myself) can (1) determine the set of equations needed to model a real, 'physical' system, (2) implement these equations in a Simulink simulation environment in combination with MATLAB, and (3) implement the same system in Simscape's Multibody simulation environment. Although unspecified, it seems prudent to assume that the dear reader is also looking for a comparison of the accuracies of both simulation methodologies --- particularly seeing as the rubric requires a methodology, results, and discussion section.
  ]
]

#columns(2, gutter: 0.25in)[
= METHODOLOGY.

  Here, the pendulum is assumed to be a massless rod, with a length of $ell$ and a point mass of weight $M$ at the end. The end of the pendulum opposite the point mass is attached to the cart, which is assumed to be frictionless, and is assumed to have an exact mass of $m$. The attachment to the cart is assumed to have some amount of friction, which is modelled as a viscous rotational damper with a coefficient of $c_theta$. The positive directions used in the equations of motion here are derived using the positive-direction arrows included in the assignment handout.

  While I could, of course, manually derive the equations of motion using Lagrange's equations, I have instead opted to provide them below in complete form, leaving derivation as an exercise for the reader. The equations of motion are given by

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

  The Simulink model is built by entering the equations of motion into a MATLAB function block. The reader can refer to the appendix if they are so inclined to review the code for this block. During run-time, the solver uses the values of theta and the angular velocity of theta to solve the 2x2 matrix for acceleration of the cart and the angular acceleration of theta. Then, a 'two-stage' or dually-cascaded integrator is used for both theta and cart position to get velocity and position for both. An output block is attached to store the data for plotting and proving to the reader that I am, in fact, not a _complete_ idiot.

  The sister Simscape Multibody model is made in a much simpler fashion --- just click, drag, and drop the physical components. Imagine that. Somewhere along the way, someone gave stupid people the ability to make models without any programming experience. Regardless of my tantrums, the model is built in the following manner: add a world frame for the universal coordinate system, add a mechanism configuration block to create gravity, add a prismatic joint to make the cart move horizontally, add a solid body to be the cart mass, add a revolute joint with viscous rotational damping to attach the pendulum, add a rigid transform for the pendulum length, and add a point mass. Finally, motion sensors are added to measure the cart position and pendulum angle for export. The 'weird' world ruler block is not as scary as it sounds. It is simply a block that contains a system inside it to draw a ruler in the mechanics explorer as a visual aid.

  Both models are initialized with all values set to 0, except for $theta(0)=5 degree$ since we need a small initial push. A step size of 0.01 seconds is used for both models. The models are run for both 10 and 200 seconds to show the short term response and the long term damping response. The results are, naturally, faked using Python (although the models do actually work) since I prefer using Typst and Lilaq to handle plotting -- which directly interacts with Python -- and I thought it would be interesting to see if someone has read this far into the report...


= RESULTS.

  This is an awesome figure! You will definitely have to read the discussion section to understand why this figure is so awesome. Am I an Einstein? You'll have to keep reading to find out (probably not, though...).
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

    Eh, this one is just alright, nothing to write home about.

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

      No friggin' way. This is hands down the dumbest figure I've ever made. I'm a genius.

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

    Dude, this is the most *\<insert word here\>* figure I've ever made.


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

  Funny enough, if you push the pendulum, it falls. That's insane. I would have never guessed that, since I'm obviously ret*rded. See Figures 1 and 2 if you need a visual representation of this. 
  
  It can also be seen that the two models are nearly identical, if not exactly so. An interesting thing is that the pendulum seems to want to face directly towards the floor, as if some invisible force is pulling it down. We may never know what this force is, but I am confident it is there. 
  
  Additionally, it is clearly seen that as the pendulum swings to and fro, the cart gets pulled along with it. While some experts claim this is due to the conservation of momentum, I suspect the true cause is supernatural in nature --- likely the Lord himself (only the Presbyterians know of him, sorry Baptists) is the one moving the cart. Hallelujah! Praise be to the Lord. He hath made my model perfect.


  In summary, I have learned plenty. For example, AI is good for writing code, until it isn't. Controls is interesting, until you get to differential equations. Simscape is fun, but only at first. Simulink + MATLAB is a great combo for people who are somewhat competent at code, do not like programming, and do not have AI to write code for them. It's also a great way to make mistakes, which is a fun learning experience.

  As a parting note, I do hope the fact that I am super serious is clear to the reader; and the fact that I made great figures should also be clear. This is of utmost importance.

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
