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
    This report evaluates an extended Kalman filter (EKF) and an unscented Kalman filter (UKF) for the nonlinear vehicle-state estimation problem posed in the EMCH792 final project. The analysis used the provided deployment dataset, estimated sensor variances directly from the calibration sets, and compared rectangular propagation, scalar measurement gating, and fourth-order Runge-Kutta (RK4) propagation. The calibration pass yielded $R_1$ = #y1_variance_text and $R_2$ = #y2_variance_text with a constant sample period of #dt_text s. A short sweep over initial covariance scale and scalar chi-square gate threshold selected a covariance scale of #chosen_p0_scale_text and a #chosen_gate_label gate at #chosen_gate_threshold_text. Across the full comparison, the rectangular UKF outperformed the rectangular EKF in ungated accuracy, while the RK4 UKF achieved the best overall position error at #best_position_rmse_text m. The gating logic removed the largest $y_2$ outliers and improved heading estimation, but excessive late rejection of $y_1$ measurements increased position error in the gated runs.
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

#let column_figure(path, caption) = block(width: 100%, above: 0.8em, below: 1.0em)[
  #align(center)[#image(path, width: 92%)]
  #v(0.25em)
  #set text(size: 8pt)
  #caption
]

#let column_table(body, caption) = figure(
  kind: table,
  block(width: 100%)[
    #set text(size: 8pt)
    #body
  ],
  caption: [#caption],
)

= Problem I. Calibration Variance Estimation

The first task was to estimate the two sensor variances from the calibration data and lock the deployment sample period. The calibration pass produced $R_1$ = #y1_variance_text for the range-like measurement and $R_2$ = #y2_variance_text for the cubic heading sensor. The deployment dataset remained uniformly sampled at #dt_text s, which made the rectangular covariance propagation required by the assignment directly applicable. The filters were initialized from the first truth sample so that the comparison emphasized filter behavior, rather than startup mismatch, across the 100 available samples.

= Problem II. EKF and UKF Formulation

Both filters used the assignment state $x = [x, y, psi, u]^T$ with steering angle and longitudinal acceleration as inputs, fixed geometry $l_f = l_r = 1$, and the prescribed continuous-time process covariance. The EKF used the rectangular Euler prediction and first-order Jacobian linearization for both process and measurement updates. The UKF used the scaled unscented transform with $alpha = 10^-3$, $beta = 2$, and $kappa = 0$, propagated each sigma point through the selected integrator, and reconstructed mean and covariance from the propagated sigma set. In every configuration, the two measurements were processed sequentially as scalar updates so that each sensor could be accepted or rejected independently.

#column_figure(
  "figures/estimator_flow.pdf",
  [Standalone CeTZ diagram of the sequential estimation workflow. The figure was authored separately, compiled to PDF, and then imported into the main IEEE-formatted document as a standard image asset.],
)

The ungated rectangular comparison favored the UKF. The EKF rectangular run produced a position RMSE of #ekf_rect_no_gate_pos_text m with a heading RMSE of #ekf_rect_no_gate_heading_deg_text deg, while the rectangular UKF reduced these values to #ukf_rect_no_gate_pos_text m and #ukf_rect_no_gate_heading_deg_text deg. This result is consistent with the nonlinear measurement model, especially the $psi^3$ sensor, where the UKF preserved nonlinear curvature more effectively than the first-order EKF approximation.

#full_width_figure(
  "figures/trajectory.png",
  [Truth and estimated trajectories for the main filter configurations. The ungated UKF remains closest to the measured path, while the gated runs become increasingly prediction dominated late in the record.],
)

= Problem III. Measurement Gating Study

The tuning sweep compared two reasonable scalar chi-square thresholds, namely 95% and 99%, across five initial covariance scales. The selected setting was the #chosen_gate_label gate with a #chosen_p0_scale_text scaling on the base initial covariance because it minimized the composite score across the gated EKF and UKF rectangular runs.

#full_width_table(
  tuning_table,
  [Initialization-scale and gate-threshold sweep used to select the final gated comparison settings.],
)

