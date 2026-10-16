function result = run_pole_revision()
% Update a COPY of the aligned model, then run the two required tests.
folder = fileparts(mfilename('fullpath'));
previous = pwd; cleanup = onCleanup(@() cd(previous)); cd(folder);
Simulink.fileGenControl('set','CacheFolder',fullfile(tempdir,'emch792-pole-cache'), ...
    'CodeGenFolder',fullfile(tempdir,'emch792-pole-code'),'createDir',true);
fprintf('Calculating pole-placement gain.\n');
[K,A,B,poles] = design_pole_controller();
C = ctrb(A,B);
assert(rank(C)==4);
assert(norm(sort(eig(A-B*K))-sort(poles(:)),inf)<1e-8);
assert(norm(K-place(A,B,poles),inf)<1e-8);
model = 'inverted_pendulum_controlled';
fprintf('Loading aligned Simulink model.\n');
load_system(model);
% Preserve every block position, connector, mask, and subsystem.
set_param([model '/State feedback'],'Gain',mat2str(-K,17));
set_param(model,'StopTime','30');
w = get_param(model,'ModelWorkspace');
assignin(w,'disturbance_signal',[0 0;30.1 0]);
set_param([model '/Nonlinear plant/Angle'],'InitialCondition','5*pi/180');
save_system(model);
rng(79202,'twister'); t=(0:0.1:30.1)'; unit=2*rand(size(t))-1;
angles=[5 10 20 30]; bounds=[2.5 5 7.5 10];
for j=1:numel(angles)
    fprintf('Release test %.0f degrees.\n',angles(j));
    result.releases(j)=run_case(model,angles(j),[t 0*t],K);
    result.releases(j).label_value=angles(j);
end
for j=1:numel(bounds)
    fprintf('Random-force test %.1f N.\n',bounds(j));
    result.disturbances(j)=run_case(model,0,[t bounds(j)*unit],K);
    result.disturbances(j).label_value=bounds(j);
end
% Independent linear response checks both solver output and pole assignment.
time=(0:0.02:30)'; initial=[0;0;5*pi/180;0];
[~,linear]=ode45(@(~,z)(A-B*K)*z,time,initial, ...
    odeset('RelTol',1e-10,'AbsTol',1e-12,'MaxStep',0.01));
assert(norm(linear(end,:)'-expm((A-B*K)*30)*initial,inf)<1e-8);
assert(norm(linear(end,:),inf)<1e-7);
result.linear=struct('time_s',time','x_m',linear(:,1)', ...
    'theta_deg',linear(:,3)'*180/pi);
result.design=struct('A',A,'B',B,'K',K,'rank',rank(C), ...
    'requested_real',real(poles),'requested_imag',imag(poles), ...
    'actual_real',real(eig(A-B*K)),'actual_imag',imag(eig(A-B*K)), ...
    'coefficient',poly(poles),'place_gain_difference',norm(K-place(A,B,poles),inf));
result.settings=struct('duration_s',30,'seed',79202,'force_limit_N',10, ...
    'disturbance_hold_s',0.1,'analysis_step_s',0.02);
fid=fopen('pole_results.json','w'); fprintf(fid,'%s\n',jsonencode(result,'PrettyPrint',true)); fclose(fid);
close_system(model,0);
% Reopen from disk and simulate without base-workspace input data.
fprintf('Testing standalone saved model.\n');
clear disturbance_signal;
load_system(model); standalone=sim(model);
assert(all(isfinite(standalone.state_log.Data),'all'));
close_system(model,0);
disp(result.design);
for j=1:numel(angles), disp(result.releases(j).metrics); end
for j=1:numel(bounds), disp(result.disturbances(j).metrics); end
fprintf('Pole-placement revision and standalone test completed.\n');
end

function result=run_case(model,angle,disturbance,K)
input=Simulink.SimulationInput(model);
input=input.setVariable('disturbance_signal',disturbance,'Workspace',model);
input=input.setBlockParameter([model '/Nonlinear plant/Angle'], ...
    'InitialCondition',num2str(angle*pi/180,17));
output=sim(input); time=(0:0.02:30)';
z=sample(output.state_log,time); u=sample(output.force_command,time);
d=sample(output.base_disturbance,time);
assert(all(isfinite(z),'all')); assert(max(abs(u))<=10+1e-8);
assert(max(abs(d))<=max(abs(disturbance(:,2)))+1e-8);
first_fall=find(abs(z(:,3))>=pi/2,1);
if isempty(first_fall), last=numel(time); fall_time=-1; else, last=first_fall; fall_time=time(last); end
end_region=time>=28; angle_deg=z(:,3)*180/pi;
recovered=isempty(first_fall) && max(abs(angle_deg(end_region)))<2 && max(abs(z(end_region,1)))<0.05;
outside=find(abs(angle_deg)>1 | abs(z(:,1))>0.05,1,'last');
settling=-1;
if recovered
 if isempty(outside), settling=0; elseif outside<numel(time), settling=time(outside+1); end
end
metrics=struct('initial_angle_deg',angle,'bound_N',max(abs(disturbance(:,2))), ...
 'balanced',isempty(first_fall),'recovered',recovered,'fall_time_s',fall_time, ...
 'settling_time_s',settling,'angle_rms_deg',sqrt(mean(angle_deg(1:last).^2)), ...
 'peak_angle_deg',max(abs(angle_deg(1:last))),'peak_cart_m',max(abs(z(1:last,1))), ...
 'peak_applied_N',max(abs(u(1:last))),'saturation_s',trapz(time(1:last),double(abs(u(1:last))>=10-1e-6)));
result=struct('time_s',time(1:last)','theta_deg',angle_deg(1:last)', ...
 'x_m',z(1:last,1)','u_N',u(1:last)','disturbance_N',d(1:last)', ...
 'requested_N',(-z(1:last,:)*K')','metrics',metrics,'label_value',0);
end

function v=sample(signal,time)
[t,idx]=unique(double(signal.Time(:)),'stable');
y=reshape(double(signal.Data),numel(signal.Time),[]);
v=interp1(t,y(idx,:),time,'linear');
end
