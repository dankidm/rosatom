import cv2

def image_to_polygon_vertices(image_path):
    """
    Converts an image with a single polygon into a list of its vertices.

    :param image_path: Path to the image file.
    :return: List of (x, y) tuples representing the vertices of the polygon.
    """
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    
    
    if image is None:
        raise FileNotFoundError(f"Image at {image_path} not found.")
    
    # Threshold the image to create a binary mask
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        raise ValueError("No polygon detected in the image.")
    
    # Assuming the polygon is the largest contour
    polygon_contour = max(contours, key=cv2.contourArea)
    
    # Approximate the contour to get the vertices
    epsilon = 0.01 * cv2.arcLength(polygon_contour, True)  # Adjust approximation precision if needed
    approx_vertices = cv2.approxPolyDP(polygon_contour, epsilon, True)
    
    # Extract vertices as a list of (x, y) tuples
    vertices = [(point[0][0], point[0][1]) for point in approx_vertices]
    
    return vertices

# Example usage
if __name__ == "__main__":
    image_path = "masks/IMG_9208.png"  # Replace with the path to your image
    try:
        vertices = image_to_polygon_vertices(image_path)
        print("Polygon vertices:", vertices)
    except (FileNotFoundError, ValueError) as e:
        print(e)