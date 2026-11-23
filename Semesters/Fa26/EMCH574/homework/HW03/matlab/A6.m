clear; clc; close all
L = 25.5*0.0254; m = 0.0015; f1 = 196; zeta = 0.021;
Fe = 0.5; N = 10; f = linspace(20,2000,5000);
j = (1:N)'; gamma = j*pi/L; omega_j = 2*pi*f1*j;
mj = m*L/2*ones(N,1); c = 2*L*f1; tau = 1/f1;
disp(table(L,m,f1,zeta,Fe,N,c,tau))
disp(table(j,gamma,omega_j,mj,zeta*ones(N,1), ...
    'VariableNames',{'j','gamma','omega','modal_mass','zeta'}))
x = linspace(0,L,1000); U = sin(gamma*x);
figure; plot(x/L,U); xlabel('x/L'); ylabel('Mode shape'); grid on
omega = 2*pi*f; locations = [1/3 1/3; 1/3 1/2; 1/2 1/2]*L;
H = zeros(3,numel(f));
figure; hold on
for k = 1:3
    coeff = sin(gamma*locations(k,1)).*sin(gamma*locations(k,2))./mj;
    H(k,:) = sum(coeff./(omega_j.^2-omega.^2+2i*zeta*omega_j.*omega),1);
    y = 20*log10(abs(H(k,:))); plot(f,y)
    idx = find(islocalmax(y,'MinProminence',1));
    p = y(idx);
    fprintf('\nCase %c peaks (Hz, dB, nearest mode)\n','a'+k-1)
    disp([f(idx)' p' round(f(idx)'/f1)])
end
xlabel('Frequency (Hz)'); ylabel('FRF (dB re 1 m/N)')
legend('(a)','(b)','(c)'); grid on
[~,idx] = max(abs(H(2,:))); fd = f(idx);
t = linspace(0,3/fd,1000); u = real(Fe*H(2,idx)*exp(2i*pi*fd*t));
figure; plot(t,u/max(abs(u))); xlabel('Time (s)')
ylabel('Normalized displacement'); grid on
fprintf('Dominant frequency %.3f Hz, period %.6f s\n',fd,1/fd)
