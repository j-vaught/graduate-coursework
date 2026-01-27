clear all
close all
clc
fsample = 2e6;
fc = 913e6;
txPluto = sdrtx('Pluto', ...
                'RadioID','ip:169.254.27.103', ...
                'Gain', -5,...
                'CenterFrequency',fc, ...
                'BasebandSampleRate',fsample);
txPluto.ShowAdvancedProperties = true;
% Your IQ data generation starts here:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Nsamples = 20e-3*fsample; % number of samples
timeSamples = [0:Nsamples-1]'*1/fsample;
fm = 20e3;%2kHz
sb = @(t) cos(5*sin(2*pi*fm*t))+1i*sin(5*sin(2*pi*fm*t));
IQdataTX = sb(timeSamples);
% One last step common for all signals: Normalization is needed for remote
% SDRs' operation: maximum of abs(IQdataTX) should be 1 be less than 1.
if max(IQdataTX)~=0
IQdataTX = complex(IQdataTX/max(abs(IQdataTX)));
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% One last step common for all signals: Normalization is needed for remote
% SDRs' operation: maximum of abs(IQdataTX) should be 1 be less than 1.
if max(IQdataTX)~=0
IQdataTX = complex(IQdataTX/max(abs(IQdataTX)));
end
%% Step 3: Analyze TX waveform
options.showTimeDomainSignal = 1;
options.showPowerSpectralDensity = 1;
options.showIQDiagram = 1;
options.showTimeDomainSignal3D = 1;
options.fsample = fsample;
options.fcarrier = fc;
options.figureName = 'TX waveform';
options.figurePositionsOption = 1; %0: auto figure position is off, 1: auto figure position is on, 3: internal settings in analyzeIQdata.m
analyzeIQdata(IQdataTX, options)
%% Step 4: Transmit
%underflow = txPluto(IQdataTX)
transmitRepeat(txPluto,IQdataTX)