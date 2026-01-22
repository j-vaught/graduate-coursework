#!/usr/bin/env python3
"""
Verification script for EMCH792 HW1 Solutions
Uses NumPy to verify all matrix computations
"""

import numpy as np
np.set_printoptions(precision=6, suppress=True)

def print_header(text):
    print("\n" + "="*60)
    print(text)
    print("="*60)

def verify_problem_1_2():
    """Verify Problem 1.2: Commuting matrices and eigenvectors"""
    print_header("PROBLEM 1.2: Commuting Matrices")

    A = np.array([[1, 1], [0, 1]])
    B = np.array([[1, 2], [0, 1]])

    print("A =")
    print(A)
    print("\nB =")
    print(B)

    AB = A @ B
    BA = B @ A

    print("\nAB =")
    print(AB)
    print("\nBA =")
    print(BA)

    commute = np.allclose(AB, BA)
    print(f"\nAB == BA: {commute}")

    # Check A != B
    print(f"A != B: {not np.allclose(A, B)}")

    # Check neither is diagonal
    print(f"A is not diagonal: {A[0,1] != 0 or A[1,0] != 0}")
    print(f"B is not diagonal: {B[0,1] != 0 or B[1,0] != 0}")

    # Find eigenvectors
    eigvals_A, eigvecs_A = np.linalg.eig(A)
    eigvals_B, eigvecs_B = np.linalg.eig(B)

    print(f"\nEigenvalues of A: {eigvals_A}")
    print(f"Eigenvectors of A:\n{eigvecs_A}")

    print(f"\nEigenvalues of B: {eigvals_B}")
    print(f"Eigenvectors of B:\n{eigvecs_B}")

    # Check shared eigenvector [1, 0]
    v = np.array([1, 0])
    Av = A @ v
    Bv = B @ v
    print(f"\nShared eigenvector v = [1, 0]:")
    print(f"A @ v = {Av} (should be scalar * v)")
    print(f"B @ v = {Bv} (should be scalar * v)")

    return commute

def verify_problem_1_3():
    """Verify Problem 1.3: Three identities"""
    print_header("PROBLEM 1.3: Matrix Identities")

    # Use random matrices for generality
    np.random.seed(42)
    A = np.random.randn(3, 4)
    B = np.random.randn(4, 3)

    print("Testing with random matrices A (3x4) and B (4x3)")

    # Identity 1: (AB)^T = B^T A^T
    print("\n--- Identity 1: (AB)^T = B^T A^T ---")
    AB = A @ B
    lhs1 = AB.T
    rhs1 = B.T @ A.T
    id1_pass = np.allclose(lhs1, rhs1)
    print(f"(AB)^T == B^T A^T: {id1_pass}")

    # Identity 2: (AB)^{-1} = B^{-1} A^{-1} (need square invertible matrices)
    print("\n--- Identity 2: (AB)^{-1} = B^{-1} A^{-1} ---")
    A_sq = np.random.randn(3, 3) + np.eye(3)  # Add identity to help invertibility
    B_sq = np.random.randn(3, 3) + np.eye(3)

    AB_sq = A_sq @ B_sq
    lhs2 = np.linalg.inv(AB_sq)
    rhs2 = np.linalg.inv(B_sq) @ np.linalg.inv(A_sq)
    id2_pass = np.allclose(lhs2, rhs2)
    print(f"(AB)^(-1) == B^(-1) A^(-1): {id2_pass}")

    # Identity 3: Tr(AB) = Tr(BA)
    print("\n--- Identity 3: Tr(AB) = Tr(BA) ---")
    # Use non-square matrices to show general case
    A_rect = np.random.randn(3, 4)
    B_rect = np.random.randn(4, 3)

    tr_AB = np.trace(A_rect @ B_rect)
    tr_BA = np.trace(B_rect @ A_rect)
    id3_pass = np.isclose(tr_AB, tr_BA)
    print(f"Tr(AB) = {tr_AB:.6f}")
    print(f"Tr(BA) = {tr_BA:.6f}")
    print(f"Tr(AB) == Tr(BA): {id3_pass}")

    return id1_pass and id2_pass and id3_pass

