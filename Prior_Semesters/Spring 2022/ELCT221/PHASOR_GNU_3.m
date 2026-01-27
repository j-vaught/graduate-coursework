clc;
clear all;
format compact;
% input data
Iamp=0.3; Iphase=2.5; XC=13;
I=Iamp*exp(j*Iphase);
ZC=-j*XC;
V=I*ZC;
Vamp=abs(V)
Vang=angle(V)*180/pi