function F = getF_EKF(X)
% X = [x_a;, x_b]
F = zeros(2, 2);
F(1, 1) = 0; % df1dxa
F(1, 2) = sin(X(2)); % df1dxb
F(2, 1) = cos(X(1)); % df2dxa
F(2, 2) = 0; % df2dxb
end