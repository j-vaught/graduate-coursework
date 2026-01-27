function [X_sorted_normalized, e_sorted] = sort_norm_eig(X, e)
% sort_norm_eig: Sorts and normalizes eigenvectors and eigenvalues
%
% This function sorts eigenvalues in ascending order of magnitude and reorders
% the corresponding eigenvectors accordingly. It then normalizes the sorted
% eigenvectors so that the largest element in each eigenvector is +1.
%
% Inputs:
%   X(N,Ne) - matrix of Ne eigenvectors, each with N degrees of freedom
%   e(Ne)   - vector of Ne eigenvalues
%
% Outputs:
%   X_sorted_normalized - sorted and normalized eigenvectors
%   e_sorted           - sorted eigenvalues
%
% Procedure:
%   1. Sort eigenvalues e in ascending order of magnitude
%   2. Reorder the eigenvector matrix X according to the sorted indices
%   3. Normalize the sorted eigenvectors so the largest element in each column is +1

%% GET MATRIX DIMENSIONS
N = size(X, 1);   % Number of degrees of freedom
Ne = size(X, 2);  % Number of eigenvectors/eigenvalues

%% SORT EIGENVALUES BY MAGNITUDE (ASCENDING ORDER)
e_abs = abs(e);           % Absolute values of eigenvalues
[~, Is] = sort(e_abs, 'ascend');  % Indices for ascending sort

%% STORE SORTED EIGENVALUES AND EIGENVECTORS
e_sorted = zeros(1, Ne);
Xs = zeros(N, Ne);

for ne = 1:Ne
    e_sorted(ne) = e(Is(ne));      % Sorted eigenvalues
    Xs(:, ne) = X(:, Is(ne));      % Corresponding sorted eigenvectors
end

%% NORMALIZE EIGENVECTORS
% Normalize so that the largest element in each column is +1
Xabs = abs(Xs);                    % Absolute values of eigenvector elements
[~, IX] = max(Xabs, [], 1);        % Indices of maximum elements in each column

X_sorted_normalized = zeros(N, Ne); % Preallocate normalized eigenvector matrix

for j = 1:Ne
    % Scale factor to make the largest element +1
    scale = sign(Xs(IX(j), j)) * max(abs(Xs(:, j)));
    X_sorted_normalized(:, j) = Xs(:, j) / scale;
end

%% RETURN ONLY REAL PARTS IF IMAGINARY PARTS ARE NEGLIGIBLE
tolerance = 1e-10; % Threshold for numerical tolerance
if max(abs(imag(X_sorted_normalized(:)))) < tolerance
    X_sorted_normalized = real(X_sorted_normalized);
end

end % function sort_norm_eig ends here