function plot_f_z(U, f, z, plotTitle)
% plot_f_z: Plots flutter diagram (frequency and damping vs airspeed)
%
% This function creates a flutter diagram showing frequency (f) and damping ratio (z)
% versus airspeed (U) to analyze flutter characteristics.
%
% Inputs:
%   U         - airspeed range (m/s)
%   f         - frequencies (Hz)
%   z         - damping ratios
%   plotTitle - title for the plot

NU = length(U);

%% PLOT FREQUENCY VS AIRSPEED
subplot(2, 1, 1);
plot(U, f, '.r');
title(plotTitle, 'FontSize', 11, 'FontWeight', 'normal');
xlabel('U, m/s');
ylabel('f, Hz');

% Set y-axis limits based on maximum frequency
fmax = ceil(max(max(f)));
ylim([0, fmax]);

% Set x-axis limits
xlim([U(1), U(NU)]);

hold on;

%% PLOT DAMPING RATIO VS AIRSPEED
subplot(2, 1, 2);
plot(U, z * 1e2, '.g');  % Convert damping ratio to percentage
xlim([U(1), U(NU)]);
xlabel('U, m/s');
ylabel('\zeta, %');

% Set y-axis limits
ymax = 15;
ylim([-ymax, ymax]);

grid on;
hold on;

end % function plot_f_z ends here

