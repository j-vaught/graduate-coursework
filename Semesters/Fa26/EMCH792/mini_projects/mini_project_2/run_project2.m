function results = run_project2()
% Rebuild and test the nonlinear, force-controlled Mini Project 1 model.
% Run this file from MATLAB. All random inputs use a recorded fixed seed.

project_dir = fileparts(mfilename('fullpath'));
previous_dir = pwd;
cleanup = onCleanup(@() cd(previous_dir));
cd(project_dir);

% The state is z = [cart position; cart velocity; upright angle;
% angular velocity]. Positive F pushes the cart toward positive x.
M = 2.0; m = 0.5; ell = 1.0; c_theta = 0.01; g = 9.81;
force_limit = 10.0;
[K, design] = design_controller(M, m, ell, c_theta, g);
A = design.A;
compare_models();
build_controlled_model(K, force_limit);
model = 'inverted_pendulum_controlled';

% Compare unforced linear and nonlinear models while near upright.
comparison_time = (0:0.002:0.5)';
initial_state = [0; 0; deg2rad(5); 0];
options = odeset('RelTol', 1e-10, 'AbsTol', 1e-12, 'MaxStep', 0.002);
[~, linear_state] = ode45(@(~, z) A*z, comparison_time, initial_state, options);
[~, nonlinear_state] = ode45(@(~, z) nonlinear_derivative( ...
    z, M, m, ell, c_theta, g), comparison_time, initial_state, options);
