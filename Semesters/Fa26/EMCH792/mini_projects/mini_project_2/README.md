# Mini Project 2

The assignment is in `mini-project-2.pdf`. The copied `inverted_pendulum_simulink.slx` and `simulink_accelerations.m` preserve the Mini Project 1 starting point. The other copied Mini Project 1 files remain as references.

Run `run_project2` in MATLAB from this folder. It derives the state-space controller, builds `inverted_pendulum_controlled.slx` from the copied model, runs the required tests and stress cases, and writes the results and figure data. The model builder uses `controlled_accelerations.m` for the new cart-force input. Re-running the script recreates the controlled model.

Compile the report with `typst compile mini_project_2_report.typ mini_project_2_report.pdf` after the MATLAB run. The report source imports the MATLAB-generated JSON and the exported Simulink diagram.
