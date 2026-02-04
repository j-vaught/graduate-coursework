#!/usr/bin/env python3
"""
Finite Difference Analysis of Heat Transfer from Cylinder in Square Enclosure
with Convection and Radiation Effects

Author: J.C. Vaught
"""

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

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

output_lines = []

def log(msg):
    print(msg)
    output_lines.append(msg)

log("=" * 70)
log("HEAT TRANSFER FROM CYLINDER IN SQUARE ENCLOSURE - FEA ANALYSIS")
log("=" * 70)
log(f"\nGeometry:")
log(f"  Cylinder diameter:    {D_cyl*100:.1f} cm")
log(f"  Inner box width:      {w_in*100:.1f} cm")
log(f"  Outer box width:      {w_out*100:.1f} cm")
log(f"  Air gap (minimum):    {delta*100:.1f} cm")
log(f"  Plywood thickness:    {t_ply*100:.1f} cm")

# =============================================================================
# Method 1: Analytical Solution (Resistance Network)
# =============================================================================
log("\n" + "=" * 70)
log("METHOD 1: ANALYTICAL RESISTANCE NETWORK")
log("=" * 70)

# Shape factor for cylinder in square (per unit length)
S = 2 * np.pi / np.log(1.08 * w_in / D_cyl)
log(f"\nShape factor S = {S:.3f} m⁻¹")

# Rayleigh number for natural convection
g = 9.81
beta = 3.05e-3        # 1/K at 55°C
nu = 1.82e-5          # m²/s
alpha = 2.59e-5       # m²/s
dT_est = 57           # Estimated temperature difference

Ra = g * beta * dT_est * delta**3 / (nu * alpha)
Nu = 0.046 * Ra**(1/3)
k_eff = k_air * Nu

log(f"Rayleigh number Ra = {Ra:.2e}")
log(f"Nusselt number Nu = {Nu:.2f}")
log(f"Effective conductivity k_eff = {k_eff:.4f} W/(m·K)")

# Convection resistance in air gap
R_conv = 1 / (S * k_eff)
log(f"\nConvection resistance R_conv = {R_conv:.4f} (m·K)/W")

# Radiation resistance
A1 = np.pi * D_cyl    # Cylinder surface area per unit length
A2 = 4 * w_in         # Inner box surface area per unit length

# Radiation resistance coefficient
rad_denom = (1 - eps_steel)/(eps_steel * A1) + 1/A1 + (1 - eps_ply)/(eps_ply * A2)
log(f"\nRadiation terms:")
log(f"  (1-ε₁)/(ε₁·A₁) = {(1-eps_steel)/(eps_steel*A1):.4f}")
log(f"  1/A₁ = {1/A1:.4f}")
log(f"  (1-ε₂)/(ε₂·A₂) = {(1-eps_ply)/(eps_ply*A2):.4f}")
log(f"  Sum = {rad_denom:.4f}")

# Linearized radiation coefficient
T1_K = T_cyl + 273.15
T2_K_est = 310        # Estimated inner plywood temp [K]
h_rad = sigma * (T1_K**4 - T2_K_est**4) / ((T1_K - T2_K_est) * rad_denom * A1)
R_rad = 1 / (h_rad * A1)
log(f"\nLinearized radiation coefficient h_rad = {h_rad:.2f} W/(m²·K)")
log(f"Radiation resistance R_rad = {R_rad:.4f} (m·K)/W")

# Combined air gap resistance (parallel)
R_gap = 1 / (1/R_conv + 1/R_rad)
log(f"\nCombined air gap resistance R_gap = {R_gap:.4f} (m·K)/W")

# Plywood resistance
P_in = 4 * w_in       # Inner perimeter
R_ply = t_ply / (k_ply * P_in)
log(f"Plywood resistance R_ply = {R_ply:.4f} (m·K)/W")

# External convection resistance
P_out = 4 * w_out
R_ext = 1 / (h_ext * P_out)
log(f"External convection resistance R_ext = {R_ext:.4f} (m·K)/W")

# Total resistance
R_total = R_gap + R_ply + R_ext
log(f"\nTotal resistance R_total = {R_total:.4f} (m·K)/W")

