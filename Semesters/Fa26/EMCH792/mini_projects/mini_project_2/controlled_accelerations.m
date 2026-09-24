function [theta_ddot, x_ddot] = accelerations(theta_dot, theta, M, m, ell, c_theta, g, F_cart)
% Nonlinear cart-pendulum equations with an applied horizontal cart force.
% Positive theta is the upright perturbation used in Mini Project 1.

s = sin(theta);
c = cos(theta);
mass_matrix = [M + m, m * ell * c; m * ell * c, m * ell^2];
forcing = [F_cart + m * ell * s * theta_dot^2; ...
           m * g * ell * s - c_theta * theta_dot];
acceleration = mass_matrix \ forcing;

x_ddot = acceleration(1);
theta_ddot = acceleration(2);
end
