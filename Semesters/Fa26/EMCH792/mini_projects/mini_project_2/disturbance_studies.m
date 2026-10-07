function studies = disturbance_studies()
% Finite-rate disturbance profiles and paired nonlinear Simulink trials.
project_dir = fileparts(mfilename('fullpath'));
previous = pwd;
cleanup = onCleanup(@() cd(previous));
cd(project_dir);
dt = 0.002; time = (0:dt:30)';
tau = 0.1; rate = 50; seeds = 79202:79221; bounds = [2.5 5 7.5 10];
reversal_time = (0:dt:1.5)';
target = -10*ones(size(reversal_time));
target(reversal_time >= 0.5) = 10;
studies.reversal = profiles(reversal_time, target, tau, rate, -10);
for j = 1:4
    f = studies.reversal(j).force_N;
    index = find(reversal_time >= 0.5 & f(:) >= 9, 1);
    studies.reversal(j).transition_95_s = reversal_time(index)-0.5;
end
rng(seeds(1), 'twister');
unit = 2*rand(302, 1)-1;
target = 10*unit(floor(round(time/dt)*dt/0.1+1e-8)+1);
studies.random_profiles = profiles(time, target, tau, rate, 0);
for j = 1:3
    taus = [0.05 0.1 0.2];
    waves = profiles(time, target, taus(j), rate, 0);
    wave = waves(2);
    wave.setting = taus(j);
    studies.tau_sweep(j) = wave;
    rates = [25 50 100];
    waves = profiles(time, target, tau, rates(j), 0);
    wave = waves(3);
    wave.setting = rates(j);
    studies.rate_sweep(j) = wave;
end
model = 'inverted_pendulum_controlled';
load_system(model);
set_param(model, 'StopTime', '30', 'MaxStep', '0.005', ...
    'RelTol', '1e-7', 'AbsTol', '1e-9');
model_cleanup = onCleanup(@() close_model(model));
records = struct([]);
for mode = 1:2
    if mode == 1
        set_param([model '/Base disturbance'], 'Interpolate', 'off');
    else
        set_param([model '/Base disturbance'], 'Interpolate', 'on');
    end
    set_param(model, 'FastRestart', 'on');
    for b = 1:numel(bounds)
        for j = 1:numel(seeds)
            rng(seeds(j), 'twister');
            unit = 2*rand(302, 1)-1;
            target = bounds(b)*unit(floor(round(time/dt)*dt/0.1+1e-8)+1);
            if mode == 1
                disturbance = [(0:0.1:30.1)' bounds(b)*unit];
                force = target;
            else
                waves = profiles(time, target, tau, rate, 0);
                force = waves(4).force_N(:);
                disturbance = [time force];
            end
            input = Simulink.SimulationInput(model);
            input = input.setVariable('disturbance_signal', disturbance);
            input = input.setBlockParameter([model '/Nonlinear plant/Angle'], ...
                'InitialCondition', '0');
            input = input.setModelParameter('StopTime', '30');
            output = sim(input);
            analysis_time = (0:0.02:30)';
            state = sample_signal(output.get('state_log'), analysis_time);
            command = sample_signal(output.get('force_command'), analysis_time);
            angle = rad2deg(state(:, 3));
            record = struct('seed', seeds(j), 'bound_N', bounds(b), ...
                'mode', mode, 'balanced', all(abs(angle) < 90), ...
                'rms_angle_deg', sqrt(mean(angle.^2)), ...
                'peak_angle_deg', max(abs(angle)), ...
                'peak_x_m', max(abs(state(:, 1))), ...
                'saturation_percent', 100*mean(abs(command) >= 10-1e-6), ...
                'force_rms_N', sqrt(trapz(time, force.^2)/30));
            if isempty(records)
                records = record;
            else
                records(end+1) = record;
            end
            if mod(j, 5) == 0
                fprintf('Mode %d, %.1f N, seed %d of 20 complete.\n', mode, bounds(b), j);
            end
            if j == 1 && bounds(b) == 5
                studies.controller_runs(mode) = struct('time_s', analysis_time', ...
                    'theta_deg', angle', 'x_m', state(:, 1)', ...
                    'applied_N', command', 'force_N', force(1:10:end)');
            end
        end
        fprintf('Completed %s disturbance at %.1f N for 20 seeds.\n', ...
            mode_name(mode), bounds(b));
    end
    set_param(model, 'FastRestart', 'off');
end
studies.trials = records;
for b = 1:numel(bounds)
    for mode = 1:2
        group = records([records.bound_N] == bounds(b) & [records.mode] == mode);
        success = group([group.balanced]);
        index = 2*(b-1)+mode;
        if isempty(success)
            median_angle = NaN; median_x = NaN;
        else
            median_angle = median([success.rms_angle_deg]);
            median_x = median([success.peak_x_m]);
        end
        studies.seed_summary(index) = struct('bound_N', bounds(b), ...
            'mode', mode, 'balanced_count', numel(success), 'count', 20, ...
            'median_rms_angle_deg_balanced', median_angle, ...
            'median_peak_x_m_balanced', median_x, ...
            'median_force_rms_N', median([group.force_rms_N]));
    end
end
studies.nominal = records([records.seed] == seeds(1));
studies.tau_s = tau; studies.rate_limit_N_s = rate;
studies.seeds = seeds; studies.profile_step_s = dt;
studies.analysis_step_s = 0.02; studies.max_solver_step_s = 0.005;
fields = {'reversal', 'random_profiles', 'tau_sweep', 'rate_sweep'};
for f = 1:numel(fields)
    for j = 1:numel(studies.(fields{f}))
        wave = studies.(fields{f})(j);
        index = 1:5:numel(wave.time_s);
        wave.time_s = wave.time_s(index);
        wave.force_N = wave.force_N(index);
        wave.rate_N_s = wave.rate_N_s(index);
        studies.(fields{f})(j) = wave;
    end
end
fid = fopen('disturbance_studies.json', 'w');
file_cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '%s\n', jsonencode(studies, 'PrettyPrint', true));
disp('Disturbance shaping and 160 nonlinear trials saved.');
end

