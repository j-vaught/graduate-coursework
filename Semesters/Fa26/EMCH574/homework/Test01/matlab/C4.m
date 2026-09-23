% C.4. Undamped horizontal cantilever displacement release.
cfg=hw01_settings();
L=.525; E=200e9; h=.004; b=.030; m=62; % SI units.
u0=3/cfg.mmPerM; v0=0; t1=18; Nosc=13;
disp(table(L,E,h,b,m,u0,v0,t1,Nosc));
I=b*h^3/12; EI=E*I; k=3*EI/L^3;
wn=sqrt(k/m); fn=wn/(2*pi); tau=2*pi/wn;
tEnd=Nosc*tau;
t=hw01_grid(tEnd,tau,t1);
u=hw01_free(t,wn,0,u0,v0);
u1=hw01_free(t1,wn,0,u0,v0);
hw01_check_initial(wn,0,u0,v0);
disp(table(I,EI,k,wn,fn,tau,tEnd,u1*cfg.mmPerM, ...
    'VariableNames',{'I_m4','EI_Nm2','k_N_m','wn_rad_s', ...
    'fn_Hz','period_s','duration_s','u18_mm'}));
hw01_plot('C4',t,u*cfg.mmPerM,t1,u1*cfg.mmPerM,[]);
