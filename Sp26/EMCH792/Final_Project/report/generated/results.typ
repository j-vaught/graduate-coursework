#let generated_on = "2026-04-24 13:39:36"
#let dt_text = "0.100"
#let y1_variance_text = "0.087247"
#let y2_variance_text = "0.006536"
#let p0_trace_ratio_text = "0.50"
#let chosen_gate_label = "99%"
#let chosen_gate_threshold_text = "6.6349"
#let best_configuration_text = "UKF RK4, no gate"
#let best_position_rmse_text = "1.4206"
#let ekf_gating_position_change_text = "0.2061"
#let ukf_gating_position_change_text = "2.4006"
#let ekf_gating_heading_improvement_text = "12.7993"
#let ukf_gating_heading_improvement_text = "1.1132"
#let rk4_position_improvement_text = "0.2673"
#let rk4_runtime_penalty_text = "0.950"

#let ekf_rect_no_gate_pos_text = "3.6891"
#let ekf_rect_no_gate_heading_deg_text = "17.8381"
#let ekf_rect_no_gate_speed_text = "1.5688"
#let ekf_rect_no_gate_avg_trace_text = "0.7417"
#let ekf_rect_no_gate_rej_y1_text = "0"
#let ekf_rect_no_gate_rej_y2_text = "0"
#let ukf_rect_no_gate_pos_text = "1.6879"
#let ukf_rect_no_gate_heading_deg_text = "4.9532"
#let ukf_rect_no_gate_speed_text = "2.9613"
#let ukf_rect_no_gate_avg_trace_text = "6.0709"
#let ukf_rect_no_gate_rej_y1_text = "0"
#let ukf_rect_no_gate_rej_y2_text = "0"
#let ekf_rect_gate_pos_text = "3.8951"
#let ekf_rect_gate_heading_deg_text = "5.0388"
#let ekf_rect_gate_speed_text = "3.6671"
#let ekf_rect_gate_avg_trace_text = "1.1537"
#let ekf_rect_gate_rej_y1_text = "24"
#let ekf_rect_gate_rej_y2_text = "3"
#let ukf_rect_gate_pos_text = "4.0885"
#let ukf_rect_gate_heading_deg_text = "3.8400"
#let ukf_rect_gate_speed_text = "4.5974"
#let ukf_rect_gate_avg_trace_text = "13.0001"
#let ukf_rect_gate_rej_y1_text = "14"
#let ukf_rect_gate_rej_y2_text = "3"
#let ukf_rk4_no_gate_pos_text = "1.4206"
#let ukf_rk4_no_gate_heading_deg_text = "5.0272"
#let ukf_rk4_no_gate_speed_text = "2.8578"
#let ukf_rk4_no_gate_avg_trace_text = "5.9494"
#let ukf_rk4_no_gate_rej_y1_text = "0"
#let ukf_rk4_no_gate_rej_y2_text = "0"
#let ukf_rk4_gate_pos_text = "3.5206"
#let ukf_rk4_gate_heading_deg_text = "3.7895"
#let ukf_rk4_gate_speed_text = "4.5681"
#let ukf_rk4_gate_avg_trace_text = "12.7821"
#let ukf_rk4_gate_rej_y1_text = "15"
#let ukf_rk4_gate_rej_y2_text = "3"
#let ekf_rect_no_gate_runtime_ms_text = "2.228"
#let ukf_rect_no_gate_runtime_ms_text = "3.976"
#let ukf_rect_runtime_ms_text = "3.786"
#let ukf_rk4_runtime_ms_text = "4.736"

#let metrics_table = table(
  columns: 9,
  align: (left, right, right, right, right, right, right, right, right),
  inset: 5pt,
  stroke: rgb("#363636"),
  table.header([Configuration], [x], [y], [psi deg], [u], [pos.], [avg tr(P)], [rej y1], [rej y2]),
  [EKF rect., no gate], [1.1828], [3.4943], [17.8381], [1.5688], [3.6891], [0.7417], [0], [0],
  [UKF rect., no gate], [1.0710], [1.3046], [4.9532], [2.9613], [1.6879], [6.0709], [0], [0],
  [EKF rect., gate], [1.8305], [3.4382], [5.0388], [3.6671], [3.8951], [1.1537], [24], [3],
  [UKF rect., gate], [2.2324], [3.4252], [3.8400], [4.5974], [4.0885], [13.0001], [14], [3],
  [UKF RK4, no gate], [0.9634], [1.0441], [5.0272], [2.8578], [1.4206], [5.9494], [0], [0],
  [UKF RK4, gate], [2.2670], [2.6936], [3.7895], [4.5681], [3.5206], [12.7821], [15], [3],
)

#let problem3_runtime_table = table(
  columns: 3,
  align: (left, right, right),
  inset: 6pt,
  stroke: rgb("#363636"),
  table.header([Configuration], [Mean ms], [Std ms]),
  [EKF rect., no gate], [2.228], [0.846],
  [UKF rect., no gate], [3.976], [0.329],
)

#let problem6_runtime_table = table(
  columns: 3,
  align: (left, right, right),
  inset: 6pt,
  stroke: rgb("#363636"),
  table.header([Configuration], [Mean ms], [Std ms]),
  [UKF rect., no gate], [3.786], [0.058],
  [UKF RK4, no gate], [4.736], [0.017],
)

#let dataset_note = [The script used 100 samples at #dt_text s and initialized the filters from the first truth state to isolate estimator behavior from startup mismatch.]
