function returns = xyz_to_rphiz(initialEQN0, initialEQN1, initialEQN2)
syms x y z phi r

initialEQN0 = x/(x^2+y^2);
initialEQN1 = y/(x^2+y^2);
initialEQN2 = 0;

eqn0 = cos(phi);
eqn1 = sin(phi);
eqn2 = 0;

aeqn0 = -sin(phi);
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

s1=subs(c(1), x, r*cos(phi));
s1=subs(s1,y, r*sin(phi));
s1=simplify(s1);

s2=subs(c(2), x, r*cos(phi));
s2=subs(s2,y, r*sin(phi));
s2=simplify(s2);

s3=subs(c(3), x, r*cos(phi));
s3=subs(s3,y, r*sin(phi));
s3=simplify(s3);

returns=("("+char(s1)+")a_r + ("+char(s2)+")a_phi + ("+char(s3)+")a_z");




