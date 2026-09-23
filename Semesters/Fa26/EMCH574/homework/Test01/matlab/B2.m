% B.2. Illustrative values for the normalized response sketch.
cfg = hw01_settings();
wn = 1; zeta = 0.20;             % rad/s, dimensionless
C = 1; phi = 0.5; Nosc = 3;     % m, rad, cycles
assert(C>0 && zeta>=0 && zeta<1);
disp(table(wn,zeta,C,phi,Nosc));
wd = wn*sqrt(1-zeta^2); tau = 2*pi/wd;
u0 = C*sin(phi);
v0 = C*(wd*cos(phi)-zeta*wn*sin(phi));
t = hw01_grid(Nosc*tau,tau,[]);
u = hw01_free(t,wn,zeta,u0,v0);
envelope = C*exp(-zeta*wn*t);
hw01_check_initial(wn,zeta,u0,v0);
% Divide every ordinate by C, even when C differs from one.
hw01_plot('B2_envelope',wn*t, ...
    [u;envelope;-envelope]/C,[],[],[]);
