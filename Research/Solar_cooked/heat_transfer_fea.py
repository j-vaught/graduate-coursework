#!/usr/bin/env python3
"""
Finite Difference Analysis of Heat Transfer from Cylinder in Square Enclosure
with Convection and Radiation Effects

Author: J.C. Vaught
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.colors import LinearSegmentedColormap
from scipy.sparse import diags, csr_matrix
from scipy.sparse.linalg import spsolve

# Brand colors
GARNET = '#73000A'
ATLANTIC = '#466A9F'
CONGAREE = '#1F414D'
HORSESHOE = '#65780B'
ROSE = '#CC2E40'
BLACK90 = '#363636'
BLACK70 = '#5C5C5C'
HONEYCOMB = '#A49137'

# Create custom colormap using brand colors
colors_list = [CONGAREE, ATLANTIC, HORSESHOE, HONEYCOMB, ROSE, GARNET]
brand_cmap = LinearSegmentedColormap.from_list('brand', colors_list, N=256)

# =============================================================================
# Physical Parameters
# =============================================================================
D_cyl = 0.25          # Cylinder diameter [m]
r_cyl = D_cyl / 2     # Cylinder radius [m]
delta = 0.10          # Minimum gap [m]
t_ply = 0.01          # Plywood thickness [m]
L_length = 0.30       # Analysis length [m]

T_cyl = 90.0          # Cylinder temperature [°C]
T_amb = 20.0          # Ambient temperature [°C]

# Material properties
k_air = 0.0283        # Air thermal conductivity [W/(m·K)]
k_ply = 0.12          # Plywood thermal conductivity [W/(m·K)]
h_ext = 7.0           # External convection coefficient [W/(m²·K)]

# Radiation properties
sigma = 5.67e-8       # Stefan-Boltzmann constant [W/(m²·K⁴)]
eps_steel = 0.80      # Steel emissivity
eps_ply = 0.90        # Plywood emissivity

# Geometry
w_in = 2 * (r_cyl + delta)    # Inner box width [m]
w_out = w_in + 2 * t_ply      # Outer box width [m]

print("=" * 70)
print("HEAT TRANSFER FROM CYLINDER IN SQUARE ENCLOSURE - FEA ANALYSIS")
print("=" * 70)
print(f"\nGeometry:")
print(f"  Cylinder diameter:    {D_cyl*100:.1f} cm")
print(f"  Inner box width:      {w_in*100:.1f} cm")
print(f"  Outer box width:      {w_out*100:.1f} cm")
print(f"  Air gap (minimum):    {delta*100:.1f} cm")
print(f"  Plywood thickness:    {t_ply*100:.1f} cm")

# =============================================================================
# Method 1: Analytical Solution (Resistance Network)
# =============================================================================
print("\n" + "=" * 70)
print("METHOD 1: ANALYTICAL RESISTANCE NETWORK")
print("=" * 70)

# Shape factor for cylinder in square (per unit length)
S = 2 * np.pi / np.log(1.08 * w_in / D_cyl)
print(f"\nShape factor S = {S:.3f} m⁻¹")

# Rayleigh number for natural convection
g = 9.81
beta = 3.05e-3        # 1/K at 55°C
nu = 1.82e-5          # m²/s
alpha = 2.59e-5       # m²/s
dT_est = 57           # Estimated temperature difference

Ra = g * beta * dT_est * delta**3 / (nu * alpha)
Nu = 0.046 * Ra**(1/3)
k_eff = k_air * Nu

print(f"Rayleigh number Ra = {Ra:.2e}")
print(f"Nusselt number Nu = {Nu:.2f}")
print(f"Effective conductivity k_eff = {k_eff:.4f} W/(m·K)")

# Convection resistance in air gap
R_conv = 1 / (S * k_eff)
print(f"\nConvection resistance R_conv = {R_conv:.4f} (m·K)/W")

# Radiation resistance
A1 = np.pi * D_cyl    # Cylinder surface area per unit length
A2 = 4 * w_in         # Inner box surface area per unit length

# Radiation resistance coefficient
rad_denom = (1 - eps_steel)/(eps_steel * A1) + 1/A1 + (1 - eps_ply)/(eps_ply * A2)
print(f"\nRadiation terms:")
print(f"  (1-ε₁)/(ε₁·A₁) = {(1-eps_steel)/(eps_steel*A1):.4f}")
print(f"  1/A₁ = {1/A1:.4f}")
print(f"  (1-ε₂)/(ε₂·A₂) = {(1-eps_ply)/(eps_ply*A2):.4f}")
print(f"  Sum = {rad_denom:.4f}")

# Linearized radiation coefficient
T1_K = T_cyl + 273.15
T2_K_est = 310        # Estimated inner plywood temp [K]
h_rad = sigma * (T1_K**4 - T2_K_est**4) / ((T1_K - T2_K_est) * rad_denom * A1)
R_rad = 1 / (h_rad * A1)
print(f"\nLinearized radiation coefficient h_rad = {h_rad:.2f} W/(m²·K)")
print(f"Radiation resistance R_rad = {R_rad:.4f} (m·K)/W")

# Combined air gap resistance (parallel)
R_gap = 1 / (1/R_conv + 1/R_rad)
print(f"\nCombined air gap resistance R_gap = {R_gap:.4f} (m·K)/W")

# Plywood resistance
P_in = 4 * w_in       # Inner perimeter
R_ply = t_ply / (k_ply * P_in)
print(f"Plywood resistance R_ply = {R_ply:.4f} (m·K)/W")

# External convection resistance
P_out = 4 * w_out
R_ext = 1 / (h_ext * P_out)
print(f"External convection resistance R_ext = {R_ext:.4f} (m·K)/W")

# Total resistance
R_total = R_gap + R_ply + R_ext
print(f"\nTotal resistance R_total = {R_total:.4f} (m·K)/W")

# Heat loss
q_prime_analytical = (T_cyl - T_amb) / R_total
Q_analytical = q_prime_analytical * L_length
print(f"\n*** ANALYTICAL RESULTS ***")
print(f"Heat loss per unit length: {q_prime_analytical:.1f} W/m")
print(f"Heat loss for {L_length*100:.0f} cm:    {Q_analytical:.1f} W")

# Temperature distribution
T2_analytical = T_cyl - q_prime_analytical * R_gap
T3_analytical = T2_analytical - q_prime_analytical * R_ply
print(f"\nTemperature distribution:")
print(f"  T1 (cylinder):     {T_cyl:.1f} °C")
print(f"  T2 (inner ply):    {T2_analytical:.1f} °C")
print(f"  T3 (outer ply):    {T3_analytical:.1f} °C")
print(f"  T4 (ambient):      {T_amb:.1f} °C")


# =============================================================================
# Method 2: Finite Difference 2D Solution
# =============================================================================
print("\n" + "=" * 70)
print("METHOD 2: 2D FINITE DIFFERENCE (FEA-STYLE)")
print("=" * 70)

# Grid parameters
N = 101               # Grid points in each direction
domain_size = w_out * 1.5  # Extend domain slightly beyond box

x = np.linspace(-domain_size/2, domain_size/2, N)
y = np.linspace(-domain_size/2, domain_size/2, N)
dx = x[1] - x[0]
dy = y[1] - y[0]
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)

print(f"\nGrid: {N}×{N} = {N*N} nodes")
print(f"Grid spacing: dx = dy = {dx*1000:.2f} mm")

# Define regions
# 1 = cylinder (fixed T), 2 = air gap, 3 = plywood, 4 = external (convection BC)
region = np.zeros((N, N), dtype=int)

for i in range(N):
    for j in range(N):
        r = R[i, j]
        abs_x = abs(X[i, j])
        abs_y = abs(Y[i, j])

        if r <= r_cyl:
            region[i, j] = 1  # Cylinder
        elif abs_x <= w_in/2 and abs_y <= w_in/2:
            region[i, j] = 2  # Air gap
        elif abs_x <= w_out/2 and abs_y <= w_out/2:
            region[i, j] = 3  # Plywood
        else:
            region[i, j] = 4  # External

# Effective conductivity map
k_map = np.zeros((N, N))
k_map[region == 1] = 50.0      # Steel (high, essentially isothermal)
k_map[region == 2] = k_eff     # Air (effective with convection)
k_map[region == 3] = k_ply     # Plywood
k_map[region == 4] = k_air     # External air

# Build sparse matrix for finite difference
# Using 5-point stencil: (T[i+1,j] + T[i-1,j] + T[i,j+1] + T[i,j-1] - 4*T[i,j])/dx² = 0

def idx(i, j):
    """Convert 2D index to 1D"""
    return i * N + j

n_total = N * N
row_list = []
col_list = []
data_list = []
b = np.zeros(n_total)

# Add radiation source term at air-cylinder interface
def add_radiation_source(i, j, T_surf):
    """Add linearized radiation source term"""
    if region[i, j] == 2:  # In air gap
        r = R[i, j]
        # Check if near cylinder surface
        if r_cyl < r < r_cyl + 2*dx:
            # Linearized radiation heat flux from cylinder
            T_surf_K = T_surf + 273.15
            T_local_K = 310  # Estimate
            q_rad = h_rad * (T_surf_K - T_local_K) / (T_surf_K - 273.15) * (T_surf - (T_local_K - 273.15))
            return q_rad / k_eff
    return 0

print("\nBuilding sparse matrix...")
for i in range(N):
    for j in range(N):
        node = idx(i, j)

        if region[i, j] == 1:
            # Cylinder: fixed temperature
            row_list.append(node)
            col_list.append(node)
            data_list.append(1.0)
            b[node] = T_cyl

        elif region[i, j] == 4:
            # External: convection boundary (simplified - fixed at T_amb for far field)
            if i == 0 or i == N-1 or j == 0 or j == N-1:
                row_list.append(node)
                col_list.append(node)
                data_list.append(1.0)
                b[node] = T_amb
            else:
                # Interior external points - Laplacian = 0
                row_list.append(node)
                col_list.append(node)
                data_list.append(-4.0)

                if i > 0:
                    row_list.append(node)
                    col_list.append(idx(i-1, j))
                    data_list.append(1.0)
                if i < N-1:
                    row_list.append(node)
                    col_list.append(idx(i+1, j))
                    data_list.append(1.0)
                if j > 0:
                    row_list.append(node)
                    col_list.append(idx(i, j-1))
                    data_list.append(1.0)
                if j < N-1:
                    row_list.append(node)
                    col_list.append(idx(i, j+1))
                    data_list.append(1.0)

        else:
            # Air gap or plywood: Laplacian with variable k
            k_local = k_map[i, j]

            # Get neighboring conductivities (harmonic mean at interfaces)
            k_ip = 2*k_local*k_map[min(i+1, N-1), j]/(k_local + k_map[min(i+1, N-1), j] + 1e-10)
            k_im = 2*k_local*k_map[max(i-1, 0), j]/(k_local + k_map[max(i-1, 0), j] + 1e-10)
            k_jp = 2*k_local*k_map[i, min(j+1, N-1)]/(k_local + k_map[i, min(j+1, N-1)] + 1e-10)
            k_jm = 2*k_local*k_map[i, max(j-1, 0)]/(k_local + k_map[i, max(j-1, 0)] + 1e-10)

            coef_center = -(k_ip + k_im + k_jp + k_jm)

            row_list.append(node)
            col_list.append(node)
            data_list.append(coef_center)

            if i > 0:
                row_list.append(node)
                col_list.append(idx(i-1, j))
                data_list.append(k_im)
            if i < N-1:
                row_list.append(node)
                col_list.append(idx(i+1, j))
                data_list.append(k_ip)
            if j > 0:
                row_list.append(node)
                col_list.append(idx(i, j-1))
                data_list.append(k_jm)
            if j < N-1:
                row_list.append(node)
                col_list.append(idx(i, j+1))
                data_list.append(k_jp)

            # Apply convection BC at plywood-external interface
            if region[i, j] == 3:
                # Check if adjacent to external region
                neighbors = []
                if i > 0: neighbors.append(region[i-1, j])
                if i < N-1: neighbors.append(region[i+1, j])
                if j > 0: neighbors.append(region[i, j-1])
                if j < N-1: neighbors.append(region[i, j+1])

                if 4 in neighbors:
                    # Add convection loss term: h*(T - T_amb)/k = source
                    biot = h_ext * dx / k_ply
                    # Modify diagonal
                    data_list[-5] -= biot  # Adjust center coefficient
                    b[node] = -biot * T_amb * k_ply

# Create sparse matrix
A = csr_matrix((data_list, (row_list, col_list)), shape=(n_total, n_total))

print("Solving linear system...")
T_flat = spsolve(A, b)
T_2d = T_flat.reshape((N, N))

print("Solution complete!")

# Extract results
# Find temperatures at key locations
center_idx = N // 2

# Inner plywood surface (along x-axis)
inner_ply_x = w_in / 2
inner_ply_idx = np.argmin(np.abs(x - inner_ply_x))
T2_numerical = T_2d[center_idx, inner_ply_idx]

# Outer plywood surface
outer_ply_x = w_out / 2
outer_ply_idx = np.argmin(np.abs(x - outer_ply_x))
T3_numerical = T_2d[center_idx, outer_ply_idx]

# Calculate heat flux from cylinder
# Integrate heat flux over cylinder surface
q_total = 0
n_theta = 360
for theta_deg in range(n_theta):
    theta = np.radians(theta_deg)
    # Point just outside cylinder
    r_probe = r_cyl + dx
    x_probe = r_probe * np.cos(theta)
    y_probe = r_probe * np.sin(theta)

    # Find nearest grid point
    i_probe = np.argmin(np.abs(y - y_probe))
    j_probe = np.argmin(np.abs(x - x_probe))

    # Temperature gradient (radial)
    T_probe = T_2d[i_probe, j_probe]
    dT_dr = (T_cyl - T_probe) / dx

    # Heat flux contribution
    dA = 2 * np.pi * r_cyl / n_theta  # Arc length element
    q_total += k_eff * dT_dr * dA

q_prime_numerical = q_total  # W/m
Q_numerical = q_prime_numerical * L_length

print(f"\n*** NUMERICAL (FEA) RESULTS ***")
print(f"Heat loss per unit length: {q_prime_numerical:.1f} W/m")
print(f"Heat loss for {L_length*100:.0f} cm:    {Q_numerical:.1f} W")
print(f"\nTemperature distribution:")
print(f"  T1 (cylinder):     {T_cyl:.1f} °C")
print(f"  T2 (inner ply):    {T2_numerical:.1f} °C")
print(f"  T3 (outer ply):    {T3_numerical:.1f} °C")
print(f"  T4 (ambient):      {T_amb:.1f} °C")


# =============================================================================
# Method 3: Simple Iterative Verification
# =============================================================================
print("\n" + "=" * 70)
print("METHOD 3: ITERATIVE 1D RESISTANCE NETWORK")
print("=" * 70)

# Iterate to get consistent radiation resistance
T2_iter = 40  # Initial guess for inner plywood temperature

for iteration in range(10):
    T2_K = T2_iter + 273.15
    T1_K = T_cyl + 273.15

    # Radiation heat transfer per unit length
    q_rad_iter = sigma * (T1_K**4 - T2_K**4) / rad_denom

    # Linearized h_rad
    h_rad_iter = q_rad_iter / (A1 * (T_cyl - T2_iter)) if abs(T_cyl - T2_iter) > 0.1 else h_rad
    R_rad_iter = 1 / (h_rad_iter * A1)

    # Combined resistance
    R_gap_iter = 1 / (1/R_conv + 1/R_rad_iter)
    R_total_iter = R_gap_iter + R_ply + R_ext

    # Heat loss
    q_prime_iter = (T_cyl - T_amb) / R_total_iter

    # Update T2
    T2_new = T_cyl - q_prime_iter * R_gap_iter

    if abs(T2_new - T2_iter) < 0.01:
        break
    T2_iter = T2_new

T3_iter = T2_iter - q_prime_iter * R_ply
Q_iter = q_prime_iter * L_length

print(f"\nConverged after {iteration+1} iterations")
print(f"\n*** ITERATIVE RESULTS ***")
print(f"Heat loss per unit length: {q_prime_iter:.1f} W/m")
print(f"Heat loss for {L_length*100:.0f} cm:    {Q_iter:.1f} W")
print(f"\nTemperature distribution:")
print(f"  T2 (inner ply):    {T2_iter:.1f} °C")
print(f"  T3 (outer ply):    {T3_iter:.1f} °C")


# =============================================================================
# Comparison Summary
# =============================================================================
print("\n" + "=" * 70)
print("COMPARISON SUMMARY")
print("=" * 70)

print("\n{:<25} {:>15} {:>15} {:>15}".format(
    "Method", "Q (30cm) [W]", "T2 [°C]", "T3 [°C]"))
print("-" * 70)
print("{:<25} {:>15.1f} {:>15.1f} {:>15.1f}".format(
    "Analytical (linearized)", Q_analytical, T2_analytical, T3_analytical))
print("{:<25} {:>15.1f} {:>15.1f} {:>15.1f}".format(
    "2D Finite Difference", Q_numerical, T2_numerical, T3_numerical))
print("{:<25} {:>15.1f} {:>15.1f} {:>15.1f}".format(
    "Iterative 1D Network", Q_iter, T2_iter, T3_iter))


# =============================================================================
# Generate Plots
# =============================================================================
print("\n" + "=" * 70)
print("GENERATING PLOTS...")
print("=" * 70)

# Figure 1: Temperature contour plot
fig1, ax1 = plt.subplots(figsize=(10, 10))

# Mask cylinder interior for cleaner visualization
T_plot = T_2d.copy()

# Plot temperature contours
levels = np.linspace(20, 90, 36)
cf = ax1.contourf(X*100, Y*100, T_plot, levels=levels, cmap=brand_cmap)
cs = ax1.contour(X*100, Y*100, T_plot, levels=levels[::3], colors='white', linewidths=0.5, alpha=0.5)

# Add colorbar
cbar = plt.colorbar(cf, ax=ax1, label='Temperature [°C]', shrink=0.8)

# Draw geometry outlines
circle = Circle((0, 0), r_cyl*100, fill=False, color='white', linewidth=2)
ax1.add_patch(circle)

inner_box = Rectangle((-w_in/2*100, -w_in/2*100), w_in*100, w_in*100,
                       fill=False, color='white', linewidth=1.5, linestyle='--')
ax1.add_patch(inner_box)

outer_box = Rectangle((-w_out/2*100, -w_out/2*100), w_out*100, w_out*100,
                       fill=False, color='white', linewidth=2)
ax1.add_patch(outer_box)

ax1.set_xlabel('x [cm]', fontsize=12)
ax1.set_ylabel('y [cm]', fontsize=12)
ax1.set_title('2D Temperature Distribution (FEA Solution)', fontsize=14, fontweight='bold')
ax1.set_aspect('equal')
ax1.set_xlim(-35, 35)
ax1.set_ylim(-35, 35)

# Labels
ax1.text(0, 0, 'Steel\n90°C', ha='center', va='center', fontsize=10,
         color='white', fontweight='bold')
ax1.text(17, 17, 'Air', ha='center', va='center', fontsize=9, color='white')
ax1.text(24, 0, 'Plywood', ha='center', va='center', fontsize=8,
         color='white', rotation=90)

plt.tight_layout()
plt.savefig('temperature_contour.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Saved: temperature_contour.png")

# Figure 2: Temperature profile along x-axis
fig2, ax2 = plt.subplots(figsize=(12, 6))

# Extract centerline temperature
T_centerline = T_2d[center_idx, :]
x_cm = x * 100

ax2.plot(x_cm, T_centerline, color=GARNET, linewidth=2.5, label='FEA Solution')

# Add analytical points
x_points = [0, w_in/2*100, w_out/2*100, domain_size/2*100]
T_points = [T_cyl, T2_analytical, T3_analytical, T_amb]
ax2.scatter(x_points, T_points, color=ATLANTIC, s=100, zorder=5,
            label='Analytical', edgecolors='white', linewidths=2)

# Shade regions
ax2.axvspan(-r_cyl*100, r_cyl*100, alpha=0.2, color=BLACK70, label='Cylinder')
ax2.axvspan(w_in/2*100, w_out/2*100, alpha=0.2, color=HONEYCOMB, label='Plywood')
ax2.axvspan(-w_out/2*100, -w_in/2*100, alpha=0.2, color=HONEYCOMB)

# Vertical lines at boundaries
ax2.axvline(r_cyl*100, color=BLACK70, linestyle='--', linewidth=1)
ax2.axvline(-r_cyl*100, color=BLACK70, linestyle='--', linewidth=1)
ax2.axvline(w_in/2*100, color=ATLANTIC, linestyle='--', linewidth=1)
ax2.axvline(-w_in/2*100, color=ATLANTIC, linestyle='--', linewidth=1)
ax2.axvline(w_out/2*100, color=HONEYCOMB, linestyle='--', linewidth=1)
ax2.axvline(-w_out/2*100, color=HONEYCOMB, linestyle='--', linewidth=1)

ax2.set_xlabel('Position x [cm]', fontsize=12)
ax2.set_ylabel('Temperature [°C]', fontsize=12)
ax2.set_title('Temperature Profile Along Centerline (y=0)', fontsize=14, fontweight='bold')
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(-35, 35)
ax2.set_ylim(15, 95)

plt.tight_layout()
plt.savefig('temperature_profile.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Saved: temperature_profile.png")

# Figure 3: Comparison bar chart
fig3, ax3 = plt.subplots(figsize=(10, 6))

methods = ['Analytical\n(linearized)', '2D Finite\nDifference', 'Iterative\n1D Network']
Q_values = [Q_analytical, Q_numerical, Q_iter]

bars = ax3.bar(methods, Q_values, color=[ATLANTIC, GARNET, CONGAREE],
               edgecolor='black', linewidth=1.5)

# Add value labels on bars
for bar, val in zip(bars, Q_values):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f'{val:.1f} W', ha='center', va='bottom', fontsize=12, fontweight='bold')

ax3.set_ylabel('Heat Loss for 30 cm [W]', fontsize=12)
ax3.set_title('Method Comparison: Heat Loss with Radiation', fontsize=14, fontweight='bold')
ax3.set_ylim(0, max(Q_values) * 1.15)
ax3.grid(True, axis='y', alpha=0.3)

# Add reference line for convection-only case
ax3.axhline(32.0, color=ROSE, linestyle='--', linewidth=2,
            label='Convection only: 32 W')
ax3.legend(loc='upper right', fontsize=10)

plt.tight_layout()
plt.savefig('method_comparison.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Saved: method_comparison.png")

# Figure 4: Resistance breakdown pie chart
fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(14, 6))

# Convection only
sizes_conv = [R_conv, R_ply, R_ext]
labels_conv = ['Air Gap\n(conv only)', 'Plywood', 'External\nConvection']
colors_conv = [ATLANTIC, HONEYCOMB, CONGAREE]

ax4a.pie(sizes_conv, labels=labels_conv, colors=colors_conv, autopct='%1.1f%%',
         startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'},
         wedgeprops={'edgecolor': 'white', 'linewidth': 2})
ax4a.set_title('Convection Only\nTotal R = 0.656 (m·K)/W', fontsize=12, fontweight='bold')

# With radiation
R_total_rad = R_gap_iter + R_ply + R_ext
sizes_rad = [R_gap_iter, R_ply, R_ext]
labels_rad = ['Air Gap\n(conv+rad)', 'Plywood', 'External\nConvection']
colors_rad = [ATLANTIC, HONEYCOMB, CONGAREE]

ax4b.pie(sizes_rad, labels=labels_rad, colors=colors_rad, autopct='%1.1f%%',
         startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'},
         wedgeprops={'edgecolor': 'white', 'linewidth': 2})
ax4b.set_title(f'With Radiation\nTotal R = {R_total_rad:.3f} (m·K)/W', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('resistance_breakdown.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Saved: resistance_breakdown.png")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)

plt.show()
