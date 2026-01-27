clc;
clear all;
format compact;
% input data
L=20e-6; f=1e6; R=650; 
om=2*pi*f;
%Find:
%Real Total Impedance
%Imaginary Total Impedance

ZC=j*(om*L);
ZR=R;
ZT=ZR+ZC;%total impedance

%prints in order
real(ZT)
imag(ZT)