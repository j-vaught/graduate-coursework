function verify_hw01()
% Independent state-space checks and final-settling guarantees.
wn=7.3; u0=.013; v0=-.021;
times=[0 .001 .1 1];
for zeta=[0 .1 .25 1 2.3 10]
    [u,v]=hw01_free(times,wn,zeta,u0,v0);
    stateMatrix=[0 1;-wn^2 -2*zeta*wn];
    for j=1:numel(times)
        expected=expm(stateMatrix*times(j))*[u0;v0];
        assert(norm([u(j);v(j)]-expected,inf)<1e-10);
    end
end
% Vary frequency, damping, release sign, and settling-band width.
for wn=[2.3 7.4]
    for zeta=[.05 .1 .25 .7 .95]
        for fraction=[.02 .05]
            for u0=[-.012 .035]
                [ts,us,tEnvelope]=hw01_settling(wn,zeta,u0,fraction);
                band=fraction*abs(u0);
                assert(abs(abs(us)-band)<1e-10);
                wd=wn*sqrt(1-zeta^2);
                before=hw01_free(ts-1e-7/wn,wn,zeta,u0,0);
                assert(abs(before)>band);
                n=ceil(ts*wd/pi);
                nextPeak=abs(u0)*exp(-zeta*wn*n*pi/wd);
                assert(nextPeak<=band*(1+1e-10));
                assert(ts<=tEnvelope+1e-10);
            end
        end
    end
end
% The normalized sketch must be independent of illustrative amplitude.
t=linspace(0,10,101); phi=.5; wn=1; zeta=.2;
wd=wn*sqrt(1-zeta^2);
for C=[.2 1 3]
    u0=C*sin(phi); v0=C*(wd*cos(phi)-zeta*wn*sin(phi));
    actual=hw01_free(t,wn,zeta,u0,v0)/C;
    expected=exp(-zeta*wn*t).*sin(wd*t+phi);
    assert(max(abs(actual-expected))<1e-12);
end
fprintf('Verified free responses against matrix exponentials.\n');
fprintf('Verified 40 settling cases and amplitude-independent normalization.\n');
end
