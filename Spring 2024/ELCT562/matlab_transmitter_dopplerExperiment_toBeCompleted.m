clear all
close all
clc

fsample = 20e6;
fc = 5.9e9 + 100e3;
Tpacket = 10e-3;

txPluto = sdrtx('Pluto', ...
                'RadioID','ip:169.254.27.106', ...
                'Gain', 0,...
                'CenterFrequency',fc, ...
                'BasebandSampleRate',fsample);

txPluto.ShowAdvancedProperties = true;


% Your IQ data generation starts here:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Nsamples = Tpacket*fsample; % number of samples
t = (0:Nsamples-1)/fsample;
IQdataTX = exp(1j*2*pi*0*t)';

% One last step common for all signals: Normalization is needed for remote
% SDRs' operation: maximum of abs(IQdataTX) should be 1 be less than 1.
if max(IQdataTX)~=0
IQdataTX = complex(IQdataTX/max(abs(IQdataTX)));
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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
transmitRepeat(txPluto,IQdataTX)





