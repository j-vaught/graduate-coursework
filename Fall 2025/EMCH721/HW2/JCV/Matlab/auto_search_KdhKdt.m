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
%
% OUTPUT
%   Tsolutions - table with columns:
%                Kdh,Kdt,Umin_z_mode1,Umin_z_mode2,Umax_z_mode1,Umax_z_mode2,SSE
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
       'target','tolTarget','minPos','L0fun','Ld0fun','MS','CS','KS','xQP','e','m','I0'};
missing = setdiff(req, fieldnames(params));
if ~isempty(missing)
    error('auto_search_KdhKdt:MissingParams', 'Missing required params: %s', strjoin(missing,', '));
end

% --- pull into locals ---
Kdh_min = params.Kdh_min; Kdh_max = params.Kdh_max;
Kdt_min = params.Kdt_min; Kdt_max = params.Kdt_max;
step = params.step;

U = params.U(:).';
Umin_idx = params.Umin_idx;
Umax_idx = params.Umax_idx;
target = params.target;
tolTarget = params.tolTarget;
minPos = params.minPos;

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
% results layout (serial results matrix): [Kdh Kdt zUmin1 zUmin2 zUmax1 zUmax2 SSE feasibleFlag]
results = nan(double(Npairs),8);
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
    zUmax_store = nan(double(Npairs),2);
    SSE_store = nan(double(Npairs),1);
    feasible_store = false(double(Npairs),1);
    
    % parfor loop
    parfor linearIdx = 1:double(Npairs)
        % convert linear index to 2D grid indices
        [ik, jt] = ind2sub([Nkh, Nkt], linearIdx);
        Kdh_try = kh_vec(ik);
        Kdt_try = kt_vec(jt);
        
        % compute at Umin
        zzUmin = compute_two_dampings_local(U(Umin_idx), Kdh_try, Kdt_try, L0, Ld0, MS, CS, KS, xQP, e, m, I0);
        % -999 indicates numerical failure / infeasible -> skip
        if any(~isfinite(zzUmin)) || any(zzUmin <= -500)
            continue;
        end
        if any(zzUmin <= minPos)
            continue;
        end
        
        % compute at Umax
        zzUmax = compute_two_dampings_local(U(Umax_idx), Kdh_try, Kdt_try, L0, Ld0, MS, CS, KS, xQP, e, m, I0);
        if any(~isfinite(zzUmax)) || any(zzUmax <= -500)
            continue;
        end
        
        % check closeness to target at Umax
        if all(abs(zzUmax - target) <= tolTarget)
            sse = sum((zzUmax - target).^2);
            feasible_store(linearIdx) = true;
            Kdh_store(linearIdx) = Kdh_try;
            Kdt_store(linearIdx) = Kdt_try;
            zUmin_store(linearIdx,:) = zzUmin(:).';
            zUmax_store(linearIdx,:) = zzUmax(:).';
            SSE_store(linearIdx) = sse;
        end
    end % parfor
    
    % pack feasible results
    feasibleIdx = find(feasible_store);
    if ~isempty(feasibleIdx)
        Kdh_vals = Kdh_store(feasibleIdx);
        Kdt_vals = Kdt_store(feasibleIdx);
        zUmin_vals = zUmin_store(feasibleIdx,:);
        zUmax_vals = zUmax_store(feasibleIdx,:);
        SSE_vals = SSE_store(feasibleIdx);
        
        Tsolutions = table(Kdh_vals, Kdt_vals, zUmin_vals(:,1), zUmin_vals(:,2), ...
            zUmax_vals(:,1), zUmax_vals(:,2), SSE_vals, ...
            'VariableNames',{'Kdh','Kdt','Umin_z_mode1','Umin_z_mode2','Umax_z_mode1','Umax_z_mode2','SSE'});
    else
        Tsolutions = table([],[],[],[],[],[],[],'VariableNames',{'Kdh','Kdt','Umin_z_mode1','Umin_z_mode2','Umax_z_mode1','Umax_z_mode2','SSE'});
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
            zzUmin = compute_two_dampings_local(U(Umin_idx), Kdh_try, Kdt_try, L0, Ld0, MS, CS, KS, xQP, e, m, I0);
            if any(~isfinite(zzUmin)) || any(zzUmin <= -500)
                continue;
            end
            if any(zzUmin <= minPos)
                continue;
            end
            
            % compute at Umax
            zzUmax = compute_two_dampings_local(U(Umax_idx), Kdh_try, Kdt_try, L0, Ld0, MS, CS, KS, xQP, e, m, I0);
            if any(~isfinite(zzUmax)) || any(zzUmax <= -500)
                continue;
            end
            
            % check closeness to target
            if all(abs(zzUmax - target) <= tolTarget)
                writeIdx = writeIdx + 1;
                results(writeIdx,:) = [Kdh_try, Kdt_try, zzUmin(:).', zzUmax(:).', sum((zzUmax-target).^2), 1];
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
            validRows(:,5), validRows(:,6), validRows(:,7), ...
            'VariableNames',{'Kdh','Kdt','Umin_z_mode1','Umin_z_mode2','Umax_z_mode1','Umax_z_mode2','SSE'});
    else
        Tsolutions = table([],[],[],[],[],[],[],'VariableNames',{'Kdh','Kdt','Umin_z_mode1','Umin_z_mode2','Umax_z_mode1','Umax_z_mode2','SSE'});
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


