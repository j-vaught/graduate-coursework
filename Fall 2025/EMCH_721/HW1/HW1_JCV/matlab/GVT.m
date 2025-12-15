function GVT(c, m, I0, fh, ft, CPratioDefault)
% GVT: Performs Ground Vibration Test analysis
%
% This function calculates the structural matrices and performs eigenanalysis
% for an airfoil system to determine coupled modal frequencies and mode shapes.
%
% Inputs:
%   c              - airfoil chord (m)
%   m              - mass (kg)
%   I0             - moment of inertia about center of mass (kg*m^2)
%   fh             - uncoupled plunge frequency (Hz)
%   ft             - uncoupled pitch frequency (Hz)
%   CPratioDefault - default static offset as percentage of chord

wh = 2 * pi * fh;  % uncoupled plunge angular frequency (rad/s)
wt = 2 * pi * ft;  % uncoupled pitch angular frequency (rad/s)

CPratio = CPratioDefault; % static offset as % of chord

%% Calculate stiffnesses from uncoupled angular frequencies wh, wt
Kh = m * wh^2;     % plunge spring stiffness (N/m)
Kt = I0 * wt^2;    % pitch spring stiffness (N*m/rad)

fprintf('\n(b) Calculate spring stiffnesses\n');
fprintf('  Plunge stiffness Kh = %2.1f N/m\n', Kh);
fprintf('  Pitch stiffness Kt = %3.2f N*m/rad\n', Kt);
fprintf('\n');

%% Take xCP = default value and calculate Ip
CPratio = CPratioDefault;  % static offset as % of chord
xCP = CPratio * c;         % static offset value (m)

fprintf('(c) Static offset\n');
fprintf('  xCP = %2.1f%% (%6.4f m)\n', CPratio * 100, xCP);

Ip = I0 + m * xCP^2;       % moment of inertia about the elastic center (kg*m^2)
fprintf('  Ip  = %6.4f kg*m^2\n', Ip);

%% CALCULATE VIBRATION MATRICES
MS = [1, -xCP;
      -m/I0*xCP, Ip/I0];    % structural mass matrix

KS = [wh^2, 0;
      0, wt^2];             % structural stiffness matrix

fprintf('\nStructural matrices:\n');
fprintf('  Mass matrix MS:\n');
fprintf('    %8.4f  %8.4f\n', MS(1,1), MS(1,2));
fprintf('    %8.4f  %8.4f\n', MS(2,1), MS(2,2));

fprintf('  Stiffness matrix KS:\n');
fprintf('    %8.2f  %8.2f\n', KS(1,1), KS(1,2));
fprintf('    %8.2f  %8.2f\n', KS(2,1), KS(2,2));

%% CALCULATE EIGENVALUES AND EIGENVECTORS
% Use polyeig to get eigenvectors V and eigenvalues s
[V_raw, s_raw] = polyeig(KS, 0, MS);
[V, s] = sort_norm_eig(V_raw, s_raw);

fprintf('\nEigenvalues:\n');
for i = 1:length(s)
    fprintf('  s_%d = %10.4f %+10.4fi\n', i, real(s(i)), imag(s(i)));
end

fprintf('\nEigenvectors:\n');
fprintf('  %12s  %12s  %12s  %12s\n', 'V_1', 'V_2', 'V_3', 'V_4');
for i = 1:size(V, 1)
    fprintf('  ');
    for j = 1:size(V, 2)
        if abs(imag(V(i,j))) < 1e-10
            fprintf('%12.4f  ', real(V(i,j)));
        else
            fprintf('%5.2f%+5.2fi  ', real(V(i,j)), imag(V(i,j)));
        end
    end
    fprintf('\n');
end

%% EXTRACT FREQUENCIES f FROM IMAGINARY PARTS OF s AND COMPARE FREQUENCIES
ff = abs(imag(s)) / (2 * pi);   % damped frequencies (Hz)
[fc, If, ~] = unique(ff, 'stable'); % unique frequencies

