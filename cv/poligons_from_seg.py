import cv2
import numpy as np

def image_to_polygon_vertices(image_path):
    """
    Converts a segmented image into a list of polygons for each segment.

    :param image_path: Path to the segmented image file.
    :return: A list of lists of (x, y) tuples representing the vertices of each polygon.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image at {image_path} not found.")

    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    unique_values = np.unique(grayscale) 
    
    polygons = []

    for value in unique_values:
        mask = cv2.inRange(grayscale, int(value), int(value))

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx_vertices = cv2.approxPolyDP(contour, epsilon, True)

            vertices = [(point[0][0], point[0][1]) for point in approx_vertices]
            polygons.append(vertices)

    return polygons


if __name__ == "__main__":
    IMAGE_PATH = "" 
    try:
        vertices = image_to_polygon_vertices(IMAGE_PATH)
        print("Polygon vertices:", vertices)
    except (FileNotFoundError, ValueError) as e:
        print(e)