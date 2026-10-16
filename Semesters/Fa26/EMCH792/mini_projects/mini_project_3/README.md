# Mini Project 3. LQR control of the inverted pendulum

The completed report is `mini_project_3_report.pdf`. It has two main pages and two supporting appendix pages, using the same fonts, colors, margins, heading styles, gray code boxes, and aligned Simulink diagrams as Project 2. The original assignment is `mini-project-3.pdf`.

## Run and rebuild

Run `run_project3` in MATLAB R2025a with Simulink and Control System Toolbox. The runner uses the existing `inverted_pendulum_lqr.slx`, updates its gain without rearranging blocks or connectors, and saves a standalone baseline model. `design_lqr_controller.m` defines the upright linearization and Q = diag([4 2 300 10]), R = 0.5. The nonlinear acceleration equations are embedded in the model; `controlled_accelerations.m` provides their readable source.

Compile with `typst compile mini_project_3_report.typ mini_project_3_report.pdf`. The committed `project3_results.json` and diagram images allow compilation without MATLAB. All report plots are generated in Typst with Lilaq. The MATLAB assertions are kept in the verification runner, outside the short report code listings.

## Experiments and verification

Ten nonlinear runs use the same plant, 10 N actuator limit, zero disturbance, 30 s duration, 0.01 s maximum solver step, and 0.02 s analysis grid. Six runs compare pole placement with baseline LQR at 5, 10, and 20 degrees. Four additional 5-degree runs vary the angle penalty to 100 or 900 and the force penalty to 0.1 or 2; the shared baseline is reused in both sweeps. Every test starts with zero cart position and zero velocities.

Joint settling requires angle within 1 degree and cart position within 0.05 m thereafter. A 90-degree crossing marks failure. Failed histories and travel stop at the first sampled crossing. Force effort is the integral of applied force squared, and is compared over the same 30 s only for recovered runs. The JSON also stores finite-horizon cost evaluated using the same baseline Q and R for every controller, not each controller's own objective.

`pole_placement_reference.json` carries the actual Project 2 gain, matrices, and nominal trace. The Project 3 pole-placement trace reproduces that reference. Baseline LQR is checked against an independent integration of the exact nonlinear equations and a Riccati residual check. The saved model is reopened and tested independently with its embedded workspace data. These checks and their numerical residuals are recorded in `project3_results.json`.

At 5 degrees, pole placement jointly settles in 2.76 s and LQR in 4.24 s. LQR reduces force effort from 6.016 to 5.144 N² s, while peak cart travel increases from 0.276 to 0.301 m. At 20 degrees, this LQR gain recovers in 7.88 s with 2.977 m peak cart travel; the Project 2 pole-placement gain fails at 1.92 s. The report explains this tradeoff without treating LQR as a fastest-settling controller.

## Share the model

`inverted_pendulum_lqr.slx` embeds the baseline gain, zero disturbance data, and a default 5-degree release. Another person can open and simulate this file using MATLAB and Simulink without helper scripts or external data. Changing the controller weights or rerunning the verification script additionally requires Control System Toolbox.

## Historical reference material

`lqr_starting_material/` and `lqr_weight_studies.m` preserve the earlier LQR data and linear weight-study source. They are not used for this report's results or figures. The current evidence comes from `run_project3.m` and `project3_results.json`.
