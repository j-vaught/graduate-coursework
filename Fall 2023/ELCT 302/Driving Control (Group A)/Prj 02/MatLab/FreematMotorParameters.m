%Parameters for Lab 2
clc;
clear all;
close all;

%K_dc
K_dc=7.266

%K
omega=27.154;%Motor Speed at 50% Duty Cycle
i=0.7; %Motor Current
R=2.93 %Measured Armature Resistance
K=(1/K_dc)-((i*R)/omega)

%B
B=(K*i)/omega

%J
t=30E-3; %time for feedback voltage to reach 63.2% of the final value
s=-(1/t)
J=(-1*(B/s))-(K^2/(s*R))

%L
L=156.03E-6 %Measured inductance

%Percent Error
%act=1.6E-6;
%mea=40E-6;
%n=((act-mea)/mea)*100