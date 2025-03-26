#!/usr/bin/env python3

import cv2
import os
import sys
import json
import socket

def save_image(image, filename: str, output_folder: str):
    """
    Saves the processed image to the output folder with the specified filename.
    
    Args:
        image: The image to save.
        filename (str): The desired filename (including extension).
        output_folder (str): The folder where the image should be saved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_path = os.path.join(output_folder, filename)
    cv2.imwrite(output_path, image)
    print(f"Image saved at {output_path}")

def load_images(input_folder: str):
    """
    Recursively loads all images from the specified input folder and its subfolders,
    and saves them to the specified output folder.

    Args:
        input_folder (str): The folder path containing images and subfolders.
        output_folder (str): The destination folder where images will be saved.
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

def main():
    command = sys.argv[1]
    images_path = json.loads(os.environ['IMAGES_PATH'])
    
    if command == "load_images":
        #images_path = "images/"
        load_images(images_path)

    if command == "convert_format":
        target_format = json.loads(os.environ['TARGET_FORMAT'])
        convert_format(images_path, target_format)

if __name__ == '__main__':
    main()
