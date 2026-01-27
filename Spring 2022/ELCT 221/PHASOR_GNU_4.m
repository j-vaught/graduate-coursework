clc;
clear all;
format compact;
% input data
Iamp=0.2; Iphase=0.5; XL=15;
I=Iamp*exp(j*Iphase);
ZL=j*XL;
V=I*ZL;
Vamp=abs(V)
Vang=angle(V)*180/pi