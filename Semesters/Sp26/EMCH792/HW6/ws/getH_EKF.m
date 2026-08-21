function H = getH_EKF(X)
% X = [x_a;, x_b]
H = zeros(1, 2);
H(1, 1) = 2 * (X(1) + X(2));
H(1, 2) = 2 * (X(1) + X(2));
end