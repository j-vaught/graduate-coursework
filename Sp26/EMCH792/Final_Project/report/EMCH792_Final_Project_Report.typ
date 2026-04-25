#import "generated/results.typ": *

// ── Brand palette ─────────────────────────────────────────────────────
#let garnet = rgb("#73000A")
#let black = rgb("#000000")
#let black-90 = rgb("#363636")
#let black-70 = rgb("#5C5C5C")
#let black-50 = rgb("#A2A2A2")
#let black-30 = rgb("#C7C7C7")
#let black-10 = rgb("#ECECEC")
#let warm-grey = rgb("#676156")
#let sandstorm = rgb("#FFF2E3")
#let rose = rgb("#CC2E40")
#let atlantic = rgb("#466A9F")
#let congaree = rgb("#1F414D")
#let horseshoe = rgb("#65780B")
#let honeycomb = rgb("#A49137")

// ── Document setup ────────────────────────────────────────────────────
#set document(
  title: "Comparison of EKF and UKF State Estimation with Measurement Gating and RK4 Propagation",
  author: "J.C. Vaught",
)

#set heading(numbering: "1.")

#set page(
  paper: "us-letter",
  margin: (top: 0.9in, bottom: 1in, x: 0.85in),
  numbering: "1 / 1",
  number-align: center,
  footer: context [
    #set text(size: 8pt, fill: black-70)
    #grid(
      columns: (1fr, auto, 1fr),
      align: (left, center, right),
      [EMCH792 Final Project],
      counter(page).display("1 / 1", both: true),
      [J.C. Vaught],
    )
  ],
)

#set text(
  font: ("New Computer Modern", "TeX Gyre Termes", "Times New Roman", "Georgia"),
  size: 10pt,
  lang: "en",
  hyphenate: true,
)

#set par(justify: true, leading: 0.55em, first-line-indent: 0pt)

// ── Heading styles ────────────────────────────────────────────────────
#show heading.where(level: 1): it => {
  set text(fill: garnet, size: 12pt, weight: "bold")
  set block(above: 0.7em, below: 0.5em)
  block[
    #smallcaps(it.body)
    #v(-6pt)
    #line(length: 100%, stroke: 1pt + garnet)
  ]
}

#show heading.where(level: 2): it => {
  set text(fill: black-90, size: 10.5pt, weight: "bold")
  block(above: 0.7em, below: 0.3em)[#it.body]
}

#show heading.where(level: 3): it => {
  set text(fill: black-90, size: 10pt, weight: "semibold", style: "italic")
  block(above: 0.7em, below: 0.3em)[#it.body]
}

// ── Link / ref / caption / table styles ──────────────────────────────
#show link: it => text(fill: atlantic)[#it]
#show ref: it => text(fill: garnet, weight: "semibold")[#it]
#show figure.caption: it => {
  set text(size: 9pt, fill: black-70)
  block(above: 0.35em)[
    #text(fill: garnet, weight: "bold")[#it.supplement #it.counter.display()#it.separator]
    #it.body
  ]
}

#set table(
  stroke: none,
  inset: 6pt,
)

#let report-title = [Final Project: EMCH 792]
#let report-abstract = [
  This report addresses the six required tasks in the EMCH792 final project for the nonlinear kinematic bicycle model. The calibration pass yielded $R_1$ = #y1_variance_text and $R_2$ = #y2_variance_text with a constant sample period of #dt_text s. The main runs use #process_noise_description_text. A separate sensitivity check also repeats the vanilla rectangular EKF and UKF with direct $Q$ so both process-noise interpretations are documented. The vanilla rectangular comparison was metric dependent. The EKF produced the lower position RMSE at #ekf_rect_no_gate_pos_text m compared with #ukf_rect_no_gate_pos_text m for the UKF, while the UKF produced the lower heading RMSE at #ukf_rect_no_gate_heading_deg_text deg compared with #ekf_rect_no_gate_heading_deg_text deg for the EKF. A fixed scalar #chosen_gate_label normalized-innovation-squared gate with threshold #chosen_gate_threshold_text increased EKF position and heading error, while the UKF gate reduced heading RMSE but increased position RMSE after repeated $y_1$ rejections. Replacing rectangular UKF propagation with RK4 reduced UKF position RMSE by #rk4_position_improvement_text m, while the RK4 runtime increased by #rk4_runtime_penalty_text ms relative to the rectangular UKF.
]

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
  scope: "parent",
  placement: auto,
  kind: table,
  block(width: 100%)[
    #set text(size: 8pt)
    #body
  ],
  caption: [#caption],
)

