% Clear environment and close figures to ensure a clean workspace
clc;        % Clear the Command Window
clear;      % Remove all variables from the workspace
close all;  % Close all open figure windows

% Initialize variables
num_samples = 100000; % Number of samples to generate for the signal
sample_indices = 0:num_samples-1; % Array of indices for each sample
signal = cos(2*pi*sample_indices/num_samples); % Generate a cosine wave over the sample indices
num_quantization_levels = 4; % Define the number of quantization levels

% Uniform Quantization Process
% Calculate equally spaced partition values for uniform quantization across the signal range
uniform_partitions = linspace(min(signal), max(signal), num_quantization_levels+1);
% Determine the midpoints between partitions for quantization
midpoints_uniform = mean([uniform_partitions(1:end-1); uniform_partitions(2:end)]);
% Quantize the signal to the nearest midpoint
[~, quantized_uniform] = quantiz(signal, uniform_partitions(2:end-1), midpoints_uniform);

% Print the assigned quantization levels for uniform quantization
disp(['Assigned Quantization Levels (Uniform): ', mat2str(midpoints_uniform, 6)]);
% Extract and print the thresholds for uniform quantization
uniform_thresholds = uniform_partitions(2:end-1);  % The thresholds are the inner partition values
disp(['Uniform Quantization Thresholds: ', mat2str(uniform_thresholds, 6)]);

% Non-Uniform Quantization Process using K-means
% Apply the k-means algorithm to the signal to determine optimal centroids for quantization
[cluster_indices, centroids] = simple_kmeans(signal(:), num_quantization_levels);
% Map each signal sample to its nearest centroid
quantized_non_uniform = centroids(cluster_indices);

% Sort centroids and print them as the non-uniform quantization levels
sorted_centroids = sort(centroids);
disp(['Assigned Quantization Levels (Non-Uniform): ', mat2str(sorted_centroids, 6)]);
% Calculate and print the thresholds for non-uniform quantization
midpoints_non_uniform = (sorted_centroids(1:end-1) + sorted_centroids(2:end)) / 2;
disp(['Non-Uniform Quantization Thresholds: ', mat2str(midpoints_non_uniform, 6)]);


% Calculate and Compare Mean Squared Error (MSE) for both quantization methods
mse_uniform = mean((signal - quantized_uniform).^2); % MSE for uniform quantization
mse_non_uniform = mean((signal - quantized_non_uniform).^2); % MSE for non-uniform quantization

% Display the MSE results in the Command Window
disp(['MSE for Uniform Quantization: ', num2str(mse_uniform)]);
disp(['MSE for Non-Uniform Quantization: ', num2str(mse_non_uniform)]);

% Plotting the results
% Initialize figure window for plotting
figure;
set(gcf, 'Position', [100, 100, 1500, 500]); % Set the figure size

% Uniform Quantization Plot
subplot(1,2,1); % Create a subplot on the left side
hold on; % Retain plots so that new plots don't delete existing ones
grid on; % Enable grid for better readability

% Plot each quantization level with different colors for uniform quantization
for i = 1:num_quantization_levels
    level_indices = signal >= uniform_partitions(i) & signal < uniform_partitions(i+1);
    scatter(sample_indices(level_indices), signal(level_indices), 10, 'filled');
end

% Overlay the quantized signal onto the original signal plot
plot(sample_indices, quantized_uniform, 'k-', 'LineWidth', 1);

% Add lines to represent uniform quantization thresholds
for i = 2:length(uniform_partitions)-1 % Skip the first and last since they're not thresholds
    yline(uniform_partitions(i), '--', 'Color', [0 0 0], 'LineWidth', 1);
end

% Labeling the uniform quantization plot
title('Uniform Quantization');
xlabel('Sample Index');
ylabel('Signal Amplitude');

% Non-Uniform Quantization Plot
subplot(1,2,2); % Create a subplot on the right side
hold on; % Hold the current plot
grid on; % Enable grid

% Sort centroids and calculate non-uniform partitions
sorted_centroids = sort(centroids);
midpoints_non_uniform = (sorted_centroids(1:end-1) + sorted_centroids(2:end)) / 2;

% Plot each segment of the original signal based on non-uniform quantization
plot_midpoints = [-Inf, midpoints_non_uniform, Inf]; % Include extremes for the first and last segments
for i = 1:num_quantization_levels
    level_indices = signal >= plot_midpoints(i) & signal < plot_midpoints(i+1);
    scatter(sample_indices(level_indices), signal(level_indices), 10, 'filled');
end

% Overlay the quantized signal for non-uniform quantization
plot(sample_indices, quantized_non_uniform, 'k-', 'LineWidth', 1);

% Add lines for non-uniform quantization thresholds
for i = 1:length(midpoints_non_uniform)
    yline(midpoints_non_uniform(i), '--', 'Color', [0 0 0], 'LineWidth', 1);
end

% Labeling the non-uniform quantization plot
title('Non-Uniform Quantization');
xlabel('Sample Index');
ylabel('Signal Amplitude');
