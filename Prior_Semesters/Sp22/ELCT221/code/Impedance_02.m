clc;
clear all;
format compact;
% input data
C=65e-9; f=5e3;
om=2*pi*f;
%Find:
%Real Capacitor Impedance
%Imaginary Capacitor Impedance
ZC=-j/(om*C);%capacitor impedance

%prints in order
real(ZC)
imag(ZC)