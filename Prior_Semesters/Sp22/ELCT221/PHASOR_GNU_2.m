clc;
clear all;
format compact;
% input data
Iamp=0.3; Iphase=1.5; R=11;
I=Iamp*exp(j*Iphase);
V=I*R;
Vamp=abs(V)
Vang=angle(V)*180/pi