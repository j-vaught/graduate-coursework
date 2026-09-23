function [u,v] = hw01_free(t,wn,zeta,u0,v0)
% Free response in metres and m/s, including all three damping cases.
assert(isscalar(wn) && wn>0 && isfinite(wn));
assert(isscalar(zeta) && zeta>=0 && isfinite(zeta));
if zeta < 1
    alpha = zeta*wn;
    wd = wn*sqrt(1-zeta^2);
    B = (v0+alpha*u0)/wd;
    harmonic = u0*cos(wd*t)+B*sin(wd*t);
    u = exp(-alpha*t).*harmonic;
    v = exp(-alpha*t).*(-alpha*harmonic ...
        -u0*wd*sin(wd*t)+B*wd*cos(wd*t));
elseif zeta == 1
    B = v0+wn*u0;
    u = (u0+B*t).*exp(-wn*t);
    v = (B-wn*(u0+B*t)).*exp(-wn*t);
else
    q = sqrt(zeta^2-1);
    sFast = -wn*(zeta+q);
    sSlow = -wn/(zeta+q); % Avoid subtraction of nearly equal numbers.
    Cfast = (v0-sSlow*u0)/(sFast-sSlow);
    Cslow = (sFast*u0-v0)/(sFast-sSlow);
    u = Cfast*exp(sFast*t)+Cslow*exp(sSlow*t);
    v = sFast*Cfast*exp(sFast*t)+sSlow*Cslow*exp(sSlow*t);
end
end
