# Homework 01.

J.C. Vaught.

`HW01_EMCH574_solved.pdf` contains the solutions and their runnable MATLAB sources. `HW01_EMCH574.pdf` is the corrected unsolved assignment, and `HW01_EMCH574_original.pdf` is the original assignment.

C.7 and C.8 use the flex-beam-pendulum approximation on PDF page 252 of `../../lectures/EMCH574_CourseNotes_20260826.pdf`. The primary frequency is $\omega_n=\sqrt{3EI/(mL^3)+3g/(2L)}$. The tension-loaded beam model appears only as a separately identified comparison. Clear sign and resonance-threshold errors in the notes are identified in the relevant solutions rather than propagated.

Run `run_all` from the `matlab/` directory in MATLAB. It executes all eleven numerical problem scripts, displays SI inputs and results, writes `matlab/output/results.txt`, checks initial conditions, and regenerates the numerical JSON data for the solution figures. `verify_hw01` independently compares free responses with a matrix-exponential solution and checks forty settling cases with varying inputs. Individual problem scripts can also be run from that directory.

The MATLAB files are included directly in the document through `lstinputlisting`. Shared numerical and plotting functions are printed in the final section. All calculations use SI units, with explicit conversion at display boundaries. The settling routine assumes an underdamped release with zero initial velocity and locates the final threshold crossing after the last extremum outside the specified band. The result is distinguished from the conservative envelope bound.

From `figures/`, run `make` to compile the local Typst figures. Numerical response figures use the established homework palette, with teal primary curves and orange secondary curves. The local style in `figures/styles/response.typ` imports that shared palette. MATLAB uses the same colors, and the printed code has a light-gray background. The compiled figures and their data are retained for reproducibility.

From this directory, rebuild the solved document with `latexmk -xelatex -interaction=nonstopmode -halt-on-error HW01_EMCH574_solved.tex`. The original course-notes PDF and unsolved assignment are separate reference documents.
