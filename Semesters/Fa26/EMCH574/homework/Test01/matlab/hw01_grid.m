function t = hw01_grid(tEnd,period,eventTimes)
% Include exact event coordinates as well as samples per oscillation.
cfg = hw01_settings();
assert(tEnd>0 && period>0);
nIntervals = ceil(cfg.samplesPerCycle*tEnd/period);
t = unique([linspace(0,tEnd,nIntervals+1),eventTimes(:)']);
assert(all(t>=0 & t<=tEnd));
end