#let narrow_table(body, caption) = figure(
  placement: none,
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

// ── Title block ───────────────────────────────────────────────────────
#align(center)[
  #block(width: 100%, inset: (y: 0.35em))[
    #text(size: 17pt, weight: "bold", fill: black)[#report-title]
  ]
  #v(0.2em)
  #text(size: 10pt, fill: black-90)[J.C. Vaught]
]

#v(0.4em)
#line(length: 100%, stroke: 0.4pt + black-50)
#v(0.2em)

// ── Abstract callout ──────────────────────────────────────────────────
#block(
  fill: sandstorm,
  stroke: (left: 2pt + garnet),
  inset: (x: 14pt, y: 10pt),
  width: 100%,
)[
  #text(weight: "bold", size: 9.5pt, fill: garnet)[ABSTRACT.]
  #text(size: 9.5pt)[#report-abstract]
]
// ── Two-column body starts here ──────────────────────────────────────
#[
  #show: rest => columns(2, gutter: 18pt, rest)

= P1. Calib. Variance Estimation

The first task was to estimate the two sensor variances from the calibration data and confirm the deployment sample period. The calibration pass produced $R_1$ = #y1_variance_text for the range-like measurement and $R_2$ = #y2_variance_text for the cubic heading sensor. Because both calibration datasets were collected while the robot was stationary, the sample variances are a direct estimate of measurement noise rather than a mixture of motion and sensing effects. The deployment dataset remained uniformly sampled at #dt_text s, so a single discrete step size could be used consistently in every estimator variant. The filters were initialized from a zero-centered prior and used the nominal base covariance so that the baseline comparison did not consume the provided truth channels as estimator inputs. The provided truth channels were used only after filtering to compute accuracy metrics.

= P2. Vanilla EKF and UKF with Rectangular Integration

Both filters used the assignment state $x = [x, y, psi, u]^T$ with steering angle and longitudinal acceleration as inputs, fixed geometry $l_f = l_r = 1$, and the prescribed model covariance as a sample-period-scaled discrete process contribution. The EKF used rectangular Euler prediction with first-order Jacobian linearization for both the process and measurement updates. Its covariance prediction used the discrete rectangular transition $Phi = I + Delta t F$ before adding the process covariance contribution. The UKF used the scaled unscented transform with $alpha = 10^-3$, $beta = 2$, and $kappa = 0$, and propagated every sigma point with the selected discrete-time integrator. In every configuration, the two measurements were processed sequentially as scalar updates so that the gating study in Problem IV could test each sensor independently. That sequential scalar structure also makes the comparison cleaner because each sensor contributes its own innovation test, update gain, and possible rejection event.

#column_figure(
  "figures/estimator_flow.pdf",
  [Sequential EKF and UKF workflow showing prediction, independent scalar measurement tests for $y_1$ and $y_2$, optional gating, and the final stored estimate for each time sample.],
)


The ungated rectangular comparison did not produce a single winner across all metrics. The EKF rectangular run produced the lower position RMSE at #ekf_rect_no_gate_pos_text m, while the rectangular UKF produced #ukf_rect_no_gate_pos_text m. The UKF was stronger in heading, with #ukf_rect_no_gate_heading_deg_text deg compared with #ekf_rect_no_gate_heading_deg_text deg for the EKF. The covariance histories also differed. The rectangular EKF carried an average covariance trace of #ekf_rect_no_gate_avg_trace_text, while the rectangular UKF carried #ukf_rect_no_gate_avg_trace_text. That split is consistent with the structure of the problem. The EKF benefits from a relatively mild process model over one sample, while the UKF benefits more when the nonlinear measurement channels, especially $psi^3$, distort the uncertainty in a way that a single Jacobian cannot capture as well. The EKF therefore gave the tighter position result with a more compact covariance, while the UKF retained more uncertainty and handled the cubic heading measurement more effectively. Appendix B isolates how much of this difference comes from the two measurement channels, and Appendix C checks whether the conclusion is an artifact of the selected initial covariance.




