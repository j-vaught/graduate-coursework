function [decoded_binary_array, filtered_signal] = decode_bpsk_signal(received_signal)
    % This function decodes the original binary signal from the received BPSK signal.
    
    % Generate the matched filter which is a time-reversed sinc pulse
    n = -20:20; % Same range as the transmitter
    matched_filter_pulse = sinc(n / 8);
    
    % Convolve the received signal with the matched filter
    filtered_signal = conv(received_signal, matched_filter_pulse, 'same');
    
    % Initialize the decoded binary array
    n_shift = 8; % Number of samples per symbol (bit) as used in the transmitter
    n_bits = floor((length(received_signal)-1) / n_shift);
    decoded_binary_array = zeros(1, n_bits);
    
    % Decode each bit by sampling the filtered signal
    for i = 1:n_bits
        % Calculate the sample index. This assumes that the first sinc pulse peak is at index 1
        sample_index = (i-1) * n_shift + 4; % 5 or 4 is the center index of the sinc pulse
        
        % Sample the signal and determine the bit based on the sign
        decoded_binary_array(i) = filtered_signal(sample_index) > 0;
    end
end
