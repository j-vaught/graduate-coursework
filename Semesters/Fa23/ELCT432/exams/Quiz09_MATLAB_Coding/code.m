% PMF Plot
n_values = [-1, 0, 1];
alpha = 2/7;
pmf_values = alpha * (1/2).^n_values;

figure(1);
stem(n_values, pmf_values, 'filled');
title('PMF of X');
xlabel('n');
ylabel('P_X(n)');
grid on;
saveas(gcf,'plot_pmf.png');

% CDF Plot
cdf_values = cumsum(pmf_values);

figure(2);
stem(n_values, cdf_values, 'filled');
title('CDF of X');
xlabel('n');
ylabel('F_X(n)');
grid on;
saveas(gcf,'plot_cdf.png');
