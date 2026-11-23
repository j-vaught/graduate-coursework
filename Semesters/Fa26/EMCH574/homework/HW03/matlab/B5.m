% B.5. Plucked cantilever reed. SI units throughout.
clear; clc; close all
L=14e-3; h=0.3e-3; b=0.75e-3; E=200e9; rho=7850;
wmax=0.15e-3; N=5;
A=b*h; m=rho*A; I=b*h^3/12; EI=E*I; a=(EI/m)^(1/4);
fprintf('L=%g m, h=%g m, b=%g m, E=%g Pa, rho=%g kg/m^3, wmax=%g m\n',L,h,b,E,rho,wmax)
fprintf('A=%g m^2, m=%g kg/m, I=%g m^4, EI=%g N m^2, a=%g m/s^(1/2)\n',A,m,I,EI,a)
j=(1:N)'; z=zeros(N,1);
for k=1:N
    z(k)=fzero(@(q) cos(q)+1./cosh(q),[(k-0.75)*pi,(k-0.25)*pi]);
end
beta=(cosh(z)+cos(z))./(sinh(z)+sin(z));
x=linspace(0,L,2001); s=x/L;
W=cosh(z*s)-cos(z*s)-beta.*(sinh(z*s)-sin(z*s));
f=a^2*(z/L).^2/(2*pi); tau=1/f(1);
w0=wmax*(3*s.^2/2-s.^3/2);
Aj=trapz(x,W.*w0,2)./trapz(x,W.^2,2);
disp(table(j,z,f,Aj))
t=linspace(0,3*tau,2001);
tip=sum((Aj.*W(:,end)).*cos(2*pi*f*t),1);
fprintf('f1=%g Hz, period=%g s, reconstructed tip=%g m\n',f(1),tau,tip(1))
figure; plot(s,W); xlabel('x/L'); ylabel('W_j'); legend('1','2','3','4','5');
figure; plot(s,w0*1e3); xlabel('x/L'); ylabel('w_0 (mm)');
figure; bar(j,Aj*1e3); xlabel('Mode j'); ylabel('A_j (mm)');
figure; plot(t*1e3,tip*1e3); xlabel('Time (ms)'); ylabel('Tip displacement (mm)');
