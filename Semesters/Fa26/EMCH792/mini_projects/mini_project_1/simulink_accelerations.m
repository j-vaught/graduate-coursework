function [theta_ddot, x_ddot] = accelerations(theta_dot, theta, M, m, ell, c_theta, g)
% Solve the coupled nonlinear equations for the two accelerations.

s = sin(theta);
c = cos(theta);

mass_matrix = [M + m, m * ell * c; m * ell * c, m * ell^2];
forcing = [m * ell * s * theta_dot^2; m * g * ell * s - c_theta * theta_dot];

acceleration = mass_matrix \ forcing;
x_ddot = acceleration(1);
theta_ddot = acceleration(2);
end
