clc;
clear all;
format compact;
% input data
C=70.4e-12; f=4e6; L=45e-6; 
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