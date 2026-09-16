% B.5. Equal initial conditions for critical and overdamped motion.
cfg = hw01_settings();
fn = 6.25; u0 = 13/cfg.mmPerM; v0 = 0; % Hz, m, m/s
zeta = [1 2.3]; tEnd = 3;             % Required duration, s.
disp(table(fn,u0,v0,tEnd)); disp(zeta);
wn = 2*pi*fn;
q = sqrt(zeta(2)^2-1);
sFast = -wn*(zeta(2)+q); sSlow = -wn/(zeta(2)+q);
dt = 1/(abs(sSlow)*cfg.samplesPerDecayTime);
fastEnd = min(tEnd,6/abs(sFast)); % Resolve the first six fast decay times.
fastGrid = linspace(0,fastEnd,6*cfg.samplesPerDecayTime+1);
t = unique([linspace(0,tEnd,ceil(tEnd/dt)+1),fastGrid]);
u = zeros(numel(zeta),numel(t));
for j=1:numel(zeta)
    u(j,:) = hw01_free(t,wn,zeta(j),u0,v0);
    hw01_check_initial(wn,zeta(j),u0,v0);
end
disp(table(wn,sFast,sSlow));
earlyTime = .01; % Evaluation time used in the written discussion, s.
earlyU = [hw01_free(earlyTime,wn,1,u0,v0), ...
    hw01_free(earlyTime,wn,zeta(2),u0,v0)]*cfg.mmPerM;
disp(table(earlyTime,earlyU(1),earlyU(2),'VariableNames', ...
    {'time_s','critical_mm','overdamped_mm'}));
hw01_plot('B5',t,u*cfg.mmPerM,[],[],[]);
detailEnd = min(tEnd,6/abs(sSlow)); % Six slow decay times.
td = unique([linspace(0,detailEnd,ceil(detailEnd/dt)+1), ...
    fastGrid(fastGrid<=detailEnd)]);
ud = [hw01_free(td,wn,1,u0,v0); ...
    hw01_free(td,wn,zeta(2),u0,v0)];
hw01_plot('B5_detail',td,ud*cfg.mmPerM,[],[],[]);
