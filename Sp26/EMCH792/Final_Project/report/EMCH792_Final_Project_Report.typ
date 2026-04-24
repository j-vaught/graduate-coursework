#import "@preview/charged-ieee:0.1.4": ieee
#import "generated/results.typ": *

#show: ieee.with(
  title: [Comparison of EKF and UKF State Estimation with Measurement Gating and RK4 Propagation],
  authors: (
    (
      name: "J.C. Vaught",
      department: "Department of Mechanical Engineering",
      organization: "University of South Carolina",
      location: "Columbia, South Carolina, USA",
      email: "jvaught@sc.edu",
    ),
  ),
  abstract: [
    This report addresses the six required tasks in the EMCH792 final project for the nonlinear kinematic bicycle model. The calibration pass yielded $R_1$ = #y1_variance_text and $R_2$ = #y2_variance_text with a constant sample period of #dt_text s. The vanilla rectangular comparison favored the UKF over the EKF, reducing position RMSE from #ekf_rect_no_gate_pos_text m to #ukf_rect_no_gate_pos_text m and heading RMSE from #ekf_rect_no_gate_heading_deg_text deg to #ukf_rect_no_gate_heading_deg_text deg. A fixed scalar #chosen_gate_label normalized-innovation-squared gate with threshold #chosen_gate_threshold_text improved heading RMSE by #ekf_gating_heading_improvement_text deg for the EKF and #ukf_gating_heading_improvement_text deg for the UKF, but position RMSE increased because repeated $y_1$ rejections made the gated runs more prediction dominated. Replacing rectangular UKF propagation with RK4 reduced position RMSE by #rk4_position_improvement_text m, while the RK4 runtime increased by only #rk4_runtime_penalty_text ms relative to the rectangular UKF. Four appendix ablations test sensitivity to gate threshold, measurement subset, initial covariance scale, and UKF sigma-point spread.
  ],
  index-terms: (
    [Extended Kalman filter],
    [Unscented Kalman filter],
    [Nonlinear state estimation],
    [Measurement gating],
    [Runge-Kutta integration],
  ),
)

#let full_width_figure(path, caption) = figure(
  scope: "parent",
  placement: auto,
  image(path, width: 100%),
  caption: [#caption],
)

#let full_width_table(body, caption) = figure(
  scope: "parent",
  placement: auto,
  kind: table,
  block(width: 100%)[
    #set text(size: 8pt)
    #body
  ],
  caption: [#caption],
)

#let column_figure(path, caption) = figure(
  image(path, width: 92%),
  caption: [#caption],
)

#let column_table(body, caption) = figure(
  kind: table,
  block(width: 100%)[
    #set text(size: 8pt)
    #body
  ],
  caption: [#caption],
)

#let appendix_figure(path, caption) = figure(
  placement: none,
  image(path, width: 100%),
  caption: [#caption],
)

#let appendix_table(body, caption) = figure(
  placement: none,
  kind: table,
  block(width: 100%)[
    #set text(size: 7.4pt)
    #body
  ],
  caption: [#caption],
)

= Problem I. Calibration Variance Estimation

The first task was to estimate the two sensor variances from the calibration data and confirm the deployment sample period. The calibration pass produced $R_1$ = #y1_variance_text for the range-like measurement and $R_2$ = #y2_variance_text for the cubic heading sensor. The deployment dataset remained uniformly sampled at #dt_text s. The filters were initialized from a zero-centered prior and used the nominal base covariance so that the baseline comparison did not consume the provided truth channels as estimator inputs.

= Problem II. Vanilla EKF and UKF with Rectangular Integration

Both filters used the assignment state $x = [x, y, psi, u]^T$ with steering angle and longitudinal acceleration as inputs, fixed geometry $l_f = l_r = 1$, and the prescribed continuous-time process covariance. The EKF used rectangular Euler prediction with first-order Jacobian linearization for both the process and measurement updates. The UKF used the scaled unscented transform with $alpha = 10^-3$, $beta = 2$, and $kappa = 0$, and propagated every sigma point with the selected discrete-time integrator. In every configuration, the two measurements were processed sequentially as scalar updates so that the gating study in Problem IV could test each sensor independently.

#column_figure(
  "figures/estimator_flow.pdf",
  [Standalone CeTZ diagram of the sequential estimation workflow. The figure was authored separately, compiled to PDF, and then imported into the main IEEE-formatted document as a standard image asset.],
)

The ungated rectangular comparison favored the UKF. The EKF rectangular run produced a position RMSE of #ekf_rect_no_gate_pos_text m with a heading RMSE of #ekf_rect_no_gate_heading_deg_text deg, while the rectangular UKF reduced these values to #ukf_rect_no_gate_pos_text m and #ukf_rect_no_gate_heading_deg_text deg. The same trend appeared in the covariance histories. The rectangular EKF carried an average covariance trace of #ekf_rect_no_gate_avg_trace_text, while the rectangular UKF carried #ukf_rect_no_gate_avg_trace_text. The UKF therefore remained less overconfident on this nonlinear problem, especially under the cubic heading measurement. Appendix B isolates how much of this difference comes from the two measurement channels, and Appendix C checks whether the conclusion is an artifact of the selected initial covariance.

