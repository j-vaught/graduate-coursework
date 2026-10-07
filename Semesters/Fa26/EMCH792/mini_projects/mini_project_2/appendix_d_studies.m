function studies = appendix_d_studies()
% Nonlinear recovery boundary, Gaussian widths, and equal-RMS comparisons.
project_dir = fileparts(mfilename('fullpath'));
previous = pwd; cleanup = onCleanup(@() cd(previous)); cd(project_dir);
model = 'inverted_pendulum_controlled'; load_system(model);
set_param(model, 'StopTime', '30', 'MaxStep', '0.005', 'RelTol', '1e-7', 'AbsTol', '1e-9');
model_cleanup = onCleanup(@() close_model(model));
[K, ~] = design_controller(2, 0.5, 1, 0.01, 9.81);
time = (0:0.002:30)'; seeds = 79202:79221;
bounds = [2.5 5 7.5 10]; widths = [0.05 0.1 0.2]; rate = 50;
set_param([model '/Base disturbance'], 'Interpolate', 'on');
set_param(model, 'FastRestart', 'on');
release = struct([]); histories = struct([]);
for angle = 20:30
    [record, history] = run_case(model, K, angle, [0 0;30 0], 0);
    record.initial_angle_deg = angle;
    if isempty(release), release = record; histories = history;
    else, release(end+1) = record; histories(end+1) = history; end
end
success = find([release.recovered], 1, 'last');
low = release(success).initial_angle_deg; high = release(success+1).initial_angle_deg;
for angle = low+0.1:0.1:high-0.05
    [record, history] = run_case(model, K, angle, [0 0;30 0], 0);
    record.initial_angle_deg = angle; release(end+1) = record; histories(end+1) = history;
end
[~, order] = sort([release.initial_angle_deg]); release = release(order); histories = histories(order);
success = find([release.recovered], 1, 'last');
studies.release = release;
studies.boundary_angles_deg = [release(success).initial_angle_deg release(success+1).initial_angle_deg];
studies.boundary_runs = histories([success success+1]);
fprintf('Release boundary %.1f to %.1f degrees.\n', studies.boundary_angles_deg);
records = struct([]);
for width = widths
    for bound = bounds
        for seed = seeds
            target = random_target(seed, bound, time);
            force = shape_force(target, time, width, rate);
            [record, ~] = run_case(model, K, 0, [time force], rms_force(time, force, false));
            record.seed = seed; record.bound_N = bound; record.sigma_s = width;
            if isempty(records), records = record; else, records(end+1) = record; end
        end
        fprintf('Gaussian width %.2f s, bound %.1f N complete.\n', width, bound);
    end
end
studies.width_trials = records;
summary = struct([]);
for width = widths
    for bound = bounds
        group = records([records.sigma_s] == width & [records.bound_N] == bound);
        balanced = group([group.balanced]);
        item = struct('sigma_s', width, 'bound_N', bound, ...
            'balanced_count', numel(balanced), 'count', numel(group), ...
            'median_angle_rms_deg', median([balanced.rms_angle_deg]), ...
            'median_peak_x_m', median([balanced.peak_x_m]), ...
            'median_force_rms_N', median([group.force_rms_N]));
        if isempty(summary), summary = item; else, summary(end+1) = item; end
    end
end
studies.width_summary = summary;
set_param(model, 'FastRestart', 'off');
matched = struct([]); matched_runs = struct([]); target_rms = 2;
for mode = 1:2
    if mode == 1, interpolation = 'off'; else, interpolation = 'on'; end
    set_param([model '/Base disturbance'], 'Interpolate', interpolation);
    set_param(model, 'FastRestart', 'on');
    for seed = seeds
        target = random_target(seed, 10, time);
        if mode == 1, force = target; else, force = shape_force(target, time, 0.1, rate); end
        factor = target_rms/rms_force(time, force, mode == 1);
        force = factor*force;
        if factor > 1, error('Equal-RMS level requires scaling upward.'); end
        [record, history] = run_case(model, K, 0, [time force], rms_force(time, force, mode == 1));
        record.seed = seed; record.mode = mode;
        record.peak_force_N = max(abs(force));
        if mode == 1, record.max_rate_N_s = NaN;
        else, record.max_rate_N_s = max(abs(diff(force)))/0.002; end
        if isempty(matched), matched = record; else, matched(end+1) = record; end
        if seed == seeds(1)
            history.force_N = interp1(time, force, history.time_s, 'linear');
            if isempty(matched_runs), matched_runs = history;
            else, matched_runs(mode) = history; end
        end
    end
    set_param(model, 'FastRestart', 'off');
