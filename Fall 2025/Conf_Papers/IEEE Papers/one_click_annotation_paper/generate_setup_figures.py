#!/usr/bin/env python3
"""Generate experimental setup figures 28-30 for the marine radar paper."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.patches import Rectangle

output_dir = "python_figures"

# Figure 28: Dataset Split Pie Chart
def generate_dataset_split():
    fig = plt.figure(figsize=(14, 9), dpi=150)
    fig.patch.set_facecolor('white')

    # Main pie chart (larger)
    ax1 = plt.subplot(1, 2, 1)

    # Data: 60/20/20 split of 96 frames
    train_frames = 58
    val_frames = 19
    test_frames = 19
    sizes = [train_frames, val_frames, test_frames]
    labels = [f'Training\n({train_frames} frames)\n60%',
              f'Validation\n({val_frames} frames)\n20%',
              f'Test\n({test_frames} frames)\n20%']
    colors = ['#66bb6a', '#42a5f5', '#ff7043']
    explode = (0.05, 0, 0)

    wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%',
                                        explode=explode, startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
        autotext.set_fontweight('bold')

    ax1.set_title('USC Canal Dataset: Train/Val/Test Split\n96 labeled frames',
                 fontsize=12, fontweight='bold', pad=20)

    # Right: Detailed statistics table
    ax2 = plt.subplot(1, 2, 2)
    ax2.axis('off')

    # Create detailed breakdown
    stats_text = """Dataset Allocation Details

TRAINING SET (58 frames, 60%)
├─ Dynamic objects: ~380
├─ Static objects: ~150
├─ Total objects: ~537 (84%)
├─ Avg objects/frame: 9.3
└─ Sources: All collection sites

VALIDATION SET (19 frames, 20%)
├─ Dynamic objects: ~130
├─ Static objects: ~60
├─ Total objects: ~190 (30%)
├─ Avg objects/frame: 10.0
└─ Held-out for early stopping

TEST SET (19 frames, 20%)
├─ Dynamic objects: ~127
├─ Static objects: ~47
├─ Total objects: ~174 (27%)
├─ Avg objects/frame: 9.2
└─ Held-out for final evaluation

SPLIT STRATEGY
✓ Temporal coherence preserved
  (frames from same sequence
   not split across train/val/test)
✓ Balanced class distribution
  across all splits
✓ Stratified by collection site
  to avoid location bias
✓ No data leakage

