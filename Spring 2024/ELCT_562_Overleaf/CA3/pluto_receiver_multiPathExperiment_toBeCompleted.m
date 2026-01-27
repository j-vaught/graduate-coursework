% Clear workspace, close all figures and clear command window
clear
close all
clc

% Load the received IQ data from a .mat file into the MATLAB workspace
load rxData.mat

% Define the number of samples per pulse
numSamplesPerPulse = 1500;

% Index for selecting a specific pulse (currently set to 0)
pulseIndex = 0;

% Reshape the IQ data to use only the first 1500 samples of the selected pulse
reshapedIQData = IQdataTime(1 + pulseIndex*numSamplesPerPulse : (pulseIndex + 1)*numSamplesPerPulse);

% Split the reshaped IQ Data into 30 segments
splitIQData = reshape(reshapedIQData, [], 30);

% Calculate the average normalized Channel Impulse Response (CIR) over 30 pulses
averageCIR = mean(splitIQData, 2); 
averageCIR_dB = 10 * log10(abs(averageCIR).^2);
normalizedCIR_dB = averageCIR_dB - max(averageCIR_dB);

% Define pulse length and time vector for plotting
pulseLengthInSamples = TpulseInterval * fsample;
timeVectorInNanoSeconds = (0:(pulseLengthInSamples-1)) * (1e9 / fsample);

% Calculate and normalize CIR for each of the 30 pulses
CIRForEachPulse_dB = 10 * log10(abs(splitIQData).^2);
normalizedCIRForEachPulse_dB = CIRForEachPulse_dB - max(CIRForEachPulse_dB, [], 'all');

% Define FFT size for CFR calculation and calculate the normalized Channel Frequency Response (CFR)
fftSize = 256;
frequencyResponse = mean(fft(splitIQData, fftSize), 2);
frequencyResponse_dB = 10 * log10(abs(frequencyResponse).^2);
normalizedCFR_dB = fftshift(frequencyResponse_dB - max(frequencyResponse_dB));

% Create frequency vector for CFR plot
frequencyVector = linspace(-fsample/2, fsample/2, fftSize);

% Calculate coherence bandwidth
correlationFrequencyVector = linspace(-fsample/2, fsample/2, 2*fftSize-1);
correlationVector = xcorr(frequencyResponse_dB, 'normalized')';

% Plotting Section

% Plot the average normalized CIR
figure(101);
plot(timeVectorInNanoSeconds, normalizedCIR_dB);
xlabel('Time [ns]');
ylabel('Average Normalized Gain [dB]');
title('Average Normalized Channel Impulse Response');
grid on;

% Plot all 30 normalized CIRs
figure(102);
plot(timeVectorInNanoSeconds, normalizedCIRForEachPulse_dB);
xlabel('Time [ns]');
ylabel('Normalized Gain [dB]');
title('Normalized Channel Impulse Response for 30 Pulses');
grid on;

% Plot the normalized CFR
figure(103);
plot(frequencyVector, 2 * normalizedCFR_dB);
xlabel('Frequency [Hz]');
ylabel('Normalized Gain [dB]');
title('Normalized Channel Frequency Response');
grid on;

% Plot the normalized correlation
figure(104);
plot(correlationFrequencyVector, correlationVector);
xlim([-50e6 50e6]);
xlabel('Frequency [Hz]');
ylabel('Normalized Correlation');
title('Normalized Correlation');
grid on;
