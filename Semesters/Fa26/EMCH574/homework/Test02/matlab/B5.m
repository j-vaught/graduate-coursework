% B.5. Slide whistle frequency estimates.
clear; clc;

L0 = 0.0100;              % residual cavity length, m
c = 340;                 % sound speed, m/s
Le = 0.420;              % fully extended length, m
Lc = 0.260;              % fully contracted length, m

dLI = Le - Lc;           % full slider travel, m
LI = L0 + dLI;            % fully extended cavity, m
fI = c / (2 * LI);       % closed-closed fundamental, Hz

dLII = 0.50 * dLI;       % 50 percent travel, m
LII = L0 + dLII;         % half-extended cavity, m
fII = c / (2 * LII);     % closed-closed fundamental, Hz

fIII = 440 * 2^(29 / 12); % D7, Hz
LIII = c / (2 * fIII);    % cavity for D7, m
dLIII = LIII - L0;        % travel for D7, m
pct = 100 * dLIII / dLI;  % percent of full travel

% Closed-open comparison for the physical open-fipple configuration.
foI = c / (4 * LI);
foII = c / (4 * LII);
loIII = c / (4 * fIII);
po = 100 * (loIII - L0) / dLI;

fprintf('B.5 Slide Whistle\n');
fprintf('Inputs: L0 = %.4f m, Le = %.3f m, Lc = %.3f m, c = %.1f m/s\n', ...
    L0, Le, Lc, c);
fprintf('Full travel = %.3f m, cavity = %.3f m, frequency = %.3g Hz (B5)\n', ...
    dLI, LI, fI);
fprintf('50%% travel = %.3f m, cavity = %.3f m, frequency = %.4g Hz (A#6)\n', ...
    dLII, LII, fII);
fprintf('D7 frequency = %.4g Hz, cavity = %.4f m, travel = %.4f m (%.3g%%)\n', ...
    fIII, LIII, dLIII, pct);
fprintf('Closed-open comparison = %.3g Hz, %.4g Hz; D7 at %.3g%% travel\n', ...
    foI, foII, po);
