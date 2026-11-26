clear; clc; close all
L=0.445; h=0.003; b=0.037; E=200e9; rho=7850; N=5;
A=b*h; m=rho*A; I=b*h^3/12; EI=E*I; a=(EI/m)^(1/4);
z=zeros(1,N);
for j=1:N
    z(j)=fzero(@(v) cos(v)+1/cosh(v),[(j-0.75)*pi,(j-0.25)*pi]);
end
gamma=z/L; omega=a^2*gamma.^2; f=omega/(2*pi);
beta=(cosh(z)+cos(z))./(sinh(z)+sin(z));
x=linspace(0,L,1001); W=zeros(N,numel(x));
for j=1:N
    q=gamma(j)*x;
    W(j,:)=cosh(q)-cos(q)-beta(j)*(sinh(q)-sin(q));
    W(j,:)=W(j,:)/sqrt(trapz(x,W(j,:).^2)/L);
end
Wplot=W./max(abs(W),[],2);
for j=1:N
    figure; plot(x,Wplot(j,:)); ylim([-1 1]); grid on
    xlabel('x (m)'); ylabel('Unit-peak mode shape'); title(sprintf('Mode %d',j))
end
figure; plot(x,Wplot'); ylim([-1 1]); grid on; xlabel('x (m)'); ylabel('Unit-peak mode shape')
legend('1','2','3','4','5')
G=zeros(N);
for j=1:N
    for k=1:N
        G(j,k)=trapz(x,W(j,:).*W(k,:))/L;
    end
end
disp(table((1:N)',z',gamma',omega',f',beta','VariableNames', ...
    {'j','z','gamma_per_m','omega_rad_s','f_Hz','beta'}))
disp('A, m, I, EI, a'); disp([A,m,I,EI,a]); disp(G)
