% A.2. Frequency, wavelength, lightning range, and microwave mesh.
cLight = 300000*1000;             % m/s, supplied light wavespeed
cSound = 340;                     % m/s, supplied sound wavespeed
mPerMile = 1609.344;              % m/mi, exact conversion
lambdaVisible = 510e-9;           % m
lambdaAM = 550;                   % m
lambdaIR = 10e-6;                 % m
fFM = 89e6; f5G = 29e9;           % Hz
fMicrowave = 2.5e9;               % Hz
flashSecond = 32; thunderSecond = 36;
Dmesh = 1.2e-3;                   % m, approximate measured hole diameter
meshPitch = 1.6e-3;               % m, approximate measured center pitch
DelectronGiven = 2e-12;           % m, stipulated length for item 8
disp(table(cLight,cSound,mPerMile));
disp(table(lambdaVisible,lambdaAM,lambdaIR,fFM,f5G,fMicrowave));
disp(table(flashSecond,thunderSecond,Dmesh,meshPitch,DelectronGiven));

% A.2.1--4 and A.2.6. Use c = lambda*f with SI inputs.
fVisible = cLight/lambdaVisible;
fAM = cLight/lambdaAM;
fIR = cLight/lambdaIR;
lambdaFM = cLight/fFM;
lambda5G = cLight/f5G;
disp(table(fVisible,fAM,fIR,lambdaFM,lambda5G, ...
    'VariableNames',{'visible_Hz','AM_Hz','infrared_Hz', ...
    'FM_m','mobile_m'}));

% A.2.5. Arrival delay equals sound travel time minus light time.
delay = thunderSecond-flashSecond;
distance = delay/(1/cSound-1/cLight);
distanceApprox = cSound*delay;
distanceKm = distance/1000;
distanceMiles = distance/mPerMile;
lightCorrectionMm = (distance-distanceApprox)*1000;
disp(table(delay,distanceKm,distanceMiles,lightCorrectionMm));

% A.2.7. The half-wavelength limit is the assignment's criterion.
lambdaMicrowave = cLight/fMicrowave;
Dmax = lambdaMicrowave/2;
meshToWavelength = Dmesh/lambdaMicrowave; % approximate measured ratio
boundToMesh = Dmax/Dmesh;          % approximate measured ratio
disp(table(lambdaMicrowave,Dmax,Dmesh,meshPitch, ...
    meshToWavelength,boundToMesh));

% A.2.8. Treat the given 2 pm length as the wavelength.
fElectronLength = cLight/DelectronGiven;
disp(table(fElectronLength));
