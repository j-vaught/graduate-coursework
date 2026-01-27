clc
clear
close all

% Import BUMP test data; N is number of observations
% Output (Y): N-by-Ny... Ny is number of output channels
% Input (U): N-by-Nu... Nu is number of input channels
% Sample Time (Ts); Default Ts=1
Ts=0.001;
output=readmatrix('OutputData.xlsx'); % Read Excel Output File (as matrix)
input=readmatrix('InputData.xlsx'); % Read Excel Input File (as matrix)

% Smooth Data
Y=smooth(output);
U=smooth(input);

% Estimate the Transfer Function (TF): Controller Gain of Servo Motor
% Y(s)/R(s) = [Gc(s)*K_DAC*Gm(s)]/[1+Gc(s)*K_DAC*Gm(s)*K_ADC]
% NP= number of poles
% NZ= number of zeros
% sys = tfest(data,NP,NZ) % Estimates a continuous-time TF
sys=iddata(Y,U,Ts);
% Proportional (p): Gc = Kp
tf1=tfest(sys,3,0) 
% Proportional Integral (pi): Gc = Kp + (Ki/s)
tf2=tfest(sys,4,1)
% Proportional Integral Derivative (pid): Gc = Kp + (Ki/s) + Kd*s
tf3=tfest(sys,4,2)

% Step Response:
% Proportional (P):
figure;
step(tf1)
title('p')
% Proportional Integral (pi):
figure;
step(tf2)
title('pi')
% Proportional Integral Derivative (pid):
figure;
step(tf3)
title('pid')

% Second-order (Pade Approximation)
figure;
pade(0.3618,2)

