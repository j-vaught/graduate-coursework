# Mini Project 2

J.C. Vaught.

Run `run_project2` in MATLAB from this folder. It computes the gain with `design_controller.m`, compares the linear and nonlinear models near upright, verifies the linear closed-loop response, and builds the editable `inverted_pendulum_controlled.slx` from the inherited `inverted_pendulum_simulink.slx`. It then runs 30 s release tests at 5, 10, 20, 30, 45, and 60 degrees and random-force tests at bounds of 2.5, 5, 7.5, and 10 N. MATLAB, Simulink, and Control System Toolbox are required.

The script writes `metrics.json`, `plot_data.json`, and the two Simulink diagram images used by the report. The plot data include every sweep response, the linearization comparison, and the original held random-force sequence. The seed is 79202, the force update interval is 0.1 s, and the actuator command limit is 10 N.

Compile with `typst compile mini_project_2_report.typ mini_project_2_report.pdf`. The committed JSON files, diagrams, MATLAB functions, and `references.bib` allow the report to compile without rerunning MATLAB. All report text is single column, and all figures span the page text width. Figure 1 uses Lilaq legends at bottom left in panel (a) and top left in panel (b). Figure 2 uses one Lilaq legend at top left in panel (a), and Figure 3 uses one default Lilaq legend in panel (a). The main report contains the introductory design narrative, Results, and Discussion. Results begins on the first page, followed by the compact sweep figures on the second page. Its appendices follow their first references and merge the equations and linearization, controller design and function code, system diagrams, random-force protocol, and detailed results.
