#!/usr/bin/env python3
"""
Complete Heat Transfer Analysis: Cylinder in Square Enclosure
Including ALL radiation paths:
  1. Radiation from cylinder to inner plywood (enclosed)
  2. Radiation from outer plywood to surroundings

Author: J.C. Vaught
"""

import numpy as np

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

# Convert to Kelvin
T_cyl_K = T_cyl + 273.15
T_amb_K = T_amb + 273.15

# Material properties
k_air = 0.0283        # Air thermal conductivity [W/(m·K)]
k_ply = 0.12          # Plywood thermal conductivity [W/(m·K)]
h_conv_ext = 7.0      # External convection coefficient [W/(m²·K)]

# Radiation properties
sigma = 5.67e-8       # Stefan-Boltzmann constant [W/(m²·K⁴)]
eps_steel = 0.80      # Steel emissivity (oxidized)
eps_ply = 0.90        # Plywood emissivity
eps_surr = 1.0        # Surroundings emissivity (room walls, etc.)

# Geometry
w_in = 2 * (r_cyl + delta)    # Inner box width [m] = 0.45
w_out = w_in + 2 * t_ply      # Outer box width [m] = 0.47

# Surface areas per unit length
A_cyl = np.pi * D_cyl         # Cylinder surface = 0.785 m²/m
A_in = 4 * w_in               # Inner box surface = 1.80 m²/m
A_out = 4 * w_out             # Outer box surface = 1.88 m²/m

print("=" * 75)
print("COMPLETE HEAT TRANSFER ANALYSIS WITH ALL RADIATION PATHS")
print("=" * 75)

print(f"\n{'='*75}")
print("GEOMETRY AND PROPERTIES")
print("=" * 75)
print(f"\nGeometry:")
print(f"  Cylinder diameter D:     {D_cyl*100:.1f} cm")
print(f"  Cylinder radius r:       {r_cyl*100:.2f} cm")
print(f"  Air gap (minimum) δ:     {delta*100:.1f} cm")
print(f"  Inner box side w_in:     {w_in*100:.1f} cm")
print(f"  Plywood thickness t:     {t_ply*100:.1f} cm")
print(f"  Outer box side w_out:    {w_out*100:.1f} cm")

print(f"\nSurface Areas (per unit length):")
print(f"  Cylinder A_cyl:          {A_cyl:.4f} m²/m")
print(f"  Inner box A_in:          {A_in:.4f} m²/m")
print(f"  Outer box A_out:         {A_out:.4f} m²/m")

print(f"\nEmissivities:")
print(f"  Steel (oxidized) ε₁:     {eps_steel}")
print(f"  Plywood ε₂:              {eps_ply}")
print(f"  Surroundings ε₃:         {eps_surr}")

# =============================================================================
# RESISTANCE 1: Air Gap (Convection)
# =============================================================================
print(f"\n{'='*75}")
print("RESISTANCE 1: AIR GAP - NATURAL CONVECTION")
print("=" * 75)

# Air properties at film temperature ~55°C
g = 9.81              # m/s²
beta = 3.05e-3        # 1/K (thermal expansion)
nu = 1.82e-5          # m²/s (kinematic viscosity)
alpha_air = 2.59e-5   # m²/s (thermal diffusivity)
Pr = 0.703            # Prandtl number

# Shape factor for cylinder in square enclosure
S = 2 * np.pi / np.log(1.08 * w_in / D_cyl)
print(f"\nShape factor S = 2π/ln(1.08·w/D) = {S:.4f} m⁻¹")

# Rayleigh number (will iterate, initial estimate)
dT_gap_est = 40  # Initial estimate of T_cyl - T_inner_ply

Ra = g * beta * dT_gap_est * delta**3 / (nu * alpha_air)
Nu = 0.046 * Ra**(1/3)  # Enclosure correlation
k_eff = k_air * Nu

print(f"\nInitial estimates (ΔT ≈ {dT_gap_est} K):")
print(f"  Rayleigh number Ra = {Ra:.3e}")
print(f"  Nusselt number Nu = {Nu:.2f}")
print(f"  Effective conductivity k_eff = {k_eff:.4f} W/(m·K)")

R_conv_gap = 1 / (S * k_eff)
print(f"\nConvection resistance R_conv,gap = {R_conv_gap:.4f} (m·K)/W")

# =============================================================================
# RESISTANCE 2: Air Gap (Radiation) - Cylinder to Inner Plywood
# =============================================================================
print(f"\n{'='*75}")
print("RESISTANCE 2: AIR GAP - RADIATION (Cylinder → Inner Plywood)")
print("=" * 75)

# For cylinder completely enclosed by square box, F_12 = 1
F_12 = 1.0

