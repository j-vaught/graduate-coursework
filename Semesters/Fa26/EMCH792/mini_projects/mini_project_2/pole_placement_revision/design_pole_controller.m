function [K, A, B, poles] = design_pole_controller()
% State order is [x; x_dot; theta; theta_dot], with theta in radians.
M = 2; m = 0.5; ell = 1; c = 0.01; g = 9.81;
A = [0 1 0 0; 0 0 -m*g/M c/(M*ell); 0 0 0 1; ...
     0 0 (M+m)*g/(M*ell) -c*(M+m)/(M*m*ell^2)];
B = [0; 1/M; 0; -1/(M*ell)];
% Dominant pair gives damping 0.707 and an approximately 4 s envelope.
poles = [-1+1i -1-1i -3 -4];
a = poly(poles);
C = [B A*B A^2*B A^3*B];
% Ackermann's formula assigns the desired characteristic polynomial.
phi = A^4 + a(2)*A^3 + a(3)*A^2 + a(4)*A + a(5)*eye(4);
K = ([0 0 0 1]/C)*phi;
end
