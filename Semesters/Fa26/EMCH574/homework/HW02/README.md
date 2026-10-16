# EMCH 574 Homework 02

J.C. Vaught.

`HW02_EMCH574.pdf` is the formatted, unsolved assignment, and `HW02_EMCH574.tex` is its editable source. The newly supplied `source/HW02_EMCH574.docx` is preserved unchanged. `HW02_EMCH574_original.pdf` is the earlier instructor PDF of the same assignment.

`HW02_EMCH574_solved.pdf` adds the completed solutions for A.1 through A.3 to the assignment. Its source is `HW02_EMCH574_solved.tex`, with the answer text in `solutions/`. A.1 includes Typst wave sketches, and A.3 includes the road profile and car-response plots. The runnable MATLAB sources are `matlab/A2.m` and `matlab/A3.m`. The microwave-door discussion uses the reported measurements of an Oster small office microwave. Supporting sources are collected in `references.bib`.

The document uses the shared HW01 homework style. Its five problem images are inserted directly from the DOCX files in `figures/original/`; no image was redrawn or recolored. The two slide-whistle photographs are oriented by LaTeX at display time, with their source bytes unchanged. The earlier PDF-extracted images remain in `figures/` as references.

The source does not state a due date, so the title retains `TBD`. Rebuild the assignment from this directory with `latexmk -xelatex -interaction=nonstopmode -halt-on-error HW02_EMCH574.tex`, or build the solution version with `latexmk -xelatex -interaction=nonstopmode -halt-on-error HW02_EMCH574_solved.tex`. Run `make` in `figures/` to rebuild the new sketches.
