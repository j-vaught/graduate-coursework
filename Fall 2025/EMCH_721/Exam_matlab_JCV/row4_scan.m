function best = row4_scan
rho = 1.225; a1 = 2*pi; ad = 2*pi; c = 0.48; m = 3.8; I0 = 0.065;
fh = 3.2; ft = 6.8; wh = 2*pi*fh; wt = 2*pi*ft;
zh = 4e-2; zt = 3.5e-2; xCP = -0.15*c; xQP = 0.25*c;
MS = [1 -xCP; -m/I0*xCP I0/I0]; CS = [2*zh*wh 0; 0 2*zt*wt]; KS = [wh^2 0; 0 wt^2];
L0 = @(U) a1*rho*U.^2/2*c;
cd_ratio = 0.1;
cd = cd_ratio*c;
Ld0 = @(U) ad*rho*U.^2/2*cd;
e_ratio = 0.43;
e = e_ratio*c;
Umin = 2; UF = 13.04408; eps = 1e-2;
U = [Umin [(1-eps) 1 (1+eps)]*UF 23];
Kdh_min = -50; Kdh_max = 50; Kdt_min = -50; Kdt_max = 50; step = 0.5;
minDiff = inf; best = struct('Kdh',NaN,'Kdt',NaN,'row4',NaN,'zz',[]);
for Kdh_try = Kdh_min:step:Kdh_max
    for Kdt_try = Kdt_min:step:Kdt_max
        [zzTarget, ok] = compute_ordered_dampings_local(U(4), Kdh_try, Kdt_try, L0, Ld0, MS, CS, KS, xQP, e, m, I0);
        if ~ok
            continue;
        end
        diff = abs(zzTarget(4) - 0.01);
        if diff < minDiff
            minDiff = diff;
            best.Kdh = Kdh_try;
            best.Kdt = Kdt_try;
            best.row4 = zzTarget(4);
            best.zz = zzTarget;
            best.diff = diff;
        end
    end
end
best.diff = minDiff;
if nargout > 0
    [zzUmin, okUmin] = compute_ordered_dampings_local(U(1), best.Kdh, best.Kdt, L0, Ld0, MS, CS, KS, xQP, e, m, I0);
    best.Umin = zzUmin;
    best.UminValid = okUmin;
end
end

function [zz_ordered, success] = compute_ordered_dampings_local(UU, Kdh, Kdt, L0, Ld0, MS, CS, KS, xQP, cd, m, I0)
    success = false;
    zz_ordered = nan(1,4);
    L = L0(UU);
    Ld = Ld0(UU);
    MA = zeros(2); CA = zeros(2);
    KA = [0, L./m; 0, -xQP*L./I0];
    M = MS + MA; C = CS + CA; K = KS + KA;
    E = [-Ld./m; -cd*Ld./I0];
    if rcond(M) < 1e-14
        return;
    end
    AA = [zeros(2) eye(2); -M\K -M\C];
    BB = [0;0;M\E];
    H = [0 0 Kdh Kdt];
    AA_CL = AA - BB*H;
    p = eig(AA_CL);
    if numel(p) < 4 || any(~isfinite(p))
        return;
    end
    abs_p = abs(p);
    abs_p(abs_p < 1e-12) = 1e-12;
    zvals = -real(p) ./ abs_p;
    freq = abs(imag(p));
    [~, idxSort] = sort(freq, 'ascend');
    if numel(idxSort) < 4
        return;
    end
    reorderIdx = [idxSort(3); idxSort(1); idxSort(2); idxSort(4)];
    if any(~isfinite(zvals(reorderIdx)))
        return;
    end
    zz_ordered = real(zvals(reorderIdx));
    success = true;
end
