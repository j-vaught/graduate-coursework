function build_controlled_model(K, force_limit)
% Build a readable controller around the inherited Mini Project 1 plant.
% The nonlinear equations and four integrators are copied into one
% subsystem. Only the feedback loop and logging remain at the top level.

arguments
    K (1, 4) double
    force_limit (1, 1) double {mustBePositive}
end

project_dir = fileparts(mfilename('fullpath'));
previous_dir = pwd;
cleanup = onCleanup(@() cd(previous_dir));
cd(project_dir);

source = 'inverted_pendulum_simulink';
model = 'inverted_pendulum_controlled';
load_system(source);
if bdIsLoaded(model)
    close_system(model, 0);
end
new_system(model);
set_param(model, 'Solver', 'ode45', 'MaxStep', '0.01', ...
    'StopTime', '12', 'SaveTime', 'off', 'SaveOutput', 'off');

plant = [model '/Nonlinear plant'];
add_block('simulink/Ports & Subsystems/Subsystem', plant, ...
    'Position', [460 200 710 320], 'ContentPreviewEnabled', 'off');
delete_line(plant, 'In1/1', 'Out1/1');
set_param([plant '/In1'], 'Name', 'Cart force', ...
    'Position', [30 415 60 435]);
set_param([plant '/Out1'], 'Name', 'State vector', ...
    'Position', [950 235 980 255]);

% Copy the actual Mini Project 1 nonlinear block and its four integrators.
add_block([source '/Nonlinear Equations of Motion'], ...
    [plant '/Nonlinear acceleration'], ...
    'Position', [270 145 500 355]);
add_block([source '/Integrate theta accel'], ...
    [plant '/Angular velocity'], 'Position', [600 170 640 210]);
add_block([source '/Integrate theta velocity'], ...
    [plant '/Angle'], 'Position', [725 170 765 210]);
add_block([source '/Integrate x acceleration'], ...
    [plant '/Cart velocity'], 'Position', [600 290 640 330]);
add_block([source '/Integrate x velocity'], ...
    [plant '/Cart position'], 'Position', [725 290 765 330]);
set_param([plant '/Angle'], 'InitialCondition', '0');

parameter_names = {'M', 'm', 'ell', 'c_theta', 'g'};
parameter_y = [95 155 215 275 335];
for j = 1:numel(parameter_names)
    name = parameter_names{j};
    add_block([source '/' name], [plant '/' name], ...
        'Position', [45 parameter_y(j) 115 parameter_y(j)+32]);
end
close_system(source, 0);

% The copied MATLAB Function gains an eighth input, the total cart force.
root = sfroot;
chart = root.find('-isa', 'Stateflow.EMChart', ...
    'Path', [plant '/Nonlinear acceleration']);
assert(numel(chart) == 1, 'The copied nonlinear equations were not found.');
chart.Script = fileread(fullfile(project_dir, 'controlled_accelerations.m'));
set_param([plant '/Nonlinear acceleration'], 'ShowName', 'off');

% State order has the requested external input order theta, theta_dot,
% x_dot, x. Its internal Mux restores the controller state order
% [x; x_dot; theta; theta_dot].
order = [plant '/State order'];
add_block('simulink/Ports & Subsystems/Subsystem', order, ...
    'Position', [835 170 910 330], 'ContentPreviewEnabled', 'off');
delete_line(order, 'In1/1', 'Out1/1');
set_param([order '/In1'], 'Name', 'theta', 'Position', [30 35 60 55]);
set_param([order '/Out1'], 'Name', 'state', 'Position', [260 115 290 135]);
input_names = {'theta dot', 'x dot', 'x'};
input_y = [85 135 185];
for j = 1:3
    add_block('simulink/Sources/In1', [order '/' input_names{j}], ...
        'Position', [30 input_y(j) 60 input_y(j)+20], 'Port', num2str(j+1));
end
add_block('simulink/Signal Routing/Mux', [order '/State vector'], ...
    'Inputs', '4', 'Position', [190 80 195 170]);
