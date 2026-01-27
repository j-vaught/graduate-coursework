function returns = rthetaphi_to_xyz(initialEQN0, initialEQN1, initialEQN2)

 clc;
 clear;

syms x y z r theta phi 
 initialEQN0 = ((r*cos(phi)^2*cos(theta)*sin(theta))/sin(phi));
 initialEQN1 = ((r*cos(phi)^2*cos(theta)^2)/sin(phi));
 initialEQN2 = (-r*cos(phi)*cos(theta));

eqn0 = sin(theta)*cos(phi);
eqn1 = cos(theta)*cos(phi);
eqn2 = -sin(phi);
% 
% eqn0 = sin(theta)*cos(phi);
% eqn1 = sin(theta)*sin(phi);
% eqn2 = cos(theta);

aeqn0 = sin(theta)*sin(phi);
aeqn1 = cos(theta)*sin(phi);
aeqn2 = cos(phi);

% aeqn0 = cos(theta)*cos(phi);
% aeqn1 = cos(theta)*sin(phi);
% aeqn2 = -sin(theta);

beqn0 = cos(theta);
beqn1 = -sin(theta);
beqn2 = 0;

% beqn0 = -sin(phi);
% beqn1 = cos(phi);
% beqn2 = 0;

b=[initialEQN0;initialEQN1;initialEQN2];
a= [eqn0,eqn1,eqn2;
    aeqn0,aeqn1,aeqn2;
    beqn0,beqn1,beqn2];
c=a*b;

s1=subs(c(1), r, sqrt(x^2+y^2+z^2));
s1=subs(s1, theta, atan(sqrt(x^2+y^2)/z));
s1=subs(s1, phi, atan(y/x));

s2=subs(c(2), r, sqrt(x^2+y^2+z^2));
s2=subs(s2, theta, atan(sqrt(x^2+y^2)/z));
s2=subs(s2, phi, atan(y/x));

s3=subs(c(3), r, sqrt(x^2+y^2+z^2));
s3=subs(s3, theta, atan(sqrt(x^2+y^2)/z));
s3=subs(s3, phi, atan(y/x));

returns=("("+char(s1)+")a_x + ("+char(s2)+")a_y + ("+char(s3)+")a_z");




