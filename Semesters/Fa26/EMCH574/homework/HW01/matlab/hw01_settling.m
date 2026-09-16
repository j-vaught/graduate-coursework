function [ts,us,tEnvelope] = hw01_settling(wn,zeta,u0,fraction)
% Final band entry for an underdamped release with ZERO initial velocity.
assert(wn>0 && zeta>0 && zeta<1 && u0~=0);
assert(fraction>0 && fraction<1);
wd = wn*sqrt(1-zeta^2);
alpha = zeta*wn;
% Extrema occur at n*pi/wd and have magnitude abs(u0)*exp(-alpha*t).
n = max(0,ceil(log(1/fraction)*wd/(alpha*pi))-1);
tPeak = n*pi/wd;
tZero = (n*pi+pi/2+atan2(alpha,wd))/wd;
relative = @(t) hw01_free(t,wn,zeta,1,0);
ts = fzero(@(t) abs(relative(t))-fraction,[tPeak tZero]);
us = hw01_free(ts,wn,zeta,u0,0);
tEnvelope = log(1/(fraction*sqrt(1-zeta^2)))/alpha;
assert(exp(-alpha*(n+1)*pi/wd)<=fraction*(1+1e-12));
end
