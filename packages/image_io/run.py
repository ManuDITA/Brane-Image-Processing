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


def load_image():
    image_path = json.loads(os.environ['IMAGE_PATH'])
    print(image_path)
    print(os.getcwd())
    if(os.path.exists(image_path)):
        print("Image exists")
        return  f"{os.getcwd()}/{image_path} does exist"
    else:
        print("Image does not exist")
        return  f"{image_path} does not exist"


def load_images(input_folder: str):
    """
    Loads all images from the specified input folder.
    
    Args:
        input_folder (str): The folder path containing images.
        
    Returns:
        list: A list of tuples (image_path, image) for each loaded image.
    """
    print("Loading images")
    images = []
    for filename in os.listdir(input_folder):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            image_path = os.path.join(input_folder, filename)
            print(f"Loading image: {filename}")
            image = cv2.imread(image_path)
            if image is not None:
                images.append((image_path, image))
            else:
                print(f"Warning: Could not read image {image_path}")
    return images


def convert_format(image, target_format: str):
    """
    Converts the image to a target format (e.g., PNG to JPG).
    
    Args:
        image: The image to convert.
        target_format (str): The target image format (e.g., 'jpg', 'png').
        
    Returns:
        image: The image in the new format.
    """
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90] if target_format.lower() == 'jpg' else []
    success, encoded_image = cv2.imencode(f'.{target_format}', image, encode_param)
    
    if success:
        return cv2.imdecode(encoded_image, cv2.IMREAD_COLOR)
    else:
        print(f"Error: Could not convert image to {target_format} format.")
        return None

def main():
    command = sys.argv[1]
    
    if command == "load_images":
        images_path = json.loads(os.environ['IMAGES_PATH'])
        #images_path = "images/"
        print(load_images(images_path))


if __name__ == '__main__':
    main()