# Radiation resistance denominator
# 1/R_rad = σ(T1⁴-T2⁴)/(T1-T2) × 1/[(1-ε1)/(ε1·A1) + 1/(A1·F12) + (1-ε2)/(ε2·A2)]

term1 = (1 - eps_steel) / (eps_steel * A_cyl)
term2 = 1 / (A_cyl * F_12)
term3 = (1 - eps_ply) / (eps_ply * A_in)
rad_denom_inner = term1 + term2 + term3

print(f"\nRadiation network (cylinder to inner plywood):")
print(f"  View factor F_12 = {F_12} (cylinder fully enclosed)")
print(f"  (1-ε₁)/(ε₁·A₁) = {term1:.4f} m⁻²")
print(f"  1/(A₁·F₁₂)     = {term2:.4f} m⁻²")
print(f"  (1-ε₂)/(ε₂·A₂) = {term3:.4f} m⁻²")
print(f"  Total denominator = {rad_denom_inner:.4f} m⁻²")

# =============================================================================
# RESISTANCE 3: Plywood Conduction
# =============================================================================
print(f"\n{'='*75}")
print("RESISTANCE 3: PLYWOOD CONDUCTION")
print("=" * 75)

# For thin-walled approximation (t << w)
R_ply = t_ply / (k_ply * A_in)
print(f"\nPlywood resistance R_ply = t/(k·A) = {R_ply:.4f} (m·K)/W")

# More accurate: log-mean for square cross-section
# But for t/w = 0.01/0.45 ≈ 2%, thin-wall is fine

# =============================================================================
# RESISTANCE 4: External Convection
# =============================================================================
print(f"\n{'='*75}")
print("RESISTANCE 4: EXTERNAL CONVECTION")
print("=" * 75)

R_conv_ext = 1 / (h_conv_ext * A_out)
print(f"\nExternal convection resistance R_conv,ext = {R_conv_ext:.4f} (m·K)/W")

# =============================================================================
# RESISTANCE 5: External Radiation (Outer Plywood → Surroundings)
# =============================================================================
print(f"\n{'='*75}")
print("RESISTANCE 5: EXTERNAL RADIATION (Outer Plywood → Surroundings)")
print("=" * 75)

# For a convex surface radiating to large surroundings (F = 1, A_surr >> A_out)
# q_rad = ε·σ·A·(T⁴ - T_surr⁴)
# Linearized: h_rad = ε·σ·(T² + T_surr²)(T + T_surr)

print(f"\nOuter surface radiates to room (surroundings at {T_amb}°C)")
print(f"  View factor F_out→surr ≈ 1 (convex surface to large enclosure)")

# =============================================================================
# ITERATIVE SOLUTION
# =============================================================================
print(f"\n{'='*75}")
print("ITERATIVE SOLUTION FOR COMPLETE THERMAL NETWORK")
print("=" * 75)

print("""
Thermal Network:

  T_cyl ──┬── R_conv,gap ──┬── R_ply ──┬── R_conv,ext ──┬── T_amb
          │                │           │                │
          └── R_rad,inner ─┘           └── R_rad,ext ───┘

  Where:
    R_conv,gap  = Natural convection in enclosed air
    R_rad,inner = Radiation: cylinder → inner plywood
    R_ply       = Conduction through plywood
    R_conv,ext  = Natural convection to ambient
    R_rad,ext   = Radiation: outer plywood → surroundings
""")

# Initial guesses
T2 = 50.0  # Inner plywood surface [°C]
T3 = 35.0  # Outer plywood surface [°C]

print(f"\nStarting iteration with T2={T2}°C, T3={T3}°C")
print("-" * 75)
print(f"{'Iter':>4} {'T2 [°C]':>10} {'T3 [°C]':>10} {'q [W/m]':>12} {'R_total':>12}")
print("-" * 75)

