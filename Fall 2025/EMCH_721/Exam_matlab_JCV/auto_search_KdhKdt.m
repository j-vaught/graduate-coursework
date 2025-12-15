function [Tsolutions, bestRow, stats] = auto_search_KdhKdt(params)
% AUTO_SEARCH_KDHKDT  Exhaustive grid search for (Kdh,Kdt) aileron gains.
%
% USAGE
%   [Tsolutions, bestRow, stats] = auto_search_KdhKdt(params)
%
% INPUT (params struct) - required fields
%   .Kdh_min, .Kdh_max, .Kdt_min, .Kdt_max, .step
%   .U                     - vector of airspeeds (same as in script)
%   .Umin_idx, .Umax_idx   - integer indices into params.U
%   .target, .tolTarget, .minPos
%   .L0fun, .Ld0fun        - function handles L0(U) and Ld0(U)
%   .MS, .CS, .KS, .xQP, .e, .m, .I0
%
% OPTIONAL fields (params)
%   .outfname   - CSV output filename (default: 'solutions_KdhKdt.csv')
%   .useParallel- logical true/false to attempt parfor (default: true)
%   .reportEvery- progress report frequency for serial loop (default: 50000)
%   .target_idx     - index into params.U that should match the 1% target (default: Umax_idx)
%   .tolTarget      - max allowed deviation from the 1% target at params.target_idx (default: inf)
%   .tolTargetRow4  - max allowed deviation from the 1% target for the last ranked mode (default: inf)
%   .minUminZ       - minimum damping required at Umin (default: params.target)
%
% OUTPUT
%   Tsolutions - table with columns:
%                Kdh,Kdt,Umin_z_mode1,Umin_z_mode2,Utarget_z_mode1,Utarget_z_mode2,SSE
%   bestRow    - top row of Tsolutions (lowest SSE) or [] if none
%   stats      - struct with fields: elapsed, totalPairs, count
%
% NOTES
%  - The routine avoids writing inside parfor. Results are gathered and written once.
%  - The damping computation is eigenvalue-based and robust to numerical issues.
%  - If an evaluation is numerically ill-conditioned it is marked infeasible.
%
% Example:
%   params.Kdh_min = -50; params.Kdh_max = 50; params.Kdt_min = -50; params.Kdt_max = 50;
%   params.step = 0.1;
%   params.U = [3, 12.9, 13.04408, 13.17452]; params.Umin_idx = 1; params.Umax_idx = numel(params.U);
%   params.target = 0.01; params.tolTarget = 2e-4; params.minPos = 1e-6;
%   params.L0fun = @(U) a1*rho*U.^2/2*c; ... (set the rest MS,CS,KS,e,m,I0,xQP etc.)
%   [T,best,stats] = auto_search_KdhKdt(params);
%
% Author: assistant (patched version)
% Date:   2025-11-04

arguments
    params struct
end

% --- defaults ---
if ~isfield(params,'outfname'), params.outfname = 'solutions_KdhKdt.csv'; end
if ~isfield(params,'useParallel'), params.useParallel = true; end
if ~isfield(params,'reportEvery'), params.reportEvery = 50000; end

% --- required fields check (basic) ---
req = {'Kdh_min','Kdh_max','Kdt_min','Kdt_max','step','U','Umin_idx','Umax_idx', ...
       'target','minPos','L0fun','Ld0fun','MS','CS','KS','xQP','e','m','I0'};
missing = setdiff(req, fieldnames(params));
if ~isempty(missing)
    error('auto_search_KdhKdt:MissingParams', 'Missing required params: %s', strjoin(missing,', '));
end

if ~isfield(params,'tolTarget'), params.tolTarget = inf; end
if ~isfield(params,'tolTargetRow4'), params.tolTargetRow4 = inf; end
if ~isfield(params,'target_idx'), params.target_idx = params.Umax_idx; end
if ~isfield(params,'minUminZ'), params.minUminZ = params.target; end

% --- pull into locals ---
Kdh_min = params.Kdh_min; Kdh_max = params.Kdh_max;
Kdt_min = params.Kdt_min; Kdt_max = params.Kdt_max;
step = params.step;

