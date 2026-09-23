% A.3. Perfectly inelastic projectile impact followed by pendulum motion.
cfg = hw01_settings();
g = 9.81; L = 0.500; M = 45;     % m/s^2, m, kg
mp = 0.011; vp = 850;            % kg, m/s
t1 = 18; Nosc = 15; u0 = 0;     % s, cycles, m
disp(table(g,L,M,mp,vp,t1,Nosc,u0));
totalMass = M+mp;
v0 = mp*vp/totalMass;
wn = sqrt(g/L); tau = 2*pi/wn;
amplitude = v0/wn; tPeak = tau/4;
eventT = [tPeak t1];
t = hw01_grid(Nosc*tau,tau,eventT);
u = hw01_free(t,wn,0,u0,v0);
eventU = hw01_free(eventT,wn,0,u0,v0);
hw01_check_initial(wn,0,u0,v0);
assert(abs(totalMass*v0-mp*vp)<cfg.checkTolerance);
disp(table(wn,tau,v0,amplitude*cfg.mmPerM, ...
    eventU(2)*cfg.mmPerM,'VariableNames', ...
    {'wn_rad_s','period_s','v0_m_s','amplitude_mm','u18_mm'}));
hw01_plot('A3',t,u*cfg.mmPerM,eventT,eventU*cfg.mmPerM,[]);
