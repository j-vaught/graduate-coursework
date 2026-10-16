function results = run_project3()
% Compare controllers on the same saved nonlinear plant and force limit.
folder=fileparts(mfilename('fullpath')); previous=pwd;
cleanup=onCleanup(@() cd(previous)); cd(folder);
Simulink.fileGenControl('set','CacheFolder',fullfile(tempdir,'emch792-project3-cache'), ...
 'CodeGenFolder',fullfile(tempdir,'emch792-project3-code'),'createDir',true);
fprintf('Calculating LQR gain.\n');
[K,design]=design_lqr_controller(2,0.5,1,0.01,9.81);
A=design.A; B=design.B; Q=design.Q; R=design.R;
assert(rank(ctrb(A,B))==4 && all(real(eig(A-B*K))<0));
[Kcheck,S,poles]=lqr(A,B,Q,R);
assert(norm(K-Kcheck,inf)<1e-10);
assert(norm(A'*S+S*A-S*B*(R\B')*S+Q,inf)<1e-8);
prior=jsondecode(fileread('pole_placement_reference.json'));
Kpole=prior.design.K(:)';
assert(norm(prior.design.A-A,inf)<1e-12 && norm(prior.design.B-B,inf)<1e-12);
model='inverted_pendulum_lqr'; fprintf('Loading aligned plant.\n'); load_system(model);
% Retain the layout and embed the baseline gain and a 5-degree release.
set_param([model '/State feedback'],'Gain',mat2str(-K,17));
set_param([model '/Nonlinear plant/Angle'],'InitialCondition','5*pi/180');
set_param(model,'StopTime','30');
assignin(get_param(model,'ModelWorkspace'),'disturbance_signal',[0 0;30.1 0]);
save_system(model);
angles=[5 10 20];
for j=1:numel(angles)
 fprintf('Matched release %.0f degrees.\n',angles(j));
 results.comparisons(j).angle_deg=angles(j);
 results.comparisons(j).pole=run_case(model,Kpole,angles(j),Q,R,'Pole placement');
 results.comparisons(j).lqr=run_case(model,K,angles(j),Q,R,'LQR');
end
% Reuse the nominal result in both sweeps rather than rerun it.
angle_weights=[100 300 900]; force_weights=[0.1 0.5 2];
for j=1:3
 q=diag([4 2 angle_weights(j) 10]);
 if angle_weights(j)==300
  run=results.comparisons(1).lqr;
 else
  fprintf('Angle penalty %.0f.\n',angle_weights(j));
  run=run_case(model,lqr(A,B,q,R),5,Q,R,'LQR');
 end
 run.q_theta=angle_weights(j); run.R=R;
 results.angle_weights(j)=run;
 if force_weights(j)==R
  run=results.comparisons(1).lqr;
 else
  fprintf('Force penalty %.1f.\n',force_weights(j));
  run=run_case(model,lqr(A,B,Q,force_weights(j)),5,Q,R,'LQR');
 end
 run.q_theta=300; run.R=force_weights(j);
 results.force_weights(j)=run;
end
% Reproduce Project 2 on the same grid to verify the common plant and gain.
reference=prior.releases(1);
actual=results.comparisons(1).pole;
assert(norm(reference.theta_deg(:)-actual.theta_deg(:),inf)<1e-7);
assert(norm(reference.u_N(:)-actual.u_N(:),inf)<1e-7);
% Verify the nominal case against an independent exact-equation integration.
opts=odeset('RelTol',1e-10,'AbsTol',1e-12,'MaxStep',0.002);
t=(0:0.02:30)';
[~,independent]=ode45(@(~,z) derivative(z,K),t,[0;0;5*pi/180;0],opts);
simulated=results.comparisons(1).lqr;
angle_check=max(abs(independent(:,3)*180/pi-simulated.theta_deg(:)));
assert(angle_check<0.01);
results.design=design;
results.design.pole_gain=Kpole;
results.design.riccati_residual=norm(A'*S+S*A-S*B*(R\B')*S+Q,inf);
results.design.poles_real=real(poles); results.design.poles_imag=imag(poles);
results.validation=struct('project2_angle_max_difference_deg', ...
 norm(reference.theta_deg(:)-actual.theta_deg(:),inf), ...
 'independent_nonlinear_angle_max_difference_deg',angle_check,'nonlinear_runs',10);
