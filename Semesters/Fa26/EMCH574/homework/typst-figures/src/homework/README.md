# Homework figure sources

Place new assignment figures in a directory matching the homework number, such as `HW01`, `HW02`, or `HW03`. Use lowercase kebab-case for the figure filename.

Every figure should import the shared facade and use the standalone wrapper. A control or engineering diagram begins with the following source.

```typst
#import "/styles/figure.typ": *

// figure-pipeline: kind=diagram
#standalone(
  cetz-canvas({
    // Construct the diagram with CeTZ and the shared semantic styles.
  }),
)
```

Shared homework constructors are defined in `../../styles/homework-components.typ`. The current set provides the textbook-style fixed supports, pendulum schematic, projectile indicator, horizontal spring-mass schematic, tip-mass cantilever, and hanging flex-beam used by HW01. The pendulum constructor uses a circular bob, while the spring-mass constructor retains a square translating mass. The cantilever and hanging flex-beam constructors keep repeated challenge-problem geometry consistent.

Mechanical schematics use `kind=mechanics`. Quantitative plots use `kind=plot`, declare a `width-profile=full` or `width-profile=half` comment, and call `book-diagram` so that Lilaq receives the common plot theme.

Compile a new figure from the `typst-figures` directory. For example, `make figure FIGURE=src/homework/HW02/pendulum` writes `generated/homework/HW02/pendulum.pdf`.

The imported sources in `../ch01` and `../ch02` are the preferred construction examples. Copy the nearest source into the appropriate homework directory, rename it, and then change the geometry and labels while retaining the shared style calls.
