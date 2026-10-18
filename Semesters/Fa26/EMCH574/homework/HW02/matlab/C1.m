% C.1. Air vibration in a closed-open tube.
clear; clc; close all;

N = 5;
x = linspace(0, 1, 401);
n = 2 * (1:N) - 1;

U = sin((n' * pi / 2) * x);
P = -cos((n' * pi / 2) * x);

C = [0 95 115; 213 94 0; 37 40 42; 0 158 115; 80 86 91] / 255;
ls = {'-', '--', ':', '-.', '--'};

fprintf('Closed-open tube. z_j = (2j-1)pi/2.\n');
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
