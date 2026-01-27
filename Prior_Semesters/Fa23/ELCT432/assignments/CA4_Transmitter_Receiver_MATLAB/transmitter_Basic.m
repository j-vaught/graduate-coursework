clear all
close all

%% Step 1: Prepare the IQ data
fsample = 2e6; % it is fixed at the SDRs, don't change this value.
fc = 910e6; % Carrier frequency that you want to transmit. Use ISM bands 
%for transmission [e.g., choose anything between 910e6 and 920e6]
% Your IQ data generation starts here:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Step 2: Prepare the image
imageRGB = imread('gamecocks.png');
imageBW = rgb2gray(imageRGB);
numberOfRows = size(imageBW,1);
numberOfCols = size(imageBW,2);

if(1)
    figure(1); imshow(imageBW);
    title('TX: Image')
end

mt = imageBW(:);
Nsamples = numel(mt);
Tsignal = Nsamples*1/fsample;
msync = linspace(0,1,5e-3*fsample).';
inphase = [msync; 0.5*(2*double(mt)-255)/255];
quadature = zeros()
IQdataTX = inphase + 1i * quadature;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% One last step common for all signals: Normalization is needed for remote
% SDRs' operation: maximum of abs(IQdataTX) should be 1 be less than 1.

if max(IQdataTX)~=0
    IQdataTX = IQdataTX/max(abs(IQdataTX));
end
%% Step 3: Analyze TX waveform
options.showTimeDomainSignal = 1;
options.showPowerSpectralDensity = 1;
options.showIQDiagram = 1;
options.showTimeDomainSignal3D = 1;
options.fsample = fsample;
options.fcarrier = fc;
options.figureName = 'TX waveform';
options.figurePositionsOption = 1; %0: auto figure position is off, 1: auto
%figure position is on, 3: internal settings in analyzeIQdata.m
analyzeIQdata(IQdataTX, options)

%% Step 4: Transmit and receive through SDRs
configuration.timeOutMax = 300; % the maximum limit for downloading the IQ data
configuration.gainTX = 80; % the transmit power gain in dB (adjustable from
%[0:0.25:89.75])
configuration.gainRX = 8.7; % the receive power gain in dB (adjustable from [0,0.9,1.4,2.7,3.7,7.7,8.7,12.5,14.4,15.7,16.6,19.7,20.7,22.9,25.4,28,29.7,
%32.8,33.8,36.4,37.2,38.6,40.2,42.1,43.4,43.9,44.5,48,49.6])
configuration.fcenter = fc; % Carrier frequency that you want to transmit. 
%Use ISM bands for transmission [choose anything between [905e6 925e6]]
configuration.Nrepeat = 1; % This is the amount of repetations for the IQdata. 
%Transmission will repeat by Nrepeat times [choose anything between [1 10]]
[IQdataRX, fc, fsample] = transmitAndReceive(IQdataTX, configuration); % fixed to 2Msps.

%% Step 4: Analyze RX waveform
options.showTimeDomainSignal = 1;
options.showPowerSpectralDensity = 1;
options.showIQDiagram = 1;
options.showTimeDomainSignal3D = 1;
options.fsample = fsample;
options.fcarrier = fc;
options.figurePositionsOption = 1;
options.figureName = 'RX waveform';
analyzeIQdata(IQdataRX, options)

%%%%% Saves variables to a .mat file for analysis with Receiver program if
%%%%% auto functions are not working. 
save('Received_Data.mat', 'fc', 'fsample', 'IQdataRX', 'options');