% C.8. Longitudinal vibration of a free-free aluminum pressure bar.
clear; clc
D = 20e-3; E = 70e9; rho = 2700; L = 3.2;
c = sqrt(E/rho); t = L/c;
j = (1:3)'; f = j*c/(2*L);
x = linspace(0,L,501);
U = cos(j*pi*x/L);
fprintf('D = %.4g m, E = %.4g Pa, rho = %.4g kg/m^3, L = %.4g m\n',D,E,rho,L);
fprintf('c = %.6f m/s, one-way time = %.9f s\n',c,t);
disp(table(j,f,'VariableNames',{'Mode','Frequency_Hz'}));
figure; plot(x,U); grid on
xlabel('x (m)'); ylabel('Normalized displacement')
legend('j = 1','j = 2','j = 3');
