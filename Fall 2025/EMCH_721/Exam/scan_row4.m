clearvars -except Kdh_min Kdh_max Kdt_min Kdt_max step U Umin_idx Umax_idx MS CS KS L0 Ld0 xQP e m I0
Kdh_min = -50; Kdh_max = 50; Kdt_min = -50; Kdt_max = 50; step = 0.5;
Umin_idx = 1; target_idx = 4;
best.diff = inf;
best.Kdh = NaN; best.Kdt = NaN; best.vals = [];
for Kdh_try = Kdh_min:step:Kdh_max
    for Kdt_try = Kdt_min:step:Kdt_max
        [zzTarget, ok] = compute_ordered_dampings_local(U(target_idx), Kdh_try, Kdt_try, L0, Ld0, MS, CS, KS, xQP, e, m, I0);
        if ~ok
            continue;
        end
        diff = abs(zzTarget(4) - 0.01);
        if diff < best.diff
            best.diff = diff;
            best.Kdh = Kdh_try;
            best.Kdt = Kdt_try;
            best.vals = zzTarget;
        end
    end
end
best
