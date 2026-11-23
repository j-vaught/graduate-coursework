clear; clc
L=25*0.0254;
M=[6.42 4.18 2.45 1.332 0.655 0.367]'*1e-3;
T=[24.95 28.93 29.93 30.05 23.31 23.36]'*4.4482216152605;
mu=M/L; c=sqrt(T./mu); f=c/(2*L);
midi=round(69+12*log2(f/440)); fn=440*2.^((midi-69)/12);
error_percent=100*(f./fn-1);
T_match=4*L*M.*fn.^2; M_match=T./(4*L*fn.^2);
disp(table(M,mu,T,c,f,midi,fn,error_percent,T_match,M_match))
