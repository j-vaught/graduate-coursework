clc;
clear all;
format compact;
% input data
R1=175; XL1=55; XC1=22;
%Find
%real total impedance
%imaginary total impedance

ZR1=R1;
ZC1=-j*XC1;
ZL1=j*XL1;

ZParallelCircuit=1/(1/ZL1+1/ZC1);
ZT=ZR1+ZParallelCircuit;

real(ZT)
imag(ZT)
