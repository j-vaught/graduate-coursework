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
    This report addresses the six required tasks in the EMCH792 final project for the nonlinear kinematic bicycle model. The calibration pass yielded $R_1$ = #y1_variance_text and $R_2$ = #y2_variance_text with a constant sample period of #dt_text s. The vanilla rectangular comparison favored the UKF over the EKF, reducing position RMSE from #ekf_rect_no_gate_pos_text m to #ukf_rect_no_gate_pos_text m and heading RMSE from #ekf_rect_no_gate_heading_deg_text deg to #ukf_rect_no_gate_heading_deg_text deg. A fixed scalar #chosen_gate_label normalized-innovation-squared gate with threshold #chosen_gate_threshold_text improved heading RMSE by #ekf_gating_heading_improvement_text deg for the EKF and #ukf_gating_heading_improvement_text deg for the UKF, but position RMSE increased because repeated $y_1$ rejections made the gated runs more prediction dominated. Replacing rectangular UKF propagation with RK4 reduced position RMSE by #rk4_position_improvement_text m, while the RK4 runtime increased by only #rk4_runtime_penalty_text ms relative to the rectangular UKF.
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

= Problem I. Calibration Variance Estimation

The first task was to estimate the two sensor variances from the calibration data and confirm the deployment sample period. The calibration pass produced $R_1$ = #y1_variance_text for the range-like measurement and $R_2$ = #y2_variance_text for the cubic heading sensor. The deployment dataset remained uniformly sampled at #dt_text s. The filters were initialized from the first truth sample and used an initial covariance equal to #p0_trace_ratio_text of the nominal base matrix so that the baseline comparison started from the same prior in every case.

= Problem II. Vanilla EKF and UKF with Rectangular Integration

Both filters used the assignment state $x = [x, y, psi, u]^T$ with steering angle and longitudinal acceleration as inputs, fixed geometry $l_f = l_r = 1$, and the prescribed continuous-time process covariance. The EKF used rectangular Euler prediction with first-order Jacobian linearization for both the process and measurement updates. The UKF used the scaled unscented transform with $alpha = 10^-3$, $beta = 2$, and $kappa = 0$, and propagated every sigma point with the selected discrete-time integrator. In every configuration, the two measurements were processed sequentially as scalar updates so that the gating study in Problem IV could test each sensor independently.

#column_figure(
  "figures/estimator_flow.pdf",
  [Standalone CeTZ diagram of the sequential estimation workflow. The figure was authored separately, compiled to PDF, and then imported into the main IEEE-formatted document as a standard image asset.],
)

The ungated rectangular comparison favored the UKF. The EKF rectangular run produced a position RMSE of #ekf_rect_no_gate_pos_text m with a heading RMSE of #ekf_rect_no_gate_heading_deg_text deg, while the rectangular UKF reduced these values to #ukf_rect_no_gate_pos_text m and #ukf_rect_no_gate_heading_deg_text deg. The same trend appeared in the covariance histories. The rectangular EKF carried an average covariance trace of #ekf_rect_no_gate_avg_trace_text, while the rectangular UKF carried #ukf_rect_no_gate_avg_trace_text. The UKF therefore remained less overconfident on this nonlinear problem, especially under the cubic heading measurement.

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

Measurement gating was implemented as a scalar normalized innovation squared test on each sensor separately, exactly as requested in the handout. The study used a fixed #chosen_gate_label gate with threshold #chosen_gate_threshold_text. The gate did what it was supposed to do for the heading-like sensor. The EKF heading RMSE improved by #ekf_gating_heading_improvement_text deg and the UKF heading RMSE improved by #ukf_gating_heading_improvement_text deg after the strongest $y_2$ outliers were rejected. However, the position RMSE increased by #ekf_gating_position_change_text m for the EKF and by #ukf_gating_position_change_text m for the UKF because the gate also rejected many late $y_1$ measurements. The final rectangular gated runs rejected #ekf_rect_gate_rej_y1_text and #ukf_rect_gate_rej_y1_text range measurements, respectively, which made both filters coast too long on the process model alone.

#full_width_figure(
  "figures/gating_diagnostics.png",
  [Normalized innovation squared histories for both scalar sensors. The isolated $y_2$ spikes are clearly detectable, while the late growth in $y_1$ residuals explains the large number of range-measurement rejections.],
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

Taken together, the six required comparisons point to the same conclusion. The vanilla UKF was the stronger baseline on this nonlinear problem, the scalar gate was useful for removing the worst heading-sensor outliers but harmed position accuracy when range updates were rejected too often, and RK4 was the cleanest algorithmic upgrade because it improved the ungated UKF trajectory with only a modest runtime increase.

#full_width_table(
  metrics_table,
  [State-estimation accuracy, covariance summary, and measurement-rejection counts for all evaluated configurations.],
)
