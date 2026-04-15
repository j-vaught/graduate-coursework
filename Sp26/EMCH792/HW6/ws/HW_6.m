%% Clear and close everything
clear; close all; clc;

% Load HW data
load('HW6_data.mat')
time_steps = length(HW6_data.time);

%% 0. Start by entering your last name
lastName = "Vaught";
display("EMCH-792 HW6, " + lastName)

% Initialize system constants
r  = 0.1;
l  = 0.2;
dt = HW6_data.time(2) - HW6_data.time(1);

n = 3;  % state dim
m = 2;  % meas dim

% Initialize R and Q matrices
Q = diag([0.03, 0.03, 0.20]);
R = diag([0.0025, 0.0025]);

% Pull signals out of the data table for convenience
x_true   = HW6_data.x;
y_true   = HW6_data.y;
phi_true = HW6_data.phi;
ur       = HW6_data.ur;
ul       = HW6_data.ul;
y1_meas  = HW6_data.y1;
y2_meas  = HW6_data.y2;

t = HW6_data.time;

% Brand colors
c_garnet   = [115, 0, 10]/255;
c_black    = [0, 0, 0];
c_atlantic = [70, 106, 159]/255;
c_grey     = [92, 92, 92]/255;

%% 1. Extended Kalman Filter
X_ekf    = zeros(n, time_steps);
P_ekf    = zeros(n, n, time_steps);
sig_ekf  = zeros(n, time_steps);

X_ekf(:,1)     = [0; 0; 0];
P_ekf(:,:,1)   = diag([0.1, 0.1, 0.01]);
sig_ekf(:,1)   = sqrt(diag(P_ekf(:,:,1)));