#full_width_figure(
  "figures/trajectory.png",
  [Trajectory comparison for the rectangular EKF and UKF baselines, the gated rectangular filters, and the ungated RK4 UKF. The ungated rectangular EKF gives the lowest position RMSE, while the gated runs drift late in the record after repeated measurement rejection.],
)

#full_width_figure(
  "figures/covariance.png",
  [Diagonal covariance histories for the rectangular EKF, rectangular UKF, and ungated RK4 UKF. The UKF variants retain visibly larger uncertainty than the EKF, while the EKF maintains the lower position RMSE in the ungated rectangular comparison.],
)

= P3. Vanilla EKF and UKF

The average runtime study for the vanilla rectangular filters used sixty repeated executions after one warm-up pass per configuration. The EKF remained the cheaper estimator at #ekf_rect_no_gate_runtime_ms_text ms per run on average, while the rectangular UKF required #ukf_rect_no_gate_runtime_ms_text ms. That extra cost is expected because the UKF must propagate and recombine the sigma-point set at every step. The absolute runtime values are small for this ten-second record, but the relative difference is still important because the same ratio would carry into longer datasets or embedded implementations with tighter computational budgets. On this problem, the UKF runtime premium buys better heading accuracy, but not a uniformly better estimate.

#narrow_table(
  problem3_runtime_table,
  [Average runtime over sixty repeated executions for the vanilla rectangular EKF and UKF.],
)

The assignment states the model covariance as $Q = diag(0.01, 0.01, 0.1, 0.05)$. Since the model is discretized with rectangular integration, the main results add $Q Delta t$ as the discrete process contribution. The script also reruns the vanilla rectangular EKF and UKF with direct $Q$ to document the alternate interpretation. The comparison below shows that direct $Q$ makes the default-alpha UKF much less stable on this dataset, so the sample-period-scaled case is used in the required plots, tables, and gating/RK4 comparisons.

#narrow_table(
  q_interpretation_table,
  [Vanilla rectangular EKF and UKF sensitivity to the direct $Q$ and $Q Delta t$ process-noise interpretations.],
)

= P4. Measurement Gating

Measurement gating was implemented as a scalar normalized innovation squared test on each sensor separately, exactly as requested in the handout. The study used a fixed #chosen_gate_label gate with threshold #chosen_gate_threshold_text. This fixed gate was not uniformly beneficial. For the EKF, position RMSE changed from #ekf_rect_no_gate_pos_text m to #ekf_rect_gate_pos_text m and heading RMSE changed from #ekf_rect_no_gate_heading_deg_text deg to #ekf_rect_gate_heading_deg_text deg. For the UKF, the same gate improved heading RMSE by #ukf_gating_heading_improvement_text deg but increased position RMSE by #ukf_gating_position_change_text m. The final rectangular gated runs rejected #ekf_rect_gate_rej_y1_text and #ukf_rect_gate_rej_y1_text range measurements, respectively, which made both filters more prediction dominated. The important point is that gating is only useful when the rejected samples are genuinely inconsistent with the evolving state estimate. Once the filter drifts, the same gate can start rejecting measurements that are actually corrective, so the estimator becomes overconfident in its own prediction. Appendix A expands this into a threshold sweep and shows that the best heading gate and best position setting are not the same operating point.

#full_width_figure(
  "figures/gating_diagnostics.png",
  [Normalized innovation squared histories for both scalar sensors. The isolated $y_2$ spikes are clearly detectable, and the EKF and UKF rejection markers show how the late growth in $y_1$ residuals drives repeated range-measurement rejection.],
)

= P5. UKF with RK Integration