U = params.U(:).';
Umin_idx = params.Umin_idx;
Umax_idx = params.Umax_idx;
target = params.target;
tolTarget = params.tolTarget;
tolTargetRow4 = params.tolTargetRow4;
minPos = params.minPos;
target_idx = params.target_idx;
minUminZ = params.minUminZ;

L0 = params.L0fun;
Ld0 = params.Ld0fun;

MS = params.MS; CS = params.CS; KS = params.KS;
xQP = params.xQP; e = params.e; m = params.m; I0 = params.I0;

outfname = params.outfname;
useParRequested = params.useParallel;
reportEvery = params.reportEvery;

% --- grid ---
kh_vec = Kdh_min:step:Kdh_max;
kt_vec = Kdt_min:step:Kdt_max;
Nkh = numel(kh_vec);
Nkt = numel(kt_vec);
Npairs = int64(Nkh) * int64(Nkt);

fprintf('auto_search_KdhKdt: grid = [%g,%g] step=%g -> %d x %d -> %d pairs\n', ...
    Kdh_min,Kdh_max,step,Nkh,Nkt,Npairs);

% --- prepare storage ---
% results layout (serial results matrix): [Kdh Kdt zUmin1 zUmin2 zUtarget_row2 zUtarget_row3 zUtarget_row4 SSE feasibleFlag]
results = nan(double(Npairs),9);
writeIdx = 0;

% --- determine whether parfor is available & desired ---
hasParToolbox = false;
try
    hasParToolbox = license('test','Distrib_Computing_Toolbox') && (exist('parpool','file')==2 || exist('parfor','builtin')==5 || exist('parfor','file')==2);
catch
    hasParToolbox = false;
end
usePar = useParRequested && hasParToolbox;

tStart = tic;

if usePar
    fprintf('Parallel execution requested and toolbox detected -> running parfor.\n');
    % preallocate arrays for safe parfor writes
    Kdh_store = nan(double(Npairs),1);
    Kdt_store = nan(double(Npairs),1);
    zUmin_store = nan(double(Npairs),2);
    zUtarget_store = nan(double(Npairs),3);
    SSE_store = nan(double(Npairs),1);
    feasible_store = false(double(Npairs),1);
    
    % parfor loop
    parfor linearIdx = 1:double(Npairs)
        % convert linear index to 2D grid indices
        [ik, jt] = ind2sub([Nkh, Nkt], linearIdx);
        Kdh_try = kh_vec(ik);
        Kdt_try = kt_vec(jt);
        
        % compute at Umin
        [zzUmin, okUmin] = compute_ordered_dampings_local(U(Umin_idx), Kdh_try, Kdt_try, L0, Ld0, MS, CS, KS, xQP, e, m, I0);
        if ~okUmin
            continue;
        end
        if any(zzUmin <= minPos)
            continue;
        end
        if min(zzUmin(2:3)) < minUminZ
            continue;
        end
        
        % compute at target airspeed
        [zzTarget, okTarget] = compute_ordered_dampings_local(U(target_idx), Kdh_try, Kdt_try, L0, Ld0, MS, CS, KS, xQP, e, m, I0);
        if ~okTarget
            continue;
        end
        if any(zzTarget <= minPos)
            continue;
        end
        
        % check closeness to target at target_idx (rows 2–4)
        diffMid = abs(zzTarget(2:3) - target);
        diffLast = abs(zzTarget(4) - target);
        if all(diffMid <= tolTarget) && diffLast <= tolTargetRow4
            sse = sum(diffMid.^2) + diffLast^2;
            feasible_store(linearIdx) = true;
            Kdh_store(linearIdx) = Kdh_try;
            Kdt_store(linearIdx) = Kdt_try;
            zUmin_store(linearIdx,:) = zzUmin(2:3);
            zUtarget_store(linearIdx,:) = zzTarget(2:4).';
            SSE_store(linearIdx) = sse;
        end
    end % parfor
    
    % pack feasible results
    feasibleIdx = find(feasible_store);
    if ~isempty(feasibleIdx)
        Kdh_vals = Kdh_store(feasibleIdx);
        Kdt_vals = Kdt_store(feasibleIdx);
        zUmin_vals = zUmin_store(feasibleIdx,:);
        zUtarget_vals = zUtarget_store(feasibleIdx,:);
        SSE_vals = SSE_store(feasibleIdx);
        
        Tsolutions = table(Kdh_vals, Kdt_vals, zUmin_vals(:,1), zUmin_vals(:,2), ...
            zUtarget_vals(:,1), zUtarget_vals(:,2), zUtarget_vals(:,3), SSE_vals, ...
            'VariableNames',{'Kdh','Kdt','Umin_z_mode1','Umin_z_mode2','Utarget_z_row2','Utarget_z_row3','Utarget_z_row4','SSE'});
    else
        Tsolutions = table([],[],[],[],[],[],[],[],'VariableNames',{'Kdh','Kdt','Umin_z_mode1','Umin_z_mode2','Utarget_z_row2','Utarget_z_row3','Utarget_z_row4','SSE'});
    end
    
