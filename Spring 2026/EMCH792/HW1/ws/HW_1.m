%% Clear and close everything
clear; close all; clc;

%% 0. Start by entering your last name and G/UG here
lastName = "your last name here";
display("EMCH-792 HW1, " + lastName)

% For this Homework when you are asked to show that two scalars, vectors or
% matrices are equal, use the provided function checkEqual(a, b)
% Usage:
checkEqual([1, 2, 5]', [3, 3, 3]');
checkEqual(2, 2);

%% Problem 1
% Create 2 vectors v_1 = [-4, 3, 5]^T, v_2 = [1, 0, 7]^T where ^T means the
% transpose

% Find the scalar and outer product of the two vectors and show that
% v_1^T * v_2 = trace(v_1 * v_2^T)

%% Problem 2
% Create two matrices A = [-3, 5, 7; 1, 2, 4; 6, 8, -9] and
% B = [8, 1, 6; -3, 5, 7; 4, 9, -2]

% 2.1 Show that (A^T)^T = A, (A * B)^T = B^T * A^T and (A + B)^T = A^T + B^T

% 2.2 Find the rank and determinant of A and B and if the matrix is invertible,
% find their inverse

% 2.3 Show that inv(A * B) = inv(B) * inv(A)

% 2.4 Find the eigenvalues and eigenvectors of A

%% Problem 3
% Solve Example 1.1 (page 12) using Matlab
% Define matrix A

% Find the inverse of A

% Define matrix A_acute

% Define B, C and D

% Use the matrix inversion lemma to compute the inverse of A_acute

% Find the inverse of A_acute using Matlab's inv() function

% Show that the two inverses are equal
