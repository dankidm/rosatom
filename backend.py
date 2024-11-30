from flask import Flask, request, jsonify
import base64
import asyncio
import hashlib

app = Flask(__name__)

processing_status = {} # Uploaded Processing Ready or Error
processed_segments = {}


async def getSegmentsFromImage(image_data):
    return 0

async def process_image(image_id, image_data):
    processing_status[image_id] = "Processing"
    try:
        segments = await getSegmentsFromImage(image_data)
        processed_segments[image_id] = segments
        processing_status[image_id] = "Ready"
    except Exception as e:
        processing_status[image_id] = "Error"
        print(f"Exception accured when processing image {image_id}: {e}")


# POST "/" - загрузка изображения и начало обработки
@app.route('/', methods=['POST'])
def upload_image():
    try:
        data = request.json
        base64_image = data.get('image', '')

        if not base64_image:
            return jsonify({'error': 'No image provided'}), 400

        image_data = base64.b64decode(base64_image)
        image_hash = hashlib.sha256(image_data)

        processing_status[image_hash] = "Uploaded"

        asyncio.ensure_future(process_image(image_hash, image_data))

        return jsonify({'message': 'Image uploaded successfully', 'image_hash':image_hash}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
