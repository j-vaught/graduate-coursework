% B.4. Air vibration in a tube closed at both ends.
clear; clc; close all;

% 1. Input data
L = 0.85;           % tube length, m
c = 340;            % sound speed in air, m/s
rho = 1.2;          % air density, kg/m^3
N = 5;              % number of modes analyzed
j = (1:N)';

fprintf('=== Problem B.4: Air Vibration in Closed-Closed Tube ===\n');
fprintf('Input Data:\n');
fprintf('  Tube length L          = %.4f m\n', L);
fprintf('  Sound speed c          = %.1f m/s\n', c);
fprintf('  Air density rho        = %.2f kg/m^3\n', rho);
fprintf('  Bulk modulus K = rho*c^2 = %.1f kPa\n', (rho * c^2)/1e3);
fprintf('  Acoustic impedance Z   = %.1f Pa*s/m\n', rho * c);
fprintf('  Number of modes N      = %d\n\n', N);

% 2. Modal vibration characteristics
z = j * pi;                 % eigenvalues, rad
gamma = z / L;              % wavenumbers, rad/m
omega = gamma * c;          % natural angular frequencies, rad/s
f = omega / (2 * pi);       % natural frequencies, Hz
lambda = 2 * L ./ j;        % wavelengths, m

modal_table = table(j, z, gamma, omega, f, lambda, ...
    'VariableNames', {'Mode_j', 'Eigenvalue_z_j', 'Wavenumber_rad_m', ...
                      'Frequency_rad_s', 'Frequency_Hz', 'Wavelength_m'});
disp('Modal Vibration Characteristics:');
disp(modal_table);

% 3. Calculate and plot displacement modeshapes
Nx = 501;
x = linspace(0, L, Nx);
U = zeros(N, Nx);
P_norm = zeros(N, Nx);

for m = 1:N
    U(m, :) = sin(j(m) * pi * x / L);
    P_norm(m, :) = -cos(j(m) * pi * x / L);
end

% Palette colors matching course standard
C = [  0  95 115;   % deep teal
     213  94   0;   % orange
      37  40  42;   % graphite
       0 158 115;   % green
      80  86  91]/255; % slate

lineStyles = {'-', '--', ':', '-.', '--'};

figure('Name', 'Displacement Modeshapes', 'Color', 'w');
hold on;
for m = 1:N
    plot(x, U(m, :), 'Color', C(m, :), 'LineStyle', lineStyles{m}, ...
         'LineWidth', 1.4, 'DisplayName', sprintf('Mode %d (%d Hz)', m, round(f(m))));
end
yline(0, ':k', 'Alpha', 0.5);
xlabel('Position along tube, x (m)');
ylabel('Displacement modeshape, U_j(x)');
title(sprintf('Air Displacement Modeshapes (L = %.2f m, Closed-Closed)', L));
xlim([0, L]); ylim([-1.1, 1.1]);
xticks(linspace(0, L, 6));
legend('Location', 'northeast');
grid on; box on;

% 5. Graduate work: Calculate and plot normalized pressure modeshapes
figure('Name', 'Normalized Pressure Modeshapes', 'Color', 'w');
hold on;
for m = 1:N
    plot(x, P_norm(m, :), 'Color', C(m, :), 'LineStyle', lineStyles{m}, ...
         'LineWidth', 1.4, 'DisplayName', sprintf('Mode %d (%d Hz)', m, round(f(m))));
end
yline(0, ':k', 'Alpha', 0.5);
xlabel('Position along tube, x (m)');
ylabel('Normalized pressure modeshape, P_j(x)');
title(sprintf('Normalized Acoustic Pressure Modeshapes (L = %.2f m, Closed-Closed)', L));
xlim([0, L]); ylim([-1.1, 1.1]);
xticks(linspace(0, L, 6));
legend('Location', 'northeast');
grid on; box on;
