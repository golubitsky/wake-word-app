import uuid
import os

from flask import (
    Flask,
    jsonify,
    render_template,
    request
)

from src.load_image import read_image_file
from src.keras_inference import predict

app = Flask(__name__)


@app.route('/prediction', methods=['POST'])
def prediction():
    temp_path = f'/tmp/{str(uuid.uuid4())}'

    request.files['file'].save(temp_path)
    prediction = predict(read_image_file(temp_path))

    os.remove(temp_path)

    return jsonify({
        'prediction': prediction
    })


@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
