function result = illustrative_model()
% Reproduce the deterministic target-power illustration from config.json.
% Results are written below tmp/matlab and do not replace the Node outputs.

root = fileparts(fileparts(mfilename('fullpath')));
cfg = jsondecode(fileread(fullfile(root, 'data', 'config.json')));
rad = pi / 180;
tau = 2 * pi;

k = (tau * cfg.wave_frequency_hz)^2 / cfg.gravity_m_s2;
kd = k * [cos(cfg.wave_heading_deg * rad), sin(cfg.wave_heading_deg * rad)];

wave = @(x,y,t) cfg.wave_amplitude_m .* cos(kd(1).*x + kd(2).*y - tau.*cfg.wave_frequency_hz.*t);
natural = @(f,fn,zeta) struct('gain', 1 ./ hypot(1-(f./fn).^2, 2.*zeta.*f./fn), ...
    'lag', atan2(2.*zeta.*f./fn, 1-(f./fn).^2));

rx = @(a) [1 0 0; 0 cos(a) -sin(a); 0 sin(a) cos(a)];
ry = @(a) [cos(a) 0 sin(a); 0 1 0; -sin(a) 0 cos(a)];

    function s = state(t, pitchScale, phaseOffset)
        f = cfg.wave_frequency_hz;
        pr = natural(f, cfg.vessel_pitch_natural_hz, cfg.vessel_pitch_damping);
        hr = natural(f, cfg.vessel_heave_natural_hz, cfg.vessel_heave_damping);
        th = natural(f, cfg.target_heave_natural_hz, cfg.target_heave_damping);
        pitch = cfg.static_pitch_deg*rad*pitchScale*pr.gain .* ...
            cos(tau*f*t-pr.lag+phaseOffset);
        roll = cfg.roll_to_pitch_ratio*cfg.static_pitch_deg*rad*pitchScale*pr.gain .* ...
            cos(tau*f*t-pr.lag+cfg.roll_phase_deg*rad+phaseOffset);
        heave = cfg.wave_amplitude_m*hr.gain .* cos(-tau*f*t+hr.lag);
        targetHeave = cfg.wave_amplitude_m*th.gain .* ...
            cos(kd(1)*cfg.target_range_m-tau*f*t+th.lag);
        R = ry(pitch) * rx(roll);
        reference = [0; 0; cfg.radar_reference_height_m-cfg.lever_arm_m(3)+heave];
        origin = reference + R*cfg.lever_arm_m(:);
        target = [cfg.target_range_m; 0; cfg.target_reference_height_m+targetHeave];
        s = struct('pitch',pitch,'roll',roll,'heave',heave,'targetHeave',targetHeave, ...
            'rotation',R,'origin',origin,'target',target);
    end

nominalOrigin = [cfg.lever_arm_m(1); 0; cfg.radar_reference_height_m];
identityR = eye(3);
    function [p,epsilon] = beamPower(origin,target,R,beta)
        v = R'*(target-origin);
        epsilon = atan2(v(3), hypot(v(1),v(2)));
        p = exp(-4*log(2)*(epsilon/(beta*rad))^2);
    end
    function d = diffraction(origin,target,t,samples)
        v = target-origin; range = norm(v); maxNu = -Inf; minClearance = Inf;
        for jj = 1:(samples-1)
            rr = jj/samples; p = origin + rr*v;
            h = wave(p(1),p(2),t)-p(3);
            minClearance = min(minClearance,-h);
            nu = h*sqrt(2/(cfg.radio_wavelength_m*range*rr*(1-rr)));
            maxNu = max(maxNu,nu);
        end
        if maxNu <= -0.78, lossDb = 0;
        else, lossDb = 6.9 + 20*log10(hypot(maxNu-0.1,1)+maxNu-0.1); end
        d = struct('power',10^(-lossDb/10),'maxNu',maxNu, ...
            'minClearance',minClearance,'lossDb',lossDb);
    end
    function s = sample(t,pitchScale,beta,samples,phaseOffset)
        st = state(t,pitchScale,phaseOffset);
        [b,beamAngle] = beamPower(st.origin,st.target,st.rotation,beta);
        [bn,~] = beamPower(nominalOrigin,st.target,identityR,beta);
        g = diffraction(st.origin,st.target,t,samples);
        gn = diffraction(nominalOrigin,st.target,t,samples);
        factors = [bn^2, b^2, (bn*gn.power)^2, (b*g.power)^2];
        s = st; s.beam=b; s.beamAngle=beamAngle/rad; s.transmission=g.power;
        s.clearance=g.minClearance; s.maxNu=g.maxNu; s.factors=factors;
    end
    function q = reconstruct(rho,alpha,origin,R,planeHeight)
        a = R*[cos(alpha);sin(alpha);0]; b = R*[0;0;1]; L = hypot(a(3),b(3));
        qv = (planeHeight-origin(3))/(rho*L);
        if abs(qv)>1, q=[]; return; end
        epsilon = asin(qv)-atan2(a(3),b(3));
        q = origin+rho*(cos(epsilon)*a+sin(epsilon)*b);
    end

