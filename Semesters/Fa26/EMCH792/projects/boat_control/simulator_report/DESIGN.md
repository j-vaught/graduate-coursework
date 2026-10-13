# Simulator report production contract

The authoritative report source is `../simulator_report.tex`, with J.C. Vaught as author. Keep the report grounded in the simulator implementation and preserve the distinction between configured simulation behavior and measured boat performance. The companion controller report documents feedback algorithms. The simulator report retains six sections and excludes the former architecture chapter.

## Writing

Edit prose, equations, nested bullets, captions, and tables directly in LaTeX. Use section and subsection headings, a connecting paragraph at each transition, and nested bullets up to three levels for purpose, mechanism, and practical consequences. Define symbols and units in narrative context before displaying equations. End statements with periods. Keep captions short. Preserve the manufacturer's values, configuration assumptions, numerical approximations, and worked examples already documented. Store citations in the project-level `references.bib`.

The build does not convert or regenerate prose. Original Typst report and chapter files remain historical material. Complete parameter tables are an editable snapshot of the baseline configuration and must be reviewed when the model defaults change.

## Figure language

Each active figure is a standalone document under `figures/standalone/`, compiled to a one-page PDF beside its source. LaTeX imports that PDF with `\includegraphics`. Author every figure in Typst with CeTZ 0.4.2 or Lilaq 0.6.0. Use `style.typ` for the established navy/teal diagram language and standard quantitative plot colors. Retain data under `data/`. Use square corners, high contrast, filled stealth arrows, a white background, and 9 pt figure text. Label axes, units, and the signals carried by arrows. Do not route connectors through labels.

Standalone sources set a 7.06 in page width, automatic page height, and zero page margins. They import `../../style.typ` and reference `../../data/`. Keep the shared style and JSON dependencies inspectable. Avoid rasterized plots and LaTeX drawing packages.

## Build and verification

Run `uv run python simulator_report/scripts/build_latex.py` from the project directory. This compiles the eight Typst figures, runs pdfLaTeX and BibTeX through `latexmk`, and copies the finished PDF to the report's existing path. The `--skip-figures` option rebuilds after text edits, and `--figures-only` updates only the figure PDFs.

Inspect the final PDF, verify section/equation/figure numbering and references, and render pages for visual review. Keep figure PDFs and report PDFs tracked. Put compilation intermediates and inspection images under ignored `build/` directories.
