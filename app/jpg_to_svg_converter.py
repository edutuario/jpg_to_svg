import cv2
import os
import subprocess

def convert_image_to_svg(image_path, output_name, threshold=110, output_dir=None):
    """
    Converts an image to an SVG using OpenCV, ImageMagick, and Potrace.

    Args:
        image_path (str): Path to the input image.
        output_name (str): Name of the output file (without extension).
        threshold (int): Threshold value for binarization (default: 110).
            - Any pixel with an intensity **above** this value becomes **white (255)**.
            - Any pixel with an intensity **below** this value becomes **black (0)**.
        output_dir (str, optional): Directory to save output files. Defaults to the input image's directory.

    Returns:
        str: Path to the generated SVG file.
    
    Explanation:
        - The `threshold` parameter controls how dark or light the final image appears.
          A **lower** threshold (e.g., 50) makes more areas **white**.
          A **higher** threshold (e.g., 180) makes more areas **black**.
        - The `255` value in `cv2.threshold()` is the **maximum intensity** assigned to white pixels.
          It ensures that the binary image consists of only two values: **0 (black) and 255 (white)**.
    """
    if output_dir is None:
        output_dir = os.path.dirname(image_path)

    # Load and process image
    original_image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    _, bw_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)

    # Save processed image
    bw_path = os.path.join(output_dir, f"{output_name}.jpeg")
    cv2.imwrite(bw_path, bw_image)

    # Convert to PBM
    pbm_path = os.path.join(output_dir, f"{output_name}.pbm")
    subprocess.run(["magick", bw_path, pbm_path], check=True)

    # Convert PBM to SVG using Potrace
    subprocess.run(["potrace", "-s", pbm_path], check=True)

    svg_path = os.path.join(output_dir, f"{output_name}.svg")
    return svg_path