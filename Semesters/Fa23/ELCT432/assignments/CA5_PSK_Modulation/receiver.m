clear all
close all
clc
fc = 93.5e6;
fsample = 2e6;
rxPluto = sdrrx('Pluto', ...
'RadioID','ip:192.168.2.4', ...
'GainSource','Manual',...
'Gain', 50,...
'CenterFrequency',fc, ...
'OutputDataType', 'double',...
'EnableBurstMode', false, ....
'SamplesPerFrame', 10000000,...
'BasebandSampleRate',fsample);
rxPluto.ShowAdvancedProperties = true;
IQdataRX = rxPluto();
%% Step 1: Analyze RX waveform
options.showTimeDomainSignal = 1;
options.showPowerSpectralDensity = 1;
options.showIQDiagram = 1;
options.showTimeDomainSignal3D = 0;
options.fsample = fsample;
options.fcarrier = fc;
options.figureName = 'RX waveform';
options.figurePositionsOption = 1; %0: auto figure position is off, 1: auto figure position is on, 3: internal settings in analyzeIQdata.m
analyzeIQdata(IQdataRX, options)
save('lab7.mat');
IQdataRXa=myfilter(IQdataRX);
N=fsample*5;
t=(0:N-1)/fsample;
x=diff(unwrap(angle(IQdataRXa)));
y=x/(2*pi*75e3);
y=[y(1);y];
y_r=downsample(y, 10);
soundsc(y_r, 200e3);
plot(y_r)