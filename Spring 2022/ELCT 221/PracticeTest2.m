clc;
clear;
format compact;
%input data
R1=105; R2=155; L1=20e-6; C1=0.8e-9; f=1e6; Vamp=13; Vphase=0.1;

om=2*pi*f;
ZR1=R1;
ZR2=R2;
ZL1=j*om*L1;
ZC1=-j/(om*C1);

%this is what should change
Zparallelcircuit=1/(1/ZL1+1/ZR2);
ZparallelCircuitBranch2=ZR1+Zparallelcircuit;
ZT=1/(1/ZC1+1/ZparallelCircuitBranch2);% total impedance

V=Vamp*exp(j*Vphase);% total voltage
I=V/ZT;%total current
%Find
%Real Total Impedance
%Imaginary Total impedance
%Current amplitude
%current phase
%voltage amplitude and phase(degrees)
%current amplitude and phase(degrees)
disp("%   "+real(ZT));
disp("%   "+imag(ZT));

disp("%   "+abs(I));
disp("%   "+angle(I));

disp("%   "+abs(V));
disp("%   "+angle(V)*180/pi);

disp("%   "+abs(I));
disp("%   "+angle(I)*180/pi);

%   153.6862
%   -85.2822
%   0.073963
%   0.60661
%   13
%   5.7296
%   0.073963
%   34.756