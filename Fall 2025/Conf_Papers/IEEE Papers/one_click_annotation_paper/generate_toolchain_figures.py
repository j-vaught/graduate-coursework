#!/usr/bin/env python3
"""Generate open-source toolchain figures 23-27 for the marine radar paper."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
from matplotlib.widgets import Slider
import numpy as np

output_dir = "python_figures"

# Figure 23: Annotator GUI Screenshot
def generate_annotator_gui():
    fig = plt.figure(figsize=(14, 10), dpi=150)
    fig.patch.set_facecolor('white')
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Main window frame
    main_frame = FancyBboxPatch((0.2, 0.2), 13.6, 9.6, boxstyle="round,pad=0.1",
                               fill=True, facecolor='#f5f5f5', edgecolor='black', linewidth=2)
    ax.add_patch(main_frame)

    # Title bar
    title_bar = Rectangle((0.2, 9.3), 13.6, 0.5, fill=True, facecolor='#1976d2', edgecolor='black', linewidth=1.5)
    ax.add_patch(title_bar)
    ax.text(7, 9.55, 'Radar Image Annotator v1.0', ha='center', va='center',
           fontsize=11, fontweight='bold', color='white')

    # Menu bar
    menu_bar = Rectangle((0.2, 8.8), 13.6, 0.45, fill=True, facecolor='#e3f2fd', edgecolor='black', linewidth=1)
    ax.add_patch(menu_bar)
    menu_items = ['File', 'Edit', 'View', 'Help']
    for i, item in enumerate(menu_items):
        ax.text(0.8 + i*2, 9.03, item, fontsize=9, fontweight='bold')

    # Left control panel
    control_panel = Rectangle((0.3, 0.3), 2.8, 8.4, fill=True, facecolor='#eeeeee', edgecolor='black', linewidth=1.5)
    ax.add_patch(control_panel)

    # Control elements
    y_pos = 8.4
    # Load button
    load_btn = FancyBboxPatch((0.5, y_pos - 0.35), 2.4, 0.35, boxstyle="round,pad=0.03",
                             fill=True, facecolor='#4caf50', edgecolor='black', linewidth=1.5)
    ax.add_patch(load_btn)
    ax.text(1.7, y_pos - 0.18, 'Load Images...', ha='center', va='center',
           fontsize=9, fontweight='bold', color='white')

    y_pos -= 0.6
    # Brightness slider
    ax.text(0.6, y_pos, 'Brightness', fontsize=8, fontweight='bold')
    y_pos -= 0.25
    slider_bg = Rectangle((0.5, y_pos - 0.15), 2.6, 0.12, fill=True, facecolor='white', edgecolor='gray', linewidth=1)
    ax.add_patch(slider_bg)
    slider_fill = Rectangle((0.5, y_pos - 0.15), 1.56, 0.12, fill=True, facecolor='#2196f3')
    ax.add_patch(slider_fill)
    circle = Circle((2.06, y_pos - 0.09), 0.08, fill=True, facecolor='#2196f3', edgecolor='black', linewidth=0.5)
    ax.add_patch(circle)
    ax.text(3.3, y_pos - 0.09, '1.2', fontsize=7, va='center')

    y_pos -= 0.5
    # Contrast slider
    ax.text(0.6, y_pos, 'Contrast', fontsize=8, fontweight='bold')
    y_pos -= 0.25
    slider_bg = Rectangle((0.5, y_pos - 0.15), 2.6, 0.12, fill=True, facecolor='white', edgecolor='gray', linewidth=1)
    ax.add_patch(slider_bg)
    slider_fill = Rectangle((0.5, y_pos - 0.15), 1.95, 0.12, fill=True, facecolor='#ff9800')
    ax.add_patch(slider_fill)
    circle = Circle((2.45, y_pos - 0.09), 0.08, fill=True, facecolor='#ff9800', edgecolor='black', linewidth=0.5)
    ax.add_patch(circle)
    ax.text(3.3, y_pos - 0.09, '1.5', fontsize=7, va='center')

    y_pos -= 0.5
    # Class selector
    ax.text(0.6, y_pos, 'Class', fontsize=8, fontweight='bold')
    y_pos -= 0.3
    class_box = FancyBboxPatch((0.5, y_pos - 0.25), 2.6, 0.25, boxstyle="round,pad=0.02",
                              fill=True, facecolor='white', edgecolor='#999999', linewidth=1)
    ax.add_patch(class_box)
    ax.text(0.6, y_pos - 0.125, '◉ Dynamic', fontsize=8, color='lime', fontweight='bold')
    ax.text(1.7, y_pos - 0.125, '○ Static', fontsize=8, color='orange')

    y_pos -= 0.6
    # Navigation buttons
    ax.text(0.6, y_pos, 'Navigation', fontsize=8, fontweight='bold')
    y_pos -= 0.3
    nav_buttons = ['◄ Prev', 'Next ►']
    for i, btn_label in enumerate(nav_buttons):
        nav_btn = FancyBboxPatch((0.5 + i*1.35, y_pos - 0.2), 1.2, 0.25, boxstyle="round,pad=0.02",
                                fill=True, facecolor='#e0e0e0', edgecolor='black', linewidth=1)
        ax.add_patch(nav_btn)
        ax.text(1.1 + i*1.35, y_pos - 0.075, btn_label, ha='center', va='center', fontsize=8, fontweight='bold')

    y_pos -= 0.5
    # Export button
    export_btn = FancyBboxPatch((0.5, y_pos - 0.3), 2.6, 0.3, boxstyle="round,pad=0.03",
                               fill=True, facecolor='#f44336', edgecolor='black', linewidth=1.5)
    ax.add_patch(export_btn)
    ax.text(1.7, y_pos - 0.15, 'Export Labels', ha='center', va='center',
           fontsize=9, fontweight='bold', color='white')

    # Center: Radar image canvas
    canvas = Rectangle((3.3, 1), 10, 7.6, fill=True, facecolor='#000000', edgecolor='black', linewidth=2)
    ax.add_patch(canvas)

    # Draw synthetic radar on canvas
    theta = np.linspace(0, 2*np.pi, 100)
    for r in [1.5, 3, 4.5, 6]:
        x = 3.3 + 5 + (r/6.5)*4.5 * np.cos(theta)
        y = 1 + 3.8 + (r/6.5)*3.8 * np.sin(theta)
        ax.plot(x, y, 'g-', alpha=0.2, linewidth=0.8)

    # Clutter points
    np.random.seed(42)
    for _ in range(30):
        x = np.random.uniform(4, 12.8)
        y = np.random.uniform(1.5, 8.2)
        ax.plot(x, y, 'g.', markersize=2, alpha=0.4)

    # Example boats with bounding boxes
    boats = [
        (5.5, 6.5, 0.5, 0.35, 'lime', 'D'),
        (9, 3.5, 0.6, 0.4, 'lime', 'D'),
        (7, 2.2, 0.8, 0.5, 'orange', 'S'),
    ]
    for bx, by, bw, bh, color, label in boats:
        # Boat point
        ax.plot(bx, by, 'o', color=color, markersize=6)
        # Bounding box
        rect = Rectangle((bx - bw/2, by - bh/2), bw, bh, fill=False, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        # Label
        ax.text(bx - bw/2 - 0.15, by, label, fontsize=8, color=color, fontweight='bold')

    # Status bar at bottom
    status_bar = Rectangle((0.2, 0.2), 13.6, 0.25, fill=True, facecolor='#e0e0e0', edgecolor='black', linewidth=1)
    ax.add_patch(status_bar)
    ax.text(0.4, 0.325, 'Frame: 42/96  |  Annotations: 637  |  Dynamic: 380  Static: 237  |  Ready',
           fontsize=8, va='center', family='monospace')

    ax.set_title('Radar Image Annotator GUI\n(Interactive labeling tool with brightness/contrast controls)',
                fontsize=12, fontweight='bold', pad=15)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig23_annotator_gui.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig23_annotator_gui.png")
    plt.close()

# Figure 24: Annotator Workflow Diagram
def generate_annotator_workflow():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Workflow steps
    steps = [
        (1, 'Load\nRadar PNGs', '#e3f2fd'),
        (3, 'Adjust\nBrightness/\nContrast', '#bbdefb'),
        (5, 'Draw\nBounding\nBox', '#90caf9'),
        (7, 'Assign\nClass Label', '#64b5f6'),
        (9, 'Review &\nExport to\nTXT', '#42a5f5'),
        (11, 'Integration\nwith Training', '#2196f3'),
        (13, 'Done!', '#1976d2'),
    ]

    for x, label, color in steps:
        # Main box
        box = FancyBboxPatch((x - 0.65, 4.5), 1.3, 2, boxstyle="round,pad=0.1",
                            fill=True, facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(box)
        ax.text(x, 5.5, label, ha='center', va='center', fontsize=9, fontweight='bold')

    # Arrows between steps
    for i in range(len(steps) - 1):
        x1 = steps[i][0] + 0.65
        x2 = steps[i+1][0] - 0.65
        arrow = FancyArrowPatch((x1, 5.5), (x2, 5.5),
                               arrowstyle='->', mutation_scale=25, linewidth=2.5, color='darkblue')
        ax.add_patch(arrow)

    # Details under each step
    details = [
        (1, '• Select PNG folder\n• Sequential or random\n• Load metadata'),
        (3, '• Gamma correction\n• Histogram stretch\n• Real-time preview'),
        (5, '• Click & drag\n• Freeform or axis-aligned\n• Move/resize'),
        (7, '• Radio button: Dynamic/Static\n• Keyboard shortcuts: D/S\n• Color-coded boxes'),
        (9, '• Review all labels\n• Format: YOLO or Pascal\n• Save annotations.txt'),
        (11, '• Copy to training dir\n• Split train/val/test\n• Ready for PyTorch'),
        (13, '• ~637 objects labeled\n• ~2–3 hours effort\n• Reproducible dataset'),
    ]

    for i, (x, detail) in enumerate(details):
        ax.text(x, 3.8, detail, ha='center', va='top', fontsize=7, family='monospace',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, pad=0.3))

    # Bottom: Export formats
    ax.text(7, 2.5, 'Output Formats', ha='center', fontsize=10, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='#fff3e0', alpha=0.9, pad=0.5))

    format_text = """YOLO Format:
