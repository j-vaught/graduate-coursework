"""Create 4 visualizations of Charleston radar data components.

1. Raw Charleston frame (single scan, PPI image)
2. Land-only frame (from land_frames.tar.gz)
3. 3x3 collage of target objects from the object library (diverse sizes)
4. 3x3 collage of synthetic clutter streak patterns
"""

import json
import os
import sys
import tarfile
import random
import copy

import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Brand colors
GARNET = '#73000A'
BLACK90 = '#363636'
BLACK70 = '#5C5C5C'
BLACK50 = '#A2A2A2'
ATLANTIC = '#466A9F'
HORSESHOE = '#65780B'

# Add generation module to path
sys.path.insert(0, '/Volumes/MacShare/graduate-coursework/Research/echo_trail/echotrails-ablation/generation')

from radar_core.csv_handler import NUM_RANGE_BINS, RadarCSVHandler, RadarFrame, Pulse
from radar_core.converter import ConversionConfig, RadarConverter
from radar_core.clutter import generate_clutter_streaks

# Setup paths
RAW_DIR = '/Volumes/MacShare/DATA/FURUNO_data/CSV_data/GriceLab_20251117_1141_5_Constant_80_80_Interference'
DATA_DIR = '/Volumes/MacShare/graduate-coursework/Research/echo_trail/echotrails-ablation/data'
OBJ_LIB = os.path.join(DATA_DIR, 'object_library')
LAND_TAR = os.path.join(DATA_DIR, 'land_frames.tar.gz')
OUT_DIR = '/Volumes/MacShare/graduate-coursework/Research/echo_trail/presentation'

# Radar green colormap (black -> green)
radar_cmap = LinearSegmentedColormap.from_list('radar', ['black', '#00CC00'])


