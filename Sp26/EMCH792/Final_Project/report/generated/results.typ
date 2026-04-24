#let generated_on = "2026-04-24 14:58:34"
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
#let rk4_runtime_penalty_text = "0.960"

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
#let ekf_rect_no_gate_runtime_ms_text = "1.759"
#let ukf_rect_no_gate_runtime_ms_text = "3.849"
#let ukf_rect_runtime_ms_text = "3.741"
#let ukf_rk4_runtime_ms_text = "4.700"

#let gate_best_position_filter_text = "EKF"
#let gate_best_position_setting_text = "99.9%"
#let gate_best_position_rmse_text = "2.5889"
#let gate_best_heading_filter_text = "UKF"
#let gate_best_heading_setting_text = "99%"
#let gate_best_heading_rmse_text = "3.7879"
#let measurement_best_position_filter_text = "UKF"
#let measurement_best_position_setting_text = "Both sensors"
#let measurement_best_position_rmse_text = "2.8483"
#let measurement_best_heading_filter_text = "UKF"
#let measurement_best_heading_setting_text = "Both sensors"
#let measurement_best_heading_rmse_text = "4.6895"
#let prior_best_position_filter_text = "UKF"
#let prior_best_position_scale_text = "0.5"
#let prior_best_position_rmse_text = "1.6879"
#let ukf_alpha_best_position_text = "0.1"
#let ukf_alpha_best_position_rmse_text = "1.5576"
#let ukf_alpha_best_heading_text = "0.001"
#let ukf_alpha_best_heading_rmse_text = "4.6895"

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
  [EKF rect., no gate], [1.759], [0.182],
  [UKF rect., no gate], [3.849], [0.081],
)

#let problem6_runtime_table = table(
  columns: 3,
  align: (left, right, right),
  inset: 6pt,
  stroke: rgb("#363636"),
  table.header([Configuration], [Mean ms], [Std ms]),
  [UKF rect., no gate], [3.741], [0.023],
  [UKF RK4, no gate], [4.700], [0.035],
)

#let gate_ablation_table = table(
  columns: 8,
  align: (left, left, right, right, right, right, right, right),
  inset: 4pt,
  stroke: rgb("#363636"),
  table.header([Filter], [Gate], [Threshold], [Pos. RMSE], [Heading deg], [u RMSE], [avg tr(P)], [rej y1/y2]),
  [EKF], [No gate], [inf], [5.1335], [22.1313], [1.4067], [0.9432], [0/0],
  [EKF], [95%], [3.8415], [16.8178], [6.1110], [6.4933], [3.5597], [73/4],
  [EKF], [97.5%], [5.0239], [16.8178], [6.1110], [6.4933], [3.5597], [73/4],
  [EKF], [99%], [6.6349], [16.8178], [6.1110], [6.4933], [3.5597], [73/4],
  [EKF], [99.5%], [7.8794], [3.4633], [7.7553], [3.0603], [1.2323], [23/4],
  [EKF], [99.9%], [10.8276], [2.5889], [7.8727], [2.7683], [1.2038], [19/3],
  [UKF], [No gate], [inf], [2.8483], [4.6895], [3.6135], [9.8452], [0/0],
  [UKF], [95%], [3.8415], [4.8416], [3.7884], [5.5797], [14.8075], [21/4],
  [UKF], [97.5%], [5.0239], [4.6934], [3.7882], [5.5575], [14.7811], [20/4],
  [UKF], [99%], [6.6349], [4.5638], [3.7879], [5.5241], [14.7626], [19/4],
  [UKF], [99.5%], [7.8794], [4.2038], [3.8281], [5.3530], [14.4930], [17/3],
  [UKF], [99.9%], [10.8276], [4.0511], [4.0355], [5.2370], [14.4700], [15/2],
)

#let measurement_ablation_table = table(
  columns: 7,
  align: (left, left, right, right, right, right, right),
  inset: 4pt,
  stroke: rgb("#363636"),
  table.header([Filter], [Measurements], [Pos. RMSE], [Heading deg], [u RMSE], [avg tr(P)], [rej y1/y2]),
  [EKF], [Both sensors], [5.1335], [22.1313], [1.4067], [0.9432], [0/0],
  [EKF], [y1 only], [25.5305], [108.8226], [6.1079], [5.7131], [0/0],
  [EKF], [y2 only], [16.2937], [8.6002], [6.6772], [17.8372], [0/0],
  [EKF], [Prediction only], [16.8624], [87.1463], [7.5095], [186.3590], [0/0],
  [UKF], [Both sensors], [2.8483], [4.6895], [3.6135], [9.8452], [0/0],
  [UKF], [y1 only], [19.7425], [82.0128], [6.5254], [79.6766], [0/0],
  [UKF], [y2 only], [13.1532], [5.3094], [6.9164], [43.3161], [0/0],
  [UKF], [Prediction only], [11.3987], [87.1463], [7.5095], [214.3545], [0/0],
)

#let prior_ablation_table = table(
  columns: 6,
  align: (left, right, right, right, right, right),
  inset: 4pt,
  stroke: rgb("#363636"),
  table.header([Filter], [$P_0$ scale], [Pos. RMSE], [Heading deg], [u RMSE], [avg tr(P)]),
  [EKF], [0.25], [2.7316], [14.8990], [1.6901], [0.6158],
  [EKF], [0.5], [3.6891], [17.8381], [1.5688], [0.7417],
  [EKF], [1], [5.1335], [22.1313], [1.4067], [0.9432],
  [EKF], [2], [3.2750], [14.9076], [1.5857], [1.3990],
  [EKF], [5], [3.3912], [17.3085], [1.6009], [1.7238],
  [EKF], [10], [2.3993], [29.3424], [1.8481], [2.9515],
  [UKF], [0.25], [1.9343], [4.9912], [2.8874], [4.3863],
  [UKF], [0.5], [1.6879], [4.9532], [2.9613], [6.0709],
  [UKF], [1], [2.8483], [4.6895], [3.6135], [9.8452],
  [UKF], [2], [3.7641], [4.7030], [4.0733], [16.9142],
  [UKF], [5], [5.0043], [5.0142], [3.7185], [45.8353],
  [UKF], [10], [13.2877], [4.5313], [3.9228], [117.1644],
)

#let ukf_spread_ablation_table = table(
  columns: 5,
  align: (right, right, right, right, right),
  inset: 5pt,
  stroke: rgb("#363636"),
  table.header([$alpha$], [Pos. RMSE], [Heading deg], [u RMSE], [avg tr(P)]),
  [0.001], [2.8483], [4.6895], [3.6135], [9.8452],
  [0.03], [2.6800], [4.7987], [3.5114], [9.6139],
  [0.1], [1.5576], [5.7322], [2.6673], [7.6227],
  [0.3], [1.7316], [10.8339], [2.7370], [4.6149],
  [0.7], [1.7405], [14.9804], [2.8656], [4.1723],
  [1], [1.8150], [15.7675], [2.9690], [4.1409],
)

#let dataset_note = [The script used 100 samples at #dt_text s and initialized the filters from a zero-centered prior with the nominal base covariance so the comparisons did not consume deployment truth as estimator input.]
