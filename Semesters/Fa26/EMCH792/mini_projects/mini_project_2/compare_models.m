function comparisons = compare_models()
% Compare the exact plant and its upright linearization without feedback.
project_dir = fileparts(mfilename('fullpath'));
M = 2; m = 0.5; ell = 1; c_theta = 0.01; g = 9.81;
[~, design] = design_controller(M, m, ell, c_theta, g);
time = (0:0.002:1)';
sample_times = [0.1 0.25 0.5];
options = odeset('RelTol', 1e-10, 'AbsTol', 1e-12, 'MaxStep', 0.002);
angles = [2 5 10 15 20 25 30];
forces = [0.5 1 2 4 8 16];
for j = 1:numel(angles)
    comparisons.angle_runs(j) = run_case([0; 0; deg2rad(angles(j)); 0], ...
        0, angles(j), time, sample_times, options, design, M, m, ell, c_theta, g);
end
for j = 1:numel(forces)
    comparisons.force_runs(j) = run_case(zeros(4, 1), forces(j), ...
        forces(j), time, sample_times, options, design, M, m, ell, c_theta, g);
end
comparisons.sample_times_s = sample_times;
comparisons.max_step_s = 0.002;
fid = fopen(fullfile(project_dir, 'model_comparisons.json'), 'w');
assert(fid > 0, 'Cannot write comparison data.');
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '%s\n', jsonencode(comparisons, 'PrettyPrint', true));
disp('Uncontrolled model comparisons saved to model_comparisons.json.');
end

function result = run_case(initial, force, input_value, time, sample_times, ...
        options, design, M, m, ell, c_theta, g)
[~, linear] = ode45(@(~, z) design.A*z + design.B*force, time, initial, options);
[~, nonlinear] = ode45(@(~, z) exact_derivative(z, force, ...
    M, m, ell, c_theta, g), time, initial, options);
assert(all(isfinite(linear), 'all') && all(isfinite(nonlinear), 'all'), ...
    'Comparison contains nonfinite states.');
error = abs(linear - nonlinear);
indices = round(sample_times/0.002) + 1;
% Check the integrated linear states against the exact constant-input solution.
augmented = [design.A design.B*force; zeros(1, 5)];
for index = [indices numel(time)]
    exact = expm(augmented*time(index))*[initial; 1];
    assert(norm(linear(index, :)' - exact(1:4), inf) < 1e-7, ...
        'Linear integration differs from the matrix-exponential solution.');
end
result = struct('input_value', input_value, 'time_s', time', ...
    'linear_x_m', linear(:, 1)', 'nonlinear_x_m', nonlinear(:, 1)', ...
    'linear_theta_deg', rad2deg(linear(:, 3))', ...
    'nonlinear_theta_deg', rad2deg(nonlinear(:, 3))', ...
    'x_error_m', error(indices, 1)', ...
    'angle_error_deg', rad2deg(error(indices, 3))');
end

function derivative = exact_derivative(z, force, M, m, ell, c_theta, g)
[theta_ddot, x_ddot] = controlled_accelerations( ...
    z(4), z(3), M, m, ell, c_theta, g, force);
derivative = [z(2); x_ddot; z(4); theta_ddot];
end
