clc;
clear all;
format compact;
% input data
L=55e-3; f=4e3;
om=2*pi*f;
%Find:
%Real inductor Impedance
%Imaginary inductor Impedance
ZL=j*(om*L);%inductor impedance

%prints in order
real(ZL)
imag(ZL)