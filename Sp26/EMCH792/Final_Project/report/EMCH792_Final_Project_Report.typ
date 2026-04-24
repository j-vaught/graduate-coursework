#import "@preview/cetz:0.4.2"
#import "generated/results.typ": *

#set page(
  paper: "us-letter",
  margin: (x: 0.72in, y: 0.68in),
)

#set text(
  font: "New Computer Modern",
  size: 10.5pt,
  fill: rgb("#000000"),
)

#set par(
  justify: true,
  leading: 0.62em,
)

#show heading.where(level: 1): it => block(above: 1.1em, below: 0.5em)[
  #set text(fill: rgb("#73000A"), weight: "bold", size: 14pt)
  #it
]

#show heading.where(level: 2): it => block(above: 0.8em, below: 0.35em)[
  #set text(fill: rgb("#73000A"), weight: "bold", size: 11.5pt)
  #it
]

#show table.cell.where(y: 0): set text(weight: "bold")

#let highlight(body) = block(
  fill: rgb("#FFF2E3"),
  stroke: (paint: rgb("#73000A"), thickness: 0.9pt),
  inset: 10pt,
  radius: 0pt,
  width: 100%,
)[#body]

#let estimator_flow = figure(
  cetz.canvas(length: 1cm, {
    import cetz.draw: *

    let garnet = rgb("#73000A")
    let atlantic = rgb("#466A9F")
    let rose = rgb("#CC2E40")
    let horseshoe = rgb("#65780B")
    let sand = rgb("#FFF2E3")
    let light = rgb("#ECECEC")

    set-style(
      stroke: (paint: black, thickness: 0.8pt),
      mark: (fill: black, scale: 0.75),
      rect: (stroke: (paint: black, thickness: 0.8pt), fill: white),
    )

    let box(name, cx, cy, label, fill: white, w: 2.45, h: 0.95) = {
      rect((cx - w/2, cy - h/2), (cx + w/2, cy + h/2), name: name, fill: fill)
      content(name, label)
    }

    box("ctrl", 0.0, 0.0, [Inputs $delta_f, a$], fill: sand)
    box("pred", 3.2, 0.0, [Predict with Euler or RK4], fill: light, w: 2.95)
    box("sens1", 6.6, 1.2, [Update $y_1 = sqrt(x^2 + y^2)$], fill: white, w: 3.0)
    box("gate1", 6.6, -0.15, [Scalar NIS gate], fill: sand, w: 2.2)
    box("sens2", 10.0, 1.2, [Update $y_2 = psi^3$], fill: white, w: 2.5)
    box("gate2", 10.0, -0.15, [Scalar NIS gate], fill: sand, w: 2.2)
    box("state", 13.2, 0.0, [Posterior state and covariance], fill: light, w: 3.0)

    line((1.25, 0.0), (1.72, 0.0),
      mark: (end: "stealth", fill: atlantic),
      stroke: (paint: atlantic, thickness: 0.85pt))
    line((4.68, 0.0), (5.65, 0.0),
      mark: (end: "stealth", fill: atlantic),
      stroke: (paint: atlantic, thickness: 0.85pt))
    line((5.65, 0.0), (5.65, 1.2),
      mark: (end: "stealth", fill: rose),
      stroke: (paint: rose, thickness: 0.85pt))
    line((7.55, 1.2), (8.75, 1.2),
      mark: (end: "stealth", fill: garnet),
      stroke: (paint: garnet, thickness: 0.85pt))
    line((8.75, 1.2), (8.75, -0.15),
      mark: (end: "stealth", fill: rose),
      stroke: (paint: rose, thickness: 0.85pt))
    line((11.1, -0.15), (11.7, -0.15),
      mark: (end: "stealth", fill: horseshoe),
      stroke: (paint: horseshoe, thickness: 0.85pt))
    line((11.7, -0.15), (11.7, 0.0),
      mark: (end: "stealth", fill: horseshoe),
      stroke: (paint: horseshoe, thickness: 0.85pt))
    line((11.7, 0.0), (11.7 + 0.95, 0.0),
      mark: (end: "stealth", fill: atlantic),
      stroke: (paint: atlantic, thickness: 0.85pt))

    content((5.2, 0.55), text(size: 8.5pt, fill: atlantic)[Time update])
    content((7.95, 0.55), text(size: 8.5pt, fill: rose)[Gate $y_1$])
    content((11.2, 0.55), text(size: 8.5pt, fill: horseshoe)[Gate $y_2$])
  }),
  caption: [Sequential estimator flow used in every run. The EKF used Euler prediction only, while the UKF was evaluated with both Euler and RK4 prediction.],
)

#let full_width(path, caption) = figure(
  image(path, width: 100%),
  caption: [#caption],
)

#align(center)[
  #text(size: 18pt, weight: "bold", fill: rgb("#73000A"))[EMCH792 Final Project Report]

  #v(0.35em)
  #text(weight: "bold")[J.C. Vaught]

  #v(0.15em)
  #text(size: 9.5pt, fill: rgb("#363636"))[Generated from the MATLAB analysis pass on #generated_on.]
]

#v(0.8em)

#highlight[
  #dataset_note

  The calibration variances were estimated directly from the supplied datasets. The retained values were $R_1$ = #y1_variance_text and $R_2$ = #y2_variance_text. The short tuning sweep selected an initial covariance scale of #chosen_p0_scale_text and a #chosen_gate_label scalar gate with threshold #chosen_gate_threshold_text.
]

