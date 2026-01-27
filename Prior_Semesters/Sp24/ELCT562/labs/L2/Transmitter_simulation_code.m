clear; 
close all;
clc; 


% Define subcarrier indices and parameters
k = [-64:-1 1:64];          % Defines the subcarrier indices for data transmission.
kSynch = [-64:2:63];        % Subcarrier indices used for synchronization signals.
M = numel(k);               % Calculates the number of data subcarriers.
fsample = 20e6;             % Sets the sampling frequency to 20 MHz.
fspacing = 25e3;            % Sets the subcarrier spacing to 25 kHz.
Tsample = 1/fsample;        % Calculates the sampling period.
Tsym = 1/fspacing;          % Calculates the symbol period.
N = round(Tsym/Tsample);    % Calculates and rounds the samples per OFDM symbol.
Ncp = N/4;                  % Sets the length of the cyclic prefix to a quarter of the symbol length.
S = 1;                      % Defines the number of OFDM symbols to be transmitted.
T_CP = Ncp / fsample;       % Calculates the duration of the cyclic prefix.
T_OFDM = Tsym + T_CP;       % Calculates the total duration of the OFDM symbol including the cyclic prefix.

% Calculate Data Rate
bits_per_symbol = log2(16);                 % Assumes 16-QAM modulation (4 bits per symbol).
data_rate = (M * bits_per_symbol) / T_OFDM; % Calculates the data rate in bits per second.
BW = M * fspacing;                          % Calculates the total bandwidth of the OFDM system.

