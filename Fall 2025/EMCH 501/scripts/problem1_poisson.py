"""
EMCH 501 - Assignment 4
Problem 1: Exercise 15.1 Problem 7 - Poisson's Equation Solver

Solves the Poisson equation on an L-shaped domain using:
1. Direct matrix method (numpy.linalg.solve)
2. Gauss-Seidel iteration

Author: JC Vaught
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
    """Create a custom colormap using USC brand colors."""
    colors = ['#FFFFFF', '#FFF2E3', '#FFD699', '#FF9933', '#CC6600', '#73000A']
    return LinearSegmentedColormap.from_list('USC', colors, N=256)

def solve_poisson_direct():
    """
    Solve Poisson's equation using direct matrix method.
    
    Problem Setup:
    - Equation: u_xx + u_yy = -2
    - Domain: L-shaped region
    - Boundary: u = 1 on inner boundary (ABCD), u = 0 on outer boundary (DEFGA)
    - Mesh size: h = 0.5
    """
    print("=" * 70)
    print("PROBLEM 1b: Poisson's Equation on L-shaped Domain")
    print("=" * 70)
    print()
    
    # Problem parameters
    h = 0.5  # mesh size
    f = -2   # source term (u_xx + u_yy = f)
    rhs = h**2 * f  # = -0.5
    
    print(f"Parameters:")
    print(f"  Mesh size h = {h}")
    print(f"  Source term f(x,y) = {f}")
    print(f"  RHS of difference equation: h² × f = {rhs}")
    print()
    
    # Using symmetry: u1 = u6, u2 = u5
    # Variables: [u1, u2, u3, u4]
    
    print("System of equations (using symmetry u1=u6, u2=u5):")
    print("  Eq 1: -4u₁ + u₂             = -1.5  (at point 1)")
    print("  Eq 2:  u₁ - 4u₂ + u₃ + u₄   = -0.5  (at point 2)")
    print("  Eq 3:       2u₂ - 4u₃       = -0.5  (at point 3)")
    print("  Eq 4:       2u₂      - 4u₄  = -2.5  (at point 4)")
    print()
    
    # Coefficient matrix
    A = np.array([
        [-4,  1,  0,  0],   # Eq 1: -4u1 + u2 = -1.5
        [ 1, -4,  1,  1],   # Eq 2: u1 - 4u2 + u3 + u4 = -0.5
        [ 0,  2, -4,  0],   # Eq 3: 2u2 - 4u3 = -0.5
        [ 0,  2,  0, -4]    # Eq 4: 2u2 - 4u4 = -2.5
    ], dtype=float)
    
    b = np.array([-1.5, -0.5, -0.5, -2.5])
    
    print("Matrix form Ax = b:")
    print()
    print("A = ")
    for row in A:
        print(f"    [{row[0]:6.1f} {row[1]:6.1f} {row[2]:6.1f} {row[3]:6.1f}]")
    print()
    print(f"b = [{b[0]:6.2f} {b[1]:6.2f} {b[2]:6.2f} {b[3]:6.2f}]ᵀ")
    print()
    
    # Solve using numpy
    u = np.linalg.solve(A, b)
    
    print("-" * 50)
    print("SOLUTION (Direct Method):")
    print("-" * 50)
    print()
    print(f"  u₁ = u₆ = {u[0]:.6f}  (exact: 23/44 = {23/44:.6f})")
    print(f"  u₂ = u₅ = {u[1]:.6f}  (exact: 13/22 = {13/22:.6f})")
    print(f"  u₃      = {u[2]:.6f}  (exact: 37/88 = {37/88:.6f})")
    print(f"  u₄      = {u[3]:.6f}  (exact: 81/88 = {81/88:.6f})")
    print()
    
    return u

def solve_poisson_gauss_seidel(tol=1e-8, max_iter=1000):
    """
    Solve using Gauss-Seidel iteration for comparison.
    """
    print("=" * 50)
    print("GAUSS-SEIDEL ITERATION")
    print("=" * 50)
    print()
    
    # Initial guess
    u = np.array([0.5, 0.5, 0.5, 0.5])
    
    print(f"Initial guess: u = [{u[0]:.4f}, {u[1]:.4f}, {u[2]:.4f}, {u[3]:.4f}]")
    print(f"Convergence tolerance: {tol}")
    print()
    print(f"{'Iter':>5} {'u₁':>10} {'u₂':>10} {'u₃':>10} {'u₄':>10} {'Max Δu':>12}")
    print("-" * 60)
    
    for iteration in range(max_iter):
        u_old = u.copy()
        
        # Update u1: -4u1 + u2 = -1.5  =>  u1 = (1.5 + u2) / 4
        u[0] = (1.5 + u[1]) / 4
        
        # Update u2: u1 - 4u2 + u3 + u4 = -0.5  =>  u2 = (0.5 + u1 + u3 + u4) / 4
        u[1] = (0.5 + u[0] + u[2] + u[3]) / 4
        
        # Update u3: 2u2 - 4u3 = -0.5  =>  u3 = (0.5 + 2*u2) / 4
        u[2] = (0.5 + 2*u[1]) / 4
        
        # Update u4: 2u2 - 4u4 = -2.5  =>  u4 = (2.5 + 2*u2) / 4
        u[3] = (2.5 + 2*u[1]) / 4
        
        max_diff = np.max(np.abs(u - u_old))
        
        if iteration < 5 or iteration % 5 == 0 or max_diff < tol:
            print(f"{iteration+1:>5} {u[0]:>10.6f} {u[1]:>10.6f} {u[2]:>10.6f} {u[3]:>10.6f} {max_diff:>12.2e}")
        
        if max_diff < tol:
            print()
            print(f"Converged after {iteration+1} iterations!")
            break
    
    return u

def plot_l_shaped_domain(u_solution):
    """
    Create visualization of the L-shaped domain with solution values.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # --- Left plot: Domain with grid and solution values ---
    ax1 = axes[0]
    
    # Create the L-shaped domain (scaled for h=0.5)
    # The domain corners are at (0,1.5), (1,1.5), (1.5,1), (1.5,0), (2.5,0), (2.5,2.5), (0,2.5)
    # But we'll work with the figure coordinates where h=0.5 maps to unit squares
    
    # Fill L-shaped region
    L_vertices = np.array([
        [1.5, 0], [2.5, 0], [2.5, 2.5], [0, 2.5], [0, 1.5], [1, 1.5], [1.5, 1], [1.5, 0]
    ])
    L_patch = mpatches.Polygon(L_vertices, facecolor='#FFE4B5', edgecolor='black', linewidth=2)
    ax1.add_patch(L_patch)
    
    # Draw grid
    for x in np.arange(0, 3, 0.5):
        ax1.axvline(x, color='gray', linewidth=0.5, alpha=0.5)
    for y in np.arange(0, 3, 0.5):
        ax1.axhline(y, color='gray', linewidth=0.5, alpha=0.5)
    
    # Interior points with solution values (scaled coordinates)
    interior_points = {
        (0.25, 0.75): (u_solution[0], 'u₁'),  # (0.5, 1.5) scaled
        (0.5, 0.75): (u_solution[1], 'u₂'),   # (1.0, 1.5) scaled
        (0.75, 0.75): (u_solution[2], 'u₃'),  # (1.5, 1.5) scaled
        (0.5, 0.5): (u_solution[3], 'u₄'),    # (1.0, 1.0) scaled
        (0.75, 0.5): (u_solution[1], 'u₅'),   # (1.5, 1.0) scaled - equals u2
        (0.75, 0.25): (u_solution[0], 'u₆'),  # (1.5, 0.5) scaled - equals u1
    }
    
    # Map back to actual coordinates for the diagram
    actual_interior = [
        (0.5, 2.0, u_solution[0], 'u₁'),
        (1.0, 2.0, u_solution[1], 'u₂'),
        (1.5, 2.0, u_solution[2], 'u₃'),
        (1.0, 1.5, u_solution[3], 'u₄'),
        (1.5, 1.5, u_solution[1], 'u₅'),
        (1.5, 1.0, u_solution[0], 'u₆'),
    ]
    
    for x, y, val, label in actual_interior:
        ax1.plot(x, y, 'o', markersize=15, color=USC_GARNET)
        ax1.annotate(f'{label}\n{val:.4f}', (x, y), textcoords='offset points', 
                    xytext=(0, 18), ha='center', fontsize=9, fontweight='bold')
    
    # Boundary labels
    boundary_labels = [
        (0, 1.5, 'A'), (1, 1.5, 'B'), (1.5, 1, 'C'), (1.5, 0, 'D'),
        (2.5, 0, 'E'), (2.5, 2.5, 'F'), (0, 2.5, 'G')
    ]
    for x, y, label in boundary_labels:
        ax1.plot(x, y, 's', markersize=10, color='black')
        ax1.annotate(label, (x, y), textcoords='offset points', xytext=(-10, -10), fontsize=11)
    
    ax1.set_xlim(-0.3, 3)
    ax1.set_ylim(-0.3, 3)
    ax1.set_aspect('equal')
    ax1.set_xlabel('x', fontsize=12)
    ax1.set_ylabel('y', fontsize=12)
    ax1.set_title('L-Shaped Domain with Interior Point Solutions', fontsize=14, fontweight='bold')
    
    # --- Right plot: Heatmap visualization ---
    ax2 = axes[1]
    
    # Create a grid for the L-shaped domain
    # We need to mask the "cut-out" corner
    grid_size = 6  # 0 to 2.5 with h=0.5, so 6 points
    x_grid = np.linspace(0, 2.5, grid_size)
    y_grid = np.linspace(0, 2.5, grid_size)
    X, Y = np.meshgrid(x_grid, y_grid)
    
    # Initialize with NaN for masking
    U = np.full((grid_size, grid_size), np.nan)
    
    # Fill in known values
    # Outer boundary (u=0): right, top, bottom-right
    # Inner boundary (u=1): stair-step
    
    # This is simplified - just showing the concept
    # We'll create a simple interpolated view
    
    # For a proper heatmap, we'd need to define the full grid
    # Here's a simplified version showing the solution pattern
    
    # Create a simple color representation
    simple_grid = np.array([
        [np.nan, np.nan, np.nan, 0.0, 0.0, 0.0],  # y=2.5 (top boundary u=0)
        [0.0, u_solution[0], u_solution[1], u_solution[2], 0.4, 0.0],  # y=2.0
        [1.0, 1.0, u_solution[3], u_solution[1], 0.4, 0.0],  # y=1.5
        [np.nan, np.nan, 1.0, u_solution[0], 0.3, 0.0],  # y=1.0
        [np.nan, np.nan, 1.0, 0.2, 0.1, 0.0],  # y=0.5
        [np.nan, np.nan, np.nan, 0.0, 0.0, 0.0],  # y=0 (bottom boundary)
    ])[::-1]  # Flip for correct orientation
    
    cmap = create_usc_colormap()
    im = ax2.imshow(simple_grid, cmap=cmap, origin='lower', 
                    extent=[0, 2.5, 0, 2.5], vmin=0, vmax=1)
    
    plt.colorbar(im, ax=ax2, label='u(x,y)', shrink=0.8)
    ax2.set_xlabel('x', fontsize=12)
    ax2.set_ylabel('y', fontsize=12)
    ax2.set_title('Solution Heatmap (Poisson Equation)', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, 'poisson_solution.png')
    plt.savefig(fig_path, dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print()
    print(f"Saved figure: {fig_path}")
    plt.close()

def plot_stencil():
    """Create 5-point stencil visualization."""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Center point
    ax.plot(0, 0, 'o', markersize=40, color=USC_GARNET)
    ax.annotate('$u_{i,j}$\n(center)', (0, 0), ha='center', va='center', 
                fontsize=12, color='white', fontweight='bold')
    
    # Neighbor points
    neighbors = [
        (1, 0, '$u_{i+1,j}$\n(East)', '+1'),
        (-1, 0, '$u_{i-1,j}$\n(West)', '+1'),
        (0, 1, '$u_{i,j+1}$\n(North)', '+1'),
        (0, -1, '$u_{i,j-1}$\n(South)', '+1'),
    ]
    
    for x, y, label, coeff in neighbors:
        ax.plot(x, y, 'o', markersize=35, color='#4169E1')
        ax.annotate(label, (x, y), ha='center', va='center', 
                    fontsize=10, color='white', fontweight='bold')
        
        # Draw connection line
        ax.plot([0, x*0.6], [0, y*0.6], '-', color='gray', linewidth=2)
        
        # Coefficient label
        ax.annotate(coeff, (x*0.3, y*0.3), ha='center', va='center',
                    fontsize=14, color='green', fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Center coefficient
    ax.annotate('−4', (0.15, 0.15), fontsize=14, color=USC_GARNET, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-1.8, 1.8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('5-Point Laplacian Stencil\n$u_{E} + u_{W} + u_{N} + u_{S} - 4u_{C} = h^2 f$', 
                 fontsize=16, fontweight='bold', pad=20)
    
    # Add formula box
    formula = "Finite Difference Approximation:\n$\\nabla^2 u \\approx \\frac{u_{E} + u_{W} + u_{N} + u_{S} - 4u_{C}}{h^2}$"
    ax.text(0, -1.5, formula, ha='center', va='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor=USC_SANDSTORM, alpha=0.9))
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, 'stencil_diagram.png')
    plt.savefig(fig_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"Saved figure: {fig_path}")
    plt.close()

def main():
    print()
    print("╔" + "═"*68 + "╗")
    print("║" + " EMCH 501 Assignment 4 - Problem 1: Poisson's Equation ".center(68) + "║")
    print("╚" + "═"*68 + "╝")
    print()
    
    # Solve using direct method
    u_direct = solve_poisson_direct()
    
    print()
    
    # Solve using Gauss-Seidel
    u_gs = solve_poisson_gauss_seidel()
    
    print()
    print("=" * 50)
    print("COMPARISON OF METHODS")
    print("=" * 50)
    print()
    print(f"{'Variable':>10} {'Direct':>12} {'Gauss-Seidel':>14} {'Difference':>12}")
    print("-" * 50)
    for i, var in enumerate(['u₁', 'u₂', 'u₃', 'u₄']):
        diff = abs(u_direct[i] - u_gs[i])
        print(f"{var:>10} {u_direct[i]:>12.8f} {u_gs[i]:>14.8f} {diff:>12.2e}")
    
    print()
    
    # Generate plots
    print("Generating visualizations...")
    plot_stencil()
    plot_l_shaped_domain(u_direct)
    
    print()
    print("=" * 50)
    print("PROBLEM 1 COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    main()
