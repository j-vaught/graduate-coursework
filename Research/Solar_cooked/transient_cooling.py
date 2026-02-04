#!/usr/bin/env python3
"""
Transient Cooling Analysis: Water in Cylinder inside Plywood Enclosure

The water starts at 90°C and cools over time as heat is lost through
the enclosure (convection + radiation).

Author: J.C. Vaught
"""

import numpy as np

# =============================================================================
# Physical Parameters
# =============================================================================
# Geometry
D_cyl = 0.25          # Cylinder diameter [m]
r_cyl = D_cyl / 2     # Cylinder radius [m]
L_cyl = 0.30          # Cylinder length [m]
delta = 0.10          # Air gap [m]
t_ply = 0.01          # Plywood thickness [m]

# Temperatures
T_initial = 90.0      # Initial water temperature [°C]
T_amb = 20.0          # Ambient temperature [°C]

# Water properties
rho_water = 1000      # Density [kg/m³]
cp_water = 4186       # Specific heat [J/(kg·K)]

# Calculate water volume and mass
V_water = np.pi * r_cyl**2 * L_cyl  # Full cylinder volume
print(f"Full cylinder volume: {V_water*1000:.2f} liters")

# Let user specify water volume
water_volumes = [5, 10, 15]  # liters to analyze

# Material properties (for resistance calculation)
k_air = 0.0283
k_ply = 0.12
sigma = 5.67e-8
eps_steel = 0.80
eps_ply = 0.90

# Geometry for resistances
w_in = 2 * (r_cyl + delta)
w_out = w_in + 2 * t_ply
A_cyl = np.pi * D_cyl * L_cyl      # Cylinder surface area [m²]
A_in = 4 * w_in * L_cyl            # Inner box surface [m²]
A_out = 4 * w_out * L_cyl          # Outer box surface [m²]

# Natural convection parameters
g = 9.81
beta = 3.05e-3
nu = 1.82e-5
alpha_air = 2.59e-5

# Shape factor (per unit length, then multiply by L)
S_per_m = 2 * np.pi / np.log(1.08 * w_in / D_cyl)
S = S_per_m * L_cyl

# External convection
h_conv_ext = 7.0

# Radiation denominator (inner)
term1 = (1 - eps_steel) / (eps_steel * A_cyl)
term2 = 1 / A_cyl
term3 = (1 - eps_ply) / (eps_ply * A_in)
rad_denom_inner = term1 + term2 + term3

print("=" * 75)
print("TRANSIENT COOLING ANALYSIS")
print("=" * 75)
print(f"\nGeometry:")
print(f"  Cylinder: D = {D_cyl*100:.0f} cm, L = {L_cyl*100:.0f} cm")
print(f"  Surface areas: A_cyl = {A_cyl:.4f} m², A_in = {A_in:.4f} m², A_out = {A_out:.4f} m²")

def calculate_thermal_resistance(T_water, T_amb):
    """
    Calculate total thermal resistance as function of temperatures.
    Returns R_total for the entire cylinder (not per unit length).
    """
    T_water_K = T_water + 273.15
    T_amb_K = T_amb + 273.15

    # Estimate intermediate temperatures (will iterate)
    T2 = 0.6 * T_water + 0.4 * T_amb  # Inner plywood estimate
    T3 = 0.3 * T_water + 0.7 * T_amb  # Outer plywood estimate
    T2_K = T2 + 273.15
    T3_K = T3 + 273.15

    # Air gap convection
    dT_gap = max(T_water - T2, 1)
    Ra = g * beta * dT_gap * delta**3 / (nu * alpha_air)
    Nu = 0.046 * Ra**(1/3) if Ra > 1000 else 1.0
    k_eff = k_air * Nu
    R_conv_gap = 1 / (S * k_eff)

    # Inner radiation
    if abs(T_water - T2) > 0.1:
        h_rad_inner = sigma * (T_water_K**4 - T2_K**4) / ((T_water - T2) * rad_denom_inner * A_cyl)
    else:
        h_rad_inner = sigma * 4 * T2_K**3 / (rad_denom_inner * A_cyl)
    h_rad_inner = max(h_rad_inner, 0.1)  # Prevent division by zero
    R_rad_inner = 1 / (h_rad_inner * A_cyl)

    # Combined air gap
    R_gap = 1 / (1/R_conv_gap + 1/R_rad_inner)

    # Plywood conduction
    R_ply = t_ply / (k_ply * A_in)

    # External convection
    R_conv_ext = 1 / (h_conv_ext * A_out)

    # External radiation
    h_rad_ext = eps_ply * sigma * (T3_K**2 + T_amb_K**2) * (T3_K + T_amb_K)
    h_rad_ext = max(h_rad_ext, 0.1)
    R_rad_ext = 1 / (h_rad_ext * A_out)

    # Combined external
    R_ext = 1 / (1/R_conv_ext + 1/R_rad_ext)

    # Total
    R_total = R_gap + R_ply + R_ext

    return R_total, R_gap, R_ply, R_ext

