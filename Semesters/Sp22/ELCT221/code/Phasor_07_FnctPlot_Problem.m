clc;
clear all;
format compact;
% input data
R=50; IRamp=0.2; IRphase=pi*180/180;
IR=IRamp*exp(j*IRphase);
ZR=R;
VR=IR*ZR;
Iamp=abs(VR)
Iang=angle(VR)*180/pi
%Iamp=10, Iang=180