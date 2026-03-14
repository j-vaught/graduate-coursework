#set page(
  paper: "us-letter",
  margin: 1in,
  header: context {
    set text(size: 10pt)
    grid(
      columns: (1fr, 1fr, 1fr),
      align: (left, center, right),
      [Page #counter(page).display()],
      [CSCE 763],
      [JC Vaught],
    )
  },
)

#set par(justify: false, leading: 0.65em)
#set text(size: 12pt, font: "Times New Roman")

#let double_rule() = {
  v(0.2cm)
  line(length: 100%)
  v(0.1cm)
  line(length: 100%)
  v(0.3cm)
}

#let qtitle(t) = {
  pagebreak()
  v(0.5cm)
  [*#t*]
  double_rule()
}

#let toc_line(left, right) = {
  grid(columns: (1fr, auto), [#left], [#right])
}

#align(center)[
  #set text(size: 20pt, weight: "bold")
  CSCE 763: Digital Image Processing
  \
  Homework \#1
]

#v(0.6cm)

#align(center)[
  Instructor: Spring 2026
  \
  University of South Carolina
  \
  #emph[Solutions by: JC Vaught]
]

#v(0.3cm)

#align(center)[Due: 1:15 pm EST, Tuesday, Feb 3]

#v(0.8cm)

#align(center)[
  #block(
    stroke: rgb("#5C5C5C"),
    fill: white,
    inset: 12pt,
    radius: 0pt,
    width: 100%,
  )[
    #align(center, text(size: 16pt, weight: "bold")[Table of Contents])
    #v(0.3em)

    #toc_line([*Problem 1: Smallest Discernible Dot (25 pts)* ........................................], [*2*])
    #toc_line([*Problem 2: Adjacency of Image Subsets (25 pts)*], [])
    #toc_line([Part (a): 4-adjacency .................................................................], [*3*])
    #toc_line([Part (b): 8-adjacency .................................................................], [*3*])
    #toc_line([Part (c): m-adjacency .................................................................], [*3*])
    #toc_line([*Problem 3: Shortest Paths (25 pts)*], [])
    #toc_line([Part (a): $V = {0, 1}$ .................................................................], [*4*])
    #toc_line([Part (b): $V = {1, 2}$ .................................................................], [*4*])
    #toc_line([*Problem 4: Set Expressions (25 pts)* .................................................], [*5*])
  ]
]

#qtitle([Problem 1: Smallest Discernible Dot (25 pts)])

Thinking purely in geometric terms, estimate the diameter of the smallest printed dot that the eye can discern if the page on which the dot is printed is 0.5 m away from the eyes.

*Assumptions*

1. The distance between the center of the lens and the retina along the visual axis is 14 mm.
2. The visual system ceases to detect the dot when the image of the dot on the fovea becomes smaller than the diameter of one receptor (cone) in that area of the retina.
3. The fovea can be modeled as a square array of dimensions $1.5 "mm" times 1.5 "mm"$, and the cones (about $337,000$ in total) and spaces between the cones are distributed uniformly throughout this array.

#qtitle([Problem 2: Adjacency of Image Subsets (25 pts)])

Consider the two image subsets $S_1$ and $S_2$ shown below. For $V = {1}$, determine whether these two subsets are (a) 4-adjacent, (b) 8-adjacent, or (c) m-adjacent.

#align(center, image("assets/problem2.svg", width: 86%))

#qtitle([Problem 3: Shortest Paths (25 pts)])

Consider the image segment shown below.

1. Let $V = {0, 1}$ and compute the lengths of the shortest 4-, 8-, and m-path between $p$ and $q$. If a particular path does not exist between these two points, explain why.
2. Repeat for $V = {1, 2}$.

#align(center, image("assets/problem3.svg", width: 52%))

#qtitle([Problem 4: Set Expressions (25 pts)])

Give expressions for the sets shown shaded in the following figure in terms of sets $A$, $B$, and $C$. The shaded areas in each figure constitute one set, so give one expression for each of the three figures.

#align(center, image("assets/problem4_abc.svg", width: 95%))

#v(0.5cm)
#line(length: 100%)
#v(0.5cm)

#align(center, image("assets/problem4_shaded.svg", width: 98%))
