clc;
clear all;
format compact;
% input data
R1=55; R2=9.6; XL1=60; XC1=24;
%Find
%real total impedance
%imaginary total impedance

ZR1=R1;
ZR2=R2;
ZC1=-j*XC1;
ZL1=j*XL1;

ZParallelCircuit=1/(1/ZR1+1/(ZC1+ZR2));
ZT=ZL1+ZParallelCircuit;

real(ZT)
imag(ZT)
