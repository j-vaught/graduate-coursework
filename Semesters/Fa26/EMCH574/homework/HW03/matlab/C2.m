clear; clc; close all
E=70e9; rho=2700; D=22.3e-3; d=19.4e-3;
L=[500 352 312 332 384 406]'*1e-3;
e=[110 78 70 74 87 90]'*1e-3;
A=pi*(D^2-d^2)/4; m=rho*A; I=pi*(D^4-d^4)/64;
EI=E*I; a=(EI/m)^0.25;
z=fzero(@(z) cos(z)*cosh(z)-1,[4.5 5]);
beta=(cosh(z)-cos(z))/(sinh(z)-sin(z));
shape=@(s) cosh(z*s)+cos(z*s)-beta*(sinh(z*s)+sin(z*s));
node=fzero(shape,[0.1 0.4]);
gamma=z./L; omega=a^2*gamma.^2; f=omega/(2*pi);
midi=round(69+12*log2(f/440)); f_note=440*2.^((midi-69)/12);
x0=node*L; difference=100*(e-x0)./x0;
midi_natural=[72 84 89 86 81 79]'; f_target=440*2.^((midi_natural-69)/12);
L_target=sqrt(a^2*z^2./(2*pi*f_target));
disp(table(L,gamma,omega,f,midi,f_note,x0,e,difference,L_target))
fprintf('A = %.9g m^2, m = %.9g kg/m, I = %.9g m^4, EI = %.9g N m^2, a = %.9g m/s^0.5, z = %.9f, node/L = %.9f\n',A,m,I,EI,a,z,node)
s=linspace(0,1,1000); W=shape(s); W=W/max(abs(W));
figure
for k=1:6
 subplot(3,2,k); plot(s*L(k),W); grid on
 xlabel('x (m)'); ylabel(sprintf('W_%d',k))
end
