#!/usr/bin/env python3
"""
Steganalysis of page illustrations - pages 8-14, 32, 55.
Replicate the analysis from ruled-out.md for page 74:
1. Connected-component analysis
2. Nearest-neighbor spacing analysis
"""

import sys, json, pathlib
import cv2
import numpy as np
from sklearn.neighbors import NearestNeighbors

def analyze_image(image_path):
    """Run steganalysis on a single page image."""
    # Load image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return {"error": f"Could not load {image_path}"}
    
    h, w = img.shape
    
    # Threshold to isolate dark pixels (ink/dots)
    _, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
    
    # Connected component analysis
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
    
    # Filter out background (label 0) and very large components (likely text blocks)
    component_sizes = stats[1:, cv2.CC_STAT_AREA]  # exclude background
    component_centroids = centroids[1:]
    
    # Filter: keep only small components (likely dots/stippling)
    # Page 74 analysis found sizes 517-620 for "trunk" components
    # Let's filter to find small dot-like components
    small_components = component_sizes[(component_sizes > 1) & (component_sizes < 1000)]
    small_centroids = component_centroids[(component_sizes > 1) & (component_sizes < 1000)]
    
    # Nearest neighbor analysis
    if len(small_centroids) > 1:
        nbrs = NearestNeighbors(n_neighbors=2, metric='euclidean').fit(small_centroids)
        distances, _ = nbrs.kneighbors(small_centroids)
        # distances[:, 1] is distance to nearest neighbor (excluding self)
        nn_distances = distances[:, 1]
        nn_mean = np.mean(nn_distances)
        nn_std = np.std(nn_distances)
        nn_hist, nn_bins = np.histogram(nn_distances, bins=20, range=(0, 100))
    else:
        nn_mean = nn_std = 0
        nn_hist = []
        nn_bins = []
    
    # Also analyze larger components (potential text/structure)
    large_components = component_sizes[component_sizes >= 1000]
    
    return {
        "image": image_path,
        "dimensions": f"{w}x{h}",
        "total_components": num_labels - 1,
        "small_components_count": len(small_components),
        "large_components_count": len(large_components),
        "small_size_mean": float(np.mean(small_components)) if len(small_components) > 0 else 0,
        "small_size_std": float(np.std(small_components)) if len(small_components) > 0 else 0,
        "small_size_range": f"{np.min(small_components)}-{np.max(small_components)}" if len(small_components) > 0 else "N/A",
        "nn_distance_mean": float(nn_mean) if len(nn_distances) > 0 else 0,
        "nn_distance_std": float(nn_std) if len(nn_distances) > 0 else 0,
        "nn_histogram": nn_hist.tolist() if len(nn_hist) > 0 else [],
        "nn_bins": nn_bins.tolist() if len(nn_bins) > 0 else [],
    }

def main():
    pages_dir = '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/pages'
    
    # Target pages from open-leads.md: 8-14, 32, 55
    target_pages = list(range(8, 15)) + [32, 55]
    
    results = {}
    
    for page_num in target_pages:
        # Find the file (might be 8.jpg or 08.jpg)
        img_path = None
        for ext in ['.jpg', '.png']:
            for name in [f"{page_num}{ext}", f"{page_num:02d}{ext}"]:
                path = f"{pages_dir}/{name}"
                import os
                if os.path.exists(path):
                    img_path = path
                    break
            if img_path:
                break
        
        if img_path is None:
            print(f"Page {page_num}: NOT FOUND")
            results[page_num] = {"error": "Image not found"}
            continue
        
        print(f"Analyzing page {page_num} ({img_path})...")
        result = analyze_image(img_path)
        results[page_num] = result
        
        if "error" not in result:
            print(f"  Components: {result['total_components']} total, "
                  f"{result['small_components_count']} small, "
                  f"{result['large_components_count']} large")
            print(f"  Small sizes: {result['small_size_range']}, "
                  f"mean={result['small_size_mean']:.1f} std={result['small_size_std']:.1f}")
            print(f"  NN distance: mean={result['nn_distance_mean']:.2f} "
                  f"std={result['nn_distance_std']:.2f}")
        else:
            print(f"  Error: {result['error']}")
        print()
    
    # Save results
    output_path = pathlib.Path('/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/experiments/2026-09-24/steganalysis.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {output_path}")

if __name__ == '__main__':
    main()