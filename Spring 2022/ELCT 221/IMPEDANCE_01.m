clc;
clear all;
format compact;
% input data
C=50e-12; f=3e6;
om=2*pi*f;
%Find:
%Real Capacitor Impedance
%Imaginary Capacitor Impedance
ZC=-j/(om*C);%capacitor impedance

%prints in order
real(ZC)
imag(ZC)