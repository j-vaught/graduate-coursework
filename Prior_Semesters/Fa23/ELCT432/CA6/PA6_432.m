% Clean up the workspace, close all figures, and clear the command window
clear; close all; clc;

% Define the simulation parameters
N = 100000;                  % Number of samples for the message signal
k_vals = -40:40;             % Range of k values for autocorrelation function

% Generate a white noise sequence with a normally distributed random numbers
x_n = randn(1, N);           % White noise with a flat Power Spectral Density (PSD)

% Define the autocorrelation function R[k] as the squared sinc function
R_k = sinc(1/4 * k_vals).^2; % Theoretical autocorrelation function R[k]

% Calculate the Power Spectral Density (PSD) by taking the Fourier Transform of R[k]
S_xx = fft(R_k, N);          % Desired PSD is the Fourier Transform of R[k]

% Obtain the filter's frequency response by taking the square root of the PSD
H_f = sqrt(S_xx);            % Frequency response of the filter H(f)

% Apply the filter to the white noise in the frequency domain
X_n = fft(x_n);              % Compute the Fast Fourier Transform (FFT) of the white noise
Y_n = H_f .* X_n;            % Element-wise multiplication to apply the filter

% Convert the filtered signal back to the time domain
y_n = ifft(Y_n, 'symmetric'); % Inverse FFT to obtain the time domain signal

% Empirically verify the autocorrelation of the filtered signal
R_k_empirical_full = xcorr(y_n, 'unbiased');  % Compute the autocorrelation
midpoint = floor(length(R_k_empirical_full) / 2) + 1; 
R_k_empirical = R_k_empirical_full(midpoint + k_vals);

% Calculate the mean square value which represents power of the message signal
power_msg_signal = mean(y_n.^2);

% Display the calculated power of the message signal
disp(['Power of the message signal: ', num2str(power_msg_signal)]);

% Estimate and plot the PSD of the filtered signal using Welch's method
[psd_y, f_psd] = pwelch(y_n, hamming(1024), 512, 1024, 'centered', 'power');

% Plotting the results - Autocorrelation and PSD
% Plotting the Autocorrelation Function
figure;  % Create a new figure
stem(k_vals, midpoint*R_k_empirical / N, 'b', 'DisplayName', 'Empirical R''[k]');
hold on;  % Retain the current plot when adding new plots
plot(k_vals, R_k, 'r:x', 'DisplayName', 'Desired R[k]');
hold off;  % Release the current plot
title('Autocorrelation Function');
xlabel('Lag k');
ylabel('Autocorrelation');
legend show;  % Display the legend
print('Autocorrelation_Function','-dpng');  % Save the plot

% Plotting the Power Spectral Density (PSD)
figure;  % Create a new figure for PSD
plot(f_psd, 100*psd_y, 'b', 'DisplayName', 'PSD of y[n]');
title('Power Spectral Density');
xlabel('Frequency (Hz)');
ylabel('PSD');
legend show;  % Display the legend
print('Power_Spectral_Density','-dpng');  % Save the plot


% Plotting the log Power Spectral Density (PSD)
figure;  % Create a new figure for PSD
plot(f_psd, 10*log10(1000*psd_y), 'b', 'DisplayName', 'PSD of y[n]');
title('Power Spectral Density');
xlabel('Frequency (Hz)');
ylabel('PSD (dB)');
legend show;  % Display the legend
print('Power_Spectral_Density_dB','-dpng');  % Save the plot