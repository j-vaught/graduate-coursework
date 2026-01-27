% clear all
% close all
% clc


% ELCT 562
B = 20e6;
fsample = 50e6;
Tsample = 1/fsample;
fc = 915e6;
TpulseInterval = 1e-6;
Npulse = 10; % number of pulses you aggregate

% Please complete:
Nsample = 100000; % number of samples to acquire

%% Step 1: Prepare the SDR object
rxPluto = sdrrx('Pluto', ...
                'RadioID','ip:192.168.2.5', ...
                'GainSource','Manual',...
                'Gain', 55,...
                'CenterFrequency',fc, ...
                'OutputDataType', 'double',...
                'EnableBurstMode', false, ....
                'SamplesPerFrame', Nsample,...
                'BasebandSampleRate',fsample, ...
                'UseCustomFilter',false);

%% Step 2: Record the IQ data
IQdataTime = rxPluto();

%% Step 3: Analyzer the signal in time and frequency
% clear; close all; clc;
% load rxData.mat
% IQdataTimeshaped = reshape(IQdataTime,[],Npulse); % reshape the vector such that you can take the pulses within the interval
% 
% % Please complete:
% % See the normalized channel impulse response with respected to the peak (in 10 log10(abs(h(t)).^2)) (Plot in one interval)
% G = 10*log10(abs(IQdataTime).^2);
% size(G)
% xlabel('Time [ns]')
% ylabel('Gain [dB]')
% grid on
% hold on
% 
% % Please complete:
% % See the channel frequency response (in 10log10(abs(h(t)).^2))
% Nfft = 256;
% IQdataFrequencyshaped = fftshift(fft(IQdataTimeshaped, Nfft));
% figure
% xlabel('Frequency [MHz]')
% ylabel('Gain [dB]')
% grid on
% 
% % Please complete:
% % See the correlation in the frequency
% figure(3)
% grid on
% hold on
% xlabel('Frequency [MHz]')
% ylabel('Normalized correlation')

