% A.4.3. Standing-wave characteristics.
clear; clc;
c = 340; f = 3.6e3; % m/s, Hz
w = 2*pi*f;
g = w/c;
lam = c/f;
dx = lam/2;
disp(table(c,f));
fprintf('omega = %.6g rad/s\n',w);
fprintf('gamma = %.6g rad/m\n',g);
fprintf('lambda = %.6g mm\n',1000*lam);
fprintf('Node spacing = %.6g mm\n',1000*dx);
