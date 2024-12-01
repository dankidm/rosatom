print("Booting up the backend...\nPlease, don't forget to add the weights and latest checkpoint to the project folder!\n")

import os.path
from os.path import exists

from flask import Flask, request, jsonify
import base64
import hashlib

from cv.cartype_classification import get_car_type
from cv.img_to_segments import img_to_segments
from cv.poligons_from_seg import image_to_polygon_vertices
from cv.segment_inference import interface_start


app = Flask(__name__)

processing_status = {} # Uploaded Processing Ready or Error
processed_segments = {}

if not os.path.exists("img"):
    os.mkdir("img")
if not os.path.exists("seg_img"):
    os.mkdir("seg_img")

def get_segments_from_image(output_file, image_hash, path):
    # return image_to_polygon_vertices(output_file)
    return img_to_segments(output_file, image_hash, path)

def process_image(image_hash, image_data):
    processing_status[image_hash] = "Processing"
    try:
        initial_file = os.path.join("img", f"{image_hash}.png")
        initial_file_split = os.path.join("img", f"{image_hash}_split.png")
        seg_dir = os.path.join("seg_img", image_hash)

        # Save initial image
        with open(initial_file, "wb") as file:
            file.write(image_data)

        # Ensure the segmentation directory exists
        os.makedirs(seg_dir, exist_ok=True)

        processed_segments[image_hash] = {}
        processed_segments[image_hash]["Type"] = get_car_type(initial_file)

        # Start processing
        interface_start(initial_file, initial_file_split)

        # Process and store segments
        img_to_segments(initial_file_split, image_hash, seg_dir)


        for segment_file_name in os.listdir(seg_dir):
            segment_path = os.path.join(seg_dir, segment_file_name)
            processed_segments[image_hash][segment_file_name] = image_to_polygon_vertices(segment_path)


        # Cleanup temporary files and directory
        for segment_file_name in os.listdir(seg_dir):
            os.remove(os.path.join(seg_dir, segment_file_name))
        os.rmdir(seg_dir)

        os.remove(initial_file)
        os.remove(initial_file_split)

        processing_status[image_hash] = "Ready"
    except Exception as e:
        processing_status[image_hash] = "Error"
        print(f"Exception occurred when processing image {image_hash}: {e}")


# POST "/" - загрузка изображения и начало обработки
@app.route('/', methods=['POST'])
def upload_image():
    try:
        data = request.json
        base64_image = data.get('image', '')

        if not base64_image:
            return jsonify({'error': 'No image provided'}), 400

        image_data = base64.b64decode(base64_image)
        image_hash = hashlib.sha256(image_data).hexdigest()

        if image_hash in processed_segments:
            return jsonify({'message': f"Image already calculated. just use it",'image_hash':image_hash}), 200

        processing_status[image_hash] = "Uploaded"
        process_image(image_hash, image_data)

        return jsonify({'message': 'Image uploaded successfully', 'image_hash':image_hash}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# @app.route('/', methods=['POST'])
# def upload_image():
#     try:
#         data = request.json
#         image_path = data.get('image_path', '')
#
#         if not image_path or not os.path.isfile(image_path):
#             return jsonify({'error': 'Invalid or missing image path'}), 400
#
#         with open(image_path, 'rb') as img_file:
#             image_data = img_file.read()
#
#         image_hash = hashlib.sha256(image_data).hexdigest()
#
#         if image_hash in processed_segments:
#             return jsonify({'message': f"Image already calculated. Just use it", 'image_hash': image_hash}), 200
#
#         processing_status[image_hash] = "Uploaded"
#         process_image(image_hash, image_data)
#
#         return jsonify({'message': 'Image uploaded successfully', 'image_hash': image_hash}), 200
#
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# GET "/" - возвращает все созданные идентификаторы
@app.route('/', methods=['GET'])
def get_image():
    output = list()
    for i in processing_status:
        output.append(i)
    return jsonify(output), 200


# GET "/<id>/status" - статус обработки
@app.route("/<image_id>/status", methods=["GET"])
def get_status(image_id):
    if image_id not in processing_status:
        return jsonify({"error": "Image ID not found"}), 404

    return jsonify({"status": processing_status[image_id]})


# GET "/<id>/segments" - сегменты изображения
@app.route("/<image_id>/segments", methods=["GET"])
def get_segments(image_id):
    if image_id not in processed_segments:
        if image_id in processing_status and processing_status[image_id] == "processing":
            return jsonify({"error": "Processing not completed yet"}), 400
        return jsonify({"error": "Image ID not found"}), 404
    return jsonify({"segments": processed_segments[image_id]})


if __name__ == '__main__':
    app.run(debug=True)