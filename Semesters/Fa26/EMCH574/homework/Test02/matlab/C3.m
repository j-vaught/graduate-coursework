% C.3. Air vibration with closed-open and open-open boundaries.
clear; clc; close all;
L = 0.500; c = 340; rho = 1.2; N = 5; % m, m/s, kg/m^3, modes
j = (1:N)'; x = linspace(0,L,501);
C = [0 95 115; 213 94 0; 37 40 42; 0 158 115; 80 86 91]/255;
s = {'-','--',':','-.','--'};
disp(table(L,c,rho,N));
% Case (i): closed at x=0 and open at x=L.
z = (2*j-1)*pi/2; g = z/L; w = g*c; f = w/(2*pi);
disp(table(j,z,g,w,f));
U = sin(g*x); P = -cos(g*x);

figure('Color','w'); hold on;
for k = 1:N
    plot(x,U(k,:),'Color',C(k,:),'LineStyle',s{k}, ...
        'LineWidth',1.4,'DisplayName',sprintf('Mode %d (%g Hz)',k,f(k)));
end
xlabel('Position along tube, x (m)');
ylabel('Displacement modeshape, U_j(x)');
xlim([0 L]); ylim([-1.1 1.1]); xticks(0:0.1:0.5);
legend('Location','northeast'); grid on; box on;

figure('Color','w'); hold on;
for k = 1:N
    plot(x,P(k,:),'Color',C(k,:),'LineStyle',s{k}, ...
        'LineWidth',1.4,'DisplayName',sprintf('Mode %d (%g Hz)',k,f(k)));
end
xlabel('Position along tube, x (m)');
ylabel('Normalized pressure modeshape, P_j(x)');
xlim([0 L]); ylim([-1.1 1.1]); xticks(0:0.1:0.5);
legend('Location','northeast'); grid on; box on;
% Case (ii): open at both x=0 and x=L.
z = j*pi; g = z/L; w = g*c; f = w/(2*pi);
disp(table(j,z,g,w,f));
U = cos(g*x); P = sin(g*x);

figure('Color','w'); hold on;
for k = 1:N
    plot(x,U(k,:),'Color',C(k,:),'LineStyle',s{k}, ...
        'LineWidth',1.4,'DisplayName',sprintf('Mode %d (%g Hz)',k,f(k)));
end
xlabel('Position along tube, x (m)');
ylabel('Displacement modeshape, U_j(x)');
xlim([0 L]); ylim([-1.1 1.1]); xticks(0:0.1:0.5);
legend('Location','northeast'); grid on; box on;

figure('Color','w'); hold on;
for k = 1:N
    plot(x,P(k,:),'Color',C(k,:),'LineStyle',s{k}, ...
        'LineWidth',1.4,'DisplayName',sprintf('Mode %d (%g Hz)',k,f(k)));
end
xlabel('Position along tube, x (m)');
ylabel('Normalized pressure modeshape, P_j(x)');
xlim([0 L]); ylim([-1.1 1.1]); xticks(0:0.1:0.5);
legend('Location','northeast'); grid on; box on;
