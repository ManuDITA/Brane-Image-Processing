#!/usr/bin/env python3
import cv2
import os
import sys
import json
import csv

def load_images(input_folder: str):
    """
    Recursively loads all images from the specified input folder and its subfolders,
    and saves them to the specified output folder.

    Args:
        input_folder (str): The folder path containing images and subfolders.
    """
    print("Processing images recursively...")
    output_folder = "/result"

    for root, _, files in os.walk(input_folder):  # Recursively walk through directories
        for filename in files:
            if filename.lower().endswith((".jpg", ".png", ".jpeg")):
                image_path = os.path.join(root, filename)
                print(f"Processing image: {image_path}")

                image = cv2.imread(image_path)
                if image is not None:
                    # Save image to result folder with original filename
                    output_path = os.path.join(output_folder, filename)
                    cv2.imwrite(output_path, image)
                    print(f"Saved: {output_path}")
                else:
                    print(f"Warning: Could not read image {image_path}")

    print("Processing complete.")

def convert_format(images_path, target_format: str):
    """
    Converts all images in a folder to a target format (e.g., PNG to JPG).
    
    Args:
        folder_path (str): Path to the folder containing images.
        target_format (str): Target image format (e.g., 'jpg', 'png').
    """
    output_folder = "/result"

    for filename in os.listdir(images_path):
        input_path = os.path.join(images_path, filename)
        
        if os.path.isfile(input_path):
            image = cv2.imread(input_path)
            if image is None:
                print(f"Skipping {filename} (not a valid image)")
                continue
            
            new_filename = f"{os.path.splitext(filename)[0]}.{target_format}"
            output_path = os.path.join(output_folder, new_filename)

            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90] if target_format.lower() == 'jpg' else []
            success, encoded_image = cv2.imencode(f'.{target_format}', image, encode_param)

            if success:
                with open(output_path, "wb") as f:
                    f.write(encoded_image)
                print(f"Converted: {filename} -> {new_filename}")
            else:
                print(f"Error converting {filename} to {target_format}")

def get_image_metadata(image_path):
    """
    Extracts metadata from an image.
    
    Args:
        image_path (str): Path to the image.
    
    Returns:
        dict: Metadata dictionary.
    """
    metadata = {
        "Filename": os.path.basename(image_path),
        "Width": None,
        "Height": None,
        "Format": None
    }

    # Load image with OpenCV
    image = cv2.imread(image_path)
    if image is not None:
        # Get image dimensions
        metadata["Width"], metadata["Height"] = image.shape[1], image.shape[0]
        
        # Get image format (extension based on filename)
        metadata["Format"] = os.path.splitext(image_path)[-1].lower()

    return metadata

def extract_metadata(images_input_folder, output_csv="metadata.csv"):
    """
    Extracts metadata from all images in a folder (recursively) and saves to a CSV file.
    
    Args:
        images_input_folder (str): The folder containing images.
        output_csv (str): Output CSV file path.
    """
    images_metadata = []
    output_folder="/result"
    output_path = os.path.join(output_folder, output_csv)
                        
    for root, _, files in os.walk(images_input_folder):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".tiff", ".bmp", ".gif")):
                print(f"Extracting metadata from: {file}")
                image_path = os.path.join(root, file)
                metadata = get_image_metadata(image_path)
                images_metadata.append(metadata)
    
    # Write to CSV
    if images_metadata:
        with open(output_path, mode="w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=images_metadata[0].keys())
            writer.writeheader()
            writer.writerows(images_metadata)
    
    print(f"Metadata saved to {output_path}")
    

def main():
    command = sys.argv[1]
    images_path = json.loads(os.environ['IMAGES_PATH'])
    
    if command == "load_images":
        load_images(images_path)

    if command == "convert_format":
        target_format = json.loads(os.environ['TARGET_FORMAT'])
        convert_format(images_path, target_format)
        
    if command == "extract_metadata":
        output_csv = json.loads(os.environ['OUTPUT_CSV'])
        extract_metadata(images_path, output_csv)

if __name__ == '__main__':
    main()