def verify_problem_1_4():
    """Verify Problem 1.4: d(tr(AB))/dA = B^T"""
    print_header("PROBLEM 1.4: Trace Derivative")

    # The derivative d(tr(AB))/dA = B^T
    # We verify numerically: perturb A by epsilon in direction E,
    # the change in tr(AB) should be approximately tr(E @ B) = tr(B^T @ E^T) = sum(B^T .* E)

    np.random.seed(42)
    A = np.random.randn(3, 4)
    B = np.random.randn(4, 3)

    print("A is 3x4, B is 4x3")
    print("Claim: d(tr(AB))/dA = B^T")

    epsilon = 1e-7
    grad_numerical = np.zeros_like(A)

    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A_plus = A.copy()
            A_plus[i, j] += epsilon
            A_minus = A.copy()
            A_minus[i, j] -= epsilon
            grad_numerical[i, j] = (np.trace(A_plus @ B) - np.trace(A_minus @ B)) / (2 * epsilon)

    grad_analytical = B.T

    print(f"\nNumerical gradient:\n{grad_numerical}")
    print(f"\nAnalytical gradient (B^T):\n{grad_analytical}")

    match = np.allclose(grad_numerical, grad_analytical)
    print(f"\nNumerical matches B^T: {match}")

    return match

def verify_problem_1_6():
    """Verify Problem 1.6: Block matrix equation"""
    print_header("PROBLEM 1.6: Block Matrix Equation")

    # Create a random invertible matrix A
    np.random.seed(42)
    A = np.random.randn(3, 3) + 2*np.eye(3)  # Make it more likely invertible

    print("Given invertible A:")
    print(A)

    # Solution: B = A^{-1} + A, C = -A
    A_inv = np.linalg.inv(A)
    B = A_inv + A
    C = -A

    print(f"\nSolution: B = A^(-1) + A")
    print(f"B =")
    print(B)
    print(f"\nSolution: C = -A")
    print(f"C =")
    print(C)

    # Verify: [A A; B A] @ [A; C] = [0; I]
    n = A.shape[0]

    # First row: A*A + A*C = A^2 + A*(-A) = A^2 - A^2 = 0
    first_row = A @ A + A @ C
    print(f"\nVerification:")
    print(f"A^2 + A*C =")
    print(first_row)
    print(f"Should be zero matrix: {np.allclose(first_row, np.zeros((n, n)))}")

    # Second row: B*A + A*C = (A^{-1} + A)*A + A*(-A) = I + A^2 - A^2 = I
    second_row = B @ A + A @ C
    print(f"\nB*A + A*C =")
    print(second_row)
    print(f"Should be identity: {np.allclose(second_row, np.eye(n))}")

    return np.allclose(first_row, np.zeros((n, n))) and np.allclose(second_row, np.eye(n))

def verify_problem_1_7():
    """Verify Problem 1.7: Symmetric matrices with non-symmetric product"""
    print_header("PROBLEM 1.7: Symmetric Matrices, Non-Symmetric Product")

    A = np.array([[1, 1], [1, 0]])
    B = np.array([[0, 1], [1, 1]])

    print("A =")
    print(A)
    print("\nB =")
    print(B)

    # Check symmetry
    A_symmetric = np.allclose(A, A.T)
    B_symmetric = np.allclose(B, B.T)
    print(f"\nA is symmetric (A == A^T): {A_symmetric}")
    print(f"B is symmetric (B == B^T): {B_symmetric}")

    # Compute AB
    AB = A @ B
    print(f"\nAB =")
    print(AB)

    print(f"\n(AB)^T =")
    print(AB.T)

    AB_symmetric = np.allclose(AB, AB.T)
    print(f"\nAB is symmetric: {AB_symmetric}")
    print(f"Counterexample verified (AB not symmetric): {not AB_symmetric}")

    return A_symmetric and B_symmetric and (not AB_symmetric)

def main():
    print("\n" + "#"*60)
    print("# EMCH792 HW1 Solution Verification")
    print("#"*60)

    results = {}
    results['1.2'] = verify_problem_1_2()
    results['1.3'] = verify_problem_1_3()
    results['1.4'] = verify_problem_1_4()
    results['1.6'] = verify_problem_1_6()
    results['1.7'] = verify_problem_1_7()

    print_header("SUMMARY")
    all_pass = True
    for prob, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"Problem {prob}: {status}")
        all_pass = all_pass and passed

    print("\n" + "="*60)
    if all_pass:
        print("ALL SOLUTIONS VERIFIED SUCCESSFULLY!")
    else:
        print("SOME SOLUTIONS FAILED VERIFICATION!")
    print("="*60 + "\n")

    return all_pass

if __name__ == "__main__":
    main()
