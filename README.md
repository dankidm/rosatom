# Car Image Segmentation Backend

This README describes a Flask backend for processing and segmenting car images.

## Introduction

This API allows uploading base64 encoded images and receives a JSON response containing segmented information. It leverages a pre-trained model for car type detection and utilizes a segmentation pipeline for isolating various parts of the car.


## Technologies Used

* **Python:** Programming language
* **Flask:** Web framework
* **Base64:** Encoding for image transfer
* **Hashlib:** Secure hashing for image identification
* **OS:** File system operations
* **car_classification:** Custom module for car type detection
* **img_to_segments:** Custom module for segmentation processing.
* **poligons_from_seg:** Custom module to extract polygon coordinates from segmentation masks.
* **segment_interface:** Custom module that handles the image preprocessing steps needed for the segmentation algorithm.

## Directory Structure
*todo*
## API Endpoints

### `/` (POST) - Image Upload and Processing

* **Request:**
    * `Content-Type: application/json`
    * `image` (required): Base64 encoded image.
* **Response:**
    * `200 OK`: Successfully uploaded and processing started.  Returns the `image_hash` to identify the processed image.
    * `400 Bad Request`: If no image is provided.
    * `500 Internal Server Error`: For any processing errors.  Includes a descriptive error message in the response body.

### `/` (GET) - Retrieve all processed image hashes

* **Request:**
    * `GET`
* **Response:**
    * `200 OK`: Returns a JSON array of all successfully processed image hashes.


### `/<image_id>/status` (GET) - Processing Status

* **Request:**
    * `GET` on a specific `image_id`.
* **Response:**
    * `200 OK`: Returns the processing status (e.g., "Uploaded", "Processing", "Ready", "Error").  Includes a descriptive error message if the status is "Error".
    * `404 Not Found`: If the image ID is not found in the `processing_status` dictionary.

### `/<image_id>/segments` (GET) - Get Segmentation Results

* **Request:**
    * `GET` on a specific `image_id`.
* **Response:**
    * `200 OK`: Returns a JSON object containing the extracted segments with polygon coordinates, keyed by the segment name.
    * `400 Bad Request`: If processing is still ongoing.
    * `404 Not Found`: If the image ID is not found or no segmentation is completed yet.


## Data Structures

* **`processing_status` (dict):** Stores the processing status of each uploaded image (`image_hash`). Possible values are "Uploaded", "Processing", "Ready", or "Error". Includes a message field to communicate any errors.
* **`processed_segments` (dict):** Stores the processed segmentation results for each image.  Keys are `image_hash`. Values are a dictionary where keys are the segment file names and values are the polygon vertices (list of lists).


## Running the Backend

1.  **Install required packages:**
    ```bash
    pip install Flask
    ```
2.  **Add your pre-trained models to the project folder:** Ensure that the necessary files and weights for the `car_classification` and image segmentation models are correctly referenced in the corresponding Python files (`car_classification.py`, `img_to_segments.py`).  **Crucially, make sure the required files are in the correct places, so the Python code can find them.**
3.  **Run the Flask application:**
    ```bash
    python app.py
    ```

This will start the Flask development server.  You can then access the API endpoints through your web browser or a tool like `curl`.

## Error Handling

The backend includes error handling to catch exceptions during image processing and return appropriate HTTP status codes to the client.  The `processing_status` dictionary is crucial for communicating the progress and any issues to the front-end.  Detailed error messages will be included in the response.

## Important Considerations

* **Temporary Files:** The code creates temporary directories (`img`, `seg_img`) and files. Ensure you have sufficient disk space. The code includes cleanup mechanisms to remove temporary files after processing.
* **Model Dependencies:**  Ensure that all the necessary dependencies for the segmentation and classification models are installed and accessible.
* **Image Formats:** The backend currently handles PNG image files.  Adapt the code for other formats if required.
* **Concurrency:**  For higher load, consider implementing multithreading or asynchronous processing to avoid blocking the server.
* **Image Size:** Be mindful of image sizes, potentially using resizing or compression techniques if necessary.
* **File Permissions:** Ensure that the application has write access to the `img` and `seg_img` directories.



This README provides a comprehensive overview of the project.  Remember to replace placeholder comments with actual implementation details and ensure all dependencies are properly set up.