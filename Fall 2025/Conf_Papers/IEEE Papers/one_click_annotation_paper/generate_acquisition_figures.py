#!/usr/bin/env python3
"""Generate acquisition & preprocessing figures 10-17 for the marine radar paper."""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, FancyArrowPatch
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches

output_dir = "python_figures"

# Figure 10: Furuno NXT Hardware Photo (enhanced version)
def generate_furuno_hardware_detailed():
    fig, ax = plt.subplots(figsize=(11, 9), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Vessel outline
    vessel = patches.Polygon([(1.5, 2), (1.5, 4), (5, 4.5), (5, 2.5), (4.5, 2)],
                            closed=True, fill=True, facecolor='#b0b0b0', edgecolor='black', linewidth=2)
    ax.add_patch(vessel)

    # Cabin
    cabin = Rectangle((2, 3), 1.8, 1, fill=True, facecolor='#d0d0d0', edgecolor='black', linewidth=1.5)
    ax.add_patch(cabin)

    # Mast
    ax.plot([3.5, 3.5], [4.5, 7.5], 'k-', linewidth=4)

    # Radar antenna (dome)
    antenna = Circle((3.5, 7.5), 0.7, fill=True, facecolor='#ff9999', edgecolor='black', linewidth=2.5)
    ax.add_patch(antenna)

    # Antenna mounting bracket
    bracket = Rectangle((3.3, 6.6), 0.4, 0.5, fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(bracket)
    ax.plot([3.5, 3.5], [6.6, 6.6], 'ko', markersize=6)

    # Radar beam visualization (rotating)
    colors_beam = plt.cm.Reds(np.linspace(0.3, 0.8, 7))
    for idx, angle in enumerate(np.linspace(-70, 70, 7)):
        rad = np.radians(angle)
        x_end = 3.5 + 2.5 * np.sin(rad)
        y_end = 7.5 - 2.5 * np.cos(rad)
        ax.plot([3.5, x_end], [7.5, y_end], color=colors_beam[idx], linestyle='--',
               linewidth=1.5, alpha=0.6)

    # Control unit below deck
    control = FancyBboxPatch((1.8, 0.5), 2.2, 1.2, boxstyle="round,pad=0.15",
                            fill=True, facecolor='#cccccc', edgecolor='black', linewidth=2)
    ax.add_patch(control)
    ax.text(2.9, 1.1, 'Control Unit\n(GPU/CPU)', ha='center', va='center',
           fontsize=9, fontweight='bold')

    # Power cable
    ax.plot([2.2, 2.2], [1.7, 2.5], 'r-', linewidth=2.5)
    ax.plot([3.6, 3.6], [1.7, 2.5], 'b-', linewidth=2.5)

    # Water
    water = Rectangle((0, 0), 12, 1.5, fill=True, facecolor='#4a90e2', alpha=0.25)
    ax.add_patch(water)

    # Annotations with arrows
    # Antenna label
    arrow1 = FancyArrowPatch((4.5, 7.5), (5.5, 7.5), arrowstyle='->',
                            mutation_scale=20, linewidth=2, color='darkred')
    ax.add_patch(arrow1)
    ax.text(6, 7.5, 'Furuno NXT\nSolid-State Radar', fontsize=10, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='darkred', linewidth=1.5))

    # Rotation rate
    ax.text(3.5, 8.2, '24–48 rpm', fontsize=9, ha='center', fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    # Mast label
    arrow2 = FancyArrowPatch((4, 6), (5.5, 6), arrowstyle='->',
                            mutation_scale=20, linewidth=2, color='darkblue')
    ax.add_patch(arrow2)
    ax.text(6, 6, 'Mounting Mast\n(0–3 nm range)', fontsize=9, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='lightblue', edgecolor='darkblue', linewidth=1.5))

    # Control unit label
    arrow3 = FancyArrowPatch((1.5, 1.1), (0.5, 1.1), arrowstyle='->',
                            mutation_scale=20, linewidth=2, color='darkgreen')
    ax.add_patch(arrow3)
    ax.text(0.2, 1.1, 'Furuno NXT\nControl Unit', fontsize=8, ha='right', va='center', fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='lightgreen', edgecolor='darkgreen', linewidth=1.5))

    ax.set_aspect('equal')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig10_furuno_hardware_detailed.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig10_furuno_hardware_detailed.png")
    plt.close()

