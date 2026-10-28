# EMCH 574 Test 2

Open `Test02_EMCH574_solved.pdf` for the complete solution. The editable master is `Test02_EMCH574_solved.tex`. The original assignment is retained unchanged in `source/Test_2_EMCH574.pdf`.

The solution covers A.3, A.4, A.5, B.4, B.5, B.6, and both C.3 boundary cases, including graduate work. Sections marked “Nothing here” in the assignment are identified in the test scope. The layout, class teal palette, equation formatting, tables, MATLAB listings, and reusable analytical work follow HW01, HW02, and Test01.

Problem photographs and diagrams in `figures/original/` retain their original JPEG bytes. Photographs are oriented in LaTeX. Analytical figures use the existing homework Typst styles, with sources and data in `figures/src/` and PDFs in `figures/generated/`.

Build the document from this directory with `latexmk -xelatex -interaction=nonstopmode -halt-on-error Test02_EMCH574_solved.tex`. Rebuild analytical figures from `figures/` with `make PALETTE=homework`. The shared Typst styles are in `../typst-figures/`.

Run the seven `.m` files in `matlab/` directly in MATLAB. They calculate and display results and create direct plots where requested. They do not export data files. All seven were executed in MATLAB R2025a and checked on October 28, 2026. The numerical and independent review record is in `review/verification.txt`.

B.5 uses the closed–closed whistle idealization from the course notes as its primary model and explicitly calculates the closed–open alternative. A.5 distinguishes the finite course-note chart from the unbounded equal-temperament frequency relation. B.6 uses the impedance-consistent reference pressure so that pressure and intensity decibel levels agree.
