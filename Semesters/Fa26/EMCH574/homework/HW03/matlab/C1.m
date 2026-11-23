% C.1. Positive flexible eigenvalues of a free-free uniform beam.
clear; clc;
N = 10;
j = (1:N)';
estimate = (j + 0.5) * pi;
z = zeros(N, 1);
for k = 1:N
    % sech(z) - cos(z) has the same positive roots as
    % cosh(z) cos(z) - 1 and avoids overflow.
    z(k) = fzero(@(q) sech(q) - cos(q), ...
        [estimate(k) - pi/4, estimate(k) + pi/4]);
end
fprintf(' j       root              approximation       difference\n')
fprintf('%2d  %16.11f  %16.11f  % .3e\n', ...
    [j, z, estimate, z-estimate].');