fun = [fh, ft];                 % uncoupled frequencies
df = (fc - fun) ./ fun;         % frequency differences

fprintf('\nFrequency comparison:\n');
fprintf('  Coupled frequencies:   f_I  = %7.4f Hz,  f_II = %7.4f Hz\n', fc(1), fc(2));
fprintf('  Uncoupled frequencies: f_h  = %7.4f Hz,  f_t  = %7.4f Hz\n', fh, ft);
fprintf('  Frequency differences: df_I = %7.4f%%,  df_II = %6.4f%%\n', df(1)*100, df(2)*100);

%% MODESHAPES VI, VII
V_modes = V(:, If);  % modeshapes

fprintf('\nModeshapes:\n');
fprintf('  %15s %15s\n', 'V_I', 'V_II');
fprintf('  %s\n', repmat('-', 1, 32));
for i = 1:size(V_modes, 1)
    fprintf('  %15.4f %15.4f\n', V_modes(i, 1), V_modes(i, 2));
end

%% REPEAT FOR OTHER VALUES OF CPratio
fprintf('\n(d) Analysis for various xCP values\n');
CPratio = [-20, -10, -1, 0, 1, 10, 20] * 1e-2; % static offset as % of chord
N_CP = length(CPratio);

fprintf(' CPratio (%%):  ');
fprintf('%9.1f%% ', CPratio * 100);
fprintf('\n\n');

xCP = CPratio * c; % static offset values (m)
fprintf(' xCP (m):       ');
fprintf('%10.4f ', xCP);
fprintf('\n\n');

Ip = I0 + m * xCP.^2; % moment of inertia about elastic center (kg*m^2)
fprintf(' Ip (kg*m^2):   ');
fprintf('%10.4f ', Ip);
fprintf('\n');

f = zeros(2, N_CP);
df = zeros(2, N_CP);
V_modes = zeros(2, 2, N_CP);

for nCP = 1:N_CP
    MS_temp = [1, -xCP(nCP);
               -m/I0*xCP(nCP), Ip(nCP)/I0];
    KS_temp = [wh^2, 0;
               0, wt^2];
    [V_raw, s_raw] = polyeig(KS_temp, 0, MS_temp);
    [V, s] = sort_norm_eig(V_raw, s_raw);
    ff_temp = abs(imag(s)) / (2 * pi);
    [fc_temp, If_temp, ~] = unique(ff_temp, 'stable');
    dff_temp = (fc_temp - fun) ./ fun;
    f(:, nCP) = fc_temp; % frequencies
    df(:, nCP) = dff_temp; % frequency differences
    V_m = V(:, If_temp);
    V_modes(:, :, nCP) = V_m; % modeshapes
end

fprintf('\nCoupled frequencies:\n');
fprintf(' f_I (Hz):      ');
fprintf('%10.4f ', f(1, :));
fprintf('\n');
fprintf(' f_II (Hz):     ');
fprintf('%10.4f ', f(2, :));
fprintf('\n');

fprintf('\nFrequency differences:\n');
fprintf(' df_I (%%):      ');
fprintf('%9.4f%% ', df(1, :) * 100);
fprintf('\n');
fprintf(' df_II (%%):     ');
fprintf('%9.4f%% ', df(2, :) * 100);
fprintf('\n');

fprintf('\nMode I:\n');
fprintf(' V_I(1):        ');
fprintf('%10.4f ', squeeze(V_modes(1, 1, :)));
fprintf('\n');
fprintf(' V_I(2):        ');
fprintf('%10.4f ', squeeze(V_modes(2, 1, :)));
fprintf('\n');

fprintf('\nMode II:\n');
fprintf(' V_II(1):       ');
fprintf('%10.4f ', squeeze(V_modes(1, 2, :)));
fprintf('\n');
fprintf(' V_II(2):       ');
fprintf('%10.4f ', squeeze(V_modes(2, 2, :)));
fprintf('\n');

end % function GVT ends here