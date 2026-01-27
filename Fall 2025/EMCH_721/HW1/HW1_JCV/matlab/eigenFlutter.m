function [r, f, z, sigma, v] = eigenFlutter(rho, a1, c, m, I0, xQP, U, MS, CS, KS)
% eigenFlutter: Calculates eigenvalues and eigenvectors for flutter analysis
%
% This function computes the eigenvalues and eigenvectors of the aeroelastic
% system across a range of airspeeds to analyze flutter characteristics.
%
% Inputs:
%   rho  - air density (kg/m^3)
%   a1   - lift curve slope
%   c    - airfoil chord (m)
%   m    - mass (kg)
%   I0   - moment of inertia about center of mass (kg*m^2)
%   xQP  - aerodynamic center offset from elastic axis (m)
%   U    - airspeed range (m/s)
%   MS   - structural mass matrix
%   CS   - structural damping matrix
%   KS   - structural stiffness matrix
%
% Outputs:
%   r     - eigenvalues
%   f     - frequencies (Hz)
%   z     - damping ratios
%   sigma - real parts of eigenvalues
%   v     - eigenvectors (modeshapes)

tol = 1e-10; % tolerance for discarding machine zero
NU = length(U);

%% Define aerodynamic lift function
L0 = @(UU) rho * UU^2 / 2 * c * a1; % Lift function for a generic speed UU

%% Preallocate output arrays
r = zeros(4, NU);
v = zeros(2, 4, NU);
f = zeros(4, NU);
z = zeros(4, NU);
sigma = zeros(4, NU);

%% Loop through each airspeed
for jU = 1:NU
    %% Define flutter matrices
    MA = zeros(2, 2); % aerodynamic mass matrix (zero for quasi-steady model)
    CA = zeros(2, 2); % aerodynamic damping matrix (zero for quasi-steady model)
    
    % Aerodynamic stiffness matrix
    KA = [0, L0(U(jU)) / m;
          0, -xQP * L0(U(jU)) / I0];
    
    % Total system matrices
    M = MS + MA; % system mass matrix
    C = CS + CA; % system viscous damping matrix
    K = KS + KA; % system stiffness matrix
    
    %% Calculate eigenvalues: use polyeig to get eigenvectors V and eigenvalues s
    [V_raw, s_raw] = polyeig(K, C, M);
    [V, s] = sort_norm_eig(V_raw, s_raw);
    
    %% Store eigenvalues
    r(:, jU) = s;
    
    %% Extract damping and frequencies from real and imaginary parts of s
    ff = abs(imag(s)) / (2 * pi); % frequencies (Hz)
    
    % Calculate real parts with tolerance filtering
    sig = real(s);
    sig = sig .* (abs(sig) > tol);
    
    % Calculate damping ratios
    zz = -sig ./ abs(s); % damping ratios
    
    % Sort damping in descending order
    [~, Iz] = sort(sig, 'descend');
    
    % Store frequencies and damping values
    for i = 1:4
        f(i, jU) = ff(Iz(i));
        z(i, jU) = zz(Iz(i));
        sigma(i, jU) = real(s(Iz(i)));
        v(:, i, jU) = V(:, Iz(i));
    end
end % jU loop ends here

end % function eigenFlutter ends here