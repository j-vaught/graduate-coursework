clear all
close all
clc


% ELCT 562
    % Constants
    B = 20e6; % Bandwidth of the sinc pulse
    fsample = 50e6; % Sample rate of the SDR
    Tsample = 1/fsample; % Sample time
    fc = 915e6; % Carrier frequency
    TpulseInterval = 1e-6; % Pulse repetition interval
    numPulses = 1000; % Number of pulses


    % Your IQ data generation starts here:
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   
    % Define the sinc pulse of 100 [50-(-50)] samples in length
    ptx = sinc(B*(-50:1:50)*Tsample);

    % Generate numPulses of random symbols [1,-1,j,-j] evenly distributed
    randomSymbols = exp(1j*pi/2*randi([0, 3], numPulses, 1));
    
    % Create a empty list for impulses
    impulseSeries = zeros(1, numPulses * length(ptx));

    % Every 100 samples, it inserts an impulse of the random symbol
    impulseSeries(1:length(ptx):end) = randomSymbols;
    
    % Convolve the sinc pulse with the impulse series
    IQdataTX = conv(ptx, impulseSeries);
    
    %% Step 2: Analyze TX Signal
    options.showTimeDomainSignal = 1;
    options.showPowerSpectralDensity = 1;
    options.showIQDiagram = 0;
    options.showTimeDomainSignal3D = 0;
    options.fsample = fsample;
    options.fcarrier = fc;
    options.figureName = 'TX waveform';
    options.figurePositionsOption = 1; %0: auto figure position is off, 1: auto figure position is on, 3: internal settings in analyzeIQdata.m
    analyzeIQdata(IQdataTX, options)
    
    %% Step 3: Transmit
    if(1)
        % One last step common for all signals: Normalization is needed for remote
        % SDRs' operation: maximum of abs(IQdataTX) should be 1 be less than 1.
        if max(IQdataTX)~=0
            IQdataTX = complex(IQdataTX/max(abs(IQdataTX)));
        end
        txPluto = sdrtx('Pluto', ...
                        'RadioID','ip:169.254.27.102', ...
                        'Gain', -5,...
                        'CenterFrequency',fc, ...
                        'BasebandSampleRate',fsample);
        
        txPluto.ShowAdvancedProperties = true;
        transmitRepeat(txPluto,IQdataTX)
    end
