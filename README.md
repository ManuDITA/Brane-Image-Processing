# Brane Image Processing Project

This project is designed to process image datasets using a modular pipeline approach. It consists of two main packages: `image_io` and `image_filters`. Each package is responsible for specific tasks in the image processing pipeline. Below is an explanation of each package and how the pipeline is constructed.

---

## Installation and execution
This section will explain how to get this pipeline up and running. All the commands are relative to this path so make sure to be in this directory when executing the commands.

```bash
cd /path/to/this/dir
```

### 1. Build your dataset
Here we are building our data to make it accessible as dataset to Brane.

```properties
brane data build --no-links ./images/data.yml
```

In case we are making changes to our dataset (adding, removing or modifying images or the path), make sure to regenerate a new dataset by removing the old one and building a new one as shown in the next command. 

```properties
brane data remove data_images && brane data build --no-links /new/path/to/data.yml
```
> **_NOTE:_**  The path to our dataset could be anywhere in our system.

### 2. Build your packages
In this project we have two main packages as described in [Packages](./README.md#packages). In order to use them in our pipeline, we first have to build them:

```properties
brane package build ./packages/image_io/container.yml
brane package build ./packages/image_filters/container.yml
```

Let's execute `brane package list` to see if the packages have been correctly built:
```bash
brane package list
 ID          NAME                  VERSION     KIND        CREATED          SIZE      
 0c4b4d24    image_filters         1.0.0       ecu         2 days ago       440.38 MB 
 3eb2a465    image_io              1.0.0       ecu         27 hours ago     440.38 MB
 ```

As I can see the required packages in the command output, I can finally proceed with running the pipeline

### 3. Run the pipeline
We can now run the pipeline by referring to the pipeline script in our current folder. If everything has been set up correctly, the workflow should start and finish.

```command
brane workflow run image-processing.bs
  Image processing pipeline starting
  Loading dataset (removes dirs and non-image files)
  Converting images in jpg
  Applying gray filter
  Applying blur to grayed images (kernel size=15)
  Detect faces in pictures
  Extract images metadata, save in edited_images.csv
  Commit metadata
  Commit edited images

  Workflow returned value 'Finish'
```

I can then find my results in `~/.local/share/brane/data/metadata_result/data` and `~/.local/share/brane/data/output_data/data`

## Packages
The following packages have been developed for the purpose of this pipeline. They could be expanded to fit additional functionalities of the packages in order to provide more tools and possibilities to researchers. 

### 1. `image_io`
The `image_io` package is responsible for handling input/output operations related to images. It provides functionality to load images, convert their formats, and extract metadata. The key components of this package are:

#### Functions:
- **`load_images(input_folder: str)`**  
  Recursively loads all images from the specified folder dataset. Non-image files are ignored

- **`convert_format(images_path, target_format: str)`**  
  Converts all images from a dataset to a specified format (e.g., PNG to JPG). 

- **`extract_metadata(image_path, output_csv: str)`**  
  Extracts metadata from a dataset and saves it to a CSV file.

---

### 2. `image_filters`
The `image_filters` package provides various image processing filters and transformations. It includes functionality for grayscale conversion, blurring, edge detection, and face detection.

#### Functions:
- **`grayscale_image(images_path)`**  
  Converts a dataset to grayscale and saves the result.

- **`blur_image(images_path, kernel_size=5)`**  
  Applies a Gaussian blur to a dataset with a specified kernel size and saves the result.

- **`edge_detection_image(images_path)`**  
  Detects edges in a dataset using the Canny edge detection algorithm and saves the result.

- **`detect_faces(images_path)`**  
  Detects faces in a dataset using OpenCV's pre-trained Haar cascade model and saves the result with rectangles drawn around detected faces.

---

## Pipeline

The pipeline is defined in the `image-processing.bs` file and orchestrates the tasks provided by the `image_io` and `image_filters` packages. Below is an overview of the pipeline steps:

1. **Load Dataset**  
   The pipeline starts by loading the dataset using the `load_images` action from the `image_io` package. This step removes non-image files and levels all files contained in subdirectories.

2. **Convert Images to JPG**  
   The `convert_format` action is used to convert all images in the dataset to the JPG format.

3. **Apply Grayscale Filter**  
   The `grayscale` action from the `image_filters` package is applied to convert all images to grayscale.

4. **Apply Blur Filter**  
   The `blur` action is applied to the grayscaled images with a kernel size of 15 to create a blurred effect.

5. **Detect Faces**  
   The `face_detection` action is used to detect faces in the blurred images. Detected faces are highlighted with rectangles.

6. **Extract Metadata**  
   The `extract_metadata` action from the `image_io` package is used to extract metadata from the processed images and save it to a CSV file named `edited_images.csv`.

7. **Commit Results**  
   The pipeline commits the metadata and the processed images as results for further use.

---

## Summary

The project is a modular image processing pipeline that leverages the `image_io` and `image_filters` packages to perform a series of transformations and analyses on image datasets. The pipeline is designed to be flexible and extendable, allowing for additional actions or steps to be added as needed.