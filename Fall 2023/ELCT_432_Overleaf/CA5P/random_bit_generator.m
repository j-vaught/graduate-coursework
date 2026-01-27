% Clear figures, variables, and close all plots
clf;
clear;
close all;

% Part 1: Random bit generator and plot for N=10
N = 10;
samples_per_element = 5;
seq = randi([0, 1], 1, N);
%seq(seq == 0) = -1;

expanded_seq = repelem(seq, samples_per_element);
figure('Position', [100, 100, 1024, 768]);
stem(expanded_seq, 'Marker','o', 'LineStyle', 'none');
title('Random Bit Sequence for N=10');
xlabel('Sample Index');
ylabel('Amplitude');
ylim([-0.5 1.5]); % Set y-limits
saveas(gcf, 'random_bit_sequence.png');

% Part 2: Mean, variance, and power
Ns = [10, 100, 1000, 1e4];
mean_values = zeros(1, length(Ns));
variance_values = zeros(1, length(Ns));
power_values = zeros(1, length(Ns));

for i = 1:length(Ns)
    N = Ns(i);
    seq = randi([0, 1], 1, N);
    seq(seq == 0) = -1;
    mean_values(i) = mean(seq);
    variance_values(i) = var(seq);
    power_values(i) = mean(seq.^2);
end

T = table(Ns', mean_values', variance_values', power_values', 'VariableNames', ...
{'N', 'Mean', 'Variance', 'Power'});
disp(T);

% Part 3: Histograms
figure('Position', [100, 100, 1024, 768]);
subplot(1, 2, 1);
seq_10 = randi([0, 1], 1, 10);
%seq_10(seq_10 == 0) = -1;
counts_10 = histcounts(seq_10, [-1.5 -0.5 0.5 1.5]);
bar(-1:1:1, counts_10, 'FaceColor', 'b');
title('Histogram for N=10');
xlabel('Value');
ylabel('Frequency');

subplot(1, 2, 2);
seq_1e4 = randi([0, 1], 1, 1e4);
%seq_1e4(seq_1e4 == 0) = -1;
counts_1e4 = histcounts(seq_1e4, [-1.5 -0.5 0.5 1.5]);
bar(-1:1:1, counts_1e4, 'FaceColor', 'r');
title('Histogram for N=10^4');
xlabel('Value');
ylabel('Frequency');
saveas(gcf, 'histograms.png');