# Heat loss
q_prime_analytical = (T_cyl - T_amb) / R_total
Q_analytical = q_prime_analytical * L_length
log(f"\n*** ANALYTICAL RESULTS (WITH RADIATION) ***")
log(f"Heat loss per unit length: {q_prime_analytical:.1f} W/m")
log(f"Heat loss for {L_length*100:.0f} cm:    {Q_analytical:.1f} W")

# Temperature distribution
T2_analytical = T_cyl - q_prime_analytical * R_gap
T3_analytical = T2_analytical - q_prime_analytical * R_ply
log(f"\nTemperature distribution:")
log(f"  T1 (cylinder):     {T_cyl:.1f} °C")
log(f"  T2 (inner ply):    {T2_analytical:.1f} °C")
log(f"  T3 (outer ply):    {T3_analytical:.1f} °C")
log(f"  T4 (ambient):      {T_amb:.1f} °C")


# =============================================================================
# Method 2: Finite Difference 2D Solution
# =============================================================================
log("\n" + "=" * 70)
log("METHOD 2: 2D FINITE DIFFERENCE (FEA-STYLE)")
log("=" * 70)

# Grid parameters
N = 81                # Grid points in each direction
domain_size = w_out * 1.3  # Extend domain slightly beyond box

x = np.linspace(-domain_size/2, domain_size/2, N)
y = np.linspace(-domain_size/2, domain_size/2, N)
dx = x[1] - x[0]
dy = y[1] - y[0]
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)

log(f"\nGrid: {N}×{N} = {N*N} nodes")
log(f"Grid spacing: dx = dy = {dx*1000:.2f} mm")

# Define regions
# 1 = cylinder (fixed T), 2 = air gap, 3 = plywood, 4 = external
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

def idx(i, j):
    """Convert 2D index to 1D"""
    return i * N + j

n_total = N * N
row_list = []
col_list = []
data_list = []
b = np.zeros(n_total)

log("\nBuilding sparse matrix...")
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
            # External: convection boundary
            if i == 0 or i == N-1 or j == 0 or j == N-1:
                row_list.append(node)
                col_list.append(node)
                data_list.append(1.0)
                b[node] = T_amb
            else:
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
            # Air gap or plywood
            k_local = k_map[i, j]

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

            # Convection BC at plywood-external interface
            if region[i, j] == 3:
                neighbors = []
                if i > 0: neighbors.append(region[i-1, j])
                if i < N-1: neighbors.append(region[i+1, j])
                if j > 0: neighbors.append(region[i, j-1])
                if j < N-1: neighbors.append(region[i, j+1])

                if 4 in neighbors:
                    biot = h_ext * dx / k_ply
                    data_list[-5] -= biot
                    b[node] = -biot * T_amb * k_ply

# Create sparse matrix
A = csr_matrix((data_list, (row_list, col_list)), shape=(n_total, n_total))

log("Solving linear system...")
T_flat = spsolve(A, b)
T_2d = T_flat.reshape((N, N))

log("Solution complete!")

# Extract results
center_idx = N // 2

# Inner plywood surface
inner_ply_x = w_in / 2
inner_ply_idx = np.argmin(np.abs(x - inner_ply_x))
T2_numerical = T_2d[center_idx, inner_ply_idx]

# Outer plywood surface
outer_ply_x = w_out / 2
outer_ply_idx = np.argmin(np.abs(x - outer_ply_x))
T3_numerical = T_2d[center_idx, outer_ply_idx]

# Calculate heat flux from cylinder
q_total = 0
n_theta = 360
for theta_deg in range(n_theta):
    theta = np.radians(theta_deg)
    r_probe = r_cyl + dx
    x_probe = r_probe * np.cos(theta)
    y_probe = r_probe * np.sin(theta)

    i_probe = np.argmin(np.abs(y - y_probe))
    j_probe = np.argmin(np.abs(x - x_probe))

    T_probe = T_2d[i_probe, j_probe]
    dT_dr = (T_cyl - T_probe) / dx

    dA = 2 * np.pi * r_cyl / n_theta
    q_total += k_eff * dT_dr * dA

q_prime_numerical = q_total
Q_numerical = q_prime_numerical * L_length

log(f"\n*** NUMERICAL (FEA) RESULTS ***")
log(f"Heat loss per unit length: {q_prime_numerical:.1f} W/m")
log(f"Heat loss for {L_length*100:.0f} cm:    {Q_numerical:.1f} W")
log(f"\nTemperature distribution:")
log(f"  T1 (cylinder):     {T_cyl:.1f} °C")
log(f"  T2 (inner ply):    {T2_numerical:.1f} °C")
log(f"  T3 (outer ply):    {T3_numerical:.1f} °C")
log(f"  T4 (ambient):      {T_amb:.1f} °C")


