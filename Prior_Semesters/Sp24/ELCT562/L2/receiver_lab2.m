
    % ELCT 562
    B = 2.6e6;
    fsample = 20e6;
    Tsample = 1/fsample;
    fc = 910e6;
    TpulseInterval = 1e-6;
    Npulse = 10; % number of pulses you aggregate
    
    
    % Please complete:
    Nsample = 16000; % number of samples to acquire
    
    %% Step 1: Prepare the SDR object
    rxPluto = sdrrx('Pluto', ...
                    'RadioID','ip:192.168.2.1', ...
                    'GainSource','Manual',...
                    'Gain', 25,...
                    'CenterFrequency',fc, ...
                    'OutputDataType', 'double',...
                    'EnableBurstMode', false, ....
                    'SamplesPerFrame', Nsample,...
                    'BasebandSampleRate',fsample, ...
                    'UseCustomFilter',false);
    
    %% Step 2: Record the IQ data
    IQdataTime = rxPluto();
    options.showTimeDomainSignal = 1;
        options.showPowerSpectralDensity = 1;
        options.showIQDiagram = 1;
        options.showTimeDomainSignal3D = 1;
        options.fsample = fsample;
        options.fcarrier = fc;
        options.figureName = 'TX waveform TRANSMITTED';
        options.figurePositionsOption = 1; %0: auto figure position is off, 1: auto figure position is on, 3: internal settings in analyzeIQdata.m
        analyzeIQdata(IQdataTime, options)
        
    % Define subcarrier indices and parameters
    k = [-26:-1 1:26]; % Subcarrier indices for data
    kSynch = [-26:2:25]; % Subcarrier indices for synchronization
    M = numel(k); % Number of subcarriers
    fsample = 20e6; % Sampling frequency in Hz
    fspacing = 50e3; % Subcarrier spacing in Hz
    Tsample = 1/fsample; % Sampling period
    Tsym = 1/fspacing; % Symbol period
    N = round(Tsym/Tsample); % Samples per OFDM symbol, rounded to nearest integer
    Ncp = N/4; % Length of cyclic prefix, quarter of symbol length
    S = 10; % Number of OFDM symbols
    fc=910e6; %Center Frequency
    
    % Calculate OFDM symbol duration including CP
    Tsym = 1 / fspacing; % Symbol duration without cyclic prefix
    T_CP = Ncp / fsample; % Cyclic prefix duration
    T_OFDM = Tsym + T_CP; % Total OFDM symbol duration including CP
    
    bits_per_symbol=16; % For 16-QAM
    % Calculate Data Rate
    bits_per_OFDM_symbol = M * bits_per_symbol; % Total bits per OFDM symbol
    data_rate = bits_per_OFDM_symbol / T_OFDM; % Data rate in bps
    
    % Calculate Bandwidth
    BW = M * fspacing; % Approximate bandwidth
    
    % Display results
    disp(['OFDM Symbol Duration (including CP): ', num2str(T_OFDM), ' seconds']);
    disp(['Data Rate: ', num2str(data_rate / 1e6), ' Mbps']);
    disp(['Bandwidth: ', num2str(BW / 1e6), ' MHz']);
    
    
    Ga = [1 1 1 1 -1 1 1 -1 -1 1 -1 1 -1 1 -1 -1 1 -1 1 1 1 -1 -1 1 1 1];
    Gb = [1 1 1 1 -1 1 1 -1 -1 1 -1 1 1 1 1 1 -1 1 -1 -1 -1 1 1 -1 -1 -1];
    chestSymbols = [Ga Gb];
    syncSymbols = sqrt(2)*(Ga);
    symbolsMapped = zeros(N,S+2);
    symbolsMapped(mod(kSynch,N)+1,1) = syncSymbols;
    symbolsMapped(mod(k,N)+1,2) = chestSymbols;
    X = dftmtx(N)'/sqrt(N);
    r = IQdataTime;
    
    %% Receiver 
    L = N/2;
    P = zeros(1,numel(r)/2);
    R = zeros(1,numel(r)/2);
    for n = 1:numel(r)/2
     for m = 0:L-1
     P(n) = P(n) + r(n+m)*conj(r(n+m+L));
     R(n) = R(n) + r(n+m+L)*conj(r(n+m+L));
     end
    end
    
    figure(4)
    plot(abs(P))
    
    
    metricSync = abs(P).^2./abs(R).^2;
    figure(5)
    plot(abs(metricSync))
    
    
    [~,ind]=find((metricSync)>0.85);
    Nchoosen = ind(end)-5;
    thetaCFO = P(Nchoosen)/abs(P(Nchoosen));
    fcfoEst = -angle(thetaCFO)/(2*pi*L)*fsample
    Npacket = (S+1)*(N+Ncp);
    rPacket = r(Nchoosen+2*L+[0:Npacket-1]);
    rPacket = rPacket.*exp(1i*2*pi*-fcfoEst*[0:Npacket-1].'*Tsample);
    rShaped = reshape(rPacket,N+Ncp,S+1);
    rOFDM = rShaped(Ncp+1:end,:);
    dataSymbol = X'*rOFDM;
    hCFRe = dataSymbol(:,1)./symbolsMapped(:,2);
    
    
    figure(6)
    hold on
    plot([-N/2:N/2-1],abs(fftshift(hCFRe)),'-x','displayname','Channel frequency response est')
    xlim([-N/2, N/2-1])
    xlabel('Subcarrier index')
    ylabel('Amplitude')
    grid on
    
    
    dataSymbolEq = dataSymbol(:,2:end)./repmat(hCFRe,1,S);
    symEstimate = dataSymbolEq(mod(k,N)+1,:);
    scatterplot(symEstimate(:))
    
    
%     bitsRX = zeros(size(symEstimate));
%     bitsRX((real(symEstimate)>0)) = 1;

% Assuming symEstimate contains the estimated symbols from your 16-QAM demodulated signal
% And assuming the constellation is normalized for Unit Average Power as in your encoder

% 16-QAM Demodulation to get back the indices
symbolIndices = qamdemod(symEstimate, 16, 'UnitAveragePower', true);

% Convert indices to binary (each index will be converted back to 4 bits)
% Since the indices range from 0 to 15, we need 4 bits to represent each symbol
bitsRX = de2bi(symbolIndices, 'left-msb');
bitsrx = bitsRX(:, end:-1:1);

% Reshape the bits back into the original bitTX format
% Assuming M and N represent the original dimensions of bitTX
% You may need to adjust dimensions based on how bitTX was originally structured
bitsrxa = reshape(bitsrx.', [], 1).';

    str = char(bin2dec(reshape(char(bitsrxa(:)+'0'), 8,[]).')).'


