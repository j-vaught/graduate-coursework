clc;
clear all;
format compact;
% input data
R=9.8; L2=7e-3; Vs=3.2;
om=1e3;
%each component's Impedance
ZL2=j*om*L2;
ZR=R;
%Total Impedance
ZT=ZR+ZL2;
% Voltage through R
I=Vs/ZT; %voltage through whole circuit and R

%prints amplitude of current in circuit
Iamp=abs(I)
Iang=angle(I)