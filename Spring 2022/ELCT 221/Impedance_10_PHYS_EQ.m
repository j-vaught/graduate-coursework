clc;
clear all;
format compact;
% input data
ZTreal=20; ZTimag=-13; f=5e6; 
om=2*pi*f;

C=1/(ZTimag*-om);
R=ZTreal;

R
C