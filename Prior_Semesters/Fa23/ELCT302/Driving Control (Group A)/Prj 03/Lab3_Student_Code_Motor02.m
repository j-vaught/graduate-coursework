%% Notation
%ELCT 302
%Team Number:Group Letter
%Group Member Name, Group Member Name
%Lab 3

%% Close open windows and clear command window
close all;
clear all;
clc;

%% Measured motor parameters
Ti = 1E3;

L = 156E-6;        %insert value here
R = 2.93;          %insert value here
K = 0.0621;        %insert value here
J = 8.75E-5;    %insert value here
B = 0.0016;     %insert value here

%% Transfer function of the open loop DC Motor
num = K;                                      %insert value here
denom = [J*L (J*R)+(B*L) (R*B)+K^2];          %insert value here
Gmotor = tf(num,denom);                       %open loop transfer function

%% Gains of the forward loop
RH = 16/(2*pi);    %insert value here         %Rad to Hz
GR = (1/7.5);      %insert value here         %Gear Ratio 
FV = 0.0022;       %insert value here         %Frequency to voltage
ADC = (1/3.3);     %insert value here         %ADC conversion voltage to ADC#
DutyC = 1;         %insert value here         %Conversion from ADC# to Duty cycle
Vbat = 7.2;        %insert value here         %Gain of the battery
Feedback = RH*FV*ADC;                         %Feedback path gain
Gforward = GR*Gmotor*DutyC*Feedback*Vbat;     %Forward path gain

%% Bode plot of the open-loop transfer function including forward gain
figure;
bode(Gforward);    %insert transfer function
title('Open Loop Bode Plot');
grid on;

%% Data that can be used to find ideal wc and wm
%[mag,phase,freq] = bode(Gforward, logspace(5,9,100));
%Gjwc = mag;
%Pgjwc = phase;
%frequency = freq;

%% Declaring wc and wm
wc = 30;          %insert crossover frequency (rad/s)
wm = deg2rad(60); %insert phase margin

%% Frequency response
F = freqresp(Gforward, wc);                   %insert [transfer function, wc]
magGforward = abs(F);                         %magnitude for PI controller
angleGforward = angle(F);                     %phase for PI controller

%% Calulcating parameters for the PI controller
Kp = (magGforward^-1)*cos(pi+wm-angleGforward);
Ki = (-wc)*(magGforward^-1)*sin(pi+wm-angleGforward);

%% Including the PI controller in the control loop
num1 = [Kp Ki];                               %insert Kp and Ki in transfer function form
denom1 = [1 0];                               %insert Kp and Ki in transfer function form
Gc = tf(num1,denom1);                         %transfer function for PI controller
Gcopen = Gc*Gforward;                         %open-loop + controller transfer function

%% Margin plot with the PI controller but not the feedback loop
figure;
margin(Gcopen);
title('Forward Loop Bode Plot with Controller but no Feedback');
grid on;

%% Nyquist plot with the PI controller but not the feedback loop
figure;
nyquist(Gcopen); %insert transfer function
title('Forward Loop Nyquist Plot with Controller but no Feedback');
grid on;

%% The complete transfer function
Gclose=Gcopen/(1+(Gcopen));                   %closed loop system transfer function

%% Step response of the closed loop
figure;
step(Gclose);   %plot the step response of Gclose
title('Closed Loop Step Response');
grid on;