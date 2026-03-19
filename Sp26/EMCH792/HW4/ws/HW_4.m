%% Clear and close everything
clear; close all; clc;
rng(792, "twister");  % reproducible stochastic simulation

%% 0. Start by entering your last name
lastName = "Vaught";
display("EMCH-792 HW4, " + lastName)

%% 1. Derive the discrete time system dynamics

% Continuous-time mass-spring-damper: m*x_ddot + b*x_dot + k*x = u(t)
% Parameters
m = 1;      % mass [kg]
b = 2.5;    % damping coefficient [Ns/m]
k = 5;      % spring constant [N/m]

% Continuous-time state-space: x_dot = A*x + B*u
A = [0, 1; -k/m, -b/m];
B = [0; 1/m];

% Discretize using matrix exponential (Eq. 1.104)
Ts = 0.1;                           % sampling period [s]
F = expm(A * Ts);                   % discrete state transition matrix
G = (F - eye(2)) * inv(A) * B;     % discrete input matrix

% Observation matrix (measure position only)
H = [1, 0];

% Noise covariances
Q = 0.01 * eye(2);   % process noise covariance
R = 0.01;            % measurement noise variance

fprintf('F = \n'); disp(F);
fprintf('G = \n'); disp(G);

%% 2. Simulate the system for 10 seconds while collecting the true and
% estimated states, the measurements and the a priori and a posteriori
% error covariance

Tf = 10;              % total simulation time [s]
N = round(Tf / Ts);   % number of time steps

% Initial conditions
x_true = [0; 0];
x_est  = [0; 0];
P_post = [1, 0; 0, 2];

% Pre-allocate storage
x_true_hist = zeros(2, N);
x_est_hist  = zeros(2, N);
y_hist      = zeros(1, N);
P_pri_hist  = zeros(2, 2, N);
P_post_hist = zeros(2, 2, N);

for k_step = 1:N
    % Input signal
    u = 10 * sin((k_step - 1) * Ts);

    % True state propagation with process noise
    w = chol(Q)' * randn(2, 1);
    x_true = F * x_true + G * u + w;

    % Measurement with noise
    v = sqrt(R) * randn;
    y = H * x_true + v;

    % --- Kalman Filter (Eq. 5.19) ---
    % Time update (prediction)
    x_pred = F * x_est + G * u;
    P_pri  = F * P_post * F' + Q;

    % Measurement update (correction)
    K      = P_pri * H' / (H * P_pri * H' + R);
    x_est  = x_pred + K * (y - H * x_pred);
    P_post = (eye(2) - K * H) * P_pri;

    % Store
    x_true_hist(:, k_step) = x_true;
    x_est_hist(:, k_step)  = x_est;
    y_hist(k_step)         = y;
    P_pri_hist(:, :, k_step)  = P_pri;
    P_post_hist(:, :, k_step) = P_post;
end

t = (1:N) * Ts;  % time vector

%% 3. Calculate the mean and std of the error between the true and
% estimated state.

err = x_true_hist - x_est_hist;

err_mean_pos = mean(err(1, :));
err_std_pos  = std(err(1, :));
err_mean_vel = mean(err(2, :));
err_std_vel  = std(err(2, :));

fprintf('\n--- Error Statistics ---\n');
fprintf('Position error: mean = %.4f, std = %.4f\n', err_mean_pos, err_std_pos);
fprintf('Velocity error: mean = %.4f, std = %.4f\n', err_mean_vel, err_std_vel);

% What can you comment about the calculated values?
% The mean error is approximately zero for both states, indicating
% the Kalman Filter is an unbiased estimator.

% How does the calculated std compare to the steady state theoretical std
% from the a posteriori error covariance matrix?
P_post_final = P_post_hist(:, :, N);
theo_std_pos = sqrt(P_post_final(1, 1));
theo_std_vel = sqrt(P_post_final(2, 2));

fprintf('\nComparison of calculated std vs theoretical steady-state std:\n');
fprintf('Position: calculated std = %.4f, theoretical std = %.4f\n', err_std_pos, theo_std_pos);
fprintf('Velocity: calculated std = %.4f, theoretical std = %.4f\n', err_std_vel, theo_std_vel);

% Steady-state comparison should use only the converged portion.
ss_start_idx = floor(0.5 * N) + 1;
err_ss = err(:, ss_start_idx:end);
P_post_ss_mean = mean(P_post_hist(:, :, ss_start_idx:end), 3);
err_ss_std_pos = std(err_ss(1, :));
err_ss_std_vel = std(err_ss(2, :));
theo_ss_std_pos = sqrt(P_post_ss_mean(1, 1));
theo_ss_std_vel = sqrt(P_post_ss_mean(2, 2));

fprintf('\nSteady-state-only comparison (last 50%% of samples):\n');
fprintf('Position: empirical ss std = %.4f, covariance-based ss std = %.4f\n', err_ss_std_pos, theo_ss_std_pos);
fprintf('Velocity: empirical ss std = %.4f, covariance-based ss std = %.4f\n', err_ss_std_vel, theo_ss_std_vel);

% The calculated standard deviation should be close to the theoretical
% steady-state standard deviation from the final a posteriori error
% covariance matrix, confirming the filter has converged to its
% steady-state performance.

