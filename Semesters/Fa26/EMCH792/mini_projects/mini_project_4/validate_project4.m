function validate_project4()
% Reopen the standalone model and verify the constrained sampled controller.
folder=fileparts(mfilename('fullpath')); cd(folder);
Simulink.fileGenControl('set','CacheFolder',fullfile(tempdir,'emch792-project4-cache'), ...
    'CodeGenFolder',fullfile(tempdir,'emch792-project4-code'),'createDir',true);
resultfile=fullfile(folder,'project4_results.json');
r=jsondecode(fileread(resultfile)); model='inverted_pendulum_mpc';
load_system(model); ws=get_param(model,'ModelWorkspace'); base=getVariable(ws,'mpc_controller');
% Load and run the file without the original project's workspace.
out=sim(model);
[peak,effort,statusmin,statusmax]=raw_checks(out);
assert(peak<=10+1e-7 && statusmin>0);
t=(0:0.02:30)'; z=sample(out.state_log,t,'linear');
r.validation.standalone_angle_max_difference_deg=max(abs(z(:,3)*180/pi-r.comparison.mpc.theta_deg(:)));
assert(r.validation.standalone_angle_max_difference_deg<1e-8);
r.validation.raw_peak_force_N=peak;
r.validation.qp_status_min=statusmin; r.validation.qp_status_max=statusmax;
r.validation.standalone_passed=true;
r.comparison.mpc.metrics.effort_N2_s=effort;
r.comparison.mpc.metrics.peak_force_N=peak;
r.comparison.mpc.metrics.effort_method='Exact integral of piecewise-constant logged force';
% Repeat using shorter prediction horizons and the same controller weights.
ps=[20 35 50];
for i=1:numel(ps)
  if ps(i)==50
    run=out;
  else
    alt=base; alt.PredictionHorizon=ps(i); assignin(ws,'mpc_controller',alt);
    run=sim(model);
  end
  [pk,en,qmin,~]=raw_checks(run); zz=sample(run.state_log,t,'linear'); aa=zz(:,3)*180/pi;
  good=all(isfinite(zz),'all') && max(abs(aa(t>=28)))<=1 && max(abs(zz(t>=28,1)))<=0.05 && max(abs(aa))<90;
  outside=find(abs(aa)>1 | abs(zz(:,1))>0.05,1,'last'); st=-1;
  if good, if isempty(outside), st=0; elseif outside<numel(t), st=t(outside+1); end, end
  r.horizon_study(i)=struct('steps',ps(i),'seconds',ps(i)*0.05,'recovered',good, ...
      'settling_time_s',st,'peak_cart_m',max(abs(zz(:,1))), ...
      'peak_force_N',pk,'effort_N2_s',en,'status_min',qmin);
  assert(pk<=10+1e-7 && qmin>0);
end
assignin(ws,'mpc_controller',base);
% Export the actual Simulink block diagram for the report appendix.
try
    open_system(model); set_param(model,'PaperPositionMode','auto');
    print(['-s' model],'-dpng','-r180',fullfile(folder,'mpc_model_diagram.png'));
catch err
    warning('Diagram export failed: %s',err.message);
end
close_system(model,0);
fid=fopen(resultfile,'w'); cleaner=onCleanup(@() fclose(fid));
fprintf(fid,'%s\n',jsonencode(r,'PrettyPrint',true));
disp(r.validation); disp(r.horizon_study);
end

function [peak,effort,statusmin,statusmax]=raw_checks(out)
u=out.force_command; peak=max(abs(u.Data(:))); t=double(u.Time(:)); x=double(u.Data(:));
[t,ind]=unique(t,'last'); x=x(ind);
% Applied controller force is piecewise constant between recorded updates.
effort=sum(diff(t).*x(1:end-1).^2);
s=double(out.qp_status.Data(:)); statusmin=min(s); statusmax=max(s);
assert(all(isfinite(s)) && all(s>0));
end
function y=sample(signal,t,method)
[tx,idx]=unique(double(signal.Time(:)),'stable');
data=reshape(double(signal.Data),numel(signal.Time),[]);
y=interp1(tx,data(idx,:),t,method,'extrap');
end
