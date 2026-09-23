function cfg = hw01_settings()
% Shared numerical and display settings. Calculations use SI units.
cfg.mmPerM = 1e3;
cfg.umPerM = 1e6;
cfg.secondsPerMinute = 60;
cfg.samplesPerCycle = 200;
cfg.samplesPerDecayTime = 50;
cfg.settlingFraction = 0.02;
cfg.checkTolerance = 1e-10;
cfg.colors = [0 95 115; 213 94 0; 37 40 42]/255;
cfg.dataDirectory = fullfile(fileparts(mfilename('fullpath')), ...
    '..','figures','src','solutions','data');
end
