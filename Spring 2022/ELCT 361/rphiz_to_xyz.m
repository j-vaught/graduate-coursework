function returns = rphiz_to_xyz(initialEQN0, initialEQN1, initialEQN2)
syms x y z phi r

%test numbers
%NNED TO find a way to simplify the algebraic expression further
%initialEQN0 = 3*cos(phi);
%initialEQN1 = -2*r;
%initialEQN2 = 5;

eqn0 = cos(phi);
eqn1 = -sin(phi);
eqn2 = 0;

aeqn0 = sin(phi);
aeqn1 = cos(phi);
aeqn2 = 0;

beqn0 = 0;
beqn1 = 0;
beqn2 = 1;


b=[initialEQN0;initialEQN1;initialEQN2];
a= [eqn0,eqn1,eqn2;
    aeqn0,aeqn1,aeqn2;
    beqn0,beqn1,beqn2];
c=a*b;

s1=subs(c(1), r, sqrt(x^2+y^2));
s1=subs(s1, phi, atan(y/x));

s2=subs(c(2), r, sqrt(x^2+y^2));
s2=subs(s2, phi, atan(y/x));

s3=subs(c(3), r, sqrt(x^2+y^2));
s3=subs(s3, phi, atan(y/x));

returns=("("+char(s1)+")a_r + ("+char(s2)+")a_phi + ("+char(s3)+")a_z");