= Problem I

The first task was to estimate the two sensor variances from the calibration data and lock the deployment sample period. The calibration pass produced $R_1$ = #y1_variance_text for the range-like measurement and $R_2$ = #y2_variance_text for the cubic heading sensor. The deployment dataset remained uniformly sampled at #dt_text seconds, which allowed the rectangular covariance update required in the assignment to be implemented directly.

= Problem II

The estimators used the assignment state $x = [x, y, psi, u]^T$, steering and acceleration inputs, the fixed geometry $l_f = l_r = 1$, and the process covariance specified in the project prompt. Both filters applied the two scalar measurement updates in sequence, which made the gating logic transparent and allowed each sensor to be rejected independently. The workflow is summarized in the explanatory CeTZ diagram below.

#estimator_flow

For the rectangular comparison without gating, the UKF was clearly more accurate than the EKF on the nonlinear trajectory. The EKF rectangular run produced a position RMSE of #ekf_rect_no_gate_pos_text m with a heading RMSE of #ekf_rect_no_gate_heading_deg_text deg, while the UKF rectangular run reduced those values to #ukf_rect_no_gate_pos_text m and #ukf_rect_no_gate_heading_deg_text deg. That gap is consistent with the nonlinear measurement pair, especially the $psi^3$ sensor, where the sigma-point approximation handled curvature more gracefully than the first-order EKF linearization.

#full_width("figures/trajectory.png", [Truth and estimated trajectories. The no-gate UKF stays closest to the measured path, while the gated runs show the cost of relying more heavily on the imperfect process model late in the maneuver.])

#full_width("figures/state_timeseries.png", [State histories for the principal comparison cases. The gated filters improve heading consistency but become more prediction dominated in position and speed near the end of the record.])

= Problem III

The tuning sweep compared two defensible scalar chi-square thresholds, namely 95% and 99%, across five initial covariance scales. The selected combination was the #chosen_gate_label gate with a #chosen_p0_scale_text scaling on the base initial covariance because it minimized the composite score across the gated EKF and UKF rectangular runs.

#tuning_table

The gating study showed a mixed but interpretable result. The faulty $y_2$ sensor was rejected three times in every final gated run, which is visible as the isolated spikes in the lower NIS plot. Those rejections reduced the heading RMSE from #ekf_rect_no_gate_heading_deg_text deg to #ekf_rect_gate_heading_deg_text deg for the EKF and from #ukf_rect_no_gate_heading_deg_text deg to #ukf_rect_gate_heading_deg_text deg for the UKF. At the same time, the rectangular gated filters also rejected a large number of $y_1$ measurements, namely #ekf_rect_gate_rej_y1_text for the EKF and #ukf_rect_gate_rej_y1_text for the UKF, so the position RMSE worsened to #ekf_rect_gate_pos_text m and #ukf_rect_gate_pos_text m. The practical conclusion is that the gate successfully identified the obviously bad heading-like outliers, but the process model was not strong enough to carry the full state estimate once too many range-like measurements were withheld.

#full_width("figures/gating_diagnostics.png", [Normalized innovation squared histories for both sensors. The $y_2$ outliers are sharp and isolated, while the late $y_1$ residual growth explains why the gated runs become increasingly prediction dominated.])

= Problem IV

Replacing the UKF rectangular propagation with RK4 improved the ungated accuracy. The UKF RK4 run without gating achieved the best overall position RMSE in the study at #best_position_rmse_text m, improving on the rectangular UKF by #rk4_position_improvement_text m. Under the same gating logic, the RK4 variant also gave the best heading RMSE among the gated UKF runs at #ukf_rk4_gate_heading_deg_text deg, although the late measurement rejections still limited the position benefit.

The covariance histories below reinforce that comparison. The UKF covariance traces are larger than the EKF trace because the sigma-point method retains more nonlinear uncertainty, and the RK4 propagation keeps that covariance evolution slightly smoother than the rectangular UKF during the final portion of the maneuver.

#full_width("figures/covariance.png", [Diagonal covariance histories for the three gated comparison cases. The UKF variants carry more uncertainty than the EKF, which is consistent with the stronger nonlinear treatment.])

= Problem V

The runtime comparison used sixty repeated executions per configuration to smooth timer noise. The EKF remained the cheapest option at #ekf_rect_gate_runtime_ms_text ms per run on average, the rectangular UKF required #ukf_rect_gate_runtime_ms_text ms, and the RK4 UKF increased that cost to #ukf_rk4_gate_runtime_ms_text ms. The RK4 propagation therefore added about #rk4_runtime_penalty_text ms relative to the rectangular UKF, which is a modest penalty for a measurable gain in ungated trajectory accuracy.

#runtime_table

= Problem VI

The main conclusions are straightforward. The UKF was the better estimator for this dataset because the nonlinear dynamics and the $psi^3$ measurement were strong enough for the first-order EKF approximation to lose accuracy. The covariance comparison also favored the UKF qualitatively, since the sigma-point filters carried larger and more credible uncertainty envelopes instead of the tighter EKF trace. Measurement gating helped where it needed to help, namely by removing the worst $y_2$ outliers and reducing heading error, but it also exposed the weakness of the process model by rejecting too many late $y_1$ measurements. RK4 prediction was the cleanest upgrade in the study because it produced the best overall ungated trajectory while increasing runtime only slightly.

#metrics_table
