import csv
import matplotlib.pyplot as plt
import numpy as np
import os

# Configuration for "Science" style plots
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['figure.dpi'] = 300

OUTPUT_DIR = 'bbox_analysis_figures'

def load_data():
    widths, heights = [], []
    center_xs, center_ys = [], []

    # Load Sizes
    if os.path.exists('bbox_sizes.csv'):
        with open('bbox_sizes.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    widths.append(float(row['width']))
                    heights.append(float(row['height']))
                except ValueError: pass
    
    # Load Centers
    if os.path.exists('bbox_centers.csv'):
        with open('bbox_centers.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    center_xs.append(float(row['center_x']))
                    center_ys.append(float(row['center_y']))
                except ValueError: pass
                
    return np.array(widths), np.array(heights), np.array(center_xs), np.array(center_ys)

def plot_spatial_heatmap(x, y):
    """Figure 1: Spatial distribution of object centers."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Use a 2D histogram (heatmap)
    # Assuming typical image aspect ratio, but we let data define limits
    h = ax.hist2d(x, y, bins=64, cmap='inferno', density=True, cmin=1e-10)
    
    ax.set_title('Object Center Spatial Distribution', fontsize=14, pad=15)
    ax.set_xlabel('Center X (pixels)', fontsize=12)
    ax.set_ylabel('Center Y (pixels)', fontsize=12)
    
    # Invert Y axis to match image coordinates (0,0 at top-left)
    ax.invert_yaxis()
    
    cbar = plt.colorbar(h[3], ax=ax)
    cbar.set_label('Density', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '01_spatial_heatmap.png'))
    plt.close()
    print("Generated 01_spatial_heatmap.png")

def plot_size_distribution(w, h):
    """Figure 2: Width vs Height distribution (Hexbin)."""
    fig, ax = plt.subplots(figsize=(7, 7))
    
    # Hexbin plot is great for dense scatter data
    hb = ax.hexbin(w, h, gridsize=40, cmap='Blues', mincnt=1, bins='log', edgecolors='none')
    
    # Add diagonal lines for common aspect ratios
    max_val = max(np.max(w), np.max(h))
    ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.3, label='1:1 Ratio')
    ax.plot([0, max_val], [0, max_val/2], 'r--', alpha=0.3, label='2:1 Ratio')
    ax.plot([0, max_val/2], [0, max_val], 'g--', alpha=0.3, label='1:2 Ratio')

    ax.set_title('Bounding Box Dimensions (Log Scale Density)', fontsize=14, pad=15)
    ax.set_xlabel('Width (pixels)', fontsize=12)
    ax.set_ylabel('Height (pixels)', fontsize=12)
    ax.legend(loc='upper right')
    
    cb = fig.colorbar(hb, ax=ax)
    cb.set_label('Count (log10)', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '02_size_hexbin.png'))
    plt.close()
    print("Generated 02_size_hexbin.png")

def plot_aspect_ratio_area(w, h):
    """Figure 3: Aspect Ratio distribution."""
    areas = w * h
    aspect_ratios = w / h
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Aspect Ratio Hist
    # Filter extreme outliers for better visualization
    valid_ar = aspect_ratios[aspect_ratios < 5] 
    
    ax1.hist(valid_ar, bins=50, color='#2c3e50', alpha=0.7, edgecolor='black', linewidth=0.5)
    ax1.axvline(1.0, color='r', linestyle='--', alpha=0.5, label='Square')
    ax1.set_title('Aspect Ratio Distribution (W/H)', fontsize=14)
    ax1.set_xlabel('Aspect Ratio', fontsize=12)
    ax1.set_ylabel('Count', fontsize=12)
    ax1.legend()

    # Area Hist (Sqrt Area usually linearizes scale better visually)
    sqrt_area = np.sqrt(areas)
    ax2.hist(sqrt_area, bins=50, color='#e74c3c', alpha=0.7, edgecolor='black', linewidth=0.5)
    ax2.set_title('Object Scale Distribution', fontsize=14)
    ax2.set_xlabel('Square Root of Area (px)', fontsize=12)
    ax2.set_ylabel('Count', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '03_shape_scale_analysis.png'))
    plt.close()
    print("Generated 03_shape_scale_analysis.png")

def plot_scale_vs_position(cx, cy, w, h):
    """Figure 4: Object Scale vs. Vertical Position (Perspective Check)."""
    areas = w * h
    sqrt_area = np.sqrt(areas)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Scatter plot with some transparency
    # We use Center Y because in most camera/radar setups, Y correlates with range (depth)
    sc = ax.scatter(cy, sqrt_area, alpha=0.1, s=3, c='#2980b9', edgecolors='none')
    
    # Add a trend line (polynomial fit)
    z = np.polyfit(cy, sqrt_area, 2)
    p = np.poly1d(z)
    x_trend = np.linspace(min(cy), max(cy), 100)
    ax.plot(x_trend, p(x_trend), 'r--', linewidth=2, label='Trend')

    ax.set_title('Object Scale vs. Vertical Position (Perspective)', fontsize=14)
    ax.set_xlabel('Vertical Position (Center Y) [px]', fontsize=12)
    ax.set_ylabel('Object Scale (Sqrt Area) [px]', fontsize=12)
    ax.legend()
    
    # Add annotation about perspective
    ax.text(0.05, 0.95, 'Top of Image (Far?)', transform=ax.transAxes, 
            verticalalignment='top', fontsize=10, style='italic', bbox=dict(facecolor='white', alpha=0.7))
    ax.text(0.95, 0.95, 'Bottom of Image (Near?)', transform=ax.transAxes, 
            verticalalignment='top', horizontalalignment='right', fontsize=10, style='italic', bbox=dict(facecolor='white', alpha=0.7))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '04_scale_vs_position.png'))
    plt.close()
    print("Generated 04_scale_vs_position.png")

def simple_kmeans(data, k=5, max_iters=100):
    """Simple K-means implementation to avoid sklearn dependency."""
    # Random initialization
    centroids = data[np.random.choice(data.shape[0], k, replace=False)]
    
    for _ in range(max_iters):
        # Assign points to nearest centroid
        distances = np.sqrt(((data - centroids[:, np.newaxis])**2).sum(axis=2))
        labels = np.argmin(distances, axis=0)
        
        # Update centroids
        new_centroids = np.array([data[labels == i].mean(axis=0) for i in range(k)])
        
        if np.all(centroids == new_centroids):
            break
        centroids = new_centroids
        
    return centroids, labels

def plot_kmeans_anchors(w, h):
    """Figure 5: Optimal Anchor Boxes using K-Means."""
    data = np.column_stack((w, h))
    k = 5 # Standard for YOLO
    
    try:
        centroids, labels = simple_kmeans(data, k=k)
        
        # Sort centroids by area
        areas = centroids[:, 0] * centroids[:, 1]
        sorted_indices = np.argsort(areas)
        centroids = centroids[sorted_indices]
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Scatter of all points
        ax.scatter(w, h, alpha=0.05, s=2, c='gray', label='Ground Truth Boxes')
        
        # Draw anchor boxes
        colors = plt.cm.viridis(np.linspace(0, 1, k))
        for i, (cw, ch) in enumerate(centroids):
            rect = plt.Rectangle((0, 0), cw, ch, linewidth=2, edgecolor=colors[i], facecolor='none', 
                                 label=f'Anchor {i+1}: {int(cw)}x{int(ch)}')
            ax.add_patch(rect)
            ax.scatter([cw], [ch], c='red', s=50, zorder=5)

        ax.set_title(f'Optimal Anchor Boxes (K={k})', fontsize=14)
        ax.set_xlabel('Width (pixels)', fontsize=12)
        ax.set_ylabel('Height (pixels)', fontsize=12)
        ax.legend(loc='lower right', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, '05_kmeans_anchors.png'))
        plt.close()
        print("Generated 05_kmeans_anchors.png")
        
    except Exception as e:
        print(f"Skipping K-Means plot due to error: {e}")

if __name__ == "__main__":
    print("Loading data...")
    w, h, cx, cy = load_data()
    
    if len(w) > 0:
        print(f"Processing {len(w)} boxes...")
        plot_spatial_heatmap(cx, cy)
        plot_size_distribution(w, h)
        plot_aspect_ratio_area(w, h)
        plot_scale_vs_position(cx, cy, w, h)
        plot_kmeans_anchors(w, h)
        print(f"All figures saved to {os.path.abspath(OUTPUT_DIR)}")
    else:
        print("No data found! Check csv files.")
