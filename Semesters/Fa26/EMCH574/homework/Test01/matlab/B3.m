% B.3. Damped displacement release and permanent 2 percent settling.
cfg = hw01_settings();
m = 5.3; k = 530; c = 22;        % kg, N/m, N s/m
u0 = 4/cfg.mmPerM; v0 = 0;    % m, m/s
Nosc = 12;
disp(table(m,k,c,u0,v0,Nosc));
wn = sqrt(k/m); cCritical = 2*sqrt(m*k);
zeta = c/cCritical; wd = wn*sqrt(1-zeta^2);
tau = 2*pi/wd;
[ts,us,tEnvelope] = hw01_settling(wn,zeta,u0,cfg.settlingFraction);
eventT = [0 tau ts];
eventU = hw01_free(eventT,wn,zeta,u0,v0);
t = hw01_grid(Nosc*tau,tau,eventT);
u = hw01_free(t,wn,zeta,u0,v0);
hw01_check_initial(wn,zeta,u0,v0);
disp(table(wn,cCritical,zeta,wd,tau,ts,tEnvelope));
alpha=zeta*wn; s1=-alpha+1i*wd; s2=conj(s1);
A=u0; B=(v0+alpha*u0)/wd;
C1=(A-1i*B)/2; C2=conj(C1);
amplitude=hypot(A,B); phase=atan2(A,B);
disp(table(s1,s2,C1,C2,A,B,amplitude,phase));
disp(table(eventT',eventU'*cfg.mmPerM, ...
    'VariableNames',{'time_s','displacement_mm'}));
band = cfg.settlingFraction*abs(u0)*cfg.mmPerM;
hw01_plot('B3',t,u*cfg.mmPerM,eventT,eventU*cfg.mmPerM,band);
% A two-period detail makes the final crossing visible.
detailStart = max(0,ts-tau); detailEnd = ts+tau;
td = unique([linspace(detailStart,detailEnd, ...
    2*cfg.samplesPerCycle+1),ts]);
ud = hw01_free(td,wn,zeta,u0,v0);
hw01_plot('B3_settling',td,ud*cfg.mmPerM,ts,us*cfg.mmPerM,band);
