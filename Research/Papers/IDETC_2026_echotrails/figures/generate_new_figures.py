"""
Generate 6 new figures for the echo trails IDETC 2026 paper.
Uses brand colors per specifications.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
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


def fig_pipeline():
    """Figure 12: System pipeline diagram."""
    fig, ax = plt.subplots(figsize=(7, 1.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2)
    ax.axis('off')

    stages = [
        (1.0, 'RCS\nSimulator', GARNET),
        (2.8, 'Raw PPI\nFrames', ATLANTIC),
        (4.6, 'Trail\nRenderer', GARNET),
        (6.4, 'Trailed\nPPI', ATLANTIC),
        (8.2, 'YOLOv8\nDetector', GARNET),
    ]

    # Configurable parameters annotation
    param_labels = [
        (4.6, '$N$, $f(k)$, encoding,\ncolor mapping'),
    ]

    bw = 1.2
    bh = 0.7
    yc = 1.0

    for x, label, color in stages:
        rect = patches.FancyBboxPatch(
            (x - bw/2, yc - bh/2), bw, bh,
            boxstyle="square,pad=0",
            linewidth=1.2, edgecolor=BLACK_90, facecolor=color, zorder=2)
        ax.add_patch(rect)
        ax.text(x, yc, label, ha='center', va='center',
                fontsize=8, fontweight='bold', color=WHITE)

    # Arrows
    for i in range(len(stages) - 1):
        x1 = stages[i][0] + bw/2
        x2 = stages[i+1][0] - bw/2
        ax.annotate('', xy=(x2, yc), xytext=(x1, yc),
                    arrowprops=dict(arrowstyle='->', lw=1.5, color=BLACK_70))

    # Parameter annotation with arrow pointing to Trail Renderer
    ax.annotate('$N$, $f(k)$, encoding, color',
                xy=(4.6, yc + bh/2), xytext=(4.6, yc + bh/2 + 0.55),
                fontsize=7, ha='center', va='bottom', color=BLACK_70,
                arrowprops=dict(arrowstyle='->', lw=1, color=BLACK_50))

    # Output annotation
    ax.text(9.5, yc, 'mAP$_{50}$\nBBoxes', ha='center', va='center',
            fontsize=8, color=BLACK_70, fontstyle='italic')
    ax.annotate('', xy=(9.2, yc), xytext=(8.2 + bw/2, yc),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=BLACK_70))

    fig.savefig(os.path.join(OUTDIR, 'fig_pipeline.pdf'))
    plt.close(fig)
    print('  fig_pipeline.pdf')


def fig_iou():
    """Figure 13: IoU degradation from trail streaks."""
    fig, axes = plt.subplots(1, 3, figsize=(7, 2.2))

    scenarios = [
        ('No Trail\nIoU = 0.82', False, False),
        ('Short Trail ($N\\!=\\!3$)\nIoU = 0.71', True, False),
        ('Long Trail ($N\\!=\\!12$)\nIoU = 0.38', True, True),
    ]

    for ax, (title, has_trail, long_trail) in zip(axes, scenarios):
        size = 120
        img = np.zeros((size, size, 3))
        np.random.seed(7)
        img[:, :, 1] = np.random.exponential(0.02, (size, size))

        # Target at center
        cy, cx = 60, 55
        draw_target(img, cy, cx, 4, 0.95)

        if has_trail:
            n_steps = 12 if long_trail else 3
            for k in range(1, n_steps + 1):
                w = 0.85 * (1 - k / (n_steps + 2))
                draw_target(img, cy, cx + k * 4, 3, w)

        ax.imshow(np.clip(img, 0, 1), interpolation='nearest', aspect='equal')

        # Ground truth bbox (white dashed)
        gt = patches.Rectangle((cx - 7, cy - 7), 14, 14,
                               linewidth=1.5, edgecolor=WHITE,
                               facecolor='none', linestyle='--', zorder=5)
        ax.add_patch(gt)

        # Predicted bbox
        if not has_trail:
            pred = patches.Rectangle((cx - 8, cy - 8), 16, 16,
                                     linewidth=1.5, edgecolor=GRASS,
                                     facecolor='none', zorder=5)
        elif not long_trail:
            pred = patches.Rectangle((cx - 8, cy - 9), 28, 18,
                                     linewidth=1.5, edgecolor=HONEYCOMB,
                                     facecolor='none', zorder=5)
        else:
            pred = patches.Rectangle((cx - 8, cy - 10), 62, 20,
                                     linewidth=1.5, edgecolor=ROSE,
                                     facecolor='none', zorder=5)
        ax.add_patch(pred)

        ax.set_title(title, fontsize=8, fontweight='bold')
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_linewidth(1)
            spine.set_color(BLACK_90)

    fig.tight_layout(pad=0.5)
    fig.savefig(os.path.join(OUTDIR, 'fig_iou.pdf'))
    plt.close(fig)
    print('  fig_iou.pdf')


def fig_range_displacement():
    """Figure 14: Range-dependent pixel displacement on PPI."""
    fig, ax = plt.subplots(figsize=(3.5, 3.2))

    size = 300
    img = np.zeros((size, size, 3))
    np.random.seed(42)
    img[:, :, 1] = np.random.exponential(0.015, (size, size))

    center = size // 2

    # Range rings
    for r_px, label in [(40, '200 m'), (100, '1 nm'), (180, '3 nm')]:
        theta = np.linspace(0, 2 * np.pi, 200)
        ax.plot(center + r_px * np.cos(theta), center + r_px * np.sin(theta),
                '--', color='#555555', linewidth=0.6, alpha=0.7)
        ax.text(center + r_px * 0.71 + 3, center - r_px * 0.71 - 3,
                label, fontsize=6, color=BLACK_50, rotation=-45)

    # Targets at 3 ranges, same physical speed, different pixel displacement
    # Near: large displacement (10 px/scan)
    near_cx, near_cy = center + 30, center - 25
    draw_target(img, near_cy, near_cx, 3, 0.95)
    for k in range(1, 8):
        w = 0.8 * (1 - k / 10)
        draw_target(img, near_cy + k * 3, near_cx - k * 3, 2, w)

    # Mid: moderate displacement (4 px/scan)
    mid_cx, mid_cy = center + 75, center - 65
    draw_target(img, mid_cy, mid_cx, 3, 0.9)
    for k in range(1, 8):
        w = 0.75 * (1 - k / 10)
        draw_target(img, mid_cy + k * 2, mid_cx - k * 1, 2, w)

    # Far: tiny displacement (1 px/scan)
    far_cx, far_cy = center + 130, center - 120
    draw_target(img, far_cy, far_cx, 3, 0.85)
    for k in range(1, 8):
        w = 0.7 * (1 - k / 10)
        draw_target(img, far_cy + k, far_cx, 2, w)

    ax.imshow(np.clip(img, 0, 1), interpolation='nearest', aspect='equal')

    # Motion arrows
    ax.annotate('10 px/scan', xy=(near_cx - 15, near_cy + 18),
                xytext=(near_cx - 40, near_cy + 40),
                fontsize=6, color=GRASS, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=GRASS, lw=1))
    ax.annotate('4 px/scan', xy=(mid_cx - 5, mid_cy + 12),
                xytext=(mid_cx - 35, mid_cy + 35),
                fontsize=6, color=GRASS, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=GRASS, lw=1))
    ax.annotate('1 px/scan', xy=(far_cx, far_cy + 8),
                xytext=(far_cx - 25, far_cy + 30),
                fontsize=6, color=GRASS, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=GRASS, lw=1))

    # Vessel marker at center
    ax.plot(center, center, '+', color=WHITE, markersize=8, markeredgewidth=1)

    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_linewidth(1)
        spine.set_color(BLACK_90)

    fig.savefig(os.path.join(OUTDIR, 'fig_range_displacement.pdf'))
    plt.close(fig)
    print('  fig_range_displacement.pdf')


def fig_adaptive_trail():
    """Figure 15: Range-adaptive trail rendering concept."""
    fig, axes = plt.subplots(1, 2, figsize=(7, 3.0))

    np.random.seed(42)

    for panel, ax in enumerate(axes):
        size = 250
        img = np.zeros((size, size, 3))
        img[:, :, 1] = np.random.exponential(0.015, (size, size))

        center = size // 2

        # Range rings
        for r_px in [35, 75, 130]:
            theta = np.linspace(0, 2 * np.pi, 200)
            ring_x = center + r_px * np.cos(theta)
            ring_y = center + r_px * np.sin(theta)
            for i in range(len(theta)):
                rx, ry = int(ring_x[i]), int(ring_y[i])
                if 0 <= rx < size and 0 <= ry < size:
                    img[ry, rx, 1] = max(img[ry, rx, 1], 0.12)

        if panel == 0:
            # Fixed N=12 for all ranges
            ax.set_title('(a) Fixed trail length ($N=12$)',
                         fontsize=8, fontweight='bold')
            configs = [
                (25, 45, 12, 4),    # near: long trail, fast pixel movement
                (60, -30, 12, 2),   # mid
                (110, 160, 12, 1),  # far
            ]
        else:
            # Adaptive: short near, long far
            ax.set_title('(b) Range-adaptive trail length',
                         fontsize=8, fontweight='bold')
            configs = [
                (25, 45, 3, 4),     # near: short trail
                (60, -30, 8, 2),    # mid: medium trail
                (110, 160, 20, 1),  # far: long trail
            ]

        for r, angle_deg, N, px_per_scan in configs:
            angle = np.radians(angle_deg)
            cx = int(center + r * np.cos(angle))
            cy = int(center + r * np.sin(angle))

            # Movement direction (tangential)
            dx_move = -np.sin(angle) * px_per_scan
            dy_move = np.cos(angle) * px_per_scan

            # Current target
            draw_target(img, cy, cx, 3, 0.95)

            # Trail
            for k in range(1, N + 1):
                w = 0.85 * (1 - k / (N + 2))
                tx = int(cx - k * dx_move)
                ty = int(cy - k * dy_move)
                if 0 <= tx < size and 0 <= ty < size:
                    draw_target(img, ty, tx, 2, w)

        # Center marker
        ax.plot(center, center, '+', color=WHITE, markersize=6, markeredgewidth=0.8)

        ax.imshow(np.clip(img, 0, 1), interpolation='nearest', aspect='equal')
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_linewidth(1)
            spine.set_color(BLACK_90)

    fig.tight_layout(pad=0.5)
    fig.savefig(os.path.join(OUTDIR, 'fig_adaptive_trail.pdf'))
    plt.close(fig)
    print('  fig_adaptive_trail.pdf')


def fig_color_ppi():
    """Figure 16: Four color schemes rendered on PPI imagery."""
    fig, axes = plt.subplots(1, 4, figsize=(7, 2.0))

    schemes = [
        ('Monochrome', 'mono'),
        ('Two-tone', 'twotone'),
        ('Gradient', 'gradient'),
        ('Intensity-mapped', 'intmap'),
    ]

    np.random.seed(42)
    N = 10

    for ax, (title, mode) in zip(axes, schemes):
        size = 120
        img = np.zeros((size, size, 3))
        img += np.random.exponential(0.01, (size, size, 1)) * np.array([0, 0.3, 0])

        cy, cx = 60, 45
        target_r = 3

        for k in range(N, -1, -1):
            age_frac = k / N
            w = 1.0 - age_frac * 0.8
            tx = cx + k * 4
            ty = cy

            if mode == 'mono':
                # Green only, intensity fades
                color = np.array([0, w * 0.9, 0])
            elif mode == 'twotone':
                if k == 0:
                    color = np.array([0, 0.95, 0])  # current: green
                else:
                    color = np.array([0.7 * w, 0.1 * w, 0.1 * w])  # trail: red-ish (garnet)
            elif mode == 'gradient':
                # Green -> yellow -> red
                if age_frac < 0.33:
                    color = np.array([age_frac * 3 * 0.8, 0.9 * w, 0])
                elif age_frac < 0.66:
                    color = np.array([0.8 * w, 0.9 * (1 - age_frac) * w, 0])
                else:
                    color = np.array([0.7 * w, 0.15 * w, 0])
            elif mode == 'intmap':
                # Color based on return strength (strong=bright green, weak=dim blue)
                strength = 0.9  # this target is strong
                color = np.array([0, strength * w, (1 - strength) * w * 0.3])

            r = target_r if k == 0 else 2
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    if dy**2 + dx**2 <= r**2:
                        ny, nx = ty + dy, tx + dx
                        if 0 <= ny < size and 0 <= nx < size:
                            for c in range(3):
                                img[ny, nx, c] = max(img[ny, nx, c], color[c])

        ax.imshow(np.clip(img, 0, 1), interpolation='nearest', aspect='equal')
        ax.set_title(title, fontsize=7, fontweight='bold')
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_linewidth(1)
            spine.set_color(BLACK_90)

    fig.tight_layout(pad=0.3)
    fig.savefig(os.path.join(OUTDIR, 'fig_color_ppi.pdf'))
    plt.close(fig)
    print('  fig_color_ppi.pdf')


def fig_binary_prop_ppi():
    """Figure 17: Binary vs proportional encoding on PPI with mixed targets."""
    fig, axes = plt.subplots(1, 2, figsize=(7, 2.8))

    modes = [
        ('(a) Binary encoding', 'binary'),
        ('(b) Proportional encoding', 'proportional'),
    ]

    np.random.seed(42)

    for ax, (title, mode) in zip(axes, modes):
        size = 160
        img = np.zeros((size, size, 3))
        img[:, :, 1] = np.random.exponential(0.015, (size, size))

        # Strong target (large vessel, high RCS): top-left area
        strong_cy, strong_cx = 50, 50
        strong_rcs = 1.0

        # Weak target (small buoy, low RCS): bottom-right area
        weak_cy, weak_cx = 110, 110
        weak_rcs = 0.25

        targets = [
            (strong_cy, strong_cx, strong_rcs, 4, -2, 3),
            (weak_cy, weak_cx, weak_rcs, 2, 3, -2),
        ]

        N = 8
        for cy, cx, rcs, radius, dy_move, dx_move in targets:
            # Current return
            if mode == 'binary':
                trail_intensity = 1.0  # any signal -> full intensity
            else:
                trail_intensity = rcs  # proportional to RCS

            draw_target(img, cy, cx, radius, 0.95 if mode == 'binary' else rcs)

            # Trail
            for k in range(1, N + 1):
                w = (1 - k / (N + 2))
                if mode == 'binary':
                    pixel_val = w  # full intensity, decayed by age only
                else:
                    pixel_val = rcs * w  # scaled by original RCS

                ty = cy + k * dy_move
                tx = cx + k * dx_move
                if 0 <= ty < size and 0 <= tx < size:
                    draw_target(img, int(ty), int(tx), radius - 1, pixel_val)

        # Labels
        ax.imshow(np.clip(img, 0, 1), interpolation='nearest', aspect='equal')

        # Annotate targets
        ax.annotate('Vessel\n(strong RCS)', xy=(strong_cx, strong_cy),
                    xytext=(strong_cx + 30, strong_cy - 25),
                    fontsize=6, color=WHITE, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color=WHITE, lw=0.8))
        ax.annotate('Buoy\n(weak RCS)', xy=(weak_cx, weak_cy),
                    xytext=(weak_cx - 55, weak_cy + 20),
                    fontsize=6, color=WHITE, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color=WHITE, lw=0.8))

        ax.set_title(title, fontsize=9, fontweight='bold')
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_linewidth(1)
            spine.set_color(BLACK_90)

    fig.tight_layout(pad=0.5)
    fig.savefig(os.path.join(OUTDIR, 'fig_binary_prop_ppi.pdf'))
    plt.close(fig)
    print('  fig_binary_prop_ppi.pdf')


if __name__ == '__main__':
    print('Generating new figures...')
    fig_pipeline()
    fig_iou()
    fig_range_displacement()
    fig_adaptive_trail()
    fig_color_ppi()
    fig_binary_prop_ppi()
    print('Done.')
