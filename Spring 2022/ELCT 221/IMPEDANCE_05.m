clc;
clear all;
format compact;
% input data
C=65e-9; f=1e3; R=770; 
om=2*pi*f;
%Find:
%Real Total Impedance
%Imaginary Total Impedance

ZC=-j/(om*C);%capacitor impedance
ZR=R;
ZT=ZR+ZC;

%prints in order
real(ZT)
imag(ZT)