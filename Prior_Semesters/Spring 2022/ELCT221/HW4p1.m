clc;
clear;
format compact ;
R1=4; R4=4; XL2=5; XC3=5; Vs1amp=15; Vs1phase=1.8; Is2amp=0.029; Is2phase=1.8;
V=Vs1amp*exp(j*Vs1phase);% total voltage
I=Is2amp*exp(j*Is2phase);% total voltage

%V/R1=1/R1+1/XL2+1/XC3,-1/XC3
%I=-1/XC3, 1/R4+1/XC3
Matrix=[1/R1+1/XL2+1/XC3,-1/XC3;-1/XC3,1/R4+1/XC3];
CurrentMatrix=[V/R1;];
