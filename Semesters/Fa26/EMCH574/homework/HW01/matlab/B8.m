% B.8. Horizontal cantilever response after an embedded impact.
cfg=hw01_settings();
L=.568; E=200e9; h=.003; b=.037; % m, Pa, m, m
M=53; mp=.018; vp=935;           % kg, kg, m/s
t1=10; Nosc=10; u0=0;          % s, cycles, m
disp(table(L,E,h,b,M,mp,vp,t1,Nosc,u0));
I=b*h^3/12; k=3*E*I/L^3;
totalMass=M+mp; v0=mp*vp/totalMass;
wn=sqrt(k/totalMass); tau=2*pi/wn;
amplitude=v0/wn; eventT=[tau/4 t1];
t=hw01_grid(Nosc*tau,tau,eventT);
u=hw01_free(t,wn,0,u0,v0);
eventU=hw01_free(eventT,wn,0,u0,v0);
hw01_check_initial(wn,0,u0,v0);
assert(abs(totalMass*v0-mp*vp)<cfg.checkTolerance);
disp(table(I,k,v0,wn,tau,amplitude*cfg.mmPerM, ...
    eventU(2)*cfg.mmPerM,'VariableNames', ...
    {'I_m4','k_N_m','v0_m_s','wn_rad_s','period_s','amplitude_mm','u10_mm'}));
hw01_plot('B8',t,u*cfg.mmPerM,eventT,eventU*cfg.mmPerM,[]);
