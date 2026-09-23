% C.8. Flex-beam pendulum using course notes, PDF page 252.
cfg=hw01_settings();
L=.440; M=62; mp=.011; vp=1020;   % m, kg, kg, m/s
E=200e9; h=.004; b=.030; g=9.81; % Pa, m, m, m/s^2
Nosc=23; t1=18; u0=0;
disp(table(L,M,mp,vp,E,h,b,g,Nosc,t1,u0));
I=b*h^3/12; EI=E*I; k=3*EI/L^3;
totalMass=M+mp; v0=mp*vp/totalMass;
% Tip slope/displacement = 3/(2L) in the course approximation.
slopePerDisplacement=3/(2*L);
gravityStiffness=totalMass*g*slopePerDisplacement;
effectiveStiffness=k+gravityStiffness;
wn=sqrt(effectiveStiffness/totalMass);
fn=wn/(2*pi); tau=2*pi/wn; amplitude=v0/wn;
eventT=[tau/4 t1];
t=hw01_grid(Nosc*tau,tau,eventT);
u=hw01_free(t,wn,0,u0,v0);
eventU=hw01_free(eventT,wn,0,u0,v0);
hw01_check_initial(wn,0,u0,v0);
assert(abs(totalMass*v0-mp*vp)<cfg.checkTolerance);
disp(table(I,EI,k,gravityStiffness,effectiveStiffness,v0,wn,fn,tau));
disp(table(eventT',eventU'*cfg.mmPerM, ...
    'VariableNames',{'time_s','displacement_mm'}));
hw01_plot('C8',t,u*cfg.mmPerM,eventT,eventU*cfg.mmPerM,[], ...
    'C8. Flex-beam pendulum using the course-note model');
% Recalculate A.3 from its own inputs for the requested comparison.
L_A3=.500; M_A3=45; mp_A3=.011; vp_A3=850;
wn_A3=sqrt(g/L_A3); v0_A3=mp_A3*vp_A3/(M_A3+mp_A3);
amplitude_A3=v0_A3/wn_A3;
fprintf('Frequency increase over A.3 = %.4g percent\n',100*(wn/wn_A3-1));
fprintf('Amplitude reduction from A.3 = %.4g percent\n', ...
    100*(1-amplitude/amplitude_A3));
% Optional comparison only. The primary answer uses the course model.
preload=totalMass*g; lambda=sqrt(preload/EI);
kT=preload/(L-tanh(lambda*L)/lambda);
wnAlternative=sqrt(kT/totalMass);
tauAlternative=2*pi/wnAlternative;
amplitudeAlternative=v0/wnAlternative;
u10Alternative=hw01_free(t1,wnAlternative,0,u0,v0);
disp(table(wnAlternative,tauAlternative, ...
    amplitudeAlternative*cfg.mmPerM,u10Alternative*cfg.mmPerM, ...
    'VariableNames',{'alternative_wn_rad_s','alternative_period_s', ...
    'alternative_amplitude_mm','alternative_u18_mm'}));
