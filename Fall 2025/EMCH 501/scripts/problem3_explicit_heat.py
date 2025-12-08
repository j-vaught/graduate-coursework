"""
EMCH 501 - Assignment 4
Problem 3: Exercise 15.2 Problem 12 - Explicit Finite Difference Heat Equation

Solves the heat equation using the explicit (forward-time, centered-space) method.

Equation: u_xx = u_t, 0 < x < 1, 0 < t < 1
BC: u(0,t) = 0, u(1,t) = 0
IC: u(x,0) = x(1-x)

Author: JC Vaught
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'figures')

# USC Brand Colors
USC_GARNET = '#73000A'
USC_SANDSTORM = '#FFF2E3'
USC_BLACK90 = '#565656'

def create_usc_colormap():
    """Create a custom colormap using warm colors."""
    colors = ['#000033', '#003366', '#006699', '#3399CC', '#66CCFF', 
              '#FFFF99', '#FFCC66', '#FF9933', '#FF6600', '#CC3300', USC_GARNET]
    return LinearSegmentedColormap.from_list('heat', colors, N=256)

def explicit_heat_solver():
    """
    Solve the heat equation using the explicit finite difference method.
    """
    print("=" * 70)
    print("PROBLEM 3: Explicit Finite Difference Method for Heat Equation")
    print("=" * 70)
    print()
    
    # Problem parameters
    L = 1.0           # Domain length [0, 1]
    T_final = 1.0     # Final time
    n = 5             # Number of spatial divisions
    m = 50            # Number of time steps
    
    h = L / n         # Spatial step = 0.2
    dt = T_final / m  # Time step = 0.02
    lam = dt / h**2   # Stability parameter (k=1 for this equation)
    
    print("STEP 1: Determine Grid Parameters")
    print("-" * 40)
    print(f"  Domain: [0, {L}], Time: [0, {T_final}]")
    print(f"  n = {n} spatial divisions → h = {h}")
    print(f"  m = {m} time steps → Δt = {dt}")
    print()
    print(f"  λ = Δt/h² = {dt}/{h}² = {dt}/{h**2} = {lam}")
    print()
    print("  ╔════════════════════════════════════════════╗")
    print(f"  ║  λ = {lam}                                    ║")
    print("  ║  Stability condition: λ ≤ 0.5 ✓ (at limit!) ║")
    print("  ╚════════════════════════════════════════════╝")
    print()
    
    # Grid points
    x = np.linspace(0, L, n + 1)
    t = np.linspace(0, T_final, m + 1)
    
    print("STEP 2: Initial and Boundary Conditions")
    print("-" * 40)
    print(f"  Initial condition: u(x, 0) = x(1-x)")
    print()
    print(f"  {'i':>4} {'x_i':>8} {'u(x_i, 0)':>12}")
    print("  " + "-" * 28)
    for i in range(n + 1):
        u_val = x[i] * (1 - x[i])
        print(f"  {i:>4} {x[i]:>8.2f} {u_val:>12.4f}")
    print()
    print("  Boundary conditions: u(0,t) = u(1,t) = 0")
    print()
    
    # Initialize solution array
    u = np.zeros((m + 1, n + 1))
    u[0, :] = x * (1 - x)  # Initial condition
    
    print("STEP 3: Explicit Update Formula")
    print("-" * 40)
    print("  The difference equation is:")
    print(f"    u_{{i,j+1}} = λ·u_{{i+1,j}} + (1-2λ)·u_{{i,j}} + λ·u_{{i-1,j}}")
    print()
    print(f"  With λ = {lam}:")
    print(f"    u_{{i,j+1}} = {lam}·u_{{i+1,j}} + {1-2*lam}·u_{{i,j}} + {lam}·u_{{i-1,j}}")
    print()
    print("  Simplifying (since 1-2λ = 0):")
    print("    u_{i,j+1} = 0.5·(u_{i+1,j} + u_{i-1,j})")
    print()
    print("  ⟹ Each point becomes the AVERAGE of its neighbors!")
    print()
    
    print("STEP 4: First Few Time Steps (Manual)")
    print("-" * 40)
    
    # Time stepping
    for j in range(m):
        for i in range(1, n):
            u[j + 1, i] = lam * u[j, i + 1] + (1 - 2*lam) * u[j, i] + lam * u[j, i - 1]
        
        # Print first few time steps manually
        if j < 3:
            print(f"  j = {j} → j = {j+1} (t = {t[j]:.2f} → t = {t[j+1]:.2f}):")
            for i in range(1, n):
                left = u[j, i - 1]
                center = u[j, i]
                right = u[j, i + 1]
                new_val = u[j + 1, i]
                print(f"    u_{{{i},{j+1}}} = 0.5×({right:.4f} + {left:.4f}) = {new_val:.4f}")
            print()
    
    # Print results table
    print("NUMERICAL RESULTS")
    print("=" * 65)
    print()
    print("Solution at selected times:")
    print("-" * 65)
    header = f"{'t':>8} |" + "".join([f" x={xi:.1f} |" for xi in x])
    print(header)
    print("-" * 65)
    
    times_to_print = [0, 10, 20, 30, 40, 50]  # j indices
    for j in times_to_print:
        row = f"{t[j]:>8.2f} |" + "".join([f" {u[j,i]:.4f} |" for i in range(n+1)])
        print(row)
    print("-" * 65)
    print()
    
    # Analysis
    print("OBSERVATIONS")
    print("-" * 40)
    print("  1. Symmetry: The solution maintains symmetry about x = 0.5")
    print("  2. Maximum: The peak temperature is always at x = 0.5")
    print("  3. Decay: The solution decays exponentially toward the boundaries")
    print()
    
    # Energy analysis
    print("ENERGY DECAY ANALYSIS")
    print("-" * 40)
    energies = []
    for j in range(0, m + 1, 10):
        energy = np.trapz(u[j, :]**2, x)
        energies.append((t[j], energy))
        print(f"  t = {t[j]:.2f}: Total energy = {energy:.6f}")
    print()
    
    # Analytical comparison
    print("ANALYTICAL SOLUTION COMPARISON")
    print("-" * 40)
    print("  Exact solution (Fourier series):")
    print("    u(x,t) = Σ B_n sin(nπx) exp(-n²π²t)")
    print()
    print("  where B_n = (2/L) ∫₀¹ x(1-x) sin(nπx) dx")
    print()
    print("  For odd n: B_n = 8/(n³π³)")
    print("  For even n: B_n = 0")
    print()
    
    # Compute analytical solution for comparison
    def analytical_solution(x, t, n_terms=50):
        result = np.zeros_like(x)
        for n in range(1, n_terms + 1, 2):  # Odd terms only
            Bn = 8 / (n**3 * np.pi**3)
            result += Bn * np.sin(n * np.pi * x) * np.exp(-n**2 * np.pi**2 * t)
        return result
    
    print("  Comparison at x = 0.5:")
    print(f"  {'t':>8} {'Numerical':>12} {'Analytical':>12} {'Error':>12}")
    print("  " + "-" * 48)
    for j in [0, 10, 20, 30, 40, 50]:
        u_num = u[j, n//2]  # Value at x = 0.5
        u_ana = analytical_solution(np.array([0.5]), t[j], n_terms=100)[0]
        error = abs(u_num - u_ana)
        print(f"  {t[j]:>8.2f} {u_num:>12.6f} {u_ana:>12.6f} {error:>12.2e}")
    print()
    
    return x, t, u, analytical_solution

def plot_heat_evolution(x, t, u):
    """Create line plot of temperature profiles at different times."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    times_to_plot = [0, 10, 20, 30, 40, 50]
    colors = plt.cm.plasma(np.linspace(0, 0.9, len(times_to_plot)))
    
    for j, color in zip(times_to_plot, colors):
        ax.plot(x, u[j, :], 'o-', color=color, linewidth=2, markersize=8,
                label=f't = {t[j]:.1f}')
    
    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('u(x, t)', fontsize=14)
    ax.set_title('Temperature Profiles at Different Times\n(Explicit Finite Difference Method)', 
                  fontsize=16, fontweight='bold')
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.02, 0.28)
    
    # Add initial condition formula
    ax.text(0.5, 0.22, r'IC: $u(x,0) = x(1-x)$', ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor=USC_SANDSTORM, alpha=0.8))
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, 'heat_explicit_evolution.png')
    plt.savefig(fig_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"Saved figure: {fig_path}")
    plt.close()