<class_id> <x_center> <y_center> <width> <height>
(normalized to 0-1)

Pascal VOC Format:
<xmin> <ymin> <xmax> <ymax> <class_name>
(pixel coordinates)

Both supported by OpenCV, PyTorch, TensorFlow"""

    ax.text(7, 1.2, format_text, ha='center', va='center', fontsize=7, family='monospace',
           bbox=dict(boxstyle='round', facecolor='#e8f5e9', alpha=0.95, pad=0.4))

    ax.set_title('Annotator Workflow: From Raw Images to Training-Ready Labels',
                fontsize=13, fontweight='bold', pad=15)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig24_annotator_workflow.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig24_annotator_workflow.png")
    plt.close()

# Figure 25: Radar2PNG Converter Workflow
def generate_radar2png_workflow():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Pipeline stages
    stages = [
        (1.5, 'Input:\nFuruno\nRaw Data\n(proprietary)', '#ffccbc'),
        (3.5, 'Decode\nRange–\nAzimuth\nSweeps', '#ffab91'),
        (5.5, 'Interpolate\nPolar →\nCartesian', '#ff8a65'),
        (7.5, 'Quantize &\nIntensity\nMap', '#ff7043'),
        (9.5, 'Generate\n1735×1735\nPNG', '#ff5722'),
        (11.5, 'Record\nMetadata\nJSON', '#e64a19'),
        (13, 'Output:\nTraining\nDataset', '#bf360c'),
    ]

    for x, label, color in stages:
        box = FancyBboxPatch((x - 0.65, 6), 1.3, 2, boxstyle="round,pad=0.08",
                            fill=True, facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(box)
        ax.text(x, 7, label, ha='center', va='center', fontsize=8, fontweight='bold', color='white')

    # Arrows
    for i in range(len(stages) - 1):
        x1 = stages[i][0] + 0.65
        x2 = stages[i+1][0] - 0.65
        arrow = FancyArrowPatch((x1, 7), (x2, 7),
                               arrowstyle='->', mutation_scale=20, linewidth=2.5, color='darkred')
        ax.add_patch(arrow)

    # Input/Output details
    input_text = """Input Specification:
