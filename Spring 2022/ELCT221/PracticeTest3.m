clc;
clear;
format compact;
%input data
R1=195; L1=18e-6; L2=14e-6; C1=1.4e-9; frequency=1e6; Vamp=19; Vphase=0.1;

om=2*pi*frequency;

%this should change depending on which electrical components you have
ZR1=R1;
ZL1=j*om*L1;
ZL2=j*om*L2;
ZC1=-j/(om*C1);

%this is what should change
Zseriescircuit=ZL1+ZL2;
ZT=1/(1/ZC1+1/ZR1+1/Zseriescircuit);% total impedance

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

%   125.3448
%   -93.4394
%   0.12153
%   0.74059
%   19
%   5.7296
%   0.12153
%   42.4326