for iteration in range(20):
    T2_K = T2 + 273.15
    T3_K = T3 + 273.15

    # Update Rayleigh number based on actual ΔT
    dT_gap = T_cyl - T2
    if dT_gap > 1:
        Ra = g * beta * dT_gap * delta**3 / (nu * alpha_air)
        Nu = 0.046 * Ra**(1/3)
        k_eff = k_air * Nu
        R_conv_gap = 1 / (S * k_eff)

    # Inner radiation resistance (cylinder to inner plywood)
    # q_rad = σ(T1⁴-T2⁴) / rad_denom_inner
    # Linearized: h_rad = σ(T1⁴-T2⁴)/((T1-T2)·rad_denom_inner·A1)
    if abs(T_cyl - T2) > 0.1:
        h_rad_inner = sigma * (T_cyl_K**4 - T2_K**4) / ((T_cyl - T2) * rad_denom_inner * A_cyl)
    else:
        h_rad_inner = sigma * 4 * T2_K**3 / (rad_denom_inner * A_cyl)
    R_rad_inner = 1 / (h_rad_inner * A_cyl)

    # Combined air gap resistance (parallel conv + rad)
    R_gap = 1 / (1/R_conv_gap + 1/R_rad_inner)

    # External radiation resistance (outer plywood to surroundings)
    # For surface to large enclosure: q = ε·σ·A·(T³⁴-T_surr⁴)
    # Linearized: h_rad = ε·σ·(T3² + T_amb²)(T3 + T_amb)
    h_rad_ext = eps_ply * sigma * (T3_K**2 + T_amb_K**2) * (T3_K + T_amb_K)
    R_rad_ext = 1 / (h_rad_ext * A_out)

    # Combined external resistance (parallel conv + rad)
    R_ext = 1 / (1/R_conv_ext + 1/R_rad_ext)

    # Total resistance
    R_total = R_gap + R_ply + R_ext

    # Heat flux per unit length
    q_prime = (T_cyl - T_amb) / R_total

    # Update temperatures
    T2_new = T_cyl - q_prime * R_gap
    T3_new = T2_new - q_prime * R_ply

    print(f"{iteration+1:>4} {T2:>10.2f} {T3:>10.2f} {q_prime:>12.2f} {R_total:>12.4f}")

    # Check convergence
    if abs(T2_new - T2) < 0.01 and abs(T3_new - T3) < 0.01:
        T2, T3 = T2_new, T3_new
        print("-" * 75)
        print(f"Converged after {iteration+1} iterations!")
        break

    T2, T3 = T2_new, T3_new

# Final results
Q_total = q_prime * L_length

print(f"\n{'='*75}")
print("FINAL RESULTS (WITH ALL RADIATION PATHS)")
print("=" * 75)

print(f"\nTemperature Distribution:")
print(f"  T1 (cylinder surface):      {T_cyl:.1f}°C  ({T_cyl_K:.1f} K)")
print(f"  T2 (inner plywood):         {T2:.1f}°C  ({T2+273.15:.1f} K)")
print(f"  T3 (outer plywood):         {T3:.1f}°C  ({T3+273.15:.1f} K)")
print(f"  T4 (ambient):               {T_amb:.1f}°C  ({T_amb_K:.1f} K)")

print(f"\nThermal Resistances (per unit length):")
print(f"  Air gap - convection:       R_conv,gap  = {R_conv_gap:.4f} (m·K)/W")
print(f"  Air gap - radiation:        R_rad,inner = {R_rad_inner:.4f} (m·K)/W")
print(f"  Air gap - COMBINED:         R_gap       = {R_gap:.4f} (m·K)/W")
print(f"  Plywood conduction:         R_ply       = {R_ply:.4f} (m·K)/W")
print(f"  External - convection:      R_conv,ext  = {R_conv_ext:.4f} (m·K)/W")
print(f"  External - radiation:       R_rad,ext   = {R_rad_ext:.4f} (m·K)/W")
print(f"  External - COMBINED:        R_ext       = {R_ext:.4f} (m·K)/W")
print(f"  ─────────────────────────────────────────────────────")
print(f"  TOTAL:                      R_total     = {R_total:.4f} (m·K)/W")

print(f"\nHeat Transfer Coefficients:")
print(f"  Inner radiation h_rad,in:   {h_rad_inner:.2f} W/(m²·K)")
print(f"  External radiation h_rad,ex: {h_rad_ext:.2f} W/(m²·K)")
print(f"  External convection h_conv:  {h_conv_ext:.2f} W/(m²·K)")

print(f"\nHeat Loss:")
print(f"  Per unit length q':         {q_prime:.1f} W/m")
print(f"  For L = {L_length*100:.0f} cm:             Q = {Q_total:.1f} W")

# =============================================================================
# COMPARISON WITH SIMPLER MODELS
# =============================================================================
print(f"\n{'='*75}")
print("COMPARISON WITH SIMPLER MODELS")
print("=" * 75)

# Model 1: Convection only (no radiation anywhere)
R_total_conv_only = R_conv_gap + R_ply + R_conv_ext
q_conv_only = (T_cyl - T_amb) / R_total_conv_only
Q_conv_only = q_conv_only * L_length

# Model 2: Inner radiation only (original analysis)
R_gap_inner_rad = 1 / (1/R_conv_gap + 1/R_rad_inner)
R_total_inner_rad = R_gap_inner_rad + R_ply + R_conv_ext
q_inner_rad = (T_cyl - T_amb) / R_total_inner_rad
Q_inner_rad = q_inner_rad * L_length

# Model 3: Complete (both radiation paths) - already calculated
Q_complete = Q_total