else
    fprintf('Parallel not used -> running serial loop. Reporting every %d pairs.\n', reportEvery);
    loopCount = 0;
    foundCount = 0;
    for ik = 1:Nkh
        Kdh_try = kh_vec(ik);
        for jt = 1:Nkt
            loopCount = loopCount + 1;
            Kdt_try = kt_vec(jt);
            
            % compute at Umin
            [zzUmin, okUmin] = compute_ordered_dampings_local(U(Umin_idx), Kdh_try, Kdt_try, L0, Ld0, MS, CS, KS, xQP, e, m, I0);
            if ~okUmin
                continue;
            end
            if any(zzUmin <= minPos)
                continue;
            end
            if min(zzUmin(2:3)) < minUminZ
                continue;
            end
            
            % compute at target airspeed
            [zzTarget, okTarget] = compute_ordered_dampings_local(U(target_idx), Kdh_try, Kdt_try, L0, Ld0, MS, CS, KS, xQP, e, m, I0);
            if ~okTarget
                continue;
            end
            if any(zzTarget <= minPos)
                continue;
            end
            
            % check closeness to target
            diffMid = abs(zzTarget(2:3) - target);
            diffLast = abs(zzTarget(4) - target);
            if all(diffMid <= tolTarget) && diffLast <= tolTargetRow4
                writeIdx = writeIdx + 1;
                results(writeIdx,:) = [Kdh_try, Kdt_try, zzUmin(2:3).', zzTarget(2:4).', sum(diffMid.^2) + diffLast^2, 1];
                foundCount = foundCount + 1;
            end
            
            if mod(loopCount, reportEvery) == 0
                elapsed = toc(tStart);
                fprintf('Checked %d / %d pairs. Feasible: %d. Elapsed: %.1fs\n', loopCount, Npairs, foundCount, elapsed);
            end
        end
    end
    
    % build table from valid written rows using feasible flag (col 8)
    if writeIdx > 0
        validRows = results(1:writeIdx,:);
        Tsolutions = table(validRows(:,1), validRows(:,2), validRows(:,3), validRows(:,4), ...
            validRows(:,5), validRows(:,6), validRows(:,7), validRows(:,8), ...
            'VariableNames',{'Kdh','Kdt','Umin_z_mode1','Umin_z_mode2','Utarget_z_row2','Utarget_z_row3','Utarget_z_row4','SSE'});
    else
        Tsolutions = table([],[],[],[],[],[],[],[],'VariableNames',{'Kdh','Kdt','Umin_z_mode1','Umin_z_mode2','Utarget_z_row2','Utarget_z_row3','Utarget_z_row4','SSE'});
    end
end

% --- finalize, sort, write CSV ---
if isempty(Tsolutions) || isempty(Tsolutions.Kdh)
    fprintf('No feasible solutions found in grid search.\n');
    bestRow = [];
    stats.elapsed = toc(tStart);
    stats.totalPairs = Npairs;
    stats.count = 0;
    return;
end

Tsolutions = sortrows(Tsolutions,'SSE');
try
    writetable(Tsolutions, outfname);
    fprintf('Grid search complete: %d feasible candidates. Results saved to "%s".\n', height(Tsolutions), outfname);
catch ME
    warning('auto_search_KdhKdt:WriteFailed','Could not write CSV: %s', ME.message);
end

bestRow = Tsolutions(1,:);
stats.elapsed = toc(tStart);
stats.totalPairs = Npairs;
stats.count = height(Tsolutions);

end % main function
