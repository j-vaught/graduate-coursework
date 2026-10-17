% A.2. Frequencies, wavelengths, and lightning distance.
clear; clc;
c = 3e8; cs = 340;               % light and sound speeds, m/s
lv = 510e-9; la = 550; li = 10e-6; % wavelengths, m
ff = 89e6; fg = 29e9; fm = 2.5e9; % frequencies, Hz
dt = 36-32;                     % lightning arrival delay, s
D = 1.2e-3; p = 1.6e-3;         % measured mesh diameter and pitch, m
de = 2e-12;                     % supplied electron length, m
disp(table(c,cs,lv,la,li,ff,fg,fm,dt,D,p,de));

% A.2.1--4. Use c = lambda*f.
fv = c/lv; fa = c/la; fi = c/li; lf = c/ff;
fprintf('Visible frequency = %.6g Hz\n',fv);
fprintf('AM frequency = %.6g Hz\n',fa);
fprintf('Infrared frequency = %.6g Hz\n',fi);
fprintf('FM wavelength = %.6g m\n',lf);

% A.2.5. Sound travel time minus light travel time is dt.
d = dt/(1/cs-1/c);
fprintf('Lightning distance = %.6g km = %.6g mi\n', ...
    d/1000,d/1609.344);

% A.2.6--7. Mobile and microwave wavelengths.
lg = c/fg; lm = c/fm; dm = lm/2;
fprintf('5G wavelength = %.6g mm\n',1000*lg);
fprintf('Microwave wavelength = %.6g mm\n',1000*lm);
fprintf('Maximum hole diameter = %.6g mm\n',1000*dm);
fprintf('Measured Oster hole diameter = %.3g mm; pitch = %.3g mm\n', ...
    1000*D,1000*p);
fprintf('Hole/wavelength = %.6g; limit/hole = %.6g\n',D/lm,dm/D);

% A.2.8. Use the supplied length as the wavelength.
fe = c/de;
fprintf('Electron-length frequency = %.6g Hz (gamma ray)\n',fe);