Replacing the rectangular UKF propagation with RK4 improved the ungated UKF accuracy. The rectangular UKF produced a position RMSE of #ukf_rect_no_gate_pos_text m, while the ungated RK4 UKF reduced that value to #ukf_rk4_no_gate_pos_text m for an improvement of #rk4_position_improvement_text m. The heading RMSE remained nearly unchanged at #ukf_rect_no_gate_heading_deg_text deg for the rectangular UKF and #ukf_rk4_no_gate_heading_deg_text deg for the RK4 UKF. The main benefit therefore appeared in the planar trajectory and state histories, where the higher-order integrator reduced accumulated discretization error within the UKF family, although the corrected rectangular EKF remained lower in position RMSE. This outcome is reasonable because the UKF repeatedly pushes multiple sigma points through the dynamics, so any improvement in propagation accuracy is inherited by the entire transformed distribution instead of a single mean-state prediction.

#full_width_figure(
  "figures/state_timeseries.png",
  [State estimates versus time for the vanilla rectangular EKF, vanilla rectangular UKF, and ungated RK4 UKF. The RK4 UKF mainly improves the position channels while leaving the heading history close to the rectangular UKF result.],
)

= P6. RK4 UKF vs. Rectangular UKF

The integrator runtime comparison again used sixty repeated executions after one warm-up pass per configuration. The rectangular UKF required #ukf_rect_runtime_ms_text ms per run on average, while the RK4 UKF required #ukf_rk4_runtime_ms_text ms. The RK4 propagation therefore added #rk4_runtime_penalty_text ms per run relative to the rectangular UKF. That extra cost is modest, but the RK4 benefit should be interpreted as a UKF-specific improvement rather than the best overall position result. In other words, RK4 is a sensible refinement if the UKF has already been selected for its nonlinear-measurement behavior, but it does not overturn the broader result that the rectangular EKF remains the strongest nominal position estimator in this particular setup.

#narrow_table(
  problem6_runtime_table,
  [Average runtime over sixty repeated executions for the rectangular and RK4 UKF implementations.],
)

Taken together, the six required comparisons point to a metric-dependent conclusion. The corrected rectangular EKF was the stronger position estimator for the nominal ungated case, while the UKF was stronger on heading. The scalar gate was useful for removing some heading-sensor outliers in the UKF, but it harmed position accuracy when range updates were rejected too often and did not improve the corrected EKF result. RK4 was a useful UKF upgrade because it improved the ungated UKF trajectory with only a modest runtime increase. The broader lesson is that estimator choice here depends less on which filter is universally best and more on which error channel matters most, how aggressively one is willing to gate measurements, and how much runtime budget is available for better propagation. The appendix studies show that these conclusions depend on the operating objective, the gate threshold, and the UKF sigma-point spread.

#full_width_table(
  metrics_table,
  [State-estimation accuracy, covariance summary, and measurement-rejection counts for all evaluated configurations.],
)
]

#pagebreak()

= Appendix A. Gate Threshold Sensitivity

The main gating result uses a scalar #chosen_gate_label normalized-innovation-squared threshold, but the behavior is not fully described by that single operating point. This sweep varies the scalar confidence level while keeping the same rectangular EKF and UKF, the same calibration variances, and the same sequential one-sensor-at-a-time update order. The best position result in this sweep is #gate_best_position_filter_text with the #gate_best_position_setting_text setting at #gate_best_position_rmse_text m, while the best heading result is #gate_best_heading_filter_text with the #gate_best_heading_setting_text setting at #gate_best_heading_rmse_text deg. The sweep is useful because it separates the idea of gating from the particular threshold chosen for the main comparison.

#appendix_figure(
  "figures/ablation_gate_thresholds.png",
  [Gate-threshold ablation for the rectangular EKF and UKF. Position accuracy and heading accuracy respond differently because rejecting late $y_1$ updates removes radial information, while rejecting isolated $y_2$ outliers can improve heading.],
)

#appendix_table(
  gate_ablation_table,
  [Gate-threshold ablation metrics for scalar NIS gating. The threshold column is the one-degree-of-freedom chi-square cutoff used independently for each sensor.],
)

The sweep makes the tradeoff in Problem IV explicit. A tighter gate can remove large innovations, but once the predicted trajectory drifts, the range innovation itself becomes large and the gate starts rejecting information that would otherwise pull the estimate back toward the measurement record. That feedback loop explains why the gated heading result can improve while the position result degrades.

#pagebreak()

= Appendix B. Sensor Contribution Ablation