print(f"\n{'Model':<35} {'R_total':>12} {'Q (30cm)':>12} {'vs Conv':>10}")
print("-" * 75)
print(f"{'1. Convection only':<35} {R_total_conv_only:>12.4f} {Q_conv_only:>10.1f} W {'(base)':>10}")
print(f"{'2. + Inner radiation':<35} {R_total_inner_rad:>12.4f} {Q_inner_rad:>10.1f} W {f'+{(Q_inner_rad/Q_conv_only-1)*100:.0f}%':>10}")
print(f"{'3. + External radiation (COMPLETE)':<35} {R_total:>12.4f} {Q_complete:>10.1f} W {f'+{(Q_complete/Q_conv_only-1)*100:.0f}%':>10}")

print(f"\n{'='*75}")
print("RESISTANCE BREAKDOWN BY COMPONENT")
print("=" * 75)

# For complete model
print(f"\n{'Component':<30} {'Resistance':>12} {'Fraction':>10} {'ΔT':>10}")
print("-" * 75)
R_gap_frac = R_gap / R_total * 100
R_ply_frac = R_ply / R_total * 100
R_ext_frac = R_ext / R_total * 100
dT_gap = q_prime * R_gap
dT_ply = q_prime * R_ply
dT_ext = q_prime * R_ext
print(f"{'Air gap (conv+rad)':<30} {R_gap:>12.4f} {R_gap_frac:>9.1f}% {dT_gap:>9.1f}°C")
print(f"{'Plywood conduction':<30} {R_ply:>12.4f} {R_ply_frac:>9.1f}% {dT_ply:>9.1f}°C")
print(f"{'External (conv+rad)':<30} {R_ext:>12.4f} {R_ext_frac:>9.1f}% {dT_ext:>9.1f}°C")
print("-" * 75)
print(f"{'TOTAL':<30} {R_total:>12.4f} {'100.0%':>10} {T_cyl-T_amb:>9.1f}°C")

print(f"\n{'='*75}")
print("EFFECT OF EACH RADIATION PATH")
print("=" * 75)

print(f"\n1. Inner Radiation (cylinder → inner plywood):")
print(f"   Without: R_gap = R_conv = {R_conv_gap:.4f} (m·K)/W")
print(f"   With:    R_gap = {R_gap:.4f} (m·K)/W")
print(f"   Reduction: {(1-R_gap/R_conv_gap)*100:.1f}%")

print(f"\n2. External Radiation (outer plywood → surroundings):")
print(f"   Without: R_ext = R_conv,ext = {R_conv_ext:.4f} (m·K)/W")
print(f"   With:    R_ext = {R_ext:.4f} (m·K)/W")
print(f"   Reduction: {(1-R_ext/R_conv_ext)*100:.1f}%")

print(f"\n{'='*75}")
print("SUMMARY")
print("=" * 75)
print(f"""
For a 25 cm diameter cylinder at 90°C in a plywood box with 10 cm air gap:

  ┌─────────────────────────────────────────────────────────────┐
  │  HEAT LOSS FOR 30 cm LENGTH:                                │
  │                                                             │
  │    Convection only:           {Q_conv_only:5.1f} W                      │
  │    + Inner radiation:         {Q_inner_rad:5.1f} W  (+{(Q_inner_rad/Q_conv_only-1)*100:.0f}%)              │
  │    + External radiation:      {Q_complete:5.1f} W  (+{(Q_complete/Q_conv_only-1)*100:.0f}% total)        │
  │                                                             │
  │  Adding external radiation increases heat loss by           │
  │  {(Q_complete/Q_inner_rad-1)*100:.0f}% compared to inner-radiation-only model.          │
  └─────────────────────────────────────────────────────────────┘

Temperature profile:  {T_cyl:.0f}°C → {T2:.0f}°C → {T3:.0f}°C → {T_amb:.0f}°C
                      (cyl)   (inner)  (outer)  (amb)
""")

# Save to file
with open('complete_analysis_results.txt', 'w') as f:
    f.write(f"Complete Heat Transfer Analysis Results\n")
    f.write(f"=" * 50 + "\n\n")
    f.write(f"Heat Loss for 30 cm:\n")
    f.write(f"  Convection only:        {Q_conv_only:.1f} W\n")
    f.write(f"  + Inner radiation:      {Q_inner_rad:.1f} W\n")
    f.write(f"  + External radiation:   {Q_complete:.1f} W (COMPLETE)\n\n")
    f.write(f"Temperature Distribution:\n")
    f.write(f"  Cylinder:      {T_cyl:.1f}°C\n")
    f.write(f"  Inner plywood: {T2:.1f}°C\n")
    f.write(f"  Outer plywood: {T3:.1f}°C\n")
    f.write(f"  Ambient:       {T_amb:.1f}°C\n")

print("\nResults saved to: complete_analysis_results.txt")