def simulate_cooling(V_liters, T_init, T_amb, t_max_hours=24, dt_seconds=60):
    """
    Simulate transient cooling using forward Euler method.

    dT/dt = -Q / (m * cp) = -(T - T_amb) / (R_total * m * cp)

    Returns time array and temperature array.
    """
    # Water mass
    V_m3 = V_liters / 1000  # Convert to m³
    m_water = rho_water * V_m3  # kg

    # Thermal capacitance
    C = m_water * cp_water  # J/K

    # Time parameters
    t_max = t_max_hours * 3600  # seconds
    n_steps = int(t_max / dt_seconds)

    # Arrays
    t = np.zeros(n_steps + 1)
    T = np.zeros(n_steps + 1)
    Q = np.zeros(n_steps + 1)
    R = np.zeros(n_steps + 1)

    # Initial conditions
    T[0] = T_init
    R[0], _, _, _ = calculate_thermal_resistance(T_init, T_amb)
    Q[0] = (T_init - T_amb) / R[0]

    # Time stepping
    for i in range(n_steps):
        # Current thermal resistance (temperature-dependent)
        R_total, _, _, _ = calculate_thermal_resistance(T[i], T_amb)
        R[i] = R_total

        # Heat loss rate [W]
        Q[i] = (T[i] - T_amb) / R_total

        # Temperature change
        dT = -Q[i] * dt_seconds / C

        # Update
        t[i+1] = t[i] + dt_seconds
        T[i+1] = T[i] + dT

        # Stop if very close to ambient
        if T[i+1] < T_amb + 0.1:
            T[i+1:] = T_amb
            t[i+1:] = t[i+1]
            break

    # Final values
    R[-1], _, _, _ = calculate_thermal_resistance(T[-1], T_amb)
    Q[-1] = (T[-1] - T_amb) / R[-1]

    return t, T, Q, R, m_water, C

# =============================================================================
# Run simulations for different water volumes
# =============================================================================
print(f"\n{'='*75}")
print("SIMULATION RESULTS")
print("=" * 75)

results = {}

for V in water_volumes:
    print(f"\n--- Water Volume: {V} liters ---")

    t, T, Q, R, m, C = simulate_cooling(V, T_initial, T_amb, t_max_hours=24)

    results[V] = {'t': t, 'T': T, 'Q': Q, 'R': R, 'm': m, 'C': C}

    # Find time to reach certain temperatures
    temps_of_interest = [80, 70, 60, 50, 40, 30, 25]

    print(f"  Water mass: {m:.2f} kg")
    print(f"  Thermal capacitance: {C/1000:.1f} kJ/K")
    print(f"  Initial heat loss: {Q[0]:.1f} W")
    print(f"  Initial thermal resistance: {R[0]:.4f} K/W")

    print(f"\n  Time to reach temperature:")
    for T_target in temps_of_interest:
        if T_target >= T_initial:
            continue
        idx = np.where(T <= T_target)[0]
        if len(idx) > 0:
            t_reach = t[idx[0]] / 3600  # Convert to hours
            print(f"    {T_target}°C: {t_reach:.2f} hours ({t_reach*60:.0f} min)")
        else:
            print(f"    {T_target}°C: > 24 hours")

# =============================================================================
# Calculate time constant
# =============================================================================
print(f"\n{'='*75}")
print("TIME CONSTANT ANALYSIS")
print("=" * 75)