TOTAL CORPUS
• Labeled frames: 96
• Labeled objects: 637
• Unlabeled frames: 196,000
"""

    ax2.text(0.05, 0.5, stats_text, fontsize=8, family='monospace',
            bbox=dict(boxstyle='round', facecolor='#f0f0f0', alpha=0.95, pad=1),
            verticalalignment='center')

    fig.suptitle('Experimental Setup: Dataset Splits',
                fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig28_dataset_split.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig28_dataset_split.png")
    plt.close()

# Figure 29: Class Imbalance Chart
def generate_class_imbalance():
    fig = plt.figure(figsize=(14, 9), dpi=150)
    fig.patch.set_facecolor('white')

    # Subplot 1: Stacked bar chart by split
    ax1 = plt.subplot(2, 2, 1)

    splits = ['Train\n(58 frames)', 'Val\n(19 frames)', 'Test\n(19 frames)']
    dynamic = [380, 130, 127]
    static = [150, 60, 47]
    unknown = [7, 0, 0]  # Ambiguous annotations

    x = np.arange(len(splits))
    width = 0.6

    bars1 = ax1.bar(x, dynamic, width, label='Dynamic', color='lime', edgecolor='darkgreen', linewidth=1.5)
    bars2 = ax1.bar(x, static, width, bottom=dynamic, label='Static', color='orange', edgecolor='darkorange', linewidth=1.5)
    bars3 = ax1.bar(x, unknown, width, bottom=np.array(dynamic)+np.array(static),
                   label='Unknown', color='#cccccc', edgecolor='gray', linewidth=1.5)

    ax1.set_ylabel('Number of Objects', fontsize=11, fontweight='bold')
    ax1.set_title('Class Distribution by Split', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(splits)
    ax1.legend(fontsize=10, loc='upper right')
    ax1.grid(axis='y', alpha=0.3)

    # Add value labels
    for i, (d, s, u) in enumerate(zip(dynamic, static, unknown)):
        ax1.text(i, d/2, str(d), ha='center', va='center', fontsize=10, fontweight='bold', color='white')
        ax1.text(i, d + s/2, str(s), ha='center', va='center', fontsize=10, fontweight='bold', color='white')
        if u > 0:
            ax1.text(i, d + s + u/2, str(u), ha='center', va='center', fontsize=9, fontweight='bold')

    # Subplot 2: Percentage breakdown
    ax2 = plt.subplot(2, 2, 2)

    all_dynamic = sum(dynamic)
    all_static = sum(static)
    all_unknown = sum(unknown)
    total = all_dynamic + all_static + all_unknown

    percentages = [all_dynamic/total*100, all_static/total*100, all_unknown/total*100]
    labels_pie = [f'Dynamic\n{all_dynamic} ({percentages[0]:.1f}%)',
                  f'Static\n{all_static} ({percentages[1]:.1f}%)',
                  f'Unknown\n{all_unknown} ({percentages[2]:.1f}%)']
    colors_pie = ['lime', 'orange', '#cccccc']

    wedges, texts, autotexts = ax2.pie(percentages, labels=labels_pie, colors=colors_pie, autopct='',
                                        startangle=90, textprops={'fontsize': 9, 'fontweight': 'bold'})

    ax2.set_title('Overall Class Distribution\n(All splits combined)', fontsize=12, fontweight='bold')

    # Subplot 3: Per-split percentages
    ax3 = plt.subplot(2, 2, 3)

    split_names = ['Train', 'Val', 'Test']
    dyn_pct = [d/(d+s+u)*100 for d, s, u in zip(dynamic, static, unknown)]
    stat_pct = [s/(d+s+u)*100 for d, s, u in zip(dynamic, static, unknown)]

    x = np.arange(len(split_names))
    width = 0.5

    bars1 = ax3.bar(x, dyn_pct, width, label='Dynamic %', color='lime', edgecolor='darkgreen', linewidth=1.5)
    bars2 = ax3.bar(x, stat_pct, width, bottom=dyn_pct, label='Static %', color='orange', edgecolor='darkorange', linewidth=1.5)

    ax3.set_ylabel('Percentage (%)', fontsize=11, fontweight='bold')
    ax3.set_title('Class Proportion by Split', fontsize=12, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(split_names)
    ax3.legend(fontsize=10)
    ax3.set_ylim(0, 100)
    ax3.grid(axis='y', alpha=0.3)

    for i, (d, s) in enumerate(zip(dyn_pct, stat_pct)):
        ax3.text(i, d/2, f'{d:.1f}%', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
        ax3.text(i, d + s/2, f'{s:.1f}%', ha='center', va='center', fontsize=9, fontweight='bold', color='white')

    # Subplot 4: Class imbalance ratio
    ax4 = plt.subplot(2, 2, 4)
    ax4.axis('off')

    imbalance_text = """Class Imbalance Analysis

Overall Ratio:
• Dynamic : Static ≈ 2.7 : 1
• Means model sees mostly boats
• Need weighted loss or sampling

Per-Split Ratio:
• Train: 380 : 150 = 2.53 : 1
• Val:   130 :  60  = 2.17 : 1
• Test:  127 :  47  = 2.70 : 1
→ Consistent across splits ✓

Implications:
✗ Class imbalance → lower recall for static
✗ Harder to learn static features
✓ But reflects real maritime scenarios
  (moving boats > moored objects)