• Proprietary Furuno format
• Binary range-azimuth sweeps
• Metadata: timestamp, range, speed
• Typical file: ~1 GB/2 hours
• Raw polar grid: 868×800
"""

    ax.text(1.5, 4.5, input_text, ha='center', va='top', fontsize=7, family='monospace',
           bbox=dict(boxstyle='round', facecolor='#fff9c4', alpha=0.95, pad=0.3))

    processing_text = """Processing Steps:
1. Read binary Furuno format
2. Extract range bins & angles
3. Apply bilinear interpolation
4. Normalize intensity (0–255)
5. Write 8-bit grayscale PNG
6. Log: timestamp, param, hash
"""

    ax.text(5.5, 4.5, processing_text, ha='center', va='top', fontsize=7, family='monospace',
           bbox=dict(boxstyle='round', facecolor='#e1f5fe', alpha=0.95, pad=0.3))

    output_text = """Output Specification:
• PNG format (single channel)
• Resolution: 1735×1735
• Pixel values: 0–255 (grayscale)
• File size: ~300 KB/sweep
• Metadata JSON (separate file)
• ~196K frames per campaign
"""

    ax.text(11.5, 4.5, output_text, ha='center', va='top', fontsize=7, family='monospace',
           bbox=dict(boxstyle='round', facecolor='#c8e6c9', alpha=0.95, pad=0.3))

    # Command-line example
    cli_text = """$ python radar2png.py \\
    --input ./raw_furuno_data/ \\
    --output ./png_output/ \\
    --resolution 1735 \\
    --range-scale 3.0 \\
    --interpolation bilinear \\
    --record-metadata \\
    --verbose