for i = 2:time_steps
    % Previous estimate
    x_prev = X_ekf(:, i-1);
    P_prev = P_ekf(:, :, i-1);
    u_prev = [ur(i-1); ul(i-1)];

    % --- Predict ---
    x_pred = f_robot(x_prev, u_prev, r, l, dt);
    F      = getF(x_prev, u_prev, r, dt);
    P_pred = F * P_prev * F' + Q;

    % --- Update ---
    z      = [y1_meas(i); y2_meas(i)];
    H      = getH(x_pred);
    z_pred = h_robot(x_pred);
    y_innov = z - z_pred;
    % wrap angle innovation to [-pi, pi]
    y_innov(2) = atan2(sin(y_innov(2)), cos(y_innov(2)));

    S = H * P_pred * H' + R;
    K = P_pred * H' / S;

    x_upd = x_pred + K * y_innov;
    I3 = eye(n);
    P_upd = (I3 - K * H) * P_pred * (I3 - K * H)' + K * R * K';
    P_upd = (P_upd + P_upd') / 2;

    X_ekf(:, i)   = x_upd;
    P_ekf(:,:,i)  = P_upd;
    sig_ekf(:, i) = sqrt(max(diag(P_upd), 0));
end

%% 2. Unscented Kalman Filter
X_ukf   = zeros(n, time_steps);
P_ukf   = zeros(n, n, time_steps);
sig_ukf = zeros(n, time_steps);

X_ukf(:,1)   = [0; 0; 0];
P_ukf(:,:,1) = diag([0.1, 0.1, 0.01]);
sig_ukf(:,1) = sqrt(diag(P_ukf(:,:,1)));

% UKF with 2n sigma points (textbook eq. 14.29), equal weights 1/(2n)
for i = 2:time_steps
    x_prev = X_ukf(:, i-1);
    P_prev = P_ukf(:, :, i-1);
    u_prev = [ur(i-1); ul(i-1)];

    % --- Sigma points (2n, no center) ---
    L = chol((P_prev + P_prev') / 2 + 1e-12 * eye(n), 'lower');
    x_sig = zeros(n, 2*n);
    for j = 1:n
        x_sig(:, 2*j - 1) = x_prev + sqrt(n) * L(:, j);
        x_sig(:, 2*j    ) = x_prev - sqrt(n) * L(:, j);
    end

    % --- Propagate through process model ---
    s_sig = zeros(n, 2*n);
    for j = 1:(2*n)
        s_sig(:, j) = f_robot(x_sig(:, j), u_prev, r, l, dt);
    end

    x_pred = sum(s_sig, 2) / (2*n);
    P_pred = Q;
    for j = 1:(2*n)
        ds = s_sig(:, j) - x_pred;
        ds(3) = atan2(sin(ds(3)), cos(ds(3)));
        P_pred = P_pred + (ds * ds') / (2*n);
    end
    P_pred = (P_pred + P_pred') / 2;

    % --- Measurement sigma points from propagated predicted sigma points ---
    y_sig = zeros(m, 2*n);
    for j = 1:(2*n)
        y_sig(:, j) = h_robot(s_sig(:, j));
    end
    % Unwrap y2 angle values around predicted mean bearing to avoid branch cut
    ang_ref = atan2(x_pred(2), x_pred(1));
    for j = 1:(2*n)
        y_sig(2, j) = ang_ref + atan2(sin(y_sig(2, j) - ang_ref), ...
                                      cos(y_sig(2, j) - ang_ref));
    end

    y_mean = sum(y_sig, 2) / (2*n);

    Pyy = R;
    Pxy = zeros(n, m);
    for j = 1:(2*n)
        dy = y_sig(:, j) - y_mean;
        dx = s_sig(:, j) - x_pred;
        dx(3) = atan2(sin(dx(3)), cos(dx(3)));
        Pyy = Pyy + (dy * dy') / (2*n);
        Pxy = Pxy + (dx * dy') / (2*n);
    end

    z = [y1_meas(i); y2_meas(i)];
    % Wrap measured bearing close to the predicted bearing
    z(2) = y_mean(2) + atan2(sin(z(2) - y_mean(2)), cos(z(2) - y_mean(2)));
    y_innov = z - y_mean;

    K = Pxy / Pyy;
    x_upd = x_pred + K * y_innov;
    P_upd = P_pred - K * Pyy * K';
    P_upd = (P_upd + P_upd') / 2;

    X_ukf(:, i)   = x_upd;
    P_ukf(:,:,i)  = P_upd;
    sig_ukf(:, i) = sqrt(max(diag(P_upd), 0));
end

%% 3. Plot the filters results
state_names = {'x [m]', 'y [m]', '\phi [rad]'};
truth = [x_true, y_true, phi_true]';

fig_states = figure('Name','True vs Estimated states','Color','w','Position',[100 100 900 700]);
for k = 1:3
    subplot(3, 1, k); hold on; grid on; box on;
    plot(t, truth(k,:),    '-',  'Color', c_black,    'LineWidth', 1.8);
    plot(t, X_ekf(k,:),    '--', 'Color', c_garnet,   'LineWidth', 1.4);
    plot(t, X_ukf(k,:),    ':',  'Color', c_atlantic, 'LineWidth', 1.6);
    ylabel(state_names{k});
    if k == 1
        legend('True', 'EKF', 'UKF', 'Location', 'best');
        title('True vs Estimated States');
    end
    if k == 3
        xlabel('time [s]');
    end
end

%% 4. Plot the filters error levels and estimated error bounds
err_ekf = X_ekf - truth;
err_ukf = X_ukf - truth;
% wrap phi error
err_ekf(3,:) = atan2(sin(err_ekf(3,:)), cos(err_ekf(3,:)));
err_ukf(3,:) = atan2(sin(err_ukf(3,:)), cos(err_ukf(3,:)));

fig_ekf_err = figure('Name','EKF error with 3\sigma bounds','Color','w','Position',[100 100 900 700]);
for k = 1:3
    subplot(3, 1, k); hold on; grid on; box on;
    plot(t,  err_ekf(k,:),       '-',  'Color', c_garnet, 'LineWidth', 1.4);
    plot(t,  3*sig_ekf(k,:),     '--', 'Color', c_grey,   'LineWidth', 1.0);
    plot(t, -3*sig_ekf(k,:),     '--', 'Color', c_grey,   'LineWidth', 1.0);
    ylabel(['err ' state_names{k}]);
    if k == 1
        legend('EKF error', '\pm3\sigma', 'Location', 'best');
        title('EKF estimation error and 3\sigma bounds');
    end
    if k == 3, xlabel('time [s]'); end
end

fig_ukf_err = figure('Name','UKF error with 3\sigma bounds','Color','w','Position',[100 100 900 700]);
for k = 1:3
    subplot(3, 1, k); hold on; grid on; box on;
    plot(t,  err_ukf(k,:),       '-',  'Color', c_atlantic, 'LineWidth', 1.4);
    plot(t,  3*sig_ukf(k,:),     '--', 'Color', c_grey,     'LineWidth', 1.0);
    plot(t, -3*sig_ukf(k,:),     '--', 'Color', c_grey,     'LineWidth', 1.0);
    ylabel(['err ' state_names{k}]);
    if k == 1
        legend('UKF error', '\pm3\sigma', 'Location', 'best');
        title('UKF estimation error and 3\sigma bounds');
    end
    if k == 3, xlabel('time [s]'); end
end

% Save figures as PNGs for review
exportgraphics(fig_states,  'fig_states.png',  'Resolution', 150);
exportgraphics(fig_ekf_err, 'fig_ekf_err.png', 'Resolution', 150);
exportgraphics(fig_ukf_err, 'fig_ukf_err.png', 'Resolution', 150);

%% Any functions need to go under here
function x_next = f_robot(x, u, r, l, dt)
    % Differential drive discrete-time motion model
    % x = [x; y; phi], u = [ur; ul]
    ur_k = u(1); ul_k = u(2);
    phi  = x(3);
    x_next = zeros(3,1);
    x_next(1) = x(1) + 0.5 * dt * r * (ur_k + ul_k) * cos(phi);
    x_next(2) = x(2) + 0.5 * dt * r * (ur_k + ul_k) * sin(phi);
    x_next(3) = phi  + dt * (r / l) * (ur_k - ul_k);
end

function y = h_robot(x)
    % Polar measurement model
    y = zeros(2,1);
    y(1) = sqrt(x(1)^2 + x(2)^2);
    y(2) = atan2(x(2), x(1));
end

function F = getF(x, u, r, dt)
    % Jacobian of f wrt state
    ur_k = u(1); ul_k = u(2);
    phi  = x(3);
    F = eye(3);
    F(1, 3) = -0.5 * dt * r * (ur_k + ul_k) * sin(phi);
    F(2, 3) =  0.5 * dt * r * (ur_k + ul_k) * cos(phi);
end

function H = getH(x)
    % Jacobian of h wrt state
    xp = x(1); yp = x(2);
    rr = sqrt(xp^2 + yp^2);
    if rr < 1e-9
        rr = 1e-9;
    end
    H = zeros(2, 3);
    H(1, 1) = xp / rr;
    H(1, 2) = yp / rr;
    H(1, 3) = 0;
    H(2, 1) = -yp / (rr^2);
    H(2, 2) =  xp / (rr^2);
    H(2, 3) = 0;
end
