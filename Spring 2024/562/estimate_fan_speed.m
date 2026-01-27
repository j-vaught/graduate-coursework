clc;

fc = 5.9e9 + 100e3;
r = 27/100;

fcenter = 85.8e3;
fleft = 84.49e3;
fright = 86.95e3;

c = 3e8;

dfr = fright - fcenter;
dfl = fcenter - fleft;

v1 = dfr/fc * c;
v2 = dfl/fc * c;

v = (v1+v2)/2

rpm1 = v1/(2*pi*r) * 60;
rpm2 = v2/(2*pi*r) * 60;

rpm = (rpm1+rpm2)/2