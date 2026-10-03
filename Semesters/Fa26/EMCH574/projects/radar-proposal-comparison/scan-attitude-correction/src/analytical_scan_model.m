function checks = analytical_scan_model()
% Reproduce the controlled oscillator and known-plane geometry calculations.
% Author J.C. Vaught. No measured radar data are processed by this function.
% Run from this folder or add it to the MATLAB path. Typst draws the figures.
root = fileparts(fileparts(mfilename('fullpath')));
c = jsondecode(fileread(fullfile(root, 'data', 'config.json')));
u = linspace(c.frequency_ratio_min, c.frequency_ratio_max, c.frequency_ratio_samples);
gain = 1 ./ hypot(1-u.^2, 2*c.damping_ratio*u);
error100 = zeros(size(u));
error300 = zeros(size(u));
coverageNarrow = zeros(size(u));
coverageWide = zeros(size(u));
inverseError = 0;
for k = 1:numel(u)
    mid = pose(0, u(k), c);
    err = zeros(1, numel(c.illustrative_ranges_m));
    seen = zeros(1, numel(c.illustrative_elevation_beamwidths_deg));
    for j = 0:c.azimuths_per_scan-1
        alpha = 2*pi*j/c.azimuths_per_scan;
        t = (j/(c.azimuths_per_scan-1)-0.5)*c.scan_period_s;
        current = pose(t, u(k), c);
        for r = 1:numel(c.illustrative_ranges_m)
            rho = c.illustrative_ranges_m(r);
            truth = point_on_plane(rho, alpha, current);
            estimate = point_on_plane(rho, alpha, mid);
            err(r) = max(err(r), norm(truth.xyz(1:2)-estimate.xyz(1:2)));
            sensor = current.R'*(truth.xyz-current.s);
            angle_error = atan2(sin(atan2(sensor(2), sensor(1))-alpha), ...
                                cos(atan2(sensor(2), sensor(1))-alpha));
            inverseError = max([inverseError, abs(norm(sensor)-rho), ...
                abs(angle_error)*rho, abs(truth.xyz(3))]);
            if r == 1
                for b = 1:numel(seen)
                    if abs(truth.epsilon) <= deg2rad(c.illustrative_elevation_beamwidths_deg(b))/2
                        seen(b) = seen(b)+1;
                    end
                end
            end
        end
    end
    error100(k) = err(1)/c.radar_range_bins_m(1);
    error300(k) = err(2)/c.radar_range_bins_m(2);
    coverageNarrow(k) = seen(1)/c.azimuths_per_scan;
    coverageWide(k) = seen(2)/c.azimuths_per_scan;
end
assert(inverseError < 1e-9, 'Inverse geometry check failed.');
output = struct('config',c,'ratio',u,'gain',gain, ...
    'error100',error100,'error300',error300, ...
    'coverageNarrow',coverageNarrow,'coverageWide',coverageWide);
fid = fopen(fullfile(root,'data','analytical-matlab.json'),'w');
cleanup = onCleanup(@() fclose(fid));
fprintf(fid,'%s\n',jsonencode(output,PrettyPrint=true));
checks = struct('inverse_consistency_max_error',inverseError, ...
    'max_gain',max(gain),'max_error_ratio_100',max(error100), ...
    'max_error_ratio_300',max(error300));
disp(checks)
end

function p = pose(t, u, c)
g = 1/hypot(1-u*u,2*c.damping_ratio*u);
lag = atan2(2*c.damping_ratio*u,1-u*u);
phase = 2*pi*c.natural_frequency_hz*u*t-lag;
pitch = deg2rad(c.static_pitch_deflection_deg)*g*sin(phase);
roll = deg2rad(c.static_pitch_deflection_deg)*g* ...
    c.roll_to_pitch_forcing_ratio*sin(phase+c.roll_phase_offset_rad);
Rx = [1 0 0; 0 cos(roll) -sin(roll); 0 sin(roll) cos(roll)];
Ry = [cos(pitch) 0 sin(pitch); 0 1 0; -sin(pitch) 0 cos(pitch)];
p.R = Ry*Rx;
p.s = [0;0;c.imu_origin_height_m]+p.R*c.imu_to_radar_lever_arm_m(:);
end

function q = point_on_plane(rho, alpha, p)
a = p.R*[cos(alpha);sin(alpha);0];
b = p.R*[0;0;1];
s = -p.s(3)/rho/hypot(a(3),b(3));
assert(abs(s)<=1, 'No intersection with configured plane.');
q.epsilon = asin(s)-atan2(a(3),b(3));
q.xyz = p.s+rho*(cos(q.epsilon)*a+sin(q.epsilon)*b);
end