Processing: 196000 sweeps → 196000 PNGs
Elapsed: ~45 minutes
Output size: 56 GB
Metadata: metadata.json (1 file)
"""

    ax.text(7, 1.8, cli_text, ha='center', va='center', fontsize=7, family='monospace',
           bbox=dict(boxstyle='round', facecolor='#f5f5f5', edgecolor='black', linewidth=1.5, alpha=0.95, pad=0.4))

    ax.set_title('Radar2PNG Converter Workflow: Proprietary → Standard Formats',
                fontsize=13, fontweight='bold', pad=15)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig25_radar2png_workflow.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig25_radar2png_workflow.png")
    plt.close()

# Figure 26: Command-line Usage Examples
def generate_cli_examples():
    fig, ax = plt.subplots(figsize=(14, 10), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(7, 9.5, 'Command-Line Usage Examples', ha='center', fontsize=14, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='#e0e0e0', alpha=0.9, pad=0.5))

    # Tool 1: Radar2PNG
    y_start = 8.5
    ax.text(0.5, y_start, '1. Radar2PNG Converter', fontsize=11, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='#ffccbc', alpha=0.8, pad=0.3))

    cmd1 = """# Basic conversion
$ python radar2png.py --input ./raw_data --output ./pngs

# With all options
$ python radar2png.py \\
    --input ./raw_furuno/ \\
    --output ./training_pngs/ \\
    --resolution 1735 \\
    --range-scale 3.0 \\
    --interpolation bilinear \\
    --brightness 1.0 \\
    --contrast 1.2 \\
    --record-metadata \\
    --threads 4 \\
    --verbose
"""

    ax.text(0.7, y_start - 0.4, cmd1, fontsize=7, family='monospace',
           bbox=dict(boxstyle='round', facecolor='white', edgecolor='#ff7043', linewidth=1.5, alpha=0.95, pad=0.4),
           verticalalignment='top')

    # Tool 2: Annotator
    y_start = 5.2
    ax.text(0.5, y_start, '2. Radar Image Annotator', fontsize=11, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='#bbdefb', alpha=0.8, pad=0.3))

    cmd2 = """# Launch GUI
$ python annotator.py --input ./pngs

# Advanced options
$ python annotator.py \\
    --input ./pngs/ \\
    --output ./labels.txt \\
    --format yolo \\
    --classes dynamic,static \\
    --colors lime,orange \\
    --start-frame 0 \\
    --colormap gray \\
    --fullscreen
"""

    ax.text(0.7, y_start - 0.4, cmd2, fontsize=7, family='monospace',
           bbox=dict(boxstyle='round', facecolor='white', edgecolor='#42a5f5', linewidth=1.5, alpha=0.95, pad=0.4),
           verticalalignment='top')

    # Tool 3: EchoTrail Generator
    y_start = 1.9
    ax.text(0.5, y_start, '3. Echo-Trail Generator', fontsize=11, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='#c8e6c9', alpha=0.8, pad=0.3))

    cmd3 = """# Generate trails for existing PNGs
$ python echo_trail.py \\
    --input ./pngs/ \\
    --output ./trails/ \\
    --trail-lengths 4,8,16 \\
    --opacity-schedule linear

