% Receiver System for wireless communication correction

%% Step 1a: Coarse Sync
[~, nCoarseSync] = max(real(IQdataRX));
coarseTime = calcCoarseTime(nCoarseSync, fsample);
displayCoarseSync(nCoarseSync, coarseTime);

%% Step 2: CFO Estimation
syncRX = IQdataRX(nCoarseSync - 3000 : nCoarseSync);
[y, freqValues] = performFFT(syncRX, fsample);
plotSegmentForCFO(syncRX);
fCFOEst =  estimateCFO(y, freqValues);

%% Step 3: CFO and Phase Correction
IQdataRXcorrected = correctCFO(IQdataRX, fsample, fCFOEst);
phaseErrorEstimate = estimatePhaseError(IQdataRXcorrected);
IQdataRXcorrected = correctPhaseError(IQdataRXcorrected, phaseErrorEstimate);
analyzeIQdata(IQdataRXcorrected, options);


%% Step 4: Fine Time Sync using Maximum Likelihood Estimation
nFineSync = performFineTimeSync(IQdataRXcorrected, nCoarseSync);
plotFineTimeSync(IQdataRXcorrected, nCoarseSync);

%% Step 5: Display Image
displayReceivedImage(IQdataRXcorrected, nFineSync);


%% Helper Functions

function coarseTime = calcCoarseTime(nCoarseSync, fsample)
    coarseTime = nCoarseSync / fsample;
end

function displayCoarseSync(nCoarseSync, coarseTime)
    fprintf('Coarse sync index: %d, Coarse sync time: %f seconds\n', nCoarseSync, coarseTime);
end

function plotSegmentForCFO(syncRX)
    figure(2);
    plot(real(syncRX));
    xlabel('Sample Index');
    ylabel('Amplitude');
    title('Segment for CFO Estimation');
end

function [y, freqValues] = performFFT(syncRX, fsample)
    N = 2^15;
    y = fft(syncRX, N);
    y = fftshift(y);
    freqValues = (0 : N - 1) / N - 0.5;
    freqValues = freqValues * fsample;
end

function fCFOEst = estimateCFO(y, freqValues)
    [~, nCFO] = max(abs(y));
    fCFOEst = freqValues(nCFO);
    fprintf('Estimated CFO: %f Hz\n', fCFOEst);
end

function IQdataRXcorrected = correctCFO(IQdataRX, fsample, fCFOEst)
    t = (0 : numel(IQdataRX) - 1).' / fsample;
    IQdataRXcorrected = IQdataRX .* exp(-1i * 2 * pi * fCFOEst * t);
    fprintf('CFO corrected.\n');
end

function phaseErrorEstimate = estimatePhaseError(IQdataRXcorrected)
    phaseErrorEstimate = angle(mean(IQdataRXcorrected));
    fprintf('Estimated phase error: %f radians\n', phaseErrorEstimate);
end

function IQdataRXcorrected = correctPhaseError(IQdataRXcorrected, phaseErrorEstimate)
    IQdataRXcorrected = IQdataRXcorrected .* exp(-1i * phaseErrorEstimate);
    fprintf('Phase corrected.\n');
end

function nFineSync = performFineTimeSync(IQdataRXcorrected, nCoarseSync)
    nRange = -1000 : 1000;
    [~, ind] = max(abs(diff(real(IQdataRXcorrected(nCoarseSync + nRange)))));
    nFineSync = nCoarseSync + nRange(ind);
    fprintf('Fine sync index: %d\n', nFineSync);
end

function plotFineTimeSync(IQdataRXcorrected, nCoarseSync)
    nRange = -1000 : 1000;
    figure(4);
    plot(real(IQdataRXcorrected(nCoarseSync + nRange)));
    xlabel('Sample Index');
    ylabel('Amplitude');
    title('Fine Time Sync');
end

function displayReceivedImage(IQdataRXcorrected, nFineSync)
    messageRX = real(IQdataRXcorrected(nFineSync + [1 : 25600]));
    messageRXscaled = uint8((messageRX / max(abs(messageRX)) + 1) / 2 * 255);
    fprintf('Message extracted and scaled.\n');

    % Plot the magnitude of the received signal
    figure(100);
    plot(messageRX);
    title('Magnitude of Received Signal');
    xlabel('Sample Index');
    ylabel('Magnitude');
    imageRXBW = reshape(messageRXscaled, 160, 160);
    figure(7);
    imshow(imageRXBW);
    title('Received Image');
    fprintf('Image displayed.\n');
end

