clc;
clear all;
format compact;
% input data
Zreal=7.02; Zimag=3.84; Vamp=12; Vphase=0.2;
V=Vamp*exp(j*Vphase);
ZL=j*Zimag+Zreal;
I=V/ZL;
Iamp=abs(I)
Iang=angle(I)*180/pi