The two sensors contribute different information. The range-like sensor $y_1$ directly constrains radial position but does not identify the sign or tangential component of the planar state by itself. The cubic heading sensor $y_2$ constrains orientation, but its local slope is $3 psi^2$, so it becomes weak near $psi = 0$ and highly nonlinear as the heading grows in magnitude. This ablation reruns the rectangular EKF and UKF with both sensors, with only $y_1$, with only $y_2$, and with prediction only. It therefore exposes whether the nominal ranking comes from one dominant channel or from the interaction of both measurements.

#appendix_figure(
  "figures/ablation_measurements.png",
  [Measurement-subset ablation for rectangular EKF and UKF runs. The comparison separates radial measurement information from heading measurement information and includes a prediction-only baseline.],
)

#appendix_table(
  measurement_ablation_table,
  [Sensor contribution ablation. The best position result is #measurement_best_position_filter_text using #measurement_best_position_setting_text at #measurement_best_position_rmse_text m, and the best heading result is #measurement_best_heading_filter_text using #measurement_best_heading_setting_text at #measurement_best_heading_rmse_text deg.],
)

The useful baseline is not merely the result of one sensor dominating the other. The filters need $y_1$ to keep the path from drifting radially, and they need $y_2$ to keep heading errors from accumulating into position error. With the corrected EKF covariance prediction, the EKF and UKF ranking is metric dependent rather than one-sided. The EKF gives the strongest position result in the nominal rectangular case, while the UKF benefits in heading from sigma-point propagation through $sqrt(x^2 + y^2)$ and $psi^3$ instead of a single local linearization.

#pagebreak()

= Appendix C. Initial Covariance Scale

The nominal runs use a zero-centered initial mean and an initial covariance with diagonal entries $4$, $4$, $(20 pi / 180)^2$, and $0.25$. This appendix scales that entire covariance by a single multiplier while keeping the initial mean, measurements, controls, and rectangular integration fixed. The purpose is to test whether the EKF and UKF ranking depends on one hand-selected prior confidence. That is an important check because both filters start from a deliberately neutral but imperfect prior.

#appendix_figure(
  "figures/ablation_prior_scale.png",
  [Initial covariance scale ablation for the rectangular EKF and UKF. The horizontal axis multiplies the nominal $P_0$ used in the main study.],
)

#appendix_table(
  prior_ablation_table,
  [Initial covariance scale ablation metrics. The best position result is #prior_best_position_filter_text at a scale of #prior_best_position_scale_text with #prior_best_position_rmse_text m position RMSE.],
)

The covariance scale sweep is a useful check because the chosen zero-centered prior starts at a point where the EKF measurement Jacobians for both sensors are locally weak or singular. A very small initial covariance can make that local linearization too trusted, while a larger covariance gives the measurement updates room to move the estimate. The UKF is still not immune to prior tuning, but the sweep shows why maintaining uncertainty is preferable on this problem.

#pagebreak()

= Appendix D. UKF Sigma-Point Spread

The main UKF uses $alpha = 10^-3$, $beta = 2$, and $kappa = 0$. The parameter $alpha$ controls the spread of sigma points around the mean, so it changes how aggressively the UKF samples the nonlinear measurement and process models. This appendix varies $alpha$ for the rectangular UKF while leaving all other settings unchanged. It is included to distinguish a genuine algorithmic trend from a result that depends too strongly on one narrow default tuning.

#appendix_figure(
  "figures/ablation_ukf_spread.png",
  [UKF alpha ablation for the rectangular UKF. The sweep tests whether the reported UKF performance depends on the default narrow sigma-point spread.],
)

#appendix_table(
  ukf_spread_ablation_table,
  [UKF sigma-point spread ablation. The best position result occurs at $alpha = #ukf_alpha_best_position_text$ with #ukf_alpha_best_position_rmse_text m position RMSE, while the best heading result occurs at $alpha = #ukf_alpha_best_heading_text$ with #ukf_alpha_best_heading_rmse_text deg heading RMSE.],
)

The alpha sweep tests the numerical robustness of the UKF result. If the UKF advantage disappeared under modest alpha changes, the main conclusion would be more a tuning artifact than an estimator comparison. Instead, the sweep gives a tuning envelope for the same algorithmic choice and clarifies how much performance is available from sigma-point spread alone before changing the integrator to RK4.
