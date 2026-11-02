function format_and_verify()
folder=fileparts(mfilename('fullpath')); cd(folder);
Simulink.fileGenControl('set','CacheFolder',fullfile(tempdir,'emch792-project4-cache'), ...
 'CodeGenFolder',fullfile(tempdir,'emch792-project4-code'),'createDir',true);
model='inverted_pendulum_mpc'; load_system(model); format_project4_layout(model);
save_system(model); output=sim(model);
assert(max(abs(output.force_command.Data(:)))<=10+1e-7 && all(output.qp_status.Data(:)>0));
r=jsondecode(fileread('project4_results.json')); t=(0:.02:30)';
[tx,idx]=unique(double(output.state_log.Time(:)),'stable');
z=reshape(double(output.state_log.Data),numel(output.state_log.Time),[]);
z=interp1(tx,z(idx,:),t,'linear');
assert(max(abs(z(:,3)*180/pi-r.comparison.mpc.theta_deg(:)))<1e-8);
open_system(model); set_param(model,'PaperPositionMode','auto');
print(['-s' model],'-dpng','-r180',fullfile(folder,'mpc_model_diagram.png'));
close_system(model,0); fprintf('Reformatted model reopened and verified.\n');
end
