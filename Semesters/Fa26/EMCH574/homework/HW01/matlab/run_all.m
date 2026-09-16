function run_all()
% Recalculate every numerical solution and its Typst figure data.
root = fileparts(mfilename('fullpath'));
addpath(root);
output = fullfile(root,'output');
if ~isfolder(output), mkdir(output); end
logPath = fullfile(output,'results.txt');
if isfile(logPath), delete(logPath); end
diary(logPath);
cleanup = onCleanup(@() finishLog(logPath));
format long g
problems = {'A2','A3','B2','B3','B4','B5','B7','B8','C4','C6','C8'};
for j=1:numel(problems)
    fprintf('\nProblem %s. SI inputs unless units are shown.\n',problems{j});
    runProblem(fullfile(root,[problems{j} '.m']));
end
verify_hw01();
fprintf('\nAll 11 problem scripts and verification checks passed.\n');
end

function runProblem(path)
run(path);
end

function finishLog(path)
diary('off');
% Keep the recorded MATLAB tables free of trailing display padding.
contents = regexprep(fileread(path),'[ \t]+(?=\r?\n)','');
fid = fopen(path,'w');
assert(fid~=-1,'Cannot write results transcript.');
cleanup = onCleanup(@() fclose(fid));
fprintf(fid,'%s',contents);
end
