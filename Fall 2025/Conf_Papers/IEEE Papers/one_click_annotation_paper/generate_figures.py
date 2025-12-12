#!/usr/bin/env python3
"""Generate placeholder figures for the marine radar paper."""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import Circle, Rectangle, Polygon, Wedge, FancyBboxPatch
import matplotlib.patches as mpatches
from PIL import Image, ImageDraw, ImageFont
import io

output_dir = "python_figures"

# Figure 1: Furuno NXT Radar Hardware
def generate_radar_hardware():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Vessel outline
    vessel = Polygon([(1, 2), (1, 3.5), (4.5, 4), (4.5, 2.5), (4, 2)],
                     closed=True, fill=True, facecolor='#b0b0b0', edgecolor='black', linewidth=2)
    ax.add_patch(vessel)

    # Cabin
    cabin = Rectangle((1.5, 3), 1.5, 1, fill=True, facecolor='#d0d0d0', edgecolor='black', linewidth=1.5)
    ax.add_patch(cabin)

    # Mast
    ax.plot([3, 3], [4, 6.5], 'k-', linewidth=3)

    # Radar antenna (circular dome)
    antenna = Circle((3, 6.5), 0.6, fill=True, facecolor='#ff9999', edgecolor='black', linewidth=2)
    ax.add_patch(antenna)

    # Antenna mounting bracket
    ax.plot([3, 3], [4.8, 5.9], 'k-', linewidth=2)
    bracket = Rectangle((2.85, 4.8), 0.3, 0.3, fill=False, edgecolor='black', linewidth=1)
    ax.add_patch(bracket)

    # Radar beam visualization
    for angle in np.linspace(-60, 60, 5):
        rad = np.radians(angle)
        x_end = 3 + 2.5 * np.sin(rad)
        y_end = 6.5 - 2.5 * np.cos(rad)
        ax.plot([3, x_end], [6.5, y_end], 'r--', alpha=0.3, linewidth=1)

    # Control unit below deck
    control = FancyBboxPatch((1.2, 0.3), 2, 1.2, boxstyle="round,pad=0.1",
                             fill=True, facecolor='#cccccc', edgecolor='black', linewidth=1.5)
    ax.add_patch(control)
    ax.text(2.2, 0.9, 'Control\nUnit', ha='center', va='center', fontsize=10, fontweight='bold')

    # Cable connections
    ax.plot([2.2, 2.2], [1.5, 2.5], 'k-', linewidth=2)
    ax.plot([2.8, 2.8], [1.5, 2.5], 'k-', linewidth=2)

    # Water
    water = Rectangle((0, 0), 10, 1.5, fill=True, facecolor='#4a90e2', alpha=0.3)
    ax.add_patch(water)

    # Labels
    ax.text(3, 7.3, 'Furuno NXT\nRadar Antenna', ha='center', fontsize=11, fontweight='bold')
    ax.text(5.5, 3, 'Vessel', ha='left', fontsize=10, style='italic')
    ax.text(2.2, -0.5, '(Mounted on research vessel or shore)', ha='center', fontsize=9, style='italic')

    ax.set_aspect('equal')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig01_radar_hardware.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig01_radar_hardware.png")
    plt.close()