%% 4. Plot the true, estimated, and measured position.

% Brand colors
garnet   = [115, 0, 10] / 255;
atlantic = [70, 106, 159] / 255;
honeycomb = [164, 145, 55] / 255;
black90  = [54, 54, 54] / 255;

figure(1);
plot(t, x_true_hist(1, :), '-', 'Color', garnet, 'LineWidth', 1.5); hold on;
plot(t, x_est_hist(1, :), '-', 'Color', atlantic, 'LineWidth', 1.5);
plot(t, y_hist, '.', 'Color', honeycomb, 'MarkerSize', 8);
hold off;
xlabel('Time [s]');
ylabel('Position [m]');
title('Position: True, Estimated, and Measured');
legend('True', 'Estimated', 'Measured', 'Location', 'best');
grid on;
set(gca, 'Box', 'on');

% Plot the true and estimated velocity.
figure(2);
plot(t, x_true_hist(2, :), '-', 'Color', garnet, 'LineWidth', 1.5); hold on;
plot(t, x_est_hist(2, :), '-', 'Color', atlantic, 'LineWidth', 1.5);
hold off;
xlabel('Time [s]');
ylabel('Velocity [m/s]');
title('Velocity: True and Estimated');
legend('True', 'Estimated', 'Location', 'best');
grid on;
set(gca, 'Box', 'on');

%% 5. Plot the position error and the expected bounds.

sigma_pos = squeeze(sqrt(P_post_hist(1, 1, :)))';
sigma_vel = squeeze(sqrt(P_post_hist(2, 2, :)))';

figure(3);
plot(t, err(1, :), '-', 'Color', garnet, 'LineWidth', 1.2); hold on;
plot(t, 2 * sigma_pos, '--', 'Color', atlantic, 'LineWidth', 1.2);
plot(t, -2 * sigma_pos, '--', 'Color', atlantic, 'LineWidth', 1.2);
hold off;
xlabel('Time [s]');
ylabel('Position Error [m]');
title('Position Estimation Error with \pm2\sigma Bounds');
legend('Error', '+2\sigma', '-2\sigma', 'Location', 'best');
grid on;
set(gca, 'Box', 'on');

% Plot the velocity error and the expected bounds.
figure(4);
plot(t, err(2, :), '-', 'Color', garnet, 'LineWidth', 1.2); hold on;
plot(t, 2 * sigma_vel, '--', 'Color', atlantic, 'LineWidth', 1.2);
plot(t, -2 * sigma_vel, '--', 'Color', atlantic, 'LineWidth', 1.2);
hold off;
xlabel('Time [s]');
ylabel('Velocity Error [m/s]');
title('Velocity Estimation Error with \pm2\sigma Bounds');
legend('Error', '+2\sigma', '-2\sigma', 'Location', 'best');
grid on;
set(gca, 'Box', 'on');

%% 6. Plot the a priori and a posteriori error covariance

steps = 1:N;

P_pri_11  = squeeze(P_pri_hist(1, 1, :));
P_post_11 = squeeze(P_post_hist(1, 1, :));
P_pri_22  = squeeze(P_pri_hist(2, 2, :));
P_post_22 = squeeze(P_post_hist(2, 2, :));
P_pri_12  = squeeze(P_pri_hist(1, 2, :));
P_post_12 = squeeze(P_post_hist(1, 2, :));

figure(5);
subplot(3, 1, 1);
plot(steps, P_pri_11, '-', 'Color', garnet, 'LineWidth', 1.2); hold on;
plot(steps, P_post_11, '-', 'Color', atlantic, 'LineWidth', 1.2);
hold off;
xlabel('Time Step');
ylabel('Variance [m^2]');
title('Position Variance: P_{pri}(1,1) and P_{post}(1,1)');
legend('A Priori', 'A Posteriori', 'Location', 'best');
grid on;
set(gca, 'Box', 'on');

subplot(3, 1, 2);
plot(steps, P_pri_22, '-', 'Color', garnet, 'LineWidth', 1.2); hold on;
plot(steps, P_post_22, '-', 'Color', atlantic, 'LineWidth', 1.2);
hold off;
xlabel('Time Step');
ylabel('Variance [(m/s)^2]');
title('Velocity Variance: P_{pri}(2,2) and P_{post}(2,2)');
legend('A Priori', 'A Posteriori', 'Location', 'best');
grid on;
set(gca, 'Box', 'on');

subplot(3, 1, 3);
plot(steps, P_pri_12, '-', 'Color', garnet, 'LineWidth', 1.2); hold on;
plot(steps, P_post_12, '-', 'Color', atlantic, 'LineWidth', 1.2);
hold off;
xlabel('Time Step');
ylabel('Covariance [m^2/s]');
title('Cross Covariance: P_{pri}(1,2) and P_{post}(1,2)');
legend('A Priori', 'A Posteriori', 'Location', 'best');
grid on;
set(gca, 'Box', 'on');

%% Save figures
saveas(figure(1), 'position_plot.png');
saveas(figure(2), 'velocity_plot.png');
saveas(figure(3), 'position_error.png');
saveas(figure(4), 'velocity_error.png');
saveas(figure(5), 'covariance_plot.png');
