% EMCH 574 HW03 B.2. Cantilever eigenvalues.
clear; clc
N = 10;
D = @(z) cos(z) + 1 ./ cosh(z);
j = (1:N).';
z = zeros(N,1);
for k = 1:N
    z(k) = fzero(D, [(k-0.75)*pi, (k-0.25)*pi]);
end
zApprox = (j-0.5)*pi;
disp(table(j,z,zApprox,z-zApprox, ...
    'VariableNames',{'Mode','Eigenvalue','Approximation','Difference'}))
