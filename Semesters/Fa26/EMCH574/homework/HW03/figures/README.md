# HW03 figures.

This folder owns the figures used by HW03. Existing extracted raster images remain here. Editable Typst sources belong in `src/`, and compiled PDFs belong in `generated/`. The shared workshop retains its original copies.

From this directory, run `make` to compile all local Typst figures, or `make figure FIGURE=src/figure-name` to compile one. Include compiled figures from the homework document with `figures/generated/figure-name.pdf`.

Typst sources import `/typst-figures/styles/figure.typ` and compile with the parent homework directory as the project root. Styles remain shared with the reference workshop. Changes to a local figure do not update the shared source copy automatically.
