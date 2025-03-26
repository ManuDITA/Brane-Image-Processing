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

    
def blur(image_path, output_path, kernel_size=5):

    image = cv2.imread(image_path)
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    cv2.imwrite(output_path, blurred_image)

def main():
    command = sys.argv[1]
    
    if command == "grayscale":
        images_path = json.loads(os.environ['IMAGE_PATH'])

        output_path = f"/result/grayscaled_{os.path.basename(images_path)}"
        print("Applying grayscale filter")
        print(os.listdir('.'))
        print(os.listdir('images/data'))
        grayscale_image(images_path, output_path)

    
    if command == "blur":
        images_path = json.loads(os.environ['IMAGE_PATH'])
        output_path = f"/result/blurred_{os.path.basename(images_path)}"
        print("Applying blur filter")
        blur(images_path, output_path)

    print(yaml.dump({"output": output_path}))

if __name__ == '__main__':
    main()