results.settings=struct('stop_time_s',30,'analysis_step_s',0.02, ...
 'max_step_s',str2double(get_param(model,'MaxStep')), ...
 'relative_tolerance',get_param(model,'RelTol'),'force_limit_N',10, ...
 'settling_angle_deg',1,'settling_cart_m',0.05);
fprintf('Testing standalone LQR model.\n'); close_system(model,0); load_system(model);
standalone=sim(model); zs=standalone.state_log.Data;
assert(all(isfinite(zs),'all') && abs(zs(end,3))<pi/180 && abs(zs(end,1))<0.05);
close_system(model,0);
results.validation.standalone_passed=true;
fid=fopen('project3_results.json','w'); fprintf(fid,'%s\n',jsonencode(results,'PrettyPrint',true)); fclose(fid);
for j=1:numel(angles)
 disp(results.comparisons(j).angle_deg);
 disp(results.comparisons(j).pole.metrics); disp(results.comparisons(j).lqr.metrics);
end
for run=results.angle_weights, fprintf('q=%g R=%g\n',run.q_theta,run.R); disp(run.metrics); end
for run=results.force_weights, fprintf('q=%g R=%g\n',run.q_theta,run.R); disp(run.metrics); end
fprintf('Project 3 completed and validated.\n');
end

function run=run_case(model,K,angle,Qcommon,Rcommon,label)
input=Simulink.SimulationInput(model);
input=input.setBlockParameter([model '/State feedback'],'Gain',mat2str(-K,17));
input=input.setBlockParameter([model '/Nonlinear plant/Angle'], ...
 'InitialCondition',num2str(angle*pi/180,17));
output=sim(input); time=(0:0.02:30)';
z=sample(output.state_log,time); u=sample(output.force_command,time);
d=sample(output.base_disturbance,time);
assert(all(isfinite(z),'all') && all(isfinite(u)) && max(abs(u))<=10+1e-8);
assert(max(abs(d))<1e-12 && abs(z(1,3)-angle*pi/180)<1e-12);
first=find(abs(z(:,3))>=pi/2,1);
if isempty(first), last=numel(time); fall=-1; else, last=first; fall=time(last); end
angles=z(:,3)*180/pi;
recovered=isempty(first) && max(abs(angles(time>=28)))<=1 && max(abs(z(time>=28,1)))<=0.05;
outside=find(abs(angles)>1 | abs(z(:,1))>0.05,1,'last'); ts=-1;
if recovered
 if isempty(outside),ts=0;elseif outside<numel(time),ts=time(outside+1);end
end
metrics=struct('recovered',recovered,'fall_time_s',fall,'settling_time_s',ts, ...
 'peak_angle_deg',max(abs(angles(1:last))),'peak_cart_m',max(abs(z(1:last,1))), ...
 'peak_force_N',max(abs(u(1:last))),'effort_N2_s',trapz(time(1:last),u(1:last).^2), ...
 'common_cost',trapz(time(1:last),sum((z(1:last,:)*Qcommon).*z(1:last,:),2)+Rcommon*u(1:last).^2), ...
 'saturation_s',trapz(time(1:last),double(abs(u(1:last))>=10-1e-6)));
run=struct('label',label,'initial_angle_deg',angle,'gain',K,'time_s',time(1:last)', ...
 'theta_deg',angles(1:last)','x_m',z(1:last,1)','u_N',u(1:last)', ...
 'requested_N',(-z(1:last,:)*K')','metrics',metrics);
end

function v=sample(signal,time)
[t,idx]=unique(double(signal.Time(:)),'stable');
y=reshape(double(signal.Data),numel(signal.Time),[]);
v=interp1(t,y(idx,:),time,'linear');
end

function dz=derivative(z,K)
% Independent evaluation of the exact equations used by the embedded plant.
u=min(max(-K*z,-10),10); s=sin(z(3)); c=cos(z(3));
a=[2.5 .5*c;.5*c .5]\[u+.5*s*z(4)^2;.5*9.81*s-.01*z(4)];
dz=[z(2);a(1);z(4);a(2)];
end
