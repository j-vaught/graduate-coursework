#!/usr/bin/env python3
"""
Script to generate a clean LaTeX document with 6-panel figure showing cropped images 
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
    """Generate a clean LaTeX figure with 6-panel images and TikZ bounding boxes, no text"""
    
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
\documentclass[border=2pt]{standalone}
\usepackage{graphicx}
\usepackage{tikz}
\usetikzlibrary{calc}

\begin{document}

\begin{tikzpicture}
% Position the first row of images
"""

    # Process first row (images 0, 1, 2)
    for idx in range(min(3, len(selected_frame_ids))):
        frame_id = selected_frame_ids[idx]
        cropped_img_path = f"processed_images/cropped/{frame_id}_all_bboxes_cropped.jpg"
        full_img_path = f"/Users/jacobvaught/Downloads/Classes/Fall 2025/Conf_Papers/IEEE Papers/one_click_annotation_paper/{cropped_img_path}"

        # Get actual image dimensions
        img_width, img_height = get_image_dimensions(full_img_path)
        if img_width is None or img_height is None:
            print(f"Warning: Could not read image dimensions for {full_img_path}")
            img_width, img_height = 400, 400  # Default values

        # Position the images side by side in the first row
        x_pos = idx * 3.5  # Adjust spacing as needed
        y_pos = 0  # First row

        latex_content += f"\\node[anchor=north west, inner sep=0] (img{idx}) at ({x_pos},{y_pos}) {{\\includegraphics[width=3cm]{{{cropped_img_path}}}}};\n"
        latex_content += f"\\begin{{scope}}[shift={{(img{idx}.south west)}}]\n"

        # Process each bounding box for this frame using actual image dimensions
        for bbox in frame_bboxes[frame_id]:
            xmin, ymin, xmax, ymax = bbox

            # Calculate actual coordinates based on image size and node position
            # The image is scaled to 3cm width, and height is calculated based on aspect ratio
            width_scale = 3.0  # width of the image in cm
            height_scale = (img_height / img_width) * 3.0  # height based on aspect ratio

            # Convert original image coordinates to the scaled image coordinates
            scaled_xmin = (xmin / img_width) * width_scale
            scaled_ymin = (ymin / img_height) * height_scale
            scaled_xmax = (xmax / img_width) * width_scale
            scaled_ymax = (ymax / img_height) * height_scale

            # In TikZ with the shift={(imgX.south west)}, the origin (0,0) is at the bottom-left
            # of the image. The y-axis increases upward (opposite to image coordinates).
            # So we need to flip the Y coordinates relative to the image height
            # Convert image coordinates (top-left origin) to TikZ coordinates (bottom-left origin)
            tikz_ymin = height_scale - scaled_ymax  # Note: swapping max and min due to coordinate flip
            tikz_ymax = height_scale - scaled_ymin  # Note: swapping max and min due to coordinate flip

            latex_content += f"  \\draw[green, thick] ({scaled_xmin}cm, {tikz_ymin}cm) rectangle ({scaled_xmax}cm, {tikz_ymax}cm);\n"

        latex_content += "\\end{scope}\n"
        # Add frame ID labels (ID: XXXX format) below the image
        latex_content += f"\\node[anchor=north] at (img{idx}.south) {{\\small ID: {frame_id}}};\n"

    # Process second row (images 3, 4, 5)
    for idx in range(3, min(6, len(selected_frame_ids))):
        frame_id = selected_frame_ids[idx]
        cropped_img_path = f"processed_images/cropped/{frame_id}_all_bboxes_cropped.jpg"
        full_img_path = f"/Users/jacobvaught/Downloads/Classes/Fall 2025/Conf_Papers/IEEE Papers/one_click_annotation_paper/{cropped_img_path}"

        # Get actual image dimensions
        img_width, img_height = get_image_dimensions(full_img_path)
        if img_width is None or img_height is None:
            print(f"Warning: Could not read image dimensions for {full_img_path}")
            img_width, img_height = 400, 400  # Default values

        # Position the images side by side in the second row
        x_pos = (idx - 3) * 3.5  # Adjust spacing as needed, starting from 0 again
        y_pos = -4  # Second row, positioned below the first row

        latex_content += f"\\node[anchor=north west, inner sep=0] (img{idx}) at ({x_pos},{y_pos}) {{\\includegraphics[width=3cm]{{{cropped_img_path}}}}};\n"
        latex_content += f"\\begin{{scope}}[shift={{(img{idx}.south west)}}]\n"

        # Process each bounding box for this frame using actual image dimensions
        for bbox in frame_bboxes[frame_id]:
            xmin, ymin, xmax, ymax = bbox

            # Calculate actual coordinates based on image size and node position
            # The image is scaled to 3cm width, and height is calculated based on aspect ratio
            width_scale = 3.0  # width of the image in cm
            height_scale = (img_height / img_width) * 3.0  # height based on aspect ratio

            # Convert original image coordinates to the scaled image coordinates
            scaled_xmin = (xmin / img_width) * width_scale
            scaled_ymin = (ymin / img_height) * height_scale
            scaled_xmax = (xmax / img_width) * width_scale
            scaled_ymax = (ymax / img_height) * height_scale

            # In TikZ with the shift={(imgX.south west)}, the origin (0,0) is at the bottom-left
            # of the image. The y-axis increases upward (opposite to image coordinates).
            # So we need to flip the Y coordinates relative to the image height
            # Convert image coordinates (top-left origin) to TikZ coordinates (bottom-left origin)
            tikz_ymin = height_scale - scaled_ymax  # Note: swapping max and min due to coordinate flip
            tikz_ymax = height_scale - scaled_ymin  # Note: swapping max and min due to coordinate flip

            latex_content += f"  \\draw[green, thick] ({scaled_xmin}cm, {tikz_ymin}cm) rectangle ({scaled_xmax}cm, {tikz_ymax}cm);\n"

        latex_content += "\\end{scope}\n"
        # Add frame ID labels (ID: XXXX format) below the image
        latex_content += f"\\node[anchor=north] at (img{idx}.south) {{\\small ID: {frame_id}}};\n"

    latex_content += "\\end{tikzpicture}\n"
    
    # Close the document
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