"""
Generate figures for the echo trails IDETC 2026 paper.
Result figures read real experimental data from ../results/ CSV files.
Uses brand colors per specifications.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import pandas as pd

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
RESULTS_DIR = os.path.join(os.path.dirname(OUTDIR), 'results')

plt.rcParams.update({
    'font.size': 10,
    'font.family': 'serif',
    'axes.linewidth': 1.0,
    'axes.edgecolor': BLACK_90,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
})


def load_csv(name):
    """Load a results CSV file into a DataFrame."""
    return pd.read_csv(os.path.join(RESULTS_DIR, name))


# ═══════════════════════════════════════════════════════════════════════
# Conceptual / illustration figures (unchanged)
# ═══════════════════════════════════════════════════════════════════════

def draw_target(img, cy, cx, radius, intensity):
    """Draw a circular target blip on an image array."""
    h, w = img.shape[:2]
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dy**2 + dx**2 <= radius**2:
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < h and 0 <= nx < w:
                    if img.ndim == 3:
                        img[ny, nx, 1] = max(img[ny, nx, 1], intensity)
                    else:
                        img[ny, nx] = max(img[ny, nx], intensity)


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
        img = np.zeros((size, size, 3))
        noise = np.random.exponential(0.04, (size, size))
        img[:, :, 1] = noise * 0.5

        buoy_y, buoy_x = 55, 60
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dy**2 + dx**2 <= 9:
                    img[buoy_y + dy, buoy_x + dx, 1] = 0.7

        vessel_y, vessel_x = 100, 140
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                if dy**2 + dx**2 <= 16:
                    img[vessel_y + dy, vessel_x + dx, 1] = 0.95

        if idx == 0:
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    if dy**2 + dx**2 <= 9:
                        img[buoy_y + dy, buoy_x + dx, 1] = 0.15
        elif idx == 1:
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
                            img[buoy_y + dy, buoy_x + dx, 1] = max(img[buoy_y + dy, buoy_x + dx, 1], 0.7 * 1.2)
        elif idx == 2:
            for dk in range(1, 25):
                w = 1 - dk / 24
                for dy in range(-4, 5):
                    for dx in range(-4, 5):
                        if dy**2 + dx**2 <= 16:
                            ny = vessel_y + dk * 2
                            if 0 <= ny + dy < size:
                                img[ny + dy, vessel_x + dx, 1] = max(img[ny + dy, vessel_x + dx, 1], 0.9 * w)
            for dy in range(-4, 5):
                for dx in range(-4, 5):
                    if dy**2 + dx**2 <= 16:
                        img[buoy_y + dy, buoy_x + dx, 1] = min(1.0, 0.85)
        elif idx == 3:
            t1_y, t1_x = 80, 110
            t2_y, t2_x = 120, 110
            for dy in range(-4, 5):
                for dx in range(-4, 5):
                    if dy**2 + dx**2 <= 16:
                        img[t1_y + dy, t1_x + dx, 1] = 0.95
                        img[t2_y + dy, t2_x + dx, 1] = 0.95
            for dk in range(1, 16):
                w = 1 - dk / 16
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        if dy**2 + dx**2 <= 9:
                            ny1 = t1_y + dk * 2
                            nx1 = t1_x + dk
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

        if idx == 0:
            rect = patches.Rectangle((vessel_x - 8, vessel_y - 8), 16, 16,
                                     linewidth=1.5, edgecolor=HORSESHOE, facecolor='none')
            ax.add_patch(rect)
            ax.text(vessel_x - 8, vessel_y - 10, 'vessel', fontsize=5, color=HORSESHOE, fontweight='bold')
            ax.plot(buoy_x, buoy_y, 'x', color=ROSE, markersize=8, markeredgewidth=2)
            ax.text(buoy_x + 5, buoy_y - 2, '?', fontsize=7, color=ROSE, fontweight='bold')
        elif idx == 1:
            rect1 = patches.Rectangle((buoy_x - 7, buoy_y - 7), 14, 14,
                                      linewidth=1.5, edgecolor=HORSESHOE, facecolor='none')
            rect2 = patches.Rectangle((vessel_x - 8, vessel_y - 8), 16, 16,
                                      linewidth=1.5, edgecolor=HORSESHOE, facecolor='none')
            ax.add_patch(rect1)
            ax.add_patch(rect2)
            ax.text(buoy_x - 7, buoy_y - 9, 'buoy', fontsize=5, color=HORSESHOE, fontweight='bold')
            ax.text(vessel_x - 8, vessel_y - 10, 'vessel', fontsize=5, color=HORSESHOE, fontweight='bold')
        elif idx == 2:
            rect1 = patches.Rectangle((buoy_x - 8, buoy_y - 8), 16, 16,
                                      linewidth=1.5, edgecolor=HORSESHOE, facecolor='none')
            rect2 = patches.Rectangle((vessel_x - 10, vessel_y - 8), 20, 60,
                                      linewidth=1.5, edgecolor=HONEYCOMB, facecolor='none', linestyle='--')
            ax.add_patch(rect1)
            ax.add_patch(rect2)
            ax.text(buoy_x - 8, buoy_y - 10, 'buoy', fontsize=5, color=HORSESHOE, fontweight='bold')
            ax.text(vessel_x - 10, vessel_y - 10, 'vessel?', fontsize=5, color=HONEYCOMB, fontweight='bold')
        elif idx == 3:
            t1_y, t1_x = 80, 110
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

    tau = 4
    f_exp = np.exp(-k / tau)
    f_conc = np.clip(1.0 - (k / N) ** 3, 0, 1)
    f_lin = 1 - k / N
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
    """Simulated PPI showing no-trail, exponential, concave, step."""
    fig, axes = plt.subplots(1, 4, figsize=(7, 2.2))
    titles = ['No Trails', 'Exponential', 'Concave', 'Step']

    np.random.seed(42)
    for idx, (ax, title) in enumerate(zip(axes, titles)):
        size = 200
        img = np.random.exponential(0.03, (size, size))

        cy, cx = 80, 130
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dy**2 + dx**2 <= 9:
                    img[cy + dy, cx + dx] = 0.9

        if idx == 1:
            for dk in range(1, 13):
                w = np.exp(-dk / 3)
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        if dy**2 + dx**2 <= 9:
                            ny = cy + dy + dk
                            if 0 <= ny < size:
                                img[ny, cx + dx] = max(img[ny, cx + dx], 0.9 * w)
        elif idx == 2:
            N_trail = 12
            for dk in range(1, N_trail + 1):
                w = max(0, 1.0 - (dk / N_trail) ** 3)
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        if dy**2 + dx**2 <= 9:
                            ny = cy + dy + dk
                            if 0 <= ny < size:
                                img[ny, cx + dx] = max(img[ny, cx + dx], 0.9 * w)
        elif idx == 3:
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


# ═══════════════════════════════════════════════════════════════════════
# Result figures — real experimental data from CSVs
# ═══════════════════════════════════════════════════════════════════════

def fig3_trail_length_speed():
    """A1: mAP vs trail length for each speed class (real data)."""
    df = load_csv('a1_trail_length.csv')

    fig, ax = plt.subplots(figsize=(3.5, 2.8))
    N_vals = [0, 3, 6, 12, 24]

    speed_classes = {
        'stationary': ('Stationary', GARNET, 'o'),
        'slow': ('Slow (2 px/scan)', ATLANTIC, 's'),
        'medium': ('Medium (5 px/scan)', HORSESHOE, '^'),
        'fast': ('Fast (15 px/scan)', CONGAREE, 'D'),
    }

    for speed_name, (label, color, marker) in speed_classes.items():
        means = []
        cis = []
        for n in N_vals:
            cond = f'{speed_name}_N{n}'
            row = df[df['condition'] == cond]
            if len(row) > 0:
                means.append(row['mAP50_mean'].values[0])
                cis.append(row['mAP50_ci'].values[0])
            else:
                means.append(np.nan)
                cis.append(0)

        means = np.array(means)
        cis = np.array(cis)
        ax.errorbar(N_vals, means, yerr=cis, fmt=f'{marker}-', color=color,
                     linewidth=2, markersize=5, capsize=3, capthick=1, label=label)

    ax.set_xlabel('Trail length $N$ (scans)')
    ax.set_ylabel('mAP$_{50}$')
    ax.set_xlim(-1, 26)
    ax.set_ylim(-0.02, 0.90)
    ax.legend(fontsize=7, frameon=False, loc='upper right')

    fig.savefig(os.path.join(OUTDIR, 'fig3_trail_length_speed.pdf'))
    plt.close(fig)


def fig4_decay_shape():
    """A2: Decay shape comparison (real data)."""
    df = load_csv('a2_decay.csv')

    fig, ax = plt.subplots(figsize=(3.5, 2.8))

    # Extract decay function names from condition column
    decay_map = {
        'base_decayexponential': 'Exponential',
        'base_decayconcave': 'Concave',
        'base_decaylinear': 'Linear',
        'base_decaystep': 'Step',
    }

    labels = []
    means = []
    cis = []
    colors = [GARNET, ATLANTIC, HORSESHOE, CONGAREE]

    for cond, label in decay_map.items():
        row = df[df['condition'] == cond]
        if len(row) > 0:
            labels.append(label)
            means.append(row['mAP50_mean'].values[0])
            cis.append(row['mAP50_ci'].values[0])

    x = np.arange(len(labels))
    bars = ax.bar(x, means, yerr=cis, width=0.6, color=colors[:len(labels)],
                  capsize=4, edgecolor=BLACK_90, linewidth=0.5)

    ax.set_ylabel('mAP$_{50}$')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(0, max(means) * 1.8 if max(means) > 0 else 0.15)

    # Annotate values on bars
    for bar, mean, ci in zip(bars, means, cis):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + ci + 0.003,
                f'{mean:.3f}', ha='center', va='bottom', fontsize=7, color=BLACK_70)

    fig.savefig(os.path.join(OUTDIR, 'fig4_decay_shape.pdf'))
    plt.close(fig)


def fig5_binary_proportional():
    """A3: Binary vs proportional trail intensity (real data)."""
    df = load_csv('a3_intensity.csv')

    fig, axes = plt.subplots(1, 2, figsize=(7, 2.8))

    # Left: bar chart
    ax = axes[0]
    mode_map = {
        'mixed_rcs_intensitybinary': 'Binary',
        'mixed_rcs_intensityproportional': 'Proportional',
    }

    labels = []
    means = []
    cis = []
    bar_colors = [GARNET, ATLANTIC]

    for cond, label in mode_map.items():
        row = df[df['condition'] == cond]
        if len(row) > 0:
            labels.append(label)
            means.append(row['mAP50_mean'].values[0])
            cis.append(row['mAP50_ci'].values[0])

    x = np.arange(len(labels))
    bars = ax.bar(x, means, yerr=cis, width=0.5, color=bar_colors[:len(labels)],
                  capsize=5, edgecolor=BLACK_90, linewidth=0.5)

    for bar, mean, ci in zip(bars, means, cis):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + ci + 0.002,
                f'{mean:.4f}', ha='center', va='bottom', fontsize=8, color=BLACK_70)

    ax.set_ylabel('mAP$_{50}$')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylim(0, max(means) * 2.2 if max(means) > 0 else 0.1)
    ax.set_title('(a) Detection performance', fontsize=9, fontweight='bold')

    # Right: conceptual illustration (kept from original)
    ax2 = axes[1]
    scans = np.arange(0, 13)
    orig_strong = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.95, 0.90, 0.80, 0.60, 0.40, 0.20, 0.05])
    orig_weak = np.array([0.3, 0.3, 0.3, 0.3, 0.3, 0.28, 0.25, 0.20, 0.15, 0.10, 0.05, 0.02, 0.00])
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
    """A4: Color scheme comparison (real data)."""
    df = load_csv('a4_color.csv')

    fig, axes = plt.subplots(1, 2, figsize=(7, 2.8))

    # Left: bar chart
    ax = axes[0]
    color_map = {
        'mixed_rcs_colormono': 'Mono',
        'mixed_rcs_colortwotone': 'Two-tone',
        'mixed_rcs_colorgradient': 'Gradient',
        'mixed_rcs_colorintensity': 'Intensity',
    }
    bar_colors = [GARNET, ATLANTIC, HORSESHOE, CONGAREE]

    labels = []
    means = []
    cis = []

    for cond, label in color_map.items():
        row = df[df['condition'] == cond]
        if len(row) > 0:
            labels.append(label)
            means.append(row['mAP50_mean'].values[0])
            cis.append(row['mAP50_ci'].values[0])

    x = np.arange(len(labels))
    bars = ax.bar(x, means, yerr=cis, width=0.6, color=bar_colors[:len(labels)],
                  capsize=4, edgecolor=BLACK_90, linewidth=0.5)

    for bar, mean, ci in zip(bars, means, cis):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + ci + 0.005,
                f'{mean:.3f}', ha='center', va='bottom', fontsize=7, color=BLACK_70)

    ax.set_ylabel('mAP$_{50}$')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(0, max(means) * 2.0 if max(means) > 0 else 0.2)
    ax.set_title('(a) Detection performance', fontsize=9, fontweight='bold')

    # Right: color scheme illustration (kept from original)
    ax2 = axes[1]
    bar_y = [3, 2, 1, 0]
    label_list = ['Monochrome', 'Two-tone', 'Gradient', 'Intensity Map']

    for i, intensity in enumerate(np.linspace(1.0, 0.1, 10)):
        ax2.barh(3, 0.08, left=i * 0.08, color=(0, intensity * 0.6, 0), height=0.6)

    for i in range(10):
        if i < 3:
            ax2.barh(2, 0.08, left=i * 0.08, color=(0, 0.6, 0), height=0.6)
        else:
            frac = (i - 3) / 7
            ax2.barh(2, 0.08, left=i * 0.08, color=(0.5 * (1 - frac), 0, 0.5 * (1 - frac)), height=0.6)

    for i in range(10):
        frac = i / 9
        r = frac
        g = 1.0 - 0.5 * frac
        b = 0
        ax2.barh(1, 0.08, left=i * 0.08, color=(r, g * 0.7, b), height=0.6)

    for i in range(10):
        base_intensity = 0.8 if i < 5 else 0.3
        fade = 1 - i / 12
        ax2.barh(0, 0.08, left=i * 0.08, color=(0, base_intensity * fade * 0.7, 0), height=0.6)

    ax2.set_yticks(bar_y)
    ax2.set_yticklabels(label_list, fontsize=7)
    ax2.set_xlim(-0.02, 0.85)
    ax2.set_xlabel('Trail age $\\rightarrow$', fontsize=8)
    ax2.set_title('(b) Color encoding schemes', fontsize=9, fontweight='bold')
    ax2.set_xticks([])

    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'fig6_color_schemes.pdf'))
    plt.close(fig)


def fig7_range_dependence():
    """A5: Range dependence — mAP vs trail length at different ranges (real data)."""
    df = load_csv('a5_range.csv')

    fig, ax = plt.subplots(figsize=(3.5, 2.8))
    N_vals = [0, 3, 6, 12, 24]

    range_classes = {
        'near': ('Near (~200 m)', GARNET, 'o'),
        'far': ('Far (~3 nm)', HORSESHOE, '^'),
    }

    for range_name, (label, color, marker) in range_classes.items():
        means = []
        cis = []
        valid_N = []
        for n in N_vals:
            cond = f'{range_name}_N{n}'
            row = df[df['condition'] == cond]
            if len(row) > 0:
                valid_N.append(n)
                means.append(row['mAP50_mean'].values[0])
                cis.append(row['mAP50_ci'].values[0])

        means = np.array(means)
        cis = np.array(cis)
        ax.errorbar(valid_N, means, yerr=cis, fmt=f'{marker}-', color=color,
                     linewidth=2, markersize=5, capsize=3, capthick=1, label=label)

    ax.set_xlabel('Trail length $N$ (scans)')
    ax.set_ylabel('mAP$_{50}$')
    ax.set_xlim(-1, 26)
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=7, frameon=False)

    fig.savefig(os.path.join(OUTDIR, 'fig7_range_dependence.pdf'))
    plt.close(fig)


def fig8_clutter():
    """A6: Clutter level interaction (real data)."""
    df = load_csv('a6_clutter.csv')

    fig, ax = plt.subplots(figsize=(3.5, 2.8))

    clutter_order = ['low', 'moderate', 'heavy']
    clutter_labels = ['Low', 'Moderate', 'Heavy']

    means = []
    cis = []
    for level in clutter_order:
        row = df[df['condition'] == level]
        if len(row) > 0:
            means.append(row['mAP50_mean'].values[0])
            cis.append(row['mAP50_ci'].values[0])
        else:
            means.append(0)
            cis.append(0)

    x = np.arange(len(clutter_labels))
    bars = ax.bar(x, means, yerr=cis, width=0.5, color=[ATLANTIC, GARNET, CONGAREE],
                  capsize=5, edgecolor=BLACK_90, linewidth=0.5)

    for bar, mean, ci in zip(bars, means, cis):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + ci + 0.005,
                f'{mean:.3f}', ha='center', va='bottom', fontsize=8, color=BLACK_70)

    ax.set_ylabel('mAP$_{50}$')
    ax.set_xticks(x)
    ax.set_xticklabels(clutter_labels)
    ax.set_ylim(0, max(means) * 1.4 if max(means) > 0 else 0.5)

    fig.savefig(os.path.join(OUTDIR, 'fig8_clutter.pdf'))
    plt.close(fig)


def fig9_merging():
    """A7: Target proximity — mAP vs separation (real data)."""
    df = load_csv('a7_proximity.csv')

    fig, ax = plt.subplots(figsize=(3.5, 2.8))

    # Extract separations and sort
    separations = []
    means = []
    cis = []

    for _, row in df.iterrows():
        cond = row['condition']
        sep = int(cond.replace('sep_', '').replace('m', ''))
        separations.append(sep)
        means.append(row['mAP50_mean'])
        cis.append(row['mAP50_ci'])

    # Sort by separation
    order = np.argsort(separations)
    separations = np.array(separations)[order]
    means = np.array(means)[order]
    cis = np.array(cis)[order]

    ax.errorbar(separations, means, yerr=cis, fmt='o-', color=GARNET,
                linewidth=2, markersize=5, capsize=3, capthick=1)

    ax.axhline(y=0.5, color=BLACK_30, linestyle=':', linewidth=1)
    ax.text(max(separations) + 2, 0.5, 'mAP=0.5', fontsize=7, color=BLACK_50, va='center')

    ax.set_xlabel('Target separation (m)')
    ax.set_ylabel('mAP$_{50}$')
    ax.set_xlim(5, max(separations) + 10)
    ax.set_ylim(0.4, max(means) * 1.15)

    fig.savefig(os.path.join(OUTDIR, 'fig9_merging.pdf'))
    plt.close(fig)


def fig10_crossing():
    """A8: Crossing trajectories (real data)."""
    df = load_csv('a8_crossing.csv')

    fig, axes = plt.subplots(1, 2, figsize=(7, 2.8))

    # Left: mAP vs crossing angle
    ax = axes[0]

    angles = []
    means = []
    cis = []

    for _, row in df.iterrows():
        cond = row['condition']
        angle = int(cond.replace('angle_', ''))
        angles.append(angle)
        means.append(row['mAP50_mean'])
        cis.append(row['mAP50_ci'])

    order = np.argsort(angles)
    angles = np.array(angles)[order]
    means = np.array(means)[order]
    cis = np.array(cis)[order]

    ax.errorbar(angles, means, yerr=cis, fmt='o-', color=GARNET,
                linewidth=2, markersize=5, capsize=3, capthick=1)

    ax.set_xlabel('Crossing angle (degrees)')
    ax.set_ylabel('mAP$_{50}$')
    ax.set_xlim(10, 95)
    ax.set_ylim(0.1, max(means) * 1.3 + max(cis))
    ax.set_title('(a) Detection vs crossing angle', fontsize=9, fontweight='bold')

    # Right: illustration of crossing trails (kept)
    ax2 = axes[1]
    np.random.seed(42)
    size = 150
    img = np.random.exponential(0.02, (size, size))

    t1_positions = [(40 + i * 4, 30 + i * 6) for i in range(12)]
    t2_positions = [(100 - i * 4, 30 + i * 6) for i in range(12)]

    for age, (y, x_pos) in enumerate(t1_positions):
        w = max(0, 1 - age / 12)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if dy**2 + dx**2 <= 4 and 0 <= y + dy < size and 0 <= x_pos + dx < size:
                    img[y + dy, x_pos + dx] = max(img[y + dy, x_pos + dx], 0.9 * w)

    for age, (y, x_pos) in enumerate(t2_positions):
        w = max(0, 1 - age / 12)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if dy**2 + dx**2 <= 4 and 0 <= y + dy < size and 0 <= x_pos + dx < size:
                    img[y + dy, x_pos + dx] = max(img[y + dy, x_pos + dx], 0.9 * w)

    ax2.imshow(np.clip(img, 0, 1), cmap='Greens', vmin=0, vmax=1,
               interpolation='nearest', aspect='equal')
    ax2.set_title('(b) Crossing trail overlap', fontsize=9, fontweight='bold')
    ax2.set_xticks([])
    ax2.set_yticks([])
    for spine in ax2.spines.values():
        spine.set_linewidth(1)

    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'fig10_crossing.pdf'))
    plt.close(fig)


def fig11_summary_heatmap():
    """Summary heatmap: mAP across A1 trail length × speed (real data)."""
    df = load_csv('a1_trail_length.csv')

    fig, ax = plt.subplots(figsize=(3.5, 3.0))

    speed_order = ['stationary', 'slow', 'medium', 'fast']
    speed_labels = ['Stationary', 'Slow\n(2 px/s)', 'Medium\n(5 px/s)', 'Fast\n(15 px/s)']
    N_vals = [0, 3, 6, 12, 24]
    N_labels = ['0', '3', '6', '12', '24']

    data = np.zeros((len(speed_order), len(N_vals)))
    for i, speed in enumerate(speed_order):
        for j, n in enumerate(N_vals):
            cond = f'{speed}_N{n}'
            row = df[df['condition'] == cond]
            if len(row) > 0:
                data[i, j] = row['mAP50_mean'].values[0]

    im = ax.imshow(data, cmap='RdYlGn', aspect='auto', vmin=0.0, vmax=0.85,
                   interpolation='nearest')
    ax.set_xticks(range(len(N_labels)))
    ax.set_xticklabels(N_labels)
    ax.set_yticks(range(len(speed_labels)))
    ax.set_yticklabels(speed_labels, fontsize=8)
    ax.set_xlabel('Trail length $N$')
    ax.set_ylabel('Speed class')

    for i in range(len(speed_order)):
        for j in range(len(N_vals)):
            val = data[i, j]
            ax.text(j, i, f'{val:.3f}', ha='center', va='center',
                    fontsize=7, color='black' if val > 0.15 else 'white')

    fig.colorbar(im, ax=ax, label='mAP$_{50}$', shrink=0.85)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'fig11_summary_heatmap.pdf'))
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
    print('All figures generated.')
