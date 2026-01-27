function summed_output = generate_bpsk_signal_optimized2(binary_array)
    % Constants
    n_samples = 41;  % Number of samples for the sinc function
    n_shift = 8;     % Shift between each pulse
    n_zeros = n_shift - 1;  % Number of zeros to insert between pulses

    % Precompute the sinc pulse
    n = -20:20;  % Sample numbers for sinc
    sinc_pulse = sinc(n / n_shift);

    % Convert binary array to BPSK values
    bpsk_values = 2 * binary_array - 1;

    % Create an upsampled array with zeros between the BPSK values
    upsampled_bpsk_values = zeros(1, numel(bpsk_values) + numel(bpsk_values) * n_zeros);
    upsampled_bpsk_values(1:n_shift:end-n_zeros) = bpsk_values;

    % Perform the convolution
    summed_output = conv(upsampled_bpsk_values, sinc_pulse, 'full');

    % Exclude the first and last 16 samples, which are affected by the convolution 'full' option
    summed_output = summed_output(17:end-23);
end