def render_raw_charleston():
    """Render a single raw Charleston radar frame as PPI."""
    csv_files = sorted([f for f in os.listdir(RAW_DIR) if f.endswith('.csv')])
    csv_path = os.path.join(RAW_DIR, csv_files[len(csv_files) // 2])

    frame = RadarCSVHandler.read_csv_uncached(csv_path)
    converter = RadarConverter(ConversionConfig())
    gray = converter.polar_to_cartesian_gray(frame)

    fig, ax = plt.subplots(1, 1, figsize=(8, 8), facecolor='black')
    ax.imshow(gray, cmap=radar_cmap, vmin=0, vmax=255)
    ax.set_title('Raw Charleston Recording (Single Scan)', color='white',
                 fontsize=14, fontweight='bold', pad=10)
    ax.axis('off')
    fig.tight_layout(pad=0.5)
    out_path = os.path.join(OUT_DIR, 'viz_raw_charleston.png')
    fig.savefig(out_path, dpi=200, facecolor='black', bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {out_path}')


def render_land_frame():
    """Extract and render one land frame from the tar archive."""
    converter = RadarConverter(ConversionConfig())

    with tarfile.open(LAND_TAR, 'r:gz') as tar:
        members = [m for m in tar.getmembers() if m.name.endswith('.csv')]
        members.sort(key=lambda m: m.name)
        member = members[len(members) // 2]
        f = tar.extractfile(member)
        tmp_path = '/tmp/_land_frame_tmp.csv'
        with open(tmp_path, 'wb') as out:
            out.write(f.read())
        frame = RadarCSVHandler.read_csv_uncached(tmp_path)
        os.remove(tmp_path)

    gray = converter.polar_to_cartesian_gray(frame)

    fig, ax = plt.subplots(1, 1, figsize=(8, 8), facecolor='black')
    ax.imshow(gray, cmap=radar_cmap, vmin=0, vmax=255)
    ax.set_title('Land-Only Frame (Targets/Interference Removed)', color='white',
                 fontsize=14, fontweight='bold', pad=10)
    ax.axis('off')
    fig.tight_layout(pad=0.5)
    out_path = os.path.join(OUT_DIR, 'viz_land_frame.png')
    fig.savefig(out_path, dpi=200, facecolor='black', bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {out_path}')


def render_object_collage():
    """Create a 3x3 collage of target objects with diverse sizes."""
    files = sorted(f for f in os.listdir(OBJ_LIB) if f != 'metadata.json')
    objects = []
    for fname in files:
        with open(os.path.join(OBJ_LIB, fname)) as fh:
            obj = json.load(fh)
        if 'echo_data' in obj:
            objects.append(obj)

    # Sort by area
    objects.sort(key=lambda o: o.get('area', 0))

    # Pick 3 from each size tier: small, medium, large
    n = len(objects)
    tier_size = n // 3
    selected = []
    for tier_idx in range(3):
        start = tier_idx * tier_size
        end = start + tier_size if tier_idx < 2 else n
        chunk = objects[start:end]
        random.seed(42 + tier_idx)
        # Pick 3 with varying aspect ratios within each tier
        chunk_with_ratio = [(o, len(o['echo_data']) / max(len(o['echo_data'][0]), 1)) for o in chunk]
        chunk_with_ratio.sort(key=lambda x: x[1])
        # Pick from spread: low ratio, mid ratio, high ratio
        indices = [0, len(chunk_with_ratio) // 2, len(chunk_with_ratio) - 1]
        for i in indices:
            selected.append(chunk_with_ratio[i][0])

    # Sort selected by area for presentation: small→large, top-left to bottom-right
    selected.sort(key=lambda o: o.get('area', 0))

    fig, axes = plt.subplots(3, 3, figsize=(10, 10), facecolor='black')
    fig.suptitle('Target Objects from Object Library', color='white',
                 fontsize=16, fontweight='bold', y=0.98)

    size_labels = ['Small', 'Small', 'Small', 'Medium', 'Medium', 'Medium',
                   'Large', 'Large', 'Large']

    for idx, ax in enumerate(axes.flat):
        if idx < len(selected):
            obj = selected[idx]
            echo = np.array(obj['echo_data'], dtype=np.float32)
            ax.imshow(echo, cmap=radar_cmap, vmin=0, vmax=255, aspect='equal',
                      interpolation='nearest')
            area = obj.get('area', 0)
            h, w = len(obj['echo_data']), len(obj['echo_data'][0])
            ax.set_title(f'{size_labels[idx]}  |  {h}x{w}  |  Area: {area}',
                         color=BLACK50, fontsize=9, pad=4)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(BLACK70)
            spine.set_linewidth(0.5)

    fig.tight_layout(pad=1.0, rect=[0, 0, 1, 0.95])
    out_path = os.path.join(OUT_DIR, 'viz_target_collage.png')
    fig.savefig(out_path, dpi=200, facecolor='black', bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {out_path}')


def make_blank_frame(num_pulses=720):
    """Create a blank RadarFrame for clutter injection."""
    import math
    pulses = []
    for i in range(num_pulses):
        angle_rad = (i / num_pulses) * 2.0 * math.pi
        angle_ticks = int((i / num_pulses) * 4096)
        p = Pulse(
            status=1,
            scale=496,
            range_=5,
            gain=80,
            angle_ticks=angle_ticks,
            angle_rad=angle_rad,
            echoes=np.zeros(NUM_RANGE_BINS, dtype=np.uint8)
        )
        pulses.append(p)
    frame = RadarFrame(
        source_path='synthetic',
        timestamp='synthetic',
        pulses=pulses
    )
    frame.update_unique_angles()
    return frame


def render_clutter_collage():
    """Create a 3x3 collage of synthetic clutter patterns at different intensities."""
    converter = RadarConverter(ConversionConfig())

    # 9 clutter configurations: vary streak count and intensity
    configs = [
        (15,  (30, 80),   'Light  |  15 streaks'),
        (25,  (40, 100),  'Light-Med  |  25 streaks'),
        (40,  (50, 120),  'Moderate  |  40 streaks'),
        (60,  (60, 140),  'Med-Heavy  |  60 streaks'),
        (80,  (70, 160),  'Heavy  |  80 streaks'),
        (100, (80, 180),  'Very Heavy  |  100 streaks'),
        (120, (90, 200),  'Extreme  |  120 streaks'),
        (150, (100, 220), 'Severe  |  150 streaks'),
        (200, (120, 252), 'Maximum  |  200 streaks'),
    ]

    fig, axes = plt.subplots(3, 3, figsize=(12, 12), facecolor='black')
    fig.suptitle('Synthetic Clutter Patterns (Radial Streaks)',
                 color='white', fontsize=16, fontweight='bold', y=0.98)

    for idx, (ax, (n_streaks, intensity_range, label)) in enumerate(zip(axes.flat, configs)):
        frame = make_blank_frame()
        generate_clutter_streaks(frame, n_streaks, intensity_range, seed=100 + idx)
        gray = converter.polar_to_cartesian_gray(frame)
        ax.imshow(gray, cmap=radar_cmap, vmin=0, vmax=255)
        ax.set_title(label, color=BLACK50, fontsize=9, pad=4)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(BLACK70)
            spine.set_linewidth(0.5)

    fig.tight_layout(pad=1.0, rect=[0, 0, 1, 0.95])
    out_path = os.path.join(OUT_DIR, 'viz_clutter_collage.png')
    fig.savefig(out_path, dpi=200, facecolor='black', bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {out_path}')


if __name__ == '__main__':
    print('=== Creating Charleston Data Visualizations ===')
    print()

    print('[1/4] Rendering raw Charleston frame...')
    render_raw_charleston()
    print()

    print('[2/4] Rendering land-only frame...')
    render_land_frame()
    print()

    print('[3/4] Creating target object collage...')
    render_object_collage()
    print()

    print('[4/4] Creating synthetic clutter collage...')
    render_clutter_collage()
    print()

    print('=== Done! ===')