The gate did exactly what it was intended to do for the heading-like sensor. The faulty $y_2$ measurement was rejected three times in each final gated run, which reduced the heading RMSE from #ekf_rect_no_gate_heading_deg_text deg to #ekf_rect_gate_heading_deg_text deg for the EKF and from #ukf_rect_no_gate_heading_deg_text deg to #ukf_rect_gate_heading_deg_text deg for the UKF. However, the same logic also rejected many late $y_1$ measurements, namely #ekf_rect_gate_rej_y1_text in the EKF and #ukf_rect_gate_rej_y1_text in the UKF. As a consequence, the position RMSE increased to #ekf_rect_gate_pos_text m and #ukf_rect_gate_pos_text m for the gated rectangular filters. The practical interpretation is that the scalar normalized innovation squared test was effective at flagging the strongest outliers, but the process model was not accurate enough to fully replace the range-like measurement once repeated rejections accumulated near the end of the maneuver.

#full_width_figure(
  "figures/gating_diagnostics.png",
  [Normalized innovation squared histories for both scalar sensors. The isolated $y_2$ spikes are clearly detectable, while the late growth in $y_1$ residuals explains the large number of range-measurement rejections.],
)

= Problem IV. RK4 Propagation for the UKF

Replacing the UKF rectangular propagation with RK4 improved the ungated accuracy. The ungated RK4 UKF achieved the best position RMSE in the study at #best_position_rmse_text m, improving on the ungated rectangular UKF by #rk4_position_improvement_text m. Under the same gating logic, the RK4 UKF also delivered the best heading RMSE among the gated UKF runs at #ukf_rk4_gate_heading_deg_text deg, although the persistent late measurement rejections still limited the position benefit in the gated case.

#full_width_figure(
  "figures/state_timeseries.png",
  [State estimates versus time for the principal comparison cases. The gated filters maintain improved heading agreement, but their position and speed estimates drift as measurements are rejected.],
)

The covariance histories support that interpretation. The UKF carried a larger uncertainty envelope than the EKF, which is expected for a sigma-point method operating on the same nonlinear dynamics and measurement set. The RK4 propagation also produced a slightly smoother covariance evolution than the rectangular UKF during the final part of the trajectory.

#full_width_figure(
  "figures/covariance.png",
  [Diagonal covariance histories for the gated EKF, gated rectangular UKF, and gated RK4 UKF. The UKF variants retain visibly larger uncertainty than the EKF, which is consistent with their stronger nonlinear treatment.],
)

= Problem V. Runtime Comparison

The runtime study used sixty repeated executions per configuration so that transient timing noise would not dominate the comparison. The EKF remained the cheapest method at #ekf_rect_gate_runtime_ms_text ms per run on average, the rectangular UKF required #ukf_rect_gate_runtime_ms_text ms, and the RK4 UKF required #ukf_rk4_gate_runtime_ms_text ms. The RK4 propagation therefore added about #rk4_runtime_penalty_text ms relative to the rectangular UKF. That cost increase is modest compared with the gain in ungated trajectory accuracy.

#column_table(
  runtime_table,
  [Average runtime over sixty repeated executions for the principal estimator configurations.],
)

= Problem VI. Overall Comparison and Conclusions

The overall comparison is clear. The UKF was the stronger estimator for this dataset because the nonlinear process and measurement relationships were significant enough that the EKF linearization lost accuracy. The covariance comparison also favored the UKF qualitatively because the sigma-point filters carried larger and more credible uncertainty levels instead of the tighter EKF covariance trace. Measurement gating helped where it mattered most by removing the strongest $y_2$ outliers and reducing heading error, but it also exposed the weakness of the process model by forcing the filters to coast through too many late $y_1$ rejections. Finally, the RK4 propagation was the cleanest algorithmic improvement in the study because it produced the best overall ungated trajectory while increasing runtime only slightly.

#full_width_table(
  metrics_table,
  [State-estimation accuracy, covariance summary, and measurement-rejection counts for all evaluated configurations.],
)
