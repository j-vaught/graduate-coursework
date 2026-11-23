% Simply supported uniform steel beam, SI units.
L = 0.445; b = 0.037; h = 0.003;
E = 200e9; rho = 7850; N = 5; Nx = 1000;
A = b*h; m = rho*A; I = b*h^3/12;
EI = E*I; a = (EI/m)^(1/4);
j = (1:N)'; z = j*pi; gamma = z/L;
omega = a^2*gamma.^2; f = omega/(2*pi);
disp('L, b, h, E, rho, N, Nx');
disp([L b h E rho N Nx]);
disp('A, m, I, EI, a'); disp([A m I EI a]);
disp('j, z, gamma, omega, f'); disp([j z gamma omega f]);
x = linspace(0,L,Nx);
W = sin(gamma*x);
phi = sqrt(2/L)*W;
G = zeros(N);
for p = 1:N
    for q = 1:N
        G(p,q) = trapz(x,phi(p,:).*phi(q,:));
    end
end
disp('Unit-integral modal Gram matrix'); disp(G);
figure;
for k = 1:N
    subplot(2,3,k); plot(x,W(k,:)); grid on;
    xlabel('x (m)'); ylabel(sprintf('W_%d',k));
end
subplot(2,3,6); plot(x,W); grid on;
xlabel('x (m)'); ylabel('W_j');
