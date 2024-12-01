import cv2
import numpy as np

def image_to_polygon_vertices(image_path):
    """
    Converts a segmented image into a list of polygons for each segment.

    :param image_path: Path to the segmented image file.
    :return: A list of lists of (x, y) tuples representing the vertices of each polygon.
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image at {image_path} not found.")

    # Convert to grayscale
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold the grayscale image to create binary masks for each unique segment
    unique_values = np.unique(grayscale)  # Get unique intensity values (segments)
    
    polygons = []

    for value in unique_values:
        # Create a binary mask for the current segment
        mask = cv2.inRange(grayscale, int(value), int(value))

        # Find contours for the current mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            # Approximate the contour to reduce the number of points
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx_vertices = cv2.approxPolyDP(contour, epsilon, True)

            # Convert to a list of (x, y) tuples
            vertices = [(point[0][0], point[0][1]) for point in approx_vertices]
            polygons.append(vertices)

    return polygons

# Example usage
if __name__ == "__main__":
    image_path = "segmented_image.png"  # Replace with the path to your image
    try:
        vertices = image_to_polygon_vertices(image_path)
        print("Polygon vertices:", vertices)
    except (FileNotFoundError, ValueError) as e:
        print(e)