# Figure 11: Range-Azimuth Coordinate System Diagram
def generate_range_azimuth_diagram():
    fig, axes = plt.subplots(1, 2, figsize=(14, 7), dpi=150)
    fig.patch.set_facecolor('white')

    # Left: Polar grid visualization
    ax1 = axes[0]
    ax1.set_xlim(-1.2, 1.2)
    ax1.set_ylim(-1.2, 1.2)
    ax1.set_aspect('equal')

    # Range rings
    for r in [0.2, 0.4, 0.6, 0.8, 1.0]:
        theta = np.linspace(0, 2*np.pi, 100)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        ax1.plot(x, y, 'k--', alpha=0.4, linewidth=1)
        if r < 1.0:
            ax1.text(r, 0.05, f'{int(r*868)} bins', fontsize=8, alpha=0.7)

    # Azimuth rays
    n_rays = 12
    for angle in np.linspace(0, 2*np.pi, n_rays, endpoint=False):
        x = np.cos(angle)
        y = np.sin(angle)
        ax1.plot([0, x], [0, y], 'k-', alpha=0.3, linewidth=0.8)

    # Example boat echo (bright spot)
    boat_r, boat_angle = 0.6, np.pi/4
    boat_x = boat_r * np.cos(boat_angle)
    boat_y = boat_r * np.sin(boat_angle)
    circle = Circle((boat_x, boat_y), 0.05, color='red', zorder=10, alpha=0.8)
    ax1.add_patch(circle)
    ax1.arrow(0, 0, boat_x*0.9, boat_y*0.9, head_width=0.05, head_length=0.03,
             fc='red', ec='red', alpha=0.5, linestyle='--')

    # Labels
    ax1.text(0, -1.35, 'Range Ring Spacing:\n868 bins × (0.5–3 nm) ÷ 868',
            ha='center', fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

    ax1.text(0.7, 0.7, 'Boat\nEcho', fontsize=9, color='red', fontweight='bold')

    ax1.set_xlabel('Cartesian X', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Cartesian Y', fontsize=10, fontweight='bold')
    ax1.set_title('Polar Range-Azimuth Grid\n(868 radial bins × ~800 azimuth angles/sweep)',
                 fontsize=11, fontweight='bold')
    ax1.grid(True, alpha=0.2)

    # Right: Data format specification
    ax2 = axes[1]
    ax2.axis('off')

    spec_text = """Raw Radar Data Format

Hardware: Furuno NXT
Antenna Rotation: 24–48 rpm
Full Rotation: PPI Sweep

Range Dimension:
  • 868 range bins
  • ~0.5–3 nm configurable
  • ~20 m bin spacing

Azimuth Dimension:
  • 600–1000 angles/sweep
  • Varies with rotation speed
  • ~0.3–0.6° resolution

Quantization:
  • Effective: 4-bit (16 levels)
  • Plus zero-level background
  • Dynamic range limited

Output per Sweep:
  • Complex or magnitude-only
  • Range × Azimuth matrix
  • Timestamped metadata

Sampling Rate:
  • 24 rpm → ~40 Hz effective
  • 48 rpm → ~80 Hz effective
"""

    ax2.text(0.1, 0.5, spec_text, fontsize=10, family='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9, pad=1),
            verticalalignment='center')

    fig.suptitle('Range-Azimuth Coordinate System: Raw Data Layout',
                fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig11_range_azimuth_diagram.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig11_range_azimuth_diagram.png")
    plt.close()

# Figure 12: Raw Polar Data Quantization
def generate_quantization_comparison():
    fig = plt.figure(figsize=(14, 10), dpi=150)
    fig.patch.set_facecolor('white')

    # Create synthetic raw data
    size = 180
    y, x = np.ogrid[:size, :size]
    center = size / 2
    radius = size / 2
    mask = (x - center)**2 + (y - center)**2 <= radius**2

    # High dynamic range data (floating point)
    hdr_data = np.random.exponential(20, (size, size))
    # Add clutter
    clutter = np.random.rand(size, size) < 0.05
    hdr_data[clutter] = np.random.exponential(30, np.sum(clutter))
    # Add boats
    for _ in range(3):
        bx = int(np.random.uniform(30, size-30))
        by = int(np.random.uniform(30, size-30))
        yb, xb = np.ogrid[max(0, by-8):min(size, by+8), max(0, bx-8):min(size, bx+8)]
        dist = (xb - bx)**2 + (yb - by)**2
        hdr_data[max(0, by-8):min(size, by+8), max(0, bx-8):min(size, bx+8)][dist <= 64] = 200

    hdr_data[~mask] = 0
    hdr_data = np.clip(hdr_data, 0, 255)

    # 4-bit quantization (16 levels)
    quantized_4bit = (hdr_data / 255.0 * 15).astype(int) * (255 / 15)
    quantized_4bit[~mask] = 0

    # 8-bit (hypothetical)
    quantized_8bit = hdr_data.copy()
    quantized_8bit[~mask] = 0

    # Subplots
    ax1 = plt.subplot(2, 3, 1)
    im1 = ax1.imshow(hdr_data, cmap='gray', origin='upper')
    ax1.set_title('Original HDR Data\n(Floating Point)', fontsize=11, fontweight='bold')
    ax1.axis('off')
    plt.colorbar(im1, ax=ax1, label='Intensity')

    ax2 = plt.subplot(2, 3, 2)
    im2 = ax2.imshow(quantized_4bit, cmap='gray', origin='upper')
    ax2.set_title('4-bit Quantized\n(Furuno NXT Actual)', fontsize=11, fontweight='bold', color='red')
    ax2.axis('off')
    plt.colorbar(im2, ax=ax2, label='Intensity')

    ax3 = plt.subplot(2, 3, 3)
    im3 = ax3.imshow(quantized_8bit, cmap='gray', origin='upper')
    ax3.set_title('8-bit Hypothetical\n(For Comparison)', fontsize=11, fontweight='bold', color='green')
    ax3.axis('off')
    plt.colorbar(im3, ax=ax3, label='Intensity')

    # Histograms
    ax4 = plt.subplot(2, 3, 4)
    ax4.hist(hdr_data.flatten(), bins=50, color='steelblue', alpha=0.7, edgecolor='black')
    ax4.set_title('Original Distribution', fontsize=10, fontweight='bold')
    ax4.set_xlabel('Intensity')
    ax4.set_ylabel('Frequency')
    ax4.grid(axis='y', alpha=0.3)

    ax5 = plt.subplot(2, 3, 5)
    ax5.hist(quantized_4bit.flatten(), bins=16, color='coral', alpha=0.7, edgecolor='black')
    ax5.set_title('4-bit Quantized (16 levels)', fontsize=10, fontweight='bold', color='red')
    ax5.set_xlabel('Intensity')
    ax5.set_ylabel('Frequency')
    ax5.set_xlim(0, 260)
    ax5.grid(axis='y', alpha=0.3)

    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')
    comparison_text = """Quantization Effects

4-bit (Furuno NXT):
✓ Compact storage
✓ Fast processing
✗ Loss of dynamic range
✗ Banding artifacts
✗ Reduced contrast

8-bit (Hypothetical):
✓ Better dynamic range
✓ Smoother gradations
✗ 2× memory usage
✗ Slower processing

Impact on Detection:
4-bit still sufficient for:
• Boat detection (strong returns)
• Clutter differentiation
• Range/azimuth localization

Main limitation:
Low-intensity object
detection (small boats,
distant targets)
"""
    ax6.text(0.05, 0.5, comparison_text, fontsize=9, family='monospace',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9),
            verticalalignment='center')

    fig.suptitle('Raw Data Quantization: 4-bit vs. 8-bit Comparison',
                fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig12_quantization_comparison.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig12_quantization_comparison.png")
    plt.close()

# Figure 13: Conversion Pipeline Steps
def generate_conversion_pipeline():
    fig = plt.figure(figsize=(14, 10), dpi=150)
    fig.patch.set_facecolor('white')

    # Create example data at each stage
    size_polar = 150
    size_cart = 150

    # Stage 1: Raw polar data
    y, x = np.ogrid[:size_polar, :size_polar]
    center = size_polar / 2
    radius = size_polar / 2
    mask = (x - center)**2 + (y - center)**2 <= radius**2

    polar_data = np.random.normal(20, 5, (size_polar, size_polar))
    clutter = np.random.rand(size_polar, size_polar) < 0.05
    polar_data[clutter] = np.random.uniform(50, 150, np.sum(clutter))
    for _ in range(2):
        bx = int(np.random.uniform(30, size_polar-30))
        by = int(np.random.uniform(30, size_polar-30))
        yb, xb = np.ogrid[max(0, by-6):min(size_polar, by+6), max(0, bx-6):min(size_polar, bx+6)]
        dist = (xb - bx)**2 + (yb - by)**2
        polar_data[max(0, by-6):min(size_polar, by+6), max(0, bx-6):min(size_polar, bx+6)][dist <= 36] = 200
    polar_data[~mask] = 0
    polar_data = np.clip(polar_data, 0, 255)

    # Stage 2: Cartesian (simple interpolation for demo)
    cartesian_data = polar_data.copy()  # Simplified - real code uses actual polar->cart transform
    cartesian_data = (cartesian_data - cartesian_data.min()) / (cartesian_data.max() - cartesian_data.min()) * 255

    # Stage 3: Intensity mapped
    intensity_mapped = cartesian_data.copy()

    # Stage 4: PNG output (same size)
    png_output = intensity_mapped.copy()

    # Subplots
    ax1 = plt.subplot(2, 3, 1)
    im1 = ax1.imshow(polar_data, cmap='gray', origin='upper')
    ax1.set_title('Stage 1: Raw Polar Data\n(Range × Azimuth)', fontsize=10, fontweight='bold')
    ax1.axis('off')
    ax1.text(0.5, -0.15, '868 bins × 800 angles', ha='center', transform=ax1.transAxes, fontsize=9)

    ax2 = plt.subplot(2, 3, 2)
    im2 = ax2.imshow(cartesian_data, cmap='gray', origin='upper')
    ax2.set_title('Stage 2: Polar→Cartesian\n(Interpolation)', fontsize=10, fontweight='bold')
    ax2.axis('off')
    ax2.text(0.5, -0.15, 'Bilinear interp.', ha='center', transform=ax2.transAxes, fontsize=9)

    ax3 = plt.subplot(2, 3, 3)
    im3 = ax3.imshow(intensity_mapped, cmap='gray', origin='upper')
    ax3.set_title('Stage 3: Intensity Map\n(Contrast Stretch)', fontsize=10, fontweight='bold')
    ax3.axis('off')
    ax3.text(0.5, -0.15, '8-bit grayscale', ha='center', transform=ax3.transAxes, fontsize=9)

    ax4 = plt.subplot(2, 3, 4)
    im4 = ax4.imshow(png_output, cmap='gray', origin='upper')
    ax4.set_title('Stage 4: PNG Output\n(1735×1735)', fontsize=10, fontweight='bold')
    ax4.axis('off')
    ax4.text(0.5, -0.15, 'Ready for DL', ha='center', transform=ax4.transAxes, fontsize=9)

    # Pipeline diagram
    ax5 = plt.subplot(2, 3, (5, 6))
    ax5.axis('off')
    ax5.set_xlim(0, 10)
    ax5.set_ylim(0, 3)

    # Boxes and arrows
    boxes = [
        (0.5, 1.5, 'Raw\nFuruno\nData'),
        (2.5, 1.5, 'Polar→\nCartesian'),
        (4.5, 1.5, 'Quantize\n& Map'),
        (6.5, 1.5, 'Normalize'),
        (8.5, 1.5, '1735×1735\nPNG'),
    ]

    for x, y, label in boxes:
        rect = FancyBboxPatch((x-0.35, y-0.35), 0.7, 0.7, boxstyle="round,pad=0.05",
                             fill=True, facecolor='lightblue', edgecolor='black', linewidth=2)
        ax5.add_patch(rect)
        ax5.text(x, y, label, ha='center', va='center', fontsize=8, fontweight='bold')

    # Arrows
    for i in range(len(boxes)-1):
        x_from = boxes[i][0] + 0.35
        x_to = boxes[i+1][0] - 0.35
        arrow = FancyArrowPatch((x_from, boxes[i][1]), (x_to, boxes[i+1][1]),
                               arrowstyle='->', mutation_scale=20, linewidth=2, color='darkblue')
        ax5.add_patch(arrow)

    # Parameters box
    params_text = """Processing Parameters:
• Interpolation: Bilinear
• Output Resolution: 1735×1735
• Color Map: Grayscale
• Metadata: Recorded (timestamp, range, speed)
• Optional: CFAR preprocessing, contrast stretch
"""
    ax5.text(5, 0.3, params_text, fontsize=8, ha='center',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, pad=0.5))

    fig.suptitle('Conversion Pipeline: Raw Polar → Training-Ready PNG',
                fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig13_conversion_pipeline.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig13_conversion_pipeline.png")
    plt.close()

# Figure 14: Range Setting Variability
def generate_range_variability():
    fig, axes = plt.subplots(1, 3, figsize=(14, 5), dpi=150)
    fig.patch.set_facecolor('white')

    range_settings = [
        (0.5, '0.5 nm\n(Close Range)'),
        (1.5, '1.5 nm\n(Medium Range)'),
        (3.0, '3.0 nm\n(Maximum Range)'),
    ]

    for idx, (range_nm, title) in enumerate(range_settings):
        ax = axes[idx]
        size = 200

        # Scale depends on range setting
        scale_factor = range_nm / 3.0  # Normalize to max 3 nm

        # Create synthetic radar image with scale-dependent features
        img = np.random.normal(10, 3, (size, size))
        y, x = np.ogrid[:size, :size]
        center = size / 2
        radius = size / 2
        mask = (x - center)**2 + (y - center)**2 <= radius**2
        img[~mask] = 0
        img = np.clip(img, 0, 255)

        # Add clutter
        clutter = np.random.rand(size, size) < 0.06
        img[clutter] = np.random.uniform(80, 180, np.sum(clutter))

        # Add boats scaled by range setting
        n_boats = np.random.randint(2, 5)
        for _ in range(n_boats):
            angle = np.random.uniform(0, 2*np.pi)
            r = np.random.uniform(30, radius - 20)
            bx = int(center + r * np.cos(angle))
            by = int(center + r * np.sin(angle))

            # Boat size scales with range (farther = smaller in pixels)
            sz = max(2, int(6 * (1 - scale_factor*0.5)))
            yb, xb = np.ogrid[max(0, by-sz):min(size, by+sz),
                              max(0, bx-sz):min(size, bx+sz)]
            boat_mask = (xb - bx)**2 + (yb - by)**2 <= sz**2
            img[max(0, by-sz):min(size, by+sz),
                max(0, bx-sz):min(size, bx+sz)][boat_mask] = 245

        ax.imshow(img, cmap='gray', origin='upper')
        ax.set_xlim(0, size)
        ax.set_ylim(0, size)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=11, fontweight='bold')

        # Add info text
        info_text = f"Spatial Resolution:\n~{int(1735*(range_nm/3.0)/868)} m/pixel\nObjects appear {'small' if range_nm == 3.0 else 'medium' if range_nm == 1.5 else 'large'}"
        ax.text(0.5, -0.12, info_text, ha='center', transform=ax.transAxes, fontsize=9,
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    fig.suptitle('Range Setting Variability: Impact on Spatial Resolution and Boat Size',
                fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig14_range_variability.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig14_range_variability.png")
    plt.close()

# Figure 15: Echo-Trail Generation Visualization
def generate_echo_trail_visualization():
    fig = plt.figure(figsize=(14, 10), dpi=150)
    fig.patch.set_facecolor('white')

    # Create 4 sequential frames showing boat motion
    size = 160
    frames = []
    boat_positions = [(60, 80), (80, 75), (100, 70), (120, 65)]  # Moving boat

    for idx, (bx, by) in enumerate(boat_positions):
        frame = np.random.normal(15, 3, (size, size))
        y, x = np.ogrid[:size, :size]
        center = size / 2
        radius = size / 2
        mask = (x - center)**2 + (y - center)**2 <= radius**2
        frame[~mask] = 0

        # Clutter
        clutter = np.random.rand(size, size) < 0.04
        frame[clutter] = np.random.uniform(60, 140, np.sum(clutter))

        # Boat
        sz = 5
        yb, xb = np.ogrid[max(0, by-sz):min(size, by+sz), max(0, bx-sz):min(size, bx+sz)]
        boat_mask = (xb - bx)**2 + (yb - by)**2 <= sz**2
        frame[max(0, by-sz):min(size, by+sz), max(0, bx-sz):min(size, bx+sz)][boat_mask] = 240

        frames.append(np.clip(frame, 0, 255))

    # Row 1: Individual frames
    titles = ['Frame T-3\n(Oldest)', 'Frame T-2', 'Frame T-1', 'Frame T\n(Current)']
    for i in range(4):
        ax = plt.subplot(3, 4, i+1)
        ax.imshow(frames[i], cmap='gray', origin='upper')
        ax.set_title(titles[i], fontsize=10, fontweight='bold')
        ax.axis('off')

    # Row 2: Opacity visualization
    opacities = [0.15, 0.35, 0.65, 1.0]
    for i in range(4):
        ax = plt.subplot(3, 4, i+5)
        # Show with opacity info
        ax.imshow(frames[i], cmap='gray', origin='upper', alpha=opacities[i])
        ax.set_facecolor('white')
        ax.set_title(f'α={opacities[i]:.2f}', fontsize=10, fontweight='bold')
        ax.axis('off')

    # Row 3: Composite echo trail
    ax_composite = plt.subplot(3, 2, 5)
    composite = np.zeros_like(frames[0], dtype=float)
    for i, frame in enumerate(frames):
        composite += opacities[i] * frame
    composite = np.clip(composite / 2.0, 0, 255)
    ax_composite.imshow(composite, cmap='gray', origin='upper')
    ax_composite.set_title('Echo Trail Composite\n(T=4)', fontsize=11, fontweight='bold', color='darkred')
    ax_composite.axis('off')

    # Algorithm box
    ax_algo = plt.subplot(3, 2, 6)
    ax_algo.axis('off')
    algo_text = """Echo-Trail Algorithm

Input: Frames I_{t-T+1}...I_t
       Trail length T=4
       Opacity α=[0.15, 0.35, 0.65, 1.0]

Process:
for k ← 1 to T:
  C ← C + α_k · I_{t-T+k}

Output: Composite C (1735×1735 PNG)

Benefits:
✓ Temporal context
✓ Motion perception
✓ Data augmentation
✓ No tracking needed

Variants:
• Trail length: T ∈ {1, 4, 8, 16}
• Opacity: linear or exponential decay
• Training: randomized per batch
"""
    ax_algo.text(0.05, 0.5, algo_text, fontsize=9, family='monospace',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.95),
                verticalalignment='center')

    fig.suptitle('Synthetic Echo-Trail Generation: Adding Temporal Context',
                fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig15_echo_trail_generation.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig15_echo_trail_generation.png")
    plt.close()

# Figure 16: Echo-Trail Length Comparison
def generate_echo_trail_variants():
    fig = plt.figure(figsize=(14, 8), dpi=150)
    fig.patch.set_facecolor('white')

    # Create base frames
    size = 160
    frames_base = []
    for idx in range(5):
        frame = np.random.normal(15, 3, (size, size))
        y, x = np.ogrid[:size, :size]
        center = size / 2
        radius = size / 2
        mask = (x - center)**2 + (y - center)**2 <= radius**2
        frame[~mask] = 0

        clutter = np.random.rand(size, size) < 0.05
        frame[clutter] = np.random.uniform(60, 150, np.sum(clutter))

        # Boat in different positions
        bx, by = 80 + idx*8, 80 - idx*4
        sz = 5
        yb, xb = np.ogrid[max(0, by-sz):min(size, by+sz), max(0, bx-sz):min(size, bx+sz)]
        boat_mask = (xb - bx)**2 + (yb - by)**2 <= sz**2
        frame[max(0, by-sz):min(size, by+sz), max(0, bx-sz):min(size, bx+sz)][boat_mask] = 245

        frames_base.append(np.clip(frame, 0, 255))

    # Trail lengths and opacity schedules
    trail_configs = [
        (1, [1.0], 'T=1\n(Single Frame)'),
        (4, [0.25, 0.5, 0.75, 1.0], 'T=4\n(Medium Trail)'),
        (8, np.linspace(0.1, 1.0, 8), 'T=8\n(Long Trail)'),
        (16, np.linspace(0.05, 1.0, 16), 'T=16\n(Very Long Trail)'),
    ]

    for config_idx, (trail_len, opacities, title) in enumerate(trail_configs):
        ax = plt.subplot(2, 4, config_idx + 1)

        # Create composite
        composite = np.zeros_like(frames_base[0], dtype=float)
        frames_to_use = frames_base[max(0, 5-trail_len):]
        for i, frame in enumerate(frames_to_use):
            opacity_idx = i if len(opacities) == len(frames_to_use) else min(i, len(opacities)-1)
            composite += opacities[opacity_idx] * frame

        composite = np.clip(composite / max(1, len(frames_to_use)), 0, 255)
        ax.imshow(composite, cmap='gray', origin='upper')
        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.axis('off')

        # Add info below
        ax.text(0.5, -0.15, f'Frames used: {len(frames_to_use)}\nGhosting: {"None" if trail_len == 1 else "Visible" if trail_len <= 4 else "Heavy"}',
               ha='center', transform=ax.transAxes, fontsize=8,
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

    # Analysis panel
    ax_analysis = plt.subplot(2, 4, (5, 8))
    ax_analysis.axis('off')
    analysis_text = """Trail Length Analysis

T=1 (Single Frame):
  • Baseline: no temporal context
  • Fastest inference
  • Misses motion cues

T=4 (Optimal):
  • Good motion perception
  • Moderate ghosting
  • Trade-off balanced

T=8 (Longer Context):
  • Enhanced motion
  • Visible ghosting
  • Slower processing

T=16 (Maximum):
  • Extensive history
  • Heavy ghosting/blur
  • Fast-moving objects distort
  • Risk of label-feature mismatch

Recommendation:
Use T ∈ {4, 8} for best
detection of dynamic boats
in cluttered scenes
"""
    ax_analysis.text(0.05, 0.5, analysis_text, fontsize=9, family='monospace',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.95),
                    verticalalignment='center')

    fig.suptitle('Echo-Trail Length Variants: T=1, T=4, T=8, T=16',
                fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig16_echo_trail_variants.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig16_echo_trail_variants.png")
    plt.close()

# Figure 17: Moving Boat with Velocity Vector
def generate_motion_visualization():
    fig = plt.figure(figsize=(14, 8), dpi=150)
    fig.patch.set_facecolor('white')

    # Create 4 frames with moving boat
    size = 160
    frames = []
    boat_trajectory = [(60, 100), (75, 95), (90, 90), (105, 85)]  # Diagonal motion

    for idx, (bx, by) in enumerate(boat_trajectory):
        frame = np.random.normal(15, 3, (size, size))
        y, x = np.ogrid[:size, :size]
        center = size / 2
        radius = size / 2
        mask = (x - center)**2 + (y - center)**2 <= radius**2
        frame[~mask] = 0

        clutter = np.random.rand(size, size) < 0.04
        frame[clutter] = np.random.uniform(60, 140, np.sum(clutter))

        # Boat
        sz = 4
        yb, xb = np.ogrid[max(0, by-sz):min(size, by+sz), max(0, bx-sz):min(size, bx+sz)]
        boat_mask = (xb - bx)**2 + (yb - by)**2 <= sz**2
        frame[max(0, by-sz):min(size, by+sz), max(0, bx-sz):min(size, bx+sz)][boat_mask] = 240

        frames.append(np.clip(frame, 0, 255))

    # Left: Individual frames with trajectory
    for i in range(4):
        ax = plt.subplot(2, 4, i+1)
        ax.imshow(frames[i], cmap='gray', origin='upper')

        # Mark boat position
        bx, by = boat_trajectory[i]
        ax.plot(bx, by, 'r+', markersize=15, markeredgewidth=2)

        # Draw entire trajectory up to current frame
        traj_x = [boat_trajectory[j][0] for j in range(i+1)]
        traj_y = [boat_trajectory[j][1] for j in range(i+1)]
        ax.plot(traj_x, traj_y, 'r--', alpha=0.5, linewidth=1.5)

        ax.set_title(f'Frame {i} (t={i})', fontsize=10, fontweight='bold')
        ax.axis('off')

    # Right: Echo trail with velocity vector
    ax_echo = plt.subplot(2, 4, (5, 6))

    # Create echo trail
    composite = np.zeros_like(frames[0], dtype=float)
    opacities = [0.15, 0.35, 0.65, 1.0]
    for i, frame in enumerate(frames):
        composite += opacities[i] * frame
    composite = np.clip(composite / 2.0, 0, 255)

    ax_echo.imshow(composite, cmap='gray', origin='upper')

    # Overlay trajectory and velocity
    traj_x = [pos[0] for pos in boat_trajectory]
    traj_y = [pos[1] for pos in boat_trajectory]
    ax_echo.plot(traj_x, traj_y, 'lime', linewidth=2, marker='o', markersize=8, alpha=0.8)

    # Velocity vector
    vx = boat_trajectory[-1][0] - boat_trajectory[-2][0]
    vy = boat_trajectory[-1][1] - boat_trajectory[-2][1]
    ax_echo.arrow(boat_trajectory[-1][0], boat_trajectory[-1][1], vx*3, vy*3,
                 head_width=3, head_length=2, fc='yellow', ec='yellow', linewidth=2)

    ax_echo.set_title('Echo Trail with Motion\n(Velocity Vector)', fontsize=11, fontweight='bold', color='darkgreen')
    ax_echo.axis('off')
    ax_echo.text(0.5, -0.1, 'Yellow arrow: estimated velocity', ha='center', transform=ax_echo.transAxes,
                fontsize=9, bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # Analysis
    ax_analysis = plt.subplot(2, 4, (7, 8))
    ax_analysis.axis('off')
    analysis_text = """Motion Detection Benefits

Echo Trail Advantages:
✓ Makes boat trajectory visible
✓ Distinguishes dynamic from static
✓ Provides temporal context
✓ No explicit tracking needed

Velocity Estimation:
• Position changes per sweep
• ~40–80 Hz effective rate
• Enables motion-based filtering

Model Learning:
• Learns motion patterns
• Distinguishes wakes/clutter
• Improves in crowded scenes

Limitations:
✗ Only past motion (T→t)
✗ Doesn't predict future
✗ Fast maneuvers cause blur
✗ Label-frame timestamp must align
"""
    ax_analysis.text(0.05, 0.5, analysis_text, fontsize=9, family='monospace',
                    bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.95),
                    verticalalignment='center')

    fig.suptitle('Motion Visualization: Moving Boat Trajectory with Echo Trail and Velocity Vector',
                fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig17_motion_visualization.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig17_motion_visualization.png")
    plt.close()

if __name__ == '__main__':
    print("Generating acquisition & preprocessing figures 10-17...")
    generate_furuno_hardware_detailed()
    generate_range_azimuth_diagram()
    generate_quantization_comparison()
    generate_conversion_pipeline()
    generate_range_variability()
    generate_echo_trail_visualization()
    generate_echo_trail_variants()
    generate_motion_visualization()
    print("\nAll acquisition figures generated successfully!")
