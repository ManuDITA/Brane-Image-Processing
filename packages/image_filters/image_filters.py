#!/usr/bin/env python3

import cv2
import os
import sys
import json
import yaml
import socket

def edge_detection_image(image_path, output_path, threshold1=100, threshold2=200):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale first
    edges = cv2.Canny(image, threshold1, threshold2)
    cv2.imwrite(output_path, edges)

def detect_faces(image_path, output_path, scale_factor=1.1, min_neighbors=5):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load OpenCV's pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=min_neighbors, minSize=(30, 30))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Save the output image
    cv2.imwrite(output_path, image)

    print(f"Detected {len(faces)} faces in {image_path}. Output saved at {output_path}.")


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
    source_images_path = json.loads(os.environ['IMAGES_PATH'])
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
                
    if command == "edge_detection":
        
        print("Applying edge detection to dataset")

        for filename in os.listdir(source_images_path):
            image_path = os.path.join(source_images_path, filename)
            if os.path.isfile(image_path):
                image_output_path = os.path.join(result_folder, f"edge_detected_{filename}")
                print(f"Applying edge_detection filter to {image_path}")
                edge_detection_image(image_path, image_output_path)

    if command == "face_detection":
        
        print("Applying face detection to dataset")

        for filename in os.listdir(source_images_path):
            image_path = os.path.join(source_images_path, filename)
            if os.path.isfile(image_path):
                image_output_path = os.path.join(result_folder, f"face_detected_{filename}")
                print(f"Applying face_detection filter to {image_path}")
                detect_faces(image_path, image_output_path)

    #print(yaml.dump({"output": output_path}))

if __name__ == '__main__':
    main()
