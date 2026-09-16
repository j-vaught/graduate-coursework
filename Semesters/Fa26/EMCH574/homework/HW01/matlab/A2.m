% A.2. Ten supplied lengths, their means, and displacement release.
cfg = hw01_settings();
g = 9.81;                         % m/s^2
Lmm = [561.535 562.691 563.845 563.845 565.000 ...
    565.000 566.155 566.155 567.309 568.464];
L = Lmm/cfg.mmPerM;               % m
u0 = 2/cfg.mmPerM; v0 = 0;       % m, m/s
t1 = 10; Nosc = 10;              % s, cycles
disp(table(g,u0,v0,t1,Nosc));
wnEach = sqrt(g./L);
fnEach = wnEach/(2*pi);
tauEach = 2*pi./wnEach;
disp(table(Lmm',wnEach',fnEach',tauEach', ...
    'VariableNames',{'L_mm','wn_rad_s','fn_Hz','period_s'}));
wn = mean(wnEach); fn = mean(fnEach); tauMean = mean(tauEach);
periodOfMeanFrequency = 2*pi/wn;
disp(table(wn,fn,tauMean,periodOfMeanFrequency));
% The prompt requests the MEAN of the individual periods for duration.
tEnd = Nosc*tauMean;
t = hw01_grid(tEnd,periodOfMeanFrequency,t1);
u = hw01_free(t,wn,0,u0,v0);
u1 = hw01_free(t1,wn,0,u0,v0);
uEnd = hw01_free(tEnd,wn,0,u0,v0);
hw01_check_initial(wn,0,u0,v0);
disp(table(tEnd,u1*cfg.mmPerM,uEnd*cfg.mmPerM, ...
    'VariableNames',{'duration_s','u10_mm','uEnd_mm'}));
hw01_plot('A2',t,u*cfg.mmPerM,t1,u1*cfg.mmPerM,[]);
