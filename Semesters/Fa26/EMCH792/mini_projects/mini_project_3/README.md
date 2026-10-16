# Mini Project 3. LQR starting material

The original handout is `mini-project-3.pdf`. It requires LQR design about upright, application to the nonlinear model, a perturbed-upright test, comparison with the Mini Project 2 pole-placement controller, angle and control-force plots, and a discussion of the state and input weights.

`inverted_pendulum_lqr.slx` retains the manually aligned nonlinear plant and feedback diagram with the existing LQR gain. `design_lqr_controller.m` calculates that gain from Q = diag([4 2 300 10]) and R = 0.5. `controlled_accelerations.m` documents the equations already embedded in the model.

`lqr_starting_material/` preserves previous LQR test data. These are historical results for reuse, not a completed Project 3 comparison. `lqr_weight_studies.m` is the reused linear weight-study function, adapted to call `design_lqr_controller.m`; it writes fresh results to `controller_studies.json` when run from this folder. It has not yet been re-run here.

The remaining Project 3 work is a matched comparison against the revised Project 2 pole-placement gain, using identical initial conditions, plant parameters, force limits, solver settings, and observation time. Re-run both controllers and report angle, cart motion, and applied force. The old LQR report stays preserved in the Project 2 directory.

Before running this starting model, define `disturbance_signal = [0 0;30.1 0];` in MATLAB. Set the nonlinear plant Angle integrator initial condition to `5*pi/180` for a 5-degree release. The copied model is reference material; the matched LQR-versus-pole-placement runner is still to be written.