# As Python library
from echo_trail import EchoTrailGenerator
gen = EchoTrailGenerator(trail_length=4)
composite = gen.generate(frame_sequence, opacities=[0.25, 0.5, 0.75, 1.0])
"""

    ax.text(0.7, y_start - 0.4, cmd3, fontsize=7, family='monospace',
           bbox=dict(boxstyle='round', facecolor='white', edgecolor='#66bb6a', linewidth=1.5, alpha=0.95, pad=0.4),
           verticalalignment='top')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig26_cli_examples.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig26_cli_examples.png")
    plt.close()

# Figure 27: Toolchain Integration Diagram
def generate_toolchain_integration():
    fig, ax = plt.subplots(figsize=(14, 10), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(7, 9.5, 'Complete Toolchain Integration Pipeline', ha='center', fontsize=14, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='#e0e0e0', alpha=0.9, pad=0.5))

    # Full pipeline visualization
    pipeline_stages = [
        (1, 8.5, 'Furuno NXT\nRadar\n(raw data)', '#ffccbc', 'Input'),
        (1, 6.5, 'Binary\nRange–Azimuth\nSweeps', '#ffccbc', ''),
        (3.5, 7.5, 'Radar2PNG\nConverter', '#ff7043', 'Tool 1'),
        (3.5, 5.5, 'PNG Images\n+ Metadata', '#ff7043', ''),
        (6, 7.5, 'Radar\nAnnotator\nGUI', '#42a5f5', 'Tool 2'),
        (6, 5.5, 'Bounding Box\nLabels\n(YOLO/Pascal)', '#42a5f5', ''),
        (8.5, 7.5, 'EchoTrail\nGenerator', '#66bb6a', 'Tool 3'),
        (8.5, 5.5, 'Temporal\nAugmented\nFrames', '#66bb6a', ''),
        (11.5, 7.5, 'Training\nPipeline\n(PyTorch)', '#9c27b0', 'Integration'),
        (11.5, 5.5, 'Trained\nDetector\nModel', '#9c27b0', ''),
        (11.5, 3.5, 'Detection\nResults', '#7b1fa2', 'Output'),
    ]

    # Draw all boxes
    for x, y, label, color, category in pipeline_stages:
        if 'Furuno' in label or 'Detection' in label or 'Trained' in label:
            w, h = 1.2, 1.2
        elif 'Training' in label:
            w, h = 1.2, 1.8
        else:
            w, h = 1, 1

        box = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.08",
                            fill=True, facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, fontweight='bold', color='white')

        # Category label
        if category:
            ax.text(x, y + h/2 + 0.25, category, ha='center', fontsize=7, style='italic',
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.6, pad=0.1))

    # Draw arrows
    arrows = [
        # Input to Radar2PNG
        ((1.6, 8.5), (2.5, 8.0)),
        ((1.6, 6.5), (2.5, 6.0)),
        # Radar2PNG to Annotator
        ((4.5, 8.0), (5.2, 8.0)),
        ((4.5, 6.0), (5.2, 6.0)),
        # Annotator to EchoTrail
        ((6.8, 8.0), (7.8, 8.0)),
        ((6.8, 6.0), (7.8, 6.0)),
        # EchoTrail to Training
        ((9.3, 8.0), (10.6, 8.0)),
        ((9.3, 6.0), (10.6, 6.0)),
        # Training to output
        ((11.5, 4.7), (11.5, 4.0)),
    ]

    for (x1, y1), (x2, y2) in arrows:
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                               arrowstyle='->', mutation_scale=20, linewidth=2.5, color='darkblue')
        ax.add_patch(arrow)

    # Data flow info boxes
    info_boxes = [
        (1, 4.8, 'Acquisition:\n• 196K unlabeled\n• Time-series data\n• Variable range'),
        (3.5, 4.8, 'Preprocessing:\n• Polar→Cartesian\n• 1735×1735 PNG\n• ~300 KB/frame'),
        (6, 4.8, 'Annotation:\n• 96 labeled frames\n• 2 classes\n• 637 objects'),
        (8.5, 4.8, 'Augmentation:\n• T ∈ {1,4,8,16}\n• Opacity decay\n• Motion context'),
        (11.5, 2.2, 'Deployment:\n• mAP@0.5\n• Per-class metrics\n• Inference: 30-200ms'),
    ]

    for x, y, info in info_boxes:
        ax.text(x, y, info, ha='center', va='top', fontsize=7, family='monospace',
               bbox=dict(boxstyle='round', facecolor='#fffde7', alpha=0.9, edgecolor='gray', linewidth=1, pad=0.3))

    # Bottom: Key Features
    features = """Key Features:
✓ Open-source (GitHub) — Reproducible and auditable
✓ Modular design — Use any combination of tools
✓ Documented parameters — Record all preprocessing settings
✓ Multi-format support — YOLO, Pascal VOC, COCO formats
✓ Batch processing — Handle thousands of frames efficiently
✓ Python-based — Easy integration with PyTorch/TensorFlow
"""

    ax.text(7, 0.4, features, ha='center', va='center', fontsize=8, family='monospace',
           bbox=dict(boxstyle='round', facecolor='#e8f5e9', edgecolor='black', linewidth=1.5, alpha=0.95, pad=0.4))

    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig27_toolchain_integration.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: fig27_toolchain_integration.png")
    plt.close()

if __name__ == '__main__':
    print("Generating toolchain figures 23-27...")
    generate_annotator_gui()
    generate_annotator_workflow()
    generate_radar2png_workflow()
    generate_cli_examples()
    generate_toolchain_integration()
    print("\nAll toolchain figures generated successfully!")
