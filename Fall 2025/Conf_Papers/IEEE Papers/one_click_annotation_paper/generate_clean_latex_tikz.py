#!/usr/bin/env python3
"""
Script to generate a clean LaTeX document with 6-panel TikZ figure showing cropped images 
with bounding boxes drawn using TikZ, without headers or captions for direct import.
"""

import os
import re
from pathlib import Path
import cv2

def parse_bounding_boxes_data(data_file):
    """Parse the bounding box data file to extract coordinates for each frame"""
    with open(data_file, 'r') as f:
        content = f.read()
    
    # Split content into sections by frame ID
    sections = re.split(r'\n\[(\d+)\]\n', content)[1:]  # Remove first empty element
    
    frame_data = {}
    for i in range(0, len(sections), 2):
        frame_id = sections[i]
        bbox_section = sections[i+1]
        
        # Parse bounding boxes for this frame
        bboxes = []
        for line in bbox_section.strip().split('\n'):
            if line.strip() and line.startswith('bbox_'):
                # Extract coordinates from format: bbox_N: xmin,ymin,xmax,ymax
                parts = line.split(':')
                coords = [int(x.strip()) for x in parts[1].split(',')]
                bboxes.append(coords)
        
        frame_data[frame_id] = bboxes
    
    return frame_data

def get_image_dimensions(image_path):
    """Get the dimensions (width, height) of an image"""
    image = cv2.imread(image_path)
    if image is not None:
        height, width = image.shape[:2]
        return width, height
    return None, None

def generate_clean_latex_tikz_figure(processed_data_dir, output_latex_path):
    """Generate a clean LaTeX figure with 6-panel TikZ images and bounding boxes, no text"""
    
    # Parse the bounding box data file
    data_file = os.path.join(processed_data_dir, 'bounding_boxes_data.txt')
    frame_bboxes = parse_bounding_boxes_data(data_file)
    
    # Get list of frame IDs with cropped images
    cropped_dir = os.path.join(processed_data_dir, 'cropped')
    cropped_files = [f for f in os.listdir(cropped_dir) if f.endswith('_all_bboxes_cropped.jpg')]
    
    # Extract frame IDs from filenames
    frame_ids = []
    for cf in cropped_files:
        frame_id = cf.replace('_all_bboxes_cropped.jpg', '')
        if frame_id in frame_bboxes:  # Only include frames that have bounding box data
            frame_ids.append(frame_id)
    
    # Limit to first 6 frames
    selected_frame_ids = frame_ids[:6]
    
    # LaTeX content for a standalone figure
    latex_content = r"""% Clean 6-panel figure with TikZ bounding boxes for import
\documentclass[10pt,a4paper]{article}
\usepackage[margin=0.1in]{geometry} % Minimal margins
\usepackage{graphicx}
\usepackage{subcaption}
\usepackage{tikz}
\usetikzlibrary{calc}

% Remove page numbering and headers
\pagestyle{empty}

\begin{document}

% 6-panel figure with cropped images and TikZ bounding boxes
\centering
"""
    
    # Process each selected frame to create TikZ images
    for idx, frame_id in enumerate(selected_frame_ids):
        # Determine if this is in the first row (1-3) or second row (4-6)
        if idx < 3:  # First row
            if idx == 0:  # First image in row
                latex_content += "\\begin{subfigure}{0.32\\textwidth}\n"
            else:
                latex_content += "\\hfill\n\\begin{subfigure}{0.32\\textwidth}\n"
        else:  # Second row
            if idx == 3:  # First image in second row
                latex_content += "\\vspace{0.1cm}\n\n"  # Add smaller vertical space between rows
                latex_content += "\\begin{subfigure}{0.32\\textwidth}\n"
            else:
                latex_content += "\\hfill\n\\begin{subfigure}{0.32\\textwidth}\n"
        
        # Begin TikZ picture for the image with annotations
        latex_content += "\\centering\n"
        latex_content += "\\begin{tikzpicture}\n"
        
        # Add the cropped image
        cropped_img_path = f"processed_images/cropped/{frame_id}_all_bboxes_cropped.jpg"
        full_img_path = f"/Users/jacobvaught/Downloads/Classes/Fall 2025/Conf_Papers/IEEE Papers/one_click_annotation_paper/{cropped_img_path}"
        
        # Get actual image dimensions
        img_width, img_height = get_image_dimensions(full_img_path)
        if img_width is None or img_height is None:
            print(f"Warning: Could not read image dimensions for {full_img_path}")
            # Use a default approach with the old normalization
            img_width, img_height = 400, 400  # Default values
        
        latex_content += f"\\node[anchor=south west, inner sep=0] (image) at (0,0) {{\\includegraphics[width=\\textwidth]{{{cropped_img_path}}}}};\n"
        latex_content += "\\begin{scope}[x={(image.south east)},y={(image.north west)}]\n"
        
        # Process each bounding box for this frame using actual image dimensions
        for bbox in frame_bboxes[frame_id]:
            xmin, ymin, xmax, ymax = bbox
            
            # Normalize coordinates to [0,1] range based on actual image dimensions
            # In TikZ scope with [x={(image.south east)},y={(image.north west)}],
            # (0,0) is bottom-left and (1,1) is top-right
            # Image coordinates have (0,0) at top-left, so we need to invert Y
            norm_xmin = xmin / img_width
            norm_ymin = 1 - (ymax / img_height)  # Invert y coordinate
            norm_xmax = xmax / img_width
            norm_ymax = 1 - (ymin / img_height)  # Invert y coordinate
            
            latex_content += f"  \\draw[green, thick] ({norm_xmin}, {norm_ymin}) rectangle ({norm_xmax}, {norm_ymax});\n"
        
        latex_content += "\\end{scope}\n"
        latex_content += "\\end{tikzpicture}\n"
        latex_content += "\\end{subfigure}\n"
    
    # Close the figure and document
    latex_content += r"""
\end{document}
"""

    # Write LaTeX content to file
    with open(output_latex_path, 'w') as f:
        f.write(latex_content)
    
    print(f"Clean LaTeX figure generated: {output_latex_path}")
    print(f"Processed frames: {selected_frame_ids}")


if __name__ == "__main__":
    # Define paths
    processed_data_dir = "/Users/jacobvaught/Downloads/Classes/Fall 2025/Conf_Papers/IEEE Papers/one_click_annotation_paper/processed_images"
    output_latex_path = "/Users/jacobvaught/Downloads/Classes/Fall 2025/Conf_Papers/IEEE Papers/one_click_annotation_paper/radar3000_clean_tikz.tex"
    
    # Generate the clean LaTeX figure
    generate_clean_latex_tikz_figure(processed_data_dir, output_latex_path)
    
    print("Clean LaTeX figure with TikZ bounding boxes has been generated successfully!")