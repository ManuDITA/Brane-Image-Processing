#!/usr/bin/env python3

import cv2
import os
import sys
import json
import yaml
import socket

def list_directory_contents(path="."):
    print(f"Contents of '{path}':")
    print(os.listdir(path))
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            print(f"[DIR]  {item}")  # Mark directories
            print("      └──", os.listdir(item_path))  # Print subdirectory contents
        else:
            print(f"[FILE] {item}")

def grayscale_image(image_path, output_path):

    image = cv2.imread(image_path) 
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(output_path, gray_image)

    
def blur_image(image_path, output_path, kernel_size=5):

    if kernel_size % 2 == 0:
        kernel_size += 1  # Make it odd
    if kernel_size <= 0:
        kernel_size = 1   # Set a default valid value
    image = cv2.imread(image_path)
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    cv2.imwrite(output_path, blurred_image)

def main():
    command = sys.argv[1]
    source_images_path = json.loads(os.environ['IMAGE_PATH'])
    result_folder = "/result"
    
    if command == "grayscale":
        #loading a dataset folder path now. It is a folder with images inside
        print("Applying grayscale filter to dataset")
        
        for filename in os.listdir(source_images_path):
            image_path = os.path.join(source_images_path, filename)
            if os.path.isfile(image_path):
                image_output_path = os.path.join(result_folder, f"grayscaled_{filename}")
                print(f"Applying grayscale filter to {image_path}")
                grayscale_image(image_path, image_output_path)
                
        return result_folder
    
    if command == "blur":
        
        print("Applying blur filter to dataset")
        kernel_size = json.loads(os.environ['KERNEL_SIZE'])

        for filename in os.listdir(source_images_path):
            image_path = os.path.join(source_images_path, filename)
            if os.path.isfile(image_path):
                image_output_path = os.path.join(result_folder, f"blurred_{filename}")
                print(f"Applying grayscale filter to {image_path}")
                blur_image(image_path, image_output_path, kernel_size)

    #print(yaml.dump({"output": output_path}))

if __name__ == '__main__':
    main()