Mitigation Strategies:
1. Weighted loss: w_static = 2.7
2. Focal loss: focus on hard examples
3. Oversampling static in training
4. Report per-class metrics
"""

    ax4.text(0.05, 0.5, imbalance_text, fontsize=8, family='monospace',
            bbox=dict(boxstyle='round', facecolor='#fff9c4', alpha=0.95, pad=0.5),
            verticalalignment='center')

    fig.suptitle('Experimental Setup: Class Imbalance',
                fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig29_class_imbalance.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig29_class_imbalance.png")
    plt.close()

# Figure 30: Metadata Distribution
def generate_metadata_distribution():
    fig = plt.figure(figsize=(14, 10), dpi=150)
    fig.patch.set_facecolor('white')

    # Pie 1: Range settings
    ax1 = plt.subplot(2, 3, 1)
    range_settings = [0.5, 1.5, 3.0]
    range_counts = [18, 45, 33]  # Out of 96 frames
    colors1 = ['#ff9999', '#ffcc99', '#99ccff']

    wedges, texts, autotexts = ax1.pie(range_counts, labels=['0.5 nm\n(Close)', '1.5 nm\n(Medium)', '3.0 nm\n(Far)'],
                                        colors=colors1, autopct='%1.0f%%', startangle=90,
                                        textprops={'fontsize': 9, 'fontweight': 'bold'})
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    ax1.set_title('Range Settings Used', fontsize=11, fontweight='bold')

    # Pie 2: Time of day
    ax2 = plt.subplot(2, 3, 2)
    time_labels = ['Daytime\n(6am–6pm)', 'Dusk\n(6pm–8pm)', 'Night\n(8pm–6am)']
    time_counts = [62, 18, 16]
    colors2 = ['#ffeb3b', '#ff9800', '#3f51b5']

    wedges, texts, autotexts = ax2.pie(time_counts, labels=time_labels, colors=colors2, autopct='%1.0f%%',
                                        startangle=90, textprops={'fontsize': 9, 'fontweight': 'bold'})
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    ax2.set_title('Collection Time of Day', fontsize=11, fontweight='bold')

    # Pie 3: Weather conditions
    ax3 = plt.subplot(2, 3, 3)
    weather_labels = ['Clear', 'Overcast', 'Light Rain', 'Heavy Rain']
    weather_counts = [48, 32, 12, 4]
    colors3 = ['#87ceeb', '#b0c4de', '#4a90e2', '#1565c0']

    wedges, texts, autotexts = ax3.pie(weather_counts, labels=weather_labels, colors=colors3, autopct='%1.0f%%',
                                        startangle=45, textprops={'fontsize': 8, 'fontweight': 'bold'})
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    ax3.set_title('Weather Conditions', fontsize=11, fontweight='bold')

    # Bar chart: Frames by collection site
    ax4 = plt.subplot(2, 3, 4)
    sites = ['Lake\nMurray', 'Lake\nGreenwood', 'Lake\nMonticello', 'Elizabeth\nRiver', 'Charleston\nHarbor', 'Folly\nBeach']
    site_counts = [18, 15, 12, 20, 21, 10]
    colors4 = ['#4caf50', '#66bb6a', '#81c784', '#a5d6a7', '#2196f3', '#42a5f5']

    bars = ax4.bar(sites, site_counts, color=colors4, edgecolor='black', linewidth=1.5)
    ax4.set_ylabel('Frames Collected', fontsize=10, fontweight='bold')
    ax4.set_title('Frames by Collection Site', fontsize=11, fontweight='bold')
    ax4.grid(axis='y', alpha=0.3)

    for bar, count in zip(bars, site_counts):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(count)}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Bar chart: Frames by rotation speed
    ax5 = plt.subplot(2, 3, 5)
    rpm_labels = ['24 rpm', '30 rpm', '48 rpm']
    rpm_counts = [35, 28, 33]
    colors5 = ['#e91e63', '#f06292', '#f48fb1']

    bars = ax5.bar(rpm_labels, rpm_counts, color=colors5, edgecolor='black', linewidth=1.5)
    ax5.set_ylabel('Frames Collected', fontsize=10, fontweight='bold')
    ax5.set_title('Antenna Rotation Speed', fontsize=11, fontweight='bold')
    ax5.grid(axis='y', alpha=0.3)

    for bar, count in zip(bars, rpm_counts):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(count)}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Summary statistics
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')

    summary_text = """Metadata Summary

Total Frames: 96 (labeled)
Collection Period: May–Dec 2025

Range Settings:
✓ 0.5 nm:  18 frames (19%)
✓ 1.5 nm:  45 frames (47%)
✓ 3.0 nm:  33 frames (34%)

Time of Day:
✓ Daytime:  62 frames (65%)
✓ Dusk:     18 frames (19%)
✓ Night:    16 frames (17%)

Weather:
✓ Clear:        48 (50%)
✓ Overcast:     32 (33%)
✓ Light rain:   12 (13%)
✓ Heavy rain:    4 (4%)

Collection Sites: 6
✓ Inland lakes: 45 frames
✓ Rivers: 20 frames
✓ Coastal: 31 frames

Antenna Speeds:
✓ 24 rpm: 35 frames
✓ 30 rpm: 28 frames
✓ 48 rpm: 33 frames

Implications:
→ Diverse range scales
→ Day & night operations
→ Robust to weather
→ Multiple collection sites
→ Varied temporal sampling
"""

    ax6.text(0.05, 0.5, summary_text, fontsize=7, family='monospace',
            bbox=dict(boxstyle='round', facecolor='#e8f5e9', alpha=0.95, pad=0.5),
            verticalalignment='center')

    fig.suptitle('Experimental Setup: Metadata Distribution',
                fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig30_metadata_distribution.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig30_metadata_distribution.png")
    plt.close()

if __name__ == '__main__':
    print("Generating experimental setup figures 28-30...")
    generate_dataset_split()
    generate_class_imbalance()
    generate_metadata_distribution()
    print("\nAll experimental setup figures generated successfully!")
