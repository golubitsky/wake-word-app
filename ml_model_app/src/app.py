import uuid
import os

from flask import (
    Flask,
    render_template,
    request
)

from src.load_image import read_image_file
from src.keras_inference import predict

app = Flask(__name__)


def response_for_post():
    temp_path = f'/tmp/{str(uuid.uuid4())}'

    request.files['file'].save(temp_path)
    prediction = predict(read_image_file(temp_path))

    os.remove(temp_path)

    return render_template('result.html', prediction=prediction)


@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        return response_for_post()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
