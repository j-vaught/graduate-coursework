function studies = controller_studies()
% Linear-plant controller comparisons for Appendix B. No random disturbance.
project_dir = fileparts(mfilename('fullpath'));
[baseline_gain, design] = design_controller(2, 0.5, 1, 0.01, 9.81);
A = design.A; B = design.B;
time = (0:0.01:30)';
options = odeset('RelTol', 1e-10, 'AbsTol', 1e-12, 'MaxStep', 0.005);
initial = [0; 0; deg2rad(5); 0];
studies.baseline = simulate('LQR', A, B, baseline_gain, initial, time, inf, options);
short_time = (0:0.01:1)';
[~, uncontrolled] = ode45(@(~, z) A*z, short_time, initial, options);
studies.uncontrolled = struct('label', 'No feedback', 'time_s', short_time', ...
    'x_m', uncontrolled(:, 1)', 'theta_deg', rad2deg(uncontrolled(:, 3))');
angle_weights = [100 300 900];
force_weights = [0.1 0.5 2];
for j = 1:3
    Q = diag([4 2 angle_weights(j) 10]);
    K = lqr(A, B, Q, 0.5);
    run = simulate(sprintf('q_theta = %g', angle_weights(j)), ...
        A, B, K, initial, time, inf, options);
    run.q_theta = angle_weights(j);
    run.R = 0.5;
    studies.angle_weights(j) = run;
    K = lqr(A, B, design.Q, force_weights(j));
    run = simulate(sprintf('R = %g', force_weights(j)), ...
        A, B, K, initial, time, inf, options);
    run.q_theta = 300;
    run.R = force_weights(j);
    studies.force_weights(j) = run;
end
angles = [5 20];
for j = 1:2
    initial = [0; 0; deg2rad(angles(j)); 0];
    studies.saturation(j).initial_angle_deg = angles(j);
    studies.saturation(j).unlimited = simulate('Unlimited', A, B, ...
        baseline_gain, initial, time, inf, options);
    studies.saturation(j).limited = simulate('Limited to 10 N', A, B, ...
        baseline_gain, initial, time, 10, options);
end
studies.design = design;
studies.duration_s = 30;
studies.analysis_step_s = 0.01;
studies.max_step_s = 0.005;
studies.settling_angle_deg = 1;
studies.settling_position_m = 0.02;
fid = fopen(fullfile(project_dir, 'controller_studies.json'), 'w');
assert(fid > 0, 'Cannot write controller studies.');
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '%s\n', jsonencode(studies, 'PrettyPrint', true));
for run = [studies.angle_weights studies.force_weights]
    fprintf('%s: settling %.2f s, travel %.4f m, peak %.3f N, effort %.3f N^2 s\n', ...
        run.label, run.metrics.settling_time_s, run.metrics.peak_x_m, ...
        run.metrics.peak_requested_N, run.metrics.effort_N2_s);
end
for run = studies.saturation
    fprintf('%g deg: unlimited %.2f s; limited %.2f s; saturation %.3f s\n', ...
        run.initial_angle_deg, run.unlimited.metrics.settling_time_s, ...
        run.limited.metrics.settling_time_s, run.limited.metrics.saturation_duration_s);
end
end

function run = simulate(label, A, B, K, initial, time, limit, options)
assert(all(real(eig(A-B*K)) < 0), 'Unconstrained feedback is unstable.');
[~, state] = ode45(@(~, z) A*z+B*min(max(-K*z, -limit), limit), ...
    time, initial, options);
assert(all(isfinite(state), 'all'), 'Nonfinite response.');
requested = -state*K';
applied = min(max(requested, -limit), limit);
assert(all(abs(applied) <= limit), 'Actuator limit exceeded.');
if isinf(limit)
    exact = expm((A-B*K)*time(end))*initial;
    assert(norm(state(end, :)'-exact, inf) < 1e-7, ...
        'Linear solution differs from matrix exponential.');
end
outside = abs(state(:, 1)) > 0.02 | abs(rad2deg(state(:, 3))) > 1;
last = find(outside, 1, 'last');
settling = NaN;
if isempty(last)
    settling = 0;
elseif last < numel(time)
    settling = time(last+1);
end
metrics = struct('settling_time_s', settling, ...
    'peak_x_m', max(abs(state(:, 1))), ...
    'peak_requested_N', max(abs(requested)), ...
    'peak_applied_N', max(abs(applied)), ...
    'effort_N2_s', trapz(time, applied.^2), ...
    'saturation_duration_s', trapz(time, double(abs(requested) > limit)), ...
    'recovered', ~any(outside(time >= time(end)-2)), ...
    'final_state_norm', norm(state(end, :)));
index = 1:2:numel(time);
run = struct('label', label, 'K', K, 'time_s', time(index)', ...
    'x_m', state(index, 1)', 'theta_deg', rad2deg(state(index, 3))', ...
    'requested_N', requested(index)', 'applied_N', applied(index)', ...
    'metrics', metrics);
end
