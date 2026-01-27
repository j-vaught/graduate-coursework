clc;
clear all;
format compact;
% input data
R=5; C=1.4e-6; L2=3.9e-3; IR=1.1;
om=10e3;
%each component's Impedance
ZC=-j/(om*C);
ZL2=j*om*L2;
ZR=R;
%Total Impedance
ZT=1/(1/ZR+1/ZC+1/ZL2);
% Voltage through R
Vs=IR*ZR; %voltage through whole circuit and R
IC=Vs/ZC; %Current through C

%prints amplitude of current through C
I=abs(IC)
