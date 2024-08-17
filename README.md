# 📏 Length Measurement with OpenCV

Welcome to the **Length Measurement** project! This repository contains a Python-based solution that uses OpenCV to detect objects in images or video streams and measure their dimensions in real-time. This tool is particularly useful for applications in automated inspection, material measurement, and any scenario where precise length measurement is required.

## 🧰 Technologies Used

This project utilizes the following technologies:

- **Python** 🐍: The programming language used to develop the project.
- **OpenCV (`cv2`)** 📷: An open-source computer vision library used for image and video processing, contour detection, and drawing.
- **NumPy (`np`)** 🔢: A fundamental package for numerical computations in Python, used here for mathematical operations and array manipulations.
- **Custom Utility Functions** 🛠️: Helper functions like `getContours`, `warpImg`, `reorder`, and `findDist` for image processing and measurement.

## 🚀 Features

- **Object Contour Detection**: Identify the contours of objects within an image or video frame.
- **Perspective Transformation**: Warp the detected object to correct its perspective for accurate measurement.
- **Real-Time Measurement**: Measure the width and height of the detected object in centimeters, displayed in real-time.
- **Scalability**: The tool scales the measurement based on the provided scale factor, making it adaptable to various object sizes.
- **Interactive Visualization**: Draws polylines and arrows on the detected objects to visually represent the dimensions.

## 🗂️ Project Structure

Here's a brief overview of the main components in this project:

- **`main.py`**: The main script that runs the length measurement logic using OpenCV.
- **`test1.py`**: A helper script containing utility functions for contour detection, image warping, and point reordering.

## 📝 How to Use

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/length-measurement.git
    cd length-measurement
    ```

2. **Install the required libraries**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the script**:
    ```bash
    python object_length_measurement.py
    ```

4. **Input Configuration**:
    - **Webcam**: Set `webcam = True` in the script to use live video from your webcam.
    - **Image**: Set `webcam = False` and provide the image path in the `path` variable to measure dimensions in a static image.

5. **Adjusting the Scale**:
    - Modify the `scale` variable to adjust the measurement scale according to your object's size.

## 📸 Example Output

![Example Output](path_to_example_image.png)

## ⚙️ Customization

You can customize the following parameters:

- **`minArea`**: Minimum area of contours to consider for measurement.
- **`filter`**: Number of vertices in the contour to filter for specific shapes.
- **`cThr`**: Thresholds for contour detection.
- **`scale`**: Scale factor to adjust the measurement according to the actual size of objects.

## 🖼️ Visual Representation

- **Polylines**: Green polylines are drawn around detected objects.
- **Arrows**: Pink arrows show the width and height being measured.
- **Dimension Labels**: The dimensions are displayed in centimeters on the image.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue if you have any suggestions, improvements, or bug reports.

---

✨ Happy coding! ✨
