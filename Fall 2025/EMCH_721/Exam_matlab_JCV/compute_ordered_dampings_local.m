function [zz_ordered, success] = compute_ordered_dampings_local(UU, Kdh, Kdt, L0, Ld0, MS, CS, KS, xQP, Efactor, m, I0)
    % Externalized helper that returns the damping ratios in the
    % reformatted order used by HW2, so rows 2/3 are the mid flutter pair
    % and row 4 is the highest-frequency mode.
    success = false;
    zz_ordered = nan(1,4);

    eps_small = 1e-12;
    L = L0(UU);
    Ld = Ld0(UU);

    MA = zeros(2); CA = zeros(2);
    KA = [0, L./m; 0, -xQP*L./I0];
    M = MS + MA; C = CS + CA; K = KS + KA;
    E = [-Ld./m; -EfFactor.*Ld./I0];

    if rcond(M) < 1e-14
        return;
    end

    AA = [zeros(2) eye(2); -M\K -M\C];
    BB = [0; 0; M\E];
    H = [0 0 Kdh Kdt];
    AA_CL = AA - BB*H;

    p = eig(AA_CL);
    if numel(p) < 4 || any(~isfinite(p))
        return;
    end

    abs_p = abs(p);
    abs_p(abs_p < eps_small) = eps_small;
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
