%% Clear and close everything
clear; close all; clc;

%% 0. Start by entering your last name here
lastName = "Vaught";
display("EMCH-792 HW2, " + lastName)

%% 1. Define the continuous time model
% Define the model parameters
W = 0.5;

A_c = [0  1  0   0;
       0  0  0  -W;
       0  0  0   1;
       0  W  0   0];

B_c = [0 0;
       1 0;
       0 0;
       0 1];

C_c = [1 0 0 0;
       0 0 1 0];

D_c = [0 0;
       0 0];

% Define continuous time system using the ss function
sys_c = ss(A_c, B_c, C_c, D_c)

%% 2. Check the system's controllability and observability
% Check system's controllability
Co = ctrb(A_c, B_c);
controllability_rank = rank(Co);

% Write in the display function if system is controllable or not
if controllability_rank == size(A_c, 1)
    display("The system is controllable")
else
    display("The system is not controllable")
end

% Check system's observability
Ob = obsv(A_c, C_c);
observability_rank = rank(Ob);

% Write in the display function if system is observable or not
if observability_rank == size(A_c, 1)
    display("The system is observable")
else
    display("The system is not observable")
end

%% 3. Simulate the continuous system in Simulink
% Run build_simulink_models.m from the MATLAB GUI to create both .slx files
% The Simulink models are built programmatically in that script

%% 4. Get the discrete system from the continuous system
% Define the sampling time
Ts = 0.1;

sys_d = c2d(sys_c, Ts)

%% 5. Simulate the discrete system in Simulink
% Run build_simulink_models.m from the MATLAB GUI to create both .slx files

%% 6. Simulate the discrete system in Matlab
% Simulation steps
t_sim = 200;

% Reserve storage for state
x = zeros(4, t_sim);

% Set initial conditions
x(:, 1) = [0, 0.1, 0, 0.1];

% Get the discrete system matrices
A_d = sys_d.A;
B_d = sys_d.B;

% Get the state for all simulation steps
% Use u = 0.01 * randn(2, 1) as your input
for k = 1:t_sim-1
    u = 0.01 * randn(2, 1);
    x(:, k+1) = A_d * x(:, k) + B_d * u;
end

% Plot the simulation results
figure
plot(x(1,:), x(3,:));
title('Discrete-time CT simulation');
xlabel('x-coordinate, \xik'); ylabel('y-coordinate, \etak');

%% BONUS: Discrete time system dynamics for any Omega, T
% Use symbolic math to compute expm(A_c * T) for arbitrary Omega and T
syms Omega T_s real

% Symbolic continuous A matrix
A_sym = [0  1     0   0;
         0  0     0  -Omega;
         0  0     0   1;
         0  Omega 0   0];

% Symbolic continuous B matrix
B_sym = [0 0; 1 0; 0 0; 0 1];

% Discrete A matrix: F = expm(A_sym * T_s)
F = expm(A_sym * T_s);
F = simplify(F);
display("Discrete A matrix (F) for arbitrary Omega, T:")
pretty(F)

% Discrete B matrix: G = integral from 0 to T_s of expm(A_sym * tau) dtau * B
% G = inv(A_sym) * (F - eye(4)) * B_sym for invertible A
% Use integration directly to handle all cases
syms tau real
G_integrand = expm(A_sym * tau) * B_sym;
G = int(G_integrand, tau, 0, T_s);
G = simplify(G);
display("Discrete B matrix (G) for arbitrary Omega, T:")
pretty(G)

% C and D remain the same in discrete time
display("C_d = C_c (unchanged), D_d = D_c (unchanged)")
