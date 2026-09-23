# EMCH 574 Test 1 solutions

J.C. Vaught.

`Test01_EMCH574_solved.pdf` contains worked solutions for the ten populated problems in the supplied Test 1. Its editable source is `Test01_EMCH574_solved.tex`. The assignment PDF and DOCX are preserved in `source/`.

The document, problem solutions, MATLAB scripts, static illustrations, and Typst figures were copied from EMCH 574 HW01 and adapted to the Test 1 inputs. The original teal and orange formatting and code style are retained. Every solved problem includes a diagram; B.5 reuses the HW01 spring-mass-damper diagram because its assignment statement has no figure. Some unused HW01 solution and figure files remain in the copied folders as references; the Test 1 document includes only A.2, A.3, B.3, B.4, B.5, B.7, B.8, C.4, C.6, and C.8.

Run `run_all` from `matlab/` to recalculate the numbers and update the plot data. Run `make` from `figures/` to rebuild the Typst PDFs. Build the document with `latexmk -xelatex -interaction=nonstopmode -halt-on-error Test01_EMCH574_solved.tex` from this folder. The compiled PDF includes the shared MATLAB functions as an appendix.
