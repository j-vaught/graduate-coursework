function plot_f_z_Damped(U, f, z, plotTitle, plotOptions)
% plot_f_z_Damped: Plots damped flutter diagram (frequency and damping vs airspeed)
%
% This function creates a damped flutter diagram showing frequency (f) and damping ratio (z)
% versus airspeed (U) with customizable plot options for comparing damped and undamped cases.
%
% Inputs:
%   U           - airspeed range (m/s)
%   f           - frequencies (Hz)
%   z           - damping ratios
%   plotTitle   - title for the plot
%   plotOptions - plotting options (e.g., '.r', '.b')

NU = length(U); 

%% PLOT FREQUENCY VS AIRSPEED
subplot(2, 1, 1); 
plot(U, f, plotOptions); 
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
plot(U, z * 1e2, plotOptions);  % Convert damping ratio to percentage
xlim([U(1), U(NU)]); 
xlabel('U, m/s'); 

% Set y-axis limits
ymax = 15; 
ylim([-ymax, ymax]); 
ylabel('\zeta, %'); 

grid on;
hold on;

end % function plot_f_z_Damped ends here