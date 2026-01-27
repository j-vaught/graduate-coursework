clc;
clear;
close all;

%% Definitions
% Define a binary array
%binary_array = [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0,
%1, 0, 1, 0]; %My test Data

binary_array = randi([0, 1], 1, 100);
summed_signal = generate_bpsk_signal_optimized2(binary_array);

%% Figure position information
% Get the current working directory
currentDir = pwd;

% Define the path for the 'figures' directory within the current working directory
figures_dir = fullfile(currentDir, 'figures');

% Check if the 'figures' directory exists, and if not, create it
if ~exist(figures_dir, 'dir')
    mkdir(figures_dir);  % Create the directory
end

% Define figure size corresponding to 1920x1080 pixels
figure_width = 1920;
figure_height = 1080;
figure_position = [0, 0, figure_width, figure_height]; % [left, bottom, width, height]

%% Generate PSD of 10000 samples at 2MHz
% Generate BPSK with 10000 samples at 2MHz
PSD_signal = 20 * generate_bpsk_signal_optimized2(randi([0, 1], 1, 10000));%factor of 20 
% is for the power factor when doing dB scale later

% Generate PSD of 10000 samples at 2MHz and save the figure
h = figure('Visible', 'off', 'Position', figure_position);
pwelch(PSD_signal, [], [], [], 2e6, 'centered', 'power');
print(h, fullfile(figures_dir, 'PSD_signal.png'), '-dpng', '-r0'); % Save figure

% The shape is not exactly rectangular because the sinc function used for 
% pulse shaping in time domain corresponds to a rectangular function in the 
% frequency domain only when it is infinitely long. In practical systems, 
% the sinc pulse is time-limited, which causes the frequency response to be 
% a sinc function, leading to the typical "sinc squared" shape of the PSD.

% Calculate the 3dB bandwidth using pwelch
[psd_output, freq] = pwelch(PSD_signal, [], [], [], 2e6, 'centered', 'power');

% Calculate the 3dB bandwidth
power_half_max = max(psd_output)/2; % Find the half-maximum of the power
% Find the points where the PSD crosses the half-maximum value
bandwidth_idx = find(psd_output >= power_half_max);
% Calculate the 3dB bandwidth
bw_3dB = freq(bandwidth_idx(end)) - freq(bandwidth_idx(1));

% Display the 3dB bandwidth
disp(['3dB Bandwidth: ', num2str(bw_3dB), ' Hz']);


%% Add noise to the signal to achieve Eb/N0 = 2 (linear scale)
EbN0 = 10^(2/10); % Logarithmic scale

% Calculate the signal power
Eb = mean(abs(summed_signal).^2);

% Calculate the noise power spectral density N0
N0 = Eb / EbN0;

% Generate the AWGN with the calculated variance
noise = sqrt(N0 / 2) * randn(size(summed_signal));

% Add the noise to the signal
received_signal = summed_signal + noise;

%% Decode the Bits and Determine Error Rate
% Assuming decode_bpsk_signal now returns [decoded_array, filtered_signal]
[decoded_array, filtered_signal] = decode_bpsk_signal(received_signal);
[~, filtered_non_noise] = decode_bpsk_signal(summed_signal);

% Check if each bit matches
bit_matches = binary_array == decoded_array;

% Display overall success rate
success_rate = mean(bit_matches) * 100;
disp(['Overall Success Rate: ', num2str(success_rate), '%']);

%% Convert binary array to BPSK values for plotting and save the figure 
% (-1 for binary 0, and +1 for binary 1)
binary_bpsk_values = 2 * binary_array - 1;
h = figure('Visible', 'off', 'Position', figure_position);
plot(binary_bpsk_values);
title('Original Binary Data as BPSK Values');
xlabel('Bit Index');
ylabel('BPSK Value');
ylim([-1.5, 1.5]);
grid on;
print(h, fullfile(figures_dir, 'Binary_BPSK_Values.png'), '-dpng', '-r0');

%% Plot the summed BPSK signal and save the figure
h = figure('Visible', 'off', 'Position', figure_position);
plot(summed_signal);
title('Summed BPSK Signal');
xlabel('Samples [n]');
ylabel('Amplitude');
grid on;
print(h, fullfile(figures_dir, 'Summed_BPSK_Signal.png'), '-dpng', '-r0');

%% Plot the Noise Added to the System and save the figure
h = figure('Visible', 'off', 'Position', figure_position);
plot(noise);
title('Noise Added to the System');
xlabel('Samples [n]');
ylabel('Amplitude');
grid on;
print(h, fullfile(figures_dir, 'Noise_Added.png'), '-dpng', '-r0');

%% Plot the Signal with Noise and save the figure
h = figure('Visible', 'off', 'Position', figure_position);
plot(received_signal);
title('BPSK Signal with Noise');
xlabel('Samples [n]');
ylabel('Amplitude');
grid on;
print(h, fullfile(figures_dir, 'BPSK_Signal_with_Noise.png'), '-dpng', '-r0');

%% Plot the Filtered Signal and save the figure
h = figure('Visible', 'off', 'Position', figure_position);
plot(filtered_non_noise);
title('Filtered Received Signal');
xlabel('Samples [n]');
ylabel('Amplitude');
grid on;
print(h, fullfile(figures_dir, 'Filtered_Received_Signal.png'), '-dpng', '-r0');

%% Plot the Filtered Received Signal with Noise and save the figure
% This assumes that filtered_signal already includes the noise
h = figure('Visible', 'off', 'Position', figure_position);
plot(filtered_signal);
title('Filtered Received Signal with Noise');
xlabel('Samples [n]');
ylabel('Amplitude');
grid on;
print(h, fullfile(figures_dir, 'Filtered_Received_Signal_with_Noise.png'), '-dpng', '-r0');



%% Plot Comparison of Original, Filtered, and Filtered with Noise Signals
h = figure('Visible', 'on', 'Position', figure_position);
hold on; % Hold on to plot multiple datasets
plot(repelem(binary_bpsk_values, 8), 'DisplayName', 'Original Binary Data');
plot(filtered_non_noise/10, 'DisplayName', 'Filtered Received Data');
plot(filtered_signal/10, 'DisplayName', 'Filtered Received Data with Noise');
title('Comparison of Original, Filtered, and Filtered with Noise Signals');
xlabel('Samples [n]');
ylabel('Amplitude');
legend; % Show legend
grid on;
hold off;
print(h, fullfile(figures_dir, 'Combined_Original_Filtered.png'), '-dpng', '-r0');

%% Plot of BPSK Signal, Noise, and BPSK with Noise
h = figure('Visible', 'on', 'Position', figure_position);
hold on; % Hold on to plot multiple datasets
plot(summed_signal(1:200), 'DisplayName', 'BPSK Signal');
plot(noise(1:200), 'DisplayName', 'Noise');
plot(received_signal(1:200), 'DisplayName', 'BPSK Signal with Noise');
title('BPSK Signal, Noise, and BPSK Signal with Noise');
xlabel('Samples [n]');
ylabel('Amplitude');
legend; % Show legend
grid on;
hold off;
print(h, fullfile(figures_dir, 'Combined_BPSK_Noise.png'), '-dpng', '-r0');