end
studies.matched_trials = matched; studies.matched_runs = matched_runs;
for mode = 1:2
    group = matched([matched.mode] == mode);
    studies.matched_summary(mode) = struct('mode', mode, ...
        'balanced_count', sum([group.balanced]), 'count', numel(group), ...
        'median_angle_rms_deg', median([group.rms_angle_deg]), ...
        'median_peak_x_m', median([group.peak_x_m]), ...
        'median_saturation_percent', median([group.saturation_percent]), ...
        'median_force_rms_N', median([group.force_rms_N]), ...
        'maximum_peak_force_N', max([group.peak_force_N]), ...
        'maximum_rate_N_s', max([group.max_rate_N_s]));
end
studies.seeds = seeds; studies.duration_s = 30; studies.profile_step_s = 0.002;
studies.analysis_step_s = 0.02; studies.target_rms_N = target_rms;
fid = fopen('appendix_d_studies.json','w'); file_cleanup = onCleanup(@() fclose(fid));
fprintf(fid,'%s\n',jsonencode(studies,'PrettyPrint',true));
disp('Appendix D studies saved.');
end

function target = random_target(seed, bound, time)
rng(seed,'twister'); unit = 2*rand(302,1)-1;
target = bound*unit(floor(time/0.1+1e-8)+1);
end

function force = shape_force(target, time, sigma, rate)
dt = time(2)-time(1); radius = ceil(3*sigma/dt);
weights = exp(-0.5*((-radius:radius)'*dt/sigma).^2);
weights = weights/sum(weights);
padded = [repmat(target(1),radius,1);target;repmat(target(end),radius,1)];
average = conv(padded,weights,'valid'); force = zeros(size(time));
for j=2:numel(time)
    force(j)=force(j-1)+min(max(average(j)-force(j-1),-rate*dt),rate*dt);
end
end

function value = rms_force(time,force,held)
if held, value=sqrt(sum(diff(time).*force(1:end-1).^2)/time(end));
else, value=sqrt(trapz(time,force.^2)/time(end)); end
end

function [record,history] = run_case(model,K,angle,disturbance,force_rms)
input=Simulink.SimulationInput(model);
input=input.setVariable('disturbance_signal',disturbance);
input=input.setBlockParameter([model '/Nonlinear plant/Angle'],'InitialCondition',num2str(deg2rad(angle),17));
output=sim(input); time=(0:0.02:30)';
state=sample_signal(output.get('state_log'),time);
requested=-state*K'; applied=sample_signal(output.get('force_command'),time);
theta=rad2deg(state(:,3)); fall=find(abs(theta)>=90,1);
if isempty(fall), last=numel(time); failure_time=NaN; else, last=fall; failure_time=time(fall); end
recovered=isempty(fall) && abs(theta(end))<2 && sqrt(mean(theta(time>=28).^2))<2;
record=struct('balanced',isempty(fall),'recovered',recovered, ...
    'rms_angle_deg',sqrt(mean(theta.^2)),'peak_x_m',max(abs(state(:,1))), ...
    'peak_x_before_fall_m',max(abs(state(1:last,1))), ...
    'saturation_percent',100*mean(abs(applied)>=10-1e-6), ...
    'saturation_before_fall_s',trapz(time(1:last),double(abs(applied(1:last))>=10-1e-6)), ...
    'failure_time_s',failure_time,'force_rms_N',force_rms);
history=struct('time_s',time(1:last)', 'theta_deg',theta(1:last)', ...
    'x_m',state(1:last,1)', 'requested_N',requested(1:last)', ...
    'applied_N',applied(1:last)', 'initial_angle_deg',angle);
end

function values=sample_signal(signal,time)
[t,index]=unique(double(signal.Time(:)),'stable');
v=reshape(double(signal.Data),numel(signal.Time),[]);
values=interp1(t,v(index,: ),time,'linear');
end

function close_model(model)
set_param(model,'FastRestart','off'); close_system(model,0);
cache=fullfile(fileparts(mfilename('fullpath')),[model '.slxc']);
if isfile(cache),delete(cache);end
end