# Figure 2: Modality Comparison
def generate_modality_comparison():
    fig = plt.figure(figsize=(14, 5), dpi=150)
    fig.patch.set_facecolor('white')

    # Create 3 subplots for radar, camera, lidar
    modalities = [
        ('Marine Radar\n(Night, Rain, Fog)', 'radar'),
        ('Camera\n(Clear Daylight Only)', 'camera'),
        ('LiDAR\n(Clear Line-of-Sight)', 'lidar')
    ]

    for idx, (title, modality) in enumerate(modalities):
        ax = fig.add_subplot(1, 3, idx + 1)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.set_aspect('equal')

        if modality == 'radar':
            # Radar-like polar representation
            ax.set_facecolor('#1a1a2e')
            theta = np.linspace(0, 2*np.pi, 100)
            # Concentric circles (range rings)
            for r in [20, 40, 60, 80]:
                x = r * np.cos(theta)
                y = r * np.sin(theta)
                ax.plot(50 + x/2, 50 + y/2, 'g-', alpha=0.3, linewidth=0.5)

            # Boat echoes
            boat_positions = [(40, 55), (65, 35), (55, 70)]
            for bx, by in boat_positions:
                circle = Circle((bx, by), 3, color='lime', alpha=0.8)
                ax.add_patch(circle)

            # Clutter
            for _ in range(15):
                rx, ry = np.random.rand()*100, np.random.rand()*100
                ax.plot(rx, ry, 'g.', markersize=2, alpha=0.5)

            ax.text(50, 5, '✓ Works in rain, fog, night', ha='center', fontsize=9,
                   color='lime', fontweight='bold', bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))

        elif modality == 'camera':
            # Camera-like RGB image
            ax.set_facecolor('white')
            # Blue water background
            water = Rectangle((0, 0), 100, 100, fill=True, facecolor='#87ceeb')
            ax.add_patch(water)

            # Boats (simple rectangles)
            boats = [
                Rectangle((30, 50), 15, 8, fill=True, facecolor='#8b0000', edgecolor='black'),
                Rectangle((60, 30), 12, 6, fill=True, facecolor='#ffd700', edgecolor='black'),
            ]
            for boat in boats:
                ax.add_patch(boat)

            # Sun
            sun = Circle((85, 80), 5, fill=True, facecolor='yellow')
            ax.add_patch(sun)

            ax.text(50, 5, '✗ Fails in low light / fog', ha='center', fontsize=9,
                   color='red', fontweight='bold', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

        elif modality == 'lidar':
            # Point cloud-like representation
            ax.set_facecolor('#f0f0f0')
            # Random points
            cloud_x = np.random.normal(50, 15, 150)
            cloud_y = np.random.normal(50, 15, 150)
            ax.scatter(cloud_x, cloud_y, c='red', s=20, alpha=0.6)

            # Boat points
            boat_x = np.random.normal(40, 5, 30)
            boat_y = np.random.normal(55, 5, 30)
            ax.scatter(boat_x, boat_y, c='darkred', s=30, alpha=1, marker='s')

            ax.text(50, 5, '✗ Limited by weather/occlusion', ha='center', fontsize=9,
                   color='red', fontweight='bold', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

        ax.set_title(title, fontsize=11, fontweight='bold', pad=10)
        ax.axis('off')

    plt.suptitle('Sensing Modalities for Maritime Object Detection', fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig02_modality_comparison.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig02_modality_comparison.png")
    plt.close()

# Figure 3: Geographic Collection Map
def generate_collection_map():
    fig, ax = plt.subplots(figsize=(12, 10), dpi=150)
    fig.patch.set_facecolor('white')

    # Simplified state outlines
    ax.set_xlim(-83, -77)
    ax.set_ylim(32, 38)
    ax.set_aspect('equal')

    # Water background
    ax.set_facecolor('#c7e9ff')

    # Rough South Carolina and Virginia coastline
    sc_coast = [(-82.5, 33.5), (-82, 33.2), (-81.5, 33), (-81, 33.1), (-80.5, 33.5), (-80, 33.8)]
    va_coast = [(-77.5, 37.5), (-77, 37.3), (-76.5, 37.1), (-76, 37.2), (-75.5, 37.4)]

    # Land regions (very rough)
    land1 = Rectangle((-83.5, 32), 3.5, 6, fill=True, facecolor='#d4d4a8', alpha=0.5, edgecolor='gray', linewidth=1)
    ax.add_patch(land1)

    # Collection sites with coordinates (approximate)
    sites = [
        (-81.1, 34.8, 'Lake Murray', 'red'),
        (-82.3, 34.3, 'Lake Greenwood', 'red'),
        (-82.5, 34.5, 'Lake Monticello', 'red'),
        (-76.3, 36.8, 'Portsmouth\n(Elizabeth R.)', 'orange'),
        (-80.0, 32.8, 'Charleston Harbor\n+ Folly Beach', 'green'),
    ]

    for lon, lat, name, color in sites:
        # Plot marker
        ax.plot(lon, lat, 'o', markersize=14, color=color, markeredgecolor='black', markeredgewidth=2, zorder=3)

        # Add label with slight offset
        offset_x = -0.5 if lon < -80 else 0.5
        offset_y = 0.3 if lat > 34 else -0.3
        ax.text(lon + offset_x, lat + offset_y, name, fontsize=9, fontweight='bold',
               ha='center', bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9, edgecolor=color, linewidth=1.5))

    # Add legend
    legend_elements = [
        mpatches.Patch(color='red', label='Lakes (SC)', alpha=0.7),
        mpatches.Patch(color='orange', label='Rivers (VA)', alpha=0.7),
        mpatches.Patch(color='green', label='Coastal (SC)', alpha=0.7),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10, title='Collection Sites', title_fontsize=11)

    # Geographic labels
    ax.text(-82, 37.5, 'Virginia', fontsize=12, style='italic', color='gray', alpha=0.7)
    ax.text(-81.5, 33.2, 'South Carolina', fontsize=12, style='italic', color='gray', alpha=0.7)

    # Scale bar
    ax.plot([-82.5, -82], [32.3, 32.3], 'k-', linewidth=2)
    ax.text(-82.25, 32.15, '~50 km', ha='center', fontsize=9)

    # Grid
    ax.grid(True, alpha=0.2, linestyle='--')
    ax.set_xlabel('Longitude (°W)', fontsize=11)
    ax.set_ylabel('Latitude (°N)', fontsize=11)
    ax.set_title('Marine Radar Data Collection Sites\n(2025)', fontsize=13, fontweight='bold', pad=15)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig03_collection_map.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig03_collection_map.png")
    plt.close()

if __name__ == '__main__':
    print("Generating placeholder figures...")
    generate_radar_hardware()
    generate_modality_comparison()
    generate_collection_map()
    print("\nAll figures generated successfully!")
