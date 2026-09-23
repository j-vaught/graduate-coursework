# Test 1 figures.

This folder holds the HW01 figures reused for Test 1. Editable Typst sources belong in `src/`, and compiled PDFs belong in `generated/`. The shared workshop retains its original copies.

From this directory, run `make` to compile all local Typst figures, or `make figure FIGURE=src/figure-name` to compile one. Include compiled figures from the homework document with `figures/generated/figure-name.pdf`.

Typst sources import `/typst-figures/styles/figure.typ` and compile with the parent homework directory as the project root. Styles remain shared with the reference workshop. Changes to a local figure do not update the shared source copy automatically.
