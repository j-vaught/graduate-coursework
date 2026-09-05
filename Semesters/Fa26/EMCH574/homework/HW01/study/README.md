# EMCH 574 HW01 study package.

J.C. Vaught.

Open `output/pdf/HW01_worked_solutions.pdf` for the course-note map and worked solutions to A.1–A.3, B.1–B.8, and C.1–C.9. Open `output/interactive.html` in a browser for offline hover data tips, zooming, and curve comparisons.

The source assignment and its diagrams remain in the parent directory. The guide identifies course-note errors, model assumptions, numerical precision conventions, and the original MATLAB submission-language uncertainty. C.7–C.8 use the specific reduced approximation on course-note PDF page 252.

Run the following commands from this directory. Pandoc and XeLaTeX must also be installed for PDF compilation.

```sh
uv sync
uv run ruff format .
uv run ruff check . --fix
uv run ty check .
uv run python build.py
```

Edit `inputs.json` to change numerical inputs and `solutions_source.md` to change the explanatory text. The builder regenerates `solutions.md`, all figures, numerical results, the A.2 CSV table, the interactive HTML, and the PDF. `output/verification.json` records numerical integration comparisons and final-crossing checks. Full precision is retained in data exports; rounding applies only to display tables.

Python plotting is used under the explicit request for this assignment. Figures use the specified garnet, black, and accent palette. Local calculation and rendering require no account or hosted service. The HTML includes its plotting library and works offline.