% -------------------------------------------------------------------------
% Local helper (kept as a file-local function so parfor can call it)
% -------------------------------------------------------------------------
function zz2 = compute_two_dampings_local(UU, Kdh, Kdt, L0, Ld0, MS, CS, KS, xQP, e, m, I0)
% Robust damping-computation using eigenvalues of state matrix
% Returns 1x2 vector: [z_lowerFreq, z_higherFreq]
% If numerical failure occurs, returns [-999, -999].

    % tiny threshold
    eps_small = 1e-12;

    % aerodynamic terms
    L  = L0(UU);
    Ld = Ld0(UU);

    % assemble system matrices
    MA = zeros(2); CA = zeros(2);
    KA = [0, L./m; 0, -xQP*L./I0];
    M = MS + MA;
    C = CS + CA;
    K = KS + KA;
    E = [-Ld./m; -e.*Ld./I0];

    % check for ill-conditioned mass matrix
    if ~all(isfinite(M(:))) || rcond(M) < 1e-14
        zz2 = [-999, -999];
        return;
    end

    % state matrix
    AA = [zeros(2), eye(2); -M\K, -M\C];
    BB = [0;0;M\E];

    % feedback H is applied later by caller (we pass Kdh,Kdt via H below)
    H = [0 0 Kdh Kdt];
    AA_CL = AA - BB*H;

    % eigenvalues
    p = eig(AA_CL);

    if isempty(p) || any(~isfinite(p))
        zz2 = [-999, -999];
        return;
    end

    % natural freq and damping ratio for each eigenvalue
    abs_p = abs(p);
    abs_p(abs_p < eps_small) = eps_small;
    zvals = -real(p) ./ abs_p;  % damping ratio (can be negative)

    % prefer oscillatory modes (nonzero imag part)
    imagThresh = 1e-8;
    isOsc = abs(imag(p)) > imagThresh;

    if sum(isOsc) >= 2
        idxOsc = find(isOsc);
        wnOsc = abs(p(idxOsc));
        [~, ord] = sort(wnOsc, 'ascend');
        pick = idxOsc(ord(1:min(2,numel(ord))));
        zSel = zvals(pick);
        % order by frequency (lower first)
        [~, ord2] = sort(abs(imag(p(pick))));
        zSel = zSel(ord2);
        zz2 = real(zSel(:).');
        if numel(zz2) < 2, zz2(end+1:2) = zz2(end); end
        return;
    end

    % fallback: pick two smallest natural frequencies (lowest dynamic modes)
    [~, orderWn] = sort(abs_p, 'ascend');
    if numel(orderWn) >= 2
        pick = orderWn(1:2);
        zz2 = real(zvals(pick).');
    elseif numel(orderWn) == 1
        zz2 = real(zvals(orderWn(1)));
        zz2(end+1:2) = zz2(end);
    else
        zz2 = [-999, -999];
    end

    % final sanity
    if any(~isfinite(zz2))
        zz2(~isfinite(zz2)) = -999;
    end
end