n = round(cfg.time_duration_s/cfg.time_step_s)+1;
tvec = (0:n-1)'*cfg.time_step_s;
trace = struct('t',tvec,'waveAtVessel',zeros(n,1),'targetHeight',zeros(n,1), ...
    'pitch',zeros(n,1),'roll',zeros(n,1),'beam',zeros(n,1),'transmission',zeros(n,1), ...
    'referenceDb',zeros(n,1),'motionDb',zeros(n,1),'waveDb',zeros(n,1), ...
    'coupledDb',zeros(n,1),'midpointError',zeros(n,1));
inverseError = 0; minExposure = Inf;
for ii = 1:n
    t=tvec(ii); s=sample(t,1,cfg.vertical_beamwidth_deg,cfg.wave_path_samples,0);
    v=s.rotation'*(s.target-s.origin); rho=norm(v); alpha=atan2(v(2),v(1));
    p=reconstruct(rho,alpha,s.origin,s.rotation,s.target(3)); inverseError=max(inverseError,norm(p-s.target));
    sm=state(round(t/cfg.scan_period_s)*cfg.scan_period_s,1,0);
    pm=reconstruct(rho,alpha,sm.origin,sm.rotation,s.target(3));
    trace.midpointError(ii)=hypot(pm(1)-s.target(1),pm(2)-s.target(2));
    trace.waveAtVessel(ii)=wave(0,0,t); trace.targetHeight(ii)=s.target(3);
    trace.pitch(ii)=s.pitch/rad; trace.roll(ii)=s.roll/rad; trace.beam(ii)=s.beam; trace.transmission(ii)=s.transmission;
    db=cfg.baseline_target_snr_db+10*log10(max(1e-12,s.factors));
    trace.referenceDb(ii)=db(1); trace.motionDb(ii)=db(2); trace.waveDb(ii)=db(3); trace.coupledDb(ii)=db(4);
    minExposure=min(minExposure,s.target(3)-wave(s.target(1),s.target(2),t));
end

keys = {'reference','motion','wave','coupled'};
    function av = availability(pitchScale,beta,samples,phaseOffset)
        counts=zeros(1,4);
        for jj=0:(cfg.phase_samples-1)
            s=sample(jj/(cfg.phase_samples*cfg.wave_frequency_hz),pitchScale,beta,samples,phaseOffset);
            counts=counts+(cfg.baseline_target_snr_db+10*log10(max(1e-12,s.factors)) >= cfg.power_threshold_snr_db);
        end
        av=counts/cfg.phase_samples;
    end

