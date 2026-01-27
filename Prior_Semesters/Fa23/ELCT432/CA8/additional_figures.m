clc;
clear;
close all;

%% Plot EB/N0 function
step_size = 0.1; % Choose your desired step size
num_bits = 1e6; % Choose the number of bits
EB_N0_Simulation(step_size, num_bits);

%% Plot the individual sinc pulses[Illustration ONLY]
plot_sinc_pulses([0,1,0]);
plot_sinc_pulses([0,0,0]);
plot_sinc_pulses([0,1,1]);