# =============================================================================
# Method 3: Iterative 1D Resistance Network
# =============================================================================
log("\n" + "=" * 70)
log("METHOD 3: ITERATIVE 1D RESISTANCE NETWORK")
log("=" * 70)

T2_iter = 40  # Initial guess

for iteration in range(10):
    T2_K = T2_iter + 273.15
    T1_K = T_cyl + 273.15

    q_rad_iter = sigma * (T1_K**4 - T2_K**4) / rad_denom
    h_rad_iter = q_rad_iter / (A1 * (T_cyl - T2_iter)) if abs(T_cyl - T2_iter) > 0.1 else h_rad
    R_rad_iter = 1 / (h_rad_iter * A1)

    R_gap_iter = 1 / (1/R_conv + 1/R_rad_iter)
    R_total_iter = R_gap_iter + R_ply + R_ext

    q_prime_iter = (T_cyl - T_amb) / R_total_iter
    T2_new = T_cyl - q_prime_iter * R_gap_iter

    if abs(T2_new - T2_iter) < 0.01:
        break
    T2_iter = T2_new

T3_iter = T2_iter - q_prime_iter * R_ply
Q_iter = q_prime_iter * L_length

log(f"\nConverged after {iteration+1} iterations")
log(f"\n*** ITERATIVE RESULTS ***")
log(f"Heat loss per unit length: {q_prime_iter:.1f} W/m")
log(f"Heat loss for {L_length*100:.0f} cm:    {Q_iter:.1f} W")
log(f"\nTemperature distribution:")
log(f"  T2 (inner ply):    {T2_iter:.1f} °C")
log(f"  T3 (outer ply):    {T3_iter:.1f} °C")


# =============================================================================
# Convection Only Comparison
# =============================================================================
log("\n" + "=" * 70)
log("COMPARISON: CONVECTION ONLY vs WITH RADIATION")
log("=" * 70)

R_total_conv_only = R_conv + R_ply + R_ext
q_prime_conv_only = (T_cyl - T_amb) / R_total_conv_only
Q_conv_only = q_prime_conv_only * L_length

log(f"\n*** CONVECTION ONLY ***")
log(f"Total resistance: {R_total_conv_only:.4f} (m·K)/W")
log(f"Heat loss for 30 cm: {Q_conv_only:.1f} W")

log(f"\n*** WITH RADIATION ***")
log(f"Total resistance: {R_total_iter:.4f} (m·K)/W")
log(f"Heat loss for 30 cm: {Q_iter:.1f} W")

log(f"\n*** INCREASE DUE TO RADIATION ***")
log(f"Heat loss increase: {(Q_iter/Q_conv_only - 1)*100:.0f}%")
log(f"Resistance decrease: {(1 - R_total_iter/R_total_conv_only)*100:.0f}%")


# =============================================================================
# Comparison Summary
# =============================================================================
log("\n" + "=" * 70)
log("FINAL COMPARISON SUMMARY")
log("=" * 70)

log("\n{:<25} {:>15} {:>15} {:>15}".format(
    "Method", "Q (30cm) [W]", "T2 [°C]", "T3 [°C]"))
log("-" * 70)
log("{:<25} {:>15.1f} {:>15.1f} {:>15.1f}".format(
    "Analytical (linearized)", Q_analytical, T2_analytical, T3_analytical))
log("{:<25} {:>15.1f} {:>15.1f} {:>15.1f}".format(
    "2D Finite Difference", Q_numerical, T2_numerical, T3_numerical))
log("{:<25} {:>15.1f} {:>15.1f} {:>15.1f}".format(
    "Iterative 1D Network", Q_iter, T2_iter, T3_iter))
log("{:<25} {:>15.1f} {:>15} {:>15}".format(
    "Conv. Only (reference)", Q_conv_only, "--", "--"))

log("\n" + "=" * 70)
log("ANALYSIS COMPLETE")
log("=" * 70)

# Save results to file
with open('fea_results.txt', 'w') as f:
    f.write('\n'.join(output_lines))

log("\nResults saved to: fea_results.txt")
