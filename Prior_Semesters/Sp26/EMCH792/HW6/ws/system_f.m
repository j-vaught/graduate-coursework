function x_p = system_f(X)
% X = [x_a;, x_b]
x_p(1, 1) = -cos(X(2));
x_p(2, 1) =  sin(X(1));
end