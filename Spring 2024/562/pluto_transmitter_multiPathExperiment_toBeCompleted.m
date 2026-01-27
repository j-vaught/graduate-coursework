clear all
close all
clc


% ELCT 562
B = 20e6;
fsample = 50e6;
Tsample = 1/fsample;
fc = 915e6;
TpulseInterval = 1e-6;


% Your IQ data generation starts here:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% Step 1: Prepare the signal
    % Please complete
    % ptxInTime = @(t) sinc(B*t)
    % n = [-50:1:50];
    % ptx = ptxInTime(n*Tsample);
    % IQdataTX = ???;
    % IQdataTX = IQdataTX(:);

    Trep = 1/1e-6;
    N = 1000;
    n = randi([0,3],N,1);

    tSamples = [-20:20]/fsample;
    ptx = sinc(B*tSamples);
    
    symbs = exp(1j*pi/2*n);
    upFactor = fsample/Trep;
    upSymbs = upsample(symbs,upFactor);
    
    IQdataTX = conv(upSymbs,ptx);
    
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
                        'RadioID','ip:169.254.27.106', ...
                        'Gain', -5,...
                        'CenterFrequency',fc, ...
                        'BasebandSampleRate',fsample);
        
        txPluto.ShowAdvancedProperties = true;
        transmitRepeat(txPluto,IQdataTX)
    end
