#!/usr/bin/env python3
"""
Script to generate a clean LaTeX figure showing samples from the in-house dataset in a 2x3 grid format.
"""

import os
import re
from pathlib import Path
import cv2

def get_short_location_name(filepath):
    """Extract a short location name from the filepath"""
    # Extract the folder name to use as location identifier
    path_parts = Path(filepath).parts
    for part in path_parts:
        if 'MurrayDam' in part:
            return 'MDam'
        elif 'GriceLab' in part:
            return 'GLab'
        elif 'FollyBeach' in part:
            return 'FBch'
        elif 'PortsmouthCityPark' in part:
            return 'PCpk'
        elif 'LakeMonticello' in part:
            return 'LMnl'
        elif 'GreenwoodPark' in part:
            return 'GwdP'
    return 'Site'

def generate_house_dataset_figure(image_paths, output_latex_path):
    """Generate a LaTeX figure showing samples from the in-house dataset in a 2x3 grid format"""
    
    # LaTeX content for a standalone figure
    latex_content = r"""% Sample frames from in-house dataset
\documentclass[border=2pt]{standalone}
\usepackage{graphicx}
\usepackage{tikz}
\usetikzlibrary{calc}

\begin{document}

\begin{tikzpicture}
% Position the first row of images
"""
    
    # Define the image paths
    selected_images = image_paths
    
    # Process first row (images 0, 1, 2)
    for idx in range(min(3, len(selected_images))):
        img_path = selected_images[idx]
        
        # Get a short location name for the label
        short_name = get_short_location_name(img_path)
        
        # Extract the timestamp from the filename
        filename = Path(img_path).stem
        # Extract timestamp part (first part before '_trail')
        timestamp_part = filename.split('_trail')[0]
        # Take last 6 digits of timestamp for brevity
        if '_' in timestamp_part:
            parts = timestamp_part.split('_')
            if len(parts) >= 2:
                time_part = parts[-2][-6:]  # Last 6 digits of the time
            else:
                time_part = timestamp_part[-6:]  # Last 6 chars of the whole thing
        else:
            time_part = timestamp_part[-6:]
        
        # Position the images side by side in the first row
        x_pos = idx * 3.5  # Adjust spacing as needed
        y_pos = 0  # First row
        
        latex_content += f"\\node[anchor=north west, inner sep=0] (img{idx}) at ({x_pos},{y_pos}) {{\\includegraphics[width=3cm]{{{img_path}}}}};\n"
        # Add short location timestamp labels below the image
        latex_content += f"\\node[anchor=north] at (img{idx}.south) {{\\small {short_name}-{time_part}}};\n"

    # Process second row (images 3, 4, 5)
    for idx in range(3, min(6, len(selected_images))):
        img_path = selected_images[idx]
        
        # Get a short location name for the label
        short_name = get_short_location_name(img_path)
        
        # Extract the timestamp from the filename
        filename = Path(img_path).stem
        # Extract timestamp part (first part before '_trail')
        timestamp_part = filename.split('_trail')[0]
        # Take last 6 digits of timestamp for brevity
        if '_' in timestamp_part:
            parts = timestamp_part.split('_')
            if len(parts) >= 2:
                time_part = parts[-2][-6:]  # Last 6 digits of the time
            else:
                time_part = timestamp_part[-6:]  # Last 6 chars of the whole thing
        else:
            time_part = timestamp_part[-6:]
        
        # Position the images side by side in the second row
        x_pos = (idx - 3) * 3.5  # Adjust spacing as needed, starting from 0 again
        y_pos = -4  # Second row, positioned below the first row
        
        latex_content += f"\\node[anchor=north west, inner sep=0] (img{idx}) at ({x_pos},{y_pos}) {{\\includegraphics[width=3cm]{{{img_path}}}}};\n"
        # Add short location timestamp labels below the image
        latex_content += f"\\node[anchor=north] at (img{idx}.south) {{\\small {short_name}-{time_part}}};\n"

    latex_content += "\\end{tikzpicture}\n"
    
    # Close the document
    latex_content += r"""

\end{document}
"""

    # Write LaTeX content to file
    with open(output_latex_path, 'w') as f:
        f.write(latex_content)
    
    print(f"House dataset figure LaTeX generated: {output_latex_path}")
    print(f"Processed {len(selected_images)} images")


if __name__ == "__main__":
    # Define the image paths from the user's request
    image_paths = [
        "/Volumes/MacShare/Trail_data/MurrayDam_20250812_1008_2_GainRamping_40_70_None/20250812_103025_801_50_2_trail_10.png",
        "/Volumes/MacShare/Trail_data/GriceLab_20251026_1608_7_Constant_100_100_Interference/20251026_170349_630_100_7_trail_10.png",
        "/Volumes/MacShare/Trail_data/FollyBeach_20250820_1329_5_Constant_91_91_None/20250820_132956_197_91_5_trail_10.png",
        "/Volumes/MacShare/Trail_data/PortsmouthCityPark_20251029_1751_4_Constant_99_99_None/20251029_175807_896_70_4_trail_10.png",
        "/Volumes/MacShare/Trail_data/LakeMonticello_20250813_1350_0_Constant_40_75_None/20250813_140929_180_50_0_trail_10.png",
        "/Volumes/MacShare/Trail_data/GreenwoodPark_20251107_1724_4_Pulse_70_72_None/20251107_172844_337_71_4_trail_10.png"
    ]
    
    # Define output path
    output_latex_path = "/Users/jacobvaught/Downloads/Classes/Fall 2025/Conf_Papers/IEEE Papers/one_click_annotation_paper/house_dataset_samples.tex"
    
    # Generate the figure
    generate_house_dataset_figure(image_paths, output_latex_path)
    
    print("House dataset figure with 2x3 layout has been generated successfully!")