%% Transmitter Section
str = 'Hello World'; % String to transmit.
bitTX = reshape(dec2bin(str, 8).'-'0',1,[]); % Converts string to binary.
duplex = floor(M*log2(16)/(length(str)*8)); % Calculates the number of times to repeat the bit string.
repeat = repmat(bitTX, 1, duplex); % Repeats the bit string.
pad = zeros(1, M*log2(16)-duplex*88); % Pads the bit string to fit into an OFDM symbol.
tx = [repeat pad]; % Concatenates the repeated bit string and the padding.
bitTX = tx; % Final bit string for transmission.

% 16-QAM Modulation
symbolMap = qammod(0:15, 16, 'UnitAveragePower', true); % Generates a 16-QAM symbol map.
symbolsTX = reshape(qammod(bi2de(reshape(bitTX,4,[]).'),16,'UnitAveragePower',true),M,[]); % Maps bits to 16-QAM symbols.

% Preparing for OFDM
[Ga, Gb] = generateGolaySequence(4); % Generates Golay sequences for channel estimation.
deletion=M/2-length(Gb);
Ga = Ga(1:end+deletion); % Adjusts Ga sequence length.
Gb = Gb(1:end+deletion); % Adjusts Gb sequence length.
chestSymbols = [Ga Gb]'; % Combines Ga and Gb for channel estimation.
syncSymbols = sqrt(2)*(Ga)'; % Prepares synchronization symbols.

% Pre-process the received IQ data for OFDM demodulation.
symbolsMapped = zeros(N,S+2); % Initializes the symbol mapping matrix.
symbolsMapped(mod(kSynch,N)+1,1) = syncSymbols; % Inserts synchronization symbols.
symbolsMapped(mod(k,N)+1,2) = chestSymbols; % Inserts channel estimation symbols.
symbolsMapped(mod(k,N)+1,3:end) = symbolsTX; % Inserts data symbols.
X = dftmtx(N)'/sqrt(N); % Generates a normalized inverse DFT matrix.

% Perform IFFT, add cyclic prefix, and serialize for transmission
x = ifft(symbolsMapped); % Converts symbols to time domain using IFFT.
x = [x(end-Ncp+1:end,:); x]; % Appends cyclic prefix to each symbol.
x = x(:); % Serializes the OFDM symbols into a single vector for transmission.
IQdataTime = x; % Prepared time domain IQ data for transmission.

options.showTimeDomainSignal = 1;       % Option to visualize time domain signal.
options.showPowerSpectralDensity = 1;   % Option to visualize power spectral density.
options.showIQDiagram = 1;              % Option to visualize IQ diagram.
options.showTimeDomainSignal3D = 1;     % Option to visualize time domain signal in 3D.
options.fsample = fsample;              % Sampling frequency option for visualization.
options.fcarrier = 0;                   % Carrier frequency option (set to baseband).
options.figurePositionsOption = 1;      % Figure positioning option.
options.figureName = 'TX waveform';     % Name for the figure.

% Visualizes the IQ data based on specified options.
analyzeIQdata(IQdataTime, options)

%% Channel Model
% Simulate channel effects
Noffset = 500;          % Adds initial offset to simulate delay in the channel.
x = [zeros(Noffset,1); x; zeros(Noffset,1)]; % Appends zeros to simulate delay.
hCIR = zeros(1,11);     % Initializes channel impulse response.
hCIR(1) = 0.1+0.1i;     % Simulates a multipath component.
hCIR(4) = .02-.1i;      % Simulates another multipath component.
hCIR(11) = 0.5-.1i;     % Simulates a third multipath component.
varNoise = 0.01;       % Sets noise variance.
IQdataTime = filter(hCIR,1,x); % Applies the channel model to the transmitted signal.

options.figureName = 'RX waveform'; % Sets figure name for the receiver visualization.
analyzeIQdata(IQdataTime, options) % Visualizes the received IQ data.

% Synchronization and CFO estimation
L = N/2; % Half the OFDM symbol length for correlation.
P = zeros(1,floor(numel(IQdataTime)/2)); % Initializes correlation for positive lag.
R = zeros(1,floor(numel(IQdataTime)/2)); % Initializes correlation for zero lag.
for n = 1:floor(numel(IQdataTime)/2) % Iterates over half the length of the received IQ data.
    for m = 0:L-1 % Iterates over the lag values.
        P(n) = P(n) + IQdataTime(n+m)*conj(IQdataTime(n+m+L)); % Computes correlation for positive lag.
        R(n) = R(n) + IQdataTime(n+m+L)*conj(IQdataTime(n+m+L)); % Computes correlation for zero lag.
    end
end

figure(1)
plot(abs(P)) % Plots the absolute value of the correlation for positive lag.

% Plot the synchronization metric and find the beginning of the packet.
metricSync = abs(P).^2./abs(R).^2; % Calculates synchronization metric.
[~,ind]=find((metricSync)>0.95); % Finds indices where metric exceeds threshold.
Nchoosen = ind(end)-5; % Chooses the last index before a drop below threshold as the start of the packet.

figure(2)
plot(abs(metricSync)) % Plots the synchronization metric.

% Extract and correct the received packet for CFO.
thetaCFO = P(Nchoosen)/abs(P(Nchoosen)); % Calculates phase difference for CFO estimation.
fcfoEst = -angle(thetaCFO)/(2*pi*L)*fsample; % Estimates the carrier frequency offset.
Npacket = (S+1)*(N+Ncp); % Calculates the length of the packet including cyclic prefix.
rPacket = IQdataTime(Nchoosen+2*L+[0:Npacket-1]); % Extracts the packet from the received IQ data.
rPacket = rPacket.*exp(1i*2*pi*-fcfoEst*[0:Npacket-1].'*Tsample); % Corrects for the estimated CFO.

% OFDM demodulation and channel estimation.
rShaped = reshape(rPacket,N+Ncp,S+1); % Reshapes the received packet for OFDM demodulation.
rOFDM = rShaped(Ncp+1:end,:); % Removes cyclic prefix.
dataSymbol = X'*rOFDM; % Demodulates the OFDM symbols.
hCFRe = dataSymbol(:,1)./symbolsMapped(:,2); % Estimates the channel frequency response.

figure(3)
hold on
plot([-N/2:N/2-1],abs(fftshift(hCFRe)),'-x','displayname','Channel frequency response est') % Plots the estimated channel frequency response.
xlim([-N/2, N/2-1])
xlabel('Subcarrier index')
ylabel('Amplitude')
grid on

% Equalize the received symbols and estimate the transmitted data.
dataSymbolEq = dataSymbol(:,2:end)./repmat(hCFRe,1,S); % Equalizes the received symbols.
symEstimate = dataSymbolEq(mod(k,N)+1,:); % Estimates the transmitted symbols.
scatterplot(symEstimate(:)); % Plots the constellation diagram of the estimated symbols.

% Demodulate the received symbols back to bits.
symbolIndices = qamdemod(symEstimate, 16, 'UnitAveragePower', true); % Demodulates the estimated symbols.
bitsRX = de2bi(symbolIndices, 'left-msb'); % Converts the symbols to bits.
bitsrx = bitsRX(:, end:-1:1); % Reverses bit order.
bitsrxa = reshape(bitsrx.', [], 1).'; % Reshapes the bits for conversion to characters.

% Convert the received bits back to characters.
str = char(bin2dec(reshape(char(bitsrxa(:)+'0'), 8,[]).')).'; % Converts the bits back to a string.
% Display the estimated parameters and received text
fprintf('Estimated CFO: %f Hz\n', fcfoEst);
fprintf('Signal Bandwidth: %f Hz\n', BW);
fprintf('Sample Rate: %f Hz\n', fsample);
fprintf('Packet Size: %d samples\n', Npacket);
fprintf('Subcarrier Spacing: %f Hz\n', fspacing);
fprintf('Cyclic Prefix Duration: %f seconds\n', T_CP);
fprintf('Received Text: %s\n', str);
