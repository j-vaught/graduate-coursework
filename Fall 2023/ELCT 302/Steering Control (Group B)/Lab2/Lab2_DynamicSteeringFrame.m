clc
clear
close all

% State Space Model Constants for Ackerman Steering
% C: Cornering stiffness for two axels; C=22.5 kN/rad
Car=22.5e3; Caf=22.5e3;
% lf: Distance from the COM to the front axle; lf= 0.095 meters
lf=0.095;
% lr: Distance from the COM to the rear axle; lr= 0.11 meters
lr=0.11;
% Iz: Rotational moment of Inertia
% Iz = (1/12)*m*(w^2 + l^2); w-width of car, l-length of car, m-mass of car
% l=0.29 meters; w=0.185 meters; m=0.588 kg
l=0.29; w=0.185; m=0.588;
Iz=(1/12)*m*(w^(2) + l^(2));

% Vx: Car Velocity; 0.2 m/s
Vx=0.2;

% m: Vehicle Mass; m=0.588 kg

% Model Validation: 
% Assume Initial Point (0,0)
% Form matrices: A, B, C, D
A = [0, 1, 0, 0;...
           0, -(2*Caf + 2*Car)/(m*Vx), 0, -Vx-(2*lf*Caf-2*lr*Car)/(m*Vx);...
           0, 0, 0, 1;...
           0, -(2*lf*Caf-2*lr*Car)/(Iz*Vx), 0, -(2*((lf)^2)*Caf+2*((lr)^2)*Car)/(Iz*Vx)];

B = [0; (2*Caf)/m; 0; (2*lf*Caf)/Iz];

C = eye(4);

D=zeros(4,1);

sys=ss(A,B,C,D)

step(sys)
% Use State-Space class: ss(...)

% Use Step Response function: step(...)

% Approximate the global position.