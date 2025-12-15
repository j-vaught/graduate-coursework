function dampedGVT(zh, zt, MS, CS, KS)
% dampedGVT: Performs damped Ground Vibration Test analysis
%
% This function calculates the eigenvalues and eigenvectors for a damped
% system and extracts frequency and damping information for comparison
% with undamped results.
%
% Inputs:
%   zh - plunge damping ratio
%   zt - pitch damping ratio
%   MS - structural mass matrix
%   CS - structural damping matrix
%   KS - structural stiffness matrix

%% CALCULATE EIGENVALUES: use polyeig to get eigenvectors and eigenvalues
[V_raw, s_raw] = polyeig(KS, CS, MS);
[V, s] = sort_norm_eig(V_raw, s_raw);

%% EXTRACT DAMPING AND FREQUENCY FROM REAL AND IMAGINARY PARTS OF s
z = -real(s) ./ abs(s);          % damping ratios
f = abs(imag(s)) / (2 * pi);     % damped frequencies (Hz)

%% CALCULATE UNDAMPED FREQUENCIES AND MODESHAPES
[V_raw0, s_raw0] = polyeig(KS, 0, MS);
[V0, s0] = sort_norm_eig(V_raw0, s_raw0);
f0 = abs(imag(s0)) / (2 * pi);   % undamped frequencies (Hz)

%% DISPLAY FREQUENCY AND DAMPING COMPARISON
fprintf('\n');
fprintf('=========================================\n');
fprintf('DAMPED GROUND VIBRATION TEST RESULTS\n');
fprintf('=========================================\n');

% Display frequencies
fprintf('\n(a) FREQUENCIES\n');
fprintf('Damped frequencies (Hz): ');
fprintf('%8.4f ', f);
fprintf('\n');
fprintf('Undamped frequencies (Hz): ');
fprintf('%8.4f ', f0);
fprintf('\n');

% Display damping ratios
fprintf('\n(b) DAMPING RATIOS\n');
fprintf('Coupled modal damping (%%): ');
fprintf('%8.4f ', z * 100);
fprintf('\n');
fprintf('Uncoupled modal damping (%%): ');
fprintf('%8.4f %8.4f\n', zt * 100, zh * 100);

%% DISPLAY MODESHAPES
fprintf('\n(c) MODESHAPES\n');
disp('Damped modeshapes:');
disp(V);
disp('Undamped modeshapes:');
disp(V0);

end % function dampedGVT ends here