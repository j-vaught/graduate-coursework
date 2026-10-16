## Verification status

This is a draft revision. MATLAB did not complete startup during preparation, so the nonlinear runs and saved gain update are unverified. The model copy still contains the original LQR gain until the runner succeeds. The design-only JSON contains an independently checked exact-rational Ackermann gain; a minimal MATLAB session returned the same gain. Simulink loading did not finish, so there are no verified nonlinear results. Build the review draft with `typst compile --input draft=true mini_project_2_pole_placement.typ mini_project_2_pole_placement.pdf`. After MATLAB runs, compile without the draft input to populate the numerical results and figures.

# Mini Project 2. Pole-placement revision

This draft addresses the grading comments with directly selected poles and a two-page main report followed by two supporting appendix pages. The original graded report and LQR results remain unchanged in the parent folder. Reusable LQR material is also staged in `../../mini_project_3/` for the next assignment.

Run `run_pole_revision` in MATLAB R2025a with Simulink and Control System Toolbox. It applies Ackermann's formula in `design_pole_controller.m`, verifies the gain against `place`, updates only the existing model's gain and default test inputs, and runs the release and random-force tests. It does not rebuild or rearrange the model.

The selected poles are -1 +/- i, -3, and -4 per second. The dominant pair gives damping ratio 0.707 and an approximate 4 s linear settling envelope. This is a local design target; the nonlinear simulations determine actual behavior with the 10 N actuator limit.

Simulation settings and all plotted histories are stored in `pole_results.json`. Release tests use 5, 10, 20, and 30 degrees. Random tests use a held uniform disturbance at 0.1 s intervals, seed 79202, and bounds of 2.5, 5, 7.5, and 10 N. Balance requires staying within 90 degrees. Release recovery additionally requires angle below 2 degrees and cart position below 0.05 m over the final 2 s. Settling time uses persistent 1-degree and 0.05 m bounds. Failed histories are truncated at the first sampled 90-degree crossing. The source retains complete test generation outside the short PDF appendix.

Compile the report with `typst compile mini_project_2_pole_placement.typ mini_project_2_pole_placement.pdf`. Figures use Lilaq. The two Simulink images retain the user's manually aligned diagrams; their vector-gain icon does not expose the numeric gain, and the new gain is specified in the report and saved model.

The saved `.slx` embeds a zero disturbance and 5-degree initial release so it runs without supporting files. Adjust the Angle integrator initial condition to change the release. Edit `disturbance_signal` in the model workspace to change the external force. The model requires MATLAB and Simulink; calculating a new gain with the supplied function uses basic MATLAB, while the verification runner uses Control System Toolbox.
