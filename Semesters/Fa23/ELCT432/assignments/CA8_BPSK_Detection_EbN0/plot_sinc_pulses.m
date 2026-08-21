function plot_sinc_pulses(binary_array)
    % This function plots all the sinc pulses based on the binary array.
    
    % Prepare to plot
    n_samples = 41;  % Number of samples for the sinc function
    n_shift = 8;     % Shift between each pulse
    total_length = n_samples + (length(binary_array) - 1) * n_shift;
    n = -20:20;  % Sample numbers for sinc
    
    % Initialize the sum of all pulses
    summed_pulses = zeros(1, total_length);
    
    figure; hold on;  % Open a new figure and hold for multiple plots
    
    % Loop through each bit and plot the sinc pulses
    for i = 1:length(binary_array)
        value = binary_array(i) * 2 - 1;
        pulse = value * sinc(n / n_shift);
        pulse_position = 1 + (i-1) * n_shift : n_samples + (i-1) * n_shift;
        plot(pulse_position, pulse, 'DisplayName', sprintf('Pulse for bit %d', i));
        summed_pulses(pulse_position) = summed_pulses(pulse_position) + pulse;
    end
    
    % Plot the summation of all pulses
    plot(1:total_length, summed_pulses, 'k', 'LineWidth', 2, 'DisplayName', 'Summed Signal');
    
    legend show; % Show the legend
    hold off;  % Release the figure for further commands
    title('Sinc Pulses for BPSK and Summed Signal');
    xlabel('Sample number');
    ylabel('Amplitude');
    grid on;
end
