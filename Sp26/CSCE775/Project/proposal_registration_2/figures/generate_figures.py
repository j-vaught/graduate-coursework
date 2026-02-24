#!/usr/bin/env python3
"""Generate all figures for the RL-Optimized IR/RGB Registration proposal."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Brand colors
GARNET = '#73000A'
BLACK = '#000000'
WHITE = '#FFFFFF'
BLACK_90 = '#363636'
BLACK_70 = '#5C5C5C'
BLACK_50 = '#A2A2A2'
BLACK_30 = '#C7C7C7'
BLACK_10 = '#ECECEC'
WARM_GREY = '#676156'
SANDSTORM = '#FFF2E3'
ROSE = '#CC2E40'
ATLANTIC = '#466A9F'
CONGAREE = '#1F414D'
HORSESHOE = '#65780B'
GRASS = '#CED318'
HONEYCOMB = '#A49137'

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.linewidth': 1.2,
    'axes.edgecolor': BLACK_90,
    'text.color': BLACK_90,
    'axes.labelcolor': BLACK_90,
    'xtick.color': BLACK_70,
    'ytick.color': BLACK_70,
})


def draw_box(ax, xy, width, height, text, color=ATLANTIC, text_color=WHITE, fontsize=9, bold=False):
    """Draw a rectangular box with centered text."""
    box = FancyBboxPatch(xy, width, height, boxstyle="square,pad=0",
                         facecolor=color, edgecolor=BLACK_90, linewidth=1.2)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(xy[0] + width/2, xy[1] + height/2, text,
            ha='center', va='center', fontsize=fontsize, color=text_color,
            weight=weight, wrap=True)
    return box


def draw_arrow(ax, start, end, color=BLACK_70, style='->', lw=1.5):
    """Draw an arrow between two points."""
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle=style, color=color, lw=lw))


# ============================================================
# Figure 1: System Architecture Overview
# ============================================================
def fig1_system_architecture():
    fig, ax = plt.subplots(1, 1, figsize=(10, 7.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    # No title - caption comes from LaTeX \caption{}

    # === ROW 1: Sensor Inputs ===
    draw_box(ax, (0.5, 5.8), 1.6, 0.7, 'IR Camera', color=CONGAREE, fontsize=10)
    draw_box(ax, (0.5, 4.8), 1.6, 0.7, 'RGB Camera', color=CONGAREE, fontsize=10)

    # === ROW 2: Feature Extraction + Env Tag ===
    draw_box(ax, (3.0, 5.0), 2.0, 1.0, 'Feature Extraction\n& Quality Assessment', color=BLACK_70, fontsize=9)
    draw_box(ax, (6.5, 5.5), 1.8, 0.6, 'Environment Tag\n(lake / river / coast)', color=WARM_GREY, fontsize=8)

    # === ROW 3: RL Policy (DOMINANT - larger, heavier border) ===
    rl_box = FancyBboxPatch((2.5, 3.2), 5.0, 1.3, boxstyle="square,pad=0",
                             facecolor=GARNET, edgecolor=BLACK, linewidth=2.5)
    ax.add_patch(rl_box)
    ax.text(5.0, 3.85, 'RL Policy Network (SAC / TD3)',
            ha='center', va='center', fontsize=12, color=WHITE, weight='bold')

    # === ROW 4: Action outputs (same color family) ===
    draw_box(ax, (1.5, 1.8), 2.4, 0.8, 'Registration\nTransform Selection', color=ATLANTIC, text_color=WHITE, fontsize=9)
    draw_box(ax, (6.1, 1.8), 2.4, 0.8, 'Augmentation\nRecipe Selection', color=ATLANTIC, text_color=WHITE, fontsize=9)

    # Fork point for actions
    ax.plot(5.0, 2.9, 'o', color=BLACK_90, markersize=6, zorder=5)

    # === ROW 5: Bottom pipeline ===
    draw_box(ax, (1.5, 0.5), 2.4, 0.7, 'Registration & Fusion', color=CONGAREE, fontsize=9)
    draw_box(ax, (5.0, 0.5), 2.4, 0.7, 'Downstream\nPerception Task', color=CONGAREE, fontsize=9)

    # === REWARD (right column) ===
    draw_box(ax, (8.0, 0.5), 1.5, 0.7, 'Reward\nComputation', color=BLACK_50, text_color=WHITE, fontsize=9)

    # ---- ARROWS ----

    # Inputs -> Feature Extraction
    draw_arrow(ax, (2.1, 6.15), (3.0, 5.7), lw=1.8)
    draw_arrow(ax, (2.1, 5.15), (3.0, 5.3), lw=1.8)

    # Feature Extraction -> RL Policy (state)
    draw_arrow(ax, (4.0, 5.0), (4.0, 4.5), color=GARNET, lw=2.0)
    ax.text(4.3, 4.7, '$s_t$', fontsize=13, color=GARNET, weight='bold')

    # Env Tag -> RL Policy
    draw_arrow(ax, (7.4, 5.5), (6.5, 4.5), color=WARM_GREY, lw=1.5)

    # RL Policy -> fork point
    draw_arrow(ax, (5.0, 3.2), (5.0, 2.95), color=BLACK_90, lw=2.0)

    # Fork point -> two actions
    draw_arrow(ax, (5.0, 2.85), (2.7, 2.6), color=BLACK_90, lw=2.0)
    draw_arrow(ax, (5.0, 2.85), (7.3, 2.6), color=BLACK_90, lw=2.0)
    ax.text(3.3, 2.75, '$a_t$', fontsize=12, color=GARNET, weight='bold')
    ax.text(6.5, 2.75, '$a_t$', fontsize=12, color=GARNET, weight='bold')

    # Action boxes -> bottom pipeline
    draw_arrow(ax, (2.7, 1.8), (2.7, 1.2), lw=1.5)
    draw_arrow(ax, (7.3, 1.8), (7.3, 1.5), color=BLACK_50, lw=1.2)
    # Augmentation feeds into Registration & Fusion
    ax.annotate('', xy=(3.9, 0.85), xytext=(7.3, 1.5),
                arrowprops=dict(arrowstyle='->', color=BLACK_50, lw=1.2, linestyle='--'))

    # Registration & Fusion -> Downstream
    draw_arrow(ax, (3.9, 0.85), (5.0, 0.85), lw=1.8)

    # === REWARD FEEDBACK LOOP (dashed, rose-colored, clean right margin) ===
    # Downstream -> Reward (horizontal)
    draw_arrow(ax, (7.4, 0.85), (8.0, 0.85), color=ROSE, lw=2.0, style='->')

    # Reward up right margin -> into RL Policy
    # Vertical segment up right margin
    ax.plot([9.3, 9.3], [0.85, 3.85], color=ROSE, lw=2.0, linestyle='--', zorder=3)
    ax.annotate('', xy=(9.5, 0.85), xytext=(9.3, 0.85),
                arrowprops=dict(arrowstyle='-', color=ROSE, lw=0))  # invisible connector
    # Horizontal from Reward to margin
    ax.plot([9.0, 9.3], [0.85, 0.85], color=ROSE, lw=2.0, linestyle='--', zorder=3)
    # Horizontal from margin into RL Policy
    ax.annotate('', xy=(7.5, 3.85), xytext=(9.3, 3.85),
                arrowprops=dict(arrowstyle='->', color=ROSE, lw=2.0, linestyle='--'))
    ax.text(9.5, 2.5, '$r_t$', fontsize=13, color=ROSE, weight='bold')

    fig.tight_layout()
    fig.savefig('figures/fig1_system_architecture.pdf', bbox_inches='tight', dpi=300)
    fig.savefig('figures/fig1_system_architecture.png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    print("Figure 1: System Architecture saved.")


# ============================================================
# Figure 2: RL Loop Detail (MDP Formulation)
# ============================================================
def fig2_rl_loop():
    fig, ax = plt.subplots(1, 1, figsize=(9, 5.5))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    # === TOP ROW: State / Action / Reward boxes ===
    box_h = 2.0
    box_y = 3.2

    # State box
    draw_box(ax, (0.3, box_y), 2.5, box_h, '', color=BLACK_10, text_color=BLACK_90)
    ax.text(1.55, box_y + box_h - 0.25, 'State $s_t$', ha='center', fontsize=12, weight='bold', color=GARNET)
    state_items = ['Frame quality cues', 'Alignment residuals', 'Environment tag $e$', 'Prior action history']
    for i, item in enumerate(state_items):
        ax.text(1.55, box_y + box_h - 0.65 - i*0.35, item, ha='center', fontsize=9, color=BLACK_70)

    # Action box
    draw_box(ax, (3.3, box_y), 2.4, box_h, '', color=SANDSTORM, text_color=BLACK_90)
    ax.text(4.5, box_y + box_h - 0.25, 'Action $a_t$', ha='center', fontsize=12, weight='bold', color=GARNET)
    action_items = ['Transform family $\\tau$', 'Transform params $\\theta$', 'Augmentation type', 'Augmentation strength']
    for i, item in enumerate(action_items):
        ax.text(4.5, box_y + box_h - 0.65 - i*0.35, item, ha='center', fontsize=9, color=BLACK_70)

    # Reward box
    draw_box(ax, (6.2, box_y), 2.5, box_h, '', color='#F5E6E8', text_color=BLACK_90)
    ax.text(7.45, box_y + box_h - 0.25, 'Reward $r_t$', ha='center', fontsize=12, weight='bold', color=ROSE)
    reward_items = ['Alignment error $\\downarrow$', 'Perception gain $\\uparrow$', 'Robustness score', 'Consistency penalty']
    for i, item in enumerate(reward_items):
        ax.text(7.45, box_y + box_h - 0.65 - i*0.35, item, ha='center', fontsize=9, color=BLACK_70)

    # Arrows between top boxes
    draw_arrow(ax, (2.8, box_y + box_h/2), (3.3, box_y + box_h/2), color=GARNET, lw=2.5)
    draw_arrow(ax, (5.7, box_y + box_h/2), (6.2, box_y + box_h/2), color=GARNET, lw=2.5)

    # === ENVIRONMENT block (bottom) ===
    env_y = 0.3
    env_h = 2.2
    draw_box(ax, (0.5, env_y), 8.0, env_h, '', color=WHITE)
    ax.add_patch(FancyBboxPatch((0.5, env_y), 8.0, env_h, boxstyle="square,pad=0",
                                facecolor='none', edgecolor=GARNET, linewidth=2.0, linestyle='--'))
    ax.text(4.5, env_y + env_h - 0.35, 'Environment: IR/RGB Registration Pipeline',
            ha='center', fontsize=11, weight='bold', color=GARNET)

    # Sub-modules inside environment
    mod_y = env_y + 0.3
    mod_h = 0.55
    draw_box(ax, (0.8, mod_y + 0.7), 2.2, mod_h, 'Classical\nRegistration', color=BLACK_30, text_color=BLACK_90, fontsize=8)
    draw_box(ax, (3.4, mod_y + 0.7), 2.2, mod_h, 'Deep\nRegistration', color=ATLANTIC, fontsize=8)
    draw_box(ax, (6.0, mod_y + 0.7), 2.2, mod_h, 'Augmentation\nEngine', color=HORSESHOE, text_color=WHITE, fontsize=8)
    draw_box(ax, (2.0, mod_y), 5.0, mod_h, 'Downstream Task Evaluator (Detection / Tracking / Segmentation)',
             color=BLACK_10, text_color=BLACK_90, fontsize=8)

    # === ARROWS: boxes <-> environment ===
    # Action -> Environment (center)
    draw_arrow(ax, (4.5, box_y), (4.5, env_y + env_h), color=ATLANTIC, lw=2.5)
    ax.text(4.8, box_y - 0.35, '$a_t$', fontsize=11, color=ATLANTIC, weight='bold')

    # Environment -> State (left side)
    ax.annotate('', xy=(1.55, box_y), xytext=(1.55, env_y + env_h),
                arrowprops=dict(arrowstyle='->', color=CONGAREE, lw=2.5))
    ax.text(0.7, box_y - 0.35, '$s_{t+1}$', fontsize=11, color=CONGAREE, weight='bold')

    # Environment -> Reward (right side)
    ax.annotate('', xy=(7.45, box_y), xytext=(7.45, env_y + env_h),
                arrowprops=dict(arrowstyle='->', color=ROSE, lw=2.5))
    ax.text(7.8, box_y - 0.35, '$r_t$', fontsize=11, color=ROSE, weight='bold')

    fig.tight_layout()
    fig.savefig('figures/fig2_rl_loop.pdf', bbox_inches='tight', dpi=300)
    fig.savefig('figures/fig2_rl_loop.png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    print("Figure 2: RL Loop saved.")


# ============================================================
# Figure 3: Registration Transform Families
# ============================================================
def fig3_transform_families():
    fig, axes = plt.subplots(1, 4, figsize=(10, 3))

    transforms = [
        ('Rigid\n(Translation + Rotation)', 'rigid'),
        ('Affine\n(+ Scale + Shear)', 'affine'),
        ('Projective\n(Homography)', 'projective'),
        ('Deformable\n(Non-linear Warp)', 'deformable'),
    ]

    for idx, (title, ttype) in enumerate(transforms):
        ax = axes[idx]
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')

        # Draw original grid
        for i in np.linspace(-1, 1, 5):
            ax.plot([-1, 1], [i, i], color=BLACK_30, lw=0.5, zorder=1)
            ax.plot([i, i], [-1, 1], color=BLACK_30, lw=0.5, zorder=1)

        # Draw transformed grid
        np.random.seed(42 + idx)
        for i in np.linspace(-1, 1, 5):
            x = np.linspace(-1, 1, 50)
            if ttype == 'rigid':
                theta = 0.2  # ~11.5 degree rotation
                tx, ty = 0.08, 0.1  # translation
                y_h = np.full_like(x, i) * np.cos(theta) - x * np.sin(theta) + ty
                x_h = x * np.cos(theta) + np.full_like(x, i) * np.sin(theta) + tx
                y_v = x * np.cos(theta) - np.full_like(x, i) * np.sin(theta) + ty
                x_v = np.full_like(x, i) * np.cos(theta) + x * np.sin(theta) + tx
            elif ttype == 'affine':
                y_h = np.full_like(x, i) + x * 0.15
                x_h = x * 1.1
                y_v = x + np.full_like(x, i) * 0.15
                x_v = np.full_like(x, i) * 1.1
            elif ttype == 'projective':
                denom = 1 + 0.1 * x + 0.05 * np.full_like(x, i)
                y_h = np.full_like(x, i) / denom
                x_h = x / denom
                denom2 = 1 + 0.1 * np.full_like(x, i) + 0.05 * x
                y_v = x / denom2
                x_v = np.full_like(x, i) / denom2
            else:  # deformable
                y_h = np.full_like(x, i) + 0.08 * np.sin(2 * np.pi * x)
                x_h = x + 0.05 * np.cos(2.5 * np.pi * np.full_like(x, i))
                y_v = x + 0.08 * np.sin(2 * np.pi * np.full_like(x, i))
                x_v = np.full_like(x, i) + 0.05 * np.cos(2.5 * np.pi * x)

            colors = [GARNET, ATLANTIC, CONGAREE, ROSE]
            ax.plot(x_h, y_h, color=colors[idx], lw=1.0, alpha=0.7, zorder=2)
            ax.plot(x_v, y_v, color=colors[idx], lw=1.0, alpha=0.7, zorder=2)

        ax.set_title(title, fontsize=8, weight='bold', color=BLACK_90, pad=5)

    fig.tight_layout()
    fig.savefig('figures/fig3_transforms.pdf', bbox_inches='tight', dpi=300)
    fig.savefig('figures/fig3_transforms.png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    print("Figure 3: Transform Families saved.")


# ============================================================
# Figure 4: Augmentation Policy Search Space
# ============================================================
def fig4_augmentation_space():
    fig, ax = plt.subplots(1, 1, figsize=(8, 4.5))
    ax.set_xlim(0, 8.4)
    ax.set_ylim(0, 4.8)
    ax.axis('off')

    # Categories - 4 columns
    categories = [
        ('Geometric', ['Random Crop', 'Flip / Rotate', 'Elastic Deform', 'Scale Jitter'],
         ATLANTIC, 0.2),
        ('Photometric', ['Brightness', 'Contrast', 'Gamma Shift', 'Noise Injection'],
         CONGAREE, 2.2),
        ('Modality-Specific', ['IR Gain Adjust', 'Thermal Drift', 'RGB White Bal.', 'Channel Swap'],
         HORSESHOE, 4.2),
        ('Weather / Environ.', ['Fog Simulation', 'Rain Overlay', 'Low-Light Dim', 'Glare / Bloom'],
         ROSE, 6.2),
    ]

    col_w = 1.9
    for cat_name, items, color, x_start in categories:
        # Category header
        draw_box(ax, (x_start, 3.8), col_w, 0.7, cat_name, color=color, fontsize=9, bold=True)
        # Arrow from bottom item to RL banner
        ax.annotate('', xy=(x_start + col_w/2, 0.75), xytext=(x_start + col_w/2, 1.2),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
        # Item boxes
        for i, item in enumerate(items):
            y = 3.0 - i * 0.6
            draw_box(ax, (x_start, y), col_w, 0.5, item, color=BLACK_10, text_color=BLACK_90, fontsize=8)

    # Bottom: RL selects combination + magnitude
    ax.add_patch(FancyBboxPatch((0.2, 0.2), 8.0, 0.55, boxstyle="square,pad=0",
                                facecolor=SANDSTORM, edgecolor=GARNET, linewidth=1.5, linestyle='--'))
    ax.text(4.2, 0.47, 'RL Policy selects: (augmentation type, magnitude, probability) per batch',
            ha='center', fontsize=9, weight='bold', color=GARNET)

    fig.tight_layout()
    fig.savefig('figures/fig4_augmentation_space.pdf', bbox_inches='tight', dpi=300)
    fig.savefig('figures/fig4_augmentation_space.png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    print("Figure 4: Augmentation Space saved.")


# ============================================================
# Figure 5: Domain Transfer Across Water Bodies
# ============================================================
def fig5_domain_transfer():
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 5.2)
    ax.axis('off')

    # === TOP ROW: Three environment domains, evenly spaced ===
    envs = [
        ('Lake Domain', ATLANTIC, 1.3),
        ('River Domain', CONGAREE, 4.0),
        ('Coastal Domain', HORSESHOE, 6.7),
    ]
    for name, color, x in envs:
        draw_box(ax, (x - 0.9, 4.0), 1.8, 0.8, name, color=color, fontsize=9, bold=True)

    # Transfer arrows between domains (through the boxes, at midline)
    ax.annotate('', xy=(2.2, 4.4), xytext=(3.1, 4.4),
                arrowprops=dict(arrowstyle='<->', color=ROSE, lw=2.5, linestyle='--'))
    ax.annotate('', xy=(4.9, 4.4), xytext=(5.8, 4.4),
                arrowprops=dict(arrowstyle='<->', color=ROSE, lw=2.5, linestyle='--'))
    ax.text(2.65, 4.55, 'knowledge transfer', ha='center', fontsize=7, color=ROSE, style='italic')
    ax.text(5.35, 4.55, 'knowledge transfer', ha='center', fontsize=7, color=ROSE, style='italic')

    # === MIDDLE: Shared RL Policy (dominant, centered) ===
    rl_box = FancyBboxPatch((2.0, 2.5), 4.0, 1.0, boxstyle="square,pad=0",
                             facecolor=GARNET, edgecolor=BLACK, linewidth=2.5)
    ax.add_patch(rl_box)
    ax.text(4.0, 3.0, 'Shared RL Policy + Environment Conditioning $e$',
            ha='center', va='center', fontsize=10, color=WHITE, weight='bold')

    # Arrows from domains down to policy (darker)
    for x in [1.3, 4.0, 6.7]:
        draw_arrow(ax, (x, 4.0), (x if x == 4.0 else (x + (4.0 - x) * 0.4), 3.5),
                   color=BLACK_70, lw=2.0)

    # === BOTTOM ROW: Evaluation scenarios ===
    eval_y = 0.4
    eval_h = 1.3
    scenarios = [
        ('In-Domain\nEvaluation', 'Train = Test env', BLACK_10, BLACK_90, 0.5),
        ('Cross-Domain\nTransfer', 'Held-out env', SANDSTORM, BLACK_90, 3.0),
        ('Unseen Location\nGeneralization', 'Same env, new site', BLACK_10, BLACK_90, 5.5),
    ]
    for name, desc, bg, tc, x in scenarios:
        draw_box(ax, (x, eval_y), 2.0, eval_h, '', color=bg, text_color=tc, fontsize=8)
        ax.text(x + 1.0, eval_y + eval_h - 0.35, name, ha='center', va='center',
                fontsize=9, weight='bold', color=BLACK_90)
        ax.text(x + 1.0, eval_y + 0.25, desc, ha='center', va='center',
                fontsize=8, color=BLACK_70, style='italic')

    # Arrows from policy to evaluation (darker)
    draw_arrow(ax, (3.0, 2.5), (1.5, eval_y + eval_h), color=BLACK_70, lw=2.0)
    draw_arrow(ax, (4.0, 2.5), (4.0, eval_y + eval_h), color=BLACK_70, lw=2.0)
    draw_arrow(ax, (5.0, 2.5), (6.5, eval_y + eval_h), color=BLACK_70, lw=2.0)

    fig.tight_layout()
    fig.savefig('figures/fig5_domain_transfer.pdf', bbox_inches='tight', dpi=300)
    fig.savefig('figures/fig5_domain_transfer.png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    print("Figure 5: Domain Transfer saved.")


# ============================================================
# Figure 6: Expected Results / Baseline Comparison
# ============================================================
def fig6_expected_results():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    # Left: Bar chart of expected alignment error by method
    methods = ['Classical\nOnly', 'Fixed Deep\nReg.', 'AutoAugment\n(Non-RL)', 'RL Policy\n(Ours)']
    alignment_errors = [8.2, 5.4, 4.1, 2.8]
    colors = [BLACK_70, ATLANTIC, HONEYCOMB, GARNET]

    bars = ax1.bar(methods, alignment_errors, color=colors, edgecolor=BLACK_90, linewidth=0.8, width=0.65)
    ax1.set_ylabel('Mean Alignment Error (px)', fontsize=10, color=BLACK_90)
    ax1.set_title('Registration Accuracy by Method', fontsize=11, weight='bold', color=BLACK_90, pad=10)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.set_ylim(0, 10)
    for bar, val in zip(bars, alignment_errors):
        ax1.text(bar.get_x() + bar.get_width()/2, val + 0.2, f'{val}', ha='center', fontsize=9, color=BLACK_70)

    # Right: Line chart of robustness across conditions
    conditions = ['Clear', 'Overcast', 'Fog', 'Rain', 'Night']
    x = np.arange(len(conditions))

    classical = [0.78, 0.72, 0.51, 0.45, 0.30]
    deep_fixed = [0.85, 0.80, 0.68, 0.62, 0.50]
    autoaug = [0.87, 0.83, 0.74, 0.69, 0.58]
    rl_ours = [0.90, 0.88, 0.83, 0.80, 0.75]

    ax2.plot(x, classical, 'o-', color=BLACK_70, lw=2, markersize=8, label='Classical')
    ax2.plot(x, deep_fixed, 's-', color=ATLANTIC, lw=2, markersize=8, label='Fixed Deep Reg.')
    ax2.plot(x, autoaug, '^-', color=HONEYCOMB, lw=2, markersize=8, label='AutoAugment')
    ax2.plot(x, rl_ours, 'D-', color=GARNET, lw=2.5, markersize=9, label='RL Policy (Ours)')

    ax2.set_xticks(x)
    ax2.set_xticklabels(conditions, fontsize=9)
    ax2.set_ylabel('Downstream Task Score (F1)', fontsize=10, color=BLACK_90)
    ax2.set_title('Robustness Across Conditions', fontsize=11, weight='bold', color=BLACK_90, pad=10)
    ax2.legend(fontsize=8, frameon=True, edgecolor=BLACK_30, loc='lower left')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.set_ylim(0.2, 1.0)

    fig.tight_layout()
    fig.savefig('figures/fig6_expected_results.pdf', bbox_inches='tight', dpi=300)
    fig.savefig('figures/fig6_expected_results.png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    print("Figure 6: Expected Results saved.")


# ============================================================
# Figure 7: Weather Robustness Challenge Illustration
# ============================================================
def fig7_weather_conditions():
    fig, axes = plt.subplots(2, 4, figsize=(10, 5.5))

    conditions = ['Clear Day', 'Overcast', 'Fog / Haze', 'Night']
    np.random.seed(123)

    # Create a more realistic synthetic maritime scene
    res = 400
    x = np.linspace(0, 1, res)
    y = np.linspace(0, 1, res)
    X, Y = np.meshgrid(x, y)

    # Base scene regions
    horizon_y = 0.38
    sky = np.where(Y < horizon_y, 1.0, 0.0)
    water = np.where(Y >= horizon_y, 1.0, 0.0)

    # Horizon line (sharp)
    horizon_band = np.exp(-((Y - horizon_y)**2) / 0.0003) * 0.4

    # Wave texture on water
    wave1 = 0.04 * np.sin(40 * X + 8 * Y) * water
    wave2 = 0.025 * np.sin(25 * X - 12 * Y + 3) * water
    wave3 = 0.015 * np.cos(60 * X + 4 * Y) * water

    # Boat shapes: rectangular hulls + vertical masts
    def make_boat(cx, cy, hull_w, hull_h, mast_h):
        hull = np.where((np.abs(X - cx) < hull_w/2) & (np.abs(Y - cy) < hull_h/2), 1.0, 0.0)
        # Soft edges
        hull_soft = np.exp(-((X - cx)**2 / (hull_w/2)**2 + (Y - cy)**2 / (hull_h/2)**2) * 3)
        hull_soft = np.where(hull_soft > 0.3, hull_soft, 0.0)
        # Mast (thin vertical line above hull)
        mast = np.exp(-((X - cx)**2) / 0.00005) * np.where((Y < cy - hull_h/2) & (Y > cy - hull_h/2 - mast_h), 1.0, 0.0)
        return hull_soft + mast * 0.7

    boat1 = make_boat(0.22, 0.52, 0.12, 0.06, 0.12)
    boat2 = make_boat(0.55, 0.48, 0.15, 0.07, 0.15)
    boat3 = make_boat(0.78, 0.55, 0.10, 0.05, 0.10)

    # Cloud-like features in sky
    cloud1 = np.exp(-((X - 0.3)**2 / 0.02 + (Y - 0.15)**2 / 0.003)) * 0.3
    cloud2 = np.exp(-((X - 0.7)**2 / 0.03 + (Y - 0.2)**2 / 0.004)) * 0.25

    boats = boat1 + boat2 + boat3
    scene_base = horizon_band + wave1 + wave2 + wave3 + boats + cloud1 + cloud2

    for col, cond in enumerate(conditions):
        ax = axes[0, col]

        if cond == 'Clear Day':
            r = sky * 0.45 + water * 0.08 + boats * 0.35 + cloud1 * 0.5 + cloud2 * 0.5 + horizon_band * 0.2
            g = sky * 0.58 + water * 0.22 + boats * 0.28 + wave1 * 0.3 + cloud1 * 0.5 + cloud2 * 0.5 + horizon_band * 0.2
            b = sky * 0.82 + water * 0.42 + boats * 0.15 + wave2 * 0.3 + cloud1 * 0.55 + cloud2 * 0.55 + horizon_band * 0.3
            noise_std = 0.012
        elif cond == 'Overcast':
            base_r = sky * 0.5 + water * 0.18 + boats * 0.25 + horizon_band * 0.15
            base_g = sky * 0.5 + water * 0.2 + boats * 0.2 + wave1 * 0.2 + horizon_band * 0.15
            base_b = sky * 0.55 + water * 0.28 + boats * 0.15 + wave2 * 0.2 + horizon_band * 0.2
            r, g, b = base_r + 0.1, base_g + 0.1, base_b + 0.12
            noise_std = 0.02
        elif cond == 'Fog / Haze':
            fog = 0.7
            base_r = sky * 0.35 + water * 0.1 + boats * 0.12 + horizon_band * 0.05
            base_g = sky * 0.4 + water * 0.12 + boats * 0.1 + horizon_band * 0.05
            base_b = sky * 0.45 + water * 0.15 + boats * 0.08 + horizon_band * 0.06
            r = base_r * 0.3 + fog
            g = base_g * 0.3 + fog
            b = base_b * 0.3 + fog + 0.02
            noise_std = 0.018
        else:  # Night - faint moonlight glow so it doesn't look blank
            moonlight = np.exp(-((X - 0.6)**2 / 0.08 + (Y - 0.1)**2 / 0.02)) * 0.06
            r = sky * 0.02 + water * 0.012 + boats * 0.05 + horizon_band * 0.015 + moonlight * 0.3
            g = sky * 0.02 + water * 0.015 + boats * 0.04 + horizon_band * 0.015 + moonlight * 0.4
            b = sky * 0.045 + water * 0.025 + boats * 0.025 + horizon_band * 0.02 + moonlight * 0.6
            noise_std = 0.02

        rgb = np.stack([r, g, b], axis=-1)
        rgb = np.clip(rgb + np.random.normal(0, noise_std, rgb.shape), 0, 1)
        ax.imshow(rgb)
        ax.axis('off')
        ax.set_title(cond, fontsize=10, weight='bold', color=BLACK_90, pad=5)

        # Bottom row: IR (thermal) - consistent across conditions
        ax2 = axes[1, col]
        # Thermal: water is cool, sky is medium, boats are HOT
        ir_base = water * 0.25 + sky * 0.32 + horizon_band * 0.3
        ir_boats = boats * 1.3  # warm thermal signatures from engines/hulls
        ir_waves = wave1 * 0.15 + wave3 * 0.1  # subtle water texture
        ir = ir_base + ir_boats + ir_waves

        if cond == 'Night':
            # Better thermal contrast at night
            ir = water * 0.2 + sky * 0.28 + boats * 1.6 + horizon_band * 0.25 + ir_waves

        ir = np.clip(ir + np.random.normal(0, 0.01, ir.shape), 0, 1)
        ax2.imshow(ir, cmap='inferno')
        ax2.axis('off')

    # Row labels on the left side (outside the axes) - larger, black for print
    axes[0, 0].text(-0.18, 0.5, 'RGB', transform=axes[0, 0].transAxes,
                     fontsize=14, weight='bold', color=BLACK_90, rotation=90,
                     va='center', ha='center')
    axes[1, 0].text(-0.18, 0.5, 'IR', transform=axes[1, 0].transAxes,
                     fontsize=14, weight='bold', color=BLACK_90, rotation=90,
                     va='center', ha='center')

    fig.tight_layout(h_pad=0.8, w_pad=0.5)
    fig.savefig('figures/fig7_weather_conditions.pdf', bbox_inches='tight', dpi=300)
    fig.savefig('figures/fig7_weather_conditions.png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    print("Figure 7: Weather Conditions saved.")


# ============================================================
# Figure 8: SAC Algorithm Architecture
# ============================================================
def fig8_sac_architecture():
    fig, ax = plt.subplots(1, 1, figsize=(9, 5.8))
    ax.set_xlim(0, 9.5)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    # === TOP LEFT: Registration Environment ===
    draw_box(ax, (0.2, 5.5), 2.0, 1.0, 'Registration\nEnvironment', color=WARM_GREY, fontsize=9)

    # === CENTER: Actor (dominant, garnet) ===
    actor_box = FancyBboxPatch((2.8, 5.2), 2.5, 1.3, boxstyle="square,pad=0",
                                facecolor=GARNET, edgecolor=BLACK, linewidth=2.5)
    ax.add_patch(actor_box)
    ax.text(4.05, 5.85, 'Actor $\\pi_\\phi$\n(Policy Network)', ha='center', va='center',
            fontsize=11, color=WHITE, weight='bold')

    # === RIGHT: Twin Critics ===
    draw_box(ax, (6.0, 5.5), 1.5, 0.9, 'Critic\n$Q_{\\theta_1}$', color=ATLANTIC, fontsize=10, bold=True)
    draw_box(ax, (7.8, 5.5), 1.5, 0.9, 'Critic\n$Q_{\\theta_2}$', color=ATLANTIC, fontsize=10, bold=True)

    # === MIDDLE LEFT: Replay Buffer ===
    draw_box(ax, (0.2, 3.4), 2.0, 1.2, 'Replay Buffer\n$(s, a, r, s\')$', color=BLACK_10,
             text_color=BLACK_90, fontsize=9)

    # === MIDDLE CENTER: Temperature ===
    draw_box(ax, (3.5, 3.6), 2.0, 0.8, 'Temperature $\\alpha$\n(auto-tuned)', color=HONEYCOMB,
             text_color=WHITE, fontsize=9)

    # === MIDDLE RIGHT: Target networks ===
    draw_box(ax, (6.0, 3.6), 1.5, 0.8, 'Target\n$\\bar{Q}_{\\theta_1}$', color=CONGAREE, fontsize=9)
    draw_box(ax, (7.8, 3.6), 1.5, 0.8, 'Target\n$\\bar{Q}_{\\theta_2}$', color=CONGAREE, fontsize=9)

    # === BOTTOM: Objective equation box (with border) ===
    eq_box = FancyBboxPatch((0.2, 0.3), 9.1, 1.8, boxstyle="square,pad=0",
                             facecolor=SANDSTORM, edgecolor=BLACK_30, linewidth=1.2)
    ax.add_patch(eq_box)
    ax.text(4.75, 1.6, 'SAC Objective: $J(\\pi) = \\mathbb{E}_{s_t}\\left[\\mathbb{E}_{a_t \\sim \\pi}\\left[\\alpha \\log \\pi(a_t|s_t) - Q(s_t, a_t)\\right]\\right]$',
            ha='center', fontsize=10, color=BLACK_90)
    ax.text(4.75, 0.8, 'Entropy regularization encourages exploration of diverse registration strategies',
            ha='center', fontsize=9, color=BLACK_70, style='italic')

    # ---- ARROWS ----

    # Actor -> Environment (action)
    draw_arrow(ax, (2.8, 5.85), (2.2, 5.85), color=GARNET, lw=2.5)
    ax.text(1.6, 6.3, '$a_t \\sim \\pi_\\phi(\\cdot|s_t)$', fontsize=10, color=GARNET, weight='bold')

    # Environment -> Replay Buffer (store transitions)
    draw_arrow(ax, (1.2, 5.5), (1.2, 4.6), color=WARM_GREY, lw=2.0)

    # Replay Buffer -> Actor (sample batch)
    draw_arrow(ax, (2.2, 4.2), (2.8, 5.3), color=BLACK_70, lw=2.0)
    ax.text(2.05, 4.8, 'sample', fontsize=8, color=BLACK_70, style='italic')

    # Replay Buffer -> Critics (sample batch for critic update)
    ax.plot([2.2, 4.5, 4.5], [3.8, 3.8, 5.0], color=BLACK_70, lw=1.5, linestyle='-')
    ax.annotate('', xy=(6.0, 5.9), xytext=(4.5, 5.0),
                arrowprops=dict(arrowstyle='->', color=BLACK_70, lw=1.5))

    # Actor -> Critics (actor output for critic eval)
    draw_arrow(ax, (5.3, 5.85), (6.0, 5.85), color=GARNET, lw=2.0)

    # Soft update: Critics -> Targets
    draw_arrow(ax, (6.75, 5.5), (6.75, 4.4), color=BLACK_70, lw=1.5)
    draw_arrow(ax, (8.55, 5.5), (8.55, 4.4), color=BLACK_70, lw=1.5)
    ax.text(6.9, 4.85, '$\\tau$', fontsize=11, color=BLACK_70, weight='bold')
    ax.text(8.7, 4.85, '$\\tau$', fontsize=11, color=BLACK_70, weight='bold')

    # Soft update label
    ax.text(7.65, 4.6, 'soft\nupdate', fontsize=8, color=BLACK_70, ha='center', style='italic')

    # Policy gradient label under actor
    ax.text(4.05, 5.0, '$\\nabla_\\phi J(\\pi)$', fontsize=10, color=GARNET, ha='center', weight='bold')

    fig.tight_layout()
    fig.savefig('figures/fig8_sac_architecture.pdf', bbox_inches='tight', dpi=300)
    fig.savefig('figures/fig8_sac_architecture.png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    print("Figure 8: SAC Architecture saved.")


if __name__ == '__main__':
    fig1_system_architecture()
    fig2_rl_loop()
    fig3_transform_families()
    fig4_augmentation_space()
    fig5_domain_transfer()
    fig6_expected_results()
    fig7_weather_conditions()
    fig8_sac_architecture()
    print("\nAll figures generated successfully!")
