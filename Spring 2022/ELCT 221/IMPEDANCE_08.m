clc;
clear all;
format compact;
% input data
C=158e-12; f=2e6; L=20e-6; 
om=2*pi*f;
%Find:
%Real Total Impedance
%Imaginary Total Impedance

ZC=-j/(om*C);
ZL=j*(om*L);
ZT=ZL+ZC;%total impedance

%prints in order
real(ZT)
imag(ZT)