# HW01 calculations and solution source.

J.C. Vaught.

The deliverable is the parent directory's `HW01_EMCH574.pdf`, built from the existing rewritten homework document. This directory contains the Python numerical engine and explanatory source for the worked solutions.

Edit `inputs.json` for input values and `solutions_source.md` for the mathematical explanation. The build inserts one generated solution fragment beneath each problem in `HW01_EMCH574.tex`. It uses the local homework Typst facade, Lilaq, and CeTZ for all figures. Python does not draw figures.

Run the following commands here. Typst, Pandoc, latexmk, and XeLaTeX must also be installed.

```sh
uv sync
uv run ruff format .
uv run ruff check . --fix
uv run ty check .
uv run python build.py
```

`output/results.json` retains full precision and units, `output/A2_lengths.csv` stores the pendulum table, and `output/verification.json` records the analytical-versus-numerical checks. The plotted data are JSON files alongside the solution Typst sources in the homework figure library. Event markers are evaluated from the analytical expressions, including the exact final 2% crossing.

The former standalone study guide and raster plotting outputs have been replaced by the solved homework and the Typst figure pipeline. The build selects the homework's teal, orange, and neutral palette without changing the default palette of unrelated reference figures.
