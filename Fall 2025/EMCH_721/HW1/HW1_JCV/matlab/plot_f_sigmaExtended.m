function plot_f_sigmaExtended(U, f, sigma, plotTitle)
% plot_f_sigmaExtended: Plots extended flutter diagram (f and sigma vs U)
%
% This function creates an extended flutter diagram showing frequency (f) and
% real part of eigenvalues (sigma) versus airspeed (U) to identify divergence speed UD.
%
% Inputs:
%   U         - airspeed range (m/s)
%   f         - frequencies (Hz)
%   sigma     - real parts of eigenvalues
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

%% PLOT SIGMA VS AIRSPEED
subplot(2, 1, 2);
plot(U, sigma, '.g');
xlim([U(1), U(NU)]);
xlabel('U, m/s');
ylabel('\sigma = real(s)');

% Set y-axis limits
ymax = 15;
ylim([-ymax, ymax]);

grid on;
hold on;

end % Function plot_f_sigmaExtended ends here
