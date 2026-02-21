"""
Generate expected/theoretical results figures for IDETC 2026 radar paper.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Brand colors
GARNET = '#73000A'
BLACK = '#000000'
WHITE = '#FFFFFF'
BLACK_90 = '#363636'
BLACK_70 = '#5C5C5C'
BLACK_50 = '#A2A2A2'
BLACK_30 = '#C7C7C7'
BLACK_10 = '#ECECEC'
ATLANTIC = '#466A9F'
CONGAREE = '#1F414D'
HORSESHOE = '#65780B'
ROSE = '#CC2E40'
HONEYCOMB = '#A49137'
GRASS = '#CED318'

radar_cmap = LinearSegmentedColormap.from_list(
    'radar', [BLACK, GARNET, '#CC2E40', WHITE], N=256
)

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.linewidth': 1.0,
    'axes.edgecolor': BLACK_90,
    'figure.facecolor': WHITE,
    'axes.facecolor': WHITE,
})


# =====================================================================
# FIGURE 8: Repeatability across 3 gain sweeps
# =====================================================================
print("Generating Figure 8: Repeatability...")

rng = np.random.RandomState(42)
gains = np.arange(0, 101, 1)

# Metal buoy true curve
buoy_true = 15 * (1 - np.exp(-gains / 15.0))
buoy_true = np.clip(buoy_true, 0, 15)

fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))

# Left: 3 overlaid sweeps for buoy
ax = axes[0]
for i, (label, color, ls) in enumerate(zip(
    ['Sweep 1', 'Sweep 2', 'Sweep 3'],
    [GARNET, ATLANTIC, HORSESHOE],
    ['-', '--', ':']
)):
    noise = rng.normal(0, 0.4, len(gains))
    curve = np.clip(buoy_true + noise, 0, 15).astype(int)
    ax.plot(gains, curve, color=color, linewidth=1.8, linestyle=ls, label=label, alpha=0.85)

ax.fill_between(gains,
                np.clip(buoy_true - 1.0, 0, 15),
                np.clip(buoy_true + 1.0, 0, 15),
                color=BLACK_30, alpha=0.2, label='$\\pm 1\\sigma$ envelope')
ax.set_xlabel('Gain Setting', fontsize=10, color=BLACK_90)
ax.set_ylabel('Digitized Intensity', fontsize=10, color=BLACK_90)
ax.set_title('Metal Buoy (3 Sweeps)', fontsize=11, fontweight='bold', color=BLACK_90)
ax.legend(fontsize=7, loc='lower right')
ax.set_xlim(0, 100)
ax.set_ylim(0, 16.5)
ax.grid(True, alpha=0.2, color=BLACK_30)

# Right: 3 overlaid sweeps for land
land_true = 12 * (1 - np.exp(-gains / 40.0))
land_true = np.clip(land_true, 0, 15)

ax2 = axes[1]
for i, (label, color, ls) in enumerate(zip(
    ['Sweep 1', 'Sweep 2', 'Sweep 3'],
    [GARNET, ATLANTIC, HORSESHOE],
    ['-', '--', ':']
)):
    noise = rng.normal(0, 0.6, len(gains))
    curve = np.clip(land_true + noise, 0, 15).astype(int)
    ax2.plot(gains, curve, color=color, linewidth=1.8, linestyle=ls, label=label, alpha=0.85)

ax2.fill_between(gains,
                 np.clip(land_true - 1.5, 0, 15),
                 np.clip(land_true + 1.5, 0, 15),
                 color=BLACK_30, alpha=0.2, label='$\\pm 1\\sigma$ envelope')
ax2.set_xlabel('Gain Setting', fontsize=10, color=BLACK_90)
ax2.set_ylabel('Digitized Intensity', fontsize=10, color=BLACK_90)
ax2.set_title('Land Feature (3 Sweeps)', fontsize=11, fontweight='bold', color=BLACK_90)
ax2.legend(fontsize=7, loc='lower right')
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 16.5)
ax2.grid(True, alpha=0.2, color=BLACK_30)

plt.tight_layout(pad=1.0)
plt.savefig('figures/fig8_repeatability.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig8_repeatability.png', dpi=300, bbox_inches='tight')
plt.close()


# =====================================================================
# FIGURE 9: Pulse width comparison (6 PW settings, gain-response curves)
# =====================================================================
print("Generating Figure 9: Pulse width comparison...")

pw_labels = ['S1', 'S2', 'M1', 'M2', 'M3', 'L']
pw_colors = [GARNET, ROSE, ATLANTIC, CONGAREE, HORSESHOE, HONEYCOMB]

# Longer pulse = more energy on target = steeper response
# Model: onset shifts earlier and saturation shifts earlier with longer pulse
pw_energy_factors = [0.5, 0.65, 0.8, 0.9, 1.0, 1.3]

fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))

# Left: buoy response at each PW
ax = axes[0]
for pw, factor, color, label in zip(range(6), pw_energy_factors, pw_colors, pw_labels):
    response = 15 * (1 - np.exp(-gains * factor / 15.0))
    response = np.clip(response, 0, 15)
    ax.plot(gains, response, color=color, linewidth=1.8, label=label)

ax.set_xlabel('Gain Setting', fontsize=10, color=BLACK_90)
ax.set_ylabel('Digitized Intensity', fontsize=10, color=BLACK_90)
ax.set_title('Metal Buoy by Pulse Width', fontsize=11, fontweight='bold', color=BLACK_90)
ax.legend(fontsize=7, title='PW', title_fontsize=7, loc='lower right', ncol=2)
ax.set_xlim(0, 100)
ax.set_ylim(0, 16.5)
ax.grid(True, alpha=0.2, color=BLACK_30)

# Right: land response at each PW
ax2 = axes[1]
for pw, factor, color, label in zip(range(6), pw_energy_factors, pw_colors, pw_labels):
    response = 12 * (1 - np.exp(-gains * factor / 40.0))
    response = np.clip(response, 0, 15)
    ax2.plot(gains, response, color=color, linewidth=1.8, label=label)

ax2.set_xlabel('Gain Setting', fontsize=10, color=BLACK_90)
ax2.set_ylabel('Digitized Intensity', fontsize=10, color=BLACK_90)
ax2.set_title('Land Feature by Pulse Width', fontsize=11, fontweight='bold', color=BLACK_90)
ax2.legend(fontsize=7, title='PW', title_fontsize=7, loc='lower right', ncol=2)
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 16.5)
ax2.grid(True, alpha=0.2, color=BLACK_30)

plt.tight_layout(pad=1.0)
plt.savefig('figures/fig9_pulse_width_comparison.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig9_pulse_width_comparison.png', dpi=300, bbox_inches='tight')
plt.close()


# =====================================================================
# FIGURE 10: Effective dynamic range vs number of gain steps
# =====================================================================
print("Generating Figure 10: Dynamic range vs gain steps...")

fig, ax = plt.subplots(figsize=(5, 3.5))

# Show onset, saturation, span, and resolvable levels for different targets
fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))

gains_cal = np.arange(0, 101, 1)

# Left panel: gain-response curves with onset/sat/span annotated
ax = axes[0]

targets = [
    (8, 35, 'Strong buoy', GARNET),
    (30, 72, 'Weak buoy', ATLANTIC),
    (18, 85, 'Land (diffuse)', HORSESHOE),
]

for onset, sat, label, color in targets:
    span = sat - onset
    # Build a realistic curve (saturating exponential within the span)
    response = np.zeros_like(gains_cal, dtype=float)
    for i, g in enumerate(gains_cal):
        if g < onset:
            response[i] = 0
        elif g > sat:
            response[i] = 15
        else:
            t = (g - onset) / (sat - onset)
            response[i] = int(15 * (1 - np.exp(-3 * t)) / (1 - np.exp(-3)))
    # Count distinct intensity levels
    L = len(set(int(v) for v in response if 0 < v < 15)) + 2  # include 0 and 15
    R = L / 16.0
    ax.plot(gains_cal, response, color=color, linewidth=2,
            label=f'{label}\n  S={span}, L={L}, R={R:.1f}x')
    # Mark onset and saturation
    ax.plot(onset, 0, 'v', color=color, markersize=8, zorder=5)
    ax.plot(sat, 15, '^', color=color, markersize=8, zorder=5)
    # Draw span bracket
    ax.annotate('', xy=(sat, -0.8), xytext=(onset, -0.8),
               arrowprops=dict(arrowstyle='<->', color=color, linewidth=1.5))

ax.axhline(y=15, color=BLACK_30, linewidth=1, linestyle=':')
ax.axhline(y=0, color=BLACK_30, linewidth=1, linestyle=':')
ax.set_xlabel('Gain Setting', fontsize=10, color=BLACK_90)
ax.set_ylabel('Digitized Intensity', fontsize=10, color=BLACK_90)
ax.set_title('Onset, Saturation, and Span\nby Target Type', fontsize=11,
             fontweight='bold', color=BLACK_90)
ax.legend(fontsize=6.5, loc='center right')
ax.set_xlim(0, 100)
ax.set_ylim(-2.5, 17)
ax.grid(True, alpha=0.2, color=BLACK_30)

# Right panel: resolution improvement factor comparison
ax2 = axes[1]

methods = ['Single\nFrame', 'Gain\nSweep']
target_names = ['Strong buoy', 'Weak buoy', 'Land']
target_colors = [GARNET, ATLANTIC, HORSESHOE]

# Single frame: always 16 levels max, but realistically fewer
# (target may be saturated or below noise, so maybe 3-8 useful levels)
single_frame_levels = [6, 3, 10]  # typical useful levels at a single gain

# Gain sweep: L values from the curves above
sweep_levels = []
for onset, sat, label, color in targets:
    response = np.zeros(101, dtype=float)
    for i, g in enumerate(range(101)):
        if g < onset:
            response[i] = 0
        elif g > sat:
            response[i] = 15
        else:
            t = (g - onset) / (sat - onset)
            response[i] = int(15 * (1 - np.exp(-3 * t)) / (1 - np.exp(-3)))
    L = len(set(int(v) for v in response))
    sweep_levels.append(L)

x = np.arange(len(target_names))
width = 0.3
bars1 = ax2.bar(x - width/2, single_frame_levels, width, color=[c + '80' for c in target_colors],
               edgecolor=BLACK_90, linewidth=0.8, label='Single frame')
bars2 = ax2.bar(x + width/2, sweep_levels, width, color=target_colors,
               edgecolor=BLACK_90, linewidth=0.8, label='Gain sweep')

for bar, val in zip(bars1, single_frame_levels):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 0.3, str(val),
            ha='center', fontsize=8, color=BLACK_70)
for bar, val in zip(bars2, sweep_levels):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 0.3, str(val),
            ha='center', fontsize=8, fontweight='bold', color=BLACK_90)

ax2.set_ylabel('Resolvable Intensity Levels', fontsize=10, color=BLACK_90)
ax2.set_title('Resolution Improvement\n(Single Frame vs. Gain Sweep)', fontsize=11,
             fontweight='bold', color=BLACK_90)
ax2.set_xticks(x)
ax2.set_xticklabels(target_names, fontsize=9)
ax2.legend(fontsize=8, loc='upper right')
ax2.grid(True, axis='y', alpha=0.2, color=BLACK_30)
ax2.set_ylim(0, max(sweep_levels) + 4)

plt.tight_layout()
plt.savefig('figures/fig10_dynamic_range_scaling.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig10_dynamic_range_scaling.png', dpi=300, bbox_inches='tight')
plt.close()


# =====================================================================
# FIGURE 11: Merge/resolve threshold diagram
# =====================================================================
print("Generating Figure 11: Merge threshold...")

fig, ax = plt.subplots(figsize=(6, 3.5))

gains_plot = np.arange(0, 101, 1)

# Two buoys: at low gain, both below saturation and resolved
# As gain increases, both saturate and their returns overlap
buoy_a_size = 1.0 + 4.0 * (gains_plot / 100)**1.5  # apparent size in range bins
buoy_b_size = 0.5 + 3.5 * (gains_plot / 100)**1.5
separation = 5.0  # fixed physical separation in range bins

gap = separation - (buoy_a_size / 2 + buoy_b_size / 2)
gap = np.clip(gap, -3, 5)

ax.plot(gains_plot, gap, color=GARNET, linewidth=2.5)
ax.axhline(y=0, color=ROSE, linewidth=2, linestyle='--', label='Merge threshold')
ax.fill_between(gains_plot, gap, 0, where=(gap < 0), color=ROSE, alpha=0.15, label='Merged region')
ax.fill_between(gains_plot, gap, 0, where=(gap >= 0), color=HORSESHOE, alpha=0.15, label='Resolved region')

# Find merge point
merge_idx = np.where(gap < 0)[0]
if len(merge_idx) > 0:
    merge_gain = gains_plot[merge_idx[0]]
    ax.axvline(x=merge_gain, color=BLACK_50, linewidth=1, linestyle=':')
    ax.annotate(f'Merge at g={merge_gain}', xy=(merge_gain, 0.3),
               fontsize=9, color=BLACK_70, ha='center')

ax.set_xlabel('Gain Setting', fontsize=10, color=BLACK_90)
ax.set_ylabel('Inter-Target Gap (range bins)', fontsize=10, color=BLACK_90)
ax.set_title('Target Merge Threshold vs. Gain', fontsize=11,
             fontweight='bold', color=BLACK_90)
ax.legend(fontsize=8, loc='upper right')
ax.set_xlim(0, 100)
ax.grid(True, alpha=0.2, color=BLACK_30)

plt.tight_layout()
plt.savefig('figures/fig11_merge_threshold.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig11_merge_threshold.png', dpi=300, bbox_inches='tight')
plt.close()


# =====================================================================
# FIGURE 12: Temporal detection probability histogram
# =====================================================================
print("Generating Figure 12: Detection probability...")

rng = np.random.RandomState(99)

fig, ax = plt.subplots(figsize=(5, 3.5))

# Simulated detection probabilities for different target types
n_targets = 20
# Strong buoys: high detection prob (0.85-1.0)
strong_probs = rng.uniform(0.85, 1.0, 5)
# Weak buoys: variable (0.3-0.7)
weak_probs = rng.uniform(0.3, 0.7, 5)
# Land features: very high (0.95-1.0)
land_probs = rng.uniform(0.95, 1.0, 10)

bins = np.linspace(0, 1, 21)

ax.hist(strong_probs, bins=bins, color=GARNET, alpha=0.7, label='Strong buoy', edgecolor=BLACK_90)
ax.hist(weak_probs, bins=bins, color=ATLANTIC, alpha=0.7, label='Weak buoy', edgecolor=BLACK_90)
ax.hist(land_probs, bins=bins, color=HORSESHOE, alpha=0.7, label='Land', edgecolor=BLACK_90)

ax.axvline(x=0.8, color=ROSE, linewidth=2, linestyle='--', label='Persistent threshold')
ax.set_xlabel('Detection Probability (at fixed high gain)', fontsize=10, color=BLACK_90)
ax.set_ylabel('Count', fontsize=10, color=BLACK_90)
ax.set_title('Temporal Detection Probability by Target Type', fontsize=11,
             fontweight='bold', color=BLACK_90)
ax.legend(fontsize=8)
ax.set_xlim(0, 1.05)
ax.grid(True, axis='y', alpha=0.2, color=BLACK_30)

plt.tight_layout()
plt.savefig('figures/fig12_detection_probability.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig12_detection_probability.png', dpi=300, bbox_inches='tight')
plt.close()


print("All results figures generated successfully.")