defaultAvailability=availability(1,cfg.vertical_beamwidth_deg,cfg.wave_path_samples,0);
refinedAvailability=availability(1,cfg.vertical_beamwidth_deg,cfg.wave_path_samples*2,0);
amplitudeSweep=struct('staticPitch',zeros(31,1),'reference',zeros(31,1),'motion',zeros(31,1),'wave',zeros(31,1),'coupled',zeros(31,1));
for ii=0:30
    amplitudeSweep.staticPitch(ii+1)=ii*0.1;
    av=availability((ii*0.1)/cfg.static_pitch_deg,cfg.vertical_beamwidth_deg,cfg.wave_path_samples,0);
    amplitudeSweep.reference(ii+1)=av(1); amplitudeSweep.motion(ii+1)=av(2); amplitudeSweep.wave(ii+1)=av(3); amplitudeSweep.coupled(ii+1)=av(4);
end
beamSweep=struct('beamwidth',zeros(25,1),'motion',zeros(25,1),'coupled',zeros(25,1));
for ii=0:24
    beamSweep.beamwidth(ii+1)=2+ii*0.5;
    av=availability(1,beamSweep.beamwidth(ii+1),cfg.wave_path_samples,0);
    beamSweep.motion(ii+1)=av(2); beamSweep.coupled(ii+1)=av(4);
end
phase=zeros(37,4); phaseProduct=zeros(37,1); offsets=(-180:10:180)';
for ii=1:37, phase(ii,1:4)=availability(1,cfg.vertical_beamwidth_deg,cfg.wave_path_samples,offsets(ii)*rad); phaseProduct(ii)=phase(ii,2)*phase(ii,3); end
pitchResponse=natural(cfg.wave_frequency_hz,cfg.vessel_pitch_natural_hz,cfg.vessel_pitch_damping);
finiteOK=all(isfinite([trace.t;trace.pitch;trace.beam;trace.transmission;trace.coupledDb;trace.midpointError]));
refinementDelta=max(abs(defaultAvailability-refinedAvailability));
assert(finiteOK,'Illustrative model produced a non-finite value.');
assert(inverseError<=1e-8,'Known-plane inverse consistency check failed.');
assert(minExposure>0,'Target exposure check failed.');
assert(refinementDelta<=0.025,'Path refinement check failed.');
checks=struct('status',cfg.status,'waveWavelengthM',tau/k,'waveSteepness',k*cfg.wave_amplitude_m, ...
    'pitchGain',pitchResponse.gain,'pitchAmplitudeDeg',cfg.static_pitch_deg*pitchResponse.gain, ...
    'targetMinimumExposureM',minExposure,'inverseConsistencyMaxErrorM',inverseError, ...
    'availability',struct('reference',defaultAvailability(1),'motion',defaultAvailability(2),'wave',defaultAvailability(3),'coupled',defaultAvailability(4)), ...
    'phaseCoupledMinimum',min(phase(:,4)),'phaseCoupledMaximum',max(phase(:,4)), ...
    'phaseLargestProductDifference',max(abs(phase(:,4)-phaseProduct)), ...
    'refinedAvailability',struct('reference',refinedAvailability(1),'motion',refinedAvailability(2),'wave',refinedAvailability(3),'coupled',refinedAvailability(4)), ...
    'pathRefinementFractionDelta',refinementDelta, ...
    'midpoint',struct('maxErrorM',max(trace.midpointError),'medianErrorM',median(trace.midpointError)), ...
    'timeSamples',n,'phaseSamples',cfg.phase_samples);

result=struct('config',cfg,'trace',trace,'checks',checks,'amplitudeSweep',amplitudeSweep,'beamSweep',beamSweep,'phaseSweep',struct('offsetDeg',offsets,'motion',phase(:,2),'wave',phase(:,3),'coupled',phase(:,4),'independentProduct',phaseProduct));
outdir=fullfile(root,'tmp','matlab'); if ~exist(outdir,'dir'), mkdir(outdir); end
fid=fopen(fullfile(outdir,'illustrative_results.json'),'w'); fwrite(fid,jsonencode(result),'char'); fclose(fid);
end