#full_width_figure(
  "figures/trajectory.png",
  [Trajectory comparison for the rectangular EKF and UKF baselines, the gated rectangular filters, and the ungated RK4 UKF. The vanilla UKF and the ungated RK4 UKF remain closest to the truth trajectory, while the gated runs drift late in the record after repeated measurement rejection.],
)

#full_width_figure(
  "figures/covariance.png",
  [Diagonal covariance histories for the rectangular EKF, rectangular UKF, and ungated RK4 UKF. The UKF variants retain visibly larger uncertainty than the EKF, which is consistent with their stronger nonlinear treatment.],
)

= Problem III. Runtime of the Vanilla EKF and UKF

The average runtime study for the vanilla rectangular filters used sixty repeated executions after one warm-up pass per configuration. The EKF remained the cheaper estimator at #ekf_rect_no_gate_runtime_ms_text ms per run on average, while the rectangular UKF required #ukf_rect_no_gate_runtime_ms_text ms. That extra cost is expected because the UKF must propagate and recombine the sigma-point set at every step.

#column_table(
  problem3_runtime_table,
  [Average runtime over sixty repeated executions for the vanilla rectangular EKF and UKF.],
)

= Problem IV. Measurement Gating

Measurement gating was implemented as a scalar normalized innovation squared test on each sensor separately, exactly as requested in the handout. The study used a fixed #chosen_gate_label gate with threshold #chosen_gate_threshold_text. The gate did what it was supposed to do for the heading-like sensor. The EKF heading RMSE improved by #ekf_gating_heading_improvement_text deg and the UKF heading RMSE improved by #ukf_gating_heading_improvement_text deg after the strongest $y_2$ outliers were rejected. However, the position RMSE increased by #ekf_gating_position_change_text m for the EKF and by #ukf_gating_position_change_text m for the UKF because the gate also rejected many late $y_1$ measurements. The final rectangular gated runs rejected #ekf_rect_gate_rej_y1_text and #ukf_rect_gate_rej_y1_text range measurements, respectively, which made both filters coast too long on the process model alone. Appendix A expands this into a threshold sweep and shows that the best heading gate and best position gate are not the same operating point.

#full_width_figure(
  "figures/gating_diagnostics.png",
  [Normalized innovation squared histories for both scalar sensors. The isolated $y_2$ spikes are clearly detectable, and the EKF and UKF rejection markers show how the late growth in $y_1$ residuals drives repeated range-measurement rejection.],
)

= Problem V. UKF with Runge-Kutta Integration

Replacing the rectangular UKF propagation with RK4 improved the ungated UKF accuracy. The rectangular UKF produced a position RMSE of #ukf_rect_no_gate_pos_text m, while the ungated RK4 UKF reduced that value to #ukf_rk4_no_gate_pos_text m for an improvement of #rk4_position_improvement_text m. The heading RMSE remained nearly unchanged at #ukf_rect_no_gate_heading_deg_text deg for the rectangular UKF and #ukf_rk4_no_gate_heading_deg_text deg for the RK4 UKF. The main benefit therefore appeared in the planar trajectory and state histories, where the higher-order integrator reduced accumulated discretization error.

#full_width_figure(
  "figures/state_timeseries.png",
  [State estimates versus time for the vanilla rectangular EKF, vanilla rectangular UKF, and ungated RK4 UKF. The RK4 UKF mainly improves the position channels while leaving the heading history close to the rectangular UKF result.],
)

= Problem VI. Runtime of the RK4 UKF Versus the Rectangular UKF

The integrator runtime comparison again used sixty repeated executions after one warm-up pass per configuration. The rectangular UKF required #ukf_rect_runtime_ms_text ms per run on average, while the RK4 UKF required #ukf_rk4_runtime_ms_text ms. The RK4 propagation therefore added #rk4_runtime_penalty_text ms per run relative to the rectangular UKF. That extra cost is small compared with the position-accuracy gain reported in Problem V.

#column_table(
  problem6_runtime_table,
  [Average runtime over sixty repeated executions for the rectangular and RK4 UKF implementations.],
)

Taken together, the six required comparisons point to a qualified conclusion. The vanilla UKF was the stronger baseline on this nonlinear problem, the scalar gate was useful for removing the worst heading-sensor outliers but harmed position accuracy when range updates were rejected too often, and RK4 was the cleanest algorithmic upgrade because it improved the ungated UKF trajectory with only a modest runtime increase. The appendix studies show that this conclusion depends on the operating objective. A looser EKF gate can recover position accuracy, the two sensors are complementary rather than redundant, and UKF performance can improve further through prior and sigma-spread tuning.

#full_width_table(
  metrics_table,
  [State-estimation accuracy, covariance summary, and measurement-rejection counts for all evaluated configurations.],
)

#pagebreak()
#set page(columns: 1)

= Appendix A. Gate Threshold Sensitivity

