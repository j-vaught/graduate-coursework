"""
CSCE 763 - Homework 2, Problem 2
Image Subtraction Defect Detection Analysis

Demonstrates various failure modes that affect image subtraction-based
defect detection in industrial inspection applications.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import cv2
from pathlib import Path

# USC Brand Colors
USC_GARNET = '#73000A'
USC_BLACK = '#000000'
USC_BLACK90 = '#363636'
USC_BLACK70 = '#5C5C5C'
USC_BLACK50 = '#A2A2A2'
USC_ATLANTIC = '#466A9F'
USC_CONGAREE = '#1F414D'
USC_ROSE = '#CC2E40'
USC_HONEYCOMB = '#A49137'
USC_HORSESHOE = '#65780B'

# Set plot style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

def load_golden_image(path):
    """Load the golden reference image."""
    img = cv2.imread(str(path))
    if img is None:
        raise FileNotFoundError(f"Could not load image: {path}")
    # Convert BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def to_grayscale(img):
    """Convert RGB image to grayscale."""
    if len(img.shape) == 3:
        return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return img

def compute_difference(golden, test, use_abs=True):
    """Compute difference image between golden and test images."""
    golden_gray = to_grayscale(golden).astype(np.float32)
    test_gray = to_grayscale(test).astype(np.float32)
    diff = test_gray - golden_gray
    if use_abs:
        diff = np.abs(diff)
    return diff

def normalize_for_display(img):
    """Normalize image for display (0-255 range)."""
    img_min, img_max = img.min(), img.max()
    if img_max - img_min > 0:
        return ((img - img_min) / (img_max - img_min) * 255).astype(np.uint8)
    return np.zeros_like(img, dtype=np.uint8)

# ============================================================================
# FAILURE MODE SIMULATIONS
# ============================================================================

def simulate_brightness_change(img, delta):
    """Simulate illumination intensity change."""
    adjusted = img.astype(np.float32) + delta
    return np.clip(adjusted, 0, 255).astype(np.uint8)

def simulate_contrast_change(img, factor):
    """Simulate contrast/gain change."""
    mean_val = np.mean(img)
    adjusted = (img.astype(np.float32) - mean_val) * factor + mean_val
    return np.clip(adjusted, 0, 255).astype(np.uint8)

def simulate_translation(img, dx, dy):
    """Simulate spatial misalignment via translation."""
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))

def simulate_rotation(img, angle):
    """Simulate rotational misalignment."""
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(img, M, (w, h))

def simulate_scale_change(img, scale_factor):
    """Simulate scale/zoom change."""
    h, w = img.shape[:2]
    new_w, new_h = int(w * scale_factor), int(h * scale_factor)
    resized = cv2.resize(img, (new_w, new_h))

    # Center crop or pad to original size
    if scale_factor > 1:
        # Crop center
        start_x = (new_w - w) // 2
        start_y = (new_h - h) // 2
        return resized[start_y:start_y+h, start_x:start_x+w]
    else:
        # Pad with black
        result = np.zeros_like(img)
        start_x = (w - new_w) // 2
        start_y = (h - new_h) // 2
        result[start_y:start_y+new_h, start_x:start_x+new_w] = resized
        return result

def simulate_gaussian_noise(img, sigma):
    """Simulate sensor noise."""
    noise = np.random.normal(0, sigma, img.shape)
    noisy = img.astype(np.float32) + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)

def simulate_blur(img, kernel_size):
    """Simulate focus blur."""
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def simulate_vignetting(img, strength=0.5):
    """Simulate vignetting (non-uniform illumination)."""
    h, w = img.shape[:2]
    Y, X = np.ogrid[:h, :w]
    center_y, center_x = h // 2, w // 2
    max_dist = np.sqrt(center_x**2 + center_y**2)
    dist = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
    vignette = 1 - strength * (dist / max_dist)

    if len(img.shape) == 3:
        vignette = np.expand_dims(vignette, axis=2)

    result = img.astype(np.float32) * vignette
    return np.clip(result, 0, 255).astype(np.uint8)

def simulate_color_temperature_shift(img, shift):
    """Simulate white balance / color temperature change."""
    result = img.copy().astype(np.float32)
    # Warm shift: increase red, decrease blue
    # Cool shift: decrease red, increase blue
    result[:, :, 0] = np.clip(result[:, :, 0] + shift, 0, 255)  # Red
    result[:, :, 2] = np.clip(result[:, :, 2] - shift, 0, 255)  # Blue
    return result.astype(np.uint8)

def simulate_perspective_distortion(img, strength=0.05):
    """Simulate perspective/viewing angle change."""
    h, w = img.shape[:2]
    offset = int(w * strength)

    src_pts = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    dst_pts = np.float32([[offset, 0], [w-offset, 0], [w, h], [0, h]])

    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    return cv2.warpPerspective(img, M, (w, h))

def simulate_missing_component(img, x, y, w_rect, h_rect):
    """Simulate a missing component (defect)."""
    result = img.copy()
    # Fill with background-like color (dark)
    result[y:y+h_rect, x:x+w_rect] = [15, 10, 25]
    return result

def simulate_exposure_change(img, ev_stops):
    """Simulate exposure change in EV stops."""
    factor = 2 ** ev_stops
    result = img.astype(np.float32) * factor
    return np.clip(result, 0, 255).astype(np.uint8)

def simulate_shadow(img, direction='left', strength=0.4):
    """Simulate directional shadow."""
    h, w = img.shape[:2]
    if direction == 'left':
        gradient = np.linspace(strength, 1, w)
    elif direction == 'right':
        gradient = np.linspace(1, strength, w)
    elif direction == 'top':
        gradient = np.linspace(strength, 1, h).reshape(-1, 1)
    else:  # bottom
        gradient = np.linspace(1, strength, h).reshape(-1, 1)

    if direction in ['left', 'right']:
        gradient = np.tile(gradient, (h, 1))
    else:
        gradient = np.tile(gradient, (1, w))

    if len(img.shape) == 3:
        gradient = np.expand_dims(gradient, axis=2)

    result = img.astype(np.float32) * gradient
    return np.clip(result, 0, 255).astype(np.uint8)

# ============================================================================
# VISUALIZATION
# ============================================================================

def create_failure_mode_figure(golden, test, title, factor_name, save_path=None):
    """Create a figure showing golden, test, and difference images."""
    diff = compute_difference(golden, test)
    diff_normalized = normalize_for_display(diff)

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    # Golden image
    axes[0].imshow(golden)
    axes[0].set_title('Golden Image', fontsize=12, fontweight='bold', color=USC_BLACK90)
    axes[0].axis('off')

    # Test image with simulated issue
    axes[1].imshow(test)
    axes[1].set_title(f'Test Image\n({factor_name})', fontsize=12, fontweight='bold', color=USC_BLACK90)
    axes[1].axis('off')

    # Difference image
    im = axes[2].imshow(diff_normalized, cmap='hot')
    axes[2].set_title('Difference Image\n(False Positives)', fontsize=12, fontweight='bold', color=USC_ROSE)
    axes[2].axis('off')

    # Add colorbar
    cbar = plt.colorbar(im, ax=axes[2], fraction=0.046, pad=0.04)
    cbar.set_label('|Difference|', fontsize=10)

    plt.suptitle(title, fontsize=14, fontweight='bold', color=USC_GARNET, y=1.02)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close()
    else:
        plt.show()

    return diff.mean(), diff.max()

def create_comprehensive_analysis(golden_path, output_dir):
    """Create comprehensive analysis of all failure modes."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    golden = load_golden_image(golden_path)

    # Dictionary of failure modes and their parameters
    failure_modes = {
        '01_brightness_increase': {
            'func': simulate_brightness_change,
            'params': {'delta': 40},
            'title': 'Factor 1: Illumination Intensity Change',
            'factor_name': '+40 brightness'
        },
        '02_brightness_decrease': {
            'func': simulate_brightness_change,
            'params': {'delta': -40},
            'title': 'Factor 1: Illumination Intensity Change',
            'factor_name': '-40 brightness'
        },
        '03_contrast_high': {
            'func': simulate_contrast_change,
            'params': {'factor': 1.3},
            'title': 'Factor 2: Contrast/Gain Variation',
            'factor_name': '1.3x contrast'
        },
        '04_contrast_low': {
            'func': simulate_contrast_change,
            'params': {'factor': 0.7},
            'title': 'Factor 2: Contrast/Gain Variation',
            'factor_name': '0.7x contrast'
        },
        '05_translation': {
            'func': simulate_translation,
            'params': {'dx': 5, 'dy': 3},
            'title': 'Factor 3: Spatial Translation',
            'factor_name': '5px right, 3px down'
        },
        '06_rotation': {
            'func': simulate_rotation,
            'params': {'angle': 2},
            'title': 'Factor 4: Rotational Misalignment',
            'factor_name': '2° rotation'
        },
        '07_scale': {
            'func': simulate_scale_change,
            'params': {'scale_factor': 1.03},
            'title': 'Factor 5: Scale/Zoom Variation',
            'factor_name': '3% zoom in'
        },
        '08_noise': {
            'func': simulate_gaussian_noise,
            'params': {'sigma': 20},
            'title': 'Factor 6: Sensor Noise',
            'factor_name': 'σ=20 Gaussian noise'
        },
        '09_blur': {
            'func': simulate_blur,
            'params': {'kernel_size': 7},
            'title': 'Factor 7: Focus Blur',
            'factor_name': '7x7 Gaussian blur'
        },
        '10_vignetting': {
            'func': simulate_vignetting,
            'params': {'strength': 0.5},
            'title': 'Factor 8: Non-uniform Illumination (Vignetting)',
            'factor_name': '50% vignette'
        },
        '11_color_warm': {
            'func': simulate_color_temperature_shift,
            'params': {'shift': 30},
            'title': 'Factor 9: Color Temperature Shift',
            'factor_name': 'Warmer (+30R, -30B)'
        },
        '12_perspective': {
            'func': simulate_perspective_distortion,
            'params': {'strength': 0.05},
            'title': 'Factor 10: Perspective Distortion',
            'factor_name': '5% perspective shift'
        },
        '13_exposure_over': {
            'func': simulate_exposure_change,
            'params': {'ev_stops': 0.5},
            'title': 'Factor 11: Exposure Change',
            'factor_name': '+0.5 EV (overexposed)'
        },
        '14_shadow': {
            'func': simulate_shadow,
            'params': {'direction': 'left', 'strength': 0.5},
            'title': 'Factor 12: Directional Shadow',
            'factor_name': 'Left shadow'
        },
    }

    # Track statistics
    stats = []

    # Generate each failure mode visualization
    for name, config in failure_modes.items():
        test_img = config['func'](golden, **config['params'])
        save_path = output_dir / f"failure_{name}.png"
        mean_diff, max_diff = create_failure_mode_figure(
            golden, test_img, config['title'], config['factor_name'], save_path
        )
        stats.append({
            'name': name,
            'title': config['title'],
            'factor': config['factor_name'],
            'mean_diff': mean_diff,
            'max_diff': max_diff
        })
        print(f"Generated: {save_path.name}")

    # Create a real defect example
    h, w = golden.shape[:2]
    defective = simulate_missing_component(golden, w//3, h//3, 40, 40)
    save_path = output_dir / "failure_15_real_defect.png"
    mean_diff, max_diff = create_failure_mode_figure(
        golden, defective,
        'True Defect: Missing Component',
        'Simulated missing area',
        save_path
    )
    stats.append({
        'name': '15_real_defect',
        'title': 'True Defect',
        'factor': 'Missing component',
        'mean_diff': mean_diff,
        'max_diff': max_diff
    })
    print(f"Generated: {save_path.name}")

    return stats

def create_summary_figure(golden_path, output_dir):
    """Create a single summary figure with multiple failure modes."""
    golden = load_golden_image(golden_path)
    output_dir = Path(output_dir)

    # Select key failure modes for summary
    modes = [
        ('Brightness +40', simulate_brightness_change(golden, 40)),
        ('Translation 5px', simulate_translation(golden, 5, 3)),
        ('Rotation 2°', simulate_rotation(golden, 2)),
        ('Noise σ=20', simulate_gaussian_noise(golden, 20)),
        ('Blur 7x7', simulate_blur(golden, 7)),
        ('Vignetting', simulate_vignetting(golden, 0.5)),
    ]

    fig, axes = plt.subplots(3, 6, figsize=(18, 9))

    # First row: Test images
    # Second row: Difference images
    # Third row: Thresholded difference

    for i, (name, test) in enumerate(modes):
        diff = compute_difference(golden, test)
        diff_norm = normalize_for_display(diff)

        # Row 1: Test image
        axes[0, i].imshow(test)
        axes[0, i].set_title(name, fontsize=10, fontweight='bold')
        axes[0, i].axis('off')

        # Row 2: Difference image
        axes[1, i].imshow(diff_norm, cmap='hot')
        axes[1, i].set_title(f'Diff (mean={diff.mean():.1f})', fontsize=9)
        axes[1, i].axis('off')

        # Row 3: Thresholded (simulating detection)
        threshold = 30
        detected = (diff > threshold).astype(np.uint8) * 255
        axes[2, i].imshow(detected, cmap='gray')
        axes[2, i].set_title(f'Detected (T={threshold})', fontsize=9)
        axes[2, i].axis('off')

    # Add row labels
    fig.text(0.02, 0.78, 'Test\nImages', ha='center', va='center', fontsize=12,
             fontweight='bold', color=USC_GARNET)
    fig.text(0.02, 0.50, 'Difference\nImages', ha='center', va='center', fontsize=12,
             fontweight='bold', color=USC_GARNET)
    fig.text(0.02, 0.22, 'False\nPositives', ha='center', va='center', fontsize=12,
             fontweight='bold', color=USC_ROSE)

    plt.suptitle('Summary: Failure Modes in Image Subtraction Detection',
                 fontsize=14, fontweight='bold', color=USC_GARNET, y=0.98)

    plt.tight_layout(rect=[0.04, 0, 1, 0.95])

    save_path = output_dir / "failure_modes_summary.png"
    plt.savefig(save_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"Generated: {save_path.name}")

def create_comparison_bar_chart(stats, output_dir):
    """Create bar chart comparing mean difference for each failure mode."""
    output_dir = Path(output_dir)

    # Sort by mean difference
    stats_sorted = sorted(stats, key=lambda x: x['mean_diff'], reverse=True)

    names = [s['factor'] for s in stats_sorted]
    means = [s['mean_diff'] for s in stats_sorted]

    # Color the bars: red for failure modes, green for real defect
    colors = [USC_ROSE if 'defect' not in s['name'].lower() else USC_HORSESHOE
              for s in stats_sorted]

    fig, ax = plt.subplots(figsize=(12, 8))

    y_pos = np.arange(len(names))
    bars = ax.barh(y_pos, means, color=colors, edgecolor='none')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=10)
    ax.set_xlabel('Mean Absolute Difference', fontsize=12, fontweight='bold')
    ax.set_title('Comparison of Failure Mode Severity\n(Higher = More False Positives)',
                 fontsize=14, fontweight='bold', color=USC_GARNET)

    # Add value labels
    for bar, mean in zip(bars, means):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f'{mean:.1f}', va='center', fontsize=9)

    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=USC_ROSE, label='Failure Mode (False Positive)'),
        Patch(facecolor=USC_HORSESHOE, label='True Defect')
    ]
    ax.legend(handles=legend_elements, loc='lower right')

    ax.invert_yaxis()
    plt.tight_layout()

    save_path = output_dir / "failure_modes_comparison.png"
    plt.savefig(save_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"Generated: {save_path.name}")

def main():
    """Main execution."""
    base_dir = Path(__file__).parent
    golden_path = base_dir / "example_golden.png"
    output_dir = base_dir / "figures"

    print("=" * 60)
    print("CSCE 763 - HW2 Problem 2: Image Subtraction Analysis")
    print("=" * 60)
    print(f"\nGolden image: {golden_path}")
    print(f"Output directory: {output_dir}\n")

    # Run comprehensive analysis
    stats = create_comprehensive_analysis(golden_path, output_dir)

    # Create summary figure
    create_summary_figure(golden_path, output_dir)

    # Create comparison bar chart
    create_comparison_bar_chart(stats, output_dir)

    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)

    # Print statistics table
    print("\nFailure Mode Statistics:")
    print("-" * 60)
    print(f"{'Factor':<40} {'Mean Diff':>10} {'Max Diff':>10}")
    print("-" * 60)
    for s in sorted(stats, key=lambda x: x['mean_diff'], reverse=True):
        print(f"{s['factor']:<40} {s['mean_diff']:>10.2f} {s['max_diff']:>10.2f}")

if __name__ == "__main__":
    main()
