# Homework 01.

J.C. Vaught.

`HW01_EMCH574.pdf` is the solved version of the rewritten assignment. It retains the problem statements and the custom Typst assignment figures, with a worked solution following each of the twenty problems. Graduate and optional challenge work is included.

`HW01_EMCH574.tex` is the main document. The generated solution fragments are in `solutions/`. Edit the explanatory source in `study/solutions_source.md` and the numerical inputs in `study/inputs.json` before rebuilding.

Python calculates the responses and checks them against numerical integration. The existing homework figure library renders the plots with Lilaq and the mechanical diagrams with CeTZ. The output uses a blue, orange, and neutral palette selected only for HW01. The reference figure library keeps its default palette.

Run the following commands from `study/`. The build needs uv, Typst, Pandoc, latexmk, and XeLaTeX.

```sh
uv sync
uv run ruff format .
uv run ruff check . --fix
uv run ty check .
uv run python build.py
```

The builder writes response data to `../typst-figures/src/homework/HW01/solutions/data/` relative to the homework directory, compiles the figure sources, regenerates the solution fragments, and rebuilds the main PDF. The numerical outputs and validation results are stored in `study/output/`.

The horizontal-beam section inset has its width and height labels corrected to match the original assignment. The numerical weak-axis bending model follows that corrected geometry. The flex-beam pendulum solution explicitly identifies the approximation used on course-note PDF page 252.