The main gating result uses a scalar #chosen_gate_label normalized-innovation-squared threshold, but the behavior is not fully described by that single operating point. This sweep varies the scalar confidence level while keeping the same rectangular EKF and UKF, the same calibration variances, and the same sequential one-sensor-at-a-time update order. The best position result in this sweep is #gate_best_position_filter_text with the #gate_best_position_setting_text gate at #gate_best_position_rmse_text m, while the best heading result is #gate_best_heading_filter_text with the #gate_best_heading_setting_text gate at #gate_best_heading_rmse_text deg.

#appendix_figure(
  "figures/ablation_gate_thresholds.png",
  [Gate-threshold ablation for the rectangular EKF and UKF. Position accuracy and heading accuracy respond differently because rejecting late $y_1$ updates removes radial information, while rejecting isolated $y_2$ outliers can improve heading.],
)

#appendix_table(
  gate_ablation_table,
  [Gate-threshold ablation metrics for scalar NIS gating. The threshold column is the one-degree-of-freedom chi-square cutoff used independently for each sensor.],
)

The sweep makes the tradeoff in Problem IV explicit. A tighter gate can remove large innovations, but once the predicted trajectory drifts, the range innovation itself becomes large and the gate starts rejecting information that would otherwise pull the estimate back toward the measurement record. That feedback loop explains why the gated heading result can improve while the position result degrades.

= Appendix B. Sensor Contribution Ablation

The two sensors contribute different information. The range-like sensor $y_1$ directly constrains radial position but does not identify the sign or tangential component of the planar state by itself. The cubic heading sensor $y_2$ constrains orientation, but its local slope is $3 psi^2$, so it becomes weak near $psi = 0$ and highly nonlinear as the heading grows in magnitude. This ablation reruns the rectangular EKF and UKF with both sensors, with only $y_1$, with only $y_2$, and with prediction only.

#appendix_figure(
  "figures/ablation_measurements.png",
  [Measurement-subset ablation for rectangular EKF and UKF runs. The comparison separates radial measurement information from heading measurement information and includes a prediction-only baseline.],
)

#appendix_table(
  measurement_ablation_table,
  [Sensor contribution ablation. The best position result is #measurement_best_position_filter_text using #measurement_best_position_setting_text at #measurement_best_position_rmse_text m, and the best heading result is #measurement_best_heading_filter_text using #measurement_best_heading_setting_text at #measurement_best_heading_rmse_text deg.],
)

The useful baseline is not merely the result of one sensor dominating the other. The filters need $y_1$ to keep the path from drifting radially, and they need $y_2$ to keep heading errors from accumulating into position error. The UKF benefits more from the nonlinear measurement pair because it uses sigma-point propagation through $sqrt(x^2 + y^2)$ and $psi^3$ instead of a single local linearization.

= Appendix C. Initial Covariance Scale

The nominal runs use a zero-centered initial mean and an initial covariance with diagonal entries $4$, $4$, $(20 pi / 180)^2$, and $0.25$. This appendix scales that entire covariance by a single multiplier while keeping the initial mean, measurements, controls, and rectangular integration fixed. The purpose is to test whether the EKF and UKF ranking depends on one hand-selected prior confidence.

#appendix_figure(
  "figures/ablation_prior_scale.png",
  [Initial covariance scale ablation for the rectangular EKF and UKF. The horizontal axis multiplies the nominal $P_0$ used in the main study.],
)

#appendix_table(
  prior_ablation_table,
  [Initial covariance scale ablation metrics. The best position result is #prior_best_position_filter_text at a scale of #prior_best_position_scale_text with #prior_best_position_rmse_text m position RMSE.],
)

The covariance scale sweep is a useful check because the chosen zero-centered prior starts at a point where the EKF measurement Jacobians for both sensors are locally weak or singular. A very small initial covariance can make that local linearization too trusted, while a larger covariance gives the measurement updates room to move the estimate. The UKF is still not immune to prior tuning, but the sweep shows why maintaining uncertainty is preferable on this problem.

= Appendix D. UKF Sigma-Point Spread

The main UKF uses $alpha = 10^-3$, $beta = 2$, and $kappa = 0$. The parameter $alpha$ controls the spread of sigma points around the mean, so it changes how aggressively the UKF samples the nonlinear measurement and process models. This appendix varies $alpha$ for the rectangular UKF while leaving all other settings unchanged.

#appendix_figure(
  "figures/ablation_ukf_spread.png",
  [UKF alpha ablation for the rectangular UKF. The sweep tests whether the reported UKF performance depends on the default narrow sigma-point spread.],
)

#appendix_table(
  ukf_spread_ablation_table,
  [UKF sigma-point spread ablation. The best position result occurs at $alpha = #ukf_alpha_best_position_text$ with #ukf_alpha_best_position_rmse_text m position RMSE, while the best heading result occurs at $alpha = #ukf_alpha_best_heading_text$ with #ukf_alpha_best_heading_rmse_text deg heading RMSE.],
)

The alpha sweep tests the numerical robustness of the UKF result. If the UKF advantage disappeared under modest alpha changes, the main conclusion would be more a tuning artifact than an estimator comparison. Instead, the sweep gives a tuning envelope for the same algorithmic choice and clarifies how much performance is available from sigma-point spread alone before changing the integrator to RK4.
