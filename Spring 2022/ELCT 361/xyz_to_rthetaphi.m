function returns = xyz_to_rthetaphi(initialEQN0, initialEQN1, initialEQN2)

% clc;
% clear;

syms x y z r theta phi 
 initialEQN0 = 0;
 initialEQN1 = 0;
 initialEQN2 = 1;

% eqn0 = sin(theta)*cos(phi);
% eqn1 = cos(theta)*cos(phi);
% eqn2 = -sin(phi);

eqn0 = sin(theta)*cos(phi);
eqn1 = sin(theta)*sin(phi);
eqn2 = cos(theta);

% aeqn0 = sin(theta)*sin(phi);
% aeqn1 = cos(theta)*sin(phi);
% aeqn2 = cos(phi);

aeqn0 = cos(theta)*cos(phi);
aeqn1 = cos(theta)*sin(phi);
aeqn2 = -sin(theta);

% beqn0 = cos(theta);
% beqn1 = -sin(theta);
% beqn2 = 0;

beqn0 = -sin(phi);
beqn1 = cos(phi);
beqn2 = 0;

b=[initialEQN0;initialEQN1;initialEQN2];
a= [eqn0,eqn1,eqn2;
    aeqn0,aeqn1,aeqn2;
    beqn0,beqn1,beqn2];
c=a*b;

s1=subs(c(1), x, r*sin(theta)*cos(phi));
s1=subs(s1, y, r*sin(theta)*sin(phi));
s1=subs(s1, z, r*cos(theta));
s1=simplify(s1);

s2=subs(c(2), x, r*sin(theta)*cos(phi));
s2=subs(s2, y, r*sin(theta)*sin(phi));
s2=subs(s2, z, r*cos(theta));
s2=simplify(s2);

s3=subs(c(3), x, r*sin(theta)*cos(phi));
s3=subs(s3, y, r*sin(theta)*sin(phi));
s3=subs(s3, z, r*cos(theta));
s3=simplify(s3);

returns=("("+char(s1)+")a_r + ("+char(s2)+")a_theta + ("+char(s3)+")a_phi");