connect(order, 'x/1', 'State vector/1');
connect(order, 'x dot/1', 'State vector/2');
connect(order, 'theta/1', 'State vector/3');
connect(order, 'theta dot/1', 'State vector/4');
connect(order, 'State vector/1', 'state/1');
port_labels = sprintf(['port_label(''input'',1,''theta'');' ...
    'port_label(''input'',2,''theta dot'');' ...
    'port_label(''input'',3,''x dot'');' ...
    'port_label(''input'',4,''x'');' ...
    'port_label(''output'',1,''state'');']);
set_param(order, 'Mask', 'on', 'MaskDisplay', port_labels);
connect(plant, 'M/1', 'Nonlinear acceleration/3');
connect(plant, 'm/1', 'Nonlinear acceleration/4');
connect(plant, 'ell/1', 'Nonlinear acceleration/5');
connect(plant, 'c_theta/1', 'Nonlinear acceleration/6');
connect(plant, 'g/1', 'Nonlinear acceleration/7');
connect(plant, 'Cart force/1', 'Nonlinear acceleration/8');
connect(plant, 'Nonlinear acceleration/1', 'Angular velocity/1');
connect(plant, 'Nonlinear acceleration/2', 'Cart velocity/1');
connect(plant, 'Angular velocity/1', 'Angle/1');
connect(plant, 'Cart velocity/1', 'Cart position/1');
connect(plant, 'Angular velocity/1', 'Nonlinear acceleration/1');
connect(plant, 'Angle/1', 'Nonlinear acceleration/2');
connect(plant, 'Angle/1', 'State order/1');
connect(plant, 'Angular velocity/1', 'State order/2');
connect(plant, 'Cart velocity/1', 'State order/3');
connect(plant, 'Cart position/1', 'State order/4');
connect(plant, 'State order/1', 'State vector/1');

% Restore the original top-level placement and visible logging blocks.
add_block('simulink/Sources/From Workspace', ...
    [model '/Base disturbance'], ...
    'VariableName', 'disturbance_signal', 'Interpolate', 'off', ...
    'OutputAfterFinalValue', 'Holding final value', ...
    'Position', [70 105 225 145]);
add_block('simulink/Math Operations/Sum', [model '/Cart force'], ...
    'Inputs', '++', 'ShowName', 'off', ...
    'Position', [315 240 345 290]);
add_block('simulink/Math Operations/Gain', [model '/State feedback'], ...
    'Gain', mat2str(-K, 16), 'Multiplication', 'Matrix(K*u)', ...
    'Position', [805 220 940 280]);
add_block('simulink/Discontinuities/Saturation', ...
    [model '/Actuator limit'], ...
    'UpperLimit', num2str(force_limit, 17), ...
    'LowerLimit', num2str(-force_limit, 17), ...
    'Position', [1015 230 1090 270]);
log_blocks = {'State log', 'Command log', 'Disturbance log', 'Total force log'};
log_variables = {'state_log', 'force_command', 'base_disturbance', 'force_total'};
log_positions = {[785 75 965 115], [1160 135 1340 175], ...
    [70 355 250 395], [375 75 555 115]};
for j = 1:numel(log_blocks)
    add_block('simulink/Sinks/To Workspace', [model '/' log_blocks{j}], ...
        'VariableName', log_variables{j}, 'SaveFormat', 'Timeseries', ...
        'Position', log_positions{j});
end

connect(model, 'Base disturbance/1', 'Cart force/2');
connect(model, 'Cart force/1', 'Nonlinear plant/1');
connect(model, 'Nonlinear plant/1', 'State feedback/1');
connect(model, 'State feedback/1', 'Actuator limit/1');
connect(model, 'Actuator limit/1', 'Cart force/1');
connect(model, 'Nonlinear plant/1', 'State log/1');
connect(model, 'Actuator limit/1', 'Command log/1');
connect(model, 'Base disturbance/1', 'Disturbance log/1');
connect(model, 'Cart force/1', 'Total force log/1');
set_param(plant, 'ContentPreviewEnabled', 'off');

save_system(model, fullfile(project_dir, [model '.slx']));
close_system(model, 0);
end

function connect(system, source_port, destination_port)
% Auto-routing keeps the editable model aligned after block movement.
add_line(system, source_port, destination_port, 'autorouting', 'on');
end
