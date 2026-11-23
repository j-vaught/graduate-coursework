clear; clc
E=70e9; rho=2700; h=0.006; b=0.0092; L=0.0965; target=512;
A=b*h; m=rho*A; I=b*h^3/12; EI=E*I; a=(EI/m)^(1/4);
z=zeros(1,4);
for j=1:4
    z(j)=fzero(@(v) cos(v)+1/cosh(v),[(j-0.75)*pi,(j-0.25)*pi]);
end
f0=a^2*(z(1)/L)^2/(2*pi);
% Manual trial lengths, ending with the refined value.
trial=[0.098,0.0982,0.098178037];
ftrial=a^2*(z(1)./trial).^2/(2*pi);
disp('A, m, I, EI, a, initial f, percentage difference')
disp([A,m,I,EI,a,f0,100*(f0-target)/target])
disp(table(trial',ftrial','VariableNames',{'L_m','f_Hz'}))
disp('Four modal frequencies after adjustment')
disp(a^2*(z/trial(end)).^2/(2*pi))
