%% Notation
%ELCT 302
%Team #2, The Short Circuits
%Madelyn Leire Hines, Jacob Christopher Vaught
%Lab 3: Steering Design

%% Close open windows and clear command window
close all;
clear all;
clc;

%% Dynamic Coefficients
m = ;%insert value here        %Kilograms mass of the car
I_z = ;%insert value here      %Nm Moment about the Z axis
l_f = ;%insert value here      %m length between the COM and the frount axel
l_r = ;%insert value here      %m length between the COM and the rear axel
C_alphaf = 20E3;%insert value here %N/rad Cornering Stiffness of the Front tire
C_alphar = 20E3;%insert value here %N/rad Cornering Stiffness of the Rear tire
V_x = ;%insert value here      %m/s constant speed of the car

ds = ;%insert value here       %m distance from COM to the sensor

%% Transfer function of the Dynamic Model
A = [];%insert value here
B = [];%insert value here
C = [];%insert value here
D = [];%insert value here

G_dynamicsSS = ss(A,B,C,D,'StateName', {'e_1' 'e_2' 'e_3' 'e_4'},...
    'InputName','delta', 'OutputName', 'y');
G_dynamics = tf(G_dynamicsSS);

%% Servo Coefficients
%Second Order Lag Approximation
%{
omega_0 = ;%insert value here  %resonant frequency
zeta = ;%insert value here     %damping ratio
G = ;%insert value here        %steady-state gain

num = G*omega_0^2;
denom = [1, 2*zeta*omega_0, omega_0^2];
%}

%Second Order Delay Approximation
% %{
T_delay = 0.1;%insert value here  %
N_order = 2;%insert value here  %
[num,denom] = pade(T_delay, N_order);
%}

%Matlab Transfer Function Approximation
%{
num = ;%insert value here
denom = ;%insert value here
%}

%% Transfer function of the estimated Servo Motor
G_smotor = tf(num,denom, 'InputName','u', 'OutputName', 'delta');

%% Gains of the forward loop
GR = ; %insert value here                               %Gear Ratio from servo angle to turn angle
ADC = ; %insert value here                              %ADC conversion voltage to ADC#
SenSlope = ; %insert value here                         %Ratio from distance to voltage

%%Open-loop transfer function including forward gain
G_Feedback = tf(ADC*SenSlope,...                              
    'InputName','y', 'OutputName', 'y_d'); %Feedback path gain
G_plant = G_dynamics*GR*G_smotor;
G_forward = G_Feedback*G_plant; %Forward path gain
%% Bode plot of the open-loop transfer function including forward gain
figure;
bode(); %insert transfer function
title('Open Loop Bode Plot');
grid on;

%% Declaring wc and wm
wc = ; %insert crossover frequency (rad/s)
wm = ; %insert phase margin

%% Frequency response
F = freqresp(); %insert [transfer function, wc]
magGforward = abs(F);               %magnitude for PI controller
angleGforward = angle(F);           %phase for PI controller

%% Calulcating parameters for the PI controller
Kp = ; %insert equation
Kd = ; %insert equation

%% Including the PD controller in the control loop
num1 = ; %insert Kp and Kd in transfer function form
denom1 = ; %insert Kp and Kd in transfer function form


G_c = tf(num1,denom1,'InputName','e', 'OutputName', 'u');                 
G_open = G_forward*G_c;                 %open-loop + controller transfer function

%% Margin plot with the PD controller but not the feedback loop
figure;
margin();
%title('Forward Loop Bode Plot with Controller but no Feedback');
grid on;

%% Nyquist plot with the PD controller but not the feedback loop
figure;
nyquist(); %insert transfer function
title('Forward Loop Nyquist Plot with Controller but no Feedback');
grid on;

%% Pole Zero plot with the PD controller but not the feedack loop
figure;
pzplot(); %insert transfer function
title('Forward Loop Pole Zero Plot with Controller but no Feedback');
grid on;

%% The complete transfer function
%Closed Loop Transfer Function from equation
%{
%Gclose = Gcopen/(1+(Gcopen));         %closed loop system transfer function
%}

%Closed Loop Transfer Function from functions in control toolbox
% %{
sum = sumblk('e = r_d - y_d'); %Summation block from block diagram
ADC_in = tf(ADC, 1,'InputName','r', 'OutputName', 'r_d'); %referance ADC input
G_closed = connect(ADC_in, G_c, G_plant, G_Feedback, sum, 'r','y'); %connect all blocks
%}

%% Pole Zero plot of the closed loop system
figure;
pzplot(); %insert transfer function
title('Forward Loop Pole Zero Plot with Controller but no Feedback');
grid on;

%% Step response of the closed loop
figure;
step(); % plot the step response of Gclose
title('Closed Loop Step Response');
grid on;