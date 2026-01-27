%% Close open windows and clear command window
close all;
clear all;
clc;
%% Dynamic Coefficients
%% Dynamic Coefficients
m = 0.588;%insert value here        %Kilograms mass of the car
I_z = 3.73625e-3;%insert value here      %Nm Moment about the Z axis
l_f = 0.095;%insert value here      %m length between the COM and the frount axel
l_r = 0.11;%insert value here      %m length between the COM and the rear axel
C_alphaf = 20E3;%insert value here %N/rad Cornering Stiffness of the Front tire
C_alphar = 20E3;%insert value here %N/rad Cornering Stiffness of the Rear tire
V_x = 0.3;%insert value here      %m/s constant speed of the car

ds = 0.1;%insert value here10cm       %m distance from COM to the sensor

%% Transfer function of the Dynamic Model
A = [0, 1, 0, 0;...
 0, -(2*C_alphaf+2*C_alphar)/(m*V_x), 0, -V_x-(2*l_f*C_alphaf-2*l_r*C_alphar)/(m*V_x);...
 0, 0, 0, 1;...
 0, -(2*l_f*C_alphaf-2*l_r*C_alphar)/(I_z*V_x), 0, - (2*((l_f)^2)*C_alphaf+2*((l_r)^2)*C_alphar)/(I_z*V_x)];;%insert value here
B = [0; (2*C_alphaf)/m; 0; (2*l_f*C_alphaf)/I_z];%insert value here
C = [0,1,ds,0];%insert value here
D = [0];%insert value here
G_dynamicsSS = ss(A,B,C,D,'StateName', {'e_1' 'e_2' 'e_3' 'e_4'},...
 'InputName','delta', 'OutputName', 'y');
G_dynamics = tf(G_dynamicsSS)

%% Servo Coefficients
%Matlab Transfer Function Approximation
num = [-6.239, 9.676, 64.25]; %insert value here
denom = [1, 6.048, 40.46, 81.07, 39.91]; %insert value here

%% Transfer function of the estimated Servo Motor
G_smotor = tf(num,denom, 'InputName','u', 'OutputName', 'delta');
nyquist(G_smotor)

%% Gains of the forward loop
GR = 1; %insert value here %Gear Ratio from servo angle to turn angle
ADC = 5/1024; %insert value here %ADC conversion voltage to 
SenSlope = 10; %insert value here %Ratio from distance to voltage

%% Open-loop transfer function including forward gain
G_Feedback = tf(ADC*SenSlope,'InputName','y', 'OutputName', 'y_d'); 
%Feedback path gain
G_plant = G_dynamics*GR*G_smotor;
G_forward = G_Feedback*G_plant; %Forward path gain

%% Bode plot of the open-loop transfer function including forward gain
figure;
bode(G_forward); %insert transfer function
title('Open Loop Bode Plot');
grid on;

%% Declaring wc and r453rwm
wc =0.54; %insert crossover frequency (rad/s)
wm = deg2rad(68); %insert phase margin

%% Frequency response
F = freqresp(G_forward, wc); %insert [transfer function, wc]
magGforward = abs(F); %magnitude for PI controller
angleGforward = angle(F); %phase for PI controller

%% Calulcating parameters for the PI controller
Kp = (1/(magGforward))*cos(pi+wm-angleGforward) %insert equation
Kd = (1/(wc*magGforward))*sin(pi+wm-angleGforward) %insert equation

%% Including the PD controller in the control loop
num1 = [Kd, Kp]; %insert Kp and Kd in transfer function form
denom1 = [1]; %insert Kp and Kd in transfer function form
G_c = tf(num1,denom1,'InputName','e', 'OutputName', 'u'); 
G_open = G_forward*G_c; %open-loop + controller transfer function

%% Margin plot with the PD controller but not the feedback loop
%figure;
margin(G_open);
%title('Forward Loop Bode Plot with Controller but no Feedback');
%grid on;

%% Nyquist plot with the PD controller but not the feedback loop
figure;
nyquist(G_open); %insert transfer function
title('Forward Loop Nyquist Plot with Controller but no Feedback');
grid on;

%% Pole Zero plot with the PD controller but not the feedack loop
figure;
pzplot(G_open); %insert transfer function
title('Forward Loop Pole Zero Plot with Controller but no Feedback');
grid on;

%% The complete transfer function
%Closed Loop Transfer Function from equation
Gclose = G_open/(1+(G_open)); %closed loop system transfer function
%Closed Loop Transfer Function from functions in control toolbox
% %{
sum = sumblk('e = r_d - y_d'); %Summation block from block diagram
ADC_in = tf(ADC, 1,'InputName','r', 'OutputName', 'r_d'); %referance ADC input
G_closed = connect(ADC_in, G_c, G_plant, G_Feedback, sum, 'r','y'); 
%connect all blocks
%}

%% Pole Zero plot of the closed loop system
figure;
pzplot(G_closed); %insert transfer function
title('Forward Loop Pole Zero Plot with Controller but no Feedback');
grid on;

%% Step response of the closed loop
figure;
step(Gclose); % plot the step response of Gclose
title('Closed Loop Step Response');
grid on;