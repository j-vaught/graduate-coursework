clear; clc; close all
L = 22*0.0254; f1 = 440*2^((55-69)/12); N = 5; Nx = 1000;
c = 2*L*f1; j = (1:N)'; gamma = j*pi/L; omega = 2*pi*j*f1;
x = linspace(0,L,Nx); U = sin(gamma*x); Phi = sqrt(2/L)*U;
G = zeros(N);
for p=1:N
    for q=1:N
        G(p,q) = trapz(x,Phi(p,:).*Phi(q,:));
    end
end
disp(table(j,gamma,omega)); fprintf('L = %.4f m, f1 = %.6f Hz, c = %.6f m/s\n',L,f1,c); disp(G)
figure
for k=1:N
 subplot(N,1,k); plot(x,U(k,:)); grid on; ylabel(sprintf('U_%d',k))
end
xlabel('x (m)')
figure; plot(x,U'); grid on; xlabel('x (m)'); ylabel('U_j'); legend('1','2','3','4','5')
