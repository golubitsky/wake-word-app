from flask import (
    Flask,
    jsonify,
    render_template,
    request
)

from src.load_image import image_from_http_form
from src.keras_inference import predict

app = Flask(__name__)


@app.route('/prediction', methods=['POST'])
def prediction():
    with image_from_http_form(request.files['file']) as image:
        return jsonify({
            'prediction': predict(image)
        })


@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
