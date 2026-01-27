clc;
clear all;
format compact;
% input data
Vamp=10; Vphase=1.25;
V=Vamp*exp(j*Vphase)

Vamp=abs(V)
Vang=angle(V)*180/pi