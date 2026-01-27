clc;
clear all;
format compact;
% input data
L=50e-6; f=4e6;
om=2*pi*f;
%Find:
%Real inductor Impedance
%Imaginary inductor Impedance
ZL=j*(om*L);%inductor impedance

%prints in order
real(ZL)
imag(ZL)