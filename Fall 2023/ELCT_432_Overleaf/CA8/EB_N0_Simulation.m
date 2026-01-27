function EB_N0_Simulation(step_size, num_bits)

    % Define the range of Eb/N0 values
    EbN0_dB = 0:step_size:10; % Range from 0 dB to 10 dB

    % Initialize arrays to store BER results
    BER_simulated = zeros(size(EbN0_dB));
    BER_theoretical = zeros(size(EbN0_dB));

    % Generate random binary data
    data = randi([0, 1], 1, num_bits);

    % Modulate the data using BPSK modulation
    modulated_signal = generate_bpsk_signal_optimized2(data);

    % Calculate noise variance for all Eb/N0 values at once
    EbN0_linear = 10.^(EbN0_dB/10); % Convert dB to linear scale
    noise_variance = 1 ./ (2 * EbN0_linear); % Eb/N0 = 1/(2*sigma^2)

    % Pre-calculate the sqrt for the noise generation
    noise_std = sqrt(noise_variance);

    % Pre-calculate theoretical BER using Q-function
    SNR_linear = EbN0_linear; % Since BPSK has no spectral efficiency loss
    Q_sqrt = sqrt(2 * SNR_linear); % Calculate sqrt(2*SNR)
    BER_theoretical = 0.5 * erfc(Q_sqrt);

    % Run simulation
    for i = 1:length(EbN0_dB)% use 'parfor' when using over 10e6 numBits
        % Add AWGN to the signal for this iteration
        noise = noise_std(i) * randn(size(modulated_signal));
        received_signal = modulated_signal + noise;

        % Demodulate the received signal
        [demodulated_data, ~] = decode_bpsk_signal(received_signal);

        % Count the bit errors for simulated BER
        bit_errors_simulated = sum(data ~= demodulated_data);

        % Calculate the simulated BER and store it
        BER_simulated(i) = bit_errors_simulated / num_bits;
    end

    % Plot both the simulated and theoretical BER curves
    semilogy(EbN0_dB, BER_simulated, 'o-', 'DisplayName', 'Simulated BER');
    hold on;
    semilogy(EbN0_dB, BER_theoretical, 'r--', 'DisplayName', 'Theoretical BER');
    title('BER Curve for BPSK Modulation');
    xlabel('Eb/N0 (dB)');
    ylabel('Bit Error Rate (BER)');
    grid on;
    legend('Location', 'best');

end
