#let generated_on = "2026-04-24 14:30:50"
#let dt_text = "0.100"
#let y1_variance_text = "0.087247"
#let y2_variance_text = "0.006536"
#let p0_trace_ratio_text = "1.00"
#let chosen_gate_label = "99%"
#let chosen_gate_threshold_text = "6.6349"
#let best_configuration_text = "UKF RK4, no gate"
#let best_position_rmse_text = "2.6457"
#let ekf_gating_position_change_text = "11.6843"
#let ukf_gating_position_change_text = "1.7155"
#let ekf_gating_heading_improvement_text = "16.0203"
#let ukf_gating_heading_improvement_text = "0.9017"
#let rk4_position_improvement_text = "0.2026"
#let rk4_runtime_penalty_text = "0.965"

#let ekf_rect_no_gate_pos_text = "5.1335"
#let ekf_rect_no_gate_heading_deg_text = "22.1313"
#let ekf_rect_no_gate_speed_text = "1.4067"
#let ekf_rect_no_gate_avg_trace_text = "0.9432"
#let ekf_rect_no_gate_rej_y1_text = "0"
#let ekf_rect_no_gate_rej_y2_text = "0"
#let ukf_rect_no_gate_pos_text = "2.8483"
#let ukf_rect_no_gate_heading_deg_text = "4.6895"
#let ukf_rect_no_gate_speed_text = "3.6135"
#let ukf_rect_no_gate_avg_trace_text = "9.8452"
#let ukf_rect_no_gate_rej_y1_text = "0"
#let ukf_rect_no_gate_rej_y2_text = "0"
#let ekf_rect_gate_pos_text = "16.8178"
#let ekf_rect_gate_heading_deg_text = "6.1110"
#let ekf_rect_gate_speed_text = "6.4933"
#let ekf_rect_gate_avg_trace_text = "3.5597"
#let ekf_rect_gate_rej_y1_text = "73"
#let ekf_rect_gate_rej_y2_text = "4"
#let ukf_rect_gate_pos_text = "4.5638"
#let ukf_rect_gate_heading_deg_text = "3.7879"
#let ukf_rect_gate_speed_text = "5.5241"
#let ukf_rect_gate_avg_trace_text = "14.7626"
#let ukf_rect_gate_rej_y1_text = "19"
#let ukf_rect_gate_rej_y2_text = "4"
#let ukf_rk4_no_gate_pos_text = "2.6457"
#let ukf_rk4_no_gate_heading_deg_text = "4.7116"
#let ukf_rk4_no_gate_speed_text = "3.5487"
#let ukf_rk4_no_gate_avg_trace_text = "10.0960"
#let ukf_rk4_no_gate_rej_y1_text = "0"
#let ukf_rk4_no_gate_rej_y2_text = "0"
#let ukf_rk4_gate_pos_text = "4.6654"
#let ukf_rk4_gate_heading_deg_text = "3.7544"
#let ukf_rk4_gate_speed_text = "5.5725"
#let ukf_rk4_gate_avg_trace_text = "15.1788"
#let ukf_rk4_gate_rej_y1_text = "20"
#let ukf_rk4_gate_rej_y2_text = "4"
#let ekf_rect_no_gate_runtime_ms_text = "2.246"
#let ukf_rect_no_gate_runtime_ms_text = "3.750"
#let ukf_rect_runtime_ms_text = "3.615"
#let ukf_rk4_runtime_ms_text = "4.580"

#let metrics_table = table(
  columns: 9,
  align: (left, right, right, right, right, right, right, right, right),
  inset: 5pt,
  stroke: rgb("#363636"),
  table.header([Configuration], [x], [y], [psi deg], [u], [pos.], [avg tr(P)], [rej y1], [rej y2]),
  [EKF rect., no gate], [1.9084], [4.7656], [22.1313], [1.4067], [5.1335], [0.9432], [0], [0],
  [UKF rect., no gate], [1.7247], [2.2667], [4.6895], [3.6135], [2.8483], [9.8452], [0], [0],
  [EKF rect., gate], [10.8599], [12.8413], [6.1110], [6.4933], [16.8178], [3.5597], [73], [4],
  [UKF rect., gate], [2.8845], [3.5367], [3.7879], [5.5241], [4.5638], [14.7626], [19], [4],
  [UKF RK4, no gate], [1.6755], [2.0475], [4.7116], [3.5487], [2.6457], [10.0960], [0], [0],
  [UKF RK4, gate], [3.0439], [3.5357], [3.7544], [5.5725], [4.6654], [15.1788], [20], [4],
)

#let problem3_runtime_table = table(
  columns: 3,
  align: (left, right, right),
  inset: 6pt,
  stroke: rgb("#363636"),
  table.header([Configuration], [Mean ms], [Std ms]),
  [EKF rect., no gate], [2.246], [1.034],
  [UKF rect., no gate], [3.750], [0.129],
)

#let problem6_runtime_table = table(
  columns: 3,
  align: (left, right, right),
  inset: 6pt,
  stroke: rgb("#363636"),
  table.header([Configuration], [Mean ms], [Std ms]),
  [UKF rect., no gate], [3.615], [0.017],
  [UKF RK4, no gate], [4.580], [0.014],
)

#let dataset_note = [The script used 100 samples at #dt_text s and initialized the filters from a zero-centered prior with the nominal base covariance so the comparisons did not consume deployment truth as estimator input.]
