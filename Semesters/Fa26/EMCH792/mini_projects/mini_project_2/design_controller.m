function [K, design] = design_controller(M, m, ell, c_theta, g)
% Design state feedback for z = [x; x_dot; theta; theta_dot].
% Theta is measured in radians from upright; force is in newtons.

A = [0 1 0 0; ...
     0 0 -m*g/M c_theta/(M*ell); ...
     0 0 0 1; ...
     0 0 (M+m)*g/(M*ell) -c_theta*(M+m)/(M*m*ell^2)];
B = [0; 1/M; 0; -1/(M*ell)];

% Selected penalties for position, velocity, angle, angular velocity.
% The input penalty balances state regulation against control effort.
Q = diag([4 2 300 10]);
R = 0.5;
controllability_rank = rank(ctrb(A, B));
assert(controllability_rank == 4, 'The linear model is not controllable.');
[K, ~, poles] = lqr(A, B, Q, R);
assert(all(real(poles) < 0), 'The linear closed loop is unstable.');

design = struct('A', A, 'B', B, 'Q', Q, 'R', R, 'K', K, ...
    'poles_real', real(poles), 'poles_imag', imag(poles), ...
    'controllability_rank', controllability_rank);
end
