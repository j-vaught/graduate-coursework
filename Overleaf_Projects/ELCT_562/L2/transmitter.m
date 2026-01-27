% Clear workspace, close all figures, and clear command window
clear all;
close all;
clc;

% Define subcarrier indices and parameters
k = [-26:-1 1:26]; % Subcarrier indices for data
kSync = [-26:2:25]; % Subcarrier indices for synchronization
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



%% Transmitter Section
% Generate random bits

str = 'Hello World';
bitTX = reshape(dec2bin(str, 8).'-'0',1,[]);
repeat=repmat(bitTX, 1, 23);
pad=zeros(1,2080-23*88);
tx= [repeat pad];
bitTX = tx;

% 16-QAM Modulation
symbolMap = qammod(0:15, 16, 'UnitAveragePower', true); % 16-QAM symbol map
symbolsTX = reshape(qammod(bi2de(reshape(bitTX,4,[]).'),16,'UnitAveragePower',true),M,[]); % Map bits to 16-QAM symbols


referenceSymbolsCHEST = 2*randi([0,1],M,1)-1; % Random reference symbols for channel estimation
referenceSymbolsSYNC = (2*randi([0,1],M/2,1)-1)*sqrt(2); % Synchronization symbols, boosted by sqrt(2)


Ga = [1 1 1 1 -1 1 1 -1 -1 1 -1 1 -1 1 -1 -1 1 -1 1 1 1 -1 -1 1 1 1];
Gb = [1 1 1 1 -1 1 1 -1 -1 1 -1 1 1 1 1 1 -1 1 -1 -1 -1 1 1 -1 -1 -1];
referenceSymbolsCHEST = [Ga Gb]';
referenceSymbolsSYNC = sqrt(2)*(Ga)';


% Initialize symbol padding and insert reference and data symbols
symbolsTXpad = zeros(N,S+2); % Preallocate space for padded symbols
symbolsTXpad(mod(kSync,N)+1,1) = referenceSymbolsSYNC; % Insert synchronization symbols
symbolsTXpad(mod(k,N)+1,2) = referenceSymbolsCHEST; % Insert channel estimation symbols
symbolsTXpad(mod(k,N)+1,3:end) = symbolsTX; % Insert data symbols



% Perform IFFT, add cyclic prefix, and serialize for transmission
x = ifft(symbolsTXpad); % Convert to time domain
x = [x(end-Ncp+1:end,:); x]; % Add cyclic prefix
x = x(:); % Serialize

% Analyze and visualize transmitted waveform if enabled
if false
    options.showTimeDomainSignal = 1;
    options.showPowerSpectralDensity = 1;
    options.showIQDiagram = 1;
    options.showTimeDomainSignal3D = 1;
    options.fsample = fsample;
    options.fcarrier = 0;
    options.figurePositionsOption = 1;
    options.figureName = 'TX waveform ORIGINAL';
    analyzeIQdata(x, options);
end


IQdataTX=x;
options.showTimeDomainSignal = 1;
    options.showPowerSpectralDensity = 1;
    options.showIQDiagram = 0;
    options.showTimeDomainSignal3D = 0;
    options.fsample = fsample;
    options.fcarrier = fc;
    options.figureName = 'TX waveform TRANSMITTED';
    options.figurePositionsOption = 1; %0: auto figure position is off, 1: auto figure position is on, 3: internal settings in analyzeIQdata.m
    analyzeIQdata(IQdataTX, options)
    
  
    if(1)
        
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

