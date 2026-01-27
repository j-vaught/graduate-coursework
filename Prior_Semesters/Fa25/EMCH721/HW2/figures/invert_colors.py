from PIL import Image, ImageOps
import os

# Define the directory
directory = "/Users/jacobvaught/Library/CloudStorage/OneDrive-UniversityofSouthCarolina/Classes/Fall 2025/EMCH_721/HW2/JCV/figures"

# List of images to invert (B5 through F)
images_to_process = [
    "B5.1.png", "B5.2.png",
    "C5ae.png", "C5f.png",
    "D2.png", "D3ae.png", "D3d1.png", "D3d2.png", "D3d3.png", "D3d4.png", "D3d5.png",
    "E2.png", "E3ac.png", "E3d1.png", "E3d2.png", "E3d3.png", "E3d4.png", "E3d5.png",
    "F1ad.png", "F1e.png"
]

for image_name in images_to_process:
    # Full path to the original image
    original_path = os.path.join(directory, image_name)
    
    # Check if the image exists
    if os.path.exists(original_path):
        # Open the image
        image = Image.open(original_path)
        
        # Invert the colors
        inverted_image = ImageOps.invert(image.convert('RGB'))
        
        # Create the new filename with "inverted_" prefix
        name, ext = os.path.splitext(image_name)
        new_filename = f"inverted_{name}{ext}"
        new_path = os.path.join(directory, new_filename)
        
        # Save the inverted image
        inverted_image.save(new_path)
        print(f"Saved inverted image: {new_filename}")
    else:
        print(f"Image not found: {image_name}")

print("All images processed successfully!")