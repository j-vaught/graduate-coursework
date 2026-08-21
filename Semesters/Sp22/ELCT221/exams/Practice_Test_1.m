clc;
clear all;
format compact;
%input data
R1=170; R2=75; L1=30e-6; C1=11e-9; f=1e6; Vamp=11; Vphase=0.1;

om=2*pi*f;
ZR1=R1;
ZR2=R2;
ZL1=j*om*L1;
ZC1=-j/(om*C1);
Zparallelcircuit=1/(1/ZC1+1/ZR2);
ZparallelCircuitBranch2=ZL1+Zparallelcircuit;

ZT=1/(1/ZR1+1/ZparallelCircuitBranch2);% total impedance
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

%   87.2186
%   83.6707
%   0.091012
%   -0.66464
%   11
%   5.7296
%   0.091012
%   -38.0811