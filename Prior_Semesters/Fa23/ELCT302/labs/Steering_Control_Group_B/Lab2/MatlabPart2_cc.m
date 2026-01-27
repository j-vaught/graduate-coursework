clc
clear all

Caf=22.5e3; Car=22.5e3; m=0.538; Vx=2; lf=0.0979; lr=0.0926; Iz=0.004676;

 
a = [0, 1, 0, 0;...
           0, -(2*Caf+2*Car)/(m*Vx), 0, -Vx-(2*lf*Caf-2*lr*Car)/(m*Vx);...
           0, 0, 0, 1;...
           0, -(2*lf*Caf-2*lr*Car)/(Iz*Vx), 0, -(2*((lf)^2)*Caf+2*((lr)^2)*Car)/(Iz*Vx)];

b = [0; (2*Caf)/m; 0; (2*lf*Caf)/Iz];

c=eye(4);

d=zeros(4,1);

sys=ss(a,b,c,d)

step(sys)