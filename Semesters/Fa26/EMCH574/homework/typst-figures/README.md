# EMCH 574 Typst figure workshop

This directory is the local figure workshop for the EMCH 574 homework set. It preserves the complete Typst figure system imported from [`j-vaught/Engineering-Control-Systems`](https://github.com/j-vaught/Engineering-Control-Systems) at commit `07a8ff9edde045f776b3ca29939d86273da65a71`.

The public entry point is [`styles/figure.typ`](styles/figure.typ). It imports the shared color, typography, dimension, control-diagram, mechanics, and Lilaq plot modules. New homework figures should import only that facade.

The imported production sources are unchanged and retain their upstream paths under [`src/ch01`](src/ch01) and [`src/ch02`](src/ch02). Their matching committed PDFs retain the same hierarchy under [`generated/ch01`](generated/ch01) and [`generated/ch02`](generated/ch02). The visual specimens and their PDFs live under [`tests/specimens`](tests/specimens) and [`generated/specimens`](generated/specimens). New assignment-specific sources belong under [`src/homework`](src/homework), with generated PDFs written to `generated/homework`.

The local installation provides Typst 0.15.1. The imported sources were authored for Typst 0.15.0 and compile successfully with the local patch release.

## Build one figure

Run the following command from this directory. The `.typ` suffix is optional.

```sh
make figure FIGURE=src/ch01/ch01_cs_closed_loop
```

The build preserves the source hierarchy. The example writes `generated/ch01/ch01_cs_closed_loop.pdf`. A homework source such as `src/homework/HW02/pendulum.typ` writes `generated/homework/HW02/pendulum.pdf`.

## Build figure groups

The following commands rebuild the imported reference figures, the specimens, the homework figures, or every figure respectively.

```sh
make reference-figures
make specimen-figures
make homework-figures
make figures
```

Each build uses the directory itself as the Typst project root, ignores system fonts, and sets a deterministic source epoch. CeTZ and Lilaq remain pinned by the shared style modules.

## Create a homework figure

Start from the source pattern documented in [`src/homework/README.md`](src/homework/README.md). Use `src/ch01` and `src/ch02` to borrow established layouts and component constructions. Keep colors, text settings, dimensions, arrows, line weights, and plot styles in the shared modules so the assignment figures remain visually consistent.

The original upstream figure-system documentation is preserved in [`UPSTREAM_FIGURE_SYSTEM.md`](UPSTREAM_FIGURE_SYSTEM.md). Its paths and repository-level commands describe the textbook repository and are retained for reference.
