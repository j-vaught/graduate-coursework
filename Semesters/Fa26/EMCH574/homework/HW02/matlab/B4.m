% B.4. Air vibration in a tube closed at both ends.
clear; clc; close all;
L = 0.85; c = 340; rho = 1.2; N = 5; % m, m/s, kg/m^3, modes
j = (1:N)';
disp(table(L,c,rho,N));

z = j*pi; g = z/L; w = g*c; % eigenvalue, rad/m, rad/s
f = w/(2*pi); lam = 2*L./j; % Hz, m
disp(table(j,z,g,w,f,lam));

x = linspace(0,L,501);
U = sin(g*x); P = -cos(g*x); % one mode per row
C = [0 95 115; 213 94 0; 37 40 42; 0 158 115; 80 86 91]/255;
s = {'-','--',':','-.','--'};

figure('Color','w'); hold on;
for k = 1:N
    plot(x,U(k,:),'Color',C(k,:),'LineStyle',s{k}, ...
        'LineWidth',1.4,'DisplayName',sprintf('Mode %d (%g Hz)',k,f(k)));
end
xlabel('Position along tube, x (m)');
ylabel('Displacement modeshape, U_j(x)');
xlim([0 L]); ylim([-1.1 1.1]); xticks(linspace(0,L,6));
legend('Location','northeast'); grid on; box on;

figure('Color','w'); hold on;
for k = 1:N
    plot(x,P(k,:),'Color',C(k,:),'LineStyle',s{k}, ...
        'LineWidth',1.4,'DisplayName',sprintf('Mode %d (%g Hz)',k,f(k)));
end
xlabel('Position along tube, x (m)');
ylabel('Normalized pressure modeshape, P_j(x)');
xlim([0 L]); ylim([-1.1 1.1]); xticks(linspace(0,L,6));
legend('Location','northeast'); grid on; box on;
