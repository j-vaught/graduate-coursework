%% Clear and close everything
clear; close all; clc;

%% 0. Start by entering your last name
lastName = "Vaught";
display("EMCH-792 HW3, " + lastName)

rng(792);

%% B1) Exercise 2.15, page 77
% Generate 50 independent random variables, find mean, std and plot
% histogram
N50 = 50;
u50 = rand(N50, 1);
mean50 = mean(u50);
std50 = std(u50);

% Generate 500 independent random variables, find mean, std and plot
% histogram
N500 = 500;
u500 = rand(N500, 1);
mean500 = mean(u500);
std500 = std(u500);

% Generate 5000 independent random variables, find mean, std and plot
% histogram
N5000 = 5000;
u5000 = rand(N5000, 1);
mean5000 = mean(u5000);
std5000 = std(u5000);

theoryMean = 0.5;
theoryStd = 1 / sqrt(12);

uscGarnet = [115, 0, 10] / 255;
uscAtlantic = [70, 106, 159] / 255;
uscHorseshoe = [101, 120, 11] / 255;
uscBlack = [0, 0, 0] / 255;
binEdges = linspace(0, 1, 11); % 10 bins

figure('Color', 'w', 'Position', [120 120 1100 380], 'ToolBar', 'none');
tiledlayout(1, 3, "Padding", "compact", "TileSpacing", "compact");

nexttile;
histogram(u50, binEdges, 'FaceColor', uscGarnet, 'EdgeColor', uscBlack, 'LineWidth', 1.0);
title('N = 50');
xlabel('Value'); ylabel('Count'); grid on;

nexttile;
histogram(u500, binEdges, 'FaceColor', uscAtlantic, 'EdgeColor', uscBlack, 'LineWidth', 1.0);
title('N = 500');
xlabel('Value'); ylabel('Count'); grid on;

nexttile;
histogram(u5000, binEdges, 'FaceColor', uscHorseshoe, 'EdgeColor', uscBlack, 'LineWidth', 1.0);
title('N = 5000');
xlabel('Value'); ylabel('Count'); grid on;

sgtitle('Exercise 2.15: Uniform Random Variables (10-bin Histograms)', 'FontWeight', 'bold');

fprintf('\nB1 Results (Uniform U(0,1))\n');
fprintf('Theoretical mean = %.6f, theoretical std = %.6f\n', theoryMean, theoryStd);
fprintf('N=%4d -> sample mean = %.6f, sample std = %.6f\n', N50, mean50, std50);
fprintf('N=%4d -> sample mean = %.6f, sample std = %.6f\n', N500, mean500, std500);
fprintf('N=%4d -> sample mean = %.6f, sample std = %.6f\n', N5000, mean5000, std5000);

%% B2) Noise Covariance matrix calculation
% Define A, B_u, B_w, S_w, dt1 and dt2
A = [3 1; 0 -1];
B_u = [2; -2];
B_w = [-1; 2];
S_w = 0.11;
dt1 = 0.5;
dt2 = 0.01;
dtValues = [dt1, dt2];

n = size(A, 1);
Q_c = B_w * S_w * B_w.';

fprintf('\nB2 Constants\n');
fprintf('A = \n'); disp(A);
fprintf('B_u = \n'); disp(B_u);
fprintf('B_w = \n'); disp(B_w);
fprintf('S_w = %.4f\n', S_w);
fprintf('Q_c = B_w*S_w*B_w'' = \n'); disp(Q_c);

% a. Use the Z block matrix to calculate the exact and approximate Sigma_w
Sigma_w_exact = cell(1, numel(dtValues));
Sigma_w_approx = cell(1, numel(dtValues));
Ad_Z = cell(1, numel(dtValues));

for k = 1:numel(dtValues)
    dt = dtValues(k);

    Z = [-A, Q_c; zeros(n), A.'] * dt;
    Zexp = expm(Z);
    Ad_Z{k} = inv(Zexp(1:n, 1:n));
    Sigma_w_exact{k} = Ad_Z{k} * Zexp(1:n, n+1:end);
    Sigma_w_approx{k} = Q_c * dt;

    fprintf('\nB2(a) for dt = %.3f\n', dt);
    fprintf('Sigma_w_exact = \n'); disp(Sigma_w_exact{k});
    fprintf('Sigma_w_approx = \n'); disp(Sigma_w_approx{k});
    fprintf('norm(Sigma_w_exact - Sigma_w_approx, ''fro'') = %.10f\n', ...
        norm(Sigma_w_exact{k} - Sigma_w_approx{k}, 'fro'));
end

display("Write what you noticed here")
display("- For dt = 0.5, the first-order approximation differs noticeably from exact Sigma_w.")
display("- For dt = 0.01, the approximation is very close to exact Sigma_w.")

% b. Using the Z block matrix, find Ad in each case. Verify your results
%    with the c2d() function
Ad_c2d = cell(1, numel(dtValues));
C = eye(n);
D = zeros(n, 1);
sys_c = ss(A, B_u, C, D);

for k = 1:numel(dtValues)
    dt = dtValues(k);
    sys_d = c2d(sys_c, dt);
    Ad_c2d{k} = sys_d.A;

    fprintf('\nB2(b) for dt = %.3f\n', dt);
    fprintf('Ad from Z = \n'); disp(Ad_Z{k});
    fprintf('Ad from c2d = \n'); disp(Ad_c2d{k});
    fprintf('norm(Ad_Z - Ad_c2d, ''fro'') = %.10e\n', ...
        norm(Ad_Z{k} - Ad_c2d{k}, 'fro'));
end

% c. Compare predictions of steady-space performance: Using the dlyap() and
%    lyap(), find Sigma_x_ss in both continuous and discrete systems and
%    compare them
Sigma_x_ss_cont = lyap(A, Q_c);
Sigma_x_ss_disc = cell(1, numel(dtValues));

fprintf('\nB2(c)\n');
fprintf('Sigma_x_ss_cont = \n'); disp(Sigma_x_ss_cont);

for k = 1:numel(dtValues)
    dt = dtValues(k);
    Sigma_x_ss_disc{k} = dlyap(Ad_Z{k}, Sigma_w_exact{k});

    fprintf('dt = %.3f\n', dt);
    fprintf('Sigma_x_ss_disc = \n'); disp(Sigma_x_ss_disc{k});
    fprintf('norm(Sigma_x_ss_disc - Sigma_x_ss_cont, ''fro'') = %.10e\n', ...
        norm(Sigma_x_ss_disc{k} - Sigma_x_ss_cont, 'fro'));
end

display("Write what you noticed here")
display("- Ad from Z matches c2d() up to machine precision in both dt cases.")
display("- Continuous and discrete Lyapunov solutions match numerically when exact Sigma_w is used.")
display("- A has one unstable mode, so this is an algebraic Lyapunov comparison, not a physical stationary covariance.")