print("""
For a first-order system: T(t) = T_amb + (T_init - T_amb) * exp(-t/τ)

Time constant τ = R * C = R_total * m * c_p

At t = τ: Temperature drops to 36.8% of initial ΔT above ambient
At t = 3τ: Temperature drops to 5% of initial ΔT (approximately at ambient)
""")

for V in water_volumes:
    m = results[V]['m']
    C = results[V]['C']
    R_avg = np.mean(results[V]['R'][:len(results[V]['R'])//2])  # Average R for first half

    tau = R_avg * C  # seconds
    tau_hours = tau / 3600

    # Temperature at t = tau
    T_at_tau = T_amb + (T_initial - T_amb) * np.exp(-1)

    print(f"\n{V} liters:")
    print(f"  Average R_total: {R_avg:.4f} K/W")
    print(f"  Thermal capacitance C: {C/1000:.1f} kJ/K")
    print(f"  Time constant τ = R·C = {tau:.0f} s = {tau_hours:.2f} hours")
    print(f"  At t = τ: T = {T_at_tau:.1f}°C")
    print(f"  At t = 3τ = {3*tau_hours:.1f} hours: T ≈ {T_amb + 0.05*(T_initial-T_amb):.1f}°C")

# =============================================================================
# Energy analysis
# =============================================================================
print(f"\n{'='*75}")
print("ENERGY ANALYSIS")
print("=" * 75)

for V in water_volumes:
    m = results[V]['m']

    # Total energy to cool from 90°C to 20°C
    E_total = m * cp_water * (T_initial - T_amb)  # Joules
    E_total_kWh = E_total / 3.6e6
    E_total_kJ = E_total / 1000

    print(f"\n{V} liters ({m:.1f} kg):")
    print(f"  Total thermal energy: {E_total_kJ:.1f} kJ = {E_total_kWh:.3f} kWh")
    print(f"  Initial heat loss rate: {results[V]['Q'][0]:.1f} W")
    print(f"  If constant rate: would take {E_total/results[V]['Q'][0]/3600:.1f} hours")
    print(f"  Actual time (exponential): ~{3*results[V]['R'][0]*results[V]['C']/3600:.1f} hours to reach ~25°C")

# =============================================================================
# Output data for plotting
# =============================================================================
print(f"\n{'='*75}")
print("DATA FOR LATEX PLOTTING")
print("=" * 75)

# Create data file for pgfplots
with open('cooling_data.dat', 'w') as f:
    f.write("# Time[hours] T_5L T_10L T_15L Q_5L Q_10L Q_15L\n")

    # Use common time points
    t_hours = np.linspace(0, 24, 145)  # Every 10 minutes

    for i, t_h in enumerate(t_hours):
        t_sec = t_h * 3600
        line = f"{t_h:.2f}"

        for V in water_volumes:
            # Interpolate temperature
            T_interp = np.interp(t_sec, results[V]['t'], results[V]['T'])
            line += f" {T_interp:.2f}"

        for V in water_volumes:
            # Interpolate heat loss
            Q_interp = np.interp(t_sec, results[V]['t'], results[V]['Q'])
            line += f" {Q_interp:.1f}"

        f.write(line + "\n")

print("Data saved to: cooling_data.dat")

# Also create a summary table
print(f"\n{'='*75}")
print("SUMMARY TABLE")
print("=" * 75)

print(f"\n{'Volume':<10} {'Mass':<8} {'τ':<12} {'t to 60°C':<12} {'t to 40°C':<12} {'t to 25°C':<12}")
print("-" * 75)

for V in water_volumes:
    m = results[V]['m']
    R_avg = np.mean(results[V]['R'][:len(results[V]['R'])//2])
    C = results[V]['C']
    tau = R_avg * C / 3600

    # Find times
    T = results[V]['T']
    t = results[V]['t']

    def time_to_temp(T_target):
        idx = np.where(T <= T_target)[0]
        if len(idx) > 0:
            return t[idx[0]] / 3600
        return float('inf')

    t_60 = time_to_temp(60)
    t_40 = time_to_temp(40)
    t_25 = time_to_temp(25)

    print(f"{V} L{'':<6} {m:.1f} kg{'':<2} {tau:.2f} hr{'':<5} {t_60:.2f} hr{'':<6} {t_40:.2f} hr{'':<6} {t_25:.2f} hr")

print(f"\n{'='*75}")
print("ANALYSIS COMPLETE")
print("=" * 75)
