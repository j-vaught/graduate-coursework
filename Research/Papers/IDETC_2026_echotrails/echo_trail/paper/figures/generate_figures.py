"""
Generate placeholder figures for the echo trails IDETC 2026 paper.
Uses brand colors per CLAUDE.md specifications.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

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

OUTDIR = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    'font.size': 10,
    'axes.linewidth': 1.0,
    'axes.edgecolor': BLACK_90,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
})


def fig0_splash():
    """Splash figure: same scene under 4 trail configs with YOLO bbox overlays."""
    fig, axes = plt.subplots(1, 4, figsize=(7, 2.4))
    titles = ['No Trails\n(Missed Detection)',
              'Short Trails ($N\\!=\\!6$)\n(Correct Detection)',
              'Long Trails ($N\\!=\\!24$)\n(Oversized Box)',
              'Crossing Trails\n(Merged Targets)']
    bbox_colors = [ROSE, HORSESHOE, HONEYCOMB, ROSE]

    np.random.seed(42)
    size = 200

    for idx, (ax, title, bcolor) in enumerate(zip(axes, titles, bbox_colors)):
        # Dark background with clutter
        img = np.zeros((size, size, 3))
        noise = np.random.exponential(0.04, (size, size))
        img[:, :, 1] = noise * 0.5  # green channel noise

        # Stationary buoy target at upper-left area
        buoy_y, buoy_x = 55, 60
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dy**2 + dx**2 <= 9:
                    img[buoy_y + dy, buoy_x + dx, 1] = 0.7

        # Moving vessel target at center-right
        vessel_y, vessel_x = 100, 140
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                if dy**2 + dx**2 <= 16:
                    img[vessel_y + dy, vessel_x + dx, 1] = 0.95

        if idx == 0:
            # No trails - buoy is faint, might be missed
            # Dim the buoy to simulate missed detection
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    if dy**2 + dx**2 <= 9:
                        img[buoy_y + dy, buoy_x + dx, 1] = 0.15

        elif idx == 1:
            # Short trails - nice reinforcement
            for dk in range(1, 7):
                w = np.exp(-dk / 2)
                for dy in range(-4, 5):
                    for dx in range(-4, 5):
                        if dy**2 + dx**2 <= 16:
                            ny = vessel_y + dk * 2
                            if 0 <= ny + dy < size:
                                img[ny + dy, vessel_x + dx, 1] = max(img[ny + dy, vessel_x + dx, 1], 0.9 * w)
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        if dy**2 + dx**2 <= 9:
                            img[buoy_y + dy, buoy_x + dx, 1] = max(img[buoy_y + dy, buoy_x + dx, 1], 0.7 * (1 + 0.2))

        elif idx == 2:
            # Long trails - vessel becomes a long streak
            for dk in range(1, 25):
                w = 1 - dk / 24
                for dy in range(-4, 5):
                    for dx in range(-4, 5):
                        if dy**2 + dx**2 <= 16:
                            ny = vessel_y + dk * 2
                            if 0 <= ny + dy < size:
                                img[ny + dy, vessel_x + dx, 1] = max(img[ny + dy, vessel_x + dx, 1], 0.9 * w)
            # Buoy also brighter
            for dy in range(-4, 5):
                for dx in range(-4, 5):
                    if dy**2 + dx**2 <= 16:
                        img[buoy_y + dy, buoy_x + dx, 1] = min(1.0, 0.85)

        elif idx == 3:
            # Two crossing targets with overlapping trails
            t1_y, t1_x = 80, 110
            t2_y, t2_x = 120, 110
            for dy in range(-4, 5):
                for dx in range(-4, 5):
                    if dy**2 + dx**2 <= 16:
                        img[t1_y + dy, t1_x + dx, 1] = 0.95
                        img[t2_y + dy, t2_x + dx, 1] = 0.95
            # Trails that converge
            for dk in range(1, 16):
                w = 1 - dk / 16
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        if dy**2 + dx**2 <= 9:
                            # Target 1 trail going down-right
                            ny1 = t1_y + dk * 2
                            nx1 = t1_x + dk
                            # Target 2 trail going up-right
                            ny2 = t2_y - dk * 2
                            nx2 = t2_x + dk
                            if 0 <= ny1 + dy < size and 0 <= nx1 + dx < size:
                                img[ny1 + dy, nx1 + dx, 1] = max(img[ny1 + dy, nx1 + dx, 1], 0.85 * w)
                            if 0 <= ny2 + dy < size and 0 <= nx2 + dx < size:
                                img[ny2 + dy, nx2 + dx, 1] = max(img[ny2 + dy, nx2 + dx, 1], 0.85 * w)

        ax.imshow(np.clip(img, 0, 1), interpolation='nearest', aspect='equal')
        ax.set_title(title, fontsize=7, fontweight='bold', linespacing=1.1)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_linewidth(1)
            spine.set_color(BLACK_90)

        # Draw YOLO-style bounding boxes
        import matplotlib.patches as patches
        if idx == 0:
            # Only vessel detected, buoy missed
            rect = patches.Rectangle((vessel_x - 8, vessel_y - 8), 16, 16,
                                     linewidth=1.5, edgecolor=HORSESHOE, facecolor='none')
            ax.add_patch(rect)
            ax.text(vessel_x - 8, vessel_y - 10, 'vessel', fontsize=5, color=HORSESHOE, fontweight='bold')
            # X mark where buoy should be
            ax.plot(buoy_x, buoy_y, 'x', color=ROSE, markersize=8, markeredgewidth=2)
            ax.text(buoy_x + 5, buoy_y - 2, '?', fontsize=7, color=ROSE, fontweight='bold')

        elif idx == 1:
            # Both detected correctly
            rect1 = patches.Rectangle((buoy_x - 7, buoy_y - 7), 14, 14,
                                      linewidth=1.5, edgecolor=HORSESHOE, facecolor='none')
            rect2 = patches.Rectangle((vessel_x - 8, vessel_y - 8), 16, 16,
                                      linewidth=1.5, edgecolor=HORSESHOE, facecolor='none')
            ax.add_patch(rect1)
            ax.add_patch(rect2)
            ax.text(buoy_x - 7, buoy_y - 9, 'buoy', fontsize=5, color=HORSESHOE, fontweight='bold')
            ax.text(vessel_x - 8, vessel_y - 10, 'vessel', fontsize=5, color=HORSESHOE, fontweight='bold')

        elif idx == 2:
            # Buoy detected, vessel box is oversized due to streak
            rect1 = patches.Rectangle((buoy_x - 8, buoy_y - 8), 16, 16,
                                      linewidth=1.5, edgecolor=HORSESHOE, facecolor='none')
            rect2 = patches.Rectangle((vessel_x - 10, vessel_y - 8), 20, 60,
                                      linewidth=1.5, edgecolor=HONEYCOMB, facecolor='none', linestyle='--')
            ax.add_patch(rect1)
            ax.add_patch(rect2)
            ax.text(buoy_x - 8, buoy_y - 10, 'buoy', fontsize=5, color=HORSESHOE, fontweight='bold')
            ax.text(vessel_x - 10, vessel_y - 10, 'vessel?', fontsize=5, color=HONEYCOMB, fontweight='bold')

        elif idx == 3:
            # Single merged detection instead of two
            rect = patches.Rectangle((t2_x - 12, t1_y - 8), 40, 56,
                                     linewidth=1.5, edgecolor=ROSE, facecolor='none', linestyle='--')
            ax.add_patch(rect)
            ax.text(t2_x - 12, t1_y - 10, '1 target?', fontsize=5, color=ROSE, fontweight='bold')

    fig.tight_layout(pad=0.5)
    fig.savefig(os.path.join(OUTDIR, 'fig0_splash.pdf'))
    plt.close(fig)


def fig1_decay_functions():
    """Four decay functions: exponential, concave, linear, step."""
    fig, ax = plt.subplots(figsize=(3.5, 2.5))
    N = 24
    k = np.linspace(0, N, 500)

    # Exponential (fast drop, long tail)
    tau = 4
    f_exp = np.exp(-k / tau)

    # Concave (holds then drops sharply) - power function with p=3
    f_conc = np.clip(1.0 - (k / N) ** 3, 0, 1)

    # Linear
    f_lin = 1 - k / N

    # Step (fixed full intensity, hard cutoff)
    f_step = np.where(k <= N, 1.0, 0.0)

    ax.plot(k, f_exp, color=GARNET, linewidth=2, label='Exponential')
    ax.plot(k, f_conc, color=ATLANTIC, linewidth=2, label='Concave')
    ax.plot(k, f_lin, color=HORSESHOE, linewidth=2, label='Linear')
    ax.plot(k, f_step, color=CONGAREE, linewidth=2, linestyle='--', label='Step')

    ax.set_xlabel('Scan age $k$')
    ax.set_ylabel('Decay weight $f(k)$')
    ax.set_xlim(0, N + 1)
    ax.set_ylim(-0.05, 1.1)
    ax.legend(fontsize=8, frameon=False)

    fig.savefig(os.path.join(OUTDIR, 'fig1_decay_functions.pdf'))
    plt.close(fig)


def fig2_trail_examples():
    """Simulated PPI showing no-trail, short exponential, long step."""
    fig, axes = plt.subplots(1, 4, figsize=(7, 2.2))
    titles = ['No Trails', 'Exponential', 'Concave', 'Step']

    np.random.seed(42)
    for idx, (ax, title) in enumerate(zip(axes, titles)):
        size = 200
        img = np.random.exponential(0.03, (size, size))

        # Target at center-right
        cy, cx = 80, 130
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dy**2 + dx**2 <= 9:
                    img[cy + dy, cx + dx] = 0.9

        if idx == 1:  # Exponential trail
            for dk in range(1, 13):
                w = np.exp(-dk / 3)
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        if dy**2 + dx**2 <= 9:
                            ny = cy + dy + dk
                            if 0 <= ny < size:
                                img[ny, cx + dx] = max(img[ny, cx + dx], 0.9 * w)
        elif idx == 2:  # Concave trail
            N_trail = 12
            for dk in range(1, N_trail + 1):
                w = max(0, 1.0 - (dk / N_trail) ** 3)
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        if dy**2 + dx**2 <= 9:
                            ny = cy + dy + dk
                            if 0 <= ny < size:
                                img[ny, cx + dx] = max(img[ny, cx + dx], 0.9 * w)
        elif idx == 3:  # Step trail
            for dk in range(1, 13):
                w = 1.0
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        if dy**2 + dx**2 <= 9:
                            ny = cy + dy + dk
                            if 0 <= ny < size:
                                img[ny, cx + dx] = max(img[ny, cx + dx], 0.9 * w)

        ax.imshow(np.clip(img, 0, 1), cmap='Greens', vmin=0, vmax=1,
                  interpolation='nearest', aspect='equal')
        ax.set_title(title, fontsize=8, fontweight='bold')
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_linewidth(1)

    fig.tight_layout(pad=0.5)
    fig.savefig(os.path.join(OUTDIR, 'fig2_trail_examples.pdf'))
    plt.close(fig)


def fig3_trail_length_speed():
    """A1: mAP vs trail length for each speed class."""
    fig, ax = plt.subplots(figsize=(3.5, 2.8))
    N_vals = np.array([0, 3, 6, 12, 24])

    # Placeholder data: stationary rises monotonically, moving targets peak then fall
    stationary = np.array([0.62, 0.71, 0.78, 0.83, 0.85])
    slow =       np.array([0.60, 0.68, 0.74, 0.77, 0.76])
    medium =     np.array([0.58, 0.65, 0.68, 0.63, 0.52])
    fast =       np.array([0.55, 0.60, 0.57, 0.46, 0.35])

    # 95% CI half-widths (simulated from 3 seeds)
    ci_stat = np.array([0.02, 0.02, 0.03, 0.02, 0.02])
    ci_slow = np.array([0.03, 0.02, 0.03, 0.03, 0.04])
    ci_med =  np.array([0.03, 0.03, 0.04, 0.04, 0.05])
    ci_fast = np.array([0.04, 0.03, 0.04, 0.05, 0.06])

    for vals, ci, color, marker, label in [
        (stationary, ci_stat, GARNET, 'o', 'Stationary'),
        (slow, ci_slow, ATLANTIC, 's', 'Slow (2 px/scan)'),
        (medium, ci_med, HORSESHOE, '^', 'Medium (5 px/scan)'),
        (fast, ci_fast, CONGAREE, 'D', 'Fast (15 px/scan)'),
    ]:
        ax.plot(N_vals, vals, marker + '-', color=color, linewidth=1.8,
                markersize=5, label=label, zorder=3)
        ax.fill_between(N_vals, vals - ci, vals + ci, color=color, alpha=0.12, zorder=2)

    # No-trail baseline reference
    ax.axhline(y=0.62, color=BLACK_50, linestyle=':', linewidth=0.8, alpha=0.5)
    ax.text(25.2, 0.625, 'No-trail\nbaseline', fontsize=6, color=BLACK_50,
            va='bottom', ha='right')

    # Mark optimal N for each moving class
    for vals, color, opt_n, opt_v in [
        (slow, ATLANTIC, 12, 0.77),
        (medium, HORSESHOE, 6, 0.68),
        (fast, CONGAREE, 3, 0.60),
    ]:
        ax.plot(opt_n, opt_v, 'o', color=color, markersize=9, fillstyle='none',
                linewidth=1.5, zorder=4)

    ax.set_xlabel('Trail length $N$ (scans)')
    ax.set_ylabel('mAP$_{50}$')
    ax.set_xlim(-1, 26)
    ax.set_ylim(0.25, 0.95)
    ax.legend(fontsize=7, frameon=False, loc='lower left')

    fig.savefig(os.path.join(OUTDIR, 'fig3_trail_length_speed.pdf'))
    plt.close(fig)


def fig4_decay_shape():
    """A2: Decay shape comparison grouped by speed class."""
    fig, ax = plt.subplots(figsize=(3.5, 2.8))

    categories = ['Stationary', 'Slow', 'Medium', 'Fast']
    x = np.arange(len(categories))
    width = 0.18

    none =      [0.62, 0.60, 0.58, 0.55]
    exp_vals =  [0.83, 0.76, 0.65, 0.48]
    concave =   [0.82, 0.77, 0.68, 0.53]
    linear =    [0.81, 0.74, 0.63, 0.45]
    step =      [0.84, 0.72, 0.55, 0.38]

    ax.bar(x - 2 * width, none, width, color=BLACK_50, label='No Trail')
    ax.bar(x - width, exp_vals, width, color=GARNET, label='Exponential')
    ax.bar(x, concave, width, color=ATLANTIC, label='Concave')
    ax.bar(x + width, linear, width, color=HORSESHOE, label='Linear')
    ax.bar(x + 2 * width, step, width, color=CONGAREE, label='Step')

    ax.set_ylabel('mAP$_{50}$')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=8)
    ax.set_ylim(0.25, 0.95)
    ax.legend(fontsize=6, frameon=False, ncol=3, loc='upper right')

    fig.savefig(os.path.join(OUTDIR, 'fig4_decay_shape.pdf'))
    plt.close(fig)


def fig5_binary_proportional():
    """A3: Binary vs proportional trail intensity."""
    fig, axes = plt.subplots(1, 2, figsize=(7, 2.8))

    # Left: bar chart comparing binary vs proportional across target types
    ax = axes[0]
    categories = ['Weak\nTarget', 'Strong\nTarget', 'Mixed\nScene']
    x = np.arange(len(categories))
    width = 0.25

    no_trail = [0.52, 0.78, 0.61]
    binary =   [0.68, 0.82, 0.70]
    prop =     [0.72, 0.83, 0.76]

    ax.bar(x - width, no_trail, width, color=BLACK_50, label='No Trail')
    ax.bar(x, binary, width, color=GARNET, label='Binary')
    ax.bar(x + width, prop, width, color=ATLANTIC, label='Proportional')

    ax.set_ylabel('mAP$_{50}$')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=8)
    ax.set_ylim(0.35, 0.95)
    ax.legend(fontsize=7, frameon=False)
    ax.set_title('(a) By target strength', fontsize=9, fontweight='bold')

    # Right: conceptual illustration of binary vs proportional
    ax2 = axes[1]
    scans = np.arange(0, 13)
    orig_strong = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.95, 0.90, 0.80, 0.60, 0.40, 0.20, 0.05])
    orig_weak =   np.array([0.3, 0.3, 0.3, 0.3, 0.3, 0.28, 0.25, 0.20, 0.15, 0.10, 0.05, 0.02, 0.00])
    binary_trail = np.where(orig_strong > 0.05, 1.0, 0.0)

    ax2.plot(scans, orig_strong, 'o-', color=GARNET, linewidth=2, markersize=4, label='Proportional (strong)')
    ax2.plot(scans, orig_weak, 's-', color=ATLANTIC, linewidth=2, markersize=4, label='Proportional (weak)')
    ax2.plot(scans, binary_trail, '^--', color=BLACK_70, linewidth=1.5, markersize=4, label='Binary (any target)')

    ax2.set_xlabel('Trail pixel age (scans)')
    ax2.set_ylabel('Displayed intensity')
    ax2.set_ylim(-0.05, 1.15)
    ax2.legend(fontsize=6, frameon=False)
    ax2.set_title('(b) Intensity encoding', fontsize=9, fontweight='bold')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'fig5_binary_proportional.pdf'))
    plt.close(fig)


def fig6_color_schemes():
    """A4: Color scheme comparison."""
    fig, axes = plt.subplots(1, 2, figsize=(7, 2.8))

    # Left: bar chart
    ax = axes[0]
    schemes = ['Mono', 'Two-tone', 'Gradient', 'Intensity\nMapped']
    x = np.arange(len(schemes))
    width = 0.3

    stat = [0.83, 0.81, 0.84, 0.86]
    move = [0.63, 0.67, 0.71, 0.69]

    ax.bar(x - width / 2, stat, width, color=GARNET, label='Stationary')
    ax.bar(x + width / 2, move, width, color=ATLANTIC, label='Moving')

    ax.set_ylabel('mAP$_{50}$')
    ax.set_xticks(x)
    ax.set_xticklabels(schemes, fontsize=8)
    ax.set_ylim(0.5, 0.95)
    ax.legend(fontsize=8, frameon=False)
    ax.set_title('(a) Detection performance', fontsize=9, fontweight='bold')

    # Right: color scheme illustration (simple colored bars)
    ax2 = axes[1]
    bar_y = [3, 2, 1, 0]
    labels = ['Monochrome', 'Two-tone', 'Gradient', 'Intensity Map']

    # Monochrome: all green fading
    for i, intensity in enumerate(np.linspace(1.0, 0.1, 10)):
        ax2.barh(3, 0.08, left=i * 0.08, color=(0, intensity * 0.6, 0), height=0.6)

    # Two-tone: green then purple
    for i in range(10):
        if i < 3:
            ax2.barh(2, 0.08, left=i * 0.08, color=(0, 0.6, 0), height=0.6)
        else:
            frac = (i - 3) / 7
            ax2.barh(2, 0.08, left=i * 0.08, color=(0.5 * (1 - frac), 0, 0.5 * (1 - frac)), height=0.6)

    # Gradient: green -> yellow -> red
    for i in range(10):
        frac = i / 9
        r = frac
        g = 1.0 - 0.5 * frac
        b = 0
        ax2.barh(1, 0.08, left=i * 0.08, color=(r, g * 0.7, b), height=0.6)

    # Intensity mapped: bright = strong original, dim = weak original
    for i in range(10):
        base_intensity = 0.8 if i < 5 else 0.3
        fade = 1 - i / 12
        ax2.barh(0, 0.08, left=i * 0.08, color=(0, base_intensity * fade * 0.7, 0), height=0.6)

    ax2.set_yticks(bar_y)
    ax2.set_yticklabels(labels, fontsize=7)
    ax2.set_xlim(-0.02, 0.85)
    ax2.set_xlabel('Trail age $\\rightarrow$', fontsize=8)
    ax2.set_title('(b) Color encoding schemes', fontsize=9, fontweight='bold')
    ax2.set_xticks([])

    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'fig6_color_schemes.pdf'))
    plt.close(fig)


def fig7_range_dependence():
    """A5: Range dependence — optimal trail length vs range."""
    fig, axes = plt.subplots(1, 2, figsize=(7, 2.8))

    # Left: mAP vs trail length at different ranges
    ax = axes[0]
    N_vals = [0, 3, 6, 12, 24]

    near = [0.72, 0.74, 0.70, 0.58, 0.42]   # Near: short trails best (fast pixel motion)
    mid =  [0.60, 0.68, 0.74, 0.76, 0.72]   # Mid: medium trails best
    far =  [0.48, 0.55, 0.63, 0.72, 0.78]   # Far: long trails best (slow pixel motion)

    ax.plot(N_vals, near, 'o-', color=GARNET, linewidth=2, markersize=5, label='Near (~200 m)')
    ax.plot(N_vals, mid, 's-', color=ATLANTIC, linewidth=2, markersize=5, label='Mid (~1 nm)')
    ax.plot(N_vals, far, '^-', color=HORSESHOE, linewidth=2, markersize=5, label='Far (~3 nm)')

    ax.set_xlabel('Trail length $N$ (scans)')
    ax.set_ylabel('mAP$_{50}$')
    ax.set_xlim(-1, 26)
    ax.set_ylim(0.3, 0.9)
    ax.legend(fontsize=7, frameon=False)
    ax.set_title('(a) mAP vs trail length by range', fontsize=9, fontweight='bold')

    # Right: optimal N vs range
    ax2 = axes[1]
    ranges_nm = [0.1, 0.25, 0.5, 1.0, 2.0, 3.0]
    optimal_N = [3, 4, 6, 10, 18, 24]

    ax2.plot(ranges_nm, optimal_N, 'o-', color=GARNET, linewidth=2, markersize=6)
    ax2.fill_between(ranges_nm,
                     [max(0, n - 2) for n in optimal_N],
                     [min(30, n + 2) for n in optimal_N],
                     alpha=0.15, color=GARNET)

    ax2.set_xlabel('Target range (nm)')
    ax2.set_ylabel('Optimal trail length $N^*$')
    ax2.set_xlim(0, 3.2)
    ax2.set_ylim(0, 28)
    ax2.set_title('(b) Optimal $N$ vs range', fontsize=9, fontweight='bold')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'fig7_range_dependence.pdf'))
    plt.close(fig)


def fig8_clutter():
    """A6: Clutter level interaction."""
    fig, ax = plt.subplots(figsize=(3.5, 2.8))

    clutter = ['Low', 'Moderate', 'Heavy']
    x = np.arange(len(clutter))
    width = 0.3

    no_trail =  [0.82, 0.65, 0.44]
    best_trail = [0.86, 0.76, 0.62]

    bars1 = ax.bar(x - width / 2, no_trail, width, color=BLACK_50, label='No Trail')
    bars2 = ax.bar(x + width / 2, best_trail, width, color=GARNET, label='Best Trail Config')

    # Annotate improvement
    for i in range(len(clutter)):
        diff = best_trail[i] - no_trail[i]
        ax.annotate(f'+{diff:.2f}', xy=(x[i] + width / 2, best_trail[i]),
                    xytext=(0, 5), textcoords='offset points',
                    ha='center', fontsize=7, color=GARNET, fontweight='bold')

    ax.set_ylabel('mAP$_{50}$')
    ax.set_xticks(x)
    ax.set_xticklabels(clutter)
    ax.set_ylim(0.3, 0.95)
    ax.legend(fontsize=8, frameon=False)

    fig.savefig(os.path.join(OUTDIR, 'fig8_clutter.pdf'))
    plt.close(fig)


def fig9_merging():
    """A7: Target proximity — merging threshold."""
    fig, ax = plt.subplots(figsize=(3.5, 2.8))

    separations = [10, 15, 20, 25, 35, 50, 75, 100]

    no_trail =  [0.15, 0.32, 0.55, 0.72, 0.82, 0.88, 0.90, 0.91]
    with_trail = [0.08, 0.18, 0.35, 0.58, 0.74, 0.85, 0.89, 0.90]

    ax.plot(separations, no_trail, 'o-', color=BLACK_70, linewidth=2, markersize=5, label='No Trail')
    ax.plot(separations, with_trail, 's-', color=GARNET, linewidth=2, markersize=5, label='With Trail ($N=12$)')

    ax.axhline(y=0.5, color=BLACK_30, linestyle=':', linewidth=1)
    ax.text(102, 0.5, 'mAP=0.5', fontsize=7, color=BLACK_50, va='center')

    # Mark merging thresholds
    ax.axvline(x=20, color=BLACK_70, linestyle='--', linewidth=0.8, alpha=0.5)
    ax.axvline(x=28, color=GARNET, linestyle='--', linewidth=0.8, alpha=0.5)

    ax.set_xlabel('Target separation (m)')
    ax.set_ylabel('mAP$_{50}$')
    ax.set_xlim(5, 110)
    ax.set_ylim(0, 1.0)
    ax.legend(fontsize=8, frameon=False)

    fig.savefig(os.path.join(OUTDIR, 'fig9_merging.pdf'))
    plt.close(fig)


def fig10_crossing():
    """A8: Crossing trajectories -- single-column mAP vs crossing angle."""
    fig, ax = plt.subplots(1, 1, figsize=(3.25, 2.6))

    angles = np.array([15, 30, 45, 60, 90])

    no_trail =    np.array([0.70, 0.74, 0.78, 0.80, 0.82])
    short_trail = np.array([0.65, 0.72, 0.77, 0.79, 0.81])
    long_trail =  np.array([0.38, 0.48, 0.58, 0.65, 0.72])

    ci_none =  np.array([0.03, 0.02, 0.02, 0.02, 0.02])
    ci_short = np.array([0.03, 0.03, 0.02, 0.03, 0.02])
    ci_long =  np.array([0.05, 0.04, 0.04, 0.04, 0.03])

    for vals, ci, color, marker, label in [
        (no_trail, ci_none, BLACK_70, 'o', 'No Trail'),
        (short_trail, ci_short, ATLANTIC, 's', '$N=3$'),
        (long_trail, ci_long, GARNET, '^', '$N=12$'),
    ]:
        ax.plot(angles, vals, marker + '-', color=color, linewidth=1.8,
                markersize=5, label=label, zorder=3)
        ax.fill_between(angles, vals - ci, vals + ci, color=color, alpha=0.12, zorder=2)

    # Shade the severe-degradation region
    ax.axhspan(0.3, 0.5, color=ROSE, alpha=0.06, zorder=1)
    ax.text(17, 0.33, 'Severe\ndegradation', fontsize=6, color=ROSE, fontstyle='italic')

    ax.set_xlabel('Crossing angle (degrees)')
    ax.set_ylabel('mAP$_{50}$')
    ax.set_xlim(10, 95)
    ax.set_ylim(0.3, 0.9)
    ax.legend(fontsize=7, frameon=False, loc='lower right')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'fig10_crossing.pdf'))
    plt.close(fig)


def fig11_summary_heatmap():
    """Summary heatmap: best mAP across ablation dimensions."""
    fig, axes = plt.subplots(1, 2, figsize=(7, 3.0))

    decay_fns = ['Exp.', 'Concave', 'Linear', 'Step']
    N_vals = ['0', '3', '6', '12', '24']

    # Stationary targets
    stat_data = np.array([
        [0.62, 0.71, 0.78, 0.83, 0.85],
        [0.62, 0.70, 0.77, 0.82, 0.84],
        [0.62, 0.69, 0.76, 0.81, 0.83],
        [0.62, 0.72, 0.79, 0.84, 0.86],
    ])

    # Moving targets (medium speed)
    move_data = np.array([
        [0.58, 0.65, 0.68, 0.63, 0.52],
        [0.58, 0.66, 0.71, 0.68, 0.56],
        [0.58, 0.64, 0.66, 0.60, 0.48],
        [0.58, 0.63, 0.60, 0.52, 0.38],
    ])

    for ax, data, title in zip(axes, [stat_data, move_data],
                                ['Stationary Targets', 'Moving Targets (5 px/scan)']):
        im = ax.imshow(data, cmap='RdYlGn', aspect='auto', vmin=0.35, vmax=0.90,
                       interpolation='nearest')
        ax.set_xticks(range(len(N_vals)))
        ax.set_xticklabels(N_vals)
        ax.set_yticks(range(len(decay_fns)))
        ax.set_yticklabels(decay_fns, fontsize=8)
        ax.set_xlabel('Trail length $N$')
        ax.set_ylabel('Decay function')
        ax.set_title(title, fontsize=9, fontweight='bold')

        for i in range(len(decay_fns)):
            for j in range(len(N_vals)):
                ax.text(j, i, f'{data[i, j]:.2f}', ha='center', va='center',
                        fontsize=7, color='black' if data[i, j] > 0.55 else 'white')

    fig.colorbar(im, ax=axes, label='mAP$_{50}$', shrink=0.85)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'fig11_summary_heatmap.pdf'))
    plt.close(fig)


def fig_pipeline():
    """System pipeline diagram showing data flow through processing stages."""
    import matplotlib.patches as patches
    fig, ax = plt.subplots(figsize=(7, 1.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2)
    ax.axis('off')

    # Stage positions and labels
    stages = [
        (0.8, 'RCS\nSimulator'),
        (2.2, 'Raw PPI\nFrames'),
        (3.6, 'Echo Trail\nRenderer'),
        (5.0, 'Trailed\nPPI'),
        (6.4, 'YOLOv8'),
        (7.8, 'Detections'),
    ]

    # Draw boxes and labels
    box_width = 0.8
    box_height = 0.6
    y_center = 1.0

    for x, label in stages:
        # Determine color: data stages in ATLANTIC, processing in GARNET
        if label in ['Raw PPI\nFrames', 'Trailed\nPPI', 'Detections']:
            color = ATLANTIC
        else:
            color = GARNET

        rect = patches.Rectangle((x - box_width / 2, y_center - box_height / 2),
                                box_width, box_height,
                                linewidth=1, edgecolor=BLACK_90, facecolor=color,
                                zorder=2)
        ax.add_patch(rect)
        ax.text(x, y_center, label, ha='center', va='center',
               fontsize=7, fontweight='bold', color=WHITE)

    # Draw connecting arrows
    for i in range(len(stages) - 1):
        x1 = stages[i][0] + box_width / 2
        x2 = stages[i + 1][0] - box_width / 2
        arrow = patches.FancyArrowPatch((x1, y_center), (x2, y_center),
                                       arrowstyle='->', mutation_scale=15,
                                       linewidth=1.5, color=BLACK, zorder=1)
        ax.add_patch(arrow)

    fig.savefig(os.path.join(OUTDIR, 'fig_pipeline.pdf'))
    plt.close(fig)


def fig_iou_illustration():
    """IoU degradation illustration comparing detection with and without trails."""
    fig, axes = plt.subplots(1, 2, figsize=(7, 2.5))

    for idx, ax in enumerate(axes):
        ax.set_xlim(-0.5, 4.5)
        ax.set_ylim(-0.5, 4.5)
        ax.set_aspect('equal')
        ax.set_facecolor('#1a1a1a')
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

        if idx == 0:
            # No trail case
            ax.set_title('No Trail: IoU = 0.85', fontsize=8, fontweight='bold', color='white')

            # Ground truth box (dashed)
            gt_box = patches.Rectangle((0.8, 0.8), 2.4, 2.4,
                                      linewidth=1.5, edgecolor=BLACK_70,
                                      facecolor='none', linestyle='--')
            ax.add_patch(gt_box)

            # Tight bounding box (solid)
            det_box = patches.Rectangle((1.2, 1.2), 1.6, 1.6,
                                       linewidth=1.5, edgecolor=HORSESHOE,
                                       facecolor='none')
            ax.add_patch(det_box)

            # Target blip (small circle)
            target = patches.Circle((2.0, 2.0), 0.35, color=GRASS, zorder=3)
            ax.add_patch(target)

        else:
            # Long trail case
            ax.set_title('Long Trail: IoU = 0.35', fontsize=8, fontweight='bold', color='white')

            # Ground truth box (dashed)
            gt_box = patches.Rectangle((0.8, 0.8), 2.4, 2.4,
                                      linewidth=1.5, edgecolor=BLACK_70,
                                      facecolor='none', linestyle='--')
            ax.add_patch(gt_box)

            # Oversized bounding box due to trail (dashed honeycomb)
            det_box = patches.Rectangle((0.5, 0.5), 3.5, 3.5,
                                       linewidth=1.5, edgecolor=HONEYCOMB,
                                       facecolor='none', linestyle='--')
            ax.add_patch(det_box)

            # Target blip with trail
            target = patches.Circle((2.0, 2.0), 0.35, color=GRASS, zorder=3)
            ax.add_patch(target)

            # Trail streak (elongated with fade)
            for i in range(5):
                alpha = 1.0 - i * 0.2
                trail_circle = patches.Circle((2.0 + i * 0.4, 2.0), 0.25,
                                             color=GRASS, alpha=alpha * 0.6, zorder=2)
                ax.add_patch(trail_circle)

    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'fig_iou_illustration.pdf'))
    plt.close(fig)


def fig_ppi_binary_prop():
    """Binary vs proportional PPI intensity comparison."""
    fig, axes = plt.subplots(1, 2, figsize=(7, 2.5))

    for idx, ax in enumerate(axes):
        size = 150
        img = np.zeros((size, size))

        if idx == 0:
            # Binary mode: both targets get full intensity trails
            ax.set_title('Binary: Full Intensity', fontsize=8, fontweight='bold')

            # Strong target at top-left
            for dy in range(-4, 5):
                for dx in range(-4, 5):
                    if dy**2 + dx**2 <= 16:
                        img[30 + dy, 40 + dx] = 1.0

            # Weak target at bottom-right
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    if dy**2 + dx**2 <= 4:
                        img[120 + dy, 110 + dx] = 1.0

            # Trails for both (binary = full intensity)
            for k in range(1, 8):
                for dy in range(-4, 5):
                    for dx in range(-4, 5):
                        if dy**2 + dx**2 <= 16:
                            img[30 + k * 3 + dy, 40 + dx] = max(img[30 + k * 3 + dy, 40 + dx], 1.0)
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        if dy**2 + dx**2 <= 4:
                            img[120 - k * 3 + dy, 110 + dx] = max(img[120 - k * 3 + dy, 110 + dx], 1.0)

        else:
            # Proportional mode: intensity matches original target strength
            ax.set_title('Proportional: Scaled Intensity', fontsize=8, fontweight='bold')

            # Strong target at top-left
            for dy in range(-4, 5):
                for dx in range(-4, 5):
                    if dy**2 + dx**2 <= 16:
                        img[30 + dy, 40 + dx] = 1.0

            # Weak target at bottom-right (dim)
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    if dy**2 + dx**2 <= 4:
                        img[120 + dy, 110 + dx] = 0.3

            # Trails: scaled by original intensity
            for k in range(1, 8):
                w_strong = 1.0 - k / 8
                w_weak = 0.3 * (1.0 - k / 8)
                for dy in range(-4, 5):
                    for dx in range(-4, 5):
                        if dy**2 + dx**2 <= 16:
                            img[30 + k * 3 + dy, 40 + dx] = max(img[30 + k * 3 + dy, 40 + dx], w_strong)
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        if dy**2 + dx**2 <= 4:
                            img[120 - k * 3 + dy, 110 + dx] = max(img[120 - k * 3 + dy, 110 + dx], w_weak)

        ax.imshow(np.clip(img, 0, 1), cmap='Greens', vmin=0, vmax=1,
                 interpolation='nearest', aspect='equal', origin='upper')
        ax.set_facecolor('#000000')
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_linewidth(1)
            spine.set_color(BLACK_90)

    fig.tight_layout(pad=0.5)
    fig.savefig(os.path.join(OUTDIR, 'fig_ppi_binary_prop.pdf'))
    plt.close(fig)


def fig_range_ppi():
    """Range-dependent trail appearance at same physical trail length."""
    fig, axes = plt.subplots(1, 3, figsize=(7, 2.2))

    ranges = [
        ('Near (200m)', 12),   # Long trail in pixels
        ('Mid (1 nm)', 6),     # Medium trail in pixels
        ('Far (3 nm)', 2),     # Short trail in pixels
    ]

    for idx, (ax, (label, trail_pixels)) in enumerate(zip(axes, ranges)):
        size = 140
        img = np.zeros((size, size))

        # Target at center-right
        cy, cx = 70, 100
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dy**2 + dx**2 <= 9:
                    img[cy + dy, cx + dx] = 1.0

        # Trail with N=12 physical scans, displayed at different pixel lengths
        for k in range(1, 13):
            if k <= trail_pixels:
                w = 1.0 - k / 13
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        if dy**2 + dx**2 <= 9:
                            ny = cy + k
                            if 0 <= ny < size:
                                img[ny + dy, cx + dx] = max(img[ny + dy, cx + dx], w)

        ax.imshow(np.clip(img, 0, 1), cmap='Greens', vmin=0, vmax=1,
                 interpolation='nearest', aspect='equal', origin='upper')
        ax.set_title(label, fontsize=8, fontweight='bold')
        ax.set_facecolor('#000000')
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_linewidth(1)

    fig.tight_layout(pad=0.5)
    fig.savefig(os.path.join(OUTDIR, 'fig_range_ppi.pdf'))
    plt.close(fig)


def fig_adaptive_concept():
    """Range-adaptive rendering: adaptive N at different ranges."""
    import matplotlib.patches as patches
    fig, ax = plt.subplots(figsize=(3.5, 3.0))

    # PPI-style circular display
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.set_facecolor('#000000')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Concentric range rings
    radii = [0.3, 0.7, 1.1]
    labels = ['N=3', 'N=12', 'N=24']
    colors_ring = [BLACK_30, BLACK_50, BLACK_70]

    for radius, label, ring_color in zip(radii, labels, colors_ring):
        circle = patches.Circle((0, 0), radius, linewidth=1,
                               edgecolor=ring_color, facecolor='none',
                               linestyle='--', alpha=0.6)
        ax.add_patch(circle)
        ax.text(radius - 0.1, 0.05, label, fontsize=7, color=ring_color,
               fontweight='bold', alpha=0.8)

    # Target blips at different ranges with appropriate trail lengths
    targets = [
        (0.15, 0, 3),      # Near range, N=3
        (0.5, 0, 12),      # Mid range, N=12
        (0.95, 0, 24),     # Far range, N=24
    ]

    for r_pos, theta, n_trail in targets:
        # Target blip
        blip = patches.Circle((r_pos, 0), 0.04, color=GRASS, zorder=3)
        ax.add_patch(blip)

        # Trail (simplified as fading dots)
        trail_length = min(n_trail // 4, 4)
        for k in range(1, trail_length + 1):
            alpha = (1.0 - k / trail_length) * 0.6
            trail_dot = patches.Circle((r_pos + k * 0.08, 0), 0.02,
                                      color=GRASS, alpha=alpha, zorder=2)
            ax.add_patch(trail_dot)

    fig.savefig(os.path.join(OUTDIR, 'fig_adaptive_concept.pdf'))
    plt.close(fig)


if __name__ == '__main__':
    fig0_splash()
    print('  fig0 done')
    fig1_decay_functions()
    print('  fig1 done')
    fig2_trail_examples()
    print('  fig2 done')
    fig3_trail_length_speed()
    print('  fig3 done')
    fig4_decay_shape()
    print('  fig4 done')
    fig5_binary_proportional()
    print('  fig5 done')
    fig6_color_schemes()
    print('  fig6 done')
    fig7_range_dependence()
    print('  fig7 done')
    fig8_clutter()
    print('  fig8 done')
    fig9_merging()
    print('  fig9 done')
    fig10_crossing()
    print('  fig10 done')
    fig11_summary_heatmap()
    print('  fig11 done')
    fig_pipeline()
    print('  fig_pipeline done')
    fig_iou_illustration()
    print('  fig_iou_illustration done')
    fig_ppi_binary_prop()
    print('  fig_ppi_binary_prop done')
    fig_range_ppi()
    print('  fig_range_ppi done')
    fig_adaptive_concept()
    print('  fig_adaptive_concept done')
    print('All figures generated.')
