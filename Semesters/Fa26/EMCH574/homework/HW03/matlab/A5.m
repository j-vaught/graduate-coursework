% A.5. Plucked string modal response.
clear; clc; close all;
L=25.5*0.0254; f1=196.0; umax=1.25e-3; N=10;
d=L*[1/2 1/4 7/10]; Nx=2001;
c=2*L*f1; tau=1/f1; j=(1:N)'; gamma=j*pi/L; omega=2*pi*f1*j;
x=linspace(0,L,Nx); t=linspace(0,3*tau,501);
fprintf('L = %.6g m, G3 = %.6g Hz, umax = %.6g mm, N = %d\n',L,f1,umax*1e3,N);
fprintf('c = %.6g m/s, tau = %.6g ms\n',c,tau*1e3);
disp(table(j,gamma,omega,'VariableNames',{'mode','gamma_rad_m','omega_rad_s'}));
U=sin(gamma*x);
figure; plot(x/L,U'); xlabel('x/L'); ylabel('Mode shape'); grid on;
for k=1:numel(d)
    u0=umax*min(x/d(k),(L-x)/(L-d(k)));
    A=2/L*trapz(x,U.*u0,2);
    fprintf('d = %.6g m = %.2f L\n',d(k),d(k)/L);
    disp(table(j,1000*A,'VariableNames',{'mode','A_mm'}));
    figure; plot(x/L,1000*u0,'k-',x/L,1000*(A'*U),'--'); grid on;
    xlabel('x/L'); ylabel('Displacement (mm)'); legend('Initial','Reconstructed');
    figure; bar(j,1000*A); xlabel('Mode'); ylabel('A_j (mm)'); grid on;
    response=(A.*sin(gamma*d(k)))'*cos(omega*t);
    figure; plot(1000*t,1000*response); xlabel('Time (ms)'); ylabel('u(d,t) (mm)'); grid on;
end
