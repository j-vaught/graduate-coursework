% B.4. Simply supported leaf spring with a central concentrated load.
cfg = hw01_settings();
L = 1.200; b = .040; h = .004;    % m
E = 200e9; m = 520; g = 9.81;   % Pa, kg, m/s^2
u0 = 105/cfg.mmPerM; v0 = 0;    % m, m/s
Nosc = 17; zeta = [.25 .10];
disp(table(L,b,h,E,m,g,u0,v0,Nosc)); disp(zeta);
I = b*h^3/12;                   % Rectangular second moment, m^4.
k = 48*E*I/L^3;                 % Center-load beam stiffness, N/m.
wn = sqrt(k/m); cCritical = 2*m*wn;
staticDeflection = m*g/k;
disp(table(I,k,wn,cCritical,staticDeflection));
names = {'B4_healthy','B4_worn'};
periods = 2*pi./(wn*sqrt(1-zeta.^2));
band = cfg.settlingFraction*abs(u0)*cfg.mmPerM;
for j=1:numel(zeta)
    tau = periods(j); damping = zeta(j)*cCritical;
    [ts,us,tEnvelope] = hw01_settling( ...
        wn,zeta(j),u0,cfg.settlingFraction);
    eventT = [0 tau ts];
    eventU = hw01_free(eventT,wn,zeta(j),u0,v0);
    t = hw01_grid(Nosc*tau,tau,eventT);
    u = hw01_free(t,wn,zeta(j),u0,v0);
    hw01_check_initial(wn,zeta(j),u0,v0);
    wd=2*pi/tau; alpha=zeta(j)*wn;
    s1=-alpha+1i*wd; s2=conj(s1);
    A=u0; B=(v0+alpha*u0)/wd;
    C1=(A-1i*B)/2; C2=conj(C1);
    amplitude=hypot(A,B); phase=atan2(A,B);
    disp(table(s1,s2,C1,C2,A,B,amplitude,phase));
    disp(table(zeta(j),damping,tau,ts,us*cfg.mmPerM,tEnvelope, ...
        'VariableNames',{'zeta','c_Ns_m','period_s', ...
        'settling_s','crossing_mm','envelope_s'}));
    hw01_plot(names{j},t,u*cfg.mmPerM, ...
        eventT,eventU*cfg.mmPerM,band);
end
t = hw01_grid(Nosc*max(periods),min(periods),[]);
u = zeros(numel(zeta),numel(t));
for j=1:numel(zeta)
    u(j,:) = hw01_free(t,wn,zeta(j),u0,v0);
end
hw01_plot('B4_compare',t,u*cfg.mmPerM,[],[],band);
