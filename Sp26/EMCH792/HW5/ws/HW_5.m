%% Clear and close everything
clear; close all; clc;

% Load HW data
load("HW5_data.mat")
time_steps = height(HW5_data);

%% 0. Start by entering your last name
lastName = "Vaught";
display("EMCH-792 HW5, " + lastName)

%% 1. Initialize the system
% Known mass-spring-damper constants
m = 1.0;
b = 2.5;
k = 5.0;
Ts = 0.1;

% State vector x = [position; velocity]
Ac = [0, 1; -k / m, -b / m];
Bc = [0; 1 / m];
H_pos = [1, 0];

% Exact zero-order-hold discretization
Ad = expm(Ac * Ts);
Bd = Ac \ ((Ad - eye(size(Ac))) * Bc);

% Discrete process and measurement models
Q = diag([0.005, 0.005]);
R_square_root = diag([0.025, 0.001]);
R_sequential = [0.025, 0.001];
H_square_root = [H_pos; H_pos];

% Numeric discrete-time dynamics for Problem 1
% x(k+1) = Ad x(k) + Bd u(k) + w(k)
% Ad = [ 0.9770535888,  0.0877449614;
%       -0.4387248068,  0.7576911854]
% Bd = [0.0045892822;
%       0.0877449614]

% Extract signals from the provided table
time = HW5_data.time.';
u = HW5_data.u.';
pos_true = HW5_data.pos_true.';
vel_true = HW5_data.vel_true.';
y1 = HW5_data.y1.';
y2 = HW5_data.y2.';

% Common initialization
x0_est = [0; 0];
P0 = [1, 0; 0, 2];
n_states = size(Ad, 1);

% Chi-square threshold for one scalar measurement with upper-tail area 0.005
gate_threshold = 2 * gammaincinv(0.995, 0.5);

%% 2. Square-Root filter
% Initialize the variables to store the estimated state,
% the error covariance matrix, the process and the measurement noise
% covariance
x_est_square_root = zeros(n_states, time_steps);
x_est_square_root(:, 1) = x0_est;

P_square_root_store = zeros(n_states, n_states, time_steps);
P_square_root_store(:, :, 1) = P0;

S_square_root = chol(P0, "lower");
S_Q = chol(Q, "lower");
S_R_square_root = chol(R_square_root, "lower");

% Simulate the system for all provided time steps while collecting the
% estimated states, a posteriori error covariance
for i = 2:time_steps
    x_prior = Ad * x_est_square_root(:, i - 1) + Bd * u(i - 1);
    S_prior = square_root_predict(Ad, S_square_root, S_Q);

    z_k = [y1(i); y2(i)];
    [x_post, S_post] = square_root_update(x_prior, S_prior, z_k, ...
        H_square_root, S_R_square_root);

    x_est_square_root(:, i) = x_post;
    S_square_root = S_post;
    P_square_root_store(:, :, i) = S_square_root * S_square_root.';
end

%% 3. Plot the Square-Root filter results
colors = usc_colors();

% Position plot
figure("Name", "Square-Root Filter Position", "Color", colors.white);
hold on
plot(time, pos_true, "-", "Color", colors.black, "LineWidth", 1.8)
plot(time, x_est_square_root(1, :), "--", "Color", colors.garnet, ...
    "LineWidth", 1.8)
plot(time, y1, "s", "Color", colors.atlantic, "LineStyle", "none", ...
    "MarkerSize", 5, "LineWidth", 1.0)
plot(time, y2, "x", "Color", colors.honeycomb, "LineStyle", "none", ...
    "MarkerSize", 5, "LineWidth", 1.2)
hold off
grid on
box on
title("Square-Root Kalman Filter Position")
xlabel("Time [s]")
ylabel("Position [m]")
legend("True Position", "Estimated Position", "Sensor 1", "Sensor 2", ...
    "Location", "best")
style_axes(gca, colors)

% Velocity plot
figure("Name", "Square-Root Filter Velocity", "Color", colors.white);
hold on
plot(time, vel_true, "-", "Color", colors.black, "LineWidth", 1.8)
plot(time, x_est_square_root(2, :), "--", "Color", colors.garnet, ...
    "LineWidth", 1.8)
hold off
grid on
box on
title("Square-Root Kalman Filter Velocity")
xlabel("Time [s]")
ylabel("Velocity [m/s]")
legend("True Velocity", "Estimated Velocity", "Location", "best")
style_axes(gca, colors)

%% 4. Sequential Kalman Filter
% Initialize the variables to store the estimated state,
% the error covariance matrix, the process and the measurement noise
% covariance
x_est_sequential = zeros(n_states, time_steps);
x_est_sequential(:, 1) = x0_est;

P_sequential = P0;
P_sequential_store = zeros(n_states, n_states, time_steps);
P_sequential_store(:, :, 1) = P0;

accepted_measurements = false(2, time_steps);
nis_history = nan(2, time_steps);

% Simulate the system for all provided time steps while collecting the
% estimated states, a posteriori error covariance
for i = 2:time_steps
    x_prior = Ad * x_est_sequential(:, i - 1) + Bd * u(i - 1);
    P_prior = Ad * P_sequential * Ad.' + Q;

    % Process the reliable sensor first, then gate the more accurate
    % fault-prone sensor against the updated estimate.
    measurement_values = [y1(i), y2(i)];

    x_post = x_prior;
    P_post = P_prior;

    for sensor_idx = 1:numel(measurement_values)
        [x_post, P_post, accepted_measurements(sensor_idx, i), ...
            nis_history(sensor_idx, i)] = gated_scalar_update(x_post, ...
            P_post, measurement_values(sensor_idx), H_pos, ...
            R_sequential(sensor_idx), gate_threshold);
    end

    x_est_sequential(:, i) = x_post;
    P_sequential = P_post;
    P_sequential_store(:, :, i) = P_sequential;
