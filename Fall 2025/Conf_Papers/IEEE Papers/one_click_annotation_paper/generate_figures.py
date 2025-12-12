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

# Figure 4: RADAR300 Samples
def generate_radar300_samples():
    fig, axes = plt.subplots(2, 3, figsize=(14, 9), dpi=150)
    fig.patch.set_facecolor('white')

    for ax in axes.flat:
        # Create synthetic PPI radar image
        size = 200
        img = np.random.normal(5, 2, (size, size))
        img = np.clip(img, 0, 255)

        # Add realistic circular mask (radar sweep area)
        y, x = np.ogrid[:size, :size]
        center = size / 2
        radius = size / 2
        mask = (x - center)**2 + (y - center)**2 <= radius**2
        img[~mask] = 0

        # Add some clutter (random noise points)
        noise_points = np.random.rand(size, size) < 0.03
        img[noise_points] = np.random.uniform(100, 200, np.sum(noise_points))

        # Add boat echoes (bright circular spots)
        n_boats = np.random.randint(1, 4)
        boats = []
        for _ in range(n_boats):
            # Random position within circle
            angle = np.random.uniform(0, 2*np.pi)
            r = np.random.uniform(20, radius - 20)
            bx = int(center + r * np.cos(angle))
            by = int(center + r * np.sin(angle))

            # Draw boat echo
            size_boat = np.random.randint(3, 8)
            yb, xb = np.ogrid[max(0, by-size_boat):min(size, by+size_boat),
                              max(0, bx-size_boat):min(size, bx+size_boat)]
            dist = (xb - bx)**2 + (yb - by)**2
            boat_mask = dist <= size_boat**2
            img[max(0, by-size_boat):min(size, by+size_boat),
                max(0, bx-size_boat):min(size, bx+size_boat)][boat_mask] = 255

            boats.append((bx, by, size_boat))

        # Display
        ax.imshow(img, cmap='gray', origin='upper')

        # Draw bounding boxes around detected boats
        for bx, by, sz in boats:
            rect = Rectangle((bx - 1.5*sz, by - 1.5*sz), 3*sz, 3*sz,
                           linewidth=2, edgecolor='lime', facecolor='none')
            ax.add_patch(rect)

        ax.set_xlim(0, size)
        ax.set_ylim(0, size)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(f'Frame {np.random.randint(100, 3100)}', fontsize=10, fontweight='bold')

    fig.suptitle('RADAR300: Sample Detections (Public Dataset)\n3000 frames with boat annotations',
                fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig04_radar300_samples.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig04_radar300_samples.png")
    plt.close()

# Figure 5: USC Canal Dataset Examples
def generate_usc_canal_samples():
    fig, axes = plt.subplots(2, 3, figsize=(14, 9), dpi=150)
    fig.patch.set_facecolor('white')

    for idx, ax in enumerate(axes.flat):
        # Create synthetic PPI radar image
        size = 200
        img = np.random.normal(8, 3, (size, size))
        img = np.clip(img, 0, 255)

        # Add circular mask
        y, x = np.ogrid[:size, :size]
        center = size / 2
        radius = size / 2
        mask = (x - center)**2 + (y - center)**2 <= radius**2
        img[~mask] = 0

        # Add more clutter (inland environment)
        clutter = np.random.rand(size, size) < 0.08
        img[clutter] = np.random.uniform(50, 180, np.sum(clutter))

        # Add dynamic and static boats
        n_dynamic = np.random.randint(0, 3)
        n_static = np.random.randint(0, 2)

        for d in range(n_dynamic):
            angle = np.random.uniform(0, 2*np.pi)
            r = np.random.uniform(30, radius - 20)
            bx = int(center + r * np.cos(angle))
            by = int(center + r * np.sin(angle))
            sz = np.random.randint(3, 7)
            yb, xb = np.ogrid[max(0, by-sz):min(size, by+sz),
                              max(0, bx-sz):min(size, bx+sz)]
            boat_mask = (xb - bx)**2 + (yb - by)**2 <= sz**2
            img[max(0, by-sz):min(size, by+sz),
                max(0, bx-sz):min(size, bx+sz)][boat_mask] = 240

            rect = Rectangle((bx - 1.8*sz, by - 1.8*sz), 3.6*sz, 3.6*sz,
                           linewidth=2.5, edgecolor='lime', facecolor='none')
            ax.add_patch(rect)
            ax.text(bx - 1.5*sz, by - 2.2*sz, 'D', fontsize=10, color='lime', fontweight='bold')

        for s in range(n_static):
            angle = np.random.uniform(0, 2*np.pi)
            r = np.random.uniform(10, 40)  # Closer to center (dock/pier area)
            bx = int(center + r * np.cos(angle))
            by = int(center + r * np.sin(angle))
            sz = np.random.randint(5, 10)
            yb, xb = np.ogrid[max(0, by-sz):min(size, by+sz),
                              max(0, bx-sz):min(size, bx+sz)]
            boat_mask = (xb - bx)**2 + (yb - by)**2 <= sz**2
            img[max(0, by-sz):min(size, by+sz),
                max(0, bx-sz):min(size, bx+sz)][boat_mask] = 200

            rect = Rectangle((bx - 1.8*sz, by - 1.8*sz), 3.6*sz, 3.6*sz,
                           linewidth=2.5, edgecolor='orange', facecolor='none')
            ax.add_patch(rect)
            ax.text(bx - 1.5*sz, by - 2.2*sz, 'S', fontsize=10, color='orange', fontweight='bold')

        ax.imshow(img, cmap='gray', origin='upper')
        ax.set_xlim(0, size)
        ax.set_ylim(0, size)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(f'Frame {96 - idx}', fontsize=10, fontweight='bold')

    fig.suptitle('USC Canal Dataset: Labeled Detections\n96 frames with dynamic (green) and static (orange) annotations',
                fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig05_usc_canal_samples.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig05_usc_canal_samples.png")
    plt.close()

# Figure 6: Dataset Comparison Grid
def generate_dataset_comparison():
    fig, axes = plt.subplots(3, 2, figsize=(12, 11), dpi=150)
    fig.patch.set_facecolor('white')

    datasets = [
        ("RADAR300\n(Public Source Domain)", True),
        ("USC Canal\n(Target Domain)", False),
    ]

    for col, (title, is_radar300) in enumerate(datasets):
        for row in range(3):
            ax = axes[row, col]

            size = 200
            img = np.random.normal(5 if is_radar300 else 8, 2 if is_radar300 else 3, (size, size))
            img = np.clip(img, 0, 255)

            y, x = np.ogrid[:size, :size]
            center = size / 2
            radius = size / 2
            mask = (x - center)**2 + (y - center)**2 <= radius**2
            img[~mask] = 0

            # RADAR300: cleaner, fewer boats, less clutter
            if is_radar300:
                clutter = np.random.rand(size, size) < 0.02
                n_boats = np.random.randint(1, 2)
            else:
                clutter = np.random.rand(size, size) < 0.12  # More clutter (inland)
                n_boats = np.random.randint(0, 3)

            img[clutter] = np.random.uniform(80, 200, np.sum(clutter))

            for _ in range(n_boats):
                angle = np.random.uniform(0, 2*np.pi)
                r = np.random.uniform(30, radius - 20)
                bx = int(center + r * np.cos(angle))
                by = int(center + r * np.sin(angle))
                sz = np.random.randint(2, 6)
                yb, xb = np.ogrid[max(0, by-sz):min(size, by+sz),
                                  max(0, bx-sz):min(size, bx+sz)]
                boat_mask = (xb - bx)**2 + (yb - by)**2 <= sz**2
                img[max(0, by-sz):min(size, by+sz),
                    max(0, bx-sz):min(size, bx+sz)][boat_mask] = 250

            ax.imshow(img, cmap='gray', origin='upper')
            ax.set_xlim(0, size)
            ax.set_ylim(0, size)
            ax.set_aspect('equal')
            ax.axis('off')
            if row == 0:
                ax.set_title(title, fontsize=11, fontweight='bold', pad=10)

    fig.suptitle('Dataset Comparison: Distribution Shift\nRADAR300 (left) vs. USC Canal (right)',
                fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig06_dataset_comparison.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig06_dataset_comparison.png")
    plt.close()

# Figure 7: Class Distribution Histograms
def generate_class_distribution():
    fig = plt.figure(figsize=(14, 10), dpi=150)
    fig.patch.set_facecolor('white')

    # Subplot 1: Objects per frame
    ax1 = plt.subplot(2, 3, 1)
    objects_per_frame = np.random.poisson(6.6, 96)  # 637 objects / 96 frames ≈ 6.6
    ax1.hist(objects_per_frame, bins=range(0, max(objects_per_frame)+2),
            color='steelblue', edgecolor='black', alpha=0.7)
    ax1.set_xlabel('Objects per Frame', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=11, fontweight='bold')
    ax1.set_title('Objects per Frame Distribution', fontsize=11, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)

    # Subplot 2: Bounding box area distribution
    ax2 = plt.subplot(2, 3, 2)
    bbox_areas = np.concatenate([
        np.random.lognormal(6, 1, 400),  # Dynamic boats
        np.random.lognormal(6.5, 0.9, 237)  # Static objects (larger)
    ])
    bbox_areas = np.clip(bbox_areas, 10, 5000)
    ax2.hist(bbox_areas, bins=30, color='coral', edgecolor='black', alpha=0.7)
    ax2.set_xlabel('Bounding Box Area (pixels²)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Frequency', fontsize=11, fontweight='bold')
    ax2.set_title('Object Size Distribution', fontsize=11, fontweight='bold')
    ax2.set_xscale('log')
    ax2.grid(axis='y', alpha=0.3)

    # Subplot 3: Class breakdown by split
    ax3 = plt.subplot(2, 3, 3)
    splits = ['Train\n(~58 frames)', 'Val\n(~19 frames)', 'Test\n(~19 frames)']
    dynamic_counts = [380, 130, 127]
    static_counts = [150, 60, 47]
    x = np.arange(len(splits))
    width = 0.35
    bars1 = ax3.bar(x - width/2, dynamic_counts, width, label='Dynamic', color='lime', edgecolor='black')
    bars2 = ax3.bar(x + width/2, static_counts, width, label='Static', color='orange', edgecolor='black')
    ax3.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax3.set_title('Class Distribution by Split', fontsize=11, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(splits)
    ax3.legend(fontsize=10)
    ax3.grid(axis='y', alpha=0.3)

    # Subplot 4: Dynamic vs Static pie
    ax4 = plt.subplot(2, 3, 4)
    ax4.pie([637*0.6, 237], labels=['Dynamic Boats\n(~60%)', 'Static Objects\n(~37%)'],
           colors=['lime', 'orange'], autopct='%1.1f%%', startangle=90,
           textprops={'fontsize': 10, 'weight': 'bold'})
    ax4.set_title('Class Imbalance', fontsize=11, fontweight='bold')

    # Subplot 5: Object size by class
    ax5 = plt.subplot(2, 3, 5)
    dyn_sizes = np.random.lognormal(6, 1, 400)
    stat_sizes = np.random.lognormal(6.5, 0.9, 237)
    ax5.boxplot([dyn_sizes, stat_sizes], labels=['Dynamic', 'Static'], patch_artist=True,
               boxprops=dict(facecolor='lightblue'), medianprops=dict(color='red', linewidth=2))
    ax5.set_ylabel('Bounding Box Area (pixels²)', fontsize=11, fontweight='bold')
    ax5.set_title('Size Comparison by Class', fontsize=11, fontweight='bold')
    ax5.set_yscale('log')
    ax5.grid(axis='y', alpha=0.3)

    # Subplot 6: Frame statistics
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')
    stats_text = f"""Dataset Statistics

Total Frames (labeled): 96
Total Objects: 637

Dynamic Boats: ~382 (60%)
Static Objects: ~237 (37%)
Unknown: ~18 (3%)

Avg Objects/Frame: 6.6
Max Objects/Frame: {int(np.max(objects_per_frame))}
Min Objects/Frame: {int(np.min(objects_per_frame))}

Unlabeled Frames: 196,000
"""
    ax6.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
            verticalalignment='center')

    fig.suptitle('USC Canal Dataset: Class Distribution Analysis\n96 labeled frames with 637 annotated objects',
                fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig07_class_distribution.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig07_class_distribution.png")
    plt.close()

# Figure 8: Temporal Coverage Heatmap
def generate_temporal_coverage():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
    fig.patch.set_facecolor('white')

    # Create temporal heatmap: Time of day (rows) vs. Date (columns)
    hours = np.arange(24)
    days = np.arange(214)  # May 1 to Dec 31, 2025 (roughly)

    # Generate realistic temporal distribution
    heatmap_data = np.zeros((24, 214))
    for hour in hours:
        for day in days:
            # More collection during daytime and specific days
            base = 500 if 6 <= hour <= 18 else 200
            weekly_pattern = 800 if day % 7 in [0, 6] else base  # More on weekends
            random_var = np.random.normal(0, 100)
            heatmap_data[hour, day] = max(0, weekly_pattern + random_var)

    # Plot heatmap
    im = ax.imshow(heatmap_data, cmap='YlOrRd', aspect='auto', interpolation='bilinear')

    # Set tick labels
    hour_labels = [f'{h:02d}:00' for h in hours]
    day_labels_dates = ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    ax.set_yticks(hours)
    ax.set_yticklabels(hour_labels, fontsize=9)
    ax.set_xlabel('Date (2025)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Time of Day (UTC)', fontsize=12, fontweight='bold')

    # Add month boundaries
    month_boundaries = [0, 31, 61, 92, 122, 153, 183, 214]
    for boundary in month_boundaries[1:]:
        ax.axvline(boundary, color='white', linewidth=2, alpha=0.5)

    ax.set_xticks(month_boundaries)
    ax.set_xticklabels(day_labels_dates, fontsize=10)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Frames Collected', fontsize=11, fontweight='bold')

    ax.set_title('Temporal Coverage: 196,000 Unlabeled Frames\nCollection intensity by time of day and date',
                fontsize=13, fontweight='bold', pad=15)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig08_temporal_coverage.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig08_temporal_coverage.png")
    plt.close()

# Figure 9: Pohang Canal Preview
def generate_pohang_preview():
    fig, axes = plt.subplots(1, 3, figsize=(14, 5), dpi=150)
    fig.patch.set_facecolor('white')

    for idx, ax in enumerate(axes):
        # Create synthetic Pohang radar image (different hardware characteristics)
        size = 200
        # Different quantization/characteristics than Furuno
        img = np.random.normal(10, 4, (size, size))
        img = np.clip(img, 0, 255)

        y, x = np.ogrid[:size, :size]
        center = size / 2
        radius = size / 2
        mask = (x - center)**2 + (y - center)**2 <= radius**2
        img[~mask] = 0

        # Korean canal: different clutter pattern
        clutter = np.random.rand(size, size) < 0.10
        img[clutter] = np.random.uniform(60, 200, np.sum(clutter))

        # Boats in Pohang (likely more frequent in canal)
        n_boats = np.random.randint(2, 5)
        for _ in range(n_boats):
            angle = np.random.uniform(0, 2*np.pi)
            r = np.random.uniform(25, radius - 15)
            bx = int(center + r * np.cos(angle))
            by = int(center + r * np.sin(angle))
            sz = np.random.randint(4, 8)
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
        ax.set_title(f'Pohang Frame {1000 + idx*100}', fontsize=11, fontweight='bold')

    fig.suptitle('Pohang Canal Dataset Preview\nDifferent hardware, environment, and traffic patterns (used for qualitative generalization)',
                fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig09_pohang_preview.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig09_pohang_preview.png")
    plt.close()

if __name__ == '__main__':
    print("Generating all figures...")
    generate_radar_hardware()
    generate_modality_comparison()
    generate_collection_map()
    generate_radar300_samples()
    generate_usc_canal_samples()
    generate_dataset_comparison()
    generate_class_distribution()
    generate_temporal_coverage()
    generate_pohang_preview()
    print("\nAll figures generated successfully!")
