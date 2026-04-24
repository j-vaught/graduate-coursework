#let generated_on = "2026-04-24 19:51:59"
#let dt_text = "0.100"
#let y1_variance_text = "0.087247"
#let y2_variance_text = "0.006536"
#let p0_trace_ratio_text = "1.00"
#let chosen_gate_label = "99%"
#let chosen_gate_threshold_text = "6.6349"
#let best_configuration_text = "EKF rect., no gate"
#let best_position_rmse_text = "1.1366"
#let ekf_gating_position_change_text = "8.9421"
#let ukf_gating_position_change_text = "1.7155"
#let ekf_gating_heading_change_text = "0.8668"
#let ukf_gating_heading_improvement_text = "0.9017"
#let rk4_position_improvement_text = "0.2026"
#let rk4_runtime_penalty_text = "1.183"

#let ekf_rect_no_gate_pos_text = "1.1366"
#let ekf_rect_no_gate_heading_deg_text = "6.5907"
#let ekf_rect_no_gate_speed_text = "2.4161"
#let ekf_rect_no_gate_avg_trace_text = "1.2892"
#let ekf_rect_no_gate_rej_y1_text = "0"
#let ekf_rect_no_gate_rej_y2_text = "0"
#let ukf_rect_no_gate_pos_text = "2.8483"
#let ukf_rect_no_gate_heading_deg_text = "4.6895"
#let ukf_rect_no_gate_speed_text = "3.6135"
#let ukf_rect_no_gate_avg_trace_text = "9.8452"
#let ukf_rect_no_gate_rej_y1_text = "0"
#let ukf_rect_no_gate_rej_y2_text = "0"
#let ekf_rect_gate_pos_text = "10.0787"
#let ekf_rect_gate_heading_deg_text = "7.4575"
#let ekf_rect_gate_speed_text = "4.7815"
#let ekf_rect_gate_avg_trace_text = "2.0714"
#let ekf_rect_gate_rej_y1_text = "54"
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
#let ekf_rect_no_gate_runtime_ms_text = "1.795"
#let ukf_rect_no_gate_runtime_ms_text = "3.840"
#let ukf_rect_runtime_ms_text = "3.783"
#let ukf_rk4_runtime_ms_text = "4.967"

#let gate_best_position_filter_text = "EKF"
#let gate_best_position_setting_text = "No gate"
#let gate_best_position_rmse_text = "1.1366"
#let gate_best_heading_filter_text = "UKF"
#let gate_best_heading_setting_text = "99%"
#let gate_best_heading_rmse_text = "3.7879"
#let measurement_best_position_filter_text = "EKF"
#let measurement_best_position_setting_text = "Both sensors"
#let measurement_best_position_rmse_text = "1.1366"
#let measurement_best_heading_filter_text = "UKF"
#let measurement_best_heading_setting_text = "Both sensors"
#let measurement_best_heading_rmse_text = "4.6895"
#let prior_best_position_filter_text = "EKF"
#let prior_best_position_scale_text = "1"
#let prior_best_position_rmse_text = "1.1366"
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
  [EKF rect., no gate], [0.4643], [1.0375], [6.5907], [2.4161], [1.1366], [1.2892], [0], [0],
  [UKF rect., no gate], [1.7247], [2.2667], [4.6895], [3.6135], [2.8483], [9.8452], [0], [0],
  [EKF rect., gate], [4.4555], [9.0404], [7.4575], [4.7815], [10.0787], [2.0714], [54], [4],
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
  [EKF rect., no gate], [1.795], [0.262],
  [UKF rect., no gate], [3.840], [0.088],
)

#let problem6_runtime_table = table(
  columns: 3,
  align: (left, right, right),
  inset: 6pt,
  stroke: rgb("#363636"),
  table.header([Configuration], [Mean ms], [Std ms]),
  [UKF rect., no gate], [3.783], [0.024],
  [UKF RK4, no gate], [4.967], [0.390],
)

#let gate_ablation_table = table(
  columns: 8,
  align: (left, left, right, right, right, right, right, right),
  inset: 4pt,
  stroke: rgb("#363636"),
  table.header([Filter], [Gate], [Threshold], [Pos. RMSE], [Heading deg], [u RMSE], [avg tr(P)], [rej y1/y2]),
  [EKF], [No gate], [inf], [1.1366], [6.5907], [2.4161], [1.2892], [0/0],
  [EKF], [95%], [3.8415], [15.4246], [3.9191], [6.4733], [8.3374], [73/4],
  [EKF], [97.5%], [5.0239], [13.7354], [7.4132], [5.7437], [2.6139], [62/4],
  [EKF], [99%], [6.6349], [10.0787], [7.4575], [4.7815], [2.0714], [54/4],
  [EKF], [99.5%], [7.8794], [3.4566], [7.4905], [3.1344], [1.3724], [23/4],
  [EKF], [99.9%], [10.8276], [2.1637], [7.6113], [2.7038], [1.3294], [17/3],
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
  [EKF], [Both sensors], [1.1366], [6.5907], [2.4161], [1.2892], [0/0],
  [EKF], [y1 only], [25.0239], [107.5541], [5.9931], [8.0632], [0/0],
  [EKF], [y2 only], [16.2502], [8.6035], [6.6821], [18.4955], [0/0],
  [EKF], [Prediction only], [16.8624], [87.1463], [7.5095], [206.4571], [0/0],
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
  [EKF], [0.25], [3.2657], [20.5663], [1.6873], [0.5558],
  [EKF], [0.5], [3.6262], [19.8278], [1.6218], [0.8173],
  [EKF], [1], [1.1366], [6.5907], [2.4161], [1.2892],
  [EKF], [2], [1.1902], [7.3732], [2.3986], [1.4025],
  [EKF], [5], [1.6658], [13.5432], [1.9155], [1.6915],
  [EKF], [10], [3.8753], [32.5465], [1.6699], [2.9018],
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
