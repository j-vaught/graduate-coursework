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
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis('off')
    ax.set_aspect('equal')

    # Title
    ax.text(5, 6.2, 'RL-Optimized IR/RGB Registration and Augmentation Pipeline',
            ha='center', va='center', fontsize=13, weight='bold', color=GARNET)

    # Input sensors
    draw_box(ax, (0.2, 4.5), 1.8, 0.9, 'IR Camera\nInput', color=CONGAREE)
    draw_box(ax, (0.2, 3.2), 1.8, 0.9, 'RGB Camera\nInput', color=ATLANTIC)

    # Feature extraction
    draw_box(ax, (3.0, 3.6), 1.8, 1.2, 'Feature\nExtraction\n& Quality\nAssessment', color=BLACK_70)

    # RL Agent (central)
    draw_box(ax, (5.8, 3.4), 2.2, 1.6, 'RL Policy\nNetwork\n(SAC/TD3)', color=GARNET, fontsize=10, bold=True)

    # Actions output
    draw_box(ax, (5.8, 1.5), 1.0, 1.4, 'Registration\nTransform\nSelection', color=HORSESHOE, text_color=WHITE, fontsize=8)
    draw_box(ax, (7.0, 1.5), 1.0, 1.4, 'Augmentation\nRecipe\nSelection', color=HONEYCOMB, text_color=WHITE, fontsize=8)

    # Registration module
    draw_box(ax, (3.0, 0.3), 1.8, 0.9, 'Registration\n& Fusion\nModule', color=ATLANTIC)

    # Downstream task
    draw_box(ax, (5.8, 0.3), 2.2, 0.8, 'Downstream\nPerception Task', color=CONGAREE, fontsize=9)

    # Reward signal
    draw_box(ax, (8.8, 3.6), 1.0, 1.2, 'Reward\nComputation\n$r_t$', color=ROSE, fontsize=8)

    # Environment tag
    draw_box(ax, (3.0, 5.2), 1.8, 0.6, 'Environment Tag\n(lake/river/coast)', color=WARM_GREY, fontsize=8)

    # Arrows: inputs to feature extraction
    draw_arrow(ax, (2.0, 4.95), (3.0, 4.4))
    draw_arrow(ax, (2.0, 3.65), (3.0, 4.0))

    # Feature extraction to RL agent
    draw_arrow(ax, (4.8, 4.2), (5.8, 4.2))

    # Env tag to RL agent
    draw_arrow(ax, (4.8, 5.3), (6.9, 5.0))

    # RL agent to actions
    draw_arrow(ax, (6.3, 3.4), (6.3, 2.9))
    draw_arrow(ax, (7.5, 3.4), (7.5, 2.9))

    # Actions to registration
    draw_arrow(ax, (5.8, 2.0), (4.8, 1.0))

    # Registration gets inputs
    draw_arrow(ax, (1.1, 3.2), (1.1, 1.2), style='->')
    ax.annotate('', xy=(3.0, 0.75), xytext=(1.1, 0.75),
                arrowprops=dict(arrowstyle='->', color=BLACK_70, lw=1.5))

    # Registration to downstream
    draw_arrow(ax, (4.8, 0.7), (5.8, 0.7))

    # Downstream to reward
    draw_arrow(ax, (8.0, 0.7), (9.3, 0.7))
    ax.annotate('', xy=(9.3, 3.6), xytext=(9.3, 0.7),
                arrowprops=dict(arrowstyle='->', color=ROSE, lw=2.0))

    # Reward back to agent
    draw_arrow(ax, (8.8, 4.2), (8.0, 4.2), color=ROSE, lw=2.0)

    # Labels for state/action/reward
    ax.text(5.3, 4.5, '$s_t$', fontsize=12, color=GARNET, weight='bold')
    ax.text(6.7, 3.1, '$a_t$', fontsize=12, color=GARNET, weight='bold')
    ax.text(8.3, 4.5, '$r_t$', fontsize=12, color=ROSE, weight='bold')

    fig.tight_layout()
    fig.savefig('figures/fig1_system_architecture.pdf', bbox_inches='tight', dpi=300)
    fig.savefig('figures/fig1_system_architecture.png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    print("Figure 1: System Architecture saved.")


# ============================================================
# Figure 2: RL Loop Detail (MDP Formulation)
# ============================================================
def fig2_rl_loop():
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 5.5)
    ax.axis('off')
    ax.set_aspect('equal')

    ax.text(4, 5.2, 'Markov Decision Process Formulation',
            ha='center', va='center', fontsize=13, weight='bold', color=GARNET)

    # State box
    draw_box(ax, (0.3, 2.8), 2.2, 1.8, '', color=BLACK_10, text_color=BLACK_90)
    ax.text(1.4, 4.3, 'State $s_t$', ha='center', fontsize=11, weight='bold', color=GARNET)
    state_items = [
        'Frame quality cues',
        'Alignment residuals',
        'Environment tag $e$',
        'Prior action history',
    ]
    for i, item in enumerate(state_items):
        ax.text(1.4, 3.0 + (3-i)*0.35, f'  {item}', ha='center', fontsize=8, color=BLACK_70)

    # Action box
    draw_box(ax, (3.0, 2.8), 2.0, 1.8, '', color=SANDSTORM, text_color=BLACK_90)
    ax.text(4.0, 4.3, 'Action $a_t$', ha='center', fontsize=11, weight='bold', color=GARNET)
    action_items = [
        'Transform family $\\tau$',
        'Transform params $\\theta$',
        'Augmentation type',
        'Augmentation strength',
    ]
    for i, item in enumerate(action_items):
        ax.text(4.0, 3.0 + (3-i)*0.35, f'  {item}', ha='center', fontsize=8, color=BLACK_70)

    # Reward box
    draw_box(ax, (5.5, 2.8), 2.2, 1.8, '', color='#F5E6E8', text_color=BLACK_90)
    ax.text(6.6, 4.3, 'Reward $r_t$', ha='center', fontsize=11, weight='bold', color=ROSE)
    reward_items = [
        'Alignment error $\\downarrow$',
        'Perception gain $\\uparrow$',
        'Robustness score',
        'Consistency penalty',
    ]
    for i, item in enumerate(reward_items):
        ax.text(6.6, 3.0 + (3-i)*0.35, f'  {item}', ha='center', fontsize=8, color=BLACK_70)

    # Arrows connecting them
    draw_arrow(ax, (2.5, 3.7), (3.0, 3.7), color=GARNET, lw=2)
    draw_arrow(ax, (5.0, 3.7), (5.5, 3.7), color=GARNET, lw=2)

    # Environment block below
    draw_box(ax, (1.5, 0.5), 5.0, 1.6, '', color=WHITE)
    ax.add_patch(FancyBboxPatch((1.5, 0.5), 5.0, 1.6, boxstyle="square,pad=0",
                                facecolor='none', edgecolor=GARNET, linewidth=2.0, linestyle='--'))
    ax.text(4.0, 1.85, 'Environment: IR/RGB Registration Pipeline', ha='center',
            fontsize=10, weight='bold', color=GARNET)
    ax.text(4.0, 1.35, 'Classical Registration  |  Deep Registration  |  Augmentation Engine',
            ha='center', fontsize=8, color=BLACK_70)
    ax.text(4.0, 0.85, 'Downstream Task Evaluator (Detection / Tracking / Segmentation)',
            ha='center', fontsize=8, color=BLACK_70)

    # Arrows from action to environment and back
    draw_arrow(ax, (4.0, 2.8), (4.0, 2.1), color=ATLANTIC, lw=2)
    ax.text(4.3, 2.4, '$a_t$', fontsize=10, color=ATLANTIC, weight='bold')

    # Environment back to state (left side)
    ax.annotate('', xy=(1.4, 2.8), xytext=(1.4, 2.1),
                arrowprops=dict(arrowstyle='->', color=CONGAREE, lw=2))
    ax.text(0.8, 2.35, '$s_{t+1}$', fontsize=10, color=CONGAREE, weight='bold')

    # Environment to reward (right side)
    ax.annotate('', xy=(6.6, 2.8), xytext=(6.6, 2.1),
                arrowprops=dict(arrowstyle='->', color=ROSE, lw=2))
    ax.text(6.9, 2.35, '$r_t$', fontsize=10, color=ROSE, weight='bold')

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
                y_h = np.full_like(x, i) * np.cos(0.15) - x * np.sin(0.15) * 0.0 + 0.1
                x_h = x * np.cos(0.15) + np.full_like(x, i) * np.sin(0.15) * 0.0 + 0.05
                y_v = x * np.cos(0.15) + 0.1
                x_v = np.full_like(x, i) * np.cos(0.15) + 0.05
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

    fig.suptitle('Registration Transform Families in Action Space', fontsize=12,
                 weight='bold', color=GARNET, y=1.05)
    fig.tight_layout()
    fig.savefig('figures/fig3_transforms.pdf', bbox_inches='tight', dpi=300)
    fig.savefig('figures/fig3_transforms.png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    print("Figure 3: Transform Families saved.")


# ============================================================
# Figure 4: Augmentation Policy Search Space
# ============================================================
def fig4_augmentation_space():
    fig, ax = plt.subplots(1, 1, figsize=(9, 4))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    ax.text(4.5, 4.2, 'Augmentation Policy Search Space', ha='center',
            fontsize=13, weight='bold', color=GARNET)

    # Categories
    categories = [
        ('Geometric', ['Random Crop', 'Flip / Rotate', 'Elastic Deform', 'Scale Jitter'],
         ATLANTIC, 0.3),
        ('Photometric', ['Brightness', 'Contrast', 'Gamma Shift', 'Noise Injection'],
         CONGAREE, 2.5),
        ('Modality-Specific', ['IR Gain Adjust', 'Thermal Drift', 'RGB White Bal.', 'Channel Swap'],
         HORSESHOE, 4.7),
        ('Weather/Environ.', ['Fog Simulation', 'Rain Overlay', 'Low-Light Dim', 'Glare/Bloom'],
         ROSE, 6.9),
    ]

    for cat_name, items, color, x_start in categories:
        draw_box(ax, (x_start, 3.0), 1.8, 0.7, cat_name, color=color, fontsize=8, bold=True)
        for i, item in enumerate(items):
            y = 2.4 - i * 0.55
            draw_box(ax, (x_start, y), 1.8, 0.45, item, color=BLACK_10, text_color=BLACK_90, fontsize=7)

    # Bottom: RL selects combination + magnitude
    ax.add_patch(FancyBboxPatch((0.3, 0.1), 8.4, 0.5, boxstyle="square,pad=0",
                                facecolor=SANDSTORM, edgecolor=GARNET, linewidth=1.5, linestyle='--'))
    ax.text(4.5, 0.35, 'RL Policy selects: (augmentation type, magnitude, probability) per training batch',
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
    fig, ax = plt.subplots(1, 1, figsize=(8, 4.5))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 5)
    ax.axis('off')

    ax.text(4, 4.7, 'Cross-Domain Transfer: Environment Adaptation',
            ha='center', fontsize=13, weight='bold', color=GARNET)

    # Three environment domains
    envs = [
        ('Lake', ATLANTIC, 1.2),
        ('River', CONGAREE, 4.0),
        ('Coast', HORSESHOE, 6.8),
    ]

    for name, color, x in envs:
        draw_box(ax, (x - 0.8, 3.5), 1.6, 0.8, f'{name}\nDomain', color=color, fontsize=9, bold=True)

    # Shared RL policy in center
    draw_box(ax, (2.5, 1.8), 3.0, 1.0, 'Shared RL Policy\n+ Environment Conditioning $e$',
             color=GARNET, fontsize=10, bold=True)

    # Arrows from domains to policy
    for x in [1.2, 4.0, 6.8]:
        draw_arrow(ax, (x, 3.5), (4.0, 2.8), color=BLACK_50, lw=1.5)

    # Transfer arrows
    ax.annotate('', xy=(6.0, 3.9), xytext=(2.0, 3.9),
                arrowprops=dict(arrowstyle='<->', color=ROSE, lw=2.0, linestyle='--'))
    ax.text(4.0, 4.15, 'Domain Transfer', ha='center', fontsize=9, color=ROSE, style='italic')

    # Bottom: evaluation scenarios
    draw_box(ax, (0.5, 0.3), 2.0, 1.0, 'In-Domain\nEvaluation\n(Train=Test env)', color=BLACK_10,
             text_color=BLACK_90, fontsize=8)
    draw_box(ax, (3.0, 0.3), 2.0, 1.0, 'Cross-Domain\nTransfer\n(Held-out env)', color=SANDSTORM,
             text_color=BLACK_90, fontsize=8)
    draw_box(ax, (5.5, 0.3), 2.0, 1.0, 'Unseen Location\nGeneralization\n(Same env, new site)', color=BLACK_10,
             text_color=BLACK_90, fontsize=8)

    draw_arrow(ax, (2.5, 1.8), (1.5, 1.3), color=BLACK_50)
    draw_arrow(ax, (4.0, 1.8), (4.0, 1.3), color=BLACK_50)
    draw_arrow(ax, (5.5, 1.8), (6.5, 1.3), color=BLACK_50)

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
    methods = ['Classical\nOnly', 'Fixed Deep\nRegistration', 'AutoAugment\n(Non-RL)', 'RL Policy\n(Ours)']
    alignment_errors = [8.2, 5.4, 4.1, 2.8]
    colors = [BLACK_50, ATLANTIC, HONEYCOMB, GARNET]

    bars = ax1.bar(methods, alignment_errors, color=colors, edgecolor=BLACK_90, linewidth=0.8, width=0.65)
    ax1.set_ylabel('Mean Alignment Error (px)', fontsize=10, color=BLACK_90)
    ax1.set_title('Registration Accuracy by Method', fontsize=11, weight='bold', color=GARNET, pad=10)
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

    ax2.plot(x, classical, 'o-', color=BLACK_50, lw=2, markersize=6, label='Classical')
    ax2.plot(x, deep_fixed, 's-', color=ATLANTIC, lw=2, markersize=6, label='Fixed Deep Reg.')
    ax2.plot(x, autoaug, '^-', color=HONEYCOMB, lw=2, markersize=6, label='AutoAugment')
    ax2.plot(x, rl_ours, 'D-', color=GARNET, lw=2.5, markersize=7, label='RL Policy (Ours)')

    ax2.set_xticks(x)
    ax2.set_xticklabels(conditions, fontsize=9)
    ax2.set_ylabel('Downstream Task Score (F1)', fontsize=10, color=BLACK_90)
    ax2.set_title('Robustness Across Conditions', fontsize=11, weight='bold', color=GARNET, pad=10)
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
    fig, axes = plt.subplots(2, 4, figsize=(10, 5))

    conditions = ['Clear Day', 'Overcast', 'Fog/Haze', 'Night']
    np.random.seed(123)

    for col, cond in enumerate(conditions):
        # Top row: simulated RGB
        ax = axes[0, col]
        # Create a simple scene with varying degradation
        x = np.linspace(0, 4*np.pi, 200)
        y = np.linspace(0, 4*np.pi, 200)
        X, Y = np.meshgrid(x, y)

        # Base scene
        scene = np.sin(X) * np.cos(Y) * 0.5 + 0.5

        if cond == 'Clear Day':
            rgb = np.stack([scene * 0.4, scene * 0.6 + 0.2, scene * 0.8 + 0.1], axis=-1)
        elif cond == 'Overcast':
            rgb = np.stack([scene * 0.5 + 0.2, scene * 0.5 + 0.2, scene * 0.55 + 0.2], axis=-1)
        elif cond == 'Fog/Haze':
            fog = 0.7
            rgb = np.stack([scene * 0.3 + fog, scene * 0.3 + fog, scene * 0.35 + fog], axis=-1)
            rgb = np.clip(rgb, 0, 1)
        else:  # Night
            rgb = np.stack([scene * 0.08, scene * 0.08, scene * 0.12], axis=-1)

        rgb = np.clip(rgb + np.random.normal(0, 0.02, rgb.shape), 0, 1)
        ax.imshow(rgb)
        ax.axis('off')
        if col == 0:
            ax.set_ylabel('RGB', fontsize=11, weight='bold', color=ATLANTIC, rotation=0, labelpad=35)
        ax.set_title(cond, fontsize=10, weight='bold', color=BLACK_90, pad=5)

        # Bottom row: simulated IR (thermal)
        ax2 = axes[1, col]
        # IR is more consistent across conditions
        ir = scene * 0.7 + 0.15
        if cond == 'Night':
            ir = scene * 0.8 + 0.1  # IR actually better at night
        ir = np.clip(ir + np.random.normal(0, 0.015, ir.shape), 0, 1)

        ax2.imshow(ir, cmap='inferno')
        ax2.axis('off')
        if col == 0:
            ax2.set_ylabel('IR', fontsize=11, weight='bold', color=ROSE, rotation=0, labelpad=35)

    fig.suptitle('Multimodal Perception Challenge: RGB Degrades, IR Persists',
                 fontsize=12, weight='bold', color=GARNET, y=1.02)
    fig.tight_layout()
    fig.savefig('figures/fig7_weather_conditions.pdf', bbox_inches='tight', dpi=300)
    fig.savefig('figures/fig7_weather_conditions.png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    print("Figure 7: Weather Conditions saved.")


# ============================================================
# Figure 8: SAC Algorithm Architecture
# ============================================================
def fig8_sac_architecture():
    fig, ax = plt.subplots(1, 1, figsize=(9, 5))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    ax.text(4.5, 5.2, 'Soft Actor-Critic (SAC) Architecture for Registration Control',
            ha='center', fontsize=12, weight='bold', color=GARNET)

    # Replay buffer
    draw_box(ax, (0.3, 3.5), 1.8, 1.2, 'Replay Buffer\n$(s, a, r, s\')$', color=BLACK_10,
             text_color=BLACK_90, fontsize=9)

    # Actor (policy)
    draw_box(ax, (3.0, 3.8), 1.8, 1.0, 'Actor $\\pi_\\phi$\n(Policy Network)', color=GARNET, fontsize=9, bold=True)

    # Critic 1
    draw_box(ax, (5.5, 4.0), 1.5, 0.7, 'Critic $Q_{\\theta_1}$', color=ATLANTIC, fontsize=9, bold=True)

    # Critic 2
    draw_box(ax, (7.2, 4.0), 1.5, 0.7, 'Critic $Q_{\\theta_2}$', color=ATLANTIC, fontsize=9, bold=True)

    # Temperature
    draw_box(ax, (5.5, 3.0), 1.5, 0.6, 'Temperature $\\alpha$\n(auto-tuned)', color=HONEYCOMB,
             text_color=WHITE, fontsize=8)

    # Target networks
    draw_box(ax, (5.5, 2.0), 1.5, 0.6, 'Target $\\bar{Q}_{\\theta_1}$', color=CONGAREE, fontsize=8)
    draw_box(ax, (7.2, 2.0), 1.5, 0.6, 'Target $\\bar{Q}_{\\theta_2}$', color=CONGAREE, fontsize=8)

    # Environment interaction
    draw_box(ax, (0.3, 0.5), 1.8, 1.2, 'Registration\nEnvironment', color=WARM_GREY, fontsize=9)

    # Arrows
    draw_arrow(ax, (2.1, 4.1), (3.0, 4.3))  # buffer to actor
    draw_arrow(ax, (2.1, 3.8), (5.5, 4.3))   # buffer to critic1
    draw_arrow(ax, (4.8, 4.3), (5.5, 4.3))   # actor to critic

    # Actor to environment
    draw_arrow(ax, (3.0, 3.8), (2.1, 1.7), color=GARNET, lw=2)
    ax.text(2.0, 2.8, '$a_t \\sim \\pi_\\phi(\\cdot|s_t)$', fontsize=9, color=GARNET)

    # Environment to buffer
    draw_arrow(ax, (1.2, 1.7), (1.2, 3.5), color=WARM_GREY, lw=1.5)

    # Soft update arrows
    draw_arrow(ax, (6.3, 4.0), (6.3, 2.6), color=BLACK_50, style='->', lw=1.0)
    draw_arrow(ax, (8.0, 4.0), (8.0, 2.6), color=BLACK_50, style='->', lw=1.0)
    ax.text(6.5, 3.4, '$\\tau$', fontsize=9, color=BLACK_50)
    ax.text(8.2, 3.4, '$\\tau$', fontsize=9, color=BLACK_50)

    # Loss labels
    ax.text(3.9, 3.55, '$\\nabla_\\phi J(\\pi)$', fontsize=9, color=GARNET, style='italic')

    # Objective box at bottom
    draw_box(ax, (3.0, 0.3), 5.7, 1.0, '', color=SANDSTORM, text_color=BLACK_90)
    ax.text(5.85, 1.05, 'SAC Objective: $J(\\pi) = \\mathbb{E}_{s_t}\\left[\\mathbb{E}_{a_t \\sim \\pi}\\left[\\alpha \\log \\pi(a_t|s_t) - Q(s_t, a_t)\\right]\\right]$',
            ha='center', fontsize=9, color=BLACK_90)
    ax.text(5.85, 0.55, 'Entropy regularization encourages exploration of diverse registration strategies',
            ha='center', fontsize=8, color=BLACK_70, style='italic')

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
