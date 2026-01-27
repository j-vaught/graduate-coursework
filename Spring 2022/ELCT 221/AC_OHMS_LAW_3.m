clc;
clear all;
format compact;
% input data
%f=10e3;
R=8.5; C=7.4e-6; Vs=4.8; L2=2.9e-3;
%om=2*pi*f;
om=10e3;
%each component's Impedance
ZC=-j/(om*C);
ZL2=j*om*L2;
ZR=R;
%Total Impedance
ZT=1/(1/ZR+1/ZC+1/ZL2);

I=Vs/ZT; %current through whole circuit
IL2=Vs/ZL2; %Current through IL2

%prints amplitude through L2
Im=abs(IL2)
