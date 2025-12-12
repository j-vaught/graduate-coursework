#!/usr/bin/env python3
"""
Script to randomly select 6 images from the radar3000 dataset,
crop them to bounding boxes as squares, and prepare them for LaTeX rendering.
"""

import os
import random
import xml.etree.ElementTree as ET
import cv2
import numpy as np
from pathlib import Path
import shutil

def get_image_list(images_dir):
    """Get list of all image files from the images directory"""
    image_files = []
    for file in os.listdir(images_dir):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_files.append(file)
    return sorted(image_files)

def load_annotations(xml_file):
    """Load bounding box annotations from XML file"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    annotations = []
    for obj in root.findall('object'):
        bndbox = obj.find('bndbox')
        if bndbox is not None:
            xmin = int(float(bndbox.find('xmin').text))
            ymin = int(float(bndbox.find('ymin').text))
            xmax = int(float(bndbox.find('xmax').text))
            ymax = int(float(bndbox.find('ymax').text))
            
            annotations.append({
                'bbox': [xmin, ymin, xmax, ymax],
                'name': obj.find('name').text if obj.find('name') is not None else 'unknown'
            })
    
    return annotations

def crop_to_square_containing_all_bboxes(image, all_bboxes, padding=0.1):
    """Crop image to a square that contains ALL bounding boxes in the image"""
    if not all_bboxes:
        return image, [0, 0, image.shape[1], image.shape[0]]

    # Find the bounding box that contains all individual bounding boxes
    all_xmins = [bbox[0] for bbox in all_bboxes]
    all_ymins = [bbox[1] for bbox in all_bboxes]
    all_xmaxs = [bbox[2] for bbox in all_bboxes]
    all_ymaxs = [bbox[3] for bbox in all_bboxes]

    overall_xmin = min(all_xmins)
    overall_ymin = min(all_ymins)
    overall_xmax = max(all_xmaxs)
    overall_ymax = max(all_ymaxs)

    # Calculate width and height of the overall bounding box
    width = overall_xmax - overall_xmin
    height = overall_ymax - overall_ymin

    # Determine the size of the square (use the larger dimension with padding)
    size = max(width, height)

    # Add padding
    padding_size = int(size * padding)
    size += 2 * padding_size

    # Calculate center of the overall bounding box
    center_x = (overall_xmin + overall_xmax) // 2
    center_y = (overall_ymin + overall_ymax) // 2

    # Calculate square coordinates
    half_size = size // 2
    x1 = max(0, center_x - half_size)
    y1 = max(0, center_y - half_size)
    x2 = min(image.shape[1], center_x + half_size)
    y2 = min(image.shape[0], center_y + half_size)

    # Crop the image
    cropped = image[y1:y2, x1:x2]

    return cropped, [x1, y1, x2, y2]

def process_images_and_annotations(dataset_dir, output_dir, num_images=6):
    """Main function to process images and annotations"""
    # Define paths
    images_dir = os.path.join(dataset_dir, 'Images')
    annotations_dir = os.path.join(dataset_dir, 'Annotations')
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Get list of all images
    all_images = get_image_list(images_dir)
    print(f"Found {len(all_images)} images in the dataset")
    
    # Randomly select num_images images
    selected_images = random.sample(all_images, min(num_images, len(all_images)))
    print(f"Randomly selected {len(selected_images)} images: {selected_images}")
    
    # Process each selected image
    processed_data = []
    
    for img_file in selected_images:
        # Get base filename without extension
        base_name = os.path.splitext(img_file)[0]
        xml_file = base_name + '.xml'
        
        # Construct full paths
        img_path = os.path.join(images_dir, img_file)
        xml_path = os.path.join(annotations_dir, xml_file)
        
        # Check if annotation file exists
        if not os.path.exists(xml_path):
            print(f"Warning: Annotation file {xml_path} does not exist, skipping {img_file}")
            continue
        
        # Load image
        image = cv2.imread(img_path)
        if image is None:
            print(f"Warning: Could not load image {img_path}, skipping")
            continue
        
        # Load annotations
        annotations = load_annotations(xml_path)
        if not annotations:
            print(f"Warning: No annotations found in {xml_path}, skipping")
            continue
        
        # Create a composite image with all bounding boxes for this example
        image_with_boxes = image.copy()

        # Draw all bounding boxes on the image
        all_bboxes = [ann['bbox'] for ann in annotations]
        for annotation in annotations:
            bbox = annotation['bbox']
            # Draw bounding box
            cv2.rectangle(image_with_boxes, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

        # Crop the entire image to a square containing ALL bounding boxes
        cropped_image, actual_bbox = crop_to_square_containing_all_bboxes(image, all_bboxes)

        # Save the original image with bounding boxes drawn
        annotated_img_path = os.path.join(output_dir, f"{base_name}_annotated.jpg")
        cv2.imwrite(annotated_img_path, image_with_boxes)

        # Create directory for cropped images
        cropped_dir = os.path.join(output_dir, 'cropped')
        Path(cropped_dir).mkdir(parents=True, exist_ok=True)

        # Save the cropped image that contains all bounding boxes
        cropped_img_path = os.path.join(cropped_dir, f"{base_name}_all_bboxes_cropped.jpg")
        cv2.imwrite(cropped_img_path, cropped_image)

        # Calculate the adjusted bounding box coordinates relative to the cropped image
        # We need to offset the original coordinates based on the crop location
        adjusted_annotations = []
        for annotation in annotations:
            orig_bbox = annotation['bbox']  # [xmin, ymin, xmax, ymax]
            # Adjust coordinates relative to the crop region
            adjusted_bbox = [
                orig_bbox[0] - actual_bbox[0],  # new xmin
                orig_bbox[1] - actual_bbox[1],  # new ymin
                orig_bbox[2] - actual_bbox[0],  # new xmax
                orig_bbox[3] - actual_bbox[1]   # new ymax
            ]
            # Ensure coordinates are within the cropped image bounds
            adjusted_bbox = [
                max(0, adjusted_bbox[0]),
                max(0, adjusted_bbox[1]),
                min(cropped_image.shape[1], adjusted_bbox[2]),
                min(cropped_image.shape[0], adjusted_bbox[3])
            ]
            adjusted_annotations.append({
                'original_bbox': annotation['bbox'],
                'adjusted_bbox': adjusted_bbox,
                'name': annotation['name']
            })

        processed_data.append({
            'frame_id': base_name,
            'image_path': img_path,
            'annotated_image_path': annotated_img_path,
            'cropped_image_path': cropped_img_path,
            'original_annotations': annotations,
            'adjusted_annotations': adjusted_annotations,
            'crop_coords': actual_bbox  # [x1, y1, x2, y2] of the crop region in the original image
        })
        
        print(f"Processed {img_file} with {len(annotations)} annotations")

    # Save bounding box data for LaTeX
    save_bounding_box_data(processed_data, output_dir)

    return processed_data

def save_bounding_box_data(processed_data, output_dir):
    """Save bounding box data in a format readable by LaTeX"""
    bbox_data_file = os.path.join(output_dir, 'bounding_boxes_data.txt')

    with open(bbox_data_file, 'w') as f:
        f.write("# Bounding box data for LaTeX\n")
        for data in processed_data:
            frame_id = data['frame_id']
            f.write(f"\n[{frame_id}]\n")
            for i, ann in enumerate(data['adjusted_annotations']):
                bbox = ann['adjusted_bbox']
                f.write(f"bbox_{i}: {bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}\n")

    print(f"Bounding box data saved to: {bbox_data_file}")

if __name__ == "__main__":
    # Define dataset and output directories
    dataset_dir = "/Volumes/MacShare/radar3000"
    output_dir = "/Users/jacobvaught/Downloads/Classes/Fall 2025/Conf_Papers/IEEE Papers/one_click_annotation_paper/processed_images"
    
    # Process images and get results
    results = process_images_and_annotations(dataset_dir, output_dir)
    
    print(f"\nProcessed {len(results)} images successfully")
    for result in results:
        print(f"Frame ID: {result['frame_id']}, Found {len(result['original_annotations'])} annotations")