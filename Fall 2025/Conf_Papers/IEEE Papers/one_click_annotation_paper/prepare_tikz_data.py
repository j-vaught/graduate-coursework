import csv
import numpy as np
import os
import pandas as pd

OUTPUT_DIR = 'tikz_data'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def load_data():
    widths, heights = [], []
    cx, cy = [], []
    
    # Load Sizes
    if os.path.exists('bbox_sizes.csv'):
        df = pd.read_csv('bbox_sizes.csv')
        widths = df['width'].values
        heights = df['height'].values
    
    # Load Centers
    if os.path.exists('bbox_centers.csv'):
        df = pd.read_csv('bbox_centers.csv')
        cx = df['center_x'].values
        cy = df['center_y'].values
        
    return widths, heights, cx, cy

def export_heatmap_data(cx, cy):
    # Create a 20x20 bin heatmap (lightweight for LaTeX)
    H, xedges, yedges = np.histogram2d(cx, cy, bins=25, density=True)
    
    # PGFPlots expects matrix format or x,y,z
    with open(os.path.join(OUTPUT_DIR, 'heatmap_matrix.csv'), 'w') as f:
        f.write('x,y,c\n')
        # Use bin centers
        x_centers = (xedges[:-1] + xedges[1:]) / 2
        y_centers = (yedges[:-1] + yedges[1:]) / 2
        
        for i in range(len(x_centers)):
            for j in range(len(y_centers)):
                # Invert Y for image coords if needed, usually PGFPlots handles axes
                # We'll just dump raw
                f.write(f'{x_centers[i]},{y_centers[j]},{H[i,j]}\n')
    print("Exported heatmap_matrix.csv")

def export_hist_data(w, h):
    # 1. Aspect Ratio
    ar = w / (h + 1e-6)
    ar = ar[ar < 4] # Clip extreme outliers for plot clarity
    hist_ar, bins_ar = np.histogram(ar, bins=30)
    centers_ar = (bins_ar[:-1] + bins_ar[1:]) / 2
    
    pd.DataFrame({'x': centers_ar, 'y': hist_ar}).to_csv(
        os.path.join(OUTPUT_DIR, 'hist_aspect_ratio.csv'), index=False)
        
    # 2. Scale (Sqrt Area)
    scale = np.sqrt(w * h)
    hist_sc, bins_sc = np.histogram(scale, bins=30)
    centers_sc = (bins_sc[:-1] + bins_sc[1:]) / 2
    
    pd.DataFrame({'x': centers_sc, 'y': hist_sc}).to_csv(
        os.path.join(OUTPUT_DIR, 'hist_scale.csv'), index=False)
    
    print("Exported hist_aspect_ratio.csv and hist_scale.csv")

def simple_kmeans(data, k=5):
    centroids = data[np.random.choice(data.shape[0], k, replace=False)]
    for _ in range(50):
        dists = np.sqrt(((data - centroids[:, np.newaxis])**2).sum(axis=2))
        labels = np.argmin(dists, axis=0)
        new_centroids = np.array([data[labels == i].mean(axis=0) for i in range(k)])
        if np.all(centroids == new_centroids): break
        centroids = new_centroids
    return centroids

def export_anchors_data(w, h):
    # 1. Background Scatter (Downsample to 2000 points for PDF speed)
    N = len(w)
    mask = np.random.choice(N, min(N, 2000), replace=False)
    pd.DataFrame({'w': w[mask], 'h': h[mask]}).to_csv(
        os.path.join(OUTPUT_DIR, 'scatter_downsampled.csv'), index=False)
        
    # 2. Centroids (Anchors)
    data = np.column_stack((w, h))
    anchors = simple_kmeans(data, k=5)
    # Sort by area
    anchors = anchors[np.argsort(anchors[:,0] * anchors[:,1])]
    
    pd.DataFrame({'w': anchors[:,0], 'h': anchors[:,1]}).to_csv(
        os.path.join(OUTPUT_DIR, 'anchors_centroids.csv'), index=False)
        
    print("Exported scatter_downsampled.csv and anchors_centroids.csv")

if __name__ == "__main__":
    w, h, cx, cy = load_data()
    if len(w) > 0:
        export_heatmap_data(cx, cy)
        export_hist_data(w, h)
        export_anchors_data(w, h)