function waves = profiles(time, target, tau, rate, initial)
dt = time(2)-time(1);
smooth = zeros(size(time)); limited = smooth; combined = smooth;
smooth(1) = initial; limited(1) = initial; combined(1) = initial;
for i = 2:numel(time)
    smooth(i) = target(i-1)+(smooth(i-1)-target(i-1))*exp(-dt/tau);
    limited(i) = limited(i-1)+min(max(target(i-1)-limited(i-1), -rate*dt), rate*dt);
    combined(i) = combined(i-1)+min(max(smooth(i)-combined(i-1), -rate*dt), rate*dt);
end
forces = [target smooth limited combined];
names = {'Held', 'Smoothed', 'Rate limited', 'Combined'};
for j = 1:4
    force = forces(:, j);
    if j == 1
        derivative = zeros(size(force)); maximum_rate = NaN;
    elseif j == 2
        derivative = (target-force)/tau; maximum_rate = max(abs(derivative));
    else
        derivative = [0; diff(force)/dt]; maximum_rate = max(abs(derivative));
    end
    waves(j) = struct('label', names{j}, 'time_s', time', ...
        'force_N', force', 'rate_N_s', derivative', ...
        'peak_N', max(abs(force)), ...
        'rms_N', sqrt(trapz(time, force.^2)/(time(end)-time(1))), ...
        'max_rate_N_s', maximum_rate);
end
end

function values = sample_signal(signal, time)
[logged_time, indices] = unique(double(signal.Time(:)), 'stable');
logged_values = reshape(double(signal.Data), numel(signal.Time), []);
values = interp1(logged_time, logged_values(indices, :), time, 'linear');
end

function name = mode_name(mode)
if mode == 1
    name = 'held';
else
    name = 'combined';
end
end

function close_model(model)
set_param(model, 'FastRestart', 'off');
close_system(model, 0);
cache = fullfile(fileparts(mfilename('fullpath')), [model '.slxc']);
if isfile(cache)
    delete(cache);
end
end
