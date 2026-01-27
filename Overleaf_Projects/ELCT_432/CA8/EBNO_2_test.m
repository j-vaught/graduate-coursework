clc;
clear;
close all;

% Number of simulations and pulses
numSimulations = 100;
numPulses = 1e6;
EbN0_linear = 2; % Linear scale
EbN0_dB = 10^(2/10); % Convert 2 dB to linear scale

% Pre-allocate arrays for BER results
BER_linear = zeros(1, numSimulations);
BER_dB = zeros(1, numSimulations);

for sim = 1:numSimulations
    % Generate random binary data
    data = randi([0, 1], 1, numPulses);
    
    % Generate the BPSK signal
    modulated_signal = generate_bpsk_signal_optimized2(data);
    
    % Calculate the signal power per bit
    signal_power_per_bit = mean(abs(modulated_signal).^2);
    
    % Calculate noise variance for Eb/N0 = 2 (linear scale)
    noise_variance_linear = signal_power_per_bit / (2 * EbN0_linear);
    
    % Calculate noise variance for Eb/N0 = 2 dB
    noise_variance_dB = signal_power_per_bit / (2 * EbN0_dB);
    
    % Generate noise and add to the signal for linear scale
    noise_linear = sqrt(noise_variance_linear) * randn(size(modulated_signal));
    received_signal_linear = modulated_signal + noise_linear;
    
    % Generate noise and add to the signal for dB scale
    noise_dB = sqrt(noise_variance_dB) * randn(size(modulated_signal));
    received_signal_dB = modulated_signal + noise_dB;
    
    % Decode the binary array from the BPSK signal for linear scale
    decoded_array_linear = decode_bpsk_signal(received_signal_linear);
    
    % Decode the binary array from the BPSK signal for dB scale
    decoded_array_dB = decode_bpsk_signal(received_signal_dB);
    
    % Calculate and store BER for linear scale
    BER_linear(sim) = sum(data ~= decoded_array_linear) / numPulses;
    
    % Calculate and store BER for dB scale
    BER_dB(sim) = sum(data ~= decoded_array_dB) / numPulses;
end

% Calculate statistics for linear scale
BER_linear_best = min(BER_linear);
BER_linear_worst = max(BER_linear);
BER_linear_avg = mean(BER_linear);

% Calculate statistics for dB scale
BER_dB_best = min(BER_dB);
BER_dB_worst = max(BER_dB);
BER_dB_avg = mean(BER_dB);

% Display results for linear scale
disp('Results for Eb/N0 = 2 (linear scale):');
disp(['Best BER: ', num2str(BER_linear_best)]);
disp(['Worst BER: ', num2str(BER_linear_worst)]);
disp(['Average BER: ', num2str(BER_linear_avg)]);

% Display results for dB scale
disp('Results for Eb/N0 = 2 dB:');
disp(['Best BER: ', num2str(BER_dB_best)]);
disp(['Worst BER: ', num2str(BER_dB_worst)]);
disp(['Average BER: ', num2str(BER_dB_avg)]);