end

%% 5. Plot the sequential filter results
rejected_sensor_2 = ~accepted_measurements(2, :);
rejected_sensor_2(1) = false;

% Position plot
figure("Name", "Sequential Filter Position", "Color", colors.white);
hold on
plot(time, pos_true, "-", "Color", colors.black, "LineWidth", 1.8)
plot(time, x_est_sequential(1, :), "--", "Color", colors.rose, ...
    "LineWidth", 1.8)
plot(time, y1, "s", "Color", colors.atlantic, "LineStyle", "none", ...
    "MarkerSize", 5, "LineWidth", 1.0)
plot(time, y2, "x", "Color", colors.congaree, "LineStyle", "none", ...
    "MarkerSize", 5, "LineWidth", 1.2)
plot(time(rejected_sensor_2), y2(rejected_sensor_2), "s", ...
    "Color", colors.garnet, "LineStyle", "none", "MarkerSize", 8, ...
    "LineWidth", 1.2)
hold off
grid on
box on
title("Sequential Kalman Filter Position with Measurement Gating")
xlabel("Time [s]")
ylabel("Position [m]")
legend("True Position", "Estimated Position", "Sensor 1", ...
    "Sensor 2", "Rejected Sensor 2", "Location", "best")
style_axes(gca, colors)

% Velocity plot
figure("Name", "Sequential Filter Velocity", "Color", colors.white);
hold on
plot(time, vel_true, "-", "Color", colors.black, "LineWidth", 1.8)
plot(time, x_est_sequential(2, :), "--", "Color", colors.rose, ...
    "LineWidth", 1.8)
hold off
grid on
box on
title("Sequential Kalman Filter Velocity")
xlabel("Time [s]")
ylabel("Velocity [m/s]")
legend("True Velocity", "Estimated Velocity", "Location", "best")
style_axes(gca, colors)

% Brief numerical summary for quick verification
square_root_position_rmse = sqrt(mean((pos_true - x_est_square_root(1, :)).^2));
sequential_position_rmse = sqrt(mean((pos_true - x_est_sequential(1, :)).^2));
square_root_velocity_rmse = sqrt(mean((vel_true - x_est_square_root(2, :)).^2));
sequential_velocity_rmse = sqrt(mean((vel_true - x_est_sequential(2, :)).^2));

fprintf("Square-root position RMSE: %.6f m\n", square_root_position_rmse)
fprintf("Sequential position RMSE: %.6f m\n", sequential_position_rmse)
fprintf("Square-root velocity RMSE: %.6f m/s\n", square_root_velocity_rmse)
fprintf("Sequential velocity RMSE: %.6f m/s\n", sequential_velocity_rmse)
fprintf("Sequential filter rejected %d of %d sensor-2 updates.\n", ...
    sum(rejected_sensor_2), time_steps - 1)


function S_pred = square_root_predict(A, S_prev, S_process)
    [~, R_qr] = qr([A * S_prev, S_process].', 0);
    S_pred = tril(R_qr.');
end


function [x_post, S_post] = square_root_update(x_pred, S_pred, z, H, S_meas)
    [~, R_qr] = qr([H * S_pred, S_meas].', 0);
    S_innovation = tril(R_qr.');

    P_pred = S_pred * S_pred.';
    K = ((P_pred * H.') / S_innovation.') / S_innovation;
    x_post = x_pred + K * (z - H * x_pred);

    U_post = S_pred.';
    downdate_vectors = K * S_innovation;
    for col_idx = 1:size(downdate_vectors, 2)
        U_post = cholupdate(U_post, downdate_vectors(:, col_idx), "-");
    end
    S_post = U_post.';
end


function [x_post, P_post, accepted, nis_value] = gated_scalar_update( ...
    x_prior, P_prior, measurement, H, R, gate_threshold)

    innovation = measurement - H * x_prior;
    innovation_variance = H * P_prior * H.' + R;
    nis_value = (innovation^2) / innovation_variance;
    accepted = nis_value <= gate_threshold;

    if accepted
        K = (P_prior * H.') / innovation_variance;
        x_post = x_prior + K * innovation;
        identity_matrix = eye(size(P_prior));
        P_post = (identity_matrix - K * H) * P_prior * ...
            (identity_matrix - K * H).' + K * R * K.';
    else
        x_post = x_prior;
        P_post = P_prior;
    end

    P_post = (P_post + P_post.') / 2;
end


function colors = usc_colors()
    colors.garnet = [115, 0, 10] / 255;
    colors.black = [0, 0, 0] / 255;
    colors.white = [255, 255, 255] / 255;
    colors.black90 = [54, 54, 54] / 255;
    colors.black70 = [92, 92, 92] / 255;
    colors.black50 = [162, 162, 162] / 255;
    colors.black30 = [199, 199, 199] / 255;
    colors.black10 = [236, 236, 236] / 255;
    colors.warm_grey = [103, 97, 86] / 255;
    colors.sandstorm = [255, 242, 227] / 255;
    colors.rose = [204, 46, 64] / 255;
    colors.atlantic = [70, 106, 159] / 255;
    colors.congaree = [31, 65, 77] / 255;
    colors.horseshoe = [101, 120, 11] / 255;
    colors.grass = [206, 211, 24] / 255;
    colors.honeycomb = [164, 145, 55] / 255;
end


function style_axes(ax, colors)
    ax.LineWidth = 1.0;
    ax.FontSize = 11;
    ax.XColor = colors.black90;
    ax.YColor = colors.black90;
    ax.GridColor = colors.black30;
    ax.MinorGridColor = colors.black10;
    ax.Color = colors.white;
end