comparison = struct('time_s', comparison_time', ...
    'linear_x_m', linear_state(:, 1)', ...
    'nonlinear_x_m', nonlinear_state(:, 1)', ...
    'linear_theta_deg', rad2deg(linear_state(:, 3))', ...
    'nonlinear_theta_deg', rad2deg(nonlinear_state(:, 3))');
comparison_metrics = struct( ...
    'duration_s', comparison_time(end), 'initial_angle_deg', 5, ...
    'max_x_difference_m', max(abs(linear_state(:, 1)-nonlinear_state(:, 1))), ...
    'max_angle_difference_deg', max(abs(rad2deg( ...
        linear_state(:, 3)-nonlinear_state(:, 3)))));
assert(comparison_metrics.max_angle_difference_deg < 0.5, ...
    'The near-upright model comparison differs by more than 0.5 degrees.');

% A bounded, zero-order-held horizontal force excites the cart base.
% The same realization is rescaled in the stress test for a fair comparison.
seed = 79202;
rng(seed, 'twister');
stop_time = 30.0;
% Keep one sample beyond the simulation stop so zero-order hold never
% requires extrapolation at the final solver step.
disturbance_time = (0:0.1:(stop_time + 0.1))';
unit_random = 2*rand(size(disturbance_time)) - 1;
zero_disturbance = [disturbance_time zeros(size(disturbance_time))];
base_disturbance = [disturbance_time 2.5*unit_random];

perturbation = simulate_case(model, deg2rad(5), zero_disturbance, stop_time);
random_test = simulate_case(model, 0, base_disturbance, stop_time);

% Additional tests show where the finite-force controller loses margin.
angle_grid_deg = [10 20 30 45 60];
angle_stress = repmat(struct(), numel(angle_grid_deg), 1);
for j = 1:numel(angle_grid_deg)
    run = simulate_case(model, deg2rad(angle_grid_deg(j)), ...
        zero_disturbance, stop_time);
    angle_stress(j).initial_angle_deg = angle_grid_deg(j);
    angle_stress(j).metrics = response_metrics(run, force_limit);
    angle_stress(j).response = run;
end

force_grid_N = [2.5 5 7.5 10];
force_stress = repmat(struct(), numel(force_grid_N), 1);
for j = 1:numel(force_grid_N)
    disturbance = [disturbance_time force_grid_N(j)*unit_random];
    run = simulate_case(model, 0, disturbance, stop_time);
    force_stress(j).amplitude_N = force_grid_N(j);
    force_stress(j).metrics = response_metrics(run, force_limit);
    force_stress(j).response = run;
end

% Verify the linear closed-loop time response as well as its pole signs.
linear_time = (0:0.02:stop_time)';
[~, stable_state] = ode45(@(~, z) (A-design.B*K)*z, ...
    linear_time, initial_state, options);
linear_closed_loop = struct('time_s', linear_time', ...
    'x_m', stable_state(:, 1)', 'theta_deg', rad2deg(stable_state(:, 3))');
assert(norm(stable_state(end, :)) < 1e-7, ...
    'The linear closed-loop response has not returned to equilibrium.');

results.parameters = struct('M_kg', M, 'm_kg', m, 'ell_m', ell, ...
    'c_theta_Nms_rad', c_theta, 'g_m_s2', g, 'force_limit_N', force_limit);
results.design = design;
results.model_comparison = comparison_metrics;
results.simulation = struct('duration_s', stop_time, 'max_step_s', 0.01, ...
    'analysis_step_s', 0.02);
results.design.linear_final_state_norm = norm(stable_state(end, :));
results.disturbance = struct('seed', seed, 'sample_period_s', 0.1, ...
    'nominal_amplitude_N', 2.5, 'time_s', disturbance_time, ...
    'force_N', base_disturbance(:, 2));
results.perturbation = struct('initial_angle_deg', 5, ...
    'metrics', response_metrics(perturbation, force_limit), ...
    'response', perturbation);
results.random_test = struct('metrics', ...
    response_metrics(random_test, force_limit), 'response', random_test);
results.angle_stress = angle_stress;
results.force_stress = force_stress;

% Export the JSON inputs required to compile the Typst report.
angle_runs = struct('initial_angle_deg', 5, 'response', plot_sample(perturbation));
for j = 1:numel(angle_stress)
    angle_runs(j+1).initial_angle_deg = angle_stress(j).initial_angle_deg;
    angle_runs(j+1).response = plot_sample(angle_stress(j).response);
end
force_runs = repmat(struct(), numel(force_stress), 1);
for j = 1:numel(force_stress)
    force_runs(j).amplitude_N = force_stress(j).amplitude_N;
    force_runs(j).response = plot_sample(force_stress(j).response);
end
plot_data = struct('perturbation', plot_sample(perturbation), ...
    'random_test', plot_sample(random_test), ...
    'angle_runs', angle_runs, 'force_runs', force_runs, ...
    'comparison', comparison, 'linear_closed_loop', linear_closed_loop, ...
    'disturbance_time_s', disturbance_time', ...
    'unit_disturbance', unit_random', 'disturbance_step_s', 0.1);
write_json(fullfile(project_dir, 'plot_data.json'), plot_data);
summary = rmfield(results, {'perturbation', 'random_test'});
summary.angle_stress = rmfield(angle_stress, 'response');
summary.force_stress = rmfield(force_stress, 'response');
summary.perturbation = results.perturbation.metrics;
summary.random_test = results.random_test.metrics;
write_json(fullfile(project_dir, 'metrics.json'), summary);
fprintf('K = [%s]\n', num2str(K, ' %.6f'));
fprintf('Perturbation settling time = %.3f s; peak angle = %.3f deg.\n', ...
    results.perturbation.metrics.settling_time_s, ...
    results.perturbation.metrics.peak_angle_deg);
fprintf('Random-force RMS angle = %.3f deg; peak angle = %.3f deg.\n', ...
    results.random_test.metrics.rms_angle_deg, ...
    results.random_test.metrics.peak_angle_deg);
disp('Stress test results were written to metrics.json.');
fprintf('Model comparison: max angle difference = %.6f deg, x difference = %.6f m.\n', ...
    comparison_metrics.max_angle_difference_deg, comparison_metrics.max_x_difference_m);

% Export the actual editable Simulink block diagram for the appendix.
open_system(model);
set_param(model, 'ZoomFactor', 'FitSystem');
print(['-s' model], '-dpng', '-r170', ...
    fullfile(project_dir, 'controlled_model_diagram.png'));
open_system([model '/Nonlinear plant']);
print(['-s' model '/Nonlinear plant'], '-dpng', '-r170', ...
    fullfile(project_dir, 'nonlinear_plant_diagram.png'));
close_system(model, 0);
cache_files = dir(fullfile(project_dir, '*.slxc'));
for j = 1:numel(cache_files)
    delete(fullfile(project_dir, cache_files(j).name));
end
end

function derivative = nonlinear_derivative(z, M, m, ell, c_theta, g)
% Use the same acceleration function as the nonlinear Simulink plant.
[theta_ddot, x_ddot] = controlled_accelerations( ...
    z(4), z(3), M, m, ell, c_theta, g, 0);
derivative = [z(2); x_ddot; z(4); theta_ddot];
end

function response = simulate_case(model, initial_angle_rad, disturbance, stop_time)
% Each simulation uses the same saved model with case-specific inputs.
input = Simulink.SimulationInput(model);
input = input.setVariable('disturbance_signal', disturbance);
input = input.setBlockParameter([model '/Nonlinear plant/Angle'], ...
    'InitialCondition', num2str(initial_angle_rad, 17));
input = input.setModelParameter('StopTime', num2str(stop_time, 17));
output = sim(input);
time = (0:0.02:stop_time)';
response.time_s = time;
state = resample_signal(output.get('state_log'), time);
response.x_m = state(:, 1);
response.x_dot_m_s = state(:, 2);
response.theta_deg = state(:, 3)*180/pi;
response.theta_dot_deg_s = state(:, 4)*180/pi;
response.u_N = resample_signal(output.get('force_command'), time);
response.disturbance_N = resample_signal(output.get('base_disturbance'), time);
response.total_force_N = resample_signal(output.get('force_total'), time);
assert(all(isfinite(response.theta_deg)), 'The angle response is not finite.');
end

function values = resample_signal(signal, time)
% Remove duplicate solver time stamps before interpolation.
[logged_time, indices] = unique(double(signal.Time(:)), 'stable');
logged_values = reshape(double(signal.Data), numel(signal.Time), []);
values = interp1(logged_time, logged_values(indices, :), ...
    time, 'linear', 'extrap');
end

function metrics = response_metrics(response, force_limit)
% Report angle control, cart travel, actuator use, and residual error.
time = response.time_s;
theta = response.theta_deg;
u = response.u_N;
metrics.peak_angle_deg = max(abs(theta));
metrics.rms_angle_deg = sqrt(mean(theta.^2));
metrics.final_angle_deg = theta(end);
metrics.final_2s_rms_angle_deg = sqrt(mean(theta(time >= time(end)-2).^2));
metrics.peak_cart_position_m = max(abs(response.x_m));
metrics.final_cart_position_m = response.x_m(end);
metrics.peak_command_N = max(abs(u));
metrics.saturation_fraction = mean(abs(u) >= force_limit - 1e-6);
metrics.control_effort_N2_s = trapz(time, u.^2);
last_outside = find(abs(theta) > 1, 1, 'last');
if isempty(last_outside)
    metrics.settling_time_s = 0;
elseif last_outside == numel(time)
    metrics.settling_time_s = NaN;
else
    metrics.settling_time_s = time(last_outside + 1);
end
metrics.recovered = abs(theta(end)) < 2 && ...
    metrics.final_2s_rms_angle_deg < 2;
end

function sampled = plot_sample(response)
% Plot data are decimated only after metrics use the full analysis grid.
indices = 1:2:numel(response.time_s);
fields = fieldnames(response);
for j = 1:numel(fields)
    sampled.(fields{j}) = response.(fields{j})(indices)';
end
end

function write_json(filename, value)
fid = fopen(filename, 'w');
assert(fid > 0, 'Could not open %s.', filename);
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '%s\n', jsonencode(value, 'PrettyPrint', true));
end
