%% Clear and close everything
clear; close all; clc;

%% 0. Start by entering your last name
lastName = "Vaught";
display("EMCH-792 HW3, " + lastName)

% Reproducible random draws for grading and report generation
rng(792);

% Resolve report figure output directory (expects script in ws/)
scriptPath = mfilename('fullpath');
if isempty(scriptPath)
    scriptDir = pwd;
else
    scriptDir = fileparts(scriptPath);
end
hwDir = fileparts(scriptDir);
figDir = fullfile(hwDir, "figures");
if ~exist(figDir, "dir")
    mkdir(figDir);
end

%% B1) Exercise 2.15, page 77
% Generate 50 independent random variables, find mean, std and plot
% histogram
N_values = [50, 500, 5000];
theory_mean = 0.5;
theory_std = 1 / sqrt(12);
sample_mean = zeros(size(N_values));
sample_std = zeros(size(N_values));
u_samples = cell(size(N_values));

usc_garnet = [115, 0, 10] / 255;
usc_atlantic = [70, 106, 159] / 255;
usc_horseshoe = [101, 120, 11] / 255;
usc_black = [0, 0, 0] / 255;
face_colors = [usc_garnet; usc_atlantic; usc_horseshoe];
bin_edges = linspace(0, 1, 11); % 10 bins

figure('Color', 'w', 'Position', [120 120 1100 380], 'ToolBar', 'none');
tiledlayout(1, 3, "Padding", "compact", "TileSpacing", "compact");

for i = 1:numel(N_values)
    N = N_values(i);
    u = rand(N, 1);
    u_samples{i} = u;
    sample_mean(i) = mean(u);
    sample_std(i) = std(u);

    nexttile;
    h = histogram(u, bin_edges, 'FaceColor', face_colors(i, :), ...
        'EdgeColor', usc_black, 'LineWidth', 1.0);
    h.Normalization = 'count';
    ax = gca;
    ax.Toolbar.Visible = 'off';
    title(sprintf('N = %d', N));
    xlabel('Value');
    ylabel('Count');
    grid on;
end

sgtitle('Exercise 2.15: Uniform Random Variables (10-bin Histograms)', ...
    'FontWeight', 'bold');
exportgraphics(gcf, fullfile(figDir, 'HW3_B1_histograms.png'), ...
    'Resolution', 300);

% Also generate individual histograms for each required sample size
for i = 1:numel(N_values)
    N = N_values(i);
    u = u_samples{i};

    figure('Color', 'w', 'Position', [180 180 640 420], 'ToolBar', 'none');
    h_single = histogram(u, bin_edges, 'FaceColor', face_colors(i, :), ...
        'EdgeColor', usc_black, 'LineWidth', 1.1);
    h_single.Normalization = 'count';
    ax_single = gca;
    ax_single.Toolbar.Visible = 'off';
    grid on;
    xlabel('Value');
    ylabel('Count');
    title(sprintf('Exercise 2.15 Histogram (N = %d)', N), 'FontWeight', 'bold');
    exportgraphics(gcf, fullfile(figDir, sprintf('HW3_B1_hist_%d.png', N)), ...
        'Resolution', 300);
end

fprintf('\nB1 Results (Uniform U(0,1))\n');
fprintf('Theoretical mean = %.6f, theoretical std = %.6f\n', ...
    theory_mean, theory_std);
for i = 1:numel(N_values)
    fprintf('N=%4d -> sample mean = %.6f, sample std = %.6f\n', ...
        N_values(i), sample_mean(i), sample_std(i));
end

%% B2) Noise Covariance matrix calculation
% Define A, B_u, B_w, S_w, dt1 and dt2
A = [-1 1; -2 -2];
B_u = [0; -1];
B_w = [1; 2];
S_w = 0.11;
dt_values = [0.5, 0.01];
n = size(A, 1);
Q_c = B_w * S_w * B_w.';

fprintf('\nB2 Constants\n');
fprintf('A = \n'); disp(A);
fprintf('B_u = \n'); disp(B_u);
fprintf('B_w = \n'); disp(B_w);
fprintf('S_w = %.4f\n', S_w);
fprintf('Q_c = B_w*S_w*B_w'' = \n'); disp(Q_c);

% a. Use the Z block matrix to calculate the exact and approximate Sigma_w
Sigma_w_exact_cells = cell(size(dt_values));
Sigma_w_approx_cells = cell(size(dt_values));
Ad_cells = cell(size(dt_values));
Ad_c2d_cells = cell(size(dt_values));
Sigma_x_ss_disc_cells = cell(size(dt_values));

for i = 1:numel(dt_values)
    dt = dt_values(i);

    % Van Loan / Z block matrix approach
    Z = [-A, Q_c; zeros(n), A.'] * dt;
    Z_exp = expm(Z);
    Ad = inv(Z_exp(1:n, 1:n));
    Sigma_w_exact = Ad * Z_exp(1:n, n+1:end);

    % First-order approximation
    Sigma_w_approx = Q_c * dt;

    Ad_cells{i} = Ad;
    Sigma_w_exact_cells{i} = Sigma_w_exact;
    Sigma_w_approx_cells{i} = Sigma_w_approx;

    fprintf('\nB2(a) for dt = %.3f\n', dt);
    fprintf('Sigma_w_exact = \n'); disp(Sigma_w_exact);
    fprintf('Sigma_w_approx = \n'); disp(Sigma_w_approx);
    fprintf('norm(Sigma_w_exact - Sigma_w_approx, ''fro'') = %.10f\n', ...
        norm(Sigma_w_exact - Sigma_w_approx, 'fro'));

    % b. Verify Ad with c2d()
    C = eye(n);
    D = zeros(n, 1);
    sys_c = ss(A, B_u, C, D);
    sys_d = c2d(sys_c, dt);
    Ad_c2d = sys_d.A;
    Ad_c2d_cells{i} = Ad_c2d;

    fprintf('B2(b) for dt = %.3f\n', dt);
    fprintf('Ad from Z = \n'); disp(Ad);
    fprintf('Ad from c2d = \n'); disp(Ad_c2d);
    fprintf('norm(Ad_Z - Ad_c2d, ''fro'') = %.10e\n', ...
        norm(Ad - Ad_c2d, 'fro'));

    % c. Steady-state covariance in continuous and discrete domains
    Sigma_x_ss_cont = lyap(A, Q_c);
    Sigma_x_ss_disc = dlyap(Ad, Sigma_w_exact);
    Sigma_x_ss_disc_cells{i} = Sigma_x_ss_disc;

    fprintf('B2(c) for dt = %.3f\n', dt);
    fprintf('Sigma_x_ss_cont = \n'); disp(Sigma_x_ss_cont);
    fprintf('Sigma_x_ss_disc = \n'); disp(Sigma_x_ss_disc);
    fprintf('norm(Sigma_x_ss_disc - Sigma_x_ss_cont, ''fro'') = %.10e\n', ...
        norm(Sigma_x_ss_disc - Sigma_x_ss_cont, 'fro'));
end

display("Observations:");
display("1) For dt = 0.5, Sigma_w approximate differs noticeably from exact.");
display("2) For dt = 0.01, Sigma_w approximate is very close to exact.");
display("3) Ad from Z matrix matches c2d() up to machine precision.");
display("4) Continuous and discrete steady-state covariances agree when exact Sigma_w is used.");