def plot_heat_surface(x, t, u):
    """Create 3D surface plot of the solution."""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    X, T = np.meshgrid(x, t)
    
    surf = ax.plot_surface(X, T, u, cmap=create_usc_colormap(), 
                           edgecolor='none', alpha=0.9)
    
    ax.set_xlabel('x (position)', fontsize=12, labelpad=10)
    ax.set_ylabel('t (time)', fontsize=12, labelpad=10)
    ax.set_zlabel('u(x, t)', fontsize=12, labelpad=10)
    ax.set_title('Heat Equation Solution Surface\nu_xx = u_t with u(x,0) = x(1-x)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    fig.colorbar(surf, ax=ax, shrink=0.6, label='Temperature u')
    
    ax.view_init(elev=25, azim=-60)
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, 'heat_explicit_surface.png')
    plt.savefig(fig_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"Saved figure: {fig_path}")
    plt.close()

def plot_heat_heatmap(x, t, u):
    """Create 2D heatmap of the solution evolution."""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    X, T = np.meshgrid(x, t)
    
    im = ax.pcolormesh(X, T, u, cmap=create_usc_colormap(), shading='auto')
    plt.colorbar(im, ax=ax, label='u(x, t)')
    
    ax.set_xlabel('x (position)', fontsize=14)
    ax.set_ylabel('t (time)', fontsize=14)
    ax.set_title('Heat Equation Evolution Heatmap\n$u_{xx} = u_t$ with $u(x,0) = x(1-x)$', 
                 fontsize=16, fontweight='bold')
    
    # Add contour lines
    contours = ax.contour(X, T, u, levels=8, colors='white', alpha=0.5, linewidths=0.5)
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, 'heat_explicit_heatmap.png')
    plt.savefig(fig_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"Saved figure: {fig_path}")
    plt.close()

