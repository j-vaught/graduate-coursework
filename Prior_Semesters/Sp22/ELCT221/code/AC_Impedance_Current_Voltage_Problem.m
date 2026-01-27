clc;
clear;
format compact;
% input data
R1=115; R2=36; XL1=25; XC1=120; VSamp=14; VSphase=0.8;
%Find:
%real part of ZT
%imag part of ZT
%amplitude of current
%phase of current
%amplitude of V across L1
%phase of voltage across L1
%amplitude of voltage across R1
%phase of voltage across R1

%convert everything to impedances
ZR1=R1;
ZR2=R2;
ZL1=j*XL1;
ZC1=-j*XC1;
ZParallelCircuit=1/(1/ZR1+1/(ZC1+ZR2));

ZT=ZL1+ZParallelCircuit;%total circuit impedance

V=VSamp*exp(j*VSphase);

I=V/ZT;%Total circuit current

VL1=I*ZL1;%L1 current

VR1=I*ZParallelCircuit; %Voltage at R1

%display everything in order
real(ZT)
imag(ZT)

abs(I)
angle(I)

abs(VL1)
angle(VL1)

abs(VR1)
angle(VR1)
%Results
%   61.3193
%  -17.6601
%    0.2194
%    1.0804
%    5.4849
%    2.6512
%   16.3886
%    0.4726