% B.5. Slide whistle frequency estimates.
clear; clc;

L0 = 0.006;                % residual cavity length, m
Lp = 0.006;                % piston thickness, m
Lw = 0.006;                % end-wall thickness, m
c = 340;                   % sound speed, m/s
Le = 0.210;                % measured extended overall length, m
Lc = 0.135;                % measured contracted overall length, m

dLI = Le - Lc;             % full slider travel, m
LI = L0 + dLI;             % fully extended cavity, m
fI = c / (2 * LI);         % closed-closed fundamental, Hz

dLII = 0.40 * dLI;         % 40 percent travel, m
LII = L0 + dLII;           % 40 percent cavity, m
fII = c / (2 * LII);       % 40 percent fundamental, Hz

fIII = 440 * 2^(38/12);    % B7, Hz
LIII = c / (2 * fIII);     % cavity for B7, m
dLIII = LIII - L0;         % travel for B7, m
pct = 100 * dLIII / dLI;   % percent of full travel

n = round(69 + 12*log2([fI fII]/440)); % nearest MIDI note numbers
s = ["C" "C#" "D" "D#" "E" "F" "F#" "G" "G#" "A" "A#" "B"];
notes = s(mod(n,12)+1) + string(floor(n/12)-1);

fprintf('B.5 Slide Whistle\n');
fprintf('Inputs: L0 = %.3f m, Lp = %.3f m, Lw = %.3f m, c = %.1f m/s\n', ...
    L0, Lp, Lw, c);
fprintf('Measured lengths: Le = %.3f m, Lc = %.3f m\n', Le, Lc);
fprintf('Full travel = %.3f m, cavity = %.3f m, frequency = %.2f Hz (%s)\n', ...
    dLI, LI, fI, notes(1));
fprintf('40%% travel = %.3f m, cavity = %.3f m, frequency = %.2f Hz (%s)\n', ...
    dLII, LII, fII, notes(2));
fprintf('B7 frequency = %.2f Hz, cavity = %.5f m, travel = %.5f m (%.1f%%)\n', ...
    fIII, LIII, dLIII, pct);

% Physical open-fipple, closed-piston comparison.
fo = [fI fII]/2;
lo = c/(4*fIII);
po = 100*(lo-L0)/dLI;
fprintf('Closed-open comparison: %.2f Hz, %.2f Hz; B7 at %.1f%% travel\n', ...
    fo(1), fo(2), po);
