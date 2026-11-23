% HW03 C.7. Axial bar modes and orthonormality.
clear; clc
D=20e-3; L=3.0; E=70e9; rho=2700; N=5; Nx=1000;
A=pi*D^2/4; c=sqrt(E/rho); x=linspace(0,L,Nx);
fprintf('D = %.4g m, L = %.4g m, E = %.4g Pa, rho = %.4g kg/m^3\n',D,L,E,rho)
fprintf('A = %.6g m^2, c = %.6g m/s\n',A,c)
for mode=1:3
    j=(1:N)';
    if mode==2, gamma=(j-0.5)*pi/L; else, gamma=j*pi/L; end
    omega=c*gamma; f=omega/(2*pi);
    if mode==3
        U=sqrt(2/L)*cos(gamma*x); stress=-sin(gamma*x);
    else
        U=sqrt(2/L)*sin(gamma*x); stress=cos(gamma*x);
    end
    G=zeros(N);
    for p=1:N
        for q=1:N
            G(p,q)=trapz(x,U(p,:).*U(q,:));
        end
    end
    fprintf('\nCase %d: gamma [rad/m], omega [rad/s], f [Hz]\n',mode)
    disp([gamma,omega,f])
    disp('Orthonormality matrix'); disp(G)
    fprintf('Maximum orthonormality error %.3g\n',max(abs(G-eye(N)),[],'all'))
    figure; plot(x,U'); xlabel('x (m)'); ylabel('Unit-integral mode (m^{-1/2})')
    title(sprintf('Case %d displacement modes',mode)); legend('1','2','3','4','5')
    figure; plot(x,stress'); xlabel('x (m)'); ylabel('Normalized stress mode')
    title(sprintf('Case %d stress modes',mode)); legend('1','2','3','4','5')
end
