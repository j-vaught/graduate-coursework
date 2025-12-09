"""
EMCH 501 - Assignment 4
Problem 2: Exercise 15.2 Problem 10 - Crank-Nicholson Method

Solves the heat equation using the Crank-Nicholson implicit method.

Equation: 0.25 * u_xx = u_t, 0 < x < 2, 0 < t < 0.3
BC: u(0,t) = 0, u(2,t) = 0
IC: u(x,0) = sin(πx)

Author: JC Vaught
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_banded
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'figures')

# USC Brand Colors
USC_GARNET = '#73000A'
USC_SANDSTORM = '#FFF2E3'

def crank_nicholson_solver():
    """
    Implement the full Crank-Nicholson solver for the heat equation.
    """
    print("=" * 70)
    print("PROBLEM 2: Crank-Nicholson Method for Heat Equation")
    print("=" * 70)
    print()
    
    # Problem parameters
    L = 2.0           # Domain length [0, 2]
    T = 0.3           # Final time
    k = 0.25          # Thermal diffusivity (from 0.25 * u_xx = u_t)
    n = 4             # Number of spatial divisions
    m = 30            # Number of time steps
    
    h = L / n         # Spatial step = 0.5
    dt = T / m        # Time step = 0.01
    lam = k * dt / h**2  # Stability parameter
    
    print("PART (a): Finding λ")
    print("-" * 40)
    print(f"  Domain: [0, {L}]")
    print(f"  Time interval: [0, {T}]")
    print(f"  Diffusivity k = {k}")
    print(f"  n = {n} spatial divisions → h = L/n = {L}/{n} = {h}")
    print(f"  m = {m} time steps → Δt = T/m = {T}/{m} = {dt}")
    print()
    print(f"  λ = k·Δt/h² = {k} × {dt} / {h}² = {k * dt} / {h**2} = {lam}")
    print()
    print(f"  ╔═══════════════════════╗")
    print(f"  ║     λ = {lam:.2f}         ║")
    print(f"  ╚═══════════════════════╝")
    print()
    
    # Crank-Nicholson parameters
    alpha = 2 * (1 + 1/lam)
    beta = 2 * (1 - 1/lam)
    
    print("PART (b): Setting up the system of equations")
    print("-" * 40)
    print(f"  Crank-Nicholson coefficients:")
    print(f"    α = 2(1 + 1/λ) = 2(1 + 1/{lam}) = 2(1 + {1/lam}) = {alpha}")
    print(f"    β = 2(1 - 1/λ) = 2(1 - {1/lam}) = {beta}")
    print(f"    -β = {-beta}")
    print()
    
    # Grid points
    x = np.linspace(0, L, n + 1)  # x = [0, 0.5, 1.0, 1.5, 2.0]
    t = np.linspace(0, T, m + 1)
    
    # Initial condition
    u0 = np.sin(np.pi * x)
    
    print("  Initial condition u(x,0) = sin(πx):")
    print(f"    u₀,₀ = sin(0)     = {u0[0]:.4f}")
    print(f"    u₁,₀ = sin(π/2)   = {u0[1]:.4f}")
    print(f"    u₂,₀ = sin(π)     = {u0[2]:.4f}")
    print(f"    u₃,₀ = sin(3π/2)  = {u0[3]:.4f}")
    print(f"    u₄,₀ = sin(2π)    = {u0[4]:.4f}")
    print()
    
    print("  Crank-Nicholson difference equation:")
    print("    -u_{i-1,j+1} + αu_{i,j+1} - u_{i+1,j+1} = u_{i+1,j} - βu_{i,j} + u_{i-1,j}")
    print()
    print("  For j = 0 (first time step), i = 1, 2, 3:")
    print()
    
    # Build equations for j=0
    # Interior points: i = 1, 2, 3
    # Boundary conditions: u[0,j] = 0, u[4,j] = 0
    
    # Equation for i=1
    rhs1 = u0[2] + (-beta) * u0[1] + u0[0]
    print(f"  i=1: -u₀,₁ + {alpha}u₁,₁ - u₂,₁ = u₂,₀ + ({-beta})u₁,₀ + u₀,₀")
    print(f"        0 + {alpha}u₁,₁ - u₂,₁ = {u0[2]:.0f} + {-beta}×{u0[1]:.0f} + {u0[0]:.0f}")
    print(f"        {alpha}u₁,₁ - u₂,₁ = {rhs1:.0f}")
    print()
    
    # Equation for i=2
    rhs2 = u0[3] + (-beta) * u0[2] + u0[1]
    print(f"  i=2: -u₁,₁ + {alpha}u₂,₁ - u₃,₁ = u₃,₀ + ({-beta})u₂,₀ + u₁,₀")
    print(f"        -u₁,₁ + {alpha}u₂,₁ - u₃,₁ = {u0[3]:.0f} + {-beta}×{u0[2]:.0f} + {u0[1]:.0f}")
    print(f"        -u₁,₁ + {alpha}u₂,₁ - u₃,₁ = {rhs2:.0f}")
    print()
    
    # Equation for i=3
    rhs3 = u0[4] + (-beta) * u0[3] + u0[2]
    print(f"  i=3: -u₂,₁ + {alpha}u₃,₁ - u₄,₁ = u₄,₀ + ({-beta})u₃,₀ + u₂,₀")
    print(f"        -u₂,₁ + {alpha}u₃,₁ - 0 = {u0[4]:.0f} + {-beta}×{u0[3]:.0f} + {u0[2]:.0f}")
    print(f"        -u₂,₁ + {alpha}u₃,₁ = {rhs3:.0f}")
    print()
    
    print("  SYSTEM OF EQUATIONS:")
    print("  ┌                          ┐ ┌     ┐   ┌       ┐")
    print(f"  │ {alpha:6.0f}  {-1:6.0f}  {0:6.0f} │ │ u₁,₁│   │  {rhs1:5.0f} │")
    print(f"  │ {-1:6.0f}  {alpha:6.0f}  {-1:6.0f} │ │ u₂,₁│ = │  {rhs2:5.0f} │")
    print(f"  │ {0:6.0f}  {-1:6.0f}  {alpha:6.0f} │ │ u₃,₁│   │ {rhs3:5.0f} │")
    print("  └                          ┘ └     ┘   └       ┘")
    print()
    
    # Part (c): Solve the system
    print("PART (c): Solving the system by hand")
    print("-" * 40)
    print()
    print("  Using symmetry of sin(πx):")
    print("    sin(π(2-x)) = sin(2π - πx) = -sin(πx)")
    print()
    print("  This antisymmetry is preserved by the heat equation, so:")
    print("    u₁,j = -u₃,j  for all j")
    print("    u₂,j = 0      for all j (center point)")
    print()
    print("  Substituting into equation 1:")
    print(f"    {alpha}u₁,₁ - u₂,₁ = {rhs1:.0f}")
    print(f"    {alpha}u₁,₁ - 0 = {rhs1:.0f}")
    print(f"    u₁,₁ = {rhs1:.0f}/{alpha:.0f} = {rhs1/alpha}")
    print()
    print(f"    As a fraction: u₁,₁ = 99/101 ≈ {99/101:.6f}")
    print()
    print("  Therefore:")
    print(f"    u₁,₁ =  {99/101:.6f}  =  99/101")
    print(f"    u₂,₁ =  {0:.6f}  =  0")
    print(f"    u₃,₁ = {-99/101:.6f}  = -99/101")
    print()
    
    # Verify by solving numerically
    A = np.array([
        [alpha, -1, 0],
        [-1, alpha, -1],
        [0, -1, alpha]
    ])
    b = np.array([rhs1, rhs2, rhs3])
    u_numerical = np.linalg.solve(A, b)
    
    print("  Verification (numerical solve):")
    print(f"    u₁,₁ = {u_numerical[0]:.8f}")
    print(f"    u₂,₁ = {u_numerical[1]:.8f}")
    print(f"    u₃,₁ = {u_numerical[2]:.8f}")
    print()
    
    # Now solve for full time evolution
    print("=" * 50)
    print("FULL TIME EVOLUTION (Crank-Nicholson)")
    print("=" * 50)
    
    # Initialize solution array
    u = np.zeros((m + 1, n + 1))
    u[0, :] = u0
    
    # Build tridiagonal matrix for Crank-Nicholson
    # Left side: -u_{i-1,j+1} + α*u_{i,j+1} - u_{i+1,j+1}
    # This is a tridiagonal system
    
    n_interior = n - 1  # Number of interior points (3)
    
    # Tridiagonal matrix
    A_cn = np.zeros((n_interior, n_interior))
    for i in range(n_interior):
        A_cn[i, i] = alpha
        if i > 0:
            A_cn[i, i-1] = -1
        if i < n_interior - 1:
            A_cn[i, i+1] = -1
    
    # Time stepping
    for j in range(m):
        # Build right-hand side: u_{i+1,j} - β*u_{i,j} + u_{i-1,j}
        b_cn = np.zeros(n_interior)
        for i in range(n_interior):
            i_actual = i + 1  # Map to actual grid index
            b_cn[i] = u[j, i_actual + 1] + (-beta) * u[j, i_actual] + u[j, i_actual - 1]
        
        # Solve for next time step
        u_interior = np.linalg.solve(A_cn, b_cn)
        u[j + 1, 1:n] = u_interior
    
    # Print results table
    print()
    print("Solution at selected times (coarse grid h=0.5):")
    print("-" * 65)
    header = f"{'t':>8} |" + "".join([f" x={xi:.2f} |" for xi in x])
    print(header)
    print("-" * 65)
    
    times_to_print = [0, 1, 5, 10, 15, 20, 25, 30]
    for j in times_to_print:
        row = f"{t[j]:>8.3f} |" + "".join([f" {u[j,i]:>6.4f} |" for i in range(n+1)])
        print(row)
    
    print()
    
    return x, t, u

def plot_crank_nicholson_evolution(x, t, u):
    """Create visualization of the Crank-Nicholson solution."""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # --- Left plot: Temperature profiles at different times ---
    ax1 = axes[0]
    
    times_to_plot = [0, 10, 20, 30]  # j indices
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#73000A']
    
    for j, color in zip(times_to_plot, colors):
        ax1.plot(x, u[j, :], 'o-', color=color, linewidth=2, markersize=8,
                label=f't = {t[j]:.2f}')
    
    ax1.set_xlabel('x', fontsize=12)
    ax1.set_ylabel('u(x, t)', fontsize=12)
    ax1.set_title('Temperature Profiles at Different Times\n(Crank-Nicholson Method)', 
                  fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(-0.1, 2.1)
    ax1.set_ylim(-1.1, 1.1)
    ax1.axhline(y=0, color='black', linewidth=0.5)
    
    # --- Right plot: Heatmap of evolution ---
    ax2 = axes[1]
    
    X, T = np.meshgrid(x, t)
    im = ax2.pcolormesh(X, T, u, cmap='RdBu_r', shading='auto', vmin=-1, vmax=1)
    plt.colorbar(im, ax=ax2, label='u(x, t)')
    
    ax2.set_xlabel('x', fontsize=12)
    ax2.set_ylabel('t', fontsize=12)
    ax2.set_title('Temperature Evolution Heatmap\n(Crank-Nicholson Method)', 
                  fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, 'crank_nicholson_evolution.png')
    plt.savefig(fig_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"Saved figure: {fig_path}")
    plt.close()

def main():
    print()
    print("╔" + "═"*68 + "╗")
    print("║" + " EMCH 501 Assignment 4 - Problem 2: Crank-Nicholson Method ".center(68) + "║")
    print("╚" + "═"*68 + "╝")
    print()
    
    # Run the solver
    x, t, u = crank_nicholson_solver()
    
    # Generate visualization
    print("Generating visualization...")
    plot_crank_nicholson_evolution(x, t, u)
    
    print()
    print("=" * 50)
    print("PROBLEM 2 COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    main()
