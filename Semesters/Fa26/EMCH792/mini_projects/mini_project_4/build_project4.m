function build_project4()
% Build and verify constrained MPC against the unaltered Project 3 LQR.
folder=fileparts(mfilename('fullpath')); cd(folder);
Simulink.fileGenControl('set','CacheFolder',fullfile(tempdir,'emch792-project4-cache'), ...
    'CodeGenFolder',fullfile(tempdir,'emch792-project4-code'),'createDir',true);
prior=fullfile(folder,'..','mini_project_3');
[K,d]=design_lqr_controller(2,0.5,1,0.01,9.81);
Ts=0.05; p=50; m=10;
plant=ss(d.A,d.B,eye(4),zeros(4,1));
controller=mpc(plant,Ts,p,m);
controller.MV.Min=-10; controller.MV.Max=10;
controller.Weights.OutputVariables=[2 sqrt(2) sqrt(300) sqrt(10)];
controller.Weights.ManipulatedVariables=sqrt(0.5);
controller.Weights.ManipulatedVariablesRate=0.1;
% All four physical states are directly available from the simulated plant.
% Remove default unmeasured output disturbances from the augmented state.
setoutdist(controller,'model',ss(zeros(4,1)));
setEstimator(controller,'custom');
source=fullfile(prior,'inverted_pendulum_lqr.slx');
load_system(source); old='inverted_pendulum_lqr'; model='inverted_pendulum_mpc';
save_system(old,fullfile(folder,[model '.slx'])); close_system(old,0); load_system(model);
ws=get_param(model,'ModelWorkspace'); assignin(ws,'mpc_controller',controller);
delete_line(model,'Nonlinear plant/1','State feedback/1');
delete_line(model,'State feedback/1','Actuator limit/1');
delete_block([model '/State feedback']);
load_system('mpclib');
add_block('mpclib/MPC Controller',[model '/MPC Controller'], ...
    'Position',[625 215 695 305],'mpcobj','mpc_controller', ...
    'state_inport','on','return_qpstatus','on','md_inport','off');
add_block('simulink/Sources/Constant',[model '/Upright reference'], ...
    'Value','zeros(4,1)','Position',[570 160 650 190]);
add_block('simulink/Signal Attributes/Signal Specification',[model '/State dimensions'], ...
    'Dimensions','4','Position',[580 220 610 250]);
add_line(model,'Nonlinear plant/1','State dimensions/1','autorouting','on');
add_line(model,'State dimensions/1','MPC Controller/1','autorouting','on');
add_line(model,'Upright reference/1','MPC Controller/2','autorouting','on');
add_line(model,'MPC Controller/1','Actuator limit/1','autorouting','on');
add_block('simulink/Sinks/To Workspace',[model '/Optimizer status'], ...
    'VariableName','qp_status','SaveFormat','Timeseries', ...
    'Position',[740 315 860 345]);
add_line(model,'MPC Controller/2','Optimizer status/1','autorouting','on');
format_project4_layout(model);
save_system(model);
% Simulate unchanged Project 3 first; no saved state in the original is altered.
load_system(source);
lqrout=sim(old); mpcout=sim(model);
results.settings=struct('Ts_s',Ts,'prediction_horizon_steps',p, ...
    'prediction_horizon_s',Ts*p,'control_horizon_steps',m, ...
    'force_limit_N',10,'initial_angle_deg',5,'stop_time_s',30);
results.design=struct('A',d.A,'B',d.B,'lqr_K',K, ...
    'output_weights',controller.Weights.OutputVariables, ...
    'force_weight',controller.Weights.ManipulatedVariables, ...
    'force_rate_weight',controller.Weights.ManipulatedVariablesRate);
results.comparison.lqr=extract_case(lqrout,'LQR');
results.comparison.mpc=extract_case(mpcout,'MPC');
reference=jsondecode(fileread(fullfile(prior,'project3_results.json')));
results.validation.raw_peak_force_N=max(abs(mpcout.force_command.Data(:)));
assert(results.validation.raw_peak_force_N<=10+1e-7);
assert(all(mpcout.qp_status.Data(:)>0));
results.validation.qp_status_min=min(mpcout.qp_status.Data);
results.validation.qp_status_max=max(mpcout.qp_status.Data);
results.validation.lqr_angle_max_difference_deg=max(abs(results.comparison.lqr.theta_deg(:)-reference.comparisons(1).lqr.theta_deg(:)));
results.validation.lqr_force_max_difference_N=max(abs(results.comparison.lqr.u_N(:)-reference.comparisons(1).lqr.u_N(:)));
assert(results.validation.lqr_angle_max_difference_deg<1e-6);
assert(results.validation.lqr_force_max_difference_N<1e-5);
assert(results.comparison.mpc.metrics.peak_force_N<=10+1e-7);
assert(results.comparison.mpc.metrics.recovered);
fid=fopen(fullfile(folder,'project4_results.json'),'w'); c=onCleanup(@()fclose(fid));
fprintf(fid,'%s\n',jsonencode(results,'PrettyPrint',true));
disp(results.comparison.lqr.metrics); disp(results.comparison.mpc.metrics);
close_system(old,0); close_system(model,0);
end

function result=extract_case(output,label)
t=(0:0.02:30)'; z=sample(output.state_log,t,'linear');
if strcmp(label,'LQR'), method='linear'; else, method='previous'; end
u=sample(output.force_command,t,method);
assert(all(isfinite(z),'all') && all(isfinite(u)));
if strcmp(label,'MPC')
    [rawtime,idx]=unique(double(output.force_command.Time(:)),'last');
    rawforce=double(output.force_command.Data(:)); rawforce=rawforce(idx);
    force_effort=sum(diff(rawtime).*rawforce(1:end-1).^2);
else
    force_effort=trapz(t,u.^2);
end
a=z(:,3)*180/pi; outside=find(abs(a)>1 | abs(z(:,1))>.05,1,'last');
recovered=isempty(find(abs(a)>=90,1)) && max(abs(a(t>=28)))<=1 && max(abs(z(t>=28,1)))<=.05;
settling=-1; if recovered, if isempty(outside), settling=0; elseif outside<numel(t), settling=t(outside+1); end, end
result=struct('label',label,'time_s',t','theta_deg',a','x_m',z(:,1)', ...
    'u_N',u','metrics',struct('recovered',recovered,'settling_time_s',settling, ...
    'peak_angle_deg',max(abs(a)),'peak_cart_m',max(abs(z(:,1))), ...
    'peak_force_N',max(abs(double(output.force_command.Data(:)))),'effort_N2_s',force_effort, ...
    'saturation_s',trapz(t,double(abs(u)>=10-1e-6))));
end
function y=sample(signal,t,method)
[tx,idx]=unique(double(signal.Time(:)),'stable');
data=reshape(double(signal.Data),numel(signal.Time),[]);
y=interp1(tx,data(idx,:),t,method,'extrap');
end
