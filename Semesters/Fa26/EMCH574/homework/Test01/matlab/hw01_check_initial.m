function hw01_check_initial(wn,zeta,u0,v0)
% Verify the specified displacement and velocity, before plotting.
cfg = hw01_settings();
[u,v] = hw01_free(0,wn,zeta,u0,v0);
assert(abs(u-u0)<=cfg.checkTolerance*max(1,abs(u0)));
assert(abs(v-v0)<=cfg.checkTolerance*max(1,abs(v0)));
end
