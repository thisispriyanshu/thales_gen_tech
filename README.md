## Deepfake Detection Using Facial and Eye Analysis

# Table of Contents
- [Project Overview](#project-overview)
- [Motivation](#motivation)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Metrics and Evaluation](#metrics-and-evaluation)
- [Limitations and Future Work](#limitations-and-future-work)
- [Contributors](#contributors)
- [References](#references)

---

## Project Overview
This project is a tool designed to detect deepfakes by analyzing facial and eye features, focusing particularly on inconsistencies in reflection patterns within the corneal region of the eyes. The tool uses computer vision techniques, leveraging OpenCV’s Haar Cascade Classifier for detecting faces and eyes in images, and assesses reflection patterns to distinguish real images from GAN-generated deepfakes. This approach provides a low-cost, scalable solution for deepfake detection.

## Motivation
Deepfake technology has advanced rapidly, leading to significant challenges in combating fake media. Hyper-realistic synthetic content is used in various malicious contexts, including:

- **Misinformation and fake news**: Fabricated media can mislead the public on sensitive issues.
- **Financial fraud and impersonation**: Deepfakes enable sophisticated scams and identity theft.
- **Privacy violations**: Individuals are often unknowingly featured in manipulated media.
- **Altered content of public figures**: Politicians, celebrities, and other public figures are frequent targets.

By focusing on subtle inconsistencies, such as variations in eye reflections, this tool aims to provide an effective, efficient method for identifying deepfakes, helping reduce their potential harm.

## Features
- **Face and Eye Detection**: Utilizes OpenCV’s Haar Cascade Classifier to detect faces and eyes in images.
- **Reflection Analysis**: Analyzes reflective patterns in the corneal region, where GAN-generated images often exhibit inconsistencies.
- **Metrics for Deepfake Detection**:
  - **Mean Squared Error (MSE)**: Measures pixel-level differences to detect anomalies.
  - **Structural Similarity Index (SSIM)**: Evaluates similarity based on brightness, contrast, and structure.
  - **Intersection over Union (IoU)**: Measures the overlap between reflective regions in the eyes, with lower scores indicating likely deepfakes.

## Installation
To set up this project, use the following commands to install the necessary packages:

```bash
!pip uninstall -y opencv-python
!pip install opencv-python==3.4.2.17
```
### Dependencies
- Python 3.7+
- OpenCV 3.4.2.17
- NumPy
- PIL (Python Imaging Library)
- Google Colab (recommended for visualization and testing)

### Usage

#### Face and Eye Detection:
- Ensure the XML files for Haar Cascade Classifiers (e.g., `haarcascade_frontalface_default.xml` and `haarcascade_eye.xml`) are available.
- The model identifies faces and eyes, marking these regions and isolating them for detailed analysis.

#### Reflection Pattern Analysis:
- The tool extracts reflective patterns in the eye regions, using saved images of eyes to compare reflective discrepancies between the left and right eyes.

#### Running the Model:
- Load an image and convert it to grayscale.
- Detect faces and eyes using the classifiers provided.
- Visualize the detected regions with `cv2_imshow()` if using Google Colab.

### Example Commands
To visualize detected eyes and save them as individual images:

```python
cv2_imshow(eyes)
cv2.imwrite('eyes.jpg', eyes)
```
### Metrics and Evaluation
The tool applies several metrics to assess the reflective consistency between both eyes:

- **Mean Squared Error (MSE)**: Calculates pixel-wise errors between eye reflection images. Large discrepancies indicate deepfake content.
- **Structural Similarity Index (SSIM)**: Evaluates structural similarity in brightness, contrast, and structure between the eyes. Real images typically show high SSIM values, whereas GAN-generated images tend to yield lower scores.
- **Intersection over Union (IoU)**: Measures the overlap between reflective regions, with lower scores suggesting potential deepfake content.

### Results
Experiments indicate that a combination of SSIM and IoU provides high reliability for deepfake detection. For example, ROC curves created using SSIM scores show strong discrimination between real and GAN-generated content, with AUC values close to 0.9.

### Limitations and Future Work
While effective, the model has certain limitations:

- **Lighting Conditions**: Detection accuracy can vary significantly under different lighting conditions.
- **Occlusions and Background Complexity**: Complex backgrounds and partial occlusions can reduce detection performance.
- **GAN Improvement**: As GANs improve, subtle artifacts may be less detectable with current techniques.

### Future Work:
- Introducing additional metrics for improved detection accuracy.
- Enhancing the model to handle diverse lighting and backgrounds.
- Scaling up to larger datasets to improve robustness.

### Contributors
- Apoorv Yash
- Priyanshu Agarwal
- Yuvraj Singh