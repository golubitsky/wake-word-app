from src.app import app
import re
import json


def test_root():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert re.search(r'Upload a picture', str(response.data)) is not None


def test_prediction():
    image = open("/app/ml_model_app/samples/4_sample_1.png", "rb")
    data = dict(
        file=(image, 'file'),
    )

    response = app.test_client() \
        .post('/prediction', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert json.loads(response.get_data()) == {'prediction': 4}
