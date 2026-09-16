% B.7. Constant force amplitude, as specified in the assignment.
cfg = hw01_settings();
L=.568; E=200e9; h=.003; b=.037; % m, Pa, m, m
m=.52; zeta=.14; Fhat=.012;      % kg, dimensionless, N
N0=1500; Nosc=10; Nf=5000;       % rpm, cycles, requested samples
disp(table(L,E,h,b,m,zeta,Fhat,N0,Nosc,Nf));
I=b*h^3/12; k=3*E*I/L^3;        % Cantilever tip stiffness, N/m.
wn=sqrt(k/m); wd=wn*sqrt(1-zeta^2);
cCritical=2*m*wn; c=zeta*cCritical;
uqst=Fhat/k; U=uqst/(2*zeta); tau=2*pi/wn;
wr=wn*sqrt(1-2*zeta^2);
Mr=1/(2*zeta*sqrt(1-zeta^2));
disp(table(I,k,wn,wd,cCritical,c,uqst,wr,Mr,U,tau));
t=hw01_grid(Nosc*tau,tau,[]);
uss=U*sin(wn*t);
% Cancel the steady-state initial velocity to obtain start from rest.
transient=hw01_free(t,wn,zeta,0,-U*wn);
urest=uss+transient;
[uc0,vc0]=hw01_free(0,wn,zeta,0,-U*wn);
assert(abs(uc0)<cfg.checkTolerance);
assert(abs(U*wn+vc0)<cfg.checkTolerance);
hw01_plot('B7_time',t,[uss;urest]*cfg.umPerM,[],[],[]);
f0=N0/cfg.secondsPerMinute; fn=wn/(2*pi);
f=linspace(0,f0,Nf); p=2*pi*f/wn;
FRF=@(r) 1./(1-r.^2+2i*zeta*r);
H=FRF(p);
eventF=[fn 2*fn f0]; eventH=FRF(eventF/fn);
disp(table(eventF',eventF'*cfg.secondsPerMinute, ...
    abs(eventH)',rad2deg(angle(eventH))', ...
    uqst*abs(eventH)'*cfg.umPerM,'VariableNames', ...
    {'frequency_Hz','speed_rpm','magnification','phase_deg','amplitude_um'}));
hw01_plot('B7_magnitude',f,abs(H),eventF,abs(eventH),[]);
hw01_plot('B7_phase',f,rad2deg(angle(H)),[],[],[]);