def plot_comparison(x, t, u, analytical_solution):
    """Create comparison plot between numerical and analytical solutions."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left: Comparison at different times
    ax1 = axes[0]
    times_to_plot = [0, 20, 50]
    colors = [USC_GARNET, '#4169E1', '#228B22']
    
    x_fine = np.linspace(0, 1, 100)
    
    for j, color in zip(times_to_plot, colors):
        ax1.plot(x, u[j, :], 'o', color=color, markersize=10, 
                label=f'Numerical (t={t[j]:.1f})')
        u_ana = analytical_solution(x_fine, t[j])
        ax1.plot(x_fine, u_ana, '-', color=color, linewidth=2, alpha=0.7)
    
    ax1.set_xlabel('x', fontsize=12)
    ax1.set_ylabel('u(x, t)', fontsize=12)
    ax1.set_title('Numerical vs Analytical Solution', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # Right: Error evolution at center point
    ax2 = axes[1]
    center_idx = len(x) // 2
    
    numerical_center = u[:, center_idx]
    analytical_center = [analytical_solution(np.array([0.5]), ti)[0] for ti in t]
    
    ax2.semilogy(t, np.abs(numerical_center - analytical_center) + 1e-16, 
                 'o-', color=USC_GARNET, linewidth=2, markersize=4)
    ax2.set_xlabel('t', fontsize=12)
    ax2.set_ylabel('|Error| at x = 0.5', fontsize=12)
    ax2.set_title('Error vs Time at Domain Center', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, 'heat_explicit_comparison.png')
    plt.savefig(fig_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"Saved figure: {fig_path}")
    plt.close()

def main():
    print()
    print("╔" + "═"*68 + "╗")
    print("║" + " EMCH 501 Assignment 4 - Problem 3: Explicit Heat Equation ".center(68) + "║")
    print("╚" + "═"*68 + "╝")
    print()
    
    # Run the solver
    x, t, u, analytical = explicit_heat_solver()
    
    # Generate all visualizations
    print("Generating visualizations...")
    plot_heat_evolution(x, t, u)
    plot_heat_surface(x, t, u)
    plot_heat_heatmap(x, t, u)
    plot_comparison(x, t, u, analytical)
    
    print()
    print("=" * 50)
    print("PROBLEM 3 COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    main()
