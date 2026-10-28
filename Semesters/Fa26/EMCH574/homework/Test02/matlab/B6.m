% B.6. Sound intensity and decibel calculations.
clear; clc;

rho = 1.2;                 % air density, kg/m^3
c = 340;                   % sound speed, m/s
Z = rho*c;                 % acoustic impedance, rayl
p = 88e-3;                % specified pressure, Pa
I0 = 1e-12;               % reference intensity, W/m^2
p0 = sqrt(Z*I0);          % consistent reference pressure, Pa

I = p^2/Z;
LI = 10*log10(I/I0);
Lp = 20*log10(p/p0);

D = 1.25;                 % loudspeaker diameter, m
Ls = 72;                   % loudspeaker level, dB
Is = I0*10^(Ls/10);
ps = sqrt(Z*Is);
A = pi*D^2/4;
P = Is*A;

Lh = 124;                  % car-horn level, dB
Ih = I0*10^(Lh/10);
ph = p0*10^(Lh/20);

Ip = 1;                    % pain intensity, W/m^2
pp = sqrt(Z*Ip);

fprintf('B.6 Sound intensity and dB scale\n');
fprintf('Inputs: rho = %.1f kg/m^3, c = %.1f m/s, Z = %.1f rayl\n', rho, c, Z);
fprintf('88 mPa: I = %.6e W/m^2, LI = %.4f dB, Lp = %.4f dB\n', I, LI, Lp);
fprintf('References: I0 = %.1e W/m^2, p0 = %.6e Pa\n', I0, p0);
fprintf('72 dB speaker: I = %.6e W/m^2, p = %.6f Pa, P = %.6e W\n', Is, ps, P);
fprintf('124 dB horn: I = %.6f W/m^2, p = %.6f Pa\n', Ih, ph);
fprintf('Pain reference: I = %.1f W/m^2, p = %.6f Pa, level = %.1f dB\n', ...
    Ip, pp, 10*log10(Ip/I0));
