% C.2. Air vibration in an open-open tube.
clear; clc; close all;

N = 5;
x = linspace(0, 1, 401);
n = 1:N;

U = cos((n' * pi) * x);
P = sin((n' * pi) * x);

C = [0 95 115; 213 94 0; 37 40 42; 0 158 115; 80 86 91] / 255;
ls = {'-', '--', ':', '-.', '--'};

fprintf('Open-open tube. z_j = j*pi, j >= 1.\n');
fprintf('f_j/f_1 = ');
fprintf('%g ', n);
fprintf('\n');

figure('Color', 'w');
hold on;
for j = 1:N
    plot(x, U(j, :), 'Color', C(j, :), 'LineStyle', ls{j}, ...
        'LineWidth', 1.4, 'DisplayName', sprintf('Mode %d', j));
end
xlabel('Normalized position, x/L');
ylabel('Normalized displacement, U_j');
xlim([0 1]); ylim([-1.1 1.1]);
legend('Location', 'northeast'); grid on; box on;

figure('Color', 'w');
hold on;
for j = 1:N
    plot(x, P(j, :), 'Color', C(j, :), 'LineStyle', ls{j}, ...
        'LineWidth', 1.4, 'DisplayName', sprintf('Mode %d', j));
end
xlabel('Normalized position, x/L');
ylabel('Normalized pressure, P_j');
xlim([0 1]); ylim([-1.1 1.1]);
legend('Location', 'northeast'); grid on; box on;
