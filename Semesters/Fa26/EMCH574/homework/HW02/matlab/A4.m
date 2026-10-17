% Standing waves from two equal waves traveling in opposite directions.
clear; clc;

c = 340;                 % wave speed (m/s)
f = 2.9e3;               % frequency (Hz)
w = 2*pi*f;              % angular frequency (rad/s)
g = w/c;                 % wavenumber (rad/m)
lam = c/f;               % wavelength (m)
dx = pi/g;               % distance between adjacent nodes (m)

fprintf('omega = %.6g rad/s\n', w);
fprintf('gamma = %.6g rad/m\n', g);
fprintf('lambda = %.6g m\n', lam);
fprintf('node spacing = %.6g m\n', dx);

% Show one spatial wavelength at three instants in the oscillation.
x = linspace(0, lam, 500);
t = [0, 1/8, 1/2]/f;
u = cos(g*x(:))*cos(w*t);
C = [0 95 115; 213 94 0; 37 40 42]/255; % HW01 colors

figure('Color','w');
plot(x, u(:,1), 'Color', C(1,:), 'LineWidth', 1.4);
hold on;
plot(x, u(:,2), 'Color', C(2,:), 'LineWidth', 1.4);
plot(x, u(:,3), 'Color', C(3,:), 'LineWidth', 1.4);
grid on;
xlabel('Position, x (m)');
ylabel('Displacement, u (normalized)');
xlim([0 lam]);
legend('t = 0', 't = T/8', 't = T/2', 'Location', 'best');
