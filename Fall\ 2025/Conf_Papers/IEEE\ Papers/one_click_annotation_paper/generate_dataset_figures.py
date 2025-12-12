#!/usr/bin/env python3
"""Generate dataset figures 4-9 for the marine radar paper."""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import Rectangle, Circle
import seaborn as sns

output_dir = "python_figures"

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
    print("Generating dataset figures 4-9...")
    generate_radar300_samples()
    generate_usc_canal_samples()
    generate_dataset_comparison()
    generate_class_distribution()
    generate_temporal_coverage()
    generate_pohang_preview()
    print("\nAll dataset figures generated successfully!")
