% C.6. Suddenly applied weight and ideal linear bending stresses.
cfg=hw01_settings();
L=.568; E=200e9; h=.003; b=.037; % m, Pa, m, m
m=5.35; g=9.81; yieldStress=710e6; Nosc=10; % kg, m/s^2, Pa.
disp(table(L,E,h,b,m,g,yieldStress,Nosc));
I=b*h^3/12; k=3*E*I/L^3; wn=sqrt(k/m);
F0=m*g; ust=F0/k; tau=2*pi/wn;
tPeak=pi/wn; uPeak=2*ust;
t=hw01_grid(Nosc*tau,tau,tPeak);
% Shift from the unloaded coordinate to equilibrium before solving.
u=ust+hw01_free(t,wn,0,-ust,0);
[initialRelative,initialVelocity]=hw01_free(0,wn,0,-ust,0);
assert(abs(ust+initialRelative)<cfg.checkTolerance);
assert(abs(initialVelocity)<cfg.checkTolerance);
outerFiber=h/2;
momentStatic=F0*L; momentDynamic=k*uPeak*L;
stressStatic=momentStatic*outerFiber/I;
stressDynamic=momentDynamic*outerFiber/I;
SFstatic=yieldStress/stressStatic;
SFdynamic=yieldStress/stressDynamic;
disp(table(I,k,wn,tau,ust*cfg.mmPerM,uPeak*cfg.mmPerM, ...
    stressStatic/1e6,stressDynamic/1e6,SFstatic,SFdynamic, ...
    'VariableNames',{'I_m4','k_N_m','wn_rad_s','period_s', ...
    'static_mm','dynamic_mm','static_MPa','dynamic_MPa', ...
    'SFstatic','SFdynamic'}));
fprintf('Dynamic displacement/span = %.4g\n',uPeak/L);
fprintf('Linear dynamic stress exceeds yield = %d\n',SFdynamic<1);
hw01_plot('C6',t,[u;ust*ones(size(t))]*cfg.mmPerM, ...
    tPeak,uPeak*cfg.mmPerM,[]);
