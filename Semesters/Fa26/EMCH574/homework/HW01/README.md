# Homework 01.

J.C. Vaught.

`HW01_EMCH574.pdf` is the corrected, unsolved assignment, restored with its LaTeX source from commit `cb5c53a`. It contains 28 pages, the custom assignment figures, and the prompt corrections agreed for B.4, C.5, and C.9.

`HW01_EMCH574_original.pdf` is the professor's original 33-page document.

The 58-page solved document previously occupying `HW01_EMCH574.pdf` has been removed from the current folder. Its PDF and main LaTeX source remain recoverable from commit `7f447236d2ff0a054a0ad57b41539dbf2d22e44d` at those same paths.

The existing `solutions/` fragments and `study/` calculation files are retained as supporting work. They are not included by the restored unsolved document. The study builder compiles the current main document; it does not restore the removed solution inclusions.

To rebuild the unsolved assignment from this directory, run `latexmk -xelatex -interaction=nonstopmode -halt-on-error HW01_EMCH574.tex`. The recovered PDF itself is the exact version stored at `cb5c53a`; rebuilding uses the current shared styles and figure assets.
