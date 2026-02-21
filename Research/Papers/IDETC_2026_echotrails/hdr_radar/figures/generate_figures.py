"""
Generate placeholder figures for IDETC 2026 radar paper.
These simulate what actual data would look like.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch
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

# Radar colormap: black -> garnet -> white
radar_cmap = LinearSegmentedColormap.from_list(
    'radar', [BLACK, GARNET, '#CC2E40', WHITE], N=256
)

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.linewidth': 1.0,
    'axes.edgecolor': BLACK_90,
    'text.usetex': False,
    'figure.facecolor': WHITE,
    'axes.facecolor': WHITE,
})


def make_ppi_image(gain, n_az=360, n_range=200, seed=42):
    """Generate a synthetic PPI radar image at a given gain level."""
    rng = np.random.RandomState(seed)
    img = np.zeros((n_az, n_range))

    # Noise floor scales with gain
    noise_level = gain / 100.0 * 3.0
    img += rng.rayleigh(noise_level, (n_az, n_range))

    # Land mass (strong, extended target) at range 140-180, azimuth 30-90
    land_strength = 14.0
    for az in range(30, 90):
        r_start = 140 + int(5 * np.sin(az / 10.0))
        r_end = min(r_start + 30 + int(10 * np.sin(az / 5.0)), n_range)
        for r in range(r_start, r_end):
            falloff = 1.0 - 0.5 * (r - r_start) / max(r_end - r_start, 1)
            img[az, r] += land_strength * falloff * (gain / 50.0)

    # Buoy 1 (strong metal reflector) at range 80, azimuth 150
    buoy1_strength = 12.0
    for daz in range(-2, 3):
        for dr in range(-2, 3):
            dist = np.sqrt(daz**2 + dr**2)
            if dist < 3:
                img[150 + daz, 80 + dr] += buoy1_strength * (gain / 40.0) * (1 - dist / 3)

    # Buoy 2 (weaker, smaller) at range 85, azimuth 155 -- close to buoy 1
    buoy2_strength = 6.0
    for daz in range(-1, 2):
        for dr in range(-1, 2):
            dist = np.sqrt(daz**2 + dr**2)
            if dist < 2:
                img[155 + daz, 85 + dr] += buoy2_strength * (gain / 60.0) * (1 - dist / 2)

    # Buoy 3 (weak target) at range 120, azimuth 220
    buoy3_strength = 4.0
    for daz in range(-1, 2):
        for dr in range(-1, 2):
            dist = np.sqrt(daz**2 + dr**2)
            if dist < 2:
                img[220 + daz, 120 + dr] += buoy3_strength * (gain / 70.0) * (1 - dist / 2)

    # Clip to 4-bit (0-15)
    img = np.clip(img, 0, 15).astype(int)
    return img


def polar_to_cartesian(ppi, max_range=1.0):
    """Convert PPI (azimuth x range) to Cartesian for display."""
    n_az, n_range = ppi.shape
    size = 2 * n_range
    cart = np.zeros((size, size))
    cx, cy = n_range, n_range

    for ai in range(n_az):
        theta = 2 * np.pi * ai / n_az
        for ri in range(n_range):
            x = int(cx + ri * np.sin(theta))
            y = int(cy - ri * np.cos(theta))
            if 0 <= x < size and 0 <= y < size:
                cart[y, x] = max(cart[y, x], ppi[ai, ri])
    return cart


# =====================================================================
# FIGURE 1: The gain tradeoff problem (low gain vs high gain vs HDR)
# =====================================================================
print("Generating Figure 1: Gain tradeoff...")

fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))

for ax, (gain, title) in zip(axes, [(15, 'Low Gain (g=15)'),
                                      (85, 'High Gain (g=85)'),
                                      (None, 'HDR Composite')]):
    if gain is not None:
        ppi = make_ppi_image(gain)
    else:
        # HDR: composite across all gains, normalized
        composite = np.zeros((360, 200), dtype=float)
        for g in range(0, 101, 5):
            frame = make_ppi_image(g).astype(float)
            composite += frame
        composite = composite / composite.max() * 15
        ppi = composite.astype(int)

    cart = polar_to_cartesian(ppi)
    im = ax.imshow(cart, cmap=radar_cmap, vmin=0, vmax=15,
                   interpolation='bilinear', aspect='equal')
    ax.set_title(title, fontsize=11, fontweight='bold', color=BLACK_90)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines[:].set_visible(False)

    # Add range rings
    for r_frac in [0.25, 0.5, 0.75]:
        circle = plt.Circle((200, 200), r_frac * 200, fill=False,
                            color=BLACK_50, linewidth=0.5, linestyle='--')
        ax.add_patch(circle)

# Annotations
axes[0].annotate('Buoys\nresolved', xy=(220, 130), fontsize=7, color=WHITE,
                ha='center', fontstyle='italic')
axes[0].annotate('Weak buoy\nmissing', xy=(155, 280), fontsize=7, color=BLACK_50,
                ha='center', fontstyle='italic')

axes[1].annotate('Buoys\nmerged', xy=(220, 130), fontsize=7, color=WHITE,
                ha='center', fontstyle='italic')
axes[1].annotate('Weak buoy\nvisible', xy=(155, 280), fontsize=7, color=WHITE,
                ha='center', fontstyle='italic')

axes[2].annotate('Buoys\nresolved', xy=(220, 130), fontsize=7, color=WHITE,
                ha='center', fontstyle='italic')
axes[2].annotate('Weak buoy\nvisible', xy=(155, 280), fontsize=7, color=WHITE,
                ha='center', fontstyle='italic')

plt.tight_layout(pad=1.0)
plt.savefig('figures/fig1_gain_tradeoff.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig1_gain_tradeoff.png', dpi=300, bbox_inches='tight')
plt.close()


# =====================================================================
# FIGURE 2: Gain-response curves for different target types
# =====================================================================
print("Generating Figure 2: Gain-response curves...")

gains = np.arange(0, 101, 1)

# Metal buoy: strong reflector, appears early, saturates early
buoy_response = 15 * (1 - np.exp(-gains / 15.0))
buoy_response = np.clip(buoy_response, 0, 15)

# Weak buoy: appears later, saturates later
weak_buoy_response = 15 * (1 - np.exp(-(gains - 30) / 25.0))
weak_buoy_response = np.clip(weak_buoy_response, 0, 15)

# Land (diffuse): gradual ramp, slow saturation
land_response = 12 * (1 - np.exp(-gains / 40.0))
land_response = np.clip(land_response, 0, 15)

# Noise floor
noise_response = 3.0 * (gains / 100.0)**1.5
noise_response = np.clip(noise_response, 0, 15)

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(gains, buoy_response, color=GARNET, linewidth=2.5, label='Metal buoy (strong)')
ax.plot(gains, weak_buoy_response, color=ATLANTIC, linewidth=2.5, label='Metal buoy (weak)')
ax.plot(gains, land_response, color=HORSESHOE, linewidth=2.5, label='Land (diffuse)')
ax.plot(gains, noise_response, color=BLACK_50, linewidth=1.5, linestyle='--', label='Noise floor')

# 4-bit ceiling
ax.axhline(y=15, color=BLACK_30, linewidth=1, linestyle=':', label='4-bit ceiling (15)')

# Shade the single-gain window
ax.axvspan(55, 55, color=ROSE, alpha=0.3)
ax.axvline(x=55, color=ROSE, linewidth=1.5, linestyle='-', alpha=0.6, label='Typical fixed gain')

ax.set_xlabel('Receiver Gain Setting', fontsize=11, color=BLACK_90)
ax.set_ylabel('Digitized Intensity (4-bit)', fontsize=11, color=BLACK_90)
ax.set_title('Reflectivity-vs-Gain Response by Target Type', fontsize=12,
             fontweight='bold', color=BLACK_90)
ax.set_xlim(0, 100)
ax.set_ylim(0, 16.5)
ax.set_yticks(range(0, 16, 3))
ax.legend(loc='upper left', fontsize=8, framealpha=0.9)
ax.grid(True, alpha=0.3, color=BLACK_30)

plt.tight_layout()
plt.savefig('figures/fig2_gain_response_curves.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig2_gain_response_curves.png', dpi=300, bbox_inches='tight')
plt.close()


# =====================================================================
# FIGURE 3: Streaking artifact illustration (stationary vs moving)
# =====================================================================
print("Generating Figure 3: Motion streaking...")

fig, axes = plt.subplots(1, 2, figsize=(8, 4))

n_gains = 20
n_az, n_range = 100, 100

# Stationary target composite
stat_composite = np.zeros((n_az, n_range))
for g in range(n_gains):
    gain_frac = g / n_gains
    # Point target at fixed position
    for daz in range(-2, 3):
        for dr in range(-2, 3):
            dist = np.sqrt(daz**2 + dr**2)
            if dist < 3:
                az, r = 50 + daz, 50 + dr
                if 0 <= az < n_az and 0 <= r < n_range:
                    stat_composite[az, r] += 10 * gain_frac * (1 - dist / 3)

# Moving target composite (shifts position each gain step)
move_composite = np.zeros((n_az, n_range))
for g in range(n_gains):
    gain_frac = g / n_gains
    shift = int(g * 1.5)  # target moves in azimuth
    for daz in range(-2, 3):
        for dr in range(-2, 3):
            dist = np.sqrt(daz**2 + dr**2)
            if dist < 3:
                az = 50 + daz + shift
                r = 50 + dr
                if 0 <= az < n_az and 0 <= r < n_range:
                    move_composite[az, r] += 10 * gain_frac * (1 - dist / 3)

for ax, (data, title) in zip(axes, [(stat_composite, 'Stationary Target\n(coherent accumulation)'),
                                     (move_composite, 'Moving Target\n(streaking artifact)')]):
    ax.imshow(data, cmap=radar_cmap, interpolation='bilinear', aspect='equal')
    ax.set_title(title, fontsize=11, fontweight='bold', color=BLACK_90)
    ax.set_xlabel('Range bin', fontsize=9, color=BLACK_70)
    ax.set_ylabel('Azimuth bin', fontsize=9, color=BLACK_70)

plt.tight_layout(pad=1.5)
plt.savefig('figures/fig3_streaking.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig3_streaking.png', dpi=300, bbox_inches='tight')
plt.close()


# =====================================================================
# FIGURE 4: Temporal filtering illustration (blink patterns)
# =====================================================================
print("Generating Figure 4: Temporal filtering...")

fig, axes = plt.subplots(2, 1, figsize=(8, 4), gridspec_kw={'height_ratios': [1, 1]})

n_scans = 60
rng = np.random.RandomState(123)

# Buoy 1 (strong, persistent with occasional drops)
buoy1_presence = np.ones(n_scans)
drops = rng.choice(n_scans, size=5, replace=False)
buoy1_presence[drops] = 0

# Buoy 2 (weaker, intermittent -- blinks frequently)
buoy2_presence = (rng.random(n_scans) > 0.4).astype(float)

# Merged signal (what you see at high gain)
merged = np.maximum(buoy1_presence, buoy2_presence)

ax = axes[0]
scans = np.arange(n_scans)
ax.fill_between(scans, 0, merged * 15, color=BLACK_30, alpha=0.3, step='mid', label='Merged region')
ax.step(scans, buoy1_presence * 14, where='mid', color=GARNET, linewidth=2, label='Buoy A (strong)')
ax.step(scans, buoy2_presence * 10, where='mid', color=ATLANTIC, linewidth=2, label='Buoy B (weak)')
ax.set_ylabel('Intensity', fontsize=9, color=BLACK_70)
ax.set_title('Temporal Return Patterns at Fixed High Gain', fontsize=11,
             fontweight='bold', color=BLACK_90)
ax.legend(loc='upper right', fontsize=8, ncol=3)
ax.set_xlim(0, n_scans - 1)
ax.set_ylim(0, 17)
ax.set_xticklabels([])
ax.grid(True, alpha=0.2, color=BLACK_30)

# Correlation / separation metric
ax2 = axes[1]
window = 10
buoy1_frac = np.convolve(buoy1_presence, np.ones(window)/window, mode='same')
buoy2_frac = np.convolve(buoy2_presence, np.ones(window)/window, mode='same')
separation = np.abs(buoy1_frac - buoy2_frac)

ax2.fill_between(scans, 0, separation, color=HORSESHOE, alpha=0.4)
ax2.plot(scans, separation, color=HORSESHOE, linewidth=2)
ax2.axhline(y=0.3, color=ROSE, linewidth=1.5, linestyle='--', label='Separation threshold')
ax2.set_xlabel('Scan Number', fontsize=9, color=BLACK_70)
ax2.set_ylabel('Temporal\nSeparation', fontsize=9, color=BLACK_70)
ax2.legend(loc='upper right', fontsize=8)
ax2.set_xlim(0, n_scans - 1)
ax2.set_ylim(0, 1.0)
ax2.grid(True, alpha=0.2, color=BLACK_30)

plt.tight_layout(pad=1.0)
plt.savefig('figures/fig4_temporal_filtering.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig4_temporal_filtering.png', dpi=300, bbox_inches='tight')
plt.close()


# =====================================================================
# FIGURE 5: Method comparison summary (3-panel: gain sweep, gain+PW, temporal)
# =====================================================================
print("Generating Figure 5: Method comparison...")

fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))

# Simulated effective dynamic range bar chart for each method
methods = ['Single Frame\n(Fixed Gain)', 'Gain Sweep\n(48 RPM)', 'Gain + PW\n(24 RPM)']
eff_bits = [4, 10.5, 12.8]
colors = [BLACK_50, GARNET, ATLANTIC]

ax = axes[0]
bars = ax.bar(methods, eff_bits, color=colors, width=0.6, edgecolor=BLACK_90, linewidth=0.8)
ax.set_ylabel('Effective Dynamic Range (bits)', fontsize=9, color=BLACK_70)
ax.set_title('Dynamic Range Extension', fontsize=11, fontweight='bold', color=BLACK_90)
ax.set_ylim(0, 16)
ax.axhline(y=4, color=BLACK_30, linewidth=1, linestyle=':')
ax.text(0.02, 4.3, 'Native 4-bit', fontsize=7, color=BLACK_50, transform=ax.get_yaxis_transform())
for bar, val in zip(bars, eff_bits):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.3, f'{val:.1f}',
            ha='center', fontsize=9, fontweight='bold', color=BLACK_90)
ax.grid(True, axis='y', alpha=0.2, color=BLACK_30)

# Sweep time comparison
ax2 = axes[1]
methods2 = ['Gain Sweep', 'Gain + PW', 'Temporal\nFilter']
sweep_times = [2.1, 8.4, 5.0]  # seconds for complete acquisition
colors2 = [GARNET, ATLANTIC, HORSESHOE]
bars2 = ax2.bar(methods2, sweep_times, color=colors2, width=0.6, edgecolor=BLACK_90, linewidth=0.8)
ax2.set_ylabel('Acquisition Time (s)', fontsize=9, color=BLACK_70)
ax2.set_title('Time per Complete Sweep', fontsize=11, fontweight='bold', color=BLACK_90)
ax2.grid(True, axis='y', alpha=0.2, color=BLACK_30)
for bar, val in zip(bars2, sweep_times):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 0.2, f'{val:.1f}s',
            ha='center', fontsize=9, fontweight='bold', color=BLACK_90)

# Motion tolerance
ax3 = axes[2]
methods3 = ['Gain\nSweep', 'Gain\n+ PW', 'Temporal\nFilter']
scores = [2, 1, 5]  # 1-5 scale
colors3 = [GARNET, ATLANTIC, HORSESHOE]
bars3 = ax3.bar(methods3, scores, color=colors3, width=0.6, edgecolor=BLACK_90, linewidth=0.8)
ax3.set_ylabel('Motion Tolerance (1-5)', fontsize=9, color=BLACK_70)
ax3.set_title('Moving Target Compatibility', fontsize=11, fontweight='bold', color=BLACK_90)
ax3.set_ylim(0, 6)
ax3.grid(True, axis='y', alpha=0.2, color=BLACK_30)
labels3 = ['Streaking', 'Severe\nstreaking', 'No\nartifacts']
for bar, val, lbl in zip(bars3, scores, labels3):
    ax3.text(bar.get_x() + bar.get_width()/2, val + 0.2, lbl,
            ha='center', fontsize=7, color=BLACK_70)

plt.tight_layout(pad=1.5)
plt.savefig('figures/fig5_method_comparison.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig5_method_comparison.png', dpi=300, bbox_inches='tight')
plt.close()


# =====================================================================
# FIGURE 6: System diagram (hardware setup)
# =====================================================================
print("Generating Figure 6: System diagram...")

fig, ax = plt.subplots(figsize=(8, 3))
ax.set_xlim(0, 10)
ax.set_ylim(0, 3)
ax.axis('off')

boxes = [
    (0.5, 1.0, 2.0, 1.0, 'X-Band\nRadar', GARNET),
    (3.5, 1.0, 2.0, 1.0, 'GINA\nController', ATLANTIC),
    (6.5, 1.0, 2.0, 1.0, 'Data\nAcquisition', CONGAREE),
]

for x, y, w, h, label, color in boxes:
    rect = plt.Rectangle((x, y), w, h, facecolor=color, edgecolor=BLACK_90,
                         linewidth=1.5, alpha=0.9)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, label, ha='center', va='center',
            fontsize=11, fontweight='bold', color=WHITE)

# Arrows
arrow_style = dict(arrowstyle='->', color=BLACK_90, linewidth=2, mutation_scale=15)
ax.annotate('', xy=(3.5, 1.5), xytext=(2.5, 1.5), arrowprops=arrow_style)
ax.annotate('', xy=(6.5, 1.5), xytext=(5.5, 1.5), arrowprops=arrow_style)

# Labels on arrows
ax.text(3.0, 1.85, 'Gain/PW\ncommands', ha='center', fontsize=7, color=BLACK_70)
ax.text(6.0, 1.85, '4-bit\nreturns', ha='center', fontsize=7, color=BLACK_70)

# Feedback loop
ax.annotate('', xy=(4.5, 1.0), xytext=(7.5, 1.0),
            arrowprops=dict(arrowstyle='->', color=ROSE, linewidth=1.5,
                          connectionstyle='arc3,rad=0.4', mutation_scale=12))
ax.text(6.0, 0.35, 'Sweep schedule', ha='center', fontsize=7, color=ROSE, fontstyle='italic')

plt.tight_layout()
plt.savefig('figures/fig6_system_diagram.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig6_system_diagram.png', dpi=300, bbox_inches='tight')
plt.close()


# =====================================================================
# FIGURE 7: Gain sweep waterfall (gain vs azimuth intensity strip)
# =====================================================================
print("Generating Figure 7: Gain sweep waterfall...")

fig, ax = plt.subplots(figsize=(7, 4))

n_gains_wf = 50
azimuth_slice = np.zeros((n_gains_wf, 200))

for gi, g in enumerate(np.linspace(0, 100, n_gains_wf)):
    ppi = make_ppi_image(g)
    # Take azimuth slice at az=150 (through the buoys)
    azimuth_slice[gi, :] = ppi[150, :]

im = ax.imshow(azimuth_slice, cmap=radar_cmap, aspect='auto',
               extent=[0, 200, 100, 0], interpolation='bilinear')
ax.set_xlabel('Range Bin', fontsize=11, color=BLACK_90)
ax.set_ylabel('Gain Setting', fontsize=11, color=BLACK_90)
ax.set_title('Gain Sweep Waterfall (Azimuth = 150°)', fontsize=12,
             fontweight='bold', color=BLACK_90)

cbar = plt.colorbar(im, ax=ax, label='4-bit Intensity')
cbar.set_label('4-bit Intensity', fontsize=9, color=BLACK_70)

# Annotate targets
ax.annotate('Buoy\n(saturates early)', xy=(80, 25), fontsize=8, color=WHITE,
           ha='center', fontstyle='italic')

plt.tight_layout()
plt.savefig('figures/fig7_waterfall.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig7_waterfall.png', dpi=300, bbox_inches='tight')
plt.close()

print("All figures generated